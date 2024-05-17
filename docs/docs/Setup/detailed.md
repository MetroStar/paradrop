---
id: Detailed Setup
slug: /setup/detailed
---

# Detailed Setup

More in-depth information about **paradrop**'s setup process is below.

## Provision ElasticSearch and Kibana Docker Containers with Seed Data

From your local terminal in the `paradrop` directory:

```sh
sudo ./provision_elk.sh
```

## Access ElasticSearch and Kibana

Kibana - open your browser to http://localhost:5601/

Username: `admin`

Password: `dtYe2cKY2YtyBEJ49a`

The same username and password is used to access Elasticsearch.

Example GET request:

```sh
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -H 'Content-Type: application/json' 'https://localhost:9200/'
```

## Lint and Auto-Format Python Code

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

## Default Username and Password

This information can be found in our [quick start guide](/setup/quickstart).
