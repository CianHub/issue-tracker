# Great Idea Issue Tracker 

The Great Idea Issue Tracker is a responsive web application that allows users to create, upvote, pay for, comment on, update, view progress on, delete and read tickets containing bugs or new feature suggestions. The app was developed as a platform from which an existing platform can be improved and a team can recieve constructive criticism and suggestions from their customers.
 
## UX

### User Stories

Before beginning development on the site, several user stories were created to determine who a visitor to the site could be and what they might want from the site:

- "As a user I want to be able to create tickets for bugs/features, upvote and view existing tickets, see how many hours are spent working on bugs/features per day/week/month and see what the highest voted tickets are”

- "As a customer, I want to be able to see where my money is going and the progress being made on the project. I also want to be able to have a say on the direction of the product and see what other customers think."

### Design

The application utilises a minimal responsive design based upon a heavily modified version of the [creative bootstrap theme](https://startbootstrap.com/template-overviews/creative/). 

The goal of the apps UX design was to keep everything as minimal as possible, while avoiding the app feeling empty and to provide quick and easy navigation for the user. The application was designed with a consistent colour palette, animation speed and layout e.g. each button has a consistent colour scheme such as blue for edit and red for delete across the app regardless of context (like a comment, a ticket or a user). 

Links are present where a user might instinctively look for one e.g. the title of a ticket or a username. Elements of the app were reduced for mobile users in order to provide the minimum necessary information such as in the the various tables etc due to the smaller screen space.

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

## Technologies Used

- [HTML](https://www.w3.org/)
    - The project uses **HTML** to create the website.

- [CSS](https://www.w3.org/)
    - The project uses **CSS** to style the website.

- [Bootstrap](https://getbootstrap.com/docs/3.3/)
    - The project uses **Bootstrap** to style the site and user experience.

- [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript)
    - The project uses **JavaScript** to use Bootstrap functions.

- [JQuery](https://jquery.com/)
    - The project uses **JQuery** to manipulate the DOM.

- [Python](https://www.python.org/)
    - The project uses **Python** to write the sites logic.

- [Django](https://www.djangoproject.com/)
    - The project uses **Django** for the apps backend (server, testing, load templates etc.). 

- [PostgreSQL](https://www.postgresql.org/)
    - The project uses **PostgreSQL** for the apps database. 

- [HighCharts](https://www.highcharts.com/)
    - The project uses **HighCharts** to display chart data. 

## Testing

In the development of this application testing consisted entirely of automated tests using the django unittest package.

### Automated Testing

To run tests, in the CLI enter:
```
$ python3 manage.py test
```

### Known Bugs

The console will show an error on the progress page (HighCharts error #16) due to HighCharts being defined twice on the page. This console error has no effect on the apps functionality and is due to the JS being loaded in the document head. Unfortunately due to ChartKick's requirements the JS must be loaded this way in order to function correctly.

## Planning

### Database Schema

The initial conceptual database schema for the app can be found in the file Great Idea - Issue Tracker_ Preliminary Planning.pdf included in this repository.

A PostgreSQL database was chosen as it integrated well with Django and granted a lot of flexbility. When drawing up the schema, the aim was to keep the data as modular as possible. The other major consideration was how each table relates to each other.

For example, the user table connects to the ticket table via the author field, the ticket table connects to the ticket type table via the ticket field, the comment table connects to the ticket table via the ticket field, the ticket time table connects to the ticket field via the ticket field.

### Preliminary Planning Document

The preliminary planning conducted before development began (including user stories, outline of functionality, inital conceptual database schema etc.) can be found in the repository under the name Great Idea - Issue Tracker_ Preliminary Planning.pdf.

## Deployment

This project was deployed to Heroku with Gunicorn. Inside Heroku's config vars the DATABASE_URL, SECRET_KEY, STRIPE_PUBLISHABLE, STRIPE_SECRET, HOSTNAME, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD were set. The PostgreSQL database is hosted with the Heroku add-on Heroku PostgreSQL.

The Project can be viewed at: <https://issue-tracker-cian.herokuapp.com/>

## Installation

1. Ensure Python3, pip, Django v1.11 and Virtualenv are installed.
2. Clone repository.
4. Go to the repository folder.
5. Setup the virtualenv instance: ```$ python3 -m virtualenv env```
6. Active the virtualenv instance: ```$ source env/bin/activate```
7. Install required packages from requirements.txt: ```$ pip install -r requirements.txt``` 
8. In the CLI enter: ``` $ python manage.py runserver ```
9. Set envionmental variables (see .env.example).

## Credits

### Acknowledgements

- The projects design is based on a heavily modified version of the [creative bootstrap theme](https://startbootstrap.com/template-overviews/creative/)
