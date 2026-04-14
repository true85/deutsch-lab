"""teacher.py 단위 테스트 (Supabase/OpenAI 목킹)."""
from unittest.mock import MagicMock

import pytest

from app.routers import teacher


def test_extract_used_lemmas_basic():
    sentences = [
        {"words": [{"german": "gehen"}, {"german": "Freund"}]},
        {"words": [{"german": "Haus"}]},
    ]
    assert teacher._extract_used_lemmas(sentences) == {"gehen", "freund", "haus"}


def test_extract_used_lemmas_empty_and_missing_fields():
    assert teacher._extract_used_lemmas([]) == set()
    assert teacher._extract_used_lemmas([{"words": []}]) == set()
    assert teacher._extract_used_lemmas([{}]) == set()
    assert teacher._extract_used_lemmas([{"words": [{"german": ""}, {"german": "  Kind  "}]}]) == {"kind"}


def _mock_supabase_no_existing():
    """`_save_word_to_db`용 — 기존 lemma 없음, insert 성공."""
    sb = MagicMock()
    # select().ilike().limit().execute() → 비어있음
    sb.table.return_value.select.return_value.ilike.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
    # insert().execute() → id=42
    sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 42}])
    return sb


def test_save_word_to_db_existing_skips_insert_and_embedding(monkeypatch):
    sb = MagicMock()
    sb.table.return_value.select.return_value.ilike.return_value.limit.return_value.execute.return_value = MagicMock(data=[{"id": 7}])
    embed_called = {"n": 0}
    monkeypatch.setattr(teacher, "get_embedding", lambda _: embed_called.__setitem__("n", embed_called["n"] + 1) or [0.1])

    result = teacher._save_word_to_db({"german": "Freund"}, "A1", sb)
    assert result == 7
    assert embed_called["n"] == 0
    sb.table.return_value.insert.assert_not_called()


def test_save_word_to_db_new_includes_embedding(monkeypatch):
    sb = _mock_supabase_no_existing()
    monkeypatch.setattr(teacher, "get_embedding", lambda _: [0.1, 0.2, 0.3])

    result = teacher._save_word_to_db({"german": "Haus", "translation": "집"}, "A1", sb)
    assert result == 42
    payload = sb.table.return_value.insert.call_args[0][0]
    assert payload["lemma"] == "Haus"
    assert payload["embedding"] == [0.1, 0.2, 0.3]


def test_save_word_to_db_embedding_failure_still_inserts(monkeypatch):
    sb = _mock_supabase_no_existing()

    def boom(_):
        raise RuntimeError("OpenAI down")

    monkeypatch.setattr(teacher, "get_embedding", boom)

    result = teacher._save_word_to_db({"german": "Kind"}, "A1", sb)
    assert result == 42
    payload = sb.table.return_value.insert.call_args[0][0]
    assert "embedding" not in payload  # 실패 시 embedding 키 없이 insert


def _build_profile_stub(review_due):
    return {
        "current_level": "A1",
        "avg_mastery": 0.5,
        "known_lemmas": [],
        "weak_word_lemmas": [],
        "weak_grammar_rules": [{"rule_name": "dummy", "explanation": ""}],
        "review_due_lemmas": review_due,
    }


