FROM python:3.6
ADD . /
WORKDIR /
CMD pip install -r requirements.txt
CMD python3 app/app.py
EXPOSE 5000
