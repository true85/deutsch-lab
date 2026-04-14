"""user_state words/today & today-count (words.created_at 기준) 단위 테스트."""
from unittest.mock import MagicMock

from app.routers import user_state


def test_words_today_list_uses_words_table(monkeypatch):
    """user_word_state가 아닌 words.created_at 기준으로 조회."""
    sb = MagicMock()
    sample = [
        {"id": 10, "lemma": "Haus", "translation": "집", "part_of_speech": "noun", "gender": "das", "created_at": "2026-04-14T01:00:00"},
        {"id": 11, "lemma": "Kind", "translation": "아이", "part_of_speech": "noun", "gender": "das", "created_at": "2026-04-14T00:00:00"},
    ]
    sb.table.return_value.select.return_value.gte.return_value.order.return_value.execute.return_value = MagicMock(data=sample)
    monkeypatch.setattr(user_state, "get_supabase_client", lambda: sb)

    resp = user_state.words_learned_today_list(user_id=1)

    # words 테이블에서 조회했는지
    sb.table.assert_called_with("words")
    assert resp["status"] == "ok"
    assert resp["data"] == sample


def test_words_today_count_ignores_user_id(monkeypatch):
    """현재 설계상 user_id 파라미터는 쿼리에 사용되지 않음 (싱글 유저 가정 고정)."""
    sb = MagicMock()
    sb.table.return_value.select.return_value.gte.return_value.execute.return_value = MagicMock(count=7)
    monkeypatch.setattr(user_state, "get_supabase_client", lambda: sb)

    r1 = user_state.words_learned_today(user_id=1)
    r2 = user_state.words_learned_today(user_id=999)

    assert r1 == r2
    assert r1["data"]["count"] == 7
    # 쿼리 체인에 eq("user_id", ...) 없어야 함
    chain_calls = [c[0] for c in sb.table.return_value.select.return_value.method_calls]
    assert "eq" not in chain_calls


def test_words_today_count_zero_when_none(monkeypatch):
    sb = MagicMock()
    sb.table.return_value.select.return_value.gte.return_value.execute.return_value = MagicMock(count=None)
    monkeypatch.setattr(user_state, "get_supabase_client", lambda: sb)

    resp = user_state.words_learned_today(user_id=1)
    assert resp["data"]["count"] == 0
