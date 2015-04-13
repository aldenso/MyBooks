MyBooks
=======

This is an example of Python and Flask that shows how to create a site to store
information about books.

Is not the most sophisticated work in flask, but it works pretty well.

Components:
Python2, Flask, Bootstrap, Jquery, OpenID, SQLAlchemy

First create an env to deploy the site and install the requirements.

    # mkdir -p /mytestsites/myflaskapp; cd /mytestsites
    # virtualenv myvirtualenv
    or if you have python2 and python3, make sure to use python2
    # virtualenv2 myvirtualenv

Clone the App from github.

    # cd myflaskapp
    # git clone https://github.com/aldenso/MyBooks

Activate the virtualenv.

    # source ../myvirtualenv/bin/activate

Install the requirements for python.

    (myvirtualenv)# pip install -r requirements.txt

Make sure to validate or fix the shebang path for the "db_*" and "run" scripts.

    must be something like "#!../myvirtualenv/bin/python"

Create the database for the app.

    (myvirtualenv)# ./db_create.py

That's it, now you can run the app and test it with your browser.

    (myvirtualenv)# ./run.py

    http://127.0.0.1:5000