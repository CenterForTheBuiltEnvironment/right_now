Right Now
=========

A web application for "Right Now" thermal comfort and acceptability surveys.

Todos:

 1. Correct clo values for each article in the clothing selector
 2. Load default questions if db is empty
 3. Docs


Installation
============

- Install Python 2.7 (or check that you have it)
- Install pip. See [pip installation](http://pip.readthedocs.org/en/latest/installing.html), or run

```bash
$ curl https://bootstrap.pypa.io/get-pip.py | python
```

- Install virtualenv:

```bash
$ pip install virtualenv
```

- Clone this repo:

```bash
$ git clone https://github.com/CenterForTheBuiltEnvironment/right_now.git
$ cd right_now
```

- Create a virtualenv and activate it:

```bash
$ virtualenv venv
$ . venv/bin/activate
```

- Install all of the tool's dependencies:

```bash
$ pip install -r requirements.txt
```

- Create the database and load the initial survey modules:

```bash
$ cd right_now
$ python manage.py syncdb
$ python manage.py loaddata survey_init
```

- After you run the ``syncdb`` command, you will be prompted to create a superuser. Create one you will remember! You will use these credentials to log into the administration interface and create new surveys.

- Deployment. The development database is SQLite3, which is packaged with Python and doesn't require setup in the installation process. If you are deploying the tool for production use, you will probably want to install a different database, like [Postgres](http://www.postgresql.org/). See [django docs](https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/) to learn how to deploy a Django application with Apache and mod_wdgi.
