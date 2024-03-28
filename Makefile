API_NAME := paradrop_api
UI_NAME := paradrop_ui

.PHONY: api elk superlinter develop docs

default: docker

mkcert:
	openssl req -x509 -newkey rsa:4096 -nodes -keyout ui/localhost.key -out ui/localhost.pem -days 365 -sha256 -subj '/CN=127.0.0.1' -addext 'subjectAltName=IP:127.0.0.1'
	cp -f ./ui/localhost.* ./api/

npm:
	cd ui && npm run test

docs:
	cd docs && npm install

docker: npm mkcert docs
	sudo docker compose down --remove-orphans
	sudo URL='https:\/\/127.0.0.1' docker compose up --build -d
	sleep 60
	cd ./elk && ./seed.sh

demo: npm mkcert docs
	sudo docker compose down --remove-orphans
	sudo URL='https:\/\/demo.paradrop.io' docker compose up --build -d
	sleep 60
	cd ./elk && ./seed.sh

develop: npm mkcert docs
	sudo docker compose down --remove-orphans
	sudo URL='https:\/\/develop.paradrop.io' docker compose up --build -d
	sleep 60
	cd ./elk && ./seed.sh

ui: npm
	./ui/http_server.py

api: pip
	rm -f ./api/localhost.*
	./api/app.py

down:
	sudo docker compose down --remove-orphans

up:
	sudo URL='https:\/\/127.0.0.1' docker compose up --build -d

seed:
	cd ./elk && ./seed.sh

elk:
	sudo docker rm -f opensearch
	sudo docker rm -f opensearch_dashboards

	sudo docker run -d --restart=always --name opensearch -p 127.0.0.1:9200:9200 \
		-e "discovery.type=single-node" -e "network.host=0.0.0.0" -e "http.cors.enabled=false" \
		-v "${PWD}"/elk/internal_users.yml:/usr/share/opensearch/config/opensearch-security/internal_users.yml  \
		opensearchproject/opensearch:2.11.1

	sleep 60

	sudo docker run -d --restart=always --name opensearch_dashboards -p 127.0.0.1:5601:5601 \
		-e "SERVER_HOST=0.0.0.0" \
		-v "${PWD}"/elk/opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml \
		opensearchproject/opensearch-dashboards:2.11.1

	cd ./elk && ./seed.sh

cbuilds: npm mkcert
	cd ./api && sudo docker build -t $(API_NAME) .
	cd ./ui && sudo docker build --build-arg URL='https:\/\/127.0.0.1' -t $(UI_NAME) .

crun: elk cbuilds
	sudo docker rm -f "$(API_NAME)"
	sudo docker run -d --net=host --restart=always --name="$(API_NAME)" "$(API_NAME)"
	sudo docker rm -f "$(UI_NAME)"
	sudo docker run -d --net=host --restart=always --name="$(UI_NAME)" "$(UI_NAME)"

clean:
	sudo docker compose down --remove-orphans
	sudo docker rm -f opensearch
	sudo docker rm -f opensearch_dashboards
	sudo docker rm -f paradrop_ui
	sudo docker rm -f paradrop_api
	sudo docker system prune -af
	rm -rf ./super-linter.log ./error_log.log ./api/error_log.log ./ui/package-lock.json ./build.log ./ui/build.log ./api/.pyre ./api/test_log ./api/test_log.log ./ui/static/css_min ./ui/static/js_min || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} \; || true
	find . -type d -name 'flask_session' -exec rm -rf {} \; || true
	find . -type d -name '__pycache__' -exec rm -rf {} \; || true
	find . -type d -name 'node_modules' -exec rm -rf {} \; || true
	find . -type f -name 'localhost.*' -exec rm -f {} \; || true

pip:
	pip3 install -r ./api/requirements.txt

pytest:
	cd ./api && python3 -m unittest

lint:
	pip3 install --upgrade autopep8 pyflakes pyre-check
	./lint.sh

superlinter:
	sudo docker run --name=superlinter -e RUN_LOCAL=true -e VALIDATE_CSS=false -v $(PWD):/tmp/lint github/super-linter
	sudo docker logs superlinter 2>./superlinter.log
