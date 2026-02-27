# 문장 중심 학습 시스템 설계

> Living document — 기능 추가/수정 시 이 문서도 함께 업데이트한다.

## 학습 철학

**"문장이 핵심 학습 단위다."**

- 단어·문법·시나리오를 따로 외우는 대신, 실제 문장 안에서 자연스럽게 습득
- 알고 있는 단어 위에 소수의 새 단어를 얹어 인지 부하를 최소화
- 취약 문법/단어를 자동으로 문장에 반영해 반복 노출

## 핵심 플로우

```
[사용자] "문장 생성하기"
        ↓
[API] POST /teacher/generate-sentences
  - _build_user_profile(user_id)
      → current_level, known_lemmas, weak_word_lemmas, weak_grammar_rules
  - LLM 호출 (TEACHER_GENERATE_SENTENCES_PROMPT)
      → sentences[]: german, korean, grammar_focus, blanked, hint, words[], verbs[]
  - is_new 단어 자동 DB 저장 (words 테이블)
  - 각 단어에 word_id 주입
        ↓
[UI] 문장 카드 렌더링
  - 독일어 문장 + 한국어 번역
  - 문법 포인트 표시
  - 빈칸 연습 (blanked + hint)
  - 동사 변화표 (현재형 HTML 테이블)
  - 단어 멀티셀렉트 → "단어 표시하기"
        ↓
[API] POST /user-state/words/mark  (user_id, word_id)
  - 이미 상태 있으면 무시 (idempotent)
  - 없으면 mastery_score=0.0으로 생성
        ↓
[다음 문장 생성]
  - weak_word_lemmas에 표시한 단어 포함
  - 해당 단어가 새 문장에 자연스럽게 등장
```

## 데이터 모델

### LLM 응답 스키마 (`GeneratedSentence`)

| 필드 | 타입 | 설명 |
|------|------|------|
| `german` | str | 전체 독일어 문장 |
| `korean` | str | 한국어 번역 |
| `grammar_focus` | str | 집중 문법 규칙 이름 |
| `blanked` | str \| None | 빈칸 연습용 문장 |
| `hint` | str | 빈칸 힌트 (한국어) |
| `words` | list[SentenceWord] | 문장 내 의미 단어 목록 |
| `verbs` | list[VerbConjugation] | 동사 현재형 변화표 |

### `SentenceWord`

| 필드 | 설명 |
|------|------|
| `german` | 원형(lemma) 또는 문장에 등장한 형태 |
| `translation` | 한국어 번역 |
| `part_of_speech` | verb \| noun \| adjective \| adverb \| other |
| `gender` | 명사만 (der/die/das) |
| `plural` | 복수형 |
| `is_new` | known_lemmas에 없으면 true (문장당 최대 2개) |
| `word_id` | DB에 저장된 id (후처리로 주입) |

### `VerbConjugation`

| 필드 | 설명 |
|------|------|
| `lemma` | 동사 원형 |
| `present` | 인칭별 현재형 dict (6개 인칭) |

## UI 규칙

1. **동사 변화표**: HTML `<table>` 로 3행 2열(인칭+형태) 구조
2. **신규 단어**: 멀티셀렉트 레이블에 🆕 표시
3. **단어 표시하기**: `POST /user-state/words/mark` 호출 — idempotent

## TODO

- [ ] 복습 스케줄링: 표시된 단어의 SM-2 `next_review` 기반 재등장 보장
- [ ] 문장 즐겨찾기: 마음에 드는 문장 저장 (`user_sentence_favorites` 테이블)
- [ ] 듣기 연습: TTS 통합 (독일어 문장 음성 재생)
- [ ] 쓰기 연습: 빈칸에 직접 입력 후 정답 확인 (클라이언트 사이드)
- [ ] 신규 단어 embedding: 저장 시 OpenAI embedding 자동 생성
