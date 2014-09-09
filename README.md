Right Now
=========

A web application for "Right Now" thermal comfort and acceptability surveys.

Todos:

 1. Correct clo values for each article in the clothing selector
 2. Load default questions if db is empty
 3. Docs


Installation
============

1. Install Python 2.7 (or check that you have it)
2. Install pip. See [link](http://google.com) for instructions, or run

```bash
$ curl https://bootstrap.pypa.io/get-pip.py | sudo python
```

3. Install virtualenv:

```bash
$ pip install virtualenv
```

4. Clone this repo:

```bash
$ git clone https://github.com/CenterForTheBuiltEnvironment/right_now.git
$ cd right_now
```

5. Create a virtualenv and activate it:

```bash
$ virtualenv venv
$ . venv/bin/activate
```

6. Install all of the tool's dependencies:

```bash
$ pip install -r requirements.txt
```

7. Create the database and load the initial survey modules:

```bash
$ cd right_now
$ python manage.py syncdb
$ python manage.py loaddata survey_init
```

After you run the ``syncdb`` command, you will be prompted to create a superuser. Create one you will remember! You will use these credentials to log into the administration interface and create new surveys.

8. Deployment. The development database is SQLite3, which is packaged with Python and doesn't require setup in the installation process. If you are deploying the tool for production use, you will probably want to install a different database, like Postgres.
