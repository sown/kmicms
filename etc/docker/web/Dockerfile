ARG PYTHON_VERSION=3.12-slim-bookworm

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system packages required by Wagtail and wagtail.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN addgroup --system wagtail \
    && adduser --system --ingroup wagtail wagtail

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./etc/docker/web/entrypoint /entrypoint
RUN chmod +x /entrypoint
RUN chown wagtail /entrypoint

COPY ./etc/docker/web/start /start
RUN chmod +x /start
RUN chown wagtail /start

WORKDIR /app

# avoid 'permission denied' error
RUN mkdir /app/static
RUN mkdir /app/media

COPY . .
COPY ./kmicms/kmicms/configuration.prod.py /app/kmicms/kmicms/configuration.py

RUN chown -R wagtail:wagtail /app

USER wagtail

ENTRYPOINT ["/entrypoint"]