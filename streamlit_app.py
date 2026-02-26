import requests
import streamlit as st


st.set_page_config(page_title="Deutsch Lab", layout="wide")

BASE_DEFAULT = "http://127.0.0.1:8010"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

:root {
  --bg-1: #f4f7fc;
  --bg-2: #edf2fb;
  --bg-3: #ecf8f5;
  --accent: #c98a00;
  --accent-2: #0a8f78;
  --accent-3: #d9541a;
  --ink: #1a2340;
  --muted: #6b7592;
  --panel: rgba(255,255,255,0.75);
  --panel-strong: rgba(255,255,255,0.95);
  --stroke: rgba(0,0,0,0.10);
}

html, body {
  font-family: "Space Grotesk", sans-serif;
  color: var(--ink);
  background: var(--bg-1) !important;
}

h1, h2, h3, .hero-title {
  font-family: "Sora", sans-serif;
  letter-spacing: -0.02em;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background:
    radial-gradient(1200px 520px at 10% 5%, #dde8ff, transparent),
    radial-gradient(900px 500px at 85% 15%, #c8f5eb, transparent),
    linear-gradient(135deg, var(--bg-1), var(--bg-2)) !important;
  color: var(--ink) !important;
}

[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.97) !important;
  border-right: 1px solid var(--stroke) !important;
  color: var(--ink) !important;
}

p, span, div, label {
  color: inherit;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span {
  color: var(--ink);
}

.stApp:before {
  content: "";
  position: fixed;
  inset: 0;
  background-image: repeating-linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.015) 0px,
    rgba(0, 0, 0, 0.015) 1px,
    transparent 1px,
    transparent 8px
  );
  pointer-events: none;
  z-index: 0;
}

.block-container {
  position: relative;
  z-index: 2;
  padding-top: 2.5rem;
}

.bg-orb {
  position: fixed;
  border-radius: 999px;
  opacity: 0.4;
  z-index: 1;
}

.orb-1 {
  width: 380px;
  height: 380px;
  left: -120px;
  top: 120px;
  background: radial-gradient(circle at 30% 30%, #fde68a, transparent 65%);
}

.orb-2 {
  width: 460px;
  height: 460px;
  right: -160px;
  top: 40px;
  background: radial-gradient(circle at 70% 30%, #6ee7d4, transparent 65%);
}

.hero {
  padding: 28px 32px;
  border: 1px solid var(--stroke);
  background: var(--panel);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  animation: floatIn 0.8s ease-out;
}

.hero-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
  justify-content: space-between;
}

.hero-title {
  font-size: 36px;
  margin: 8px 0 6px 0;
}

.hero-sub {
  color: var(--muted);
  font-size: 16px;
  margin-bottom: 12px;
}

.hero-panel {
  min-width: 240px;
  border: 1px solid var(--stroke);
  border-radius: 16px;
  padding: 16px;
  background: rgba(255,255,255,0.7);
}

.card {
  border: 1px solid var(--stroke);
  background: var(--panel);
  border-radius: 16px;
  padding: 16px 18px;
  margin-bottom: 12px;
  animation: fadeUp 0.6s ease-out;
}

.stat-card {
  border: 1px solid var(--stroke);
  background: var(--panel-strong);
  border-radius: 16px;
  padding: 18px;
  min-height: 120px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.stat-label {
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.stat-value {
  font-size: 30px;
  font-weight: 700;
  margin: 10px 0 6px 0;
}

.stat-sub {
  color: var(--muted);
  font-size: 13px;
}

.pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--stroke);
  color: var(--muted);
  font-size: 12px;
  margin-right: 6px;
  background: rgba(255,255,255,0.6);
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 12px;
  background: rgba(0,0,0,0.05);
  border: 1px solid var(--stroke);
  font-size: 12px;
}

.accent {
  color: var(--accent);
  font-weight: 700;
}

div.stButton > button {
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #ffffff;
  border: none;
  border-radius: 12px;
  padding: 0.6rem 1.1rem;
  font-weight: 700;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--stroke);
  color: var(--ink);
}

div[data-baseweb="select"] > div {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--stroke);
  color: var(--ink);
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="bg-orb orb-1"></div>
<div class="bg-orb orb-2"></div>
""",
    unsafe_allow_html=True,
)


def _auth_headers() -> dict:
    key = st.session_state.get("api_key", "")
    return {"X-API-Key": key} if key else {}


def api_get(base: str, path: str, params: dict | None = None):
    url = f"{base}{path}"
    resp = requests.get(url, params=params, headers=_auth_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_post(base: str, path: str, json_body: dict | list | None = None, params=None):
    url = f"{base}{path}"
    resp = requests.post(url, json=json_body, params=params, headers=_auth_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_put(base: str, path: str, json_body: dict | None = None):
    url = f"{base}{path}"
    resp = requests.put(url, json=json_body, headers=_auth_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()


def stat_card(label: str, value: str, sub: str = ""):
    st.markdown(
        f"""
