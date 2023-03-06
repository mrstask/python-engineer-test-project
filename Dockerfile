FROM python:3.10

RUN mkdir /opt/code
ADD . /opt/code
WORKDIR /opt/code

RUN python setup.py install && which flask && sleep 5

ENV PORT 5000
ENV HOST 0.0.0.0
ENV FLASK_APP=app/app.py

VOLUME ["/opt/code"]

CMD ["flask", "run", "--host=0.0.0.0"]
