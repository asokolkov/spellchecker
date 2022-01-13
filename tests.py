import unittest
from calculations import *
from files import *

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

    def test_get_coords(self):
        self.assertEqual(get_coords("консультация", texts[1]),
                         ('1.15', '1.27'))
        self.assertEqual(get_coords("Идейные", texts[1]), ('2.0', '2.7'))
        self.assertEqual(get_coords("", texts[1]), ('1.0', '1.0'))

    def test_compress_coords(self):
        self.assertEqual(compress_coords("1.1", "1.6"), ('1.2', '1.5'))
        self.assertEqual(compress_coords("1.1", "2.4"), ('1.2', '2.3'))

    def test_text_to_array(self):
        self.assertEqual(
            text_to_array(
                "1;ob234b 1ou3b4njo \n g-345t -g3w45 q34x,1.34"),
            ['1;ob234b', '1ou3b4njo', 'g-345t', '-g3w45', 'q34x,1.34'])
        self.assertEqual(text_to_array(""), [])

    def test_get_best_word(self):
        self.assertEqual(
            get_best_word("уточнния", sorted(text_results[1], reverse=True),
                          "Imported"),
            "уточнения")
        self.assertEqual(
            get_best_word("уточнения", sorted(text_results[1], reverse=True),
                          "Imported", except_word="уточнения"),
            "обучения")
        self.assertEqual(
            get_best_word("уточнния", sorted(text_results[1], reverse=True),
                          "Handmaid"),
            "уточнения")
        self.assertEqual(
            get_best_word("уточнения", sorted(text_results[1], reverse=True),
                          "Handmaid", except_word="уточнения"),
            "обучения")

    def test_read_file(self):
        x = read_file("dictionary.txt")
        self.assertEqual((x[50], x[27]), ('particularly', 'demonstration'))
        self.assertEqual(read_file("d.txt"), None)
        append_file("dictionary.txt", x)

    def test_file_to_dict(self):
        self.assertEqual(file_to_dict(),
                         {'dict_name': 'dictionary.txt', 'method': 'Imported'})
