# HackUMBC 2020 OfficeHourBot!

## What makes this so important?
    With the online transition of most classes, traditional
    way to hold office hours in a large classroom has ended.
    Therefore, we must adapt and overcome this difficulty to 
    provide a streamlined way for students and TA's (or teachers)
    to interact and maintain a healthy learning environment.

    Many classes have created Discords for students to congregate and 
    share ideas and help eachother better understand topics, and it's
    a hassle to have to change to other applications multiple times a day.

    This is why we wanted to create a fully integrated bot that makes everyone's
    lives easier. 


## How to Install
    Step 1: 
    1)Open Command Promt (CMD)
    2) Type python
    3) If you do not have python installed then it will take you to the microsoft store -> install this
    4) type "pip install discord.py" into cmd
    Step 2:
    1) Head to: https://discord.com/developers/applications
    2) Login to your account (or create an account)
    3) Create a new application (top right button); choose any name
    4) Click on the newly made application and go to the "bot" top under settings
    5) Click on "Add Bot"; USERNAME will be what is shown on the server
    6) Click on the "Copy" button under token
    7) Paste this token into the `TOKENFILE.py`
    

    
## brainstorming ideas
 - General office hour bot for any class
    What do it do???
    - student queue
        - priority queue
    - Google Calendar integration (may be hard to do)
        - google calendar api
    - Set up a discord server - starting from a fresh server
        - From ground up set up a discord server
        - Text Channels:
            - student-general
            - student-waitroom
            - student-request
            - staff-general
            - staff-commands
            - faq
        - Voice Channels:
            - hangout
            - staff-hangout (hidden)
            - office-hours (hidden)
    - Assignment list 
        - due dates 
        - own cog
    - simple commands
        - help
    - FAQ
    - Private one on one command
    - easter eggs
    - delete commands after X time
    - echo log gonna be dank
