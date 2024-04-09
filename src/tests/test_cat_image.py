import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO

from PIL import Image
import openpyxl.drawing.image
from requests.exceptions import RequestException

from cat_attack.cat_image import download_cat_pic

TEST_URL = "http://test.com"
TEST_PARAMS = {"param": "value"}
TEST_JSON_RETURN = [{"width": 800, "height": 600, "url": TEST_URL + "/cat.png"}]


class TestDownloadCatPic(unittest.TestCase):
    @patch("requests.Session")
    def test_download_success(self, mock_session: MagicMock):
        """
        Tests successful image download.

        :param mock_session: mocked requests.Session.get function
        :type mock_session: MagicMock
        """
        session_instance: MagicMock = mock_session.return_value

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = TEST_JSON_RETURN

        mock_image_response = MagicMock()
        mock_image_response.raise_for_status.return_value = None

        test_image = Image.new("RGB", (5, 5))
        image_io = BytesIO()
        test_image.save(image_io, format="PNG")
        image_data = image_io.getvalue()

        mock_image_response.content = image_data

        session_instance.get.side_effect = [mock_response, mock_image_response]

        result = download_cat_pic(TEST_URL, TEST_PARAMS)

        self.assertIsInstance(result, openpyxl.drawing.image.Image)

    @patch("requests.Session")
    def test_failed_request(self, mock_session: MagicMock):
        """
        Tests the behavior when the initial request from TheCatAPI fails.

        :param mock_session: mocked requests.Session.get function
        :type mock_session: MagicMock
        """
        session_instance: MagicMock = mock_session.return_value
        mock_response = MagicMock()

        mock_response.raise_for_status.side_effect = RequestException("Failed successfully")

        session_instance.get.side_effect = [mock_response]

        result = download_cat_pic(TEST_URL, TEST_PARAMS)

        self.assertIsNone(result)

    @patch("requests.Session")
    def test_failed_download(self, mock_session: MagicMock):
        """
        Tests the behavior when the request to download a cat image fails.

        :param mock_session: mocked requests.Session.get function
        :type mock_session: MagicMock
        """
        session_instance = mock_session.return_value

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = TEST_JSON_RETURN

        mock_image_response = MagicMock()
        mock_image_response.raise_for_status.side_effect = RequestException("Failed successfully")

        session_instance.get.side_effect = [mock_response, mock_image_response]

        result = download_cat_pic(TEST_URL, TEST_PARAMS)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
