ES_DESC := aws es describe-elasticsearch-domain --domain-name $(ES_DOMAIN)
ES_UPDATE_DOMAIN := aws es update-elasticsearch-domain-config --domain-name $(ES_DOMAIN) --access-policies file://$(POLICY_JSON)

DOCKER_BUILD := docker build \
                --no-cache=true -t s3-access-log-es-mapping-template .
DOCKER_RUN := docker run --rm -t -i --name s3-access-log-es-mapping-template \
              --env ES_ENDPOINT=$(ES_ENDPOINT) \
              --env ES_TEMPLATE_NAME=$(ES_TEMPLATE_NAME) \
              -v /etc/localtime:/etc/localtime:ro s3-access-log-es-mapping-template
DOCKER_RM := docker rm -f s3-access-log-es-mapping-template

es-desc:
	@$(ES_DESC)

es-update-domain:
	@$(ES_UPDATE_DOMAIN)

docker-build:
	@$(DOCKER_BUILD)

docker-run:
	@$(DOCKER_RUN)

docker-destroy:
	@$(DOCKER_RM)
