## Usage

- For local development, start https://github.com/schul-cloud/schul_cloud_resources_server_tests on localhost. 
- Run `app.py`

### Configuration 
Configuration uses environment variables found in `src/settings.py`.
For docker you can use `local.env` to overwrite the environment variables. `local.env` is ignored by `git`.
For local usage, no configuration should be necessary.

## Run crawler and resource-api server in docker

`docker-compose -f docker-compose.yml -f docker-compose.test.yml up`
