from io import BytesIO
from json import JSONDecodeError

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry
from openpyxl.drawing.image import Image

MIN_WIDTH = 640  # minimum size requirement for picture width
MIN_HEIGHT = 480  # minimum size requirement for picture height


def download_cat_pic(url: str, search_params: dict) -> Image | None:
    """
    Attempts to download a cat picture by using TheCatAPI. If the get requests are successful and the image fulfills
    the minimum size requirements it returns an Image object.

    :param url: request url to TheCatAPI
    :type url: str
    :param search_params: search parameters to include in the get request
    :type search_params: dict
    :return: a cat image if the download is successful or None if it fails
    :rtype: Image | None
    """
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist={429, 500, 502, 503, 504}
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))

    while True:
        try:
            response = session.get(url, params=search_params)
            response.raise_for_status()
            response_data: list[dict[str, str | int]] = response.json()
        except (RequestException, JSONDecodeError) as e:
            print(f"Request failed: {e}")
            return None

        image_width: int = response_data[0]["width"]
        image_height: int = response_data[0]["height"]

        if image_width >= MIN_WIDTH and image_height >= MIN_HEIGHT:
            image_url: str = response_data[0]["url"]

            try:
                image_response = session.get(image_url)
                image_response.raise_for_status()
                cat_image = Image(BytesIO(image_response.content))
                return cat_image
            except (RequestException, OSError) as e:
                print(f"Image download failed: {e}")
                return None
