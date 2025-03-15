---
title: Local MariaDB Galera Cluster with docker-compose
date: 2025-02-19 20:30:00 +0900
description: Hands-on setting up local MariaDB Galera Cluster with docker-compose
comments: false
mermaid: true
categories: [Tech, Database]
tags: [database, local galera cluster]
---

## Objective
In this post, we'll walk through the process of deploying MariaDB Galera Cluster using Docker Compose.

## Prerequisites

A bit ofknowledge about docker, docker-compose, and MariaDB(MySQL).

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

### What is the Galera Cluster?

MariaDB Galera Cluster is a virturally synchronous multi-leader cluster for MariaDB.
It provides a high-availability (HA) database system.

MariaDB Galera Cluster is powered by:

- Multipule MariaDB servers
- Libraries are developed by [Codership][Galera Cluster]

> Simple Image
>```mermaid
>architecture-beta
>    group cluster[Galera Cluster]
>    group client[Client]
>
>    service app(server)[Application] in client
>    service node1(database)[Node1] in cluster
>    service node2(database)[Node2] in cluster
>    service node3(database)[Node3] in cluster
>
>    node1:B <--> T:node2
>    node1:B <--> T:node3
>    node2:L <--> R:node3
>
>    app{group}:R <--> L:node1{group}
>    
>```
{: .prompt-info }


## Deploy Using docker-compose
### File Structure[^fn-nth-1]
```
.
├──docker
│   └──db
│       └──conf
│           ├──node1.cnf
│           ├──node2.cnf
│           └──node3.cnf
└── compose.yml
```

#### **`compose.yml`**
```yml
services:
  node1:
    container_name: node1
    hostname: node1 # to connect each node
    build: ./docker/db
    volumes:
      - ./docker/db/conf/node1.cnf:/etc/mysql/conf.d/my.cnf # mount confing
    environment:
      MARIADB_ROOT_PASSWORD: root
      MARIADB_DATABASE: root
    command: --wsrep-new-cluster # Start as a starter of Galera Cluster
  node2:
    container_name: node2
    hostname: node2
    build: ./docker/db
    volumes:
      - ./docker/db/conf/node2.cnf:/etc/mysql/conf.d/my.cnf
    environment:
      MARIADB_ROOT_PASSWORD: root
      MARIADB_DATABASE: root
    depends_on:
      - node1
  node3:
    container_name: node3
    hostname: node3
    build: ./docker/db
    volumes:
      - ./docker/db/conf/node3.cnf:/etc/mysql/conf.d/my.cnf
    environment:
      MARIADB_ROOT_PASSWORD: root
      MARIADB_DATABASE: root
    depends_on:
      - node1
      - node2
```
#### **`node1.cnf`**
```conf
[mysqld]
binlog_format=ROW

[galera]
wsrep_on=ON
wsrep_cluster_name=my_galera
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_node_name=node1
wsrep_node_address=node1
wsrep_cluster_address=gcomm://node1,node2,node3
```

#### **`Dockerfile`**
```Dockerfile
FROM mariadb:latest
RUN apt-get update && apt-get install -y vim galera-4
```

### Start the Cluster
To start the cluster, run the following commands:
```bash
# 1. Build containers
docker-compose build

# 2. Run containers
docker-compose up -d

# 3. Login to DB container
docker-compose exec node1 bash # or node2, node3
```

#### Check Status
To check the cluster status, login to MariaDB and run the following query:
```bash
# 1. Login to MariaDB
mariadb -uroot -proot

# 2. Check Galera Cluster Status
MariaDB [(none)]> SHOW GLOBAL STATUS LIKE 'wsrep_cluster_size';
+--------------------+-------+
| Variable_name      | Value |
+--------------------+-------+
| wsrep_cluster_size | 3     |
+--------------------+-------+
```

#### Now you're ready!
If you can see wsrep_cluster_size = 3, now you are ready to use local MariaDB Galera Cluster!
You can test how MariaDB Galera Cluster work with this environment!

If you saw value is not 3, please check logs with the following command.

```bash
# You can specify container with node1 or node2 or node3
docker-compose logs -f
```

## Next Plan: Set up for DevOps
Now we have a very simple local MariaDB Galera Cluster.
Next plan is to add Proxy & Monitor services for DevOps.

- [HAProxy](https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/): L4 Load Balancer
- [ProxySQL](https://proxysql.com/documentation/): Read and Write Splitting
- [Grafana](https://grafana.com/docs/)
  - [Prometheus](https://prometheus.io/docs/introduction/overview/)
  - [mysqld_exporter](https://github.com/prometheus/mysqld_exporter)

## Links
<!-- Footnotes -->
[^fn-nth-1]: [Entire Code](https://github.com/high-tail/local-galera-cluster/tree/initial)
<!-- Links -->

[Galera Cluster]: https://galeracluster.com/
