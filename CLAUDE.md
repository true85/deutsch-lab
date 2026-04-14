# Deutsch Lab - CLAUDE.md

## 프로젝트 개요
한국인 학습자용 독일어 학습 관리 시스템 (LMS)
- **백엔드**: FastAPI (포트 8010)
- **프론트엔드**: Streamlit
- **DB**: Supabase (PostgreSQL + pgvector)
- **LLM**: OpenAI (gpt-5.2)

## 실행 명령어

```bash
# 백엔드
uvicorn app.main:app --reload --port 8010

# 프론트엔드
streamlit run streamlit_app.py

# 테스트
pytest
```

## 환경변수

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `SUPABASE_URL` | ✅ | - | Supabase 프로젝트 URL |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ | - | Service Role Key (또는 ANON_KEY) |
| `SUPABASE_ANON_KEY` | - | - | Anon Key (대안) |
| `OPENAI_API_KEY` | - | - | OpenAI API 키 |
| `OPENAI_MODEL` | - | `gpt-5.2` | 사용할 모델 |
| `API_KEY` | - | - | 미설정 시 인증 스킵 (개발 모드) |
| `RATE_LIMIT_PER_MIN` | - | `120` | 분당 요청 제한 |

## 아키텍처

```
app/
├── main.py               # FastAPI 앱 진입점
├── routers/              # 14개 API 라우터
│   ├── words.py          # 단어 CRUD + 학습 상태
│   ├── grammar.py        # 문법 CRUD + 학습 상태
│   ├── expressions.py    # 표현 CRUD + 학습 상태
│   ├── scenarios.py      # 시나리오 CRUD + 학습 상태
│   ├── recommend.py      # 80/20 규칙 기반 추천 (인증 필요)
│   ├── study.py          # SM-2 기반 복습 세션 (인증 필요)
│   ├── user_state.py     # 사용자 학습 진도 (인증 필요)
│   ├── search.py         # 벡터 유사도 검색
│   ├── llm.py            # LLM 기능 (번역, 예문 생성 등)
│   ├── teacher.py        # AI 선생님 (단어/문장 생성, 대화)
│   └── ...
├── schemas/              # Pydantic 스키마 (입출력 검증)
│   └── teacher.py        # AI Teacher 요청/응답 스키마
├── services/
│   ├── sm2.py            # SM-2 간격 반복 알고리즘
│   └── streaks.py        # 연속 학습 날짜 계산
├── middleware/
│   ├── auth.py           # API 키 인증
│   ├── rate_limit.py     # 레이트 제한
│   └── logging.py        # 요청 로깅
└── llm/
    ├── openai_client.py  # OpenAI 클라이언트 (chat_json, get_embedding)
    ├── prompts.py        # 프롬프트 템플릿
    └── usage_tracker.py  # 토큰 사용량 추적
streamlit_app.py          # Streamlit 웹 UI
```

## 코드 패턴 / 컨벤션

### API 응답 포맷
```python
# 성공
{"status": "ok", "data": {...}}

# 오류
{"status": "error", "detail": "오류 메시지"}
```

### 네이밍
- 변수/함수명: `snake_case`
- private 헬퍼 함수: `_` prefix (예: `_calculate_next_review`)
- 타입 힌트 필수

### Supabase 쿼리 패턴
```python
result = supabase.table("words") \
    .select("*") \
    .eq("level", level) \
    .limit(10) \
    .execute()
```

### 벡터 검색 (RPC 함수 사용)
```python
result = supabase.rpc("match_words", {
    "query_embedding": embedding,
    "match_threshold": 0.8,
    "match_count": 10
}).execute()
```

### 인증 의존성
```python
# 인증이 필요한 엔드포인트
@router.get("/endpoint")
async def endpoint(user_id: str = Depends(verify_api_key)):
    ...
```

## 핵심 알고리즘

### SM-2 간격 반복 (`app/services/sm2.py`)
복습 품질(0-5) 기반으로 다음 복습 일정 계산:
- 품질 < 3: 즉시 재복습
- 품질 ≥ 3: ease factor 업데이트 후 간격 연장

### 연속 학습 스트릭 (`app/services/streaks.py`)
- 오늘 학습 여부 및 연속 일수 계산
- UTC 기준 날짜 처리

### 80/20 추천 (`app/routers/recommend.py`)
- 신규 콘텐츠 20% + 복습 필요 콘텐츠 80% 비율로 추천

