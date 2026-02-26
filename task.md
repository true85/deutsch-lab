# 작업 계획 - 독일어 학습 시스템

## 규칙
- 작업/범위 변경 시 이 문서를 반드시 업데이트.
- 상태는 정확하고 간단하게 유지.

## 단계별 계획

### Phase 0 - 기반
- [x] Supabase 프로젝트 생성 및 스키마 적용
- [x] `.env`에 Supabase/OpenAI 키 설정
- [x] FastAPI `health`, `supabase-health` 엔드포인트

### Phase 1 - 백엔드 기본 구조
- [x] FastAPI 라우터 구조 정리(`app/routers`)
- [x] 공통 응답/에러 포맷 정의
- [x] 설정 로딩/검증(환경변수 체크)
- [x] 로깅 기본 세팅

### Phase 1 - 핵심 CRUD
- [x] 단어 `POST/GET/PUT/DELETE`
- [x] 문법 `POST/GET/PUT/DELETE`
- [x] 표현 `POST/GET/PUT/DELETE`
- [x] 시나리오 `POST/GET/PUT/DELETE`
- [x] 기본 필터/페이지네이션
- [x] 간단한 검색(필드 기반)

### Phase 2 - 학습 상태
- [x] `user_word_state` CRUD
- [x] `user_grammar_state` CRUD
- [x] `user_expression_state` CRUD
- [x] `user_scenario_state` CRUD
- [x] SM-2 스케줄링 헬퍼
- [x] 오늘 복습 목록 조회 API

### Phase 3 - 문장 분석 파이프라인
- [x] 표면형 매칭 → 원형(lemma) 매핑
- [x] 단어/문법/표현 중복 체크 후 저장
- [x] 중간 테이블로 연결
- [x] 레벨/메타데이터 자동 부여
- [x] 분석 결과 요약 응답 포맷

### Phase 4 - 검색/추천
- [x] pgvector 유사도 검색 API
- [x] 80/20(아는 것/새 것) 추천 로직
- [x] 약점 기반 연습 추천
- [x] 테마/상황별 묶음 추천

### Phase 5 - 프론트 MVP (Streamlit)
- [x] ??? ???(???)
- [x] 레이아웃/네비게이션 구조
- [x] 대시보드(오늘 복습/진행도/약점)
- [x] 수동 추가 폼(단어/문법/표현)
- [x] 문장 추가(자동 분석)
- [x] 복습 플로우(UI/평가 버튼)
- [x] 검색/필터 UI

### Phase 6 - LLM 코칭
- [x] 프롬프트 템플릿 + 안전 가드레일
- [x] 시나리오 대화 연습
- [x] 피드백/교정
- [x] 사용자 레벨/알려진 단어 기반 생성

### Phase 7 - 운영/품질
- [x] 로깅/에러 추적
- [x] 기본 테스트
- [x] 비용 모니터링/레이트 리밋
- [x] 백업/복구 전략 문서화
- [x] 성능 튜닝(인덱스/쿼리)

### Phase 8 - 운영 기능 확장
- [x] 통계/성취 대시보드
- [x] 배지/스트릭
- [x] 데이터 내보내기/가져오기
- [x] OCR/음성 기능(보류)
