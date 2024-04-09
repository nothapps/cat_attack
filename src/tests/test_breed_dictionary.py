import unittest
from unittest.mock import patch, mock_open, call, MagicMock

from cat_attack.breed_dictionary import show_breeds, update_breed_dict, is_breed_id_correct


class TestBreedDictionary(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"Abyssinian": "abys","Aegean": "aege"}',
    )
    @patch("builtins.print")
    def test_show_breeds(self, mock_print: MagicMock, mock_file: MagicMock):
        """
        Tests if the function correctly displays the cat breed list.

        :param mock_print: mocked built-in print function
        :type mock_print: MagicMock
        :param mock_file: mocked built-in open function
        :type mock_file: MagicMock
        """
        show_breeds()
        expected_calls = [
            call("Here's a list of all available cat breeds with their ids:"),
            call("Abyssinian: abys"),
            call("Aegean: aege"),
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch("requests.Session.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_update_breed_dict(self, mock_file: MagicMock, mock_get: MagicMock):
        """
        Tests if the function correctly updates the cat breed dictionary.

        :param mock_file: mocked built-in open function
        :type mock_file: MagicMock
        :param mock_get: mocked requests.Session.get function
        :type mock_get: MagicMock
        """
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "Abyssinian", "id": "abys"},
            {"name": "Aegean", "id": "aege"},
        ]
        mock_get.return_value = mock_response

        update_breed_dict()

        expected_calls: list[call] = mock_file().write.call_args_list
        mock_file().write.assert_has_calls(expected_calls)

    def test_breed_id_correct(self):
        """
        Tests if the function correctly identifies a breed id as valid.
        """
        self.assertTrue(is_breed_id_correct("beng"))

    def test_breed_id_incorrect(self):
        """
        Tests if the function correctly identifies a breed id as invalid.
        """
        self.assertFalse(is_breed_id_correct("bing"))


if __name__ == "__main__":
    unittest.main()
