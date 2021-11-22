# OGYH-backend 
[![codecov](https://codecov.io/gh/OGYH-Team/ogyh-backend/branch/main/graph/badge.svg?token=90ZUcbpAOk)](https://codecov.io/gh/OGYH-Team/ogyh-backend)   
![Deploy to Heroku](https://github.com/OGYH-Team/ogyh-backend/actions/workflows/main.yml/badge.svg)    
![Deploy to Heroku](https://github.com/OGYH-Team/ogyh-backend/actions/workflows/dev.yml/badge.svg)    

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Installation](#installation)
* [Testing](#testing)

## General Information
[Open api doccument](https://ogyh-backend-dev.herokuapp.com/docs#/)

## Technologies
Project is created with:
* python 3.8
* [FastAPI](https://fastapi.tiangolo.com/)
* [MongoDB 5.0](https://docs.mongodb.com/)

## Installation

- Locally

```bash
# Install all dependencies
pip install -r requirements.txt

# Run the server locally
uvicorn app.main:app --port=5000 --reload
```

- Docker

```bash
# Build the docker image by local Dockerfile
docker build -t ogyh-backend .

# Start the container
docker run -d -p 5000:5000 --name ogyh-backend --env-file .env -v $(pwd):/usr/ogyh-backend ogyh-backend
```

## Testing
- Testing with unittest
```bash
python -m unittest
```
- Running Coverage and Produce Coverage Reports
```bash
coverage run -m unittest
coverage report -m
```
