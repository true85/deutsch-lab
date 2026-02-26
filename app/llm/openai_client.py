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


def chat_json(system_prompt: str, user_prompt: str, model: str | None = None):
    client = get_client()
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model_name,
        temperature=0.4,
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
    content = response.choices[0].message.content or "{}"
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw": content}
