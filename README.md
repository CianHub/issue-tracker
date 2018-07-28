# Great Idea Issue Tracker 

The Great Idea Issue Tracker is a responsive web application that allows users to create, upvote, pay for, comment on, update, view progress on, delete and read tickets containing bugs or new feature suggestions. The app was developed as a platform from which an existing platform can be improved and a team can recieve constructive criticism and suggestions from their customers.

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

The application was developed with Django, PostgreSQL, Python3, HTML5, CSS3, JavaScript, JQuery, HighCharts.js and Bootstrap 3 (both vanilla and a heavily modified version of the free Creative template).

## Design

The goal of the apps UX design was to keep everything as minimal as possible, while avoiding the app feeling empty and to provide quick and easy navigation for the user. The application was designed with a consistent colour palette, animation speed and layout e.g. each button has a consistent colour scheme such as blue for edit and red for delete across the app regardless of context (like a comment, a ticket or a user). Links are present where a user might instinctively look for one e.g. the title of a ticket or a username. Elements of the app were reduced for mobile users in order to provide the minimum necessary information such as in the the various tables etc due to the smaller screen space. 

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
