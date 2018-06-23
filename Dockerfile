FROM python:3-alpine

LABEL maintainer "docker@captnemo.in"

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app/

ENTRYPOINT ["python", "-u", "web.py", "3000"]
EXPOSE 3000
