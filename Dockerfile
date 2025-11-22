# included media stuffs 
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

WORKDIR /App

ARG DEV=false

COPY requirements.txt requirements.dev.txt /App/

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         libpq5 libjpeg62-turbo \
#         build-essential libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
#     pip install --upgrade pip && \
#     pip install --no-cache-dir -r /App/requirements.txt && \
#     [ "$DEV" = "true" ] && pip install --no-cache-dir -r /App/requirements.dev.txt || true && \
#     apt-get purge -y build-essential libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
#     apt-get autoremove -y && \
#     rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 libjpeg62-turbo \
        build-essential libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /App/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        pip install --no-cache-dir -r /App/requirements.dev.txt; \
    fi && \
    apt-get purge -y build-essential libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY ./App /App

# backup
# RUN useradd --create-home --shell /bin/sh django-user && \
#     chown -R django-user:django-user /App && \
#     mkdir -p /vol/static/media /vol/web/static && \
#     chown -R django-user:django-user /vol && \
#     chmod -R 755 /vol/web

# test1
RUN useradd --create-home --shell /bin/sh django-user && \
    chown -R django-user:django-user /App && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol/web && \
    chmod -R 755 /vol/web  # TEMP: for testing

USER django-user

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# fixed dockerfile
# FROM python:3.12-slim

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PATH="/usr/local/bin:$PATH"

# WORKDIR /App

# ARG DEV=false

# COPY requirements.txt requirements.dev.txt /App/

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         libpq5 libjpeg62-turbo \
#         build-essential libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
#     pip install --upgrade pip && \
#     pip install --no-cache-dir -r /App/requirements.txt && \
#     if [ "$DEV" = "true" ]; then \
#         pip install --no-cache-dir -r /App/requirements.dev.txt; \
#     fi && \
#     apt-get purge -y build-essential libpq-dev zlib1g-dev libjpeg62-turbo-dev && \
#     apt-get autoremove -y && \
#     rm -rf /var/lib/apt/lists/* && \
#     mkdir -p /vol/static/media && \ 
#     mkdir -p /vol/web/static && \
#     chown -R django-user:django-user /vol/ && \
#     chown -R 755 /vol/web

# COPY ./App /App

# RUN useradd --create-home --shell /bin/sh django-user && \
#     chown -R django-user:django-user /App

# USER django-user

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# # my own updated code 
# FROM python:3.12-slim

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PATH="/usr/local/bin:$PATH"

# WORKDIR /App

# ARG DEV=false

# # copy only requirements first (cache-friendly)
# COPY requirements.txt requirements.dev.txt /App/
# RUN apk add --update --no-cache postgresql-client jpeg-dev



# RUN apt-get update && apt-get install -y --no-install-recommends \
#     postgresql-client \
#     libjpeg-dev \
#     zlib1g-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

    
# # previous code 
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r /App/requirements.txt && \
#     if [ "$DEV" = "true" ]; then \
#       pip install --no-cache-dir -r /App/requirements.dev.txt; \
#     fi

# # copy the application code (explicitly copy host ./App into container /App)
# COPY ./App /App

# # create non-root user and give ownership of /App
# RUN useradd --create-home --shell /bin/sh django-user && \
#     chown -R django-user:django-user /App

# USER django-user

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

