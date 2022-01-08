import unittest
from calculations import *

strings = [
        ("Вертолет", "Вертолет"),
        ("Машина", "Я"),
        ("Левенштейна", '')
    ]

texts = [
    "Товарищи! сложившаяся структура организации представляет собой интересный"
    " эксперимент проверки направлений прогрессивного развития. Повседневная п"
    "рактика показывает, что укрепление и развитие структуры обеспечивает широ"
    "кому кругу (специалистов) участие в формировании дальнейших направлений р"
    "азвития.",
    "Равным образом консультация с широким активом требуют определения и уточн"
    "ения модели развития.\nИдейные соображения высшего порядка, а также рамки"
    " и место обучения кадров обеспечивает широкому кругу (специалистов) участ"
    "ие в формировании новых предложений.",
    ''
]
text_results = [
    ["Товарищи!", "сложившаяся", "структура", "организации", "представляет",
     "собой", "интересный", "эксперимент", "проверки", "направлений",
     "прогрессивного", "развития.", "Повседневная", "практика", "показывает,",
     "что", "укрепление", "и", "развитие", "структуры", "обеспечивает",
     "широкому", "кругу", "(специалистов)", "участие", "в", "формировании",
     "дальнейших", "направлений", "развития."],
    ["Равным", "образом", "консультация", "с", "широким", "активом", "требуют",
     "определения", "и", "уточнения", "модели", "развития.", "Идейные",
     "соображения", "высшего", "порядка,", "а", "также", "рамки", "и", "место",
     "обучения", "кадров", "обеспечивает", "широкому", "кругу",
     "(специалистов)", "участие", "в", "формировании", "новых",
     "предложений."],
    []
]


class TestCalculations(unittest.TestCase):

    def test_distance(self):
        self.assertEqual(distance(strings[0][0], strings[0][1]), 0)
        self.assertEqual(distance(strings[1][0], strings[1][1]), 6)
        self.assertEqual(distance(strings[2][0], strings[2][1]), 11)

    def test_imported_distance(self):
        self.assertEqual(Levenshtein.distance(strings[0][0], strings[0][1]), 0)
        self.assertEqual(Levenshtein.distance(strings[1][0], strings[1][1]), 6)
        self.assertEqual(Levenshtein.distance(strings[2][0], strings[2][1]),
                         11)

    def test_simplify(self):
        self.assertEqual(simplify_text(texts[0]), text_results[0])
        self.assertEqual(simplify_text(texts[1]), text_results[1])
        self.assertEqual(simplify_text(texts[2]), text_results[2])

    def test_check_max_length(self):
        self.assertEqual(check_word_len("First"), "First")
        self.assertEqual(check_word_len("Super-Extra-Second"),
                         "Super-Extra-Seco...")
