FROM NGINX:1.23

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./compose/producion/nginx/sources.list /etc/apt/
RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/producion/nginx/django_study.conf /etc/nginx/conf.d/django_study.conf
