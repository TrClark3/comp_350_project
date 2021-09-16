Hello World!

# Git Flow
When working on tasks, use the following order in handling git operations to avoid any sort of merge conflicts:

1. Switch to use case branch.
2. Pull from remote.
3. Resolve conflicts if there are any.
4. Complete work for commit.
5. Commit to local repository.
6. Pull from remote again.
7. Resolve conflicts if there are any.
8. Push to remote.

Make sure to commit as often as possible when working. A large amount of small commits is always better than a small amount of large commits. Maintaining good commit messages is also requested.

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
+-------------------------------------------------+  +------------------+
| Docker                                          |  | Localhost        |
|                                                 |  |                  |
|   +---------+             +-----------+         |  |                  |
|   |         +------------->           |         |  |                  |
|   |  mysql  <-------------+  adminer  +-------------->Localhost:8000  |
|   |         |:6603   3306:|           |:8080    |  |                  |
|   +---------+             +-----------+         |  |                  |
|                                                 |  |                  |
|   +----------+             +---------+          |  |                  |
|   |          |             |         |          |  |                  |
|   | OpenJDK  |             |  Httpd  +--------------->Localhost:8080  |
|   |          |             |         |:80       |  |                  |
|   +----------+             +---------+          |  |                  |
|                                                 |  |                  |
|   +-----------------------------------------+   |  |                  |
|   |           Volumes                       |   |  |                  |
|   |            mysql:                       |   |  |                  |
|   |             /var/lib/mysql+---------------------->./DB/           |
|   |            OpenJDK:                     |   |  |                  |
|   |             /opt/src+---------------------------->./Java/src      |
|   |            Httpd:                       |   |  |                  |
|   |             /usr/local/apache2/htdocs/+---------->./Web/          |
|   |                                         |   |  |                  |
|   +-----------------------------------------+   |  |                  |
|                                                 |  |                  |
+-------------------------------------------------+  +------------------+

```