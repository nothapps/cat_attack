import os
import json
from json import JSONDecodeError

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

BREEDS_URL = "http://api.thecatapi.com/v1/breeds"


def show_breeds():
    """
    Shows a list of available cat breeds along with their ids by reading a JSON file containing a dictionary.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(script_dir, "breed_dict.json")

    with open(json_path, "r") as file:
        breed_dict: dict[str, str] = json.load(file)

    print("Here's a list of all available cat breeds with their ids:")

    for name, cat_id in breed_dict.items():
        print(f"{name}: {cat_id}")


def update_breed_dict():
    """
    Updates the JSON file containing a dictionary of cat breeds and their ids by sending a get request to TheCatAPI,
    downloading the current list of breeds and saving them in the file.
    """
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist={429, 500, 502, 503, 504}
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(BREEDS_URL)
        response.raise_for_status()
        response_data: list[dict[str, str | int]] = response.json()
    except (RequestException, JSONDecodeError) as e:
        print(f"Request failed: {e}.\nUpdate unsuccessful.")
    else:
        breed_dict = {}

        for cat_breed in response_data:
            name: str = cat_breed["name"]
            cat_id: str = cat_breed["id"]
            breed_dict[name] = cat_id

        script_dir = os.path.dirname(os.path.realpath(__file__))
        json_path = os.path.join(script_dir, "breed_dict.json")

        with open(json_path, "w") as file:
            json.dump(breed_dict, file)


def is_breed_id_correct(breed_id: str) -> bool:
    """
    Checks if given breed id exists in the JSON file containing the breed dictionary.

    :param breed_id: id of a cat breed
    :type breed_id: str
    :return: if breed id is in the dictionary
    :rtype: bool
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(script_dir, "breed_dict.json")

    with open(json_path, "r") as file:
        breed_dict: dict[str, str] = json.load(file)
    all_breed_ids = breed_dict.values()

    return breed_id in all_breed_ids
