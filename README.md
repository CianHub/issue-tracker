# Great Idea Issue Tracker 

The Great Idea Issue Tracker is a responsive web application that allows users to create, upvote, pay for, comment on, update, view progress on, delete and read tickets containing bugs or new feature suggestions.

## Features

The application has several features:

1. Users can browse the existing tickets in the database.
2. Users can create their own tickets.
3. Users can edit or delete their existing tickets.
4. Users can upvote, see the status of and comment on existing tickets.
5. Users can register, view and login to their account.
6. Users must make a payment to create or upvote a new feature ticket.
7. Users can upvote or create a bug ticket for free.
8. Users can view progress on tickets being worked on.
9. If new tickets have been created since the users last login, the user is shown a notification upon their next login.

## Technologies

The application was developed with Django, PostgreSQL, Python3, HTML5, CSS3, JavaScript, JQuery, HighCharts.js and Bootstrap.

## Installation

1. Ensure Python3, pip, Django v1.11 and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder
5. Setup the virtualenv instance for the project and activate the virtualenv instance 
7. Install required packages from requirements.txt 
8. In the CLI enter: ``` $ python manage.py runserver ```

## Testing
To run tests, in the CLI enter:
```
$ python3 manage.py test
```
## Deployment

The application has been deployed to Heroku and can be viewed at: <https://issue-tracker-cian.herokuapp.com/>