<div class="stat-card">
  <div class="stat-label">{label}</div>
  <div class="stat-value">{value}</div>
  <div class="stat-sub">{sub}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ── 사이드바 ────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center;padding:16px 0 8px">
  <div style="font-size:20px;font-weight:700;color:var(--accent)">🇩🇪 Deutsch Lab</div>
  <div style="font-size:11px;color:var(--muted)">한국인을 위한 독일어 학습</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar.expander("⚙️ 서버 설정", expanded=False):
    base_url = st.text_input("API Base URL", BASE_DEFAULT, key="cfg_base_url")
    api_key_input = st.text_input("API Key", type="password", value="", key="cfg_api_key")
    st.session_state["api_key"] = api_key_input

# expander 안에서 정의된 변수는 with 블록 밖에서도 유효하지만,
# session_state 키로 안전하게 읽기
base_url = st.session_state.get("cfg_base_url", BASE_DEFAULT)

user_id = st.sidebar.number_input("사용자 ID", min_value=1, value=1, step=1)

PAGES = {
    "대시보드":  "Dashboard",
    "복습":      "Review",
    "시나리오":  "Scenarios",
    "검색":      "Search",
    "AI 선생님": "AI Teacher",
}
nav_label = st.sidebar.selectbox("메뉴", list(PAGES.keys()))
nav = PAGES[nav_label]

# ── 페이지 본문 ──────────────────────────────────────────────────────────────

if nav == "Dashboard":
    st.subheader("오늘의 학습 현황")
    col1, col2, col3, col4 = st.columns(4)
    try:
        review_data = api_get(
            base_url,
            "/study/review-today",
            {"user_id": user_id, "item_type": "word"},
        )["data"]
        due_count = len(review_data)
    except Exception:
        due_count = "-"

    bundle_meta = {}
    try:
        bundle = api_get(base_url, "/recommend/today", {"user_id": user_id})
        bundle_data = bundle["data"]
        bundle_count = len(bundle_data.get("words", []))
        bundle_scenario_count = len(bundle_data.get("scenarios", []))
        bundle_meta = bundle_data.get("meta", {})
    except Exception:
        bundle_count = "-"
        bundle_scenario_count = "-"

    try:
        weak = api_get(base_url, "/recommend/weak-grammar", {"user_id": user_id})
        weak_count = len(weak["data"])
    except Exception:
        weak_count = "-"

    with col1:
        stat_card("복습 대기 단어", str(due_count), "복습 대기 중")
    with col2:
        stat_card("추천 단어", str(bundle_count), "오늘 추천")
    with col3:
        stat_card("시나리오", str(bundle_scenario_count), "오늘 연습")
    with col4:
        avg_str = f"{bundle_meta.get('avg_mastery', 0):.0%}" if bundle_meta else "-"
        stat_card("평균 숙달도", avg_str, f"레벨: {bundle_meta.get('current_level', '-')}")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("취약 문법")
        try:
            weak = api_get(base_url, "/recommend/weak-grammar", {"user_id": user_id})
            for row in weak["data"][:4]:
                st.markdown(
                    f"<div class='card'><div class='accent'>{row['rule_name']}</div><div class='pill'>{row.get('level','')}</div></div>",
                    unsafe_allow_html=True,
                )
        except Exception as exc:
            st.error(str(exc))

    with col_right:
        st.subheader("취약 단어")
        try:
            weak_words = api_get(base_url, "/recommend/weak-words", {"user_id": user_id})
            for row in weak_words["data"][:4]:
                st.markdown(
                    f"<div class='card'><div class='accent'>{row['lemma']}</div><div class='pill'>{row.get('level','')}</div><div class='pill'>{row.get('translation','')}</div></div>",
                    unsafe_allow_html=True,
                )
        except Exception as exc:
            st.error(str(exc))

    st.divider()
    st.subheader("통계")
    try:
        overview = api_get(base_url, "/stats/overview", {"user_id": user_id})["data"]
        totals = overview["totals"]
        streaks = overview["streaks"]
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            stat_card("전체 단어", str(totals["words"]), "DB 저장")
        with sc2:
            stat_card("전체 문법", str(totals["grammar"]), "DB 저장")
        with sc3:
            stat_card("마스터 단어", str(overview["mastered_words"]), "마스터 완료")
        with sc4:
            stat_card("연속 학습", f"{streaks['current']}일", "오늘까지")
    except Exception as exc:
        st.error(str(exc))

