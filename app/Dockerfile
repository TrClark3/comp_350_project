# What image and version is the container at 
FROM python:latest

# Create directory /var/app/flask_app in container
RUN mkdir -p /var/app/flask_app
# change directory into /var/app/flask_app
WORKDIR /var/app/flask_app

# copy requirements.txt and pip install them 
COPY ./app/requirements.txt /var/app/flask_app
RUN pip install --no-cache-dir -r requirements.txt

# copy application files 
COPY ./app/ /var/app/flask_app

# set FLASK_APP 
ENV FLASK_APP ../app.py

# Copy wait script and make it executable
COPY ./wait-for-it.sh /var/app/wait-for-it.sh
RUN chmod +x /var/app/wait-for-it.sh

# On start up run wait script and when it finds flask-db is done run the app
CMD [ "../wait-for-it.sh" , "flask-db:3306" , "--strict" , "--timeout=300" , "--" , "gunicorn" , "-w 1", "-b :8000", "app:app" ,  "--reload", "--capture-output" , "--enable-stdio-inheritance" ]
