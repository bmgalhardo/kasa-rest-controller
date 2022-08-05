# kasa smart plug controller

Tested with HS110(EU). May work for other models.

Plugs are discovered by broadcasting with `BROADCAST_IP` defined in an env variable. Since we are running in the host network to be able to discover 
the devices set the `PORT` variable if 80 is already used.

## API

Documentation can be found in `/docs`.

Endpoints:
- `[GET] /discover`: returns discovered devices
- `[POST] /readings`: data={"ip": ip}, retrieve measurements
- `[POST] /label`: data={"ip": ip, "name": name}, set new alias for device
- `[POST] /switch`: data={"ip": ip}, on->off OR off->on the given device
- `[POST] /info`: data={"ip": ip}, retrieve device information
- `[GET] /metrics`: prometheus metrics

## Prometheus metrics

Provides metrics of discoverable devices and
assigns labels according to the label field. 
Point the scraper to /metrics.

Discovery of plugs runs every 30s. 
For other value set the env variable `DISCOVERY_PERIOD`.
Values are updated every 10s. 
For other value set the env variable `UPDATE_PERIOD`

## To run

with docker
```commandline
docker build -t kasa-smartplug src/
docker run -d --network host kasa-smartplug
```

with docker-compose
```commandline
docker-compose build
docker-compose up -d
```

with kubernetes
```commandline
kubectl apply -f https://raw.githubusercontent.com/bmgalhardo/kasa-controller/main/manifest.yml -n <namespace>
```