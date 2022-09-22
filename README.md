# Something game

## About code

In code I use unittest framework. The best solve for writing tests the same in JUint in java is create in all directories in test folder `__init__.py` files for creating modules. 

All tests starts with `test` prefix. Example: `test_hero.py`

For any class creating new file. Title of file named with lover case with `_` as delimiter.

## Commands for development

```shell
python -m venv env              # create enviroment
source env/bin/activate         # activate enviroment (for linux)
deactivate                      # deactivate enviroment 
pip install -r requirements.txt # load libraries from requirements.txt
pip freeze > requirements.txt   # create new file requirements.txt
python main.py                  # start project
python3 -m unittest discover    # run all tests

```
