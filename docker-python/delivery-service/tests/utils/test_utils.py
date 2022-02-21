from datetime import datetime

from src.utils import utils

# Tests para las funciones utilitarias.

class TestUtils:

    def test_filter_dict(self):

        dict = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
        }

        fields = [
            "A",
            "B",
        ]

        filtered_dict = utils.filter_dict(dict, fields)

        assert list(filtered_dict.keys()) == fields
        assert filtered_dict.get("A") == 1
        assert filtered_dict.get("B") == 2
        assert filtered_dict.get("C") == None
        assert filtered_dict.get("D") == None

    def test_format_date(self):

        test_date = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 13, microsecond = 321654)
        
        resulting_date = utils.format_date(test_date)
        expected_date = "2021-12-25 10:24:13"

        assert resulting_date == expected_date