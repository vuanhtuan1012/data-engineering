# Data Modeling

- [x] [Project: Data Modeling with Postgres](https://github.com/vuanhtuan1012/data-modeling-with-postgres)
- [x] [Project: Data Modeling with Cassandra](https://github.com/vuanhtuan1012/data-modeling-with-cassandra)

## Lessons Summarization

:point_right: [Relational Data Models](L2_Relational%20Data%20Models.md)

:point_right: NoSQL Data Models

## Setup in Windows Subsystem for Linux (WSL)

:point_right: [Jupyter notebook](#jupyter-notebook)

:point_right: [PostgreSQL](#postgresql)

:point_right: [Cassandra](#cassandra)

### Jupyter notebook

This part mentions:
- [x] install Jupyter notebook
- [x] configure notebook to no browser when it starts
- [x] change default notebook directory
- [x] prevent notebook from demanding token
- [x] start notebook without ouput in command line
- [x] stop notebook

1. Install `jupyter`
```
pip install jupyter
```

2. Configure Jupyter notebook
```
# generate jupyter notebook config file
jupyter notebook --generate-config

# edit jupyter notebook config file
vim ~/.jupyter/jupyter_notebook_config.py
```

- Set notebook to no browser by default
  - Go to the line `c.NotebookApp.open_browser = True`
  - uncomment it
  - change to `c.NotebookApp.open_browser = False`

- Change default notebook directory
  - Go to the line contains `c.NotebookApp.notebook_dir`
  - uncomment it
  - change its value `c.NotebookApp.notebook_dir = '/your/defined/path'`

3. Prevent from demanding token
Set password to Jupyter notebook will prevent it from demanding token.
```
jupyter notebook password
```

```
Enter password:
Verify password:
[NotebookPasswordApp] Wrote hashed password to /your/path/to/jupyter_notebook_config.json
```

4. Start notebook without output
```
nohup jupyter notebook > ~/jupyter_notebook.log &
```

5. Stop notebook
```
ps -ef | grep jupyter
kill -9 [jupyter-notebook pid]
```

### PostgreSQL

This part mentions:
- [x] install PostgreSQL
- [x] start PostgreSQL service
- [x] check PostgreSQL status
- [x] commandlines interacting with PostgreSQL: create user, set user password, create database, grant an user privileges on a database
- [x] install Python library to interact with PostgreSQL
- [x] PostgreSQL command line tool: connect, list all users, list all databases, list all tables in a database, list all columns in a table.
- [x] common errors

1. Install PostgreSQL
```
sudo apt-get -y update
sudo apt-get -y install postgresql
sudo apt-get install postgresql-contrib
```
:warning: A user called `postgres` is made on and this user has full superadmin access to entire PostgreSQL instance running on your OS.

2. Start PostgreSQL service
```
sudo service postgresql start
```

3. Check PostgreSQL status
```
service postgresql status
```

4. Commandlines interacting with PostgreSQL

- Create user `student`
```
sudo -u postgres createuser student
```

- Give the user `student` password `student`
```
sudo -u postgres psql
psql=# alter user student with encrypted password 'student';
```

- Create database `studentdb`
```
sudo -u postgres createdb studentdb
```

- Grant user `student` privileges on database `studentdb`
```
psql=# grant all privileges on database studentdb to student;
```

- Grant user `student` the permission to create database
```
psql=# alter user student createdb;
```

5. Install Python library `psycopg2`
```
sudo apt install libpq-dev
pip install psycopg2
```

6. PostgreSQL command line tool

- Connect to `psql` command line tool
```
sudo -u postgres psql
```

- List all users
```
postgres=# \du

# with more description on users
postgres=# \du+
```

- List all databases
```
postgres=# \l

# with more description on databases
postgres=# \l+
```

- Connect to a database
```
postgres=# \c [db name]
```

- List all tables in a database
```
yourdb=# \dt
```

- List all columns of table
 ```
yourdb=# \d [table name]
```

7. Common errors
- PostgreSQL warning when create db in jupyter notebook
```
WARNING: could not flush dirty data: Function not implemented
```

Add the following codes at the end of `/etc/postgresql/11/main/postgresql.conf`.

```
fsync = off
data_sync_retry = true
```

then restart postgresql service

```
sudo service postgresql restart
```
- Extension owner error
```
ERROR: must be owner of extension plpgsql
```

Run this command line
```
alter role [username] with superuser;
```


### Cassandra

This part mentions:
- [x] install Cassandra
- [x] start Cassandra service
- [x] check Cassandra status
- [x] commandline connect to the database
- [x] install Python library to interact with Cassandra

1. Install Cassandra

Cassandra requires Java installed on your machine, either the [Oracle Java Standard Edition 8](http://www.oracle.com/technetwork/java/javase/downloads/index.html) or [OpenJDK 8](http://openjdk.java.net/). On Ubuntu, we will use [OpenJDK 8](http://openjdk.java.net/).

```
# verify Java version
java --version

# install OpenJDK, if you don't have it
sudo apt install default-jre

# re-verify
java --version
```

```
# Add the Apache repository of Cassandra to the file cassandra.sources.list
echo "deb http://downloads.apache.org/cassandra/debian 40x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list

# Add the Apache Cassandra repository keys to the list of trusted keys on the server
curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -

# Update the package index from sources
sudo apt-get update

# Install Cassandra with APT
sudo apt-get install cassandra
```
:warning: A new Linux user `cassandra` will get created as part of the installation. The Cassandra service will also be run as this user.

2. Start Cassandra service
```
sudo service cassandra start
```

3. Check Cassandra status
```
service cassandra status
# or
nodetool status
```

4. Connect to the database
```
cqlsh
```

5. Install Python library  to interact with Cassandra
```
pip install cassandra-driver
```