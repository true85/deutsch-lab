import json
import logging
import os

from openai import OpenAI

from app.llm.usage_tracker import record_usage


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")
    return OpenAI(api_key=api_key)


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    client = get_client()
    response = client.embeddings.create(input=text, model=model)
    try:
        usage = response.usage
        if usage:
            record_usage(model, usage)
    except Exception:
        logging.getLogger("app.llm").warning("Usage tracking failed for embedding")
    return response.data[0].embedding


def _chat_once(client, model_name: str, system_prompt: str, user_prompt: str, temperature: float) -> str:
    response = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    try:
        usage = response.usage
        if usage:
            record_usage(model_name, usage)
    except Exception:
        logging.getLogger("app.llm").warning("Usage tracking failed")
    return response.choices[0].message.content or "{}"


def chat_json(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
    temperature: float = 0.7,
    retry_on_parse: bool = True,
):
    client = get_client()
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-5.2")
    content = _chat_once(client, model_name, system_prompt, user_prompt, temperature)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        if not retry_on_parse:
            logging.getLogger("app.llm").warning("chat_json: JSON parse failed (retry disabled)")
            return {"raw": content}
        logging.getLogger("app.llm").warning("chat_json: first JSON parse failed, retrying")
        retry_system = system_prompt + "\n\nCRITICAL: Return ONLY a single valid JSON object. No markdown, no code fences, no commentary."
        content = _chat_once(client, model_name, retry_system, user_prompt, temperature)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logging.getLogger("app.llm").error("chat_json: retry failed, returning raw")
            return {"raw": content}
