# MaturaSubjects
It's a project in my freetime for my A-Levels for all students in my class to choose the best subject available.
## Setup Website
- downlaod project
- download all needed library's from requirements
- create key.py file in root folder and add following variables:
    - requestkey [String] (key for admins to create new users in database)
    - host [String] (ip address)
    - userlist [list] (all usernames you want to put into database)
    - db [String] (link to database - sqlite3)
    - secret_key [String] (key for flask rest services)
    - subjects [list] (all subjects you want to choose from)
## Start Website
- start app.py
- start request.py
  - database file and users.txt should be created by now