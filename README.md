# HackUMBC 2020 OfficeHourBot!

![](LogoZoomedIn.png)

## What makes this so important?
    With the online transition of most classes, traditional
    way to hold office hours in a large classroom has ended.
    Therefore, we must adapt and overcome this difficulty to 
    provide a streamlined way for students and TA's (or teachers)
    to interact and maintain a healthy learning environment.

    Many classes have created Discords for students to congregate and 
    share ideas and help each other better understand topics, and it's
    a hassle to have to change to other applications multiple times a day.

    This is why we wanted to create a fully integrated bot that makes everyone's
    lives easier. 

## Features
    - A self creating server
        - Sets up permissions for Professor, Teaching Assistants, and Students
        - Instructor only chats
        - Student Chats
    - Authentication for students and TAs
        - Prevents unwanted students in the class discord
    - A working Office Hour Queue
        - Reject 
        - Accept
        - Priority Queue Option
        - Shows the current TAs
        - Shows the current Queue
        - Position in the Queue
    - Assignment command
    - Lecture command
        - makes a lecture with breakout groups
    - Private One on One chat
    - Help command that shows all the commands 

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
    
## Available Functions
    - Commands Available to Instructors:
        - !startOh 'priority' (optional)
            - adds the caller to the office hour session
        - !endOh
            - ends the office hour session of the caller
        - !accept
            - accepts the person in front of the queue
        - !reset
            - resets all students queue priority, keeps total
        - !reject [Student ID] [Reason]
            - removes student from queue and direct message them the reason
        - !close
            - closes a category including all voice chats and text chats
        - !private
            - creates a private one on one session
        - !addAssignment [Name] ; [Due Date] ; [Description]
            - Creates an assignment for students to view
        - !clearAssignment
            - Will clear all the listed assignments
        - !beginLecture [Number of Breakout Rooms (optional)]
            - Begins a lecture and creates rooms if applicable
        - !endLecture
            - Removes the lecture chat and breakout groups
        - !help
            - Shows instructor and student commands in discord
    - Commands Available to Students:
        - !join [Reason]
            - Lets student join queue for office hours
        - !leave
            - Lets student leave queue for office hours
        - !position
            - Shows student their position in queue
        - !onDuty
            - shows who the current TA's on duty are
        - !inQueue
            - Shows the current queue of students
        - !help
            - Shows student commands in discord

## Video steps
    - start with new guild
    - call setup command
    - show authenticate
    - show office hours
        - join
        - accept
        - reject
    - close
    - lecture
    - private

## Showcase Order
    - Fresh Server
    - Showcase role Auth by changing role with discord
    - Show help command
    - Talk about Oh Start and then p-queue option
    - Accept student
    - Deny next student
    - Add assignment
    - Show student view of assignment

![](Octocatgif.gif)
