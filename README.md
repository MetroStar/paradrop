<p align="center">
    <img width="214" height="42" src="./ui/static/assets/logo-red.png">
</p>

<h3 align="center">Simple, Easy Infrastructure Scanning</h3>

---

## Provision Elasticsearch and Kibana Docker Containers With Seed Data

From your local terminal in the paradrop directory:

```sh
cd elk
sudo ./seed.sh
```

## Access Elasticsearch and Kibana

Kibana - open your browser to <http://localhost:5601/>

Username: `admin`

Password: `dtYe2cKY2YtyBEJ49a`

The same username and password is used to access Elasticsearch.

Example GET request:

```sh
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -H 'Content-Type: application/json' 'https://localhost:9200/'
```

## Lint Code

From your local terminal in the paradrop directory:

```sh
./lint.sh
```

## Build API Docker Container

From your local terminal in the paradrop directory:

```sh
sudo ./start.sh
```

## Build UI Docker Container

From your local terminal in the paradrop directory:

```sh
cd ui
sudo ./start.sh
```

## Default Username and Password In paradrop_users Index

Username/Email: `admin@paradrop.io`

Password: `Paradrop789!`
