# 인라인 단어 클릭 — 미완성 이슈 정리

작성일: 2026-02-26 | 상태: **미해결**

---

## 목표

AI 선생님 탭 > 문장 중심 학습에서
독일어 문장 안의 단어를 **직접 클릭**하면:
1. 해당 단어가 문장 안에서 **굵게 + 금색 하이라이트**
2. DB에 `next_review = today`로 마킹 (`POST /user-state/words/mark`)
3. 다음 문장 생성 시 해당 단어가 **우선 포함**됨

---

## 현재 구현 상태

### 완료된 것

| 항목 | 파일 | 상태 |
|------|------|------|
| `_build_clickable_html()` 헬퍼 | `streamlit_app.py:315` | ✅ 구현됨 |
| `click_detector()` 호출 | `streamlit_app.py:595` | ✅ 구현됨 |
| `POST /user-state/words/mark` — next_review 버그 픽스 | `app/routers/user_state.py:63` | ✅ 완료 |
| `st-click-detector` 패키지 설치 | `.venv` | ✅ 설치됨 |

### 작동 안 되는 것

`click_detector(html, key=...)` 를 호출해도 단어 클릭 시 **반응 없음**.

---

## 원인 추정

### 1. `st-click-detector` 버전 호환 문제 (가장 유력)

- 설치된 버전: `0.1.3` (2022-03-07 릴리스, 2년 이상 업데이트 없음)
- 현재 Streamlit 버전: `1.x` — 내부 컴포넌트 API가 바뀌어 동작 안 할 수 있음
- **확인 방법**: 브라우저 개발자 도구 Console 탭에서 에러 확인

### 2. `href="#"` 링크 클릭 시 페이지 이동 처리

- `click_detector`는 `<a href="#">` 클릭 이벤트를 감지하는 방식
- Streamlit iframe 안에서 `#` 앵커 이동이 이벤트를 가로챌 수 있음

### 3. CSS 변수(`var(--ink)` 등)가 iframe 안에서 미적용

- `click_detector`는 내부적으로 iframe을 사용
- 부모 페이지의 CSS 변수가 iframe 안으로 전달되지 않음
- 단순 렌더링 문제일 수 있음 (클릭은 되지만 보이지 않는 것)

---

## 내일 시도할 해결책

### 방법 A: `st-click-detector-fix` 업그레이드 (빠름, 먼저 시도)

```bash
.venv/Scripts/python -m pip install st-click-detector-fix --no-deps
```

그리고 import 변경:
```python
# streamlit_app.py 상단
from st_click_detector import click_detector  # 현재
# → 패키지에 따라 동일하거나 다를 수 있음, 문서 확인
```

### 방법 B: `st.components.v1.html()` + postMessage 직접 구현 (확실함)

외부 패키지 없이 직접 구현. 아래 코드를 `streamlit_app.py`의 문장 루프에 삽입:

```python
import streamlit.components.v1 as components

def _word_click_component(sentence_html: str, component_key: str) -> str | None:
    """클릭된 word_id를 반환 (없으면 None)"""
    js_html = f"""
    <div id="sentence-wrap">{sentence_html}</div>
    <script>
    document.getElementById('sentence-wrap').addEventListener('click', function(e) {{
        var a = e.target.closest('a[id]');
        if (!a) return;
        e.preventDefault();
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: a.id
        }}, '*');
    }});
    </script>
    """
    result = components.html(js_html, height=60, scrolling=False)
    return result  # Streamlit 컴포넌트 값으로 반환됨
```

> ⚠️ `st.components.v1.html()`은 값을 Python으로 **반환하지 않음**.
> postMessage 방식은 실제로는 단방향이라 세션 상태를 직접 수정할 수 없음.
> → 방법 C가 현실적임.

### 방법 C: URL 쿼리 파라미터 방식 (Streamlit 공식 지원)

```python
# 각 단어 링크를 ?mark=word_id 형태로 만들기
def _build_clickable_html(german, words, marked_ids):
    import re
    result = german
    for w in sorted(words, key=lambda x: len(x.get("german", "")), reverse=True):
        wid = w.get("word_id")
        if wid is None:
            continue
        token = re.escape(w["german"])
        style = "font-weight:700;color:#c98a00;text-decoration:underline" \
                if wid in marked_ids else \
                "border-bottom:1.5px dashed #999;cursor:pointer;text-decoration:none;color:inherit"
        # href를 ?mark= 쿼리로 변경
        link = f'<a href="?mark={wid}" id="{wid}" style="{style}">{w["german"]}</a>'
        result = re.sub(rf'\b{token}\b', link, result)
    return f'<span style="font-size:1.1rem;font-weight:600;line-height:2">{result}</span>'

# 렌더링 직후 쿼리 파라미터 읽기
params = st.query_params
if "mark" in params:
    wid = int(params["mark"])
    # 마킹 처리
    api_post(base_url, "/user-state/words/mark", {"user_id": user_id, "word_id": wid})
    st.session_state[f"ts_marked_{i}"].add(wid)
    st.query_params.clear()  # 파라미터 제거
    st.rerun()
```

> ⚠️ 이 방식은 클릭마다 페이지 이동(네비게이션)이 발생하는 느낌이 있고,
> 문장 인덱스(`i`)와 word_id를 함께 전달해야 함. 파라미터: `?mark=word_id&sent=i`

### 방법 D: 단순히 버튼으로 돌아가기 (확실한 fallback)

기존 칩 버튼 방식이 가장 안정적. 모양만 개선:

```python
# 이전 커밋으로 되돌리거나, 버튼 스타일을 더 작게 조정
n_cols = min(len(words), 6)
cols = st.columns(n_cols)
for j, w in enumerate(words):
    ...
```

---

## 관련 파일

| 파일 | 관련 코드 위치 |
|------|--------------|
| `streamlit_app.py` | `L3` import, `L315` `_build_clickable_html`, `L593-605` click_detector 호출 |
| `app/routers/user_state.py` | `L63` `mark_word_for_review` (next_review 픽스 — 이미 완료) |

---

## 우선순위 권장 순서

1. **방법 A** 먼저 시도 (5분) — 버전만 바꾸면 될 수도
2. 안 되면 **방법 D** (버튼 복원, 확실히 작동) → 이후 여유 있을 때 C 시도
3. **방법 B/C**는 Streamlit 구조상 tricky하므로 시간 여유 있을 때
