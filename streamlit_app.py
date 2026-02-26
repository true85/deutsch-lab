import json
from datetime import date

import requests
import streamlit as st


st.set_page_config(page_title="Deutsch Lab", layout="wide")

BASE_DEFAULT = "http://127.0.0.1:8010"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

:root {
  --bg-1: #0b1220;
  --bg-2: #13253b;
  --bg-3: #1f2f27;
  --accent: #f4c767;
  --accent-2: #56d6bf;
  --accent-3: #ff8a5b;
  --ink: #f6f2ea;
  --muted: #b8b3ab;
  --panel: rgba(255,255,255,0.06);
  --panel-strong: rgba(255,255,255,0.12);
  --stroke: rgba(255,255,255,0.16);
}

html, body, [class*="css"]  {
  font-family: "Space Grotesk", sans-serif;
  color: var(--ink);
}

h1, h2, h3, .hero-title {
  font-family: "Sora", sans-serif;
  letter-spacing: -0.02em;
}

.stApp {
  position: relative;
  background:
    radial-gradient(1200px 520px at 10% 5%, #203a5b, transparent),
    radial-gradient(900px 500px at 85% 15%, #244b38, transparent),
    linear-gradient(135deg, var(--bg-1), var(--bg-2));
}

.stApp:before {
  content: "";
  position: fixed;
  inset: 0;
  background-image: repeating-linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.03) 0px,
    rgba(255, 255, 255, 0.03) 1px,
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
  opacity: 0.35;
  z-index: 1;
}

.orb-1 {
  width: 380px;
  height: 380px;
  left: -120px;
  top: 120px;
  background: radial-gradient(circle at 30% 30%, #ffe08a, transparent 65%);
}

.orb-2 {
  width: 460px;
  height: 460px;
  right: -160px;
  top: 40px;
  background: radial-gradient(circle at 70% 30%, #5fe1c8, transparent 65%);
}

.hero {
  padding: 28px 32px;
  border: 1px solid var(--stroke);
  background: var(--panel);
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.3);
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
  background: rgba(7, 12, 18, 0.4);
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
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 12px;
  background: rgba(0,0,0,0.35);
  border: 1px solid var(--stroke);
  font-size: 12px;
}

.accent {
  color: var(--accent);
  font-weight: 700;
}

div.stButton > button {
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #0b1220;
  border: none;
  border-radius: 12px;
  padding: 0.6rem 1.1rem;
  font-weight: 700;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
  background: rgba(10, 16, 24, 0.55);
  border: 1px solid var(--stroke);
  color: var(--ink);
}

div[data-baseweb="select"] > div {
  background: rgba(10, 16, 24, 0.55);
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


st.sidebar.markdown("### Deutsch Lab")
base_url = st.sidebar.text_input("API Base URL", BASE_DEFAULT)
user_id = st.sidebar.number_input("User ID", min_value=1, value=1, step=1)
api_key_input = st.sidebar.text_input("API Key", type="password", value="")
st.session_state["api_key"] = api_key_input
nav = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Stats", "Manual Add", "Sentence Add", "Review", "Scenarios", "Search", "Coach", "Transfer"],
)

st.markdown(
    f"""
<div class="hero">
  <div class="hero-grid">
    <div>
      <div class="pill">German Learning System</div>
      <div class="pill">Supabase + FastAPI</div>
      <div class="hero-title">Deutsch Lab</div>
      <div class="hero-sub">Focus. Flow. Fortschritt.</div>
      <div class="badge">API <span class="accent">{base_url}</span></div>
    </div>
    <div class="hero-panel">
      <div class="badge">Active User <span class="accent">#{user_id}</span></div>
      <div style="margin-top:10px; color: var(--muted);">Realtime study flow and insights.</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")


if nav == "Dashboard":
    st.subheader("Daily Snapshot")
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
        stat_card("Due Words", str(due_count), "Review queue")
    with col2:
        stat_card("Bundle", str(bundle_count), "Recommended words")
    with col3:
        stat_card("Scenarios", str(bundle_scenario_count), "Today's practice")
    with col4:
        avg_str = f"{bundle_meta.get('avg_mastery', 0):.0%}" if bundle_meta else "-"
        stat_card("Avg Mastery", avg_str, f"Level: {bundle_meta.get('current_level', '-')}")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Weak Grammar")
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
        st.subheader("Weak Words")
        try:
            weak_words = api_get(base_url, "/recommend/weak-words", {"user_id": user_id})
            for row in weak_words["data"][:4]:
                st.markdown(
                    f"<div class='card'><div class='accent'>{row['lemma']}</div><div class='pill'>{row.get('level','')}</div><div class='pill'>{row.get('translation','')}</div></div>",
                    unsafe_allow_html=True,
                )
        except Exception as exc:
            st.error(str(exc))

elif nav == "Stats":
    st.subheader("Stats & Badges")
    try:
        overview = api_get(base_url, "/stats/overview", {"user_id": user_id})["data"]
        totals = overview["totals"]
        streaks = overview["streaks"]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            stat_card("Total Words", str(totals["words"]), "Words in DB")
        with col2:
            stat_card("Total Grammar", str(totals["grammar"]), "Grammar in DB")
        with col3:
            stat_card("Total Expressions", str(totals["expressions"]), "Expressions in DB")
        with col4:
            stat_card("Mastered", str(overview["mastered_words"]), "Mastered words")

        st.markdown(
            f"<div class='card'><div class='accent'>Current Streak</div>"
            f"<div class='stat-value'>{streaks['current']} days</div></div>",
            unsafe_allow_html=True,
        )
    except Exception as exc:
        st.error(str(exc))

    st.subheader("Badges")
    try:
        badges = api_get(base_url, "/achievements", {"user_id": user_id})["data"]["badges"]
        for badge in badges:
            status = "Unlocked" if badge["unlocked"] else "Locked"
            st.markdown(
                f"<div class='card'><div class='accent'>{badge['label']}</div>"
                f"<div class='pill'>{status}</div><div>{badge['desc']}</div></div>",
                unsafe_allow_html=True,
            )
    except Exception as exc:
        st.error(str(exc))

elif nav == "Manual Add":
    st.subheader("Manual Add")
    tab_word, tab_grammar, tab_expr, tab_scenario = st.tabs(
        ["Word", "Grammar", "Expression", "Scenario"]
    )

    with tab_word:
        lemma = st.text_input("Lemma")
        pos = st.text_input("Part of Speech", "Nomen")
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"])
        translation = st.text_input("Translation")
        gender = st.text_input("Gender (der/die/das)")
        plural = st.text_input("Plural")
        theme = st.text_input("Theme")
        frequency = st.text_input("Frequency", "common")
        if st.button("Save Word"):
            payload = {
                "lemma": lemma,
                "part_of_speech": pos,
                "level": level,
                "translation": translation or None,
                "gender": gender or None,
                "plural": plural or None,
                "theme": theme or None,
                "frequency": frequency or None,
            }
            st.write(api_post(base_url, "/words", payload))

    with tab_grammar:
        rule_name = st.text_input("Rule Name")
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"], key="grammar_level")
        category = st.text_input("Category")
        explanation = st.text_area("Explanation")
        examples = st.text_area("Examples (one per line)")
        if st.button("Save Grammar"):
            payload = {
                "rule_name": rule_name,
                "level": level,
                "category": category or None,
                "explanation": explanation or None,
                "examples": [x for x in examples.splitlines() if x.strip()] or None,
            }
            st.write(api_post(base_url, "/grammar", payload))

    with tab_expr:
        german = st.text_area("German")
        korean = st.text_area("Korean")
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"], key="expr_level")
        type_ = st.text_input("Type")
        formality = st.selectbox("Formality", ["", "formal", "informal", "neutral"])
        situation = st.text_input("Situation")
        context = st.text_area("Context")
        if st.button("Save Expression"):
            payload = {
                "german": german,
                "korean": korean or None,
                "level": level,
                "type": type_ or None,
                "formality": formality or None,
                "situation": situation or None,
                "context": context or None,
            }
            st.write(api_post(base_url, "/expressions", payload))

    with tab_scenario:
        name = st.text_input("Scenario Name")
        description = st.text_area("Description")
        level_min = st.selectbox("Min Level", ["A1", "A2", "B1", "B2", "C1", "C2"], key="level_min")
        level_max = st.selectbox("Max Level", ["A1", "A2", "B1", "B2", "C1", "C2"], key="level_max")
        situation = st.text_input("Situation")
        dialogue = st.text_area("Dialogue Script (JSON)")
        if st.button("Save Scenario"):
            payload = {
                "name": name,
                "description": description or None,
                "level_min": level_min,
                "level_max": level_max,
                "situation": situation or None,
                "dialogue_script": json.loads(dialogue) if dialogue else None,
            }
            st.write(api_post(base_url, "/scenarios", payload))

elif nav == "Sentence Add":
    st.subheader("Sentence Analyze")
    sentence = st.text_area("Sentence", "Ich gehe mit meinem Freund ins Kino")
    level_hint = st.selectbox("Level Hint", ["A1", "A2", "B1", "B2", "C1", "C2"])
    save = st.toggle("Save to DB", value=True)
    if st.button("Analyze"):
        payload = {"sentence": sentence, "level_hint": level_hint, "save": save}
        st.write(api_post(base_url, "/analysis/sentence", payload))

elif nav == "Review":
    st.subheader("Review Queue")
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
                f"<div class='card'><div class='accent'>Word ID {row['word_id']}</div>"
                f"<div class='pill'>State {row['id']}</div>"
                f"<div class='pill'>Next {row.get('next_review')}</div>"
                f"<div class='pill'>✓ {success} / ✗ {fail}</div></div>",
                unsafe_allow_html=True,
            )
            quality = st.select_slider(
                f"Quality for state {row['id']}",
                options=[0, 1, 2, 3, 4, 5],
                value=4,
                key=f"q_{row['id']}",
            )
            if st.button(f"Update State {row['id']}", key=f"btn_{row['id']}"):
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
    st.subheader("Scenario Practice")

    st.write("**Today's Scenario Queue**")
    try:
        bundle = api_get(base_url, "/recommend/today", {"user_id": user_id})
        today_scenarios = bundle["data"].get("scenarios", [])
        if today_scenarios:
            for scenario in today_scenarios:
                with st.expander(f"{scenario['name']} [{scenario.get('level_min','')}-{scenario.get('level_max','')}]"):
                    st.write(scenario.get("description", ""))
                    if scenario.get("dialogue_script"):
                        st.json(scenario["dialogue_script"])
                    quality = st.select_slider(
                        "Practice Quality",
                        options=[0, 1, 2, 3, 4, 5],
                        value=4,
                        key=f"sc_q_{scenario['id']}",
                    )
                    if st.button("Mark as Practiced", key=f"sc_btn_{scenario['id']}"):
                        result = api_post(
                            base_url,
                            f"/scenarios/{scenario['id']}/practice",
                            params={"user_id": user_id, "quality": quality},
                        )
                        st.success(f"Recorded! Next review: {result['data'].get('next_review', '-')}")
        else:
            st.info("No scenarios due today.")
    except Exception as exc:
        st.error(str(exc))

    st.divider()
    st.write("**All Scenarios**")
    try:
        all_scenarios = api_get(base_url, "/scenarios", {"limit": 50})["data"]
        for scenario in all_scenarios:
            with st.expander(f"{scenario['name']} [{scenario.get('situation', '-')}]"):
                st.write(scenario.get("description", ""))
                quality = st.select_slider(
                    "Practice Quality",
                    options=[0, 1, 2, 3, 4, 5],
                    value=4,
                    key=f"all_sc_q_{scenario['id']}",
                )
                if st.button("Practice", key=f"all_sc_btn_{scenario['id']}"):
                    result = api_post(
                        base_url,
                        f"/scenarios/{scenario['id']}/practice",
                        params={"user_id": user_id, "quality": quality},
                    )
                    st.success(f"Recorded! Next review: {result['data'].get('next_review', '-')}")
    except Exception as exc:
        st.error(str(exc))

elif nav == "Search":
    st.subheader("Vector Search")
    search_type = st.selectbox(
        "Type", ["words", "grammar", "expressions", "scenarios"]
    )
    search_query = st.text_input("Search Query", "")
    limit = st.slider("Limit", min_value=1, max_value=50, value=10)
    if st.button("Search"):
        try:
            st.write(api_get(base_url, f"/search/{search_type}", {"q": search_query, "limit": limit}))
        except Exception as exc:
            st.error(str(exc))

    st.subheader("Theme Bundle")
    theme = st.text_input("Theme/Situation", "food")
    if st.button("Get Theme Bundle"):
        st.write(api_get(base_url, "/recommend/theme", {"theme": theme}))

elif nav == "Coach":
    st.subheader("LLM Coach")
    tab_feedback, tab_roleplay = st.tabs(["Feedback", "Roleplay"])

    with tab_feedback:
        text = st.text_area("Learner Sentence", "Ich gehe mit meinem Freund ins Kino")
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"], key="fb_level")
        focus = st.text_input("Focus", "grammar/word-order")
        known = st.text_input("Known Words (comma)")
        known_words = [w.strip() for w in known.split(",") if w.strip()]
        if st.button("Get Feedback"):
            payload = {
                "text": text,
                "level": level,
                "focus": focus or None,
                "known_words": known_words or None,
            }
            st.write(api_post(base_url, "/coach/feedback", payload))

    with tab_roleplay:
        scenario = st.text_input("Scenario", "restaurant order")
        level = st.selectbox("Level", ["A1", "A2", "B1", "B2", "C1", "C2"], key="rp_level")
        user_input = st.text_area("Your Reply")
        formality = st.selectbox("Formality", ["", "formal", "informal", "neutral"], key="rp_form")
        known = st.text_input("Known Words (comma, 비워두면 DB 자동 조회)", key="rp_known")
        known_words = [w.strip() for w in known.split(",") if w.strip()]
        if st.button("Start Roleplay"):
            payload = {
                "scenario": scenario,
                "level": level,
                "user_input": user_input or None,
                "formality": formality or None,
                "known_words": known_words or None,
                "user_id": user_id,
            }
            st.write(api_post(base_url, "/coach/roleplay", payload))

elif nav == "Transfer":
    st.subheader("Export / Import")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Export JSON"):
            export_data = api_get(base_url, "/transfer/export", {"user_id": user_id})
            st.json(export_data["data"])
    with col2:
        import_text = st.text_area("Import JSON", height=240)
        if st.button("Import JSON"):
            try:
                payload = json.loads(import_text)
                if "data" not in payload:
                    payload = {"user_id": user_id, "data": payload}
                if "user_id" not in payload:
                    payload["user_id"] = user_id
                st.write(api_post(base_url, "/transfer/import", payload))
            except Exception as exc:
                st.error(str(exc))
