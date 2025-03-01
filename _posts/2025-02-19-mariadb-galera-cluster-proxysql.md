---
title: Local ProxySQL Cluster and MariaDB Galera Cluster with docker-compose
date: 2025-03-01 10:00:00 +0900
description: Hands-on setting up local ProxySQL Cluster with docker-compose
comments: false
mermaid: true
categories: [Tech, Database]
tags: [database]
---

## Objective
In this post, we'll walk through the process of deploying ProxySQL Cluster using Docker Compose.

## Prerequisites

- A bit of knowledge about Docker and docker-compose will be helpful for this setup
- [Local MariaDB Galera Cluster environment (e.g., you can refer my previous post)](/posts/mariadb-galera-cluster/)

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

### What is the ProxySQL / ProxySQL Cluster?

#### ProxySQL
[ProxySQL](https://proxysql.com/documentation/) is an open source proxy middleware between application and database.
ProxySQL can work as L7 (Application Layer) proxy because it understands the MySQL and PostgreSQL protocols and features.
And we can define query rules to control database traffic. In this post, I will use this feature for read and write splitting in the MariaDB Galera Cluster.

#### ProxySQL Cluster
[ProxySQL Cluster](https://proxysql.com/documentation/proxysql-cluster/) is also provide a high-availability (HA) L7 load balancing system with a feature that allows multiple ProxySQL instances to be grouped together to form a single proxy server.
If we update one of node's configrations, it will be shared to all nodes.

#### Galera Cluster with ProxySQL
ProxySQL supports Galera Cluster configurations[^fn-nth-2][^fn-nth-3].
We can monitor and define Galera Cluster status.
For instance, assign one node as a writer node and so on.

## Deploy Using docker-compose

### File Structure[^fn-nth-1]

```
.
├──docker
│   ├──db
│   │   └──initdb.d
│   │       └──0_init.sql
│   │
│   └──proxysql
│       └──conf
│           └──proxysql.cnf
└── compose.yml
```

#### **`compose.yml`**

```yml
services:
  # === Galera Cluster ===
  # If you do not have Galera Cluster settings,
  # please refer previous post for more detail.
  node1:
    volumes:
      - ./docker/db/initdb.d:/docker-entrypoint-initdb.d # Mount proxysql user
  node2:
    volumes:
      - ./docker/db/initdb.d:/docker-entrypoint-initdb.d # Mount proxysql user
  node3:
    volumes:
      - ./docker/db/initdb.d:/docker-entrypoint-initdb.d # Mount proxysql user

  # === ProxySQL Cluster ===
  proxysql1:
    container_name: proxysql1
    hostname: proxysql1
    build: ./docker/proxysql
    volumes:
      - ./docker/proxysql/conf/proxysql.cnf:/etc/proxysql.cnf
    depends_on:
      - node1
      - node2
      - node3
  proxysql2:
    container_name: proxysql2
    hostname: proxysql2
    build: ./docker/proxysql
    volumes:
      - ./docker/proxysql/conf/proxysql.cnf:/etc/proxysql.cnf
    depends_on:
      - node1
      - node2
      - node3
      - proxysql1
  proxysql3:
    container_name: proxysql3
    hostname: proxysql3
    build: ./docker/proxysql
    volumes:
      - ./docker/proxysql/conf/proxysql.cnf:/etc/proxysql.cnf
    depends_on:
      - node1
      - node2
      - node3
      - proxysql1
      - proxysql2
```

#### **`0_init.sql`**

```sql
-- ProxySQL user
CREATE USER IF NOT EXISTS 'monitor'@'%' IDENTIFIED BY 'monitor' with MAX_USER_CONNECTIONS 9;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'monitor'@'%';

```

#### **`proxysql.cnf`**

```conf
cluster_sync_interfaces=false
admin_variables=
{
    admin_credentials="radmin:radmin;cluster_user:cluster_pass"
    mysql_ifaces="0.0.0.0:6032"
    cluster_username="cluster_user"
    cluster_password="cluster_pass"
}

mysql_variables=
{
    interfaces="0.0.0.0:6033"
    monitor_ping_timeout=999
}

; ProxySQL Cluster Configration
proxysql_servers =
(
    {
        hostname="proxysql1"
        port=6032
        weight=0
        comment="proxysql01"
    },
    {
        hostname="proxysql2"
        port=6032
        weight=0
        comment="proxysql02"
    },
    {
        hostname="proxysql3"
        port=6032
        weight=0
        comment="proxysql03"
    },
)

; Galera Cluster Configuration
mysql_galera_hostgroups =
(
    {
        writer_hostgroup=1001
        reader_hostgroup=1002
        backup_writer_hostgroup=1003
        offline_hostgroup=1999
        active=1
        max_writers=1
    }
)

; Assigning each node to hostgroup
mysql_servers =
(
    {
        address="node1",
        port=3306,
        hostgroup=1001,
        weight=1001,
        max_connections=10000,
        comment="node01"
    },
    {
        address="node2",
        port=3306,
        hostgroup=1001,
        weight=1000,
        max_connections=10000,
        comment="node02"
    },
    {
        address="node3",
        port=3306,
        hostgroup=1001,
        weight=999,
        max_connections=10000,
        comment="node03"
    },
    {
        address="node1",
        port=3306,
        hostgroup=1002,
        weight=1001,
        max_connections=10000,
        comment="node01"
    },
    {
        address="node2",
        port=3306,
        hostgroup=1002,
        weight=1000,
        max_connections=10000,
        comment="node02"
    },
    {
        address="node3",
        port=3306,
        hostgroup=1002,
        weight=999,
        max_connections=10000,
        comment="node03"
    },
    {
        address="node2",
        port=3306,
        hostgroup=1003,
        weight=1000,
        max_connections=10000,
        comment="node02"
    },
    {
        address="node3",
        port=3306,
        hostgroup=1003,
        weight=999,
        max_connections=10000,
        comment="node03"
    },
)

; Read and Write Splitting
mysql_query_rules =
(
        {
            rule_id=1
            active=1
            match_pattern="^SELECT .* FOR UPDATE"
            destination_hostgroup=1001
            apply=1
        },
        {
            rule_id=2
            active=1
            match_pattern="^SELECT"
            destination_hostgroup=1002
            apply=1
        },
        {
            rule_id=3
            active=1
            match_pattern=".*"
            destination_hostgroup=1001
            apply=1
        }
)
```

### How to start
To start the cluster, run the following commands:
```bash
# 1. Build containers
docker-compose build

# 2. Run containers
docker-compose up -d

# 3. Login to DB container
docker-compose exec proxysql1 bash # or proxysql2, proxysql3
```

#### Check ProxySQL Cluster Status
To check the cluster status, login to ProxySQL and run the following query:
```bash
# 1. Login to ProxySQL
mysql -uradmin -pradmin -P6032

# 2. Check ProxySQL Cluster Status
MySQL [(none)]> SELECT * FROM proxysql_servers;
+-----------+------+--------+------------+
| hostname  | port | weight | comment    |
+-----------+------+--------+------------+
| proxysql1 | 6032 | 0      | proxysql01 |
| proxysql2 | 6032 | 0      | proxysql02 |
| proxysql3 | 6032 | 0      | proxysql03 |
+-----------+------+--------+------------+
3 rows in set (0.001 sec)

MySQL [(none)]> SELECT * FROM stats_proxysql_servers_metrics;
+-----------+------+--------+------------+------------------+----------+---------------+---------+------------------------------+----------------------------+
| hostname  | port | weight | comment    | response_time_ms | Uptime_s | last_check_ms | Queries | Client_Connections_connected | Client_Connections_created |
+-----------+------+--------+------------+------------------+----------+---------------+---------+------------------------------+----------------------------+
| proxysql3 | 6032 | 0      | proxysql03 | 8                | 2423     | 4463          | 0       | 0                            | 0                          |
| proxysql2 | 6032 | 0      | proxysql02 | 13               | 2423     | 4457          | 0       | 0                            | 0                          |
| proxysql1 | 6032 | 0      | proxysql01 | 16               | 2424     | 4453          | 0       | 0                            | 0                          |
+-----------+------+--------+------------+------------------+----------+---------------+---------+------------------------------+----------------------------+
3 rows in set (0.002 sec)
```

#### Check ProxySQL Configuration for Galera Cluster
To check the ProxySQL settings for Galera Cluster status, login to ProxySQL and run the following query:
```bash
# 1. Login to ProxySQL
mysql -uradmin -pradmin -P6032

# 2. Check Galera Cluster Status
ySQL [(none)]> select * from mysql_servers;
+--------------+----------+------+-----------+--------+--------+-------------+-----------------+---------------------+---------+----------------+---------+
| hostgroup_id | hostname | port | gtid_port | status | weight | compression | max_connections | max_replication_lag | use_ssl | max_latency_ms | comment |
+--------------+----------+------+-----------+--------+--------+-------------+-----------------+---------------------+---------+----------------+---------+
| 1001         | node1    | 3306 | 0         | ONLINE | 1001   | 0           | 10000           | 0                   | 0       | 0              | node01  |
| 1001         | node2    | 3306 | 0         | ONLINE | 1000   | 0           | 10000           | 0                   | 0       | 0              | node02  |
| 1001         | node3    | 3306 | 0         | ONLINE | 999    | 0           | 10000           | 0                   | 0       | 0              | node03  |
| 1002         | node1    | 3306 | 0         | ONLINE | 1001   | 0           | 10000           | 0                   | 0       | 0              | node01  |
| 1002         | node2    | 3306 | 0         | ONLINE | 1000   | 0           | 10000           | 0                   | 0       | 0              | node02  |
| 1002         | node3    | 3306 | 0         | ONLINE | 999    | 0           | 10000           | 0                   | 0       | 0              | node03  |
| 1003         | node2    | 3306 | 0         | ONLINE | 1000   | 0           | 10000           | 0                   | 0       | 0              | node02  |
| 1003         | node3    | 3306 | 0         | ONLINE | 999    | 0           | 10000           | 0                   | 0       | 0              | node03  |
+--------------+----------+------+-----------+--------+--------+-------------+-----------------+---------------------+---------+----------------+---------+

MySQL [(none)]> select * from mysql_galera_hostgroups\G
*************************** 1. row ***************************
       writer_hostgroup: 1001
backup_writer_hostgroup: 1003
       reader_hostgroup: 1002
      offline_hostgroup: 1999
                 active: 1
            max_writers: 1
  writer_is_also_reader: 0
max_transactions_behind: 0
                comment:
1 row in set (0.003 sec)

MySQL [(none)]> select hostgroup_id, hostname, port, gtid_port, status, weight from runtime_mysql_servers;
+--------------+----------+------+-----------+---------+--------+
| hostgroup_id | hostname | port | gtid_port | status  | weight |
+--------------+----------+------+-----------+---------+--------+
| 1001         | node1    | 3306 | 0         | ONLINE  | 1001   |
| 1001         | node2    | 3306 | 0         | SHUNNED | 1000   |
| 1001         | node3    | 3306 | 0         | SHUNNED | 999    |
| 1003         | node2    | 3306 | 0         | ONLINE  | 1000   |
| 1003         | node3    | 3306 | 0         | ONLINE  | 999    |
+--------------+----------+------+-----------+---------+--------+
5 rows in set (0.005 sec)

```

#### Now we're redy!
We have MariaDB Galera Cluster with ProxySQL Cluster.
Next plan is to set up HAProxy as L4 load balancer.
I want to connect this environemnt via HAProxy.

## Next Plan: Set up for DevOps

- [HAProxy](https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/): L4 Load Balancer
- ~~[ProxySQL](https://proxysql.com/documentation/): Read and Write Splitting~~
- [Grafana](https://grafana.com/docs/)
  - [Prometheus](https://prometheus.io/docs/introduction/overview/)
  - [mysqld_exporter](https://github.com/prometheus/mysqld_exporter)

## Links
<!-- Footnotes -->
[^fn-nth-1]: [Entire Code](https://github.com/high-tail/local-galera-cluster/tree/proxysql)
[^fn-nth-2]: [Galera Configuration](https://proxysql.com/documentation/galera-configuration/)
[^fn-nth-3]: [Effortlessly Scaling out Galera Cluster with ProxySQL]( https://proxysql.com/blog/effortlessly-scaling-out-galera-cluster-with-proxysql/)

<!-- Links -->
