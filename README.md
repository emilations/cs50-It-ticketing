# __IT solutions ticketing system__
#### Video Demo:  https://youtu.be/SOnejLtumno
# Personal background
I am a professional mechanical engineer who decided to switch to programming. This course among other was chosen to be part of my personal plan into self-taught programming. The project and this class was taken individually and the fundamentals of programming that were taught through this class are very valuable.

# General description
My final project is a ticketing system for an IT department that handles the IT services in a mother company called ALPHA. The ticketing system gives the agents of the department tools to keep track of their services and resources. Clients/employees from ALPHA are able to submit tickets without logging in and agents of the IT department will be able to sign in and keep track, update and assign theses tickets. Agents are also able to create asset tag numbers for the materials handed to personnel’s. The system is web based using flask and python and is intended to be used solely on a computer web browser and not on mobile devices.

# Overall functionality
The ticketing system is split into two modes of operation: **Logged out** and **Logged in**.
The logged out mode enables three web pages 1-Login 2-Register 3-Submit ticket
The logged in mode enables four web pages 1-Tickets 2-Assets 3-Agents 4-Logout

    For a test drive
    Username: bruno.mars
    Password: Live

##### __MODE LOGGED OUT__

#### __Page 1 - Submit ticket:__
This page offers the ability to submit a ticket without having the need to be logged in. It permits a client to submit and log their issue into the system. The main goal of this page is to allow clients or employees from ALPHA to create their technical support tickets without having the need of an account. One submitted, the ticket will be logged into the system database to be processed by an agent who is logged in. Unfortunately, client will not have the ability to track their ticket once submitted. Clients will have to be contacted by email. The email will be of their choosing once submitting up their tickets.
#### __Page 2 - Register:__
This page is intended only for new agents in the IT department. The page allows them to create their account and enter the password they want to choose. Only people who have a secret code can register. The secret code can be shared by anyone who already has access to the portal. The secret code is called HR code and can be modified in the agents page once logged in.
#### __Page 3 - Login:__
This page is intended only for employees in the IT department. After having had registered and created the account, the user can then login using their credentials. Clients are not allowed to login to the system. Clients are offered a submit ticket page instead.

##### __MODE LOGGED IN__

#### __Page 1 - Tickets:__
This is the homepage of a user once logged in. In this page agents in the IT service department will be able to overview all the current tickets, as well as search and modify them. The search function searches tickets based on their subject alone. Tickets are displayed by status, id, asset id, agent, subject, and their owner. There is an edit button on each line of a ticket where an agent can assign an agent to because none is assigned by default. The edit button pops out a modal with a form having all the information of the current tickets inside fields that can be updated using the save changes button. An agent can modify almost all parameters of the tickets except the timestamps. A time created value is shown based on the timestamp in the server when the ticket is created. The time closed is stamped automatically when the status of the ticket is changed from open to closed. The time closed value is then erased once a ticket is opened again. There is a delete button offered inside each edit window, the delete feature is permanent and cannot be undone. Agents have the ability to create tickets themselves by clicking on the create new ticket inside the page. This button will popout a window that a has the same form of submit a ticket.

#### __Page 2 - Assets:__
This is the page where the agents can keep track of their devices and assets. Assets are presented graphically as cards and not in horizontal lines like tickets. There is an edit button into each card that permits the agent to edit the information of each asset. Asset tags can also be flagged as out of service if need be. The search function can only search asset tag based on their asset tag number. There are three types of assets to create from: laptops, cellphones and accessories.

#### __Page 3 - Agents:__
This page shows the agent database and by name and email. The only interaction offered in this page is the ability to modify the HR code that is used to register new agents. The agent table cannot be modified or altered. New registered agents will be added automatically to the table.

#### __Page 4 - Logout:__
This is not a page but rather an action to for the employee to logout from the session. Once logged out, the user will be redirected to the login page immediately.

# Files
The file structure is identical to that of the pset9 homework. This section goes in details about each file and directory purpose.

### __FOLDER flask_session:__
This is the folder that contains all the session cache from the users that login to the web page.

### __FOLDER static:__ This folder contains two icons for the webpage and two files.

FILE erp.png: An icon for the title of the website.

FILE script.js: This is a javascript file that contains the following functions: 1- myFunction that that changes the color of the font of tickets that are marked as open. 2- myFunction2 that changes the color of the font of tickets that has no agent attributed to them. 3- A function that highlights active page in the top menu. 4- A function that syncs the searched subject for the tickets. 5- A function that syncs the searched asset tag for assets.

FILE styles.css: This file contains comments for each style addition or modifications. As stated above, the website is only optimized to be viewed on a personal computer. The contents of the website is not optimized for smaller mobile device screens.

### __FOLDER template:__ This folder contains the html for the web app.

*FILE agents.html:* This is the html file that shows the page of agents. The page is only accessible in logged in mode. It has a table inside that presents all the agents registered to the ticketing system.

*FILE assets.html:* This is the html file that shows the assets already created in the system. The page is only accessible in logged in mode. The html contains three modal elements. One for the creation form of assets. One for the edit of current assets. And one for the delete confirmation popout. The search box within the page is controlled by a javascript function.

*FILE layout.html:* This is the main template file that contains the header and the footer of all the html files. This template is made to work with flask.

*FILE login.html:* This is the html page that users can put in their credentials in order to login to the website. The page is only accessible in logged out mode.

*FILE register.html:* This is the html that new users can use to create their account. The page takes in personal information from the user and lets them create their own password. The registration can only be completed if a correct HR_code is presented before submitting. The page is only accessible in logged out mode.

