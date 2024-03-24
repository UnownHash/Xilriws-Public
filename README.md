# Xilriws

This is a very hastely written solution to PTC's new Imperva protection. It uses 
a real browser to pass it every ~15 minutes. All other logins are done like in the 
past.

## Docker installation (recommended)

TODO

copy the docker-compose config to your existing docker-compose file for the unown# stack, or on its own.
if you have it on its own, you will need to make sure to uncomment the port mapping lines in the compose file. 
keep in mind there is no authentication on this, so avoid exposing it to the public internet if possible. 

copy `config.json.example` somewhere into the path of wherever your docker-compose file is, and name it whatever you'd like.
update the `volumes` section in the docker-compose to match the file name and path of the new config file

start the container with `docker-compose up -d`

in your Dragonite config, add: 

```toml
[general]
remote_auth_url = "http://maltelogin:<port>/v1/login-code"
```

this assumes you have everything in the same docker network. if you're hosting it externally, change the `maltelogin` hostname to
something else accordingly.


## Manual installation (not recommended)

Note that this has to be run without root.

copy config.example.json to config.json

you need chromedriver installed, and it needs to be in your `PATH`.
The easiest way to do this on ubuntu-like operating systems is `sudo apt install chromium-driver`.



