FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN rm -rf build dist *.egg-info src/*.egg-info
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y \
        git \
        ffmpeg && \
    apt-get clean

RUN rm -rf /var/lib/apt/lists/*

CMD ["tail", "-f", "/dev/null"]
