FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

EXPOSE 5000

ENV PORT 5000
ENV HOST 0.0.0.0
ENV FLASK_APP=app/main.py
CMD ["flask", "run", "--host=0.0.0.0"]


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY manage.py .
ENTRYPOINT ["/entrypoint.sh"]