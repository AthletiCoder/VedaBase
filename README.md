# VedaBase

Search through vedabase themewise!

## Instructions
* `pip install -r requirements.txt` to install all the project dependencies
* add `local_settings.py` to your local `.gitignore` and ensure it's not pushed to the repo
* after installing `mysql` and `mysqlclient` and enter DB credentials appropriately in `local_settings.py`
* run `python manage.py makemigrations` to check if there are any new migrations
* run `python manage.py migrate` to create tables in MySQL DB
* run `python manage.py static_tag_data` to fill tag related data into DB
