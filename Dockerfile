FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python3 app/app.py
EXPOSE 5000