elif nav == "Review":
    st.subheader("복습 큐")

    _quality_labels = {
        0: "0 전혀 모름",
        1: "1 어렴풋이",
        2: "2 어려웠음",
        3: "3 기억남",
        4: "4 쉬웠음",
        5: "5 완벽",
    }

    try:
        queue = api_get(
            base_url,
            "/study/review-today",
            {"user_id": user_id, "item_type": "word"},
        )["data"]
        for row in queue:
            success = row.get("success_count", 0)
            fail = row.get("fail_count", 0)
            st.markdown(
                f"<div class='card'><div class='accent'>단어 #{row['word_id']}</div>"
                f"<div class='pill'>다음 복습 {row.get('next_review')}</div>"
                f"<div class='pill'>✓ {success} / ✗ {fail}</div></div>",
                unsafe_allow_html=True,
            )
            quality = st.selectbox(
                "학습 품질",
                options=[0, 1, 2, 3, 4, 5],
                index=4,
                format_func=lambda x: _quality_labels[x],
                key=f"q_{row['id']}",
            )
            if st.button("복습 완료", key=f"btn_{row['id']}"):
                st.write(
                    api_post(
                        base_url,
                        "/study/review-word",
                        params={"state_id": row["id"], "quality": quality},
                    )
                )
    except Exception as exc:
        st.error(str(exc))

elif nav == "Scenarios":
    st.subheader("시나리오 연습")

    _quality_labels = {
        0: "0 전혀 모름",
        1: "1 어렴풋이",
        2: "2 어려웠음",
        3: "3 기억남",
        4: "4 쉬웠음",
        5: "5 완벽",
    }

    st.write("**오늘의 시나리오**")
    try:
        bundle = api_get(base_url, "/recommend/today", {"user_id": user_id})
        today_scenarios = bundle["data"].get("scenarios", [])
        if today_scenarios:
            for scenario in today_scenarios:
                with st.expander(f"{scenario['name']} [{scenario.get('level_min','')}-{scenario.get('level_max','')}]"):
                    st.write(scenario.get("description", ""))
                    if scenario.get("dialogue_script"):
                        st.json(scenario["dialogue_script"])
                    quality = st.selectbox(
                        "학습 품질",
                        options=[0, 1, 2, 3, 4, 5],
                        index=4,
                        format_func=lambda x: _quality_labels[x],
                        key=f"sc_q_{scenario['id']}",
                    )
                    if st.button("연습 완료", key=f"sc_btn_{scenario['id']}"):
                        result = api_post(
                            base_url,
                            f"/scenarios/{scenario['id']}/practice",
                            params={"user_id": user_id, "quality": quality},
                        )
                        st.success(f"기록 완료! 다음 복습: {result['data'].get('next_review', '-')}")
        else:
            st.info("오늘 예정된 시나리오가 없습니다.")
    except Exception as exc:
        st.error(str(exc))

    st.divider()
    st.write("**전체 시나리오**")
    try:
        all_scenarios = api_get(base_url, "/scenarios", {"limit": 50})["data"]
        for scenario in all_scenarios:
            with st.expander(f"{scenario['name']} [{scenario.get('situation', '-')}]"):
                st.write(scenario.get("description", ""))
                quality = st.selectbox(
                    "학습 품질",
                    options=[0, 1, 2, 3, 4, 5],
                    index=4,
                    format_func=lambda x: _quality_labels[x],
                    key=f"all_sc_q_{scenario['id']}",
                )
                if st.button("연습하기", key=f"all_sc_btn_{scenario['id']}"):
                    result = api_post(
                        base_url,
                        f"/scenarios/{scenario['id']}/practice",
                        params={"user_id": user_id, "quality": quality},
                    )
                    st.success(f"기록 완료! 다음 복습: {result['data'].get('next_review', '-')}")
    except Exception as exc:
        st.error(str(exc))

