# Xilriws

Unlike [Swirlix](https://github.com/UnownHash/Swirlix-Public), Xilriws doesn't use a 3rd party, but a real browser instead. 
This has the advantage of being free and not requiring an account, but might result in some issues unique to your system. 
As such, a docker installation is highly recommended, even if the rest of your setup isn't dockerized.

## Docker installation (recommended)

run `./run.sh` to download the xilriws binary and config file

build the Docker image with `docker build -t xilriws .`

copy the docker-compose config to your existing docker-compose file for the unown# stack, or on its own.
if you have it on its own, you will need to make sure to uncomment the port mapping lines in the compose file. 
keep in mind there is no authentication on this, so avoid exposing it to the public internet if possible. 

copy `config.json` somewhere into the path of wherever your docker-compose file is, and name it whatever you'd like.
the example docker-compose assumes it's named `xilriws.json`, and in the same directory as the docker-compose file. 
update the `volumes` section in the docker-compose to match the file name and path of the new config file

start the container with `docker-compose up -d`

in your Dragonite config, add: 

```toml
[general]
remote_auth_url = "http://xilriws:<port>/api/v1/login-code"
```

this assumes you have everything in the same docker network. if you're hosting it externally, change the `xilriws` hostname to
something else accordingly.


## Manual installation (not recommended)

Note that this has to be run without root.

run `./run.sh`

edit config.json as you need

you need chromedriver installed, and it needs to be in your `PATH`.
The easiest way to do this on ubuntu-like operating systems is `sudo apt install chromium-driver`.

run `./xilriws` to start the service





