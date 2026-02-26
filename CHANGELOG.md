# Changelog

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
