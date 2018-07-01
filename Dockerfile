FROM python:3-alpine

LABEL maintainer "docker@captnemo.in"

ARG BUILD_DATE
ARG VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="IndiaPost Tracker API" \
      org.label-schema.vcs-url="https://github.com/captn3m0/indiapost-tracker.git" \
      org.label-schema.url="https://github.com/captn3m0/indiapost-tracker" \
      org.label-schema.vcs-ref=$VCS_REF

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app/

ENTRYPOINT ["python", "-u", "web.py", "3000"]
EXPOSE 3000
