FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY . .

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi
RUN poetry run alembic upgrade head


EXPOSE 8000
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "app.main:app" ]