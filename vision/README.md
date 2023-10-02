# uas-2024/vision

## Getting Started
First, ensure you have [Git](https://git-scm.com/downloads) and [Docker](https://docs.docker.com/get-docker/) installed.

Then, clone this repo locally:

```
git clone https://github.com/uas-at-ucla/uas-2024
cd suas-onboard/vision
```

Note: If you get an issue saying that password authentication was removed, visit [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Build and run the Docker image:
```
make build
make run
```
The server will now be serving requests at localhost:8003. To test your
installation, go to [localhost:8003](http://localhost:8003) in your browser.
If you see "Hello World!" then your installation is working!
