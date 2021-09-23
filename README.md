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

With the way the repository is set up all instructions to build the project are included in the docker-copose.yml which then builds each container's respective Dockerfile 

## Build Rotation

1. Build
2. Start
3. Make changes
4. Rebuild
5. Test
	* if not done go back to 3
6. Shutdown

### Example

``` bash
docker-compose build --no-cache # 1 Build
docker-compose up -d # 2 Start
# Code changes are happening
docker-compose build --no-cache # 4 Rebuild
# Tests are being run
docker-compose down # 6 shutdown the containers
```
NOTE: 
* when building the --no-cache flag is important so that the all the changes are actually brought in when building

## Container Set Up

```ascii
+-------------------------------------------------+  +------------------+
| Docker                                          |  | Localhost        |
|                                                 |  |                  |
|   +---------+             +-----------+         |  |                  |
|   |         |             |           |         |  |                  |
|   |  mysql  <------------->  adminer  <-------------->Localhost:8080  |
|   |         |:6603   3306:|           |:8080    |  |                  |
|   +----^----+             +-----------+         |  |                  |
|        |                                        |  |                  |
|   +-----------------------------------------+   |  |                  |
|   |    |             Python                 |   |  |                  |
|   | +-------------------------------------+ |   |  |                  |
|   | |  |             Flask                | |   |  |                  |
|   | | +v------------+    +--------------+ | |   |  |                  |
|   | | |SQLAlchemy   +<---+RESTFUL       | | |   |  |                  |
|   | | |             |    |              +------------>Localhost:8000  |
|   | | |             +---->              | | |   |  |                  |
|   | | +-------------+    +--------------+ | |   |  |                  |
|   | +-------------------------------------+ |   |  |                  |
|   +-----------------------------------------+   |  |                  |
|                                                 |  |                  |
|   +-----------------------------------------+   |  |                  |
|   |                                         |   |  |                  |
|   |           Volumes                       |   |  |                  |
|   |            mysql:                       |   |  |                  |
|   |             /var/lib/mysql---------------------->/databse-folder/ |
|   |                                         |   |  |                  |
|   +-----------------------------------------+   |  |                  |
|                                                 |  |                  |
+-------------------------------------------------+  +------------------+

```

### Requirements Explained
1. Flask -> Python REST functionality
2. Flask-Restful -> Simplifies Flask's REST functionality
3. Flask-SQLAlchemy -> Simplifies python SQL functionality 
4. mysql-connector-python -> Connector drivers from python code to an SQL databse
5. Flask-Marshmallow -> serialization that works with Flask-SQLAlchemy  
6. Gunicorn -> Runs the web Listener for a WGSI application
