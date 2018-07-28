# Great Idea Issue Tracker 

The Great Idea Issue Tracker is a responsive web application that allows users to create, upvote, pay for, comment on, update, view progress on, delete and read tickets containing bugs or new feature suggestions.

## Features

The application has several features:

1. There are 3 roles: user, staff and superuser
2. Users can browse the existing tickets in the database.
2. Users can create their own tickets.
3. Users can edit or delete their existing tickets.
4. Users can upvote, see the status of and comment on existing tickets.
5. Users can register, view and login to their account.
6. Users must make a payment to create or upvote a new feature ticket.
7. Users can upvote or create a bug ticket for free.
8. Users can view progress on tickets being worked on.
9. If new tickets have been created since the users last login, the user is shown a notification upon their next login.
10. A staff member can do all of the above plus edit/delete any ticket or comment and view the user list page
11. A superuser can do all of the above plus edit/delete users on the user list page and promote users to staff members

## Technologies

The application was developed with Django, PostgreSQL, Python3, HTML5, CSS3, JavaScript, JQuery, HighCharts.js and Bootstrap.

## Installation

1. Ensure Python3, pip, Django v1.11 and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder.
5. Setup the virtualenv instance: ```$ python3 -m virtualenv env```
6. Active the virtualenv instance: ```$ source env/bin/activate```
7. Install required packages from requirements.txt: ```$ pip install -r requirements.txt``` 
8. In the CLI enter: ``` $ python manage.py runserver ```
9. Set envionmental variables (see .env.example).


## Testing
To run tests, in the CLI enter:
```
$ python3 manage.py test
```
## Deployment

The application has been deployed to Heroku and can be viewed at: <https://issue-tracker-cian.herokuapp.com/>
