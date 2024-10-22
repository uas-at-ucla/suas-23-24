# uas-2024/vision

## Getting Started
First, ensure you have [Git](https://git-scm.com/downloads) and [Docker](https://docs.docker.com/get-docker/) installed.

Then, clone this repo locally:

```
git clone https://github.com/uas-at-ucla/uas-2024
cd uas-2024
```

Note: If you get an issue saying that password authentication was removed, visit [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Build and run the Docker image:
```
make build
make run
```

Alternatively, if on an ARM CPU:
```
make build-arm
make run
```

The server will now be serving requests at localhost:8003. To test your
installation, go to [localhost:8003](http://localhost:8003) in your browser.
If you see "Hello World!" then your installation is working!

To run unittests:
```
make test
```
To see server visualization, go to [localhost:3000](http://localhost:3000) and navigate to the Vision Dashboard. Make sure to set the refresh rate.

## Development Tips:
+ Remember to add any downloaded libraries to `requirements.txt`
+ You can create environment variables by adding them in the `docker-compose.yml` file, under `services: web: environment:`
+ To view docker containers: `docker ps -a`
+ To view logs of processes within a container: `docker logs [container ID]`
+ To clean up dangling docker images, containers, etc.: `docker system prune`

## To use GPU in Docker Containers:
+ Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
+ Uncomment lines 14-20 in `docker-compose.yml`

Note: If running on the Jetson, change the Dockerfile on line 5 of `docker-compose.yml` to `Dockerfile-jetson`