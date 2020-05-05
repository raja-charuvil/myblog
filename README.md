Myblog
===========

Source code for my personal blog. Developed using Python Flask framework.

Requirements
------------

- Flask (`pip install flask`)
- Flask-Bootstrap (`pip install flask-bootstrap`)
- Flask-WTF (`pip install flask-wtf`)

Installation
------------

You can create a virtual environment and install the required packages with the following commands:

    $ virtualenv venv
    $ . venv/bin/activate
    (venv) $ pip install -r requirements.txt

Running the Examples
--------------------

With the virtual environment activated you can `cd` into `myblog` then following commands.

	$ set FLASK_APP=myblog.py
	$ flask create_admin (to create an admin user for the blog)
	$ flask run 
