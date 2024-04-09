# Cat Attack

## Description
Cat Attack is a Python library that finds all `.xlsx` files within a specified folder and adds an "Important" sheet with a random cat picture.

## Installation
To install Cat Attack, you can use the following command:

```bash
cd /your/path/to/cat_attack
poetry install
```

## Usage

#### Attacking Files with Cat Images
To perform an attack on all .xlsx files in a directory:

```bash
cat_attack <folder_path>
```

If you want to use pictures of a specific cat breed:

```bash
cat_attack <folder_path> --breed_id <breed_id>
```

If you want to ignore files that have already been attacked:

```bash
cat_attack <folder_path> --ignore_already_attacked
```

#### Listing Cat Breeds
To list all available cat breeds along with their IDs:

```bash
cat_breeds
```

#### Updating the Breed Dictionary
To update the local cat breed dictionary:

```bash
update_breeds
```

#### Import the library into your script
You can also import the functions directly into your script like so:
```python
from cat_attack.attack import cat_attack
from cat_attack.breed_dictionary import show_breeds, update_breed_dict

# Perform an attack on all .xlsx files in a directory
cat_attack('path/to/your/directory')

# Perform an attack on all .xlsx files in a directory with a specific cat breed
cat_attack('path/to/your/directory', breed_id='beng')

# Perform an attack on all .xlsx files in a directory and ignore files that have already been attacked
cat_attack('path/to/your/directory', ignore_already_attacked=True)

# Show all available cat breeds with their IDs
show_breeds()

# Update the local cat breed dictionary
update_breed_dict()
```

or 
```python
import cat_attack

# Perform an attack on all .xlsx files in a directory
cat_attack.cat_attack('path/to/your/directory')

# Perform an attack on all .xlsx files in a directory with a specific cat breed
cat_attack.cat_attack('path/to/your/directory', breed_id='beng')

# Perform an attack on all .xlsx files in a directory and ignore files that have already been attacked
cat_attack.cat_attack('path/to/your/directory', ignore_already_attacked=True)

# Show all available cat breeds with their IDs
cat_attack.show_breeds()

# Update the local cat breed dictionary
cat_attack.update_breed_dict()
```

