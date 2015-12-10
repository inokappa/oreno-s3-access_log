- describe-elasticsearch-domain

```sh
$ make es-desc
```

- update-elasticsearch-domain-config

```sh
$ make es-update-domain
```

- docker build

```sh
$ make docker-build
```

- docker run

```sh
$ make \
  ES_ENDPOINT="https://search-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com" \
  ES_TEMPLATE_NAME="template-name" \
docker-run
```
- docker rm

```sh
$ make docker-destroy
```
