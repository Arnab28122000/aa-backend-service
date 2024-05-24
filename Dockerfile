FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /aa-backend-service

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /aa_backend_service/
COPY ./pyproject.toml /aa-backend-service

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

COPY ./aa_backend_service /aa-backend-service/aa_backend_service
COPY ./main.py /aa-backend-service/

# expose the port that uvicorn will run the app on
ENV PORT=5000
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
