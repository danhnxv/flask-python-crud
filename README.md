# Initial database
`flask db init`

# Do migration
`flask db migrate` \
`flask db upgrade`

# install dependencies
`pip install -r requirements.txt`

# run app
`flask run`


# run tests
1. create database: `todo_test`
2. run tests
`pipenv run pytest -x`

# enable debug mode in flask v2.x
`export FLASK_ENV=true` or run app with `flask run --debug`