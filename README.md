Hello World!

# Docker Flow

## Setup

1. Have docker-compose.yml in directory
2. run commands

``` bash
docker-compose build --no-cache
docker-compose up -d 
```

## Shutdown

```bash
docker-compose down
```

## Container Set Up

```ascii
                                        LocalHost
+----------------------------------------------^--+
|Docker                                   8080:|  |
|                                              |  |
|   +---------+             +-----------+      |  |
|   |         +------------->           |      |  |
|   |  mysql  <-------------+  adminer  +------+  |
|   |         |:6603   3306:|           |:8080    |
|   +---------+             +-----------+         |
|                                                 |
|                                                 |
|                       +---------------------+   |
|                       |Volumes              |   |
|   +----------+        | mysql:              |   |
|   |          |        |  /var/lib/mysql-----+---+->/storage/docker/mysql-data
|   | OpenJDK  |        | OpenJDK:            |   |
|   |          |        |  /opt/src-----------+---+->./src/
|   +----------+        |                     |   |
|                       +---------------------+   |
|                                                 |
+-------------------------------------------------+

```