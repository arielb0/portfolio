FROM python:3
RUN apt-get update && apt-get upgrade && apt-get install -y nginx
COPY nginx.conf /etc/nginx/nginx.conf
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN /app/manage.py collectstatic --no-input
RUN /app/manage.py migrate
RUN /app/manage.py loaddata bazaar/permissions bazaar/groups restaurant/answers
EXPOSE 80
CMD service nginx start && gunicorn -w 1 scull_suite.wsgi
