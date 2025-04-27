---
title: Local HAProxy, ProxySQL Cluster, Monitoring and MariaDB Galera Cluster with docker-compose
date: 2025-04-27 10:00:00 +0900
description: Hands-on setting up local MariaDB Galera Cluser and monitoring with docker-compose
comments: false
mermaid: true
categories: [Tech, Monitoring, Visualization, DevOps, SRE]
tags: [monitoring, visualization, local galera cluster, prometheus, grafana]
---

## Objective

In this post, we’ll guide you through setting up MariaDB Galera Cluster with monitoring.
This post is the final post in a series of three on setting up a local Galera cluster.
As the last series of the following three posts, I want to set up monitoring system with Prometheus and Grafana.

1. [Just MariaDB Galera Cluster](https://high-tail.github.io/posts/mariadb-galera-cluster)
2. [with ProxySQL Cluster](https://high-tail.github.io/posts/mariadb-galera-cluster-proxysql)
3. [with HAProxy](https://high-tail.github.io/posts/mariadb-galera-cluster-proxysql-haproxy)

## Prerequisites

- A bit of knowledge about Docker and docker-compose will be helpful for this setup

> My Environment
>
> | Software       | Version |
> | :------------- | :------ |
> | colima         | 0.8.1   |
> | docker CLI     | 27.5.1  |
> | docker-compose | 2.33.0  |
>
{: .prompt-tip }

## Overview

### What is the Prometheus ?

[Prometheus](https://prometheus.io/docs/introduction/overview/) is an open-source monitoring and alerting toolkit originally build at SoundCloud.
Prometheus provides three main things:

1. Metrics Collection
2. Time-Series Database
3. Querying and Alerting

### What is the Grafana ?

[Grafana](https://grafana.com/docs/grafana/latest/) is an open-source visualization and analytics platform.
Grafana provides two main things:

1. Data Visualization
2. Dashboard Building

In this post, we will use Prometheus as datasource for dashboard.

### Local MariaDB Galera Cluster Ecosystem Overview
> Simple Image
>```mermaid
>architecture-beta
>    group cluster[Galera Cluster Ecosystem]
>    group client[Client]
>    group monitor[Monitor]
>
>    service app(server)[Application] in client
>    service HAProxy(server) [HAProxy] in cluster
>    service ProxySQL(server) [ProxySQL Cluster] in cluster
>    service MariaDBGaleraCluster(database)[MariaDB Galera Cluster] in cluster
>    service Prometheus(internet)[Prometheus] in monitor
>    service Grafana(internet)[Grafana] in monitor
>
>    HAProxy:R -- L:ProxySQL
>    ProxySQL:B -- T:MariaDBGaleraCluster
>    Prometheus:R -- L:Grafana
>
>    app{group}:R -- L:HAProxy{group}
>    MariaDBGaleraCluster{group}:R -- L:Prometheus{group}
>    
>```
{: .prompt-info }

## Deploy Using docker-compose

### File Structure[^fn-nth-1]

```
.
├── compose.yml # Update
└── docker/
    ├── db/
    │   ├── start_services.sh # New
    │   ├── start_services_bootstrap.sh # New
    │   ├── Dockerfile # Update
    │   ├── Dockerfile1 # New
    │   └── conf/
    │       └── exporter.cnf # New
    ├── grafana/ # New
    │   ├── Dockerfile
    │   └── ...
    ├── prometheus/ # New
    │   ├── Dockerfile
    │   └── conf/
    │       └── prometheus.yml
    ├── proxysql/
    │   ├── Dockerfile
    │   └── conf/
    │       └── proxysql.cnf # Update
    └── haproxy/
        ├── Dockerfile
        └── conf/
            └── haproxy.cfg # Update
```

#### **`compose.yml`**

```yml
services:
  # MariaDB Galera Cluster
  node1: # Bootstrap node
    container_name: node1
    hostname: node1
    build:
      context: ./docker/db
      dockerfile: Dockerfile1 # Update for Prometheus
    volumes:
      - ./docker/db/conf/node1.cnf:/etc/mysql/conf.d/my.cnf
      - ./docker/db/conf/exporter.cnf:/etc/.my.cnf # Update for Prometheus
      - ./docker/db/initdb.d:/docker-entrypoint-initdb.d
    environment:
      MARIADB_ROOT_PASSWORD: root
      MARIADB_DATABASE: root
    healthcheck:
      test:
        [
          "CMD",
          "healthcheck.sh",
          "--connect",
          "--su-mysql",
          "--innodb_initialized",
          "--galera_online",
        ]
      start_period: 10s
      interval: 5s
      timeout: 5s
      retries: 5
  node2:
    container_name: node2
    hostname: node2
    build: ./docker/db # Update for Prometheus
    volumes:
      - ./docker/db/conf/node2.cnf:/etc/mysql/conf.d/my.cnf
      - ./docker/db/conf/exporter.cnf:/etc/.my.cnf # Update for Prometheus
    environment:
      MARIADB_ROOT_PASSWORD: root
      MARIADB_DATABASE: root
    depends_on:
      node1: { condition: service_healthy }
  node3:
    container_name: node3
    hostname: node3
    build: ./docker/db # Update for Prometheus
    volumes:
      - ./docker/db/conf/node3.cnf:/etc/mysql/conf.d/my.cnf
      - ./docker/db/conf/exporter.cnf:/etc/.my.cnf # Update for Prometheus
    environment:
      MARIADB_ROOT_PASSWORD: root
      MARIADB_DATABASE: root
    depends_on:
      node1: { condition: service_healthy }
      node2: { condition: service_started }

  # ProxySQL Cluster
  proxysql1:
    container_name: proxysql1
    hostname: proxysql1
    build: ./docker/proxysql
    volumes:
      - ./docker/proxysql/conf/proxysql.cnf:/etc/proxysql.cnf # Update for Prometheus
    depends_on:
      node1: { condition: service_healthy }
      node2: { condition: service_started }
      node3: { condition: service_started }
  proxysql2:
    container_name: proxysql2
    hostname: proxysql2
    build: ./docker/proxysql
    volumes:
      - ./docker/proxysql/conf/proxysql.cnf:/etc/proxysql.cnf
    depends_on:
      node1: { condition: service_healthy }
      node2: { condition: service_started }
      node3: { condition: service_started }
      proxysql1: { condition: service_started }
  proxysql3:
    container_name: proxysql3
    hostname: proxysql3
    build: ./docker/proxysql
    volumes:
      - ./docker/proxysql/conf/proxysql.cnf:/etc/proxysql.cnf
    depends_on:
      node1: { condition: service_healthy }
      node2: { condition: service_started }
      node3: { condition: service_started }
      proxysql1: { condition: service_started }
      proxysql2: { condition: service_started }

  # HAProxy
  haproxy:
    container_name: haproxy
    hostname: haproxy
    build: ./docker/haproxy
    volumes:
      - ./docker/haproxy/conf/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg # Update for Prometheus
    depends_on:
      proxysql1: { condition: service_started }
      proxysql2: { condition: service_started }
      proxysql3: { condition: service_started }
    ports:
      - 6033:6033
      - 8404:8404

  # DevOps (New Section)
  ## Prometheus
  prometheus:
    container_name: prometheus
    hostname: prometheus
    build: ./docker/prometheus
    volumes:
      - ./docker/prometheus/conf/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    depends_on:
      - haproxy

  ## Grafana
  grafana:
    container_name: grafana
    hostname: grafana
    build: ./docker/grafana
    volumes:
      - ./docker/grafana/conf/grafana.ini:/etc/grafana/grafana.ini
      - ./docker/grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./docker/grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
      - ./docker/grafana/dashboards:/var/lib/grafana/dashboards
    ports:
      - 3000:3000
    depends_on:
      - prometheus
```

### What are the updates
#### **`haproxy.cfg`**
To collect HAproxy's metrics through Prometheus, we need to set the following [settings](https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/prometheus/):
```conf
frontend stats
    http-request use-service prometheus-exporter if { path /metrics }
```

#### **`proxysql.cng`**
To collect ProxySQL cluster's metrics through Prometheus, we need to set the following [settings](https://proxysql.com/documentation/prometheus-exporter/):
```conf
admin_variables=
{
    web_enabled=true
    web_port=6080
    restapi_enabled=true
    restapi_port=6070
    prometheus_memory_metrics_interval=60
}
```

#### **`docker/db/Dockerfile`**
To collect MariaDB itself and server's metrics through Prometheus, I updated Dockerfile with [node_exporter](https://github.com/prometheus/node_exporter) and [mysqld_exporter](https://github.com/prometheus/mysqld_exporter).
```Dockerfile
FROM mariadb:latest
RUN apt-get update && apt-get install -y vim galera-4 wget

# Install Node Exporter
RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz \
    && tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz \
    && mv node_exporter-1.3.1.linux-amd64/node_exporter /usr/local/bin/ \
    && rm -rf node_exporter-1.3.1.linux-amd64 node_exporter-1.3.1.linux-amd64.tar.gz

# Install MySQL Exporter
RUN wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.14.0/mysqld_exporter-0.14.0.linux-amd64.tar.gz \
    && tar xvfz mysqld_exporter-0.14.0.linux-amd64.tar.gz \
    && mv mysqld_exporter-0.14.0.linux-amd64/mysqld_exporter /usr/local/bin/ \
    && rm -rf mysqld_exporter-0.14.0.linux-amd64 mysqld_exporter-0.14.0.linux-amd64.tar.gz

# Copy the start_services.sh script into the container
COPY start_services.sh /usr/local/bin/start_services.sh
RUN chmod +x /usr/local/bin/start_services.sh

# Expose ports for Node Exporter and MySQL Exporter
EXPOSE 9100 9104

ENTRYPOINT ["/usr/local/bin/start_services.sh"]
```

##### **`docker/db/start_services.sh` and `docker/db/start_services_bootstrap.sh`**
To execute MariaDB, node_exporter, and mysqld_exporter, I created two bash scripts with distinct purposes:

- **`start_services.sh`**: Used for regular MariaDB container startup.
- **`start_services_bootstrap.sh`**: Used for bootstrapping the MariaDB Galera Cluster.

Both scripts start MariaDB, node_exporter, and mysqld_exporter, but the bootstrap script includes the `--wsrep-new-cluster` flag for initializing the Galera Cluster.

Example content of `start_services.sh`:
```bash
#!/bin/sh

# Start MariaDB with the original entry point
docker-entrypoint.sh mariadbd &

# Start Node Exporter
node_exporter &

# Start MySQL Exporter
mysqld_exporter --config.my-cnf=/etc/.my.cnf &

# Keep the container running
tail -f /dev/null
```

#### **`docker/db/Dockerfile1`**
To collect MariaDB itself and server's metrics through Prometheus, I updated Dockerfile with [node_exporter](https://github.com/prometheus/node_exporter) and [mysqld_exporter](https://github.com/prometheus/mysqld_exporter).
```Dockerfile
FROM mariadb:latest
RUN apt-get update && apt-get install -y vim galera-4 wget

# Install Node Exporter
RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz \
    && tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz \
    && mv node_exporter-1.3.1.linux-amd64/node_exporter /usr/local/bin/ \
    && rm -rf node_exporter-1.3.1.linux-amd64 node_exporter-1.3.1.linux-amd64.tar.gz

# Install MySQL Exporter
RUN wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.14.0/mysqld_exporter-0.14.0.linux-amd64.tar.gz \
    && tar xvfz mysqld_exporter-0.14.0.linux-amd64.tar.gz \
    && mv mysqld_exporter-0.14.0.linux-amd64/mysqld_exporter /usr/local/bin/ \
    && rm -rf mysqld_exporter-0.14.0.linux-amd64 mysqld_exporter-0.14.0.linux-amd64.tar.gz

# Copy the start_services_bootstrap.sh script into the container
COPY start_services_bootstrap.sh /usr/local/bin/start_services_bootstrap.sh
RUN chmod +x /usr/local/bin/start_services_bootstrap.sh

# Expose ports for Node Exporter and MySQL Exporter
EXPOSE 9100 9104

ENTRYPOINT ["/usr/local/bin/start_services_bootstrap.sh"]
```

### What are new
#### **`docker/prometheus/conf/prometheus.yml`**

```yaml
global:
  scrape_interval: "15s"
  evaluation_interval: "15s"
  
scrape_configs:
  - job_name: 'proxysql1'    
    static_configs:
      - targets: ['proxysql1:6070'] # To collect one of the ProxySQL's data
  - job_name: 'proxysql2'
    static_configs:
      - targets: ['proxysql2:6070'] # To collect one of the ProxySQL's data
  - job_name: 'proxysql3'
    static_configs:
      - targets: ['proxysql3:6070'] # To collect one of the ProxySQL's data
  - job_name: 'haproxy'
    static_configs:
      - targets: ['haproxy:8404'] # To collect HAProxy's data
  - job_name: 'node1'
    static_configs: 
      - targets: ['node1:9100', 'node1:9104'] # To collect node_exporter(port: 9100)'s and mysqld_exporter(port: 9104)'s data
  - job_name: 'node2'   
    static_configs:
      - targets: ['node2:9100', 'node2:9104'] # To collect node_exporter(port: 9100)'s and mysqld_exporter(port: 9104)'s data
  - job_name: 'node3'
    static_configs:
      - targets: ['node3:9100', 'node3:9104'] # To collect node_exporter(port: 9100)'s and mysqld_exporter(port: 9104)'s data
```

#### **`docker/grafana/provisioning/datasources/datasource.yml`**
```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090 # Promethues container
    isDefault: true
    editable: true
```


### How to start

To start all containers, run the following commands:

```bash
# 1. Build containers
docker-compose build

# 2. Run containers 
docker-compose up -d

# (and the result of command should be like the below)
[+] Running 10/10
 ✔ Network local-galera-cluster_default  Created
 ✔ Container node1                       Healthy
 ✔ Container node2                       Started
 ✔ Container node3                       Started
 ✔ Container proxysql1                   Started
 ✔ Container proxysql3                   Started
 ✔ Container haproxy                     Started
 ✔ Container prometheus                  Started
 ✔ Container grafana                     Started
```

#### Now we're ready!

You can connect to the MariaDB Galera Cluster ecosystem.

|Service|WebUI|
| -- | -- |
|HAProxy|http://localhost:8404/stats|
|Prometheus|http://localhost:9090/query|
|Grafana|http://localhost:3000|


## Completed Plan: Set up for DevOps
I've achieved my goals to have a local environment of MariaDB Galera Cluster ecosystems!
- [x] [HAProxy](https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/): L4 Load Balancer
- [x] [ProxySQL](https://proxysql.com/documentation/): Read and Write Splitting
- [x] [Grafana](https://grafana.com/docs/)
  - [x] [Prometheus](https://prometheus.io/docs/introduction/overview/)
  - [x] [mysqld_exporter](https://github.com/prometheus/mysqld_exporter)

## Links

<!-- Footnotes -->

[^fn-nth-1]: [Entire Code](https://github.com/high-tail/local-galera-cluster/tree/main) - This repository contains the complete setup and configuration files for the local MariaDB Galera Cluster ecosystem, including HAProxy, ProxySQL, Prometheus, and Grafana.

<!-- Links -->
