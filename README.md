Hello World!

# Directory

* [directory](https://github.com/TrClark3/comp_350_project#directory)
* [git flow](https://github.com/TrClark3/comp_350_project#git-flow)
* [docker flow](https://github.com/TrClark3/comp_350_project#docker-flow)
	* [build](https://github.com/TrClark3/comp_350_project#build)
	* [container-set-up](https://github.com/TrClark3/comp_350_project#container-set-up)
* [python-app](https://github.com/TrClark3/comp_350_project#python-app)
	* [structure](https://github.com/TrClark3/comp_350_project#structure)
	* [requirements-explained](https://github.com/TrClark3/comp_350_project#requirements-explained)
* [acknowledgements](https://github.com/TrClark3/comp_350_project#acknowledgements)

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


mysql container
- container holds database and related triggers/procedures/etc
- Sets up Users.sql script on start up


python container  
- hosts and runs the application
- waits for the mysql container to be up and ready
- reloads itself on code change or on failure 


adminer container
- Web interface to directly interface with database

## Build
Only necessary if there are any changes to the structure of the project includes: new files to be added, configuration changes, switching git branches. 

Always build after switching branches to avoid errors

``` bash
docker-compose build --no-cache # 1 Build
docker-compose up [-d] # 2 Start [optionally with no logs]
docker-compose down -v # 6 shutdown the containers and remove created volumes
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
|   | | |SQLAlchemy   +<---+REST API      | | |   |  |                  |
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

# Python App

## Structure

```ascii
app/
├─ website/
│  ├─ static/
│  │  ├─ css/
│  │  │  ├─ main.css
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ book-services.html
│  │  ├─ index.html
│  │  ├─ login.html
│  │  ├─ services.html
│  │  ├─ sign-up.html
│  │  ├─ thanks.html
│  │  ├─ user-dashboard.html
│  ├─ __init__.py
│  ├─ ApplicationProgramInterface.py
│  ├─ config.py
│  ├─ initialize.py
│  ├─ models.py
│  ├─ views.py
├─ Dockerfile
├─ app.py
├─ reqquirements.txt

```


## Requirements Explained
1. Flask -> Python REST functionality
2. Flask-Restful -> Simplifies Flask's REST functionality
3. Flask-SQLAlchemy -> Simplifies python SQL functionality 
4. mysql-connector-python -> Connector drivers from python code to an SQL databse
5. Flask-Marshmallow -> serialization that works with Flask-SQLAlchemy  
6. Gunicorn -> Runs the web Listener for a WGSI application

# Acknowledgements 
* [wait-for-it.sh](https://github.com/vishnubob/wait-for-it) -> the script that lets us have the Database container set up first
