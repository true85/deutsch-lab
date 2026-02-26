import os
os.environ["APP_ENV"] = "test"

from app.routers.analysis import _tokenize, _compound_lemma


class TestTokenize:
    def test_basic_words(self):
        assert _tokenize("Ich gehe nach Hause") == ["Ich", "gehe", "nach", "Hause"]

    def test_umlaut(self):
        tokens = _tokenize("Mädchen öffnet die Tür")
        assert "Mädchen" in tokens
        assert "öffnet" in tokens
        assert "Tür" in tokens

    def test_eszett(self):
        tokens = _tokenize("Ich heiße Müller")
        assert "heiße" in tokens

    def test_hyphen_compound_kept_as_one(self):
        tokens = _tokenize("Das ist ein Vor-Ort-Termin")
        assert "Vor-Ort-Termin" in tokens
        # 하이픈으로 분리된 개별 토큰이 없어야 함
        assert "Vor" not in tokens
        assert "Termin" not in tokens

    def test_nord_sued_compound(self):
        tokens = _tokenize("Der Nord-Süd-Dialog ist wichtig")
        assert "Nord-Süd-Dialog" in tokens

    def test_single_char_filtered(self):
        tokens = _tokenize("A B C Hallo")
        assert "A" not in tokens
        assert "B" not in tokens
        assert "Hallo" in tokens

    def test_punctuation_ignored(self):
        tokens = _tokenize("Guten Morgen, wie geht's?")
        assert "Guten" in tokens
        assert "Morgen" in tokens
        assert "," not in tokens

    def test_numbers_ignored(self):
        tokens = _tokenize("Er ist 25 Jahre alt")
        assert "25" not in tokens
        assert "Jahre" in tokens

    def test_empty_string(self):
        assert _tokenize("") == []

    def test_abbr_dot_not_split_sentence(self):
        # 약어 마침표로 인해 다음 단어가 분리되지 않아야 함
        tokens = _tokenize("Das kostet z.B. viel Geld")
        assert "Geld" in tokens


class TestCompoundLemma:
    def test_simple_word(self):
        assert _compound_lemma("Hause") == "hause"

    def test_hyphen_compound(self):
        assert _compound_lemma("Vor-Ort-Termin") == "termin"

    def test_two_part_compound(self):
        assert _compound_lemma("Nord-Süd") == "süd"

    def test_lowercase_result(self):
        assert _compound_lemma("GROSS") == "gross"
