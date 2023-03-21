FROM python:3.10

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /my_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
ENV FLASK_ENV=development

EXPOSE 5000

ENV PORT 5000
ENV HOST 0.0.0.0
ENV FLASK_APP=app/main.py
CMD ["flask", "run", "--host=0.0.0.0"]


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY manage.py .
ENTRYPOINT ["/entrypoint.sh"]