import click
import os

from cat_attack.file_manipulation import find_xlsx_files, attack_file
from cat_attack.breed_dictionary import is_breed_id_correct


@click.command()
@click.argument("folder_path")
@click.option("--breed_id", default=None)
@click.option("--ignore_already_attacked", is_flag=True, default=False)
def cat_attack_command(folder_path: str, breed_id: str = None, ignore_already_attacked: bool = False):
    """
    This function creates the command line interface for the cat_attack function.

    :param folder_path: path to a directory presumably containing .xlsx files
    :type folder_path: str
    :param breed_id: id of a cat breed, optional
    :type breed_id: str
    :param ignore_already_attacked: whether a file has already been attacked (has an "Important" sheet), optional
    :type ignore_already_attacked: bool
    """
    cat_attack(folder_path, breed_id, ignore_already_attacked)


def cat_attack(folder_path: str, breed_id: str = None, ignore_already_attacked: bool = False):
    """
    Performs an attack on all found .xlsx files. For each file it adds an "Important" sheet with a random cat image.
    If breed_id is provided the function will add it to the search params which results in a download of only pictures
    of that specific cat breed. It can also optionally ignore files that have already been modified.

    :param folder_path: path to a directory presumably containing .xlsx files
    :type folder_path: str
    :param breed_id: id of a cat breed, optional
    :type breed_id: str
    :param ignore_already_attacked: whether a file has already been attacked (has an "Important" sheet), optional
    :type ignore_already_attacked: bool
    """
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("No API KEY set.")

    search_params = {
        "api_key": "5a76a74a-50ae-4419-9694-ed1908365407",
        "size": "med,full",
        "mime_types": "jpg,png",
    }

    if breed_id is not None:
        search_params["breed_id"] = breed_id
        if not is_breed_id_correct(breed_id):
            print("The breed id you entered isn't in the breed id list.")
            exit()

    found_files = find_xlsx_files(folder_path)

    for file in found_files:
        attack_file(file, search_params, ignore_already_attacked)

    if found_files:
        print("Cats finished attacking all your files 😼")