*FILE searchAssets.html:* This is an html block that is used to inject the results of an asset search using javascript. The html contents is then inserted using javascript. This html can only be accessed in logged in mode.

*FILE searchTickes.html:* This is an html block that is used to inject the results of a ticket search using javascript. The html contents is then inserted using javascript. This html can only be accessed in logged in mode.

*FILE submit.html:* This is an html page that is used to submitted tickets in logged out mode. The page consists of one html form that requests information from the client that properly create a ticket.

*FILE tickets.html:* This page can only be accessed in logged in mode. This page contains five functions. One for the creation form of tickets that is triggered using the create ticket button. The create ticket form ticket is a popout modal. The second function is being able to edit each ticket. The edit button next to each line of ticket triggers another modal popout that contains modifiable inputs with the ability to save the modification. The third function of this page is to present in a table all the current tickets in the database. The fourth function of the page is to quickly search within a table using subject keywords. The fifth function of the page is to be able to delete tickets. A confirmation model is presented before deleting any ticket because the delete is permanent.

### __MAIN folder:__

*FILE app.py:* This is application file for python that is running on the back end. The file redirects and renders html as needed and requested from the browser. The app.py imports a bunch of libraries at first in order to be fully functional. The app.py also imports a function from helpers.py that introduces authentications for sessions for users. The app.py has 9 routes defined and this text will only cover the important ones. Most routes has error messaging if the user misses out an input field and does something wrong. The error messaging is different than flash messaging. Flash messaging was reserved for successfull event communication. Error messaging is passed through as a variable when rendering each html. Since each html has a flask condition for error variable definition, a message would be rendered indicating to the user that inputs are not allowed be empty or wrong user name. The app.py has three functions that are defined in order to reduce some repetive code inside each route. Two of these functions are to simply fetch the data from the POSTED from. The last function is simply a database querry for all the information needed to render tickets.html. The index route could of have had been deleted since the homepage is tickets.html. A conscious action was taken to keep the index route to keep the option of adding a dashboard later on without modifying too much code. The three main routes have both POST and GET methods. The GET method is limited to only render the information needed when a client clicks on a page. The POST method is used to retrieve information from a form submitted by a user. There is an input that is retrieved from the html form when POSTing that defines whether the action is to CREATE, MODIFY or DELETE a ticket. This method was chosen instead of defining multiple routes for each action.

*FILE helpers.py:* This is a helper file that is copied from pset9. The file is imported by app.py at launch. The files contains an important function for login and a function that is not used from pset9 for apology rendering. It was decided to keep this file as is without modification.

*FILE itsolutions.db:* This is the database used to store all the website data. The database was created using sqlite3. The database contains four tables: assets, employees, human_resources, tickets. The assets table contains all the information that were submitted in creating an asset. The asset_tag is then inserted in tickets.html for a relational database. The second table is called employees and stores all the information that was inserted while registering a new user. The database is used to authenticate users and then assign valid agents to tickets when needed. The third table is called human_resources and stores only one variable that is called code_HR. This code is used in the registration phase when creating a new user. The fourth table is called tickets and is used to store all the created tickets by tickets.html or submit.html. It was decided to just delete row when a delete action is performed instead of creating a field with a boolean record for deleted records. Therefore, deleting a record is permanent.

*FILE readme.md:* As requested by the cs50x team.

FILE requirements.txt: This lists all the required programs and framework for the website to run on.

# Lessons learned
Reducing the complexity of code is always a challenge when writing code. The simplest I found was to regroup some repeat code into a function and encapsulate more. Given the change again, most of the code would be encapsulated into function to render the code a bit more easier to read.

A lot of hours was spent trying to identify the best error reporting function to adopt. There was the choise of using the flash feature presented by flask. But the flash feature lacks customization for coloring. It was decided to keep the flash messaging for reporting successfull events such as tickets creation or deletion etc. Another choice was to use javascript triggers and functions that would insert HTML when needed to display errors. Finally the option to passthrough an error variable to the render html via the app.py was chosen. Each .html contained a block that could only be activated if flask detects that an error variable exists. If that variable exists, then the html block will contain a banner from bootstrap displaying the error message.

A lot of hours were also spent trying to display the time from a local time zone perspective. The timestamp in the database for creating tickets is using the clock from the server side which is always synchronized to UTC. A javascript function was created in order to convert the time on the client side to match its local time zone. However, after many tries, this feature was disregarded and deleted. Therefore the only time shown in the webpages is based on UTC timing as used by SQLITE3. The argument to keep server time at UTC is for having the ability to keep time porperly if users are logged in from multiple time zones. Thus, client side time zone conversion is recommended.

Most of the time spent doing this project was on the front end. It was very delicate designing and tuning the styling in the front end. Also, selecting what to put on the front end takes much more time than anticipated. Defining the scope of the web app at first with clear boundaries helps a lot. Because starting such programs without a clear requirement makes for a lot of drafts and failed experiments.

Code quality at first is easier since code becomes like spaghetti when features are added last minute. Also, fixing bugs and adding shortcuts makes the code uglier for reading purposes. That is why I recommend to have to encapsulate most code into functions instead of just adding all the line of codes into the main program.

# Things to improve
Given more time, I would create a client dashboard that permits the client to check up on their tickets updates and communicate with the agents. Another feature to give the ability for agents to change their passwords should also be of added value. It was never tested to see if multiple users can loggin to at the same time or not. It would be a good feature to add the ability of restoring deleted tickets and have a log of actions associated with every tickets. Updates to tickets are not recorded and including a tracking system could be beneficial.
