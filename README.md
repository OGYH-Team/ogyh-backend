# Getting Started
[![codecov](https://codecov.io/gh/OGYH-Team/ogyh-backend/branch/main/graph/badge.svg?token=90ZUcbpAOk)](https://codecov.io/gh/OGYH-Team/ogyh-backend)
## Run server

- Locally

```
# Install all dependencies
pip install -r requirements.txt

# Run the server locally
uvicorn app.main:app --port=5000 --reload
```

- Docker

```
# Build the docker image by local Dockerfile
docker build -t ogyh-backend .

# Start the container
docker run -d -p 5000:5000 --name ogyh-backend --env-file .env -v $(pwd):/usr/ogyh-backend ogyh-backend
```
