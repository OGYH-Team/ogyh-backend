# Getting Started

## Run server

- Locally

```
# Install all dependencies
pip install -r requirements.txt

# Run the server locally
uvicorn app.main:app --reload
```

- Docker

```
# Build the docker image by local Dockerfile
docker build -t ogyh-backend .

# Start the container
docker run -d -p 5000:5000 --name ogyh-backend -v $(pwd):/usr/ogyh-backend ogyh-backend
```
