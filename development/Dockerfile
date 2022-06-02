FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE djangoArticlesApp.settings_dev
RUN mkdir /workspace
WORKDIR /workspace
ADD requirements.txt /workspace/
RUN pip install -r requirements.txt
ADD . /workspace/
