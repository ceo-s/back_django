FROM python:3.11.3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

# ENTRYPOINT ["/app/entrypoint.dev.sh"]

# CMD ["python3", "manage.py", "runserver"]

# EXPOSE 8000 