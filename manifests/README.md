# Deployment on Kubernetes

Telegram Bots need a global bot token to interact with the API. This token is
unique to your specific bot. To mount the token into the container, create an
`.env` file with the key `MOCK_BOT_TOKEN` and your bot token:

```bash
MOCK_BOT_TOKEN=133769420:notaverysecurebottoken
MOCK_BOT_NAME=mockerellbot
```

Afterwards, run either `kustomize build .` to build the manifests with kustomize
or use `kubectl apply -k .` to directly apply the fresh manifests to your
context.
