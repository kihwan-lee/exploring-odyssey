# project-wayfarer

Interactive blog to post articles and comments on various cities.

## Index:

- [Scope](#Scope)
- [User Stories](#user-stories)
- [Wireframes](#wireframes)
- [Data Models](#data-models)
- [Milestones](#milestones)

## Scope

The final objective is to build an app where users can users track articles and comments associated to a city.  Users will be able to visualize thier own articles and comments and search for cities to add new articles and comments to. Refer to milestones for full sprints breakdown.

##### Technologies in play

- Python
- Django
- PostGreSQL
  - CrispyForms
  - Bootstrap4
  

## User Stories

Project Wayfarer user can use this app to track cities, articles, and comments, to help them manage their travels and explorations.

#### Non-authenticated Users can:

- View landing page
- Sign Up to Wayfarer

#### Authenticated users can

- View landing page
- Search for cities
- Input Articles to Cities
- Comment on Articles on Cities
- View their profile page
- View their Article history
- View past comment information
- Can edit and delete prior articles and comments
- Update their profile image

## Wireframes

### Landing

Users will see input to log in or create account

![image]()


### Registration

Users who need to create will be guided to registration page

![image]()

### Home Page

Build out workout database/log individual workouts, title, data, submit to memory
This will allow user to input workout data to database, as well as have access to edit past workouts.  These workouts will be visible with hyperlinks to view workout details

![image]()


### Show Workout Page

Details each workout by: (name, date/time, start-time/end-time, type, comments/journal)

View 1
![image]()



## Data Models

### Users

- userId
- name
- lastName
- email
- password
- img (stretch)
- workoutID
- timestamp

### Workouts

- workoutId
- name
- date/time
- start-time/end-time
- type
- comments/journal
- timestamp


### Reviews (stretch goal, inter app sharing between users, posting to social)

- userId
- workouts


## Milestones

#### Sprint 1 - 10/9

- approvals
- boilerplate/github setup

#### Sprint 2 - 10/10-10/12

- user sees homepage and is able to create profile
- user is able to input workouts and have them saved, and available for reference
- user can further specify the details of thier workout



#### Sprint 3 - 10/12 - 10/13

- CSS/Bootstrap Styling
- Introduction of 3rd model(stretch goals)
- Test Deployment


#### Sprint 4 / Bonuses - 10/14 - 10/15

- Final Asthetics 
- Presentation Preparation
- Deployment
