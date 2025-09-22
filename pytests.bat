cd render_manager/tests
pipenv run coverage run --source=render_manager -m pytest -v . 
pipenv run coverage report --omit='*/lib/site-packages/*,*/main.py,*tests/*,*/__init__.py,*/mvc/*.py'
pipenv run coverage html --omit='*/lib/site-packages/*,*/main.py,*/tests/*,*/__init__.py,*/mvc/*.py'