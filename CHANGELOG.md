# Changelog

## [0.4.1] - 2026-04-14 — 2차 리뷰 반영 (UI 톤다운 · 재시도 통합 · 결정론화)

### Added
- **`chat_json` `temperature` · `retry_on_parse` 파라미터** (`app/llm/openai_client.py`): 재시도 루프에서 temperature=0.3으로 규칙 준수율↑, 외부 루프가 재시도 관리할 때 내부 재시도 중복 방지.
- **race 방어** (`teacher.py::_save_word_to_db`): insert 시 Unique violation(SQL 23505) 발생하면 ilike 재조회로 기존 id 반환.
- **`tests/test_rate_limit.py`** (7개): X-Forwarded-For 우선, X-Real-IP fallback, `_gc_stale` interval/대상, `_allow_paths` 구성.
- **`tests/test_user_state.py`** (3개): `words/today[-count]`가 `words.created_at` 기준 + user_id 미사용 동작 고정.

### Changed
- **UI 전면 Apple 톤다운** (`streamlit_app.py`):
  - 폰트: Google Fonts 제거 → `-apple-system, BlinkMacSystemFont, "SF Pro Text"` 스택
  - 팔레트: 머스터드(#c98a00) 제거 → 잉크(#1d1d1f) + 링크 블루(#0066cc)
  - 배경: radial orb 2개 + 135° grain 제거 → solid `#fbfbfd`
  - 카드: radius 20→12~14, box-shadow 제거, hover 시 hairline만
  - 버튼: 10px → pill(980px), primary(black solid)/secondary(white stroke) 위계
  - 이모지 정리: 탭/헤더/CTA/빈 상태/토스트/완료 배지에서 제거. SM-2 품질 라디오(😵😕🤔🙂😎🎉)와 `st.balloons()`는 기능적 의미로 유지
  - 헤더: `🇩🇪 Deutsch Lab` 로고 → 작은 캡스 `DEUTSCH LAB`
  - 펄스 애니메이션 색: 노랑 → 블루
- **재시도 루프 통합** (`teacher.py::generate_sentences`): 커버리지 검증과 학습 가치 검증을 별도 2회 → **단일 검증기 1회 재시도**로 합침. 최대 LLM 호출 수 5회 → **2회**. 재시도는 temperature=0.3으로.
- **`_build_user_profile` 결정론화** (`teacher.py`): known(`order mastery_score desc`), weak(`order asc`), review_due(`order next_review asc`) + 2차 정렬 `word_id`로 세션 간 안정적인 LLM 프롬프트 보장.
- **`must_include_lemmas` 상한**: 재시도 시 `req.count` 개수를 넘지 않도록 슬라이스 (LLM 과부하 방지).

### Removed
- **미사용 상수/스키마** — `TEACHER_GENERATE_WORDS_PROMPT` (`app/llm/prompts.py`), `GenerateWordsRequest`·`GeneratedWord` (`app/schemas/teacher.py`).

### Tests
- 49 → **60 passed** (신규 10개, 기존 기능 시그니처 변경 대응).

---

## [0.4.0] - 2026-04-14 — 학습 가치 강화 & 5축 정비

### Added
- **학습 가치 룰** (`teacher.py`): 모든 문장이 (review_due 단어 OR 신규 단어) 최소 1개를 포함하도록 백엔드 검증 + 1회 재시도. 응답에 `learning_value: {total, valuable, valueless_indices}` 메타.
- **SM-2 재등장 보장 루프** (`teacher.py`): review_due 커버리지 < min(len, 3)이면 `must_include_lemmas` 주입해 1회 재시도. 응답에 `review_coverage` 메타.
- **신규 단어 embedding 자동 생성** (`teacher.py::_save_word_to_db`): `lemma (pos): translation` 포맷으로 임베딩 입력 구성 (동음이의 구분력 향상).
- **`/recommend/today` `sentence_practice` 블록**: 대시보드 최상단 "📝 오늘의 문장 연습 준비 완료" CTA의 데이터 소스.
- **`tests/test_teacher.py`** (8개): `_extract_used_lemmas`, `_save_word_to_db` (3 케이스), `generate_sentences` 재등장/학습가치 루프.
- **`tests/test_sm2.py`** parametrize 확장 (9개 → 11개): quality 경계, ease_factor 방향성, EF 하한 1.3.

### Changed
- **`/teacher/generate-sentences` 정책 변경**: 신규 단어를 `user_word_state`에 자동 등록하지 않음. 복습 큐 등록은 사용자 클릭(`/user-state/words/mark`) 시점에만.
- **`/user-state/words/today[-count]` 의미 변경**: `user_word_state.created_at` → `words.created_at`. 오늘 DB에 새로 추가된 단어를 카운트.
- **탭 순서 재배치**: `📝 문장 학습`(기본) → `대시보드` → `시나리오` → `문법` → `검색`.
- **`chat_json` 견고화** (`openai_client.py`): `response_format={"type": "json_object"}` + JSON 파싱 실패 시 1회 재시도.
- **프롬프트 정리** (`prompts.py::TEACHER_GENERATE_SENTENCES_PROMPT`): `blanked`/`hint` 필드 제거, is_new "정확히 1개" → "최대 1개", 학습 가치 룰을 최상위 강제 룰로 명시.
- **Supabase 클라이언트 싱글톤** (`supabase_client.py`): `lru_cache(maxsize=1)`로 매 호출 재생성 제거.
- **N+1 쿼리 제거** (`teacher.py::generate_sentences`): 모든 lemma를 단일 `in_()` 쿼리로 선조회 후 캐시.
- **레이트 제한 강화** (`rate_limit.py`): X-Forwarded-For/X-Real-IP 우선, 5분 stale IP GC.
- **시나리오 평가 UI**: selectbox → 이모지 라디오 (😵 😕 🤔 🙂 😎 🎉), quality≥4면 `st.balloons()`. 중첩 expander 평탄화.
- **문장 카드 UI**: `.sentence-card` div 경계, 동적 iframe 높이, 단어 클릭 펄스 애니메이션, `st.toast` 피드백, "📋 시나리오로" 라벨화.
- **대시보드 UI**: "목록 보기"를 `st.expander`로 (전체 rerun 방지), 격려형 빈 상태 문구, 에러 시 ⚠️ 표시.

### Removed
- **`POST /teacher/generate-words` 엔드포인트**: 단어 리스트 학습은 문장 중심 철학과 충돌 → 제거. `TEACHER_GENERATE_WORDS_PROMPT`/`GenerateWordsRequest`는 미사용.
- **프롬프트의 `blanked`/`hint` 필드**: 빈칸 연습 폐지 정책과 일치시킴.

### Removed (이전 정리)
- 미사용 라우터 4개: `coach.py`, `features.py`, `achievements.py`, `transfer.py` + 동반 스키마.

## [0.3.0] - 2026-02-26 — 문장 중심 학습 시스템

### Added
- **`SentenceWord` / `VerbConjugation` 스키마** (`app/schemas/teacher.py`)
  - 문장 내 단어 메타데이터 (품사, 성, 복수형, 신규 여부, DB id)
  - 동사 현재형 변화표 (6인칭 dict)
  - `GeneratedSentence`에 `words`, `verbs` 필드 추가
- **`POST /user-state/words/mark`** (`app/routers/user_state.py`)
  - 단어 복습 표시 엔드포인트 (idempotent — 이미 상태 있으면 무시)
  - body: `{user_id, word_id}` → `user_word_state` upsert
- **신규 단어 자동 저장** (`app/routers/teacher.py`)
  - `POST /teacher/generate-sentences` 응답 후처리:
    - `is_new: true` 단어를 `words` 테이블에 자동 INSERT
    - 이미 있으면 기존 id 조회 후 `word_id` 주입
    - `weak_word_lemmas` 프롬프트 입력 추가
- **`docs/learning-design.md`** — 문장 중심 학습 설계 문서 (living document)
  - 학습 철학, 핵심 플로우, 데이터 모델, UI 규칙, TODO

### Changed
- **`TEACHER_GENERATE_SENTENCES_PROMPT`** (`app/llm/prompts.py`)
  - `words[]` / `verbs[]` JSON 출력 포맷 명세 추가
  - `weak_word_lemmas` 입력 필드 추가 (취약 단어 문장에 포함)
- **AI 선생님 "문장 연습" 탭 전면 개편** (`streamlit_app.py`)
  - 문장 카드: 독일어 + 한국어 번역 + 문법 포인트
  - 동사 변화표: HTML `<table>` 3행 구조
  - 단어 멀티셀렉트: 신규 단어 🆕 표시, "단어 표시하기" 버튼
  - 생성된 문장 `session_state` 캐시 (재렌더링 방지)
- **라이트 테마 UI 전면 적용** (`streamlit_app.py`)
  - 배경: 다크 네이비 → 밝은 파스텔 블루/민트 그라디언트
  - 텍스트: `#f6f2ea` (크림) → `#1a2340` (다크 네이비)
  - 강조색: `#f4c767` (노랑) → `#c98a00` (앰버, 흰 배경 가독성)
  - 사이드바: 어두운 반투명 → 흰색
  - 입력 필드: 어두운 배경 → 흰색
  - 버튼 텍스트: 어둠 → 흰색
- **`CLAUDE.md`**: 설계 문서 참조 섹션 추가

---

## [0.2.0] - 2026-02-26 — 대화 중심 학습 + AI Teacher

### Added
- SM-2 파라미터 조정 (interval_days 6→3, ease_factor 기본값 2.5→2.7)
- `user_word_state`: `success_count`, `fail_count` 필드
- `user_scenario_state`: SM-2 필드 추가
- `POST /study/review-word` — DB 직접 업데이트 + success/fail_count 자동 처리
- `GET /recommend/weak-words` 엔드포인트
- `/recommend/today` — scenarios 포함, adaptive 난이도
- `POST /scenarios/{id}/practice` — SM-2 기반 연습 완료 기록
- **AI Teacher** (`app/routers/teacher.py`):
  - `POST /teacher/generate-words` — 사용자 프로필 기반 맞춤 단어 생성
  - `POST /teacher/generate-sentences` — 취약 문법 집중 문장 생성
  - `POST /teacher/chat` — 히스토리 기반 개인화 대화
- Streamlit: Scenarios 탭, Dashboard 취약 단어 표시, AI Teacher 탭

---

## [0.1.0] - 초기 구현

- FastAPI 백엔드 (18개 라우터)
- Supabase 연동 (PostgreSQL + pgvector)
- SM-2 간격 반복 알고리즘
- 80/20 추천 로직
- 벡터 유사도 검색
- Streamlit 웹 UI
- OpenAI 연동 (번역, 임베딩, LLM)
