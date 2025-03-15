---
title: Local HAProxy, ProxySQL Cluster and MariaDB Galera Cluster with docker-compose
date: 2025-03-15 10:00:00 +0900
description: Hands-on setting up local HAProxy with docker-compose
comments: false
mermaid: true
categories: [Tech, Load Balancers]
tags: [load balancers, local galera cluster, haproxy]
---

## Objective
In this post, we’ll guide you through setting up HAProxy to load balance a MariaDB Galera Cluster with ProxySQL Cluster. We covered this in the previous series. This setup lets you connect to the MariaDB Galera Cluster through ProxySQL Cluster.

## Prerequisites

- A bit of knowledge about Docker and docker-compose will be helpful for this setup
- [Local MariaDB Galera Cluster and ProxySQL Cluster environment (e.g., you can refer my previous post)](https://high-tail.github.io/posts/mariadb-galera-cluster-proxysql/)

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

### What is the HAProxy ?
[HAProxy](https://docs.haproxy.org/) is an open-source load balancer and proxy server for TCP and HTTP-based applications.
HAProxy can work as an L4 (Transport Layer) load balancer.
In this post, we will set up HAProxy configuration designed for L4 load balancing, as it operates at the TCP layer and routes traffic based on IP addresses and TCP ports without inspecting the content of the packets. This allows for efficient and fast load balancing of TCP connections.

In this post, we will set up an L4 load balancer to connect to one of the ProxySQL servers.

## Deploy Using docker-compose

### File Structure[^fn-nth-1]

```
.
├── compose.yml # Update
└── docker/
    ├── db/
    ├── proxysql/
    │   ├── Dockerfile
    │   └── conf/
    │       └── proxysql.cnf # Update
    └── haproxy/
        ├── Dockerfile # New
        └── conf/
            └── haproxy.cfg # New
```

#### **`compose.yml`**

```yml
services:
  # === Galera Cluster ===
  # If you do not have Galera Cluster settings,
  # please refer previous post for more detail.

  # === ProxySQL Cluster ===
  # If you do not have ProxySQL Cluster settings,
  # please refer previous post for more detail.
  
  # HAProxy
  haproxy:
    container_name: haproxy
    hostname: haproxy
    build: ./docker/haproxy
    volumes:
      - ./docker/haproxy/conf/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    depends_on:
      - proxysql1
      - proxysql2
      - proxysql3
    ports:
      - 6033:6033
      - 8404:8404
```

#### **`haproxy.cfg`**

```conf
defaults
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend stats
    mode http
    bind :8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST
    stats show-modules

frontend mysql
    mode tcp
    bind :6033
    default_backend proxysql-cluster

backend proxysql-cluster
    mode tcp
    balance roundrobin
    server proxysql1 proxysql1:6033 check port 6032
    server proxysql2 proxysql2:6033 check port 6032
    server proxysql3 proxysql3:6033 check port 6032
```

### How to start
To start the HAProxy, run the following commands:
```bash
# 1. Build containers
docker-compose build

# 2. Run containers
docker-compose up -d
```

#### Check HAProxy Status
You can check status via following URI
```text
http://localhost:8404/stats
```

#### Check connection to MariaDB Galera Cluster
To check the connection to MariaDB Galera Cluster status, you can use port=6033.
```bash
# 1. Login to one of ProxySQL via HAProxy
mysql -h localhost -P 6033 --protocol=tcp -uroot -p

# 2. Check connected node
mysql> show variables like 'hostname';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| hostname      | node1 |
+---------------+-------+
1 row in set (0.01 sec)
```
After this connection test, we will see HAProxy WebUI's sessions count had increased.

#### Now we're redy!
You can connect MariaDB Galera Cluster via HAProxy and ProxySQL Cluster.

## Next Plan: Set up for DevOps

- ~~[HAProxy](https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/): L4 Load Balancer~~
- ~~[ProxySQL](https://proxysql.com/documentation/): Read and Write Splitting~~
- [Grafana](https://grafana.com/docs/)
  - [Prometheus](https://prometheus.io/docs/introduction/overview/)
  - [mysqld_exporter](https://github.com/prometheus/mysqld_exporter)

## Links
<!-- Footnotes -->
[^fn-nth-1]: [Entire Code](https://github.com/high-tail/local-galera-cluster/tree/haproxy)

<!-- Links -->
