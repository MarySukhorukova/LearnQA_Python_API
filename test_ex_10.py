class TestNumberSymbols:

    def test_check_number_of_symbols(self):
        simple_phrase = input("Set a phrase: ")
        expected_sum = 15
        assert len(simple_phrase) <= expected_sum, f"symbols is more than {expected_sum}"