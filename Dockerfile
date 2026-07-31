FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# b. install webservice deps (python + flask deps)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# c. download webapp from github
WORKDIR /app
RUN git clone https://github.com/brightorange/plant_tracker.git . \
    && pip3 install -r requirements.txt

# d. download dummy data from S3 to a temp location
ARG DUMMY_DATA_URL
RUN test -n "$DUMMY_DATA_URL" \
    && curl -fsSL -o /tmp/dummy.csv "$DUMMY_DATA_URL"

# e. mount volume for data (app will write plants.json here)
VOLUME /data

# f. expose port 80
EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]