"""
Cat Attack is a Python library that finds all .xlsx files within a specified folder and adds an "Important" sheet
with a random cat picture.

![cat](https://cdn2.thecatapi.com/images/381.jpg)
"""

from cat_attack.attack import cat_attack
from cat_attack.breed_dictionary import show_breeds, update_breed_dict
from cat_attack.cat_image import download_cat_pic
from cat_attack.file_manipulation import find_xlsx_files, attack_file
