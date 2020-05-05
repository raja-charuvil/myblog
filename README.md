Myblog
===========

Source code for my personal blog. Developed using Python Flask framework.

Requirements
------------

- Python 3.7
- virtualenv (`pip install virtualenv`)

Installation [Windows]
------------

1. Clone the repository to local

	$ `git clone https://github.com/raja-charuvil/myblog.git`

2. cd into `myblog`

	$ `cd myblog`

3. Create a virtual environment and install the required packages with the following commands:

    $ virtualenv venv
    $ venv\Scripts\activate

4. Install dependencies

    (venv) $ pip install -r requirements.txt

Running the Examples
--------------------

With the virtual environment activated you can `cd` into `myblog` then following commands.

	$ set FLASK_APP=myblog.py
	$ flask db upgrade (to create database tables)
	$ flask create_admin (to create an admin user for the blog)
	$ flask run 
