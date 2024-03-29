# Xilriws

Unlike [Swirlix](https://github.com/UnownHash/Swirlix-Public), Xilriws doesn't use a 3rd party, but a real browser instead. 
This has the advantage of being free and not requiring an account, but might result in some issues unique to your system. 
As such, a docker installation is highly recommended, even if the rest of your setup isn't dockerized.

## Installation

1. `git clone https://github.com/UnownHash/Xilriws-Public Xilriws && cd Xilriws`
2. `cp docker-compose.yml.example docker-compose.yml && cp xilriws.json.example xilriws.json`
3. `docker-compose up -d`

in your Dragonite config, add: 

```toml
[general]
remote_auth_url = "http://xilriws:5090/api/v1/login-code"
```

this assumes you have everything in the same docker network. if you're hosting it externally, change the hostname to
something else accordingly.

### Update

1. `git pull`
2. `docker compose pull`
3. `docker compose restart`

you can change the "replicas" number to alter how many copies of the container will be spawned. traefik manages load balancing,
and should work automatically. set this number in accordance with the avaliable RAM and CPU on your machine.

the more copies of the container, the lower you can set login delay
