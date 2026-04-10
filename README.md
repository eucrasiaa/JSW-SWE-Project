JSW-SWE-Project
For CMSC 447 Spring 2026 
# A rework of the current UMBC Drop-In Tutoring page
## Key features:
1. dynamically respond to changes in:
    - Tutor Schedules
    - Tutor Arrivals/ check-ins
2. formatting changes to improve readability

## Installation:
### Requirements:
Docker: (Docker.com)[https://www.docker.com]


### Running:
1. navigate to Docker/
2. launch the docker container with `docker-compose up -d`
    - or, if using Linux, the provided `./dockTool.sh -s`
3. resulting pages sit on:

| http://localhost:4413       | student view |
| --------------------------- | ------------ |
| http://localhost:4413/staff | staff view   |

V1.1 reorganized the file layout.
added:
- various operational notes
