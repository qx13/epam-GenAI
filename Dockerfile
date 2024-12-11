FROM python:3.10-bookworm
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt update

RUN pip install uv

COPY . .
RUN uv sync

CMD ["bash", "-c", "uv run src/main.py"]
