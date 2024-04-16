# quafu-agent-py
## how to use
```bash
docker pull ghcr.io/baqic/quafu-agent-py:main
docker run -d --network=host --name=quafu-agent-py --restart=always ghcr.io/baqic/quafu-agent-py:main
```

## run with custom config
```bash
# change xxx to your quafu server ip and system id
docker run -d --network=host --name=quafu-agent-py --env QUAFU_IP=xxx --env SYSTEM_ID=xxx  --restart=always ghcr.io/baqic/quafu-agent-py:main
```

## check the logs
```bash
# if the name of your container is quafu-agent-py
docker exec -it quafu-agent-py cat /home/sq/quafu-agent-py/log/requests.log
```

## check container logs
```bash
docker logs quafu-agent-py
```