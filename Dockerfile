FROM python:3.7

ENV MONGODB_URL=mongodb+srv://OGYH:CTFfzLP00Iz0AS22@cluster0.ejoux.mongodb.net/ogyhDatabase?retryWrites=true&w=majority

WORKDIR /usr/ogyh-backend

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE ${PORT:-5000}

CMD uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000} --reload
