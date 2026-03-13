"""독일어 핵심 문법 규칙 시드 스크립트 — CEFR A1~C2"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.supabase_client import get_supabase_client

GRAMMAR_RULES = [
    # ──────────── A1 ────────────
    {
        "level": "A1",
        "rule_name": "Bestimmter Artikel",
        "category": "article",
        "explanation": "독일어 명사에는 성(남성/여성/중성)에 따라 정관사 der/die/das가 붙습니다. 명사를 외울 때 반드시 관사를 함께 암기해야 합니다.",
        "examples": [
            "Der Mann trinkt Kaffee. — 남자가 커피를 마신다.",
            "Die Frau liest ein Buch. — 여자가 책을 읽는다.",
            "Das Kind spielt draußen. — 아이가 밖에서 논다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Unbestimmter Artikel",
        "category": "article",
        "explanation": "불특정한 명사 앞에 ein(남성/중성)/eine(여성)를 씁니다. 부정관사는 처음 언급하는 사물에 사용합니다.",
        "examples": [
            "Ich sehe einen Hund. — 나는 개 한 마리를 본다.",
            "Das ist eine Katze. — 이것은 고양이다.",
            "Er hat ein Auto. — 그는 자동차가 있다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Personalpronomen",
        "category": "pronoun",
        "explanation": "인칭대명사: ich(나), du(너), er/sie/es(그/그녀/그것), wir(우리), ihr(너희), sie/Sie(그들/당신).",
        "examples": [
            "Ich bin Student. — 나는 학생이다.",
            "Er kommt aus Korea. — 그는 한국에서 왔다.",
            "Wir lernen Deutsch. — 우리는 독일어를 배운다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Präsens (regelmäßige Verben)",
        "category": "verb",
        "explanation": "규칙 동사 현재형: 어간 + -e/-st/-t/-en/-t/-en 어미를 붙입니다. (예: mach- → ich mache, du machst, er macht)",
        "examples": [
            "Ich mache Hausaufgaben. — 나는 숙제를 한다.",
            "Du spielst Gitarre. — 너는 기타를 친다.",
            "Sie kaufen Lebensmittel. — 그들은 식료품을 산다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "sein und haben",
        "category": "verb",
        "explanation": "sein(~이다)와 haben(가지다)은 불규칙 동사로 매우 자주 쓰입니다. bin/bist/ist/sind/seid/sind, habe/hast/hat/haben/habt/haben.",
        "examples": [
            "Ich bin müde. — 나는 피곤하다.",
            "Er hat einen Bruder. — 그는 남자 형제가 있다.",
            "Wir sind in Berlin. — 우리는 베를린에 있다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Nominativ und Akkusativ",
        "category": "case",
        "explanation": "주격(Nominativ)은 문장의 주어, 목적격(Akkusativ)은 직접목적어. 남성 명사의 정관사가 der→den, 부정관사 ein→einen으로 바뀝니다.",
        "examples": [
            "Der Hund beißt den Mann. — 개가 남자를 문다.",
            "Ich kaufe einen Apfel. — 나는 사과 하나를 산다.",
            "Sie sieht den Film. — 그녀는 영화를 본다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Negation mit nicht und kein",
        "category": "sentence_structure",
        "explanation": "동사·형용사·부사를 부정할 때 nicht, 명사를 부정할 때 kein(e)를 씁니다.",
        "examples": [
            "Ich verstehe das nicht. — 나는 그것을 이해하지 못한다.",
            "Er hat kein Geld. — 그는 돈이 없다.",
            "Das ist keine gute Idee. — 그것은 좋은 생각이 아니다.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "W-Fragen",
        "category": "sentence_structure",
        "explanation": "의문사로 시작하는 질문: wer(누가), was(무엇), wo(어디), wann(언제), warum(왜), wie(어떻게), woher(어디서).",
        "examples": [
            "Wo wohnst du? — 너는 어디에 사니?",
            "Was machst du? — 너는 무엇을 하니?",
            "Wie heißt du? — 너의 이름은 뭐야?",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Ja/Nein-Fragen",
        "category": "sentence_structure",
        "explanation": "동사가 문장 맨 앞으로 오면 예/아니오로 답하는 질문이 됩니다.",
        "examples": [
            "Sprichst du Deutsch? — Ja, ich spreche Deutsch.",
            "Hast du Hunger? — Nein, ich habe keinen Hunger.",
            "Bist du Student? — Ja, ich bin Student.",
        ],
    },
    {
        "level": "A1",
        "rule_name": "Plural der Nomen",
        "category": "noun",
        "explanation": "독일어 명사 복수형은 5가지 패턴(-e, -er, -en/-n, -s, 무변화+움라우트)이 있어 각 단어와 함께 암기해야 합니다.",
        "examples": [
            "das Buch → die Bücher — 책들",
            "die Frau → die Frauen — 여자들",
            "das Auto → die Autos — 자동차들",
        ],
    },
    # ──────────── A2 ────────────
    {
        "level": "A2",
        "rule_name": "Dativ",
        "category": "case",
        "explanation": "여격(Dativ)은 간접목적어에 사용. 관사 변화: der→dem, die→der, das→dem, die(복수)→den(+명사 어미 -n). 전치사 mit/aus/bei/seit/von/zu/nach/gegenüber는 항상 여격.",
        "examples": [
            "Ich helfe dem Mann. — 나는 그 남자를 돕는다.",
            "Sie gibt ihrer Mutter ein Geschenk. — 그녀는 어머니에게 선물을 준다.",
            "Wir wohnen bei einem Freund. — 우리는 친구 집에 산다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Modalverben",
        "category": "verb",
        "explanation": "화법조동사 können(~할 수 있다)/müssen(~해야 한다)/wollen(~하고 싶다)/sollen(~해야 한다)/dürfen(~해도 된다)/möchten(~하고 싶다). 본동사는 문장 끝에 원형으로.",
        "examples": [
            "Ich kann Deutsch sprechen. — 나는 독일어를 말할 수 있다.",
            "Du musst jetzt schlafen. — 너는 지금 자야 한다.",
            "Er möchte Kaffee trinken. — 그는 커피를 마시고 싶다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Perfekt",
        "category": "verb",
        "explanation": "구어체 과거: haben/sein + 과거분사(Partizip II). 이동·상태변화 동사는 sein, 나머지는 haben. 규칙: ge-+어간+-t, 불규칙: ge-+어간+-en.",
        "examples": [
            "Ich habe Kaffee getrunken. — 나는 커피를 마셨다.",
            "Sie ist nach Hause gegangen. — 그녀는 집에 갔다.",
            "Wir haben den Film gesehen. — 우리는 영화를 봤다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Trennbare Verben",
        "category": "verb",
        "explanation": "분리동사: an-/auf-/aus-/ein-/mit-/vor- 등의 전철이 문장에서 분리되어 문장 끝으로 이동합니다.",
        "examples": [
            "Ich stehe um 7 Uhr auf. — 나는 7시에 일어난다.",
            "Sie ruft ihren Freund an. — 그녀는 남자친구에게 전화한다.",
            "Wir machen das Licht aus. — 우리는 불을 끈다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Possessivartikel",
        "category": "article",
        "explanation": "소유관사 mein/dein/sein/ihr/unser/euer/ihr/Ihr는 부정관사와 같은 방식으로 격변화합니다.",
        "examples": [
            "Das ist mein Bruder. — 이 사람은 내 남동생이다.",
            "Wo ist deine Tasche? — 너의 가방은 어디 있어?",
            "Er liebt seine Familie. — 그는 가족을 사랑한다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Präpositionen mit Akkusativ",
        "category": "preposition",
        "explanation": "목적격 전치사: durch(~을 통해)/für(~을 위해)/gegen(~에 반하여)/ohne(~없이)/um(~주위에). 뒤에 오는 명사는 항상 목적격.",
        "examples": [
            "Das Geschenk ist für dich. — 선물은 너를 위한 것이다.",
            "Er geht durch den Park. — 그는 공원을 가로질러 간다.",
            "Ohne einen Plan geht es nicht. — 계획 없이는 안 된다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Imperativ",
        "category": "verb",
        "explanation": "명령형: du형(어간+-e 또는 어간만), ihr형(어간+-t), Sie형(원형+Sie). 분리동사는 전철이 문장 끝으로.",
        "examples": [
            "Komm bitte her! — 이리 와!",
            "Lest das Buch! — 책을 읽어라!",
            "Sprechen Sie bitte langsamer! — 좀 더 천천히 말씀해 주세요!",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Komparativ und Superlativ",
        "category": "adjective",
        "explanation": "비교급: 형용사+-er, 최상급: am+형용사+-sten (또는 관사와 함께 -st-+어미). 불규칙: gut→besser→am besten, viel→mehr→am meisten.",
        "examples": [
            "Berlin ist größer als München. — 베를린은 뮌헨보다 크다.",
            "Das ist das beste Restaurant. — 이것이 최고의 레스토랑이다.",
            "Er läuft schneller als ich. — 그는 나보다 빨리 달린다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Wechselpräpositionen",
        "category": "preposition",
        "explanation": "이중 전치사(an/auf/hinter/in/neben/über/unter/vor/zwischen)는 위치(wo?)일 때 여격, 방향(wohin?)일 때 목적격을 씁니다.",
        "examples": [
            "Das Buch liegt auf dem Tisch. (Dativ, wo?) — 책이 탁자 위에 있다.",
            "Ich lege das Buch auf den Tisch. (Akkusativ, wohin?) — 책을 탁자 위에 놓는다.",
            "Er sitzt neben der Tür. — 그는 문 옆에 앉아 있다.",
        ],
    },
    {
        "level": "A2",
        "rule_name": "Konjunktionen: und/aber/oder/denn",
        "category": "conjunction",
        "explanation": "등위접속사 und(그리고)/aber(그러나)/oder(또는)/denn(왜냐하면)은 두 주절을 연결하며 어순 변화 없습니다.",
        "examples": [
            "Ich lerne Deutsch, aber es ist schwer. — 독일어를 배우지만 어렵다.",
            "Er trinkt Kaffee oder Tee. — 그는 커피나 차를 마신다.",
            "Sie bleibt zu Hause, denn sie ist krank. — 그녀는 집에 있다, 왜냐하면 아프기 때문이다.",
        ],
    },
    # ──────────── B1 ────────────
    {
        "level": "B1",
        "rule_name": "Genitiv",
        "category": "case",
        "explanation": "소유격(Genitiv): 남성/중성 명사에 -s/-es 어미, 관사는 des/der/des/der. 소유 관계나 특정 전치사(wegen/trotz/während/statt) 뒤에 사용.",
        "examples": [
            "Das ist das Auto meines Vaters. — 이것은 아버지의 자동차다.",
            "Wegen des Regens bleiben wir drinnen. — 비 때문에 우리는 실내에 있다.",
            "Die Qualität des Produkts ist gut. — 제품의 품질이 좋다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Konjunktiv II (Gegenwart)",
        "category": "verb",
        "explanation": "접속법 2식 현재: 가정·공손한 표현에 사용. würde+부정사(대부분), 또는 hätte/wäre/könnte/müsste 등 직접 변화형.",
        "examples": [
            "Ich würde gern reisen. — 나는 여행하고 싶다.",
            "Wenn ich Zeit hätte, würde ich kommen. — 시간이 있다면 오겠다.",
            "Könnten Sie mir bitte helfen? — 도와주실 수 있나요?",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Passiv Präsens",
        "category": "verb",
        "explanation": "현재 수동태: werden + 과거분사. 행위자는 von+여격으로 표현(생략 가능). 주어는 행위의 대상.",
        "examples": [
            "Das Haus wird gebaut. — 집이 건축되고 있다.",
            "Der Brief wird geschrieben. — 편지가 쓰여진다.",
            "Die Pizza wird von ihm gemacht. — 피자가 그에 의해 만들어진다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Relativsätze",
        "category": "sentence_structure",
        "explanation": "관계절: 관계대명사(der/die/das, 격변화)가 이끄는 종속절로 명사를 수식. 동사는 관계절 끝으로.",
        "examples": [
            "Der Mann, der dort steht, ist mein Lehrer. — 저기 서 있는 남자가 내 선생님이다.",
            "Das Buch, das ich lese, ist interessant. — 내가 읽는 책은 흥미롭다.",
            "Die Frau, der ich geholfen habe, ist Ärztin. — 내가 도운 여자는 의사다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Nebensätze: weil/dass/wenn/ob",
        "category": "conjunction",
        "explanation": "종속접속사가 이끄는 부문장에서 정동사는 문장 끝으로. weil(왜냐하면)/dass(~것을)/wenn(~할 때, 만약)/ob(~인지).",
        "examples": [
            "Ich lerne Deutsch, weil ich in Deutschland arbeiten möchte. — 독일에서 일하고 싶어서 독일어를 배운다.",
            "Ich weiß, dass er kommt. — 그가 온다는 것을 안다.",
            "Ich frage, ob du Zeit hast. — 네가 시간이 있는지 묻는다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Reflexivverben",
        "category": "verb",
        "explanation": "재귀동사: 주어와 목적어가 동일 인물일 때 재귀대명사(mich/dich/sich/uns/euch/sich) 사용. 재귀대명사가 여격일 경우 mir/dir/sich.",
        "examples": [
            "Ich wasche mich jeden Morgen. — 나는 매일 아침 씻는다.",
            "Er freut sich über das Geschenk. — 그는 선물에 기뻐한다.",
            "Wir treffen uns um 18 Uhr. — 우리는 6시에 만난다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Präteritum",
        "category": "verb",
        "explanation": "서사 과거(문어체): 규칙동사 어간+-te/-test/-te/-ten/-tet/-ten, 불규칙동사는 별도 암기. sein→war, haben→hatte가 특히 중요.",
        "examples": [
            "Er war gestern in Berlin. — 그는 어제 베를린에 있었다.",
            "Sie hatte keine Zeit. — 그녀는 시간이 없었다.",
            "Wir machten einen langen Spaziergang. — 우리는 긴 산책을 했다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Infinitivkonstruktionen mit zu",
        "category": "sentence_structure",
        "explanation": "zu+부정사 구문: 주어가 동일할 때 주절과 연결. 분리동사는 전철+zu+어간. um...zu(~하기 위해), ohne...zu(~하지 않고).",
        "examples": [
            "Ich versuche, Deutsch zu lernen. — 나는 독일어를 배우려고 노력한다.",
            "Er fährt in die Stadt, um einzukaufen. — 그는 쇼핑하기 위해 시내에 간다.",
            "Sie geht weg, ohne zu grüßen. — 그녀는 인사도 없이 떠난다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Adjektivdeklination",
        "category": "adjective",
        "explanation": "형용사 어미변화는 3가지 유형: 정관사 뒤(약변화), 부정관사 뒤(혼합변화), 관사 없이(강변화). 격·성·수에 따라 다름.",
        "examples": [
            "Das ist ein gutes Buch. (혼합) — 이것은 좋은 책이다.",
            "Ich trinke kalten Kaffee. (강변화) — 나는 차가운 커피를 마신다.",
            "Der alte Mann schläft. (약변화) — 그 나이 든 남자는 잔다.",
        ],
    },
    {
        "level": "B1",
        "rule_name": "Futur I",
        "category": "verb",
        "explanation": "미래형: werden + 부정사(문장 끝). 하지만 일상에서는 현재형+시간부사로 미래를 표현하는 경우가 더 많습니다.",
        "examples": [
            "Ich werde morgen kommen. — 나는 내일 올 것이다.",
            "Sie wird das Buch lesen. — 그녀는 책을 읽을 것이다.",
            "Es wird regnen. — 비가 올 것이다.",
        ],
    },
    # ──────────── B2 ────────────
    {
        "level": "B2",
        "rule_name": "Passiv Präteritum und Perfekt",
        "category": "verb",
        "explanation": "과거 수동태: Präteritum은 wurde+과거분사, Perfekt는 sein+과거분사+worden(nicht geworden).",
        "examples": [
            "Das Haus wurde 1900 gebaut. — 그 집은 1900년에 지어졌다.",
            "Der Brief ist gestern geschrieben worden. — 편지는 어제 쓰여졌다.",
            "Die Regel wurde erklärt. — 규칙이 설명되었다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Konjunktiv I (Indirekte Rede)",
        "category": "verb",
        "explanation": "접속법 1식: 간접화법에서 타인의 말을 객관적으로 전달. 현재형은 어간+e 어미. sei/habe/werde가 기본형.",
        "examples": [
            "Er sagt, er sei krank. — 그는 자신이 아프다고 말한다.",
            "Sie behauptet, sie habe das nicht gewusst. — 그녀는 몰랐다고 주장한다.",
            "Der Bericht sagt, die Zahlen seien gestiegen. — 보고서는 수치가 올랐다고 한다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Partizipialkonstruktionen",
        "category": "sentence_structure",
        "explanation": "분사구문: Partizip I(현재분사 -end)은 동시 진행, Partizip II(과거분사)는 완료·수동 의미. 관계절을 압축한 표현.",
        "examples": [
            "Der schlafende Hund ist mein. (= der Hund, der schläft) — 자고 있는 개가 내 것이다.",
            "Das gebaute Haus ist schön. (= das Haus, das gebaut wurde) — 지어진 집이 아름답다.",
            "Die weinende Frau braucht Hilfe. — 울고 있는 여자는 도움이 필요하다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Zweiteilige Konnektoren",
        "category": "conjunction",
        "explanation": "양분 접속사: nicht nur...sondern auch(~뿐만 아니라), entweder...oder(둘 중 하나), weder...noch(~도 ~도 아닌), sowohl...als auch(~와 ~둘 다).",
        "examples": [
            "Er spricht nicht nur Deutsch, sondern auch Englisch. — 그는 독일어뿐만 아니라 영어도 한다.",
            "Entweder kommst du mit, oder du bleibst zu Hause. — 같이 가거나 집에 있거나.",
            "Sie mag weder Kaffee noch Tee. — 그녀는 커피도 차도 좋아하지 않는다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Konzessivangaben",
        "category": "conjunction",
        "explanation": "양보 표현: obwohl/obgleich(~임에도 불구하고, 종속절), trotzdem(그럼에도 불구하고, 주절 부사), zwar...aber(~이긴 하지만).",
        "examples": [
            "Obwohl er müde ist, arbeitet er weiter. — 피곤함에도 불구하고 계속 일한다.",
            "Es regnet; trotzdem gehe ich spazieren. — 비가 오지만 그래도 산책한다.",
            "Er ist zwar reich, aber nicht glücklich. — 부유하긴 하지만 행복하지 않다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Nominalisierung",
        "category": "noun",
        "explanation": "명사화: 동사·형용사를 명사로 변환. 동사는 대문자화하여 das+동사원형, 형용사는 -heit/-keit/-ung/-schaft 접미사 추가.",
        "examples": [
            "das Lernen macht Spaß. (lernen → das Lernen) — 배움은 즐겁다.",
            "die Schönheit der Natur (schön → Schönheit) — 자연의 아름다움.",
            "die Entwicklung der Technologie (entwickeln → Entwicklung) — 기술 발전.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Modalpartikeln",
        "category": "other",
        "explanation": "양태 불변화사(doch/mal/ja/denn/eigentlich/schon 등)는 발화자의 감정·태도를 전달. 번역이 어렵고 문맥에 따라 의미가 다양합니다.",
        "examples": [
            "Komm doch mal vorbei! — 한번 들러봐! (권유)",
            "Das ist ja unglaublich! — 이건 정말 믿을 수 없네! (놀람)",
            "Was machst du denn hier? — 여기서 뭐 하는 거야? (의아함)",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Temporale Nebensätze",
        "category": "conjunction",
        "explanation": "시간 부문장: als(과거 1회 사건)/wenn(현재·반복·조건)/während(동시)/bevor(~전에)/nachdem(~후에, 시제 한 단계 앞섬).",
        "examples": [
            "Als ich jung war, spielte ich viel. — 어렸을 때 많이 놀았다.",
            "Wenn ich nach Hause komme, esse ich. — 집에 오면 먹는다.",
            "Nachdem er gegessen hatte, schlief er. (Plusquamperfekt) — 먹고 난 후 잠을 잤다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Passiversatzformen",
        "category": "verb",
        "explanation": "수동태 대체 표현: sein+zu+부정사(의무·가능성), lassen+sich+부정사(가능성), man+능동문.",
        "examples": [
            "Das Problem ist leicht zu lösen. — 그 문제는 쉽게 해결될 수 있다.",
            "Das lässt sich nicht erklären. — 그것은 설명될 수 없다.",
            "Man spricht hier Deutsch. — 여기서는 독일어를 한다.",
        ],
    },
    {
        "level": "B2",
        "rule_name": "Kausale und finale Angaben",
        "category": "conjunction",
        "explanation": "원인(weil/da/denn)과 목적(um...zu/damit) 표현을 구분. da는 이미 알려진 이유, weil은 새로운 이유, damit은 주어가 다를 때.",
        "examples": [
            "Da er krank ist, kommt er nicht. — 그가 아프므로 오지 않는다.",
            "Er lernt Deutsch, damit seine Kinder ihn verstehen. — 아이들이 이해하도록 독일어를 배운다.",
            "Sie spart Geld, um ein Auto zu kaufen. — 자동차를 사기 위해 저축한다.",
        ],
    },
    # ──────────── C1 ────────────
    {
        "level": "C1",
        "rule_name": "Funktionsverbgefüge",
        "category": "verb",
        "explanation": "기능동사 구문: bringen/kommen/stellen/nehmen 등 의미가 약화된 동사+명사 조합. 단순 동사보다 격식체에서 자주 사용.",
        "examples": [
            "zur Verfügung stellen (= geben/anbieten) — 제공하다",
            "in Frage kommen (= möglich sein) — 고려 대상이 되다",
            "Entscheidungen treffen (= entscheiden) — 결정을 내리다",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Subjektiver Gebrauch der Modalverben",
        "category": "verb",
        "explanation": "화법조동사의 주관적 용법: 추측·가능성 표현. muss(~임에 틀림없다)/kann(~일 수 있다)/könnte(~일지도)/soll(~라고 한다)/will(~라고 주장한다).",
        "examples": [
            "Er muss sehr klug sein. — 그는 매우 똑똑함에 틀림없다.",
            "Sie könnte Recht haben. — 그녀가 옳을 수도 있다.",
            "Er soll Millionär sein. — 그는 백만장자라고 한다.",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Doppelter Infinitiv",
        "category": "verb",
        "explanation": "이중 부정사: 화법조동사나 lassen/sehen/hören이 완료형에서 과거분사 대신 부정사를 사용. haben+부정사+부정사(문장 끝).",
        "examples": [
            "Er hat kommen können. — 그는 올 수 있었다.",
            "Ich habe sie weinen sehen. — 나는 그녀가 우는 것을 보았다.",
            "Sie hat das Paket liefern lassen. — 그녀는 택배를 배달시켰다.",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Erweiterte Partizipialkonstruktionen",
        "category": "sentence_structure",
        "explanation": "확장 분사구: 분사 앞에 부사·목적어 등이 붙어 긴 수식어구 형성. 공식 문서·학술 문체에 자주 등장.",
        "examples": [
            "die von der Regierung eingeführten Maßnahmen — 정부가 도입한 조치들",
            "das seit Jahren diskutierte Problem — 수년째 논의된 문제",
            "ein aus verschiedenen Quellen zusammengestellter Bericht — 여러 출처에서 취합한 보고서",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Adversative und konzessive Konnektoren",
        "category": "conjunction",
        "explanation": "대조·양보 접속 표현: wohingegen/während(대조)/dennoch/gleichwohl(양보)/ungeachtet+Genitiv(~에도 불구하고).",
        "examples": [
            "Er arbeitet viel, wohingegen sie Urlaub macht. — 그는 일을 많이 하는 반면 그녀는 휴가를 보낸다.",
            "Die Lage ist ernst; dennoch bleiben wir ruhig. — 상황이 심각하지만 우리는 침착하다.",
            "Ungeachtet aller Schwierigkeiten hat er es geschafft. — 모든 어려움에도 불구하고 해냈다.",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Irrealer Konditionalsatz",
        "category": "sentence_structure",
        "explanation": "비현실 조건문: wenn+Konjunktiv II (현재 비현실), wenn+Plusquamperfekt Konj.II (과거 비현실). wenn 생략 시 동사가 문두로.",
        "examples": [
            "Wenn ich Geld hätte, würde ich reisen. — 돈이 있다면 여행할 텐데.",
            "Hätte ich mehr gelernt, hätte ich bestanden. — 더 공부했더라면 합격했을 텐데.",
            "Wärst du früher gekommen, hätten wir ihn getroffen. — 일찍 왔더라면 그를 만났을 텐데.",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Graduierung und Einschränkung",
        "category": "other",
        "explanation": "정도 표현·제한: kaum(거의 ~않다)/kaum...als(~하자마자)/soweit/insofern/in gewisser Weise 등 학술·격식체 표현.",
        "examples": [
            "Das ist kaum möglich. — 그것은 거의 불가능하다.",
            "Kaum hatte er das gesagt, als sie weinte. — 그가 말하자마자 그녀가 울었다.",
            "Insofern ist seine Aussage korrekt. — 그런 의미에서 그의 진술은 정확하다.",
        ],
    },
    {
        "level": "C1",
        "rule_name": "Komplexe Genitivkonstruktionen",
        "category": "case",
        "explanation": "복합 소유격: 명사구가 연쇄적으로 이어지는 구조. 공식문서·법률·학술 텍스트에서 사용. 구어체에서는 von+여격으로 대체.",
        "examples": [
            "die Ergebnisse der Untersuchung des Ausschusses — 위원회 조사 결과",
            "die Umsetzung der Strategie des Unternehmens — 기업 전략 실행",
            "im Rahmen des Projekts des Ministeriums — 부처 프로젝트 범위 내에서",
        ],
    },
    # ──────────── C2 ────────────
    {
        "level": "C2",
        "rule_name": "Absolute Konstruktionen",
        "category": "sentence_structure",
        "explanation": "절대 구문: 주절과 문법적으로 독립된 분사/명사구. 주로 격식체·문학체에서 사용하며 시간·조건·원인을 표현.",
        "examples": [
            "Den Kopf gesenkt, trat er ein. — 고개를 숙인 채 그가 들어왔다.",
            "Die Arbeit beendet, verließen sie das Büro. — 일을 마치고 그들은 사무실을 떠났다.",
            "Alles in allem betrachtet, war es ein Erfolg. — 모든 것을 고려할 때 성공이었다.",
        ],
    },
    {
        "level": "C2",
        "rule_name": "Rhetorische Mittel",
        "category": "other",
        "explanation": "수사학적 표현: Litotes(이중부정으로 긍정), Euphemismus(완곡어법), Ellipse(생략), Anapher(반복)을 이해하고 사용.",
        "examples": [
            "Das ist nicht uninteressant. (Litotes = interessant) — 이것은 흥미롭지 않은 것이 아니다.",
            "Er ist von uns gegangen. (Euphemismus = gestorben) — 그는 우리 곁을 떠났다.",
            "Wer wagt, gewinnt. (Ellipse) — 도전하는 자가 이긴다.",
        ],
    },
    {
        "level": "C2",
        "rule_name": "Wissenschaftliche Textstrukturen",
        "category": "sentence_structure",
        "explanation": "학술 문체: 수동태·기능동사구 선호, 명사화 구조, 객관적 거리감 표현(es ist anzumerken/es lässt sich feststellen).",
        "examples": [
            "Es lässt sich feststellen, dass... — ~라는 것을 알 수 있다.",
            "Im Folgenden wird erläutert... — 다음에서 설명된다...",
            "Die Ergebnisse deuten darauf hin, dass... — 결과는 ~임을 시사한다.",
        ],
    },
    {
        "level": "C2",
        "rule_name": "Komplexe Modalitätsausdrücke",
        "category": "verb",
        "explanation": "복합 양태 표현: 화법조동사+주관적용법+완료형 조합, 가능성·추측·의무의 미묘한 차이 구분.",
        "examples": [
            "Er dürfte das gewusst haben. — 그가 그것을 알았을 것이다(추측).",
            "Sie müsste längst angekommen sein. — 그녀는 이미 도착했어야 한다.",
            "Das sollte eigentlich funktionieren. — 원래 작동해야 할 텐데.",
        ],
    },
    {
        "level": "C2",
        "rule_name": "Stilistische Varianz",
        "category": "other",
        "explanation": "문체 다양성: 구어체·문어체·격식체·비격식체를 상황에 맞게 구사. 동일 내용을 다양한 구조로 표현하는 능력.",
        "examples": [
            "구어: Das ist echt schwer. / 문어: Das gestaltet sich äußerst schwierig.",
            "격식: Ich bitte Sie, ... / 비격식: Kannst du bitte...",
            "수동(격식): Es wird gebeten, ... / 능동(구어): Bitte mach...",
        ],
    },
]


def seed():
    supabase = get_supabase_client()

    # 기존 rule_name 목록 조회
    existing = supabase.table("grammar").select("rule_name").execute()
    existing_names = {row["rule_name"].lower() for row in existing.data} if existing.data else set()

    saved, skipped = 0, 0
    for rule in GRAMMAR_RULES:
        if rule["rule_name"].lower() in existing_names:
            print(f"  SKIP  [{rule['level']}] {rule['rule_name']}")
            skipped += 1
            continue
        try:
            supabase.table("grammar").insert({
                "rule_name": rule["rule_name"],
                "category": rule["category"],
                "explanation": rule["explanation"],
                "examples": rule["examples"],
                "level": rule["level"],
            }).execute()
            print(f"  SAVED [{rule['level']}] {rule['rule_name']}")
            saved += 1
            existing_names.add(rule["rule_name"].lower())
        except Exception as e:
            print(f"  ERROR [{rule['level']}] {rule['rule_name']}: {e}")

    print(f"\n완료: {saved}개 저장, {skipped}개 건너뜀")


if __name__ == "__main__":
    seed()
