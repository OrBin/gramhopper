FROM python:3.7-slim as builder

COPY . /app
WORKDIR /app/
RUN python setup.py bdist_wheel


FROM python:3.7-slim

COPY --from=builder /app/dist/gramhopper-*.whl /
RUN pip install /gramhopper-*.whl && rm /gramhopper-*.whl

CMD gramhopper