def test_generate_sentences_retries_when_coverage_below_target(monkeypatch):
    """review_due 3개 중 0개만 커버되면 재시도가 발생하고, 재시도가 더 많이 커버하면 result가 교체된다."""
    calls = {"n": 0}

    def fake_chat_json(_sys, _user, **_kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return {"sentences": [{"german": "Ich gehe.", "words": [{"german": "gehen"}]}]}
        return {"sentences": [
            {"german": "s1", "words": [{"german": "gehen"}, {"german": "Haus"}]},
            {"german": "s2", "words": [{"german": "Kind"}, {"german": "Freund"}]},
        ]}

    monkeypatch.setattr(teacher, "chat_json", fake_chat_json)
    monkeypatch.setattr(teacher, "_build_user_profile",
                        lambda _uid: _build_profile_stub(["Haus", "Kind", "Freund"]))
    sb = MagicMock()
    sb.table.return_value.select.return_value.ilike.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
    monkeypatch.setattr(teacher, "get_supabase_client", lambda: sb)
    monkeypatch.setattr(teacher, "_save_word_to_db", lambda *_a, **_kw: None)
    monkeypatch.setattr(teacher, "_upsert_word_state", lambda *_a, **_kw: None)
    monkeypatch.setattr(teacher, "_fallback_words", lambda *_a, **_kw: [])

    req = MagicMock(user_id=1, count=2)
    resp = teacher.generate_sentences(req)

    assert calls["n"] == 2
    cov = resp["data"]["review_coverage"]
    assert cov["target"] == 3
    assert cov["actual"] == 3
    assert cov["missing"] == []


def test_generate_sentences_no_retry_when_coverage_met(monkeypatch):
    calls = {"n": 0}

    def fake_chat_json(_sys, _user, **_kw):
        calls["n"] += 1
        return {"sentences": [
            {"german": "s1", "words": [{"german": "Haus"}]},
            {"german": "s2", "words": [{"german": "Kind"}]},
            {"german": "s3", "words": [{"german": "Freund"}]},
        ]}

    monkeypatch.setattr(teacher, "chat_json", fake_chat_json)
    monkeypatch.setattr(teacher, "_build_user_profile",
                        lambda _uid: _build_profile_stub(["Haus", "Kind", "Freund"]))
    sb = MagicMock()
    sb.table.return_value.select.return_value.ilike.return_value.limit.return_value.execute.return_value = MagicMock(data=[])
    monkeypatch.setattr(teacher, "get_supabase_client", lambda: sb)
    monkeypatch.setattr(teacher, "_save_word_to_db", lambda *_a, **_kw: None)
    monkeypatch.setattr(teacher, "_upsert_word_state", lambda *_a, **_kw: None)
    monkeypatch.setattr(teacher, "_fallback_words", lambda *_a, **_kw: [])

    req = MagicMock(user_id=1, count=3)
    resp = teacher.generate_sentences(req)

    assert calls["n"] == 1  # 재시도 없음
    assert resp["data"]["review_coverage"]["actual"] == 3


def test_generate_sentences_zero_review_due_no_coverage_check(monkeypatch):
    """review_due=[]일 때 coverage 재시도는 없지만, 학습 가치 룰은 여전히 적용."""
    calls = {"n": 0}

    def fake_chat_json(_sys, _user, **_kw):
        calls["n"] += 1
        # 신규 단어 1개로 학습 가치 충족
        return {"sentences": [{"german": "Ich kaufe ein Buch.",
                               "words": [{"german": "Buch", "is_new": True}]}]}

    monkeypatch.setattr(teacher, "chat_json", fake_chat_json)
    monkeypatch.setattr(teacher, "_build_user_profile",
                        lambda _uid: _build_profile_stub([]))
    sb = MagicMock()
    monkeypatch.setattr(teacher, "get_supabase_client", lambda: sb)
    monkeypatch.setattr(teacher, "_save_word_to_db", lambda *_a, **_kw: None)
    monkeypatch.setattr(teacher, "_fallback_words", lambda *_a, **_kw: [])

    req = MagicMock(user_id=1, count=1)
    resp = teacher.generate_sentences(req)

    assert calls["n"] == 1
    cov = resp["data"]["review_coverage"]
    assert cov["target"] == 0
    assert cov["actual"] == 0
    lv = resp["data"]["learning_value"]
    assert lv["valuable"] == 1
    assert lv["valueless_indices"] == []


def test_generate_sentences_retries_when_learning_value_missing(monkeypatch):
    """모든 단어가 known이고 review_due 없을 때: 학습가치 0 → 재시도 발생."""
    calls = {"n": 0}

    def fake_chat_json(_sys, _user, **_kw):
        calls["n"] += 1
        if calls["n"] == 1:
            # 모두 known, is_new 없음 → 학습 가치 0
            return {"sentences": [{"german": "s", "words": [{"german": "ich"}]}]}
        # 재시도: 신규 단어 포함
        return {"sentences": [{"german": "s2",
                               "words": [{"german": "Buch", "is_new": True}]}]}

    monkeypatch.setattr(teacher, "chat_json", fake_chat_json)
    monkeypatch.setattr(teacher, "_build_user_profile",
                        lambda _uid: {**_build_profile_stub([]), "known_lemmas": ["ich"]})
    sb = MagicMock()
    monkeypatch.setattr(teacher, "get_supabase_client", lambda: sb)
    monkeypatch.setattr(teacher, "_save_word_to_db", lambda *_a, **_kw: None)
    monkeypatch.setattr(teacher, "_fallback_words", lambda *_a, **_kw: [])

    req = MagicMock(user_id=1, count=1)
    resp = teacher.generate_sentences(req)

    assert calls["n"] == 2
    assert resp["data"]["learning_value"]["valuable"] == 1
