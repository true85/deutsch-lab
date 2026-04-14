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
  - random session_theme (12개 중 랜덤) + random_seed
      → 매 요청마다 다른 문장 생성 보장
  - LLM 호출 (TEACHER_GENERATE_SENTENCES_PROMPT, gpt-5.2, temperature=0.7, retry_on_parse=False)
      → sentences[]: german, korean, grammar_focus, words[], verbs[]
  - 통합 검증 루프: 커버리지(review_due ≥ min(len, 3)) AND 학습 가치(각 문장 review_due 또는 신규 단어 1개)를
    단일 validator로 검사. 미충족 시 must_include_lemmas(count 상한) + retry_reason 주입해 1회 재시도
    (temperature=0.3). 재시도가 더 나을 때만 교체. 총 LLM 호출 최대 2회.
  - is_new 재검증 (known_lower 세트로 LLM 실수 보정)
  - 신규 단어를 words 테이블에 저장 (embedding 자동 생성)
  - **신규 단어는 user_word_state에 자동 등록하지 않음** — 사용자가 클릭한 단어만 복습 큐에 들어감
        ↓
[UI] "📝 문장 학습" 탭 (최상단 기본 탭)
  - sentence-card div로 카드 경계 강조
  - 독일어 문장 (단어 클릭으로 mark/unmark 토글, 펄스 애니메이션 피드백)
  - 한국어 번역, 문법 포인트
  - 동사 변화표 (현재형 HTML 테이블)
  - "📋 시나리오로" 버튼 → 시나리오 생성
        ↓
[인라인 클릭] 단어 클릭 시
  - 하이라이트 ON + 펄스 → POST /user-state/words/mark (복습 큐 등록)
  - 하이라이트 OFF → POST /user-state/words/unmark
  - localStorage로 상태 유지
        ↓
[다음 문장 생성]
  - review_due_lemmas (마킹된 단어들) 우선 포함
  - 학습 가치 룰로 매 문장에 새 자극 보장
```

## 응답 메타

`/teacher/generate-sentences` 응답에는 디버그/UI용 메타가 포함됨:

| 필드 | 의미 |
|------|------|
| `review_coverage.target` | 이번 세션에 커버해야 할 review_due 개수 (= min(len, 3)) |
| `review_coverage.actual` | 실제 커버된 개수 |
| `review_coverage.missing` | 누락된 lemma 목록 |
| `learning_value.total` | 생성된 문장 수 |
| `learning_value.valuable` | 학습 가치 룰을 통과한 문장 수 |
| `learning_value.valueless_indices` | 통과 못한 문장 인덱스 |

## 학습 가치 룰

각 문장은 다음 중 **최소 하나**를 반드시 포함해야 한다:

1. `review_due_lemmas`의 단어 (사용자가 마킹한 단어)
2. 신규 단어 (`is_new=true` AND `german.lower() not in known_lemmas`)

둘 다 없는 문장 = "학습 가치 없음" → 백엔드에서 1회 재시도.

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
| `is_new` | known_lemmas에 없으면 true (문장당 최대 1개 권장) |
| `word_id` | DB에 저장된 id (후처리로 주입) |

### `VerbConjugation`

| 필드 | 설명 |
|------|------|
| `lemma` | 동사 원형 |
| `present` | 인칭별 현재형 dict (6개 인칭) |

## UI 규칙 (Apple 톤)

참고 미감: Apple.com / Linear / Vercel — 차분한 무채색, 절제된 액센트, 충분한 여백, 시스템 폰트.

1. **탭 순서**: `문장 학습` (기본) → `대시보드` → `시나리오` → `문법` → `검색` (텍스트만, 이모지 없음)
2. **팔레트**: 잉크(`--ink: #1d1d1f`) + 링크 블루(`--accent-link: #0066cc`)만. 머스터드/그린/오렌지 액센트 없음.
3. **폰트**: `-apple-system, BlinkMacSystemFont, "SF Pro Text"` 스택. 웹폰트 import 금지.
4. **배경**: solid `#fbfbfd`. radial-gradient orb, diagonal grain 금지.
5. **카드**: radius 12~14, box-shadow 없음, hover 시 `border-color` 약간 진해지는 hairline만.
6. **버튼**: pill(radius 980px). primary=잉크 solid (CTA 1곳), secondary=white stroke (기본).
7. **인라인 단어 클릭**: 펄스 애니메이션(`@keyframes wpulse`, 블루 톤) + 하이라이트 + mark API.
8. **iframe 높이**: 문장 길이 기반 동적 계산 (`48 + len//40 * 28`).
9. **시나리오 평가**: 이모지 라디오 (😵 😕 🤔 🙂 😎 🎉) — 기능적 의미가 명확해 유지. quality≥4면 `st.balloons()`.
10. **빈 상태**: 이모지 없이 담백한 muted 문구 ("오늘 복습할 단어가 없습니다.").
11. **에러 상태**: 숫자 자리에 `—` (대시).
12. **신규 단어 처리**: 백엔드에서 `words` 테이블만 저장. 복습 큐 등록은 사용자 클릭 시점에만.

## 단어 상태 관리

| 동작 | 엔드포인트 | 설명 |
|------|-----------|------|
| 단어 마킹 | `POST /user-state/words/mark` | 복습 대상으로 등록 (idempotent) |
| 마킹 해제 | `POST /user-state/words/unmark` | user_word_state 행 삭제 |
| 취약 단어 조회 | `GET /recommend/weak-words` | mastery 낮은 순 정렬 |
| 오늘 추가된 단어 | `GET /user-state/words/today[-count]` | `words.created_at >= today` 기준 |
| 복습 예정 단어 | `GET /study/review-today` | `user_word_state.next_review <= today` |

## 추천 번들

`GET /recommend/today` 응답:

```json
{
  "sentence_practice": {
    "review_due_lemmas": ["...", "..."],
    "ready": true
  },
  "words": [...],
  "expressions": [...],
  "scenarios": [...],
  "meta": {"avg_mastery": 0.6, "current_level": "A1"}
}
```

대시보드는 `sentence_practice.ready=true`일 때 최상단에 "📝 오늘의 문장 연습 준비 완료" CTA 카드를 노출.

## TODO

- [ ] 문장 즐겨찾기: 마음에 드는 문장 저장 (`user_sentence_favorites` 테이블)
- [ ] 듣기 연습: TTS 통합 (독일어 문장 음성 재생)
- [ ] 임베딩 비동기화: `_save_word_to_db`의 `get_embedding`를 백그라운드 태스크로 분리
- [ ] rate_limit Redis 백엔드 (멀티 워커 환경 대비)
