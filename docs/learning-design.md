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
      → current_level, known_lemmas, weak_word_lemmas, weak_grammar_rules, review_due_lemmas
  - random session_theme 선택 (12개 테마 중 랜덤) + random_seed 생성
      → 매 요청마다 다른 문장 생성 보장
  - LLM 호출 (TEACHER_GENERATE_SENTENCES_PROMPT, model=gpt-5.2, temperature=0.7)
      → sentences[]: german, korean, grammar_focus, words[], verbs[]
  - is_new 재검증 (known_lower 세트로 LLM 실수 보정)
  - is_new 단어 자동 DB 저장 (words 테이블) + word_id 주입
  - is_new 단어 user_word_state 자동 upsert (mastery=0, ignore_duplicates)
        ↓
[UI] 문장 카드 렌더링
  - 독일어 문장 (단어 클릭으로 mark/unmark 토글)
  - 한국어 번역
  - 문법 포인트 표시
  - 동사 변화표 (현재형 HTML 테이블)
        ↓
[인라인 클릭] 단어 클릭 시
  - 하이라이트 ON → POST /user-state/words/mark
  - 하이라이트 OFF → POST /user-state/words/unmark
  - localStorage로 상태 유지 (페이지 새로고침 후에도 복원)
        ↓
[다음 문장 생성]
  - review_due_lemmas에 표시한 단어 포함
  - 해당 단어가 새 문장에 자연스럽게 등장
```

## 다양성 보장 메커니즘

`generate_sentences`는 매 요청마다 다음을 주입한다:

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `session_theme` | 12개 테마 중 랜덤 선택 | "카페/식당", "여행", "건강/병원" 등 |
| `random_seed` | 타임스탬프 + 난수 | "20260305093412847" |

프롬프트 규칙:
- 각 문장마다 **다른 문법 규칙** 사용 (weak_grammar_rules 순환)
- 각 문장마다 **다른 동사/주어/상황** — 반복 금지
- 모든 문장이 `session_theme` 기반

## 데이터 모델

### LLM 응답 스키마 (`GeneratedSentence`)

| 필드 | 타입 | 설명 |
|------|------|------|
| `german` | str | 전체 독일어 문장 |
| `korean` | str | 한국어 번역 |
| `grammar_focus` | str | 집중 문법 규칙 이름 |
| `words` | list[SentenceWord] | 문장 내 의미 단어 목록 |
| `verbs` | list[VerbConjugation] | 동사 현재형 변화표 |

> `blanked` / `hint` 필드는 제거됨 (빈칸 연습 기능 폐지)

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
2. **단어 클릭**: 인라인 HTML+JS로 렌더링, 클릭 시 mark/unmark 토글
3. **취약 단어 삭제**: 대시보드에서 ✕ 버튼 클릭 → `POST /user-state/words/unmark` → 목록에서 즉시 제거
4. **is_new 단어**: 문장 생성 시 백엔드에서 자동으로 `user_word_state` upsert (사용자 클릭 불필요)

## 취약 단어 관리

| 동작 | 엔드포인트 | 설명 |
|------|-----------|------|
| 단어 마킹 | `POST /user-state/words/mark` | 복습 대상으로 등록 (idempotent) |
| 마킹 해제 | `POST /user-state/words/unmark` | user_word_state 행 삭제 |
| 취약 단어 조회 | `GET /recommend/weak-words` | mastery 낮은 순 정렬 |

## TODO

- [ ] 복습 스케줄링: 표시된 단어의 SM-2 `next_review` 기반 재등장 보장
- [ ] 문장 즐겨찾기: 마음에 드는 문장 저장 (`user_sentence_favorites` 테이블)
- [ ] 듣기 연습: TTS 통합 (독일어 문장 음성 재생)
- [ ] 신규 단어 embedding: 저장 시 OpenAI embedding 자동 생성
