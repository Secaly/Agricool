FROM ubuntu:latest
MAINTAINER Kevin Ledieu "kevin.ledieu.fr@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
