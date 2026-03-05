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
  pointer-events: none;
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
  background: rgba(255,255,255,0.85);
  color: var(--ink);
  border: 1px solid var(--stroke);
  border-radius: 10px;
  padding: 0.5rem 1rem;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
div.stButton > button:hover {
  background: rgba(255,255,255,1);
  border-color: var(--accent);
  color: var(--accent);
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

.dialogue-wrap { display:flex; flex-direction:column; gap:10px; padding:10px 0; }
.turn { display:flex; flex-direction:column; max-width:72%; }
.turn-left { align-self:flex-start; }
.turn-right { align-self:flex-end; align-items:flex-end; }
.turn-role { font-size:11px; color:var(--muted); margin-bottom:3px; text-transform:capitalize; }
.bubble {
  padding:10px 14px; border-radius:16px; font-size:0.9rem; line-height:1.5;
  box-shadow:0 2px 6px rgba(0,0,0,0.07);
}
.bubble-left  { background:rgba(255,255,255,0.9); border:1px solid var(--stroke); border-top-left-radius:4px; }
.bubble-right { background:#e8eef8; border:1px solid #c8d4e8; border-top-right-radius:4px; }
.bubble-de { font-weight:600; }
.bubble-ko { font-size:0.8rem; margin-top:4px; color:var(--muted); }

/* 단어 칩: 작고 인라인 느낌 */
div[data-testid="stHorizontalBlock"] div.stButton button {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 500;
  min-height: unset;
  height: auto;
  line-height: 1.6;
}

/* ── Fixed Tab Bar ── */
div[data-testid="stTabs"] [role="tablist"] {
    position: fixed;
    top: 3.75rem;   /* Streamlit 헤더 높이 */
    left: 0;
    right: 0;
    z-index: 999;
    background: rgba(244, 247, 252, 0.95);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--stroke);
    padding: 4px 1rem 0 1rem;
}

/* fixed tab bar 높이(약 45px)만큼 탭 패널 상단 여백 보정 */
div[data-testid="stTabs"] [role="tabpanel"] {
    margin-top: 45px;
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


def api_post(base: str, path: str, json_body: dict | list | None = None, params=None, timeout: int = 15):
    url = f"{base}{path}"
    resp = requests.post(url, json=json_body, params=params, headers=_auth_headers(), timeout=timeout)
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


def _render_inline_sentence(german: str, words: list, api_base: str, user_id: int) -> None:
    import re
    import streamlit.components.v1 as components

    # words 맵: 소문자 german → {word_id, translation}
    word_map = {}
    for w in words:
        key = w.get("german", "").lower()
        if key:
            word_map[key] = {
                "word_id": w.get("word_id"),
                "translation": w.get("translation", ""),
            }

    def replace_token(m):
        token = m.group(0)
        meta = word_map.get(token.lower(), {})
        wid = meta.get("word_id") or ""
        title = meta.get("translation", "")
        return (
            f'<span class="w" data-wid="{wid}" title="{title}" '
            f'style="border-bottom:1.5px dashed #999;cursor:pointer;color:inherit">'
            f'{token}</span>'
        )

    result = re.sub(r'[A-Za-zÄÖÜäöüß]+', replace_token, german)

    html = f"""<!DOCTYPE html><html><body style="margin:0;padding:4px 0;background:transparent;font-family:sans-serif">
<div style="font-size:1.1rem;font-weight:600;line-height:2">{result}</div>
<script>
const MARK_API   = "{api_base}/user-state/words/mark";
const UNMARK_API = "{api_base}/user-state/words/unmark";
const UID = {user_id};
const LS  = "ts_marked_words";

function hi(el) {{
  el.style.fontWeight = "800";
  el.style.textDecoration = "underline";
  el.style.color = "#c98a00";
  el.dataset.marked = "1";
}}

function lo(el) {{
  el.style.fontWeight = "";
  el.style.textDecoration = "";
  el.style.color = "inherit";
  el.dataset.marked = "";
}}

// localStorage 복원
try {{
  JSON.parse(localStorage.getItem(LS) || "[]")
    .forEach(wid => document.querySelectorAll('[data-wid="'+wid+'"]').forEach(hi));
}} catch(e) {{}}

// 클릭 = 토글
document.querySelectorAll('.w').forEach(el => {{
  el.onclick = function() {{
    const wid = +this.dataset.wid || 0;
    if (this.dataset.marked) {{
      lo(this);
      if (wid) {{
        try {{
          const s = JSON.parse(localStorage.getItem(LS) || "[]");
          const i = s.indexOf(wid);
          if (i > -1) {{ s.splice(i, 1); localStorage.setItem(LS, JSON.stringify(s)); }}
        }} catch(e) {{}}
        fetch(UNMARK_API, {{method:"POST", headers:{{"Content-Type":"application/json"}},
          body: JSON.stringify({{user_id:UID, word_id:wid}})}}).catch(()=>{{}});
      }}
    }} else {{
      hi(this);
      if (wid) {{
        try {{
          const s = JSON.parse(localStorage.getItem(LS) || "[]");
          if (!s.includes(wid)) {{ s.push(wid); localStorage.setItem(LS, JSON.stringify(s)); }}
        }} catch(e) {{}}
        fetch(MARK_API, {{method:"POST", headers:{{"Content-Type":"application/json"}},
          body: JSON.stringify({{user_id:UID, word_id:wid}})}}).catch(()=>{{}});
      }}
    }}
  }};
}});
</script></body></html>"""
    components.html(html, height=60, scrolling=False)


_USER_ROLES = {"customer", "tourist", "patient", "caller", "you"}

def render_dialogue(script: dict):
    # turns 형식(기존) 또는 exchanges 형식(AI 생성) 모두 지원
    turns = script.get("turns") or []
    exchanges = script.get("exchanges") or []
    if exchanges and not turns:
        turns = [
            {"role": e.get("speaker", ""), "text": e.get("german", ""), "translation": e.get("korean", "")}
            for e in exchanges
        ]
    if not turns:
        st.caption("대화 내용 없음")
        return
    parts = ['<div class="dialogue-wrap">']
    for idx, turn in enumerate(turns):
        role = turn.get("role", "")
        text = turn.get("text", "")
        translation = turn.get("translation", "")
        # _USER_ROLES 기반 판단; A/B 화자면 A=left, B=right
        if role.lower() in _USER_ROLES:
            side = "right"
        elif role.lower() == "b":
            side = "right"
        else:
            side = "left"
        parts.append(
            f'<div class="turn turn-{side}">'
            f'  <div class="turn-role">{role}</div>'
            f'  <div class="bubble bubble-{side}">'
            f'    <div class="bubble-de">{text}</div>'
            f'    <div class="bubble-ko">{translation}</div>'
            f'  </div>'
            f'</div>'
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


# ── 헤더 + 설정 ───────────────────────────────────────────────────────────────
st.markdown(
    '<div style="font-size:22px;font-weight:700;color:var(--accent);margin-bottom:4px">🇩🇪 Deutsch Lab</div>'
    '<div style="font-size:12px;color:var(--muted);margin-bottom:12px">한국인을 위한 독일어 학습</div>',
    unsafe_allow_html=True,
)
with st.expander("⚙️ 설정", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.number_input("사용자 ID", min_value=1, value=1, step=1, key="user_id")
    with col_b:
        st.text_input("API Base URL", BASE_DEFAULT, key="cfg_base_url")
    with col_c:
        _key_val = st.text_input("API Key", type="password", value="", key="cfg_api_key")
        st.session_state["api_key"] = _key_val

user_id = st.session_state.get("user_id", 1)
base_url = st.session_state.get("cfg_base_url", BASE_DEFAULT)

# ── 상단 탭 ──────────────────────────────────────────────────────────────────
tab_dash, tab_scenario, tab_search, tab_teacher = st.tabs(
    ["대시보드", "시나리오", "검색", "AI 선생님"]
)

if st.session_state.pop("dash_go_scenario", False):
    import streamlit.components.v1 as components
    components.html("""<script>
        const btns = window.parent.document.querySelectorAll('button[role="tab"]');
        for (const b of btns) {
            if (b.innerText.trim() === '시나리오') { b.click(); break; }
        }
    </script>""", height=0)

with tab_dash:
    st.subheader("오늘의 학습 현황")
    col1, col2, col3 = st.columns(3)
    try:
        review_data = api_get(
            base_url,
            "/study/review-today",
            {"user_id": user_id, "item_type": "word"},
        )["data"]
        due_count = len(review_data)
    except Exception:
        due_count = "-"

    try:
        bundle = api_get(base_url, "/recommend/today", {"user_id": user_id})
        bundle_data = bundle["data"]
        bundle_scenario_count = len(bundle_data.get("scenarios", []))
    except Exception:
        bundle_scenario_count = "-"

    try:
        today_res = api_get(base_url, "/user-state/words/today-count", {"user_id": user_id})
        today_word_count = today_res["data"]["count"]
    except Exception:
        today_word_count = "-"

    try:
        weak = api_get(base_url, "/recommend/weak-grammar", {"user_id": user_id})
        weak_count = len(weak["data"])
    except Exception:
        weak_count = "-"

    with col1:
        stat_card("복습 대기 단어", str(due_count), "복습 대기 중")
        if st.button("목록 보기", key="dash_due_btn"):
            st.session_state["dash_show_due"] = not st.session_state.get("dash_show_due", False)
    with col2:
        stat_card("시나리오", str(bundle_scenario_count), "오늘 연습")
        if st.button("시나리오 탭으로 →", key="dash_sc_btn"):
            st.session_state["dash_go_scenario"] = True
            st.rerun()
    with col3:
        stat_card("오늘 배운 단어", str(today_word_count), "오늘 처음 등록")
        if st.button("목록 보기", key="dash_today_btn"):
            st.session_state["dash_show_today"] = not st.session_state.get("dash_show_today", False)

    if st.session_state.get("dash_show_due"):
        try:
            detail = api_get(base_url, "/study/review-today",
                {"user_id": user_id, "item_type": "word", "with_details": "true"})["data"]
            if detail:
                st.dataframe(
                    [{"단어": r.get("lemma", ""), "뜻": r.get("translation", ""),
                      "레벨": r.get("level", ""), "다음복습": r.get("next_review", "")} for r in detail],
                    width='stretch', hide_index=True)
            else:
                st.info("복습 대기 단어 없음")
        except Exception as exc:
            st.error(str(exc))

    if st.session_state.get("dash_show_today"):
        try:
            today_words = api_get(base_url, "/user-state/words/today", {"user_id": user_id})["data"]
            if today_words:
                st.dataframe(
                    [{"단어": r.get("lemma", ""), "뜻": r.get("translation", ""),
                      "관사": r.get("gender", "")} for r in today_words],
                    width='stretch', hide_index=True)
            else:
                st.info("오늘 배운 단어 없음")
        except Exception as exc:
            st.error(str(exc))

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
            for row in weak_words["data"][:8]:
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(
                        f"<div class='card'><div class='accent'>{row['lemma']}</div><div class='pill'>{row.get('level','')}</div><div class='pill'>{row.get('translation','')}</div></div>",
                        unsafe_allow_html=True,
                    )
                with c2:
                    if st.button("✕", key=f"del_weak_{row['id']}", help="학습 완료로 삭제"):
                        api_post(base_url, "/user-state/words/unmark", {"user_id": user_id, "word_id": row["id"]})
                        st.rerun()
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

with tab_scenario:
    st.subheader("시나리오 연습")

    st.markdown("#### 시나리오 생성")
    situation_input = st.text_input("상황을 입력하세요", placeholder="예: 카페에서 커피 주문, 기차역에서 티켓 구매", key="sc_situation_input")
    if st.button("AI로 생성", key="sc_gen_btn"):
        if situation_input.strip():
            with st.spinner("시나리오 생성 중..."):
                result = api_post(base_url, "/teacher/generate-scenario", {
                    "user_id": user_id,
                    "situation": situation_input,
                    "save": True,
                }, timeout=60)
            if result.get("status") == "ok":
                sc = result["data"]["scenario"]
                st.success(f"저장 완료! (ID: {result['data'].get('saved_id', '-')})")
                with st.expander(f"미리보기: {sc.get('name', '')}"):
                    st.markdown(sc.get("description", ""))
                    if sc.get("dialogue_script"):
                        render_dialogue(sc["dialogue_script"])
                st.rerun()
            else:
                st.error(result.get("detail", "오류가 발생했습니다."))
        else:
            st.warning("상황을 입력해주세요.")

    st.divider()

    _quality_labels = {
        0: "0 전혀 모름",
        1: "1 어렴풋이",
        2: "2 어려웠음",
        3: "3 기억남",
        4: "4 쉬웠음",
        5: "5 완벽",
    }

    # DB에서 mastery=1.0인 시나리오 ID 로드 (새로고침 후에도 유지)
    try:
        sc_states = api_get(base_url, "/user-state/scenarios", {"user_id": user_id, "limit": 200})
        sc_mastered = {
            row["scenario_id"]
            for row in (sc_states.get("data") or [])
            if row.get("mastery_score", 0) >= 1.0
        }
    except Exception:
        sc_mastered = set()

    def _render_scenario_card(scenario: dict, btn_key: str, q_key: str):
        sc_id = scenario["id"]
        if sc_id in sc_mastered:
            st.caption("✅ 완벽 달성 — 숨겨짐")
            return
        st.markdown(
            f'<div style="color:var(--muted);font-size:0.85rem;margin-bottom:6px">'
            f'{scenario.get("description","")}&nbsp;&nbsp;'
            f'<span class="pill">{scenario.get("situation","-")}</span>'
            f'<span class="pill">{scenario.get("level_min","")}–{scenario.get("level_max","")}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if scenario.get("dialogue_script"):
            render_dialogue(scenario["dialogue_script"])
        quality = st.selectbox(
            "학습 품질",
            options=[0, 1, 2, 3, 4, 5],
            index=4,
            format_func=lambda x: _quality_labels[x],
            key=q_key,
        )
        if st.button("연습 완료", key=btn_key):
            result = api_post(
                base_url,
                f"/scenarios/{scenario['id']}/practice",
                params={"user_id": user_id, "quality": quality},
            )
            next_review = (result.get('data') or {}).get('next_review', '-')
            if quality == 5:
                st.success("완벽! 이 시나리오는 숨겨집니다.")
                st.rerun()
            else:
                st.success(f"기록 완료! 다음 복습: {next_review}")

    st.write("**오늘의 시나리오**")
    try:
        bundle = api_get(base_url, "/recommend/today", {"user_id": user_id})
        today_scenarios = bundle["data"].get("scenarios", [])
        if today_scenarios:
            for scenario in today_scenarios:
                with st.expander(f"{scenario['name']} [{scenario.get('level_min','')}-{scenario.get('level_max','')}]"):
                    _render_scenario_card(scenario, f"sc_btn_{scenario['id']}", f"sc_q_{scenario['id']}")
        else:
            st.info("오늘 예정된 시나리오가 없습니다.")
    except Exception as exc:
        st.error(str(exc))

    st.divider()
    st.write("**전체 시나리오**")
    try:
        all_scenarios = api_get(base_url, "/scenarios", {"limit": 50})["data"]
        active = [s for s in all_scenarios if s["id"] not in sc_mastered]
        done = [s for s in all_scenarios if s["id"] in sc_mastered]
        for scenario in active:
            with st.expander(f"{scenario['name']} [{scenario.get('situation', '-')}]"):
                _render_scenario_card(scenario, f"all_sc_btn_{scenario['id']}", f"all_sc_q_{scenario['id']}")
        if done:
            with st.expander(f"✅ 완료된 시나리오 ({len(done)}개)", expanded=False):
                for scenario in done:
                    with st.expander(f"{scenario['name']} [{scenario.get('situation', '-')}]"):
                        _render_scenario_card(scenario, f"done_sc_btn_{scenario['id']}", f"done_sc_q_{scenario['id']}")
    except Exception as exc:
        st.error(str(exc))

with tab_search:
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

with tab_teacher:
    st.subheader("AI 선생님")
    st.markdown("#### 문장 중심 학습")
    sent_count = st.slider("생성할 문장 수", 1, 10, 5, key="ts_count")

    if "ts_sentences" not in st.session_state:
        st.session_state["ts_sentences"] = []

    if st.button("문장 생성하기", key="ts_btn"):
        payload = {"user_id": user_id, "count": sent_count}
        result = api_post(base_url, "/teacher/generate-sentences", payload, timeout=60)
        if result.get("status") == "ok":
            st.session_state["ts_sentences"] = result.get("data", {}).get("sentences", [])
            meta = result.get("data", {}).get("meta", {})
            if meta.get("weak_grammar_targets"):
                st.caption("집중 문법: " + ", ".join(meta["weak_grammar_targets"]))
        else:
            st.error(result.get("detail", "오류가 발생했습니다."))

    for i, s in enumerate(st.session_state.get("ts_sentences", [])):
        st.markdown("---")

        col_main, col_btn = st.columns([10, 1])
        with col_btn:
            if st.button("📋", key=f"sc_gen_{i}", help="이 문장으로 시나리오 생성"):
                with st.spinner("시나리오 생성 중..."):
                    sc_result = api_post(base_url, "/teacher/generate-scenario", {
                        "user_id": user_id,
                        "situation": s.get("grammar_focus", "일상 대화"),
                        "seed_sentence": s["german"],
                        "save": True,
                    }, timeout=60)
                if sc_result.get("status") == "ok":
                    st.success(f"시나리오 저장됨! (ID: {sc_result['data'].get('saved_id', '-')})")
                else:
                    st.error(sc_result.get("detail", "오류"))

        with col_main:
            words = s.get("words", [])

            # 문장 표시 (인라인 클릭 마킹)
            _render_inline_sentence(s["german"], words, base_url, user_id)

            st.markdown(
                f'<div style="color:var(--muted);margin-bottom:4px">{s["korean"]}</div>',
                unsafe_allow_html=True,
            )
            st.caption(f"문법 포인트: {s['grammar_focus']}")

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


