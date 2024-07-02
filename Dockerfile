FROM python:3.10.14-slim-bullseye

RUN pip install --no-cache-dir httpx loguru numpy==1.26.4 pyquafu==0.4.0 

WORKDIR /home/sq/quafu-agent-py
COPY . .

ENV QUAFU_IP=120.46.209.71
ENV SYSTEM_ID=7

ENTRYPOINT [ "python3", "quafu-agent.py" ]