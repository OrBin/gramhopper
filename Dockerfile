FROM python:3.10-alpine as builder

COPY . /app
WORKDIR /app/
RUN python setup.py bdist_wheel


# For some reason, ruamel.yaml won't be installed on alpine.
# That's not important enough to investigate, just leaving it with the slim image.
FROM python:3.10-slim

COPY --from=builder /app/dist/gramhopper-*.whl /
RUN pip install /gramhopper-*.whl && rm /gramhopper-*.whl

CMD gramhopper