### AI 선생님 (`app/routers/teacher.py`)
- `_build_user_profile(user_id)`: 공통 헬퍼 — 레벨/mastery/known_lemmas/weak_lemmas/weak_grammar/review_due_lemmas 조회
- `POST /teacher/generate-sentences`: 취약 문법 + 복습 예정 단어 집중 문장 생성
  - 매 요청마다 `session_theme`(랜덤) + `random_seed` 주입 → 다양한 문장 보장
  - **통합 검증 루프**: 커버리지(review_due ≥ min(len,3))와 학습 가치(모든 문장에 review_due 또는 신규 단어 1개)를 **단일 validator로 합쳐** 최대 1회 재시도. 재시도는 `temperature=0.3` + `must_include_lemmas[:count]` 상한. 총 LLM 호출은 최대 **2회**.
  - 신규 단어는 `words` 테이블에 자동 저장 + embedding 자동 생성 (`get_embedding`은 lemma+pos+translation 포맷)
  - **신규 단어를 `user_word_state`에 자동 등록하지 않음** — 복습 큐는 사용자 클릭 시점에만 채워짐
  - `blanked`/`hint` 빈칸 연습 없음
  - 응답 메타: `review_coverage`, `learning_value` 포함
- `POST /teacher/generate-grammar`: 레벨별 문법 규칙 일괄 생성 (중복 제외 후 DB 저장)
- `POST /teacher/generate-scenario`: 상황 기반 대화 시나리오 생성 (옵션 저장)
- `POST /teacher/chat`: 히스토리 기반 개인화 대화 (free/correction/vocab_drill 모드)
- 취약 판별 기준: `mastery_score < 0.5`
- LLM 호출: `chat_json(system, user, temperature=0.7, retry_on_parse=True)` — `response_format=json_object`. `retry_on_parse=False`로 외부 루프가 재시도 관리 시 내부 재시도 비활성화 가능.
- **`_build_user_profile` 결정론**: known(mastery desc), weak(mastery asc), review_due(next_review asc) + 2차 정렬 `word_id`로 세션 간 안정적 샘플링.

### Supabase 클라이언트
- `get_supabase_client()` — `lru_cache(maxsize=1)`로 싱글톤. 매 요청 재생성 방지

### 레이트 제한 (`app/middleware/rate_limit.py`)
- IP 추출 우선순위: `X-Forwarded-For` (좌측) → `X-Real-IP` → `request.client.host`
- 5분마다 stale IP GC로 메모리 누수 방지
- 멀티 워커 환경에서는 워커별 카운터 → 단일 워커 권장 (또는 Redis 백엔드 도입)

## 주요 DB 테이블

### 콘텐츠 테이블
| 테이블 | 설명 |
|--------|------|
| `words` | 단어 (level, embedding 포함) |
| `grammar` | 문법 패턴 |
| `expressions` | 표현/구문 |
| `scenarios` | 대화 시나리오 |
| `expression_words` | expressions ↔ words 중간 테이블 |

### 학습 진도 테이블
| 테이블 | 설명 |
|--------|------|
| `user_word_state` | 단어별 SM-2 상태 (mastery_score, next_review 포함) |
| `user_grammar_state` | 문법별 SM-2 상태 |
| `user_expression_state` | 표현별 SM-2 상태 |
| `user_scenario_state` | 시나리오별 SM-2 상태 |

### 단어 학습 관련 엔드포인트
| 엔드포인트 | 설명 |
|-----------|------|
| `POST /user-state/words/mark` | 단어 복습 등록 (idempotent upsert). UI 단어 클릭 시 호출 |
| `POST /user-state/words/unmark` | 단어 복습 삭제 (user_id + word_id) |
| `GET /recommend/weak-words` | mastery 낮은 순 취약 단어 목록 |
| `GET /user-state/words/today` | 오늘 `words` 테이블에 추가된 신규 단어 목록 (lemma 기준) |
| `GET /user-state/words/today-count` | 위 목록의 카운트 |
| `GET /recommend/today` | 오늘 학습 번들 — `sentence_practice` 블록 포함 (대시보드 CTA) |

## 주의사항

- **개발 모드**: `API_KEY` 환경변수 미설정 시 인증 검사 스킵
- **레이트 제한 화이트리스트**: `/health`, `/docs`, `/redoc` 경로는 제한 없음
- **pgvector 인덱스 선택**:
  - 대용량 정적 데이터: `ivfflat`
  - 빈번한 업데이트: `hnsw`
- **Embedding 생성**: 콘텐츠 추가 시 OpenAI text-embedding-ada-002 사용

## 설계 문서

기능 계획 / 구현 전 반드시 읽을 것:

- `docs/learning-design.md` — 문장 중심 학습 시스템 핵심 설계
  (학습 철학, 데이터 흐름, UI 규칙, TODO 포함)
  새 기능 추가 또는 기존 기능 수정 시 이 문서를 먼저 확인하고,
  설계가 바뀌면 반드시 이 문서도 함께 업데이트한다.

## 검증

```bash
# 테스트 실행 (60개 통과 확인)
pytest

# 헬스 체크
curl http://localhost:8010/health

# API 문서 확인
open http://localhost:8010/docs
```
