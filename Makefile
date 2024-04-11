build:
	# x86
	docker plugin install grafana/loki-docker-driver:2.9.1 --alias loki --grant-all-permissions
	docker compose build

build-arm:
	docker plugin install miacis/loki-docker-driver --alias loki --grant-all-permissions
	docker compose build
	
run:
	python3 sys_check.py && docker compose build && docker compose up -d
	
restart:
	docker compose restart

stop:
	docker compose down

kill:
	docker compose kill
	
test:
	$(MAKE) run
	docker exec uas-2024-vision-1 bash -c "pytest --durations=0 -s"
		
coverage:
	$(MAKE) run
	docker exec uas-2024-vision-1 bash -c "coverage run -m pytest; coverage html -i"
