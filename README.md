# Todo-API-with-Flask
Take a working Angular JS Todo application and get it running via REST APIs
 developed in the Flask. The Angular JS app uses the ng-resource plugin to 
 automatically work with REST. This is a challenge issued by 
 www.teamtreehouse.com for a Python Web Development Tech Degree Project.
 All of the Angular JS is considered built by teamtreehouse for this project
 (unless otherwise noted), but may be edited by me at some point.

## Starting

Create a virtualenv and install the project requirements, which are listed in
`requirements.txt`. The easiest way to do this is with `pip install -r
requirements.txt` while your virtualenv is activated.

Then just run the app.py file and you are good to go.

## Routes

To create user objects though the api use the following routes.

 * To create a user POST a username, password, and password_verification to
 	* `/api/v1/users`

 * To receive a particular user's token submit a GET request to
 	* `/api/v1/users/token`


The following routes are expected by the JavaScript application.

* To get all the todos any user can submit a GET request to

    * `/api/v1/todos`
    
* To add a todos a logged in user user can submit a POST request the following
with "name" in the body

    * `/api/v1/todos`


* To update a todo submit a PUT request to with a new "name"

    * `/api/v1/todos/<int:id>`
    
* To delete a todo submit a DELETE request to

    * `/api/v1/todos/<int:id>`