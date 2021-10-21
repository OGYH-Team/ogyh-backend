FROM python:3.7

WORKDIR /usr/ogyh-backend

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE ${PORT:-5000}

CMD uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