elif nav == "Search":
    st.subheader("벡터 검색")

    _search_type_labels = {
        "words": "단어",
        "grammar": "문법",
        "expressions": "표현",
        "scenarios": "시나리오",
    }
    search_type = st.selectbox(
        "검색 대상",
        ["words", "grammar", "expressions", "scenarios"],
        format_func=lambda x: _search_type_labels[x],
    )
    search_query = st.text_input("검색어", "")
    limit = st.slider("결과 수", min_value=1, max_value=50, value=10)
    if st.button("검색하기"):
        try:
            st.write(api_get(base_url, f"/search/{search_type}", {"q": search_query, "limit": limit}))
        except Exception as exc:
            st.error(str(exc))

    st.subheader("테마 묶음")
    theme = st.text_input("테마 / 상황", "food")
    if st.button("테마 묶음 조회"):
        st.write(api_get(base_url, "/recommend/theme", {"theme": theme}))

elif nav == "AI Teacher":
    st.subheader("AI 선생님")
    tab_words, tab_sentences, tab_chat = st.tabs(["단어 생성", "문장 연습", "AI 대화"])

    with tab_words:
        st.markdown("#### 맞춤 단어 생성")
        word_count = st.slider("생성할 단어 수", 1, 10, 5, key="tw_count")
        theme_input = st.text_input("테마 (선택 사항)", placeholder="예: 음식, 여행, 직장 등", key="tw_theme")
        if st.button("단어 생성하기", key="tw_btn"):
            payload = {"user_id": user_id, "count": word_count, "theme": theme_input or None}
            result = api_post(base_url, "/teacher/generate-words", payload)
            if result.get("status") == "ok":
                words = result.get("data", {}).get("words", [])
                meta = result.get("data", {}).get("meta", {})
                if meta:
                    st.caption(f"레벨 범위: {meta.get('level_range', '')} / 테마: {meta.get('theme_used') or '없음'}")
                for w in words:
                    gender_str = f" ({w.get('gender', '')})" if w.get("gender") else ""
                    plural_str = f", Pl: {w['plural']}" if w.get("plural") else ""
                    st.markdown(
                        f"""<div style="background:var(--panel-strong);border-radius:10px;padding:14px 18px;margin-bottom:10px">
<span style="font-size:1.2rem;font-weight:700;color:var(--accent)">{w['german']}</span>{gender_str}
<span style="color:var(--muted);font-size:0.85rem"> {w.get('part_of_speech','')} {plural_str} · {w.get('level','')}</span><br>
<span style="font-size:1rem">{w['translation']}</span><br>
<span style="color:var(--accent-2);font-size:0.9rem"><em>{w['example_sentence']}</em></span><br>
<span style="color:var(--muted);font-size:0.85rem">{w['example_translation']}</span>
</div>""",
                        unsafe_allow_html=True,
                    )
            else:
                st.error(result.get("detail", "오류가 발생했습니다."))

    with tab_sentences:
        st.markdown("#### 문장 중심 학습")
        sent_count = st.slider("생성할 문장 수", 1, 10, 5, key="ts_count")

        if "ts_sentences" not in st.session_state:
            st.session_state["ts_sentences"] = []

        if st.button("문장 생성하기", key="ts_btn"):
            payload = {"user_id": user_id, "count": sent_count}
            result = api_post(base_url, "/teacher/generate-sentences", payload)
            if result.get("status") == "ok":
                st.session_state["ts_sentences"] = result.get("data", {}).get("sentences", [])
                meta = result.get("data", {}).get("meta", {})
                if meta.get("weak_grammar_targets"):
                    st.caption("집중 문법: " + ", ".join(meta["weak_grammar_targets"]))
            else:
                st.error(result.get("detail", "오류가 발생했습니다."))

        for i, s in enumerate(st.session_state.get("ts_sentences", [])):
            st.markdown("---")
            # 문장 + 번역
            st.markdown(
                f'<div style="font-size:1.15rem;font-weight:600;color:var(--accent)">{s["german"]}</div>'
                f'<div style="color:var(--muted);margin-bottom:6px">{s["korean"]}</div>',
                unsafe_allow_html=True,
            )
            st.caption(f"문법 포인트: {s['grammar_focus']}")
            if s.get("blanked"):
                st.markdown(f"**빈칸 연습**: {s['blanked']}  ·  **힌트**: {s['hint']}")

            # 동사 변화표
            verbs = s.get("verbs", [])
            if verbs:
                st.markdown("**동사 변화표 (현재형)**")
                for verb in verbs:
                    p = verb.get("present", {})
                    table_html = f"""
<table style="border-collapse:collapse;font-size:0.85rem;margin-bottom:6px">
  <tr>
    <td style="padding:2px 10px;color:var(--muted)">ich</td>
    <td style="padding:2px 14px;font-weight:600">{p.get('ich','')}</td>
    <td style="padding:2px 10px;color:var(--muted)">wir</td>
    <td style="padding:2px 14px;font-weight:600">{p.get('wir','')}</td>
  </tr>
  <tr>
    <td style="padding:2px 10px;color:var(--muted)">du</td>
    <td style="padding:2px 14px;font-weight:600">{p.get('du','')}</td>
    <td style="padding:2px 10px;color:var(--muted)">ihr</td>
    <td style="padding:2px 14px;font-weight:600">{p.get('ihr','')}</td>
  </tr>
  <tr>
    <td style="padding:2px 10px;color:var(--muted)">er/sie/es</td>
    <td style="padding:2px 14px;font-weight:600">{p.get('er/sie/es','')}</td>
    <td style="padding:2px 10px;color:var(--muted)">sie/Sie</td>
    <td style="padding:2px 14px;font-weight:600">{p.get('sie/Sie','')}</td>
  </tr>
</table>"""
                    st.markdown(f"*{verb['lemma']}*" + table_html, unsafe_allow_html=True)

            # 단어 복습 표시 멀티셀렉트
            words = s.get("words", [])
            if words:
                word_options = []
                word_id_map = {}
                for w in words:
                    label_parts = [w["german"]]
                    if w.get("gender"):
                        label_parts.append(f"({w['gender']})")
                    label_parts.append(f"— {w['translation']}")
                    if w.get("is_new"):
                        label_parts.append("🆕")
                    label = " ".join(label_parts)
                    word_options.append(label)
                    word_id_map[label] = w.get("word_id")

                selected = st.multiselect(
                    "복습할 단어 선택",
                    options=word_options,
                    key=f"ts_sel_{i}",
                )
                if st.button("단어 표시하기", key=f"ts_mark_{i}"):
                    success_count = 0
                    for label in selected:
                        wid = word_id_map.get(label)
                        if wid is None:
                            continue
                        mark_result = api_post(base_url, "/user-state/words/mark",
                                               {"user_id": user_id, "word_id": wid})
                        if mark_result.get("status") == "ok":
                            success_count += 1
                    if success_count:
                        st.success(f"✓ {success_count}개 단어가 다음 학습에 포함됩니다.")
                    elif selected:
                        st.warning("표시 중 오류가 발생했습니다.")

    with tab_chat:
        st.markdown("#### AI 선생님과 대화")
        if "teacher_chat_history" not in st.session_state:
            st.session_state["teacher_chat_history"] = []

        mode = st.selectbox("대화 모드", ["free", "correction", "vocab_drill"],
                            format_func=lambda x: {"free": "자유 대화", "correction": "문법 교정", "vocab_drill": "단어 위주"}[x],
                            key="tc_mode")

        for msg in st.session_state["teacher_chat_history"]:
            role_label = "나" if msg["role"] == "user" else "선생님"
            align = "right" if msg["role"] == "user" else "left"
            bg = "var(--bg-2)" if msg["role"] == "user" else "var(--panel-strong)"
            st.markdown(
                f'<div style="text-align:{align};margin:4px 0"><span style="background:{bg};'
                f'border-radius:8px;padding:8px 14px;display:inline-block;max-width:80%">'
                f'<b>{role_label}</b>: {msg["content"]}</span></div>',
                unsafe_allow_html=True,
            )

        user_msg = st.text_input("메시지 입력", key="tc_input", placeholder="독일어 또는 한국어로 입력하세요")
        col_send, col_clear = st.columns([1, 5])
        with col_send:
            send_btn = st.button("전송", key="tc_send")
        with col_clear:
            if st.button("대화 초기화", key="tc_clear"):
                st.session_state["teacher_chat_history"] = []
                st.rerun()

        if send_btn and user_msg.strip():
            history_payload = [{"role": m["role"], "content": m["content"]}
                               for m in st.session_state["teacher_chat_history"]]
            payload = {
                "user_id": user_id,
                "message": user_msg,
                "history": history_payload,
                "mode": mode,
            }
            result = api_post(base_url, "/teacher/chat", payload)
            if result.get("status") == "ok":
                data = result["data"]
                st.session_state["teacher_chat_history"].append({"role": "user", "content": user_msg})
                st.session_state["teacher_chat_history"].append({"role": "assistant", "content": data["reply"]})
                if data.get("correction"):
                    st.info(f"교정: {data['correction']}")
                if data.get("new_words"):
                    st.caption("새 단어: " + ", ".join(data["new_words"]))
                if data.get("tip"):
                    st.caption(f"팁: {data['tip']}")
                st.rerun()
            else:
                st.error(result.get("detail", "오류가 발생했습니다."))

