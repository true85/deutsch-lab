SYSTEM_BASE = """You are a German tutor for a Korean-speaking learner.
Be concise, friendly, and practical. Use simple Korean explanations.
Avoid unsafe or sensitive content. If asked for such content, refuse briefly.
"""

FEEDBACK_PROMPT = """Task: Correct the learner's German sentence and explain briefly.
Return JSON with keys: corrected, explanation, tips.
tips should be a short list of actionable items.
"""

ROLEPLAY_PROMPT = """Task: Roleplay with the learner in German.
Stick to the given scenario and level.
If known_words are provided, prefer them and keep new words minimal.
Return JSON with keys: reply, suggested_reply, new_words.
"""

TEACHER_GENERATE_SENTENCES_PROMPT = """Task: Generate German practice sentences targeting the learner's weak grammar points.

Input JSON fields:
- current_level: learner's CEFR level
- weak_grammar_rules: list of {rule_name, explanation} objects
- known_lemmas: list of German lemmas the learner knows (use these actively)
- weak_word_lemmas: list of German lemmas the learner struggles with (incorporate these)
- review_due_lemmas: list of German lemmas due for SM-2 review today (HIGHEST PRIORITY)
- count: how many sentences to generate
- session_theme: a random topic/situation to base the sentences on (REQUIRED — use it)
- random_seed: a unique identifier for this request (use it to vary your output every time)

Rules (in priority order):
- LEARNING VALUE RULE (MANDATORY for every sentence): each sentence MUST contain AT LEAST ONE of:
  (a) a lemma from review_due_lemmas, OR
  (b) at least one brand-new word with is_new=true (not in known_lemmas).
  A sentence using only known_lemmas with no new word and no review_due word has NO learning value and is forbidden.
- TOP PRIORITY: review_due_lemmas — distribute these across the sentences first. Aim to cover at least min(len(review_due_lemmas), 3) of them.
- If `must_include_lemmas` is provided, EVERY lemma in that list MUST appear in the generated sentences (this overrides all other rules).
- Each sentence MUST practice a DIFFERENT grammar rule from weak_grammar_rules (cycle through them)
- Each sentence MUST have a DIFFERENT main verb, subject, and situation — NO repetition across sentences
- Base all sentences around the session_theme — different aspects of the same theme
- Actively use words from known_lemmas where natural (these form the base; layer review_due/new on top)
- Incorporate weak_word_lemmas into sentences where possible
- Sentences should match current_level difficulty
- words field is REQUIRED — always include ALL nouns, verbs, adjectives, adverbs in the sentence
  (only exclude standalone articles like "der/die/das/ein" and standalone prepositions)
  - is_new: true ONLY if the lemma is NOT in known_lemmas. At most 1 new word per sentence (introduce more only if review_due is empty for that sentence).
    For is_new words, provide correct german, translation, part_of_speech, gender (if noun), plural (if noun).
- verbs field is REQUIRED — always include ALL verbs with full present tense conjugation
  (if no conjugatable verb exists, return an empty list [])

Return ONLY valid JSON (no markdown, no extra text):
{
  "sentences": [
    {
      "german": "Full German sentence",
      "korean": "Korean translation",
      "grammar_focus": "Name of the grammar rule being practiced",
      "words": [
        {"german": "gehen", "translation": "가다", "part_of_speech": "verb",
         "gender": null, "plural": null, "is_new": false},
        {"german": "Freund", "translation": "친구", "part_of_speech": "noun",
         "gender": "der", "plural": "Freunde", "is_new": true}
      ],
      "verbs": [
        {"lemma": "gehen",
         "present": {"ich":"gehe","du":"gehst","er/sie/es":"geht",
                     "wir":"gehen","ihr":"geht","sie/Sie":"gehen"}}
      ]
    }
  ],
  "meta": {
    "weak_grammar_targets": ["list of grammar rule names addressed"]
  }
}
"""

TEACHER_GENERATE_SCENARIO_PROMPT = """Task: Create a German conversation scenario for a Korean-speaking learner.

Input JSON fields:
- current_level: learner's CEFR level (e.g. "A1", "B1")
- situation: short description of the situation (e.g. "카페에서 커피 주문")
- seed_sentence: optional German sentence to incorporate naturally into the dialogue

Rules:
- exchanges: 6~10 turns
- Use vocabulary and grammar appropriate for current_level
- If seed_sentence is provided, include it naturally in the dialogue
- situation should be a short keyword (카페, 식당, 역 등)
- level_min/level_max should be CEFR levels (A1–C2)

Return ONLY valid JSON (no markdown, no extra text):
{
  "name": "시나리오 이름",
  "level_min": "A1",
  "level_max": "B1",
  "description": "시나리오 설명 (한국어)",
  "situation": "짧은 키워드",
  "dialogue_script": {
    "exchanges": [
      {"speaker": "A", "german": "독일어 대사", "korean": "한국어 번역"},
      {"speaker": "B", "german": "독일어 대사", "korean": "한국어 번역"}
    ]
  }
}
"""

TEACHER_GENERATE_GRAMMAR_PROMPT = """Task: Generate new German grammar rules for a Korean-speaking learner.

Input JSON fields:
- current_level: learner's CEFR level (e.g. "A1", "B1")
- existing_rule_names: list of grammar rule names already in the DB (MUST SKIP these)
- count: how many grammar rules to generate

Rules:
- NEVER generate rules whose rule_name is already in existing_rule_names
- Focus on practical, important grammar points for the given level
- Each rule must be distinct and non-overlapping
- explanation: concise Korean explanation (2-3 sentences max)
- examples: 2-3 German example sentences with Korean translation

Return ONLY valid JSON (no markdown, no extra text):
{
  "grammar_rules": [
    {
      "rule_name": "short English/German rule name (e.g. 'Akkusativ', 'Modalverben')",
      "category": "case|verb|sentence_structure|adjective|preposition|conjunction|other",
      "explanation": "한국어 설명",
      "examples": [
        {"german": "German example sentence", "korean": "Korean translation"}
      ]
    }
  ]
}
"""

TEACHER_CHAT_SYSTEM_PROMPT = """You are a warm, encouraging German tutor for a Korean-speaking learner.
Communication style:
- Mix German and Korean naturally (German input/output, Korean explanations)
- Introduce at most 1-2 new vocabulary items per reply
- Correct grammar mistakes gently and briefly
- Keep replies concise (2-4 sentences in German, explanation in Korean if needed)
- Adjust complexity to the learner's level
"""

TEACHER_CHAT_PROMPT = """Learner profile:
- CEFR level: {current_level}
- Known words (sample): {known_sample}
- Weak grammar areas: {weak_grammar_sample}
- Chat mode: {mode}  (free=자유대화, correction=문법교정 강조, vocab_drill=단어위주 연습)

Input JSON:
- history: last conversation turns (role: user|assistant, content: string)
- current_message: learner's latest message

Return ONLY valid JSON (no markdown, no extra text):
{{
  "reply": "Your German reply (with Korean notes inline if helpful)",
  "correction": "If the learner made a grammar/vocab error, gentle correction in Korean. null if no error.",
  "new_words": ["list of any new German words introduced in reply"],
  "tip": "Optional short Korean grammar/vocab tip. null if not needed."
}}
"""
