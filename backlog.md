# Epic - Exploration/Spikes
    - [ ] Spike: Explore JavaScript's Fetch functionality to understand basic HTTP requests and responses.
    - [ ] Spike: Familiarize with basics of SQL-based databases (tables, queries)
    - [ ] Explore: Document the currently displayed Tutor schedule from the website
    - [ ] Explore: Concept designs for a less ugly(?) UI for the website
    - [ ] Explore: RRule for reoccuring event syntax
# Epic - Database Backend
    - [ ] Story: Determine database schema for the database
        - [ ] Task: ER Diagram
        - [ ] Task: Define tables and relationships
    - [ ] Story: Implement schema:
        - [ ] Task: Create tables in the database 
        - [ ] Task: Create Views  
    - [ ] Story: Populate database with data
        - [ ] Task: Scripts to insert?
    - [ ] Story: Validation of data integrity and relationships
        - [ ] Task: Test queries, constraints, and relationships 
        - [ ] Task: Standardize tests, will be part of pre-commit review process!
    - [ ] Story: Plan out queries for the API
        - [ ] Task: Layout clear system for connection between Master, Exceptions, and Instances 
        - [ ] Task: Determine how frequent each will run
# Epic - Website Layouts:
    - [ ] Story: Website wireframes:
    - pages:
        1. user dashboard (with calendar view)
            - clear to read calander
            - design ? idk im not a designer what do we need
        2. tutor dashboard
            - i



# Epic - API Development - GET 
    - [ ] Spike: Review FLASK documentation w/ the python library
    - [ ] Story: Build off and implement query system:
        - [ ] Task: Combining Master + Exception
            - [ ] Subtask: standardize automation?
        - [ ] Task: Daily query for instances of day:
            - [ ] Subtask: cron job?? idk
    - [ ] Story: Endpoints:
        - [ ] Task: GET by course?
        - build out when we have a better idea of what the website needs

# Epic - Check-In / POST Api:


# Epic - JS interactions with API
    - 

# Epic - Tutor auth? 
    - probably simple just like. render their schedule based on sql query of studentID or smthn?
    - not like security is concern, just ensuring they see only their schedules to prevent mix-ups

# Epic - Beautify:
    - make it look better
