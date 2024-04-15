# Determine Dockerfile based on the device type
ifeq ($(shell test -e "/sys/firmware/devicetree/base/model" && grep -q "NVIDIA Jetson" "/sys/firmware/devicetree/base/model"; echo $$?),0)
	DOCKERFILE := Dockerfile-jetson
	BUILD_TARGET := build-arm
else
	DOCKERFILE := Dockerfile
	BUILD_TARGET := build-x86
endif

export DOCKERFILE


build:
	$(MAKE) $(BUILD_TARGET)

build-arm:
	docker plugin install miacis/loki-docker-driver:2.9.1 --alias loki --grant-all-permissions
	docker compose build

build-x86:
	docker plugin install grafana/loki-docker-driver:2.9.1 --alias loki --grant-all-permissions
	docker compose build

clean:
	find vision/images/debug -type f -iname \*.png -delete

run:
	python3 sys_check.py && docker compose build && docker compose up -d

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
