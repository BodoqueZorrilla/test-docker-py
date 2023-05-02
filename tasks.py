''''
Create this kind of taks for send emails and the payment requirements

to test it locally use this commands: 

Install Docker: 
1.- docker build -t flask-smorest-api .
Too change docker when code changes:
 2.- docker run -dp 5005:5000 -w /app -it -v "$(pwd):/app" flask-smorest-api

With the running: 
docker run -dp 5000:80 -w /app -it -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"

Running queues redis locally Mac:
docker run -w /app flask-smorest-api sh -c "rq worker -u rediss://red-ch8kvbcs3fvl67h2vd40:35vof8NBbxNXWl8Y4V4iIqPZJqQEAbtP@frankfurt-redis.render.com:6379 emails"

'''
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAIN_DOMAIN")

def send_simple_email_message(to, subject, body):
    return "send email"


def send_user_registartion_email(email, username):
    return send_simple_email_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores RESTAPI"
    )