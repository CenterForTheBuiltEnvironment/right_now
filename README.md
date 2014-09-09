Right Now
=========

A web application for "Right Now" thermal comfort, acceptability, or other surveys. Create surveys dynamically with a customized set of questions and administer the survey privately as the researcher chooses. User interfaces adapt  to the types of questions you include, whether the response is continuous, discrete, or text. Graphical reports are dynamically generated to give a summary of the reponses, and the raw data can be accessed by researchers for more detailed analysis.


Installation
============

Install [Python 2.7](https://www.python.org/download/releases/2.7/) (or check that you have it)

Install pip. See [pip installation](http://pip.readthedocs.org/en/latest/installing.html), or run

```bash
$ curl https://bootstrap.pypa.io/get-pip.py | python
```

Install virtualenv:

```bash
$ pip install virtualenv
```

Clone this repo:

```bash
$ git clone https://github.com/CenterForTheBuiltEnvironment/right_now.git
$ cd right_now
```

Create a virtualenv and activate it:

```bash
$ virtualenv venv
$ . venv/bin/activate
```

Install all of the tool's dependencies:

```bash
$ pip install -r requirements.txt
```

Create the database and load the initial survey modules:

```bash
$ cd right_now
$ python manage.py syncdb
$ python manage.py loaddata survey_init
```

After you run the ``syncdb`` command, you will be prompted to create a superuser. Create one you will remember! You will use these credentials to log into the administration interface and create new surveys.

Deployment note: The development database is SQLite3, which is packaged with Python and doesn't require setup in the installation process. If you are deploying the tool for production use, you will probably want to install a different database, like [Postgres](http://www.postgresql.org/). See [django docs](https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/) to learn how to deploy a Django application with Apache and mod_wdgi.


Using the tool
==============

Right now lets you create acceptability surveys with specific sets of questions (modules). Here we will demonstrate how to log into the admin interface and create modules, questions, and surveys.

Start by running the development server:

```bash
$ python manage.py runserver
```

Visit <http://localhost:8000/admin> and enter the credentials you created during the installation process. You should see an auth table and a survey table. In the survey table, you can see Questions, Modules, and Surveys. If you click on Surveys, you should see an entry for Test Survey. The survey is defined by a name, a list of modules, and a url token. Copy the url token (V6KAU), and visit <http://localhost:8000/survey/V6KAU> to see the survey.

Superusers can also visit <http://localhost:8000/survey> to see a list of surveys.

Users
-----

Users are currently created manually. These accounts allow a researcher to access reports and data of their surveys but not the admin interface. To create a user, log in as superuser and add an entry to the "User" table. Pick a name and password, and click save. The following form can be left unchanged. Just click save again, and you're done.

Users can log in at <http://localhost:8000/survey/login>. The will now be able to access ``/survey/<url token>/csv`` and ``/survey/<token>/report`` resources.


Reports
-------

For each survey, a dynamically generated report can be accessed at ``survey/<url token>/report``. Here you will see each question and a summary of the responses to the question. 

Each survey has a report that is viewable by superusers and users. Get data from the ``survey/<token>/csv`` resource.


Adding a new survey
-------------------

In the survey table admin page <http://localhost:8000/admin/survey/survey/>, you can click "Add survey" in the upper left hand corner. Fill out the name of the survey and a contact email. Select multiple modules by holding down command on a mac or ctrl on a linux or windows machine. Copy the randomly generated url string.

And that's it! Visit ``http://localhost:8000/survey/<url token>`` to see your survey live.

Adding new questions and modules
--------------------------------

In the same way that you added a survey, you can add a module. A module is just a container for questions that you'll define. Visit the Modules table admin page and click "Add module". Give it a name and a description and click save.

Adding questions is where things get more interesting! Visit the Questions table admin page and click "Add question". You'll need to give the question a brief name. See the list of preloaded questions for an idea of how they might look. Next, enter the question text. This is what the user taking the survey will see.

Questions can be either discrete, continuous, text, or special. Discrete questions allow you to give a list of options to give as a response to the question. These questions will be rendered as buttons where the user can select only one. Continuous questions will render a slider and will produce numerical responses in a range.

The choices and value_map fields are general-purpose for both continuous and discrete questions.

For a discrete question, create a list of the choices that will be presented to the user, such as:

```
["choice one", "choice two", "choice three"]
```

value_map will define how those choices are mapped to values that are then stored in the database. For example:

```
[1, 2, 3]
```

will map "choice one" to 1, and so on.

If the question is continous, the choices field will define categories that will be rendered as tick marks and labels on the slider. For example, one could define:

```
["low", "medium", "high"]
```

and it will render those as tick marks uniformly spaced on the slider.

The value_map will be the range that the slider maps to. It will contain two numbers. The first number will be the minimum and the second will be the maximum (slider all the way to the right). To map from 0 to 1, simply: 

```
[0, 1]
```

Text questions don't require choices or value_map, so they can be left as ``null``.

Next, insert the question in a module such as TestModule created above. You can create a survey that contains the TestModule to see your newly created objects in action.

Survey welcome text
-------------------

Currently the welcome text is the same for every survey. Modify the ``welcome.html`` template as necessary.


Special questions and modules (advanced)
----------------------------------------

If you would like to extend Right Now to include a different type of interface to be presented to a user, you can create a special module. The clothing interface is the current example of a special module.

In includes several pieces:
 1. A template for rendering the special interface.
 2. A specific module name
 3. An ``include`` block in the ``survey.html`` template in the ``<!--Special Modules-->`` section. Check the module name against the name of your special module, and include it if it's true.
 4. For each question in the special module, include a block in the ``renderResult`` javascript function found in ``survey.html``. Here you will get the response value to be inserted into the database and associated with the relevant question. For example, we get the response value of the ``SpecialClothingLevel`` question from the clothing picker interface.
 
Todos
=====

 1. Correct clo values for each article in the clothing selector
 2. User should login and see the list of surveys that they have created.
 3. Users should be able to change their password
