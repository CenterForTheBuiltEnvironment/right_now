Right Now
=========

A web application for "Right Now" thermal comfort, acceptability, or other surveys. Create surveys dynamically with a customized set of questions and administer the survey privately as the researcher chooses. User interfaces adapt to the types of questions you include, whether the response is continuous, broken scale, discrete, multiple choice, text. Graphical reports are dynamically generated to give a summary of the reponses, and the raw data can be accessed by researchers for more detailed analysis.


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

When you're ready to test or use the tool locally, run the development server:

```bash
$ python manage.py runserver
```

Visit <http://localhost:8000/> and enter the credentials you created during the installation process to log in. Now you can create and manage surveys, custom questions, and invite codes.

*Deployment note: The development database is SQLite3, which is packaged with Python and doesn't require setup in the installation process. If you are deploying the tool for production use, you will probably want to install a different database, like [Postgres](http://www.postgresql.org/). See [django docs](https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/) to learn how to deploy a Django application with Apache and mod_wdgi.*

Using the tool
==============

Surveys
-------

After you log in, you're directed to a list of the surveys you've created. Create a new one by clicking the "Create new survey" button. This will direct you to the survey form.

Complete the form, keeping in mind that you must give your survey a name. New surveys are typically marked as "Active". When the survey is complete and you don't want occupants to be able to take the survey any longer, you can make the survey inactive. The lead text is displayed in the large box when the respondent navigates to the survey. Below the "Begin survey" button is the welcome text, a longer, more detailed explanatory text about the survey you're administering. The thank you text is displayed when the user completes the survey.

In all of the text fields, you may include HTML if you want to have custom links or formatting.

Next, choose the questions you want to include in the survey. Click "View questions" to see the questions available, and then choose them by name in the dropdown menus. Click "+Add row" as many times as needed to get the number of questions you want to include. You may also mark the questions as mandatory.

Once you're done, click "Submit". You'll be sent back to the survey index page, where you can view the survey link, view a report of the survey responses so far, download the raw data, or edit any property of the survey.

Questions
---------

Click "Questions" in the navigation bar at the top of the screen to go to the question index. Here you'll see a list of custom questions you've created, and below a list of the core questions that are available to all users. Click the view icon to see detailed information about the question. Custom questions can also be edited. Below custom questions you can find a button to create new questions.

*Tip: If you want to change the wording or other aspect of a core question, simply create a new one, copy the contents of the core question, and make modifications.*

Start by giving your question a name that is short enough to be easy to remember or recognize, but long enough to be unique. Enter the text of the question you want to ask.

There are five basic types of questions: **Continuous, Acceptability, Discrete, Multiple, and Text**.

Continuous questions 
--------------------

These questions will render a slider that will provide user input in a range. The report will render a histogram of the responses collected.

Enter a list of labels for the slider to be spaced uniformly along the length of the slider. It's recommended that you provide 2 - 5 labels. Labels must be input exactly in the following format:

```
["label1", "label2", "label3", "label4", "label5"]
```

Be sure to include the square brackets, and surround your labels with **double quotes**.

In the value map field, enter the range that you want the slider input to be mapped to, in the format [minimum, maximum]. For example, the following will map the slider responses to a range of negative 3 to positive 3.

```
[-3, 3]
```

Acceptability questions
-----------------------

These questions will render a vertical slider representing a broken scale. The respondent must move the slider to the top or bottom of the slider.

Acceptability questions **must have exactly 4 labels**. Otherwise, they are formatted as above. The value map field is the same as in continous questions.

Discrete questions
------------------

Discrete questions will render a radio button interface. The user chooses exactly **one** response. For the ability to choose more than one, see "Multiple questions" below.

Enter the choices that the user can pick from. One button will be rendered per choice. You can have as many as you need, but I recommend having as few as possible.

```
["choice1", "choice2", "choice3"]
```

In the value map field, enter the numbers that you want each choice to be mapped to, respectively.

```
[1, 2, 3]
```

If the user picks "coice1" will be entered as "1" in the database.

Multiple choice questions
-------------------------

These are exactly like discrete questions, except the user can pick multiple responses. The raw data will contain a list of the choices that the user selected, instead of a single numerical value.

Text questions
--------------

These questions will provide the user a text field for an open-ended response.

Text questions don't require choices or value_map, so they can be left as ``null``.

Special clothing interface
--------------------------

To include a clothing ensemble question in your survey, include the "SpecialClothingLevel" question. 

To add other specialized intefaces, you'll need the following pieces (advanced):
 1. A template for rendering the special interface.
 2. A specific question name.
 3. An ``include`` block in the ``survey.html`` template in the ``<!--Special Modules-->`` section. Check the question name against the name of your special question, and include it if it's true.
 4. A block in the ``renderResult`` JavaScript function found in ``survey.html``. Here you will get the response value to be inserted into the database and associated with the relevant question. For example, we get the response value of the ``SpecialClothingLevel`` question from the clothing picker interface.
 
User accounts
-------------

When a new user navigates to ``/survey/login/``, they can click "create account" in the bottom right. It's really simple to create an account. All you need is a secret invite code generated by a supseruser!

Invites 
-------

To get a list of active invites, simply click "Invites" in the navigation bar. Each invite can be used to create one account. If you've already shared an invite uncheck the "Fresh" field so that you don't accidentally give the same invite to two people. Once the invite is used, it cannot be used again, but you can always generate more codes by navigating to the ``/survey/invites/`` page.
