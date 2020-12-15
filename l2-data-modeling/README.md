# Setup in Windows Subsystem for Linux (WSL)

## Install PostgreSQL
```
sudo apt-get -y update
sudo apt-get -y install postgresql
sudo apt-get install postgresql-contrib
```
- Start postgresql
```
sudo service postgresql start
```

- Check postgresql status
```
service postgresql status
```

By default a user called **postgres** is made on and the user **postgres** has full superadmin access to entire PostgreSQL instance running on your OS.

Make sure postgresql service is started.

- Create user `student` :
```
sudo -u postgres createuser student
```

- Create database `studentdb` :
```
sudo -u postgres createdb studentdb
```

- Give the user `student` password `student` :
``` 
sudo -u postgres psql
psql=# alter user student with encrypted password 'student';
```

- Grante user `student` privileges on database `studentdb`
```
psql=# grant all privileges on database studentdb to student;
```

- Grant user `student` the permission to create database
```
psql=# alter user student createdb;
```

## Install `psycopg2`
```
sudo apt install libpq-dev
pip install psycopg2
```

## Setup jupyter notebook
- Install `jupyter`
```
pip install jupyter
```

- Generate config file and config jupyter notebook
```
jupyter notebook --generate-config
vim ~/.jupyter/jupyter_notebook_config.py
```

- Set `jupyter notebook` to no browser by default
  - Go to the line `c.NotebookApp.open_browser = True`
  - uncomment it
  - change to `c.NotebookApp.open_browser = False`

- Change default notebook directory
  - Go to the line contains `c.NotebookApp.notebook_dir`
  - uncomment it
  - change its value `c.NotebookApp.notebook_dir = '/your/defined/path'`

- Set password for jupyter notebook to prevent from demanding token
```
jupyter notebook password
```
```
Enter password:
Verify password:
[NotebookPasswordApp] Wrote hashed password to /your/path/to/jupyter_notebook_config.json
```

## PostgreSQL

- Connect to `psql` command line tool
```
sudo -u postgres psql
```

- List all users
```
postgres=# \du
postgres=# \du+ (more descirption)
```

- List all databases
```
postgres=# \l
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