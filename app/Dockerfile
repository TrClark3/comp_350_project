FROM python:latest
RUN mkdir -p /var/app/flask_app
WORKDIR /var/app/flask_app
COPY ./app/requirements.txt /var/app/flask_app
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ /var/app/flask_app
ENV FLASK_APP ../app.py
COPY ../wait-for-it.sh /var/app/wait-for-it.sh
RUN chmod +x /var/app/wait-for-it.sh
CMD [ "../wait-for-it.sh" , "flask-db:3306" , "--strict" , "--timeout=300" , "--" , "gunicorn" , "-w 1", "-b :8000", "app:app" ,  "--reload" ]
