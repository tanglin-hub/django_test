upstream django_study  {
    server django_study:8000;
}

server {
    server_name  django-test-demo.22web.org;

    location /static {
        alias /apps/django_study/static;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_pass http://django_study;
    }

    listen 80;
}
location /static {
    alias /apps/django_study/static;
}