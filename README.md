# Jobberwocky

# Project Name
> Outline a brief description of your project.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Improvements](#improvements)
* [Contact](#contact)


## General Information
Jobberwocky is a project that implements the requirements proposed by Avature as a challenge for a job opportunity.
This project is a service that exposes an API to save and query job opportunities.

## Technologies Used
- [docker](https://www.docker.com/)
- [docker compose](https://docs.docker.com/compose/)
- [python](https://www.python.org/)
- [fastapi](https://fastapi.tiangolo.com/)


## Features
Implemented features
- Job Posting endpoint
- Job Seaching endpoint
- Job Searching aggregated with external sources endpoint
- Job Alerting endpoint


## Setup

### Clone the repo

```
git clone git@github.com:fernandezgonzalo/Jobberwocky.git
```

### Pull submodule jobberwocky-extra-source

```
git submodule update --init --recursive
```

### Build docker images

```
make build
```

### Run project

```
make run
```

This project has an implemented frontend with an OpenAPI specification containing the developed APIs. You can access the documentation and make API queries using the following URL: http://localhost:8000/docs.

### Test project

```
make test
```

or test with coverage, this command generates an HTML report in directory *htmlcov*. You can open the 'index.html' file to access the report.

```
make coverage
```

## Improvements
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- User Registration and Authentication: Allow users to register accounts and authenticate to access personalized features and data.
- Parametrized Job Search: Provide the ability to search for job opportunities based on various criteria like location, job type, skills, salary range, etc.
- Messaging System: Implement a messaging system for users to communicate with employers during the application process.


## Contact
Created by @fernandezgonzalo