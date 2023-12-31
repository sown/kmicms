ARG PYTHON_VERSION=3.12-slim-bookworm

FROM python:${PYTHON_VERSION} as builder

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install wheel poetry==1.7.1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:${PYTHON_VERSION} as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN addgroup --system wagtail \
    && adduser --system --ingroup wagtail wagtail

# Install system packages required by Wagtail and wagtail.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

COPY ./etc/docker/web/entrypoint /entrypoint
RUN chmod +x /entrypoint
RUN chown wagtail /entrypoint

COPY ./etc/docker/web/start /start
RUN chmod +x /start
RUN chown wagtail /start

# avoid 'permission denied' error
RUN mkdir /app/static
RUN mkdir /app/media

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./kmicms/kmicms/configuration.prod.py ./kmicms/configuration.py

COPY kmicms .

RUN chown -R wagtail:wagtail .

USER wagtail

ENTRYPOINT ["/entrypoint"]