FROM  python:3.10-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add --no-cache \
    # 基本构建工具
    gcc musl-dev \
    # Pillow 图像库依赖
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    # 数据库相关依赖
    postgresql-dev \
    # 其他常见依赖
    libffi-dev openssl-dev

WORKDIR /app

RUN pip install pipenv -i https://pypi.douban.com/simple

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --deploy --ignore-Pipfile

COPY . /app

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chomd +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]