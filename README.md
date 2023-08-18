[![Python CI](https://github.com/serVmik/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/serVmik/python-project-83/actions/workflows/pyci.yml)
[![Actions Status](https://github.com/serVmik/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/serVmik/python-project-83/actions)
<a href="https://codeclimate.com/github/serVmik/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/e4d435f6369fc2ca0214/maintainability" />
</a> <a href="https://codeclimate.com/github/serVmik/python-project-83/test_coverage"><img src="https://api.codeclimate.com/v1/badges/e4d435f6369fc2ca0214/test_coverage" /></a>

### Application description:  
[Page Analyzer is a site](https://servmik-python-project-83-5lp0.onrender.com) 
that analyzes websites for 
[SEO](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F_%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)
suitability.  
It application uses the Python library 
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
for parse websites.  
The results of the checks of websites are parsing: 
h1, title, description and code status. 
The application saves it.  

### How to install the app:  
For install and use the application you will need the following applications: 
[git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git),
[poetry](https://python-poetry.org/docs/), 
[postgresql](https://www.postgresql.org/). 
You can install them:  
```
$ sudo apt update
$ sudo apt install git-all  
$ sudo apt install curl
$ curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
```

Clone the application from GitHub and install the necessary
libraries using the 'make install' command.  
All commands starting with '$ make' are executed in the application directory.  
```
$ git clone git@github.com:serVmik/python-project-83.git  
$ cd python-project-83  
$ make install  
```

Install postgresql:  
```
$ sudo apt install postgresql
```

You need create a user:
```
$ sudo -u postgres createuser --createdb {user_name}  
```

You need to set a password for the user_name.  
```
$ sudo -u postgres psql  
postgres=# ALTER ROLE {user_name} PASSWORD '{password}';
postgres=# \q
```

Next, create the 'page_analyzer' database and tables. 
'make schema-db' command will create the tables only in the 'page_analyzer' database:
```
$ sudo -u postgres createdb --owner={user_name} page_analyzer  
$ make schema-db
```

Create '.env' file in the root folder and add the following variables to it.  
Set the secret key.  
Enter password for user_name.
```  
SECRET_KEY={secret_key}  
DATABASE_URL=postgresql://{user_name}:{password}@localhost:5432/page_analyzer  
```  

Run the application local:  
```
$ poetry shell
$ make dev  
```

Go to the browser address http://localhost:5000/  
### How to use the app:  
#### Enter a verified address.
![index_1](https://github.com/serVmik/python-project-83/assets/56305558/1410a83a-fd85-4e4a-beb8-e2f8ee7ab3b3)
#### Run a check.  
![urls_1](https://github.com/serVmik/python-project-83/assets/56305558/e9f7a290-380f-43a7-85ec-ae6b8882b6be)
#### Get results.
![urls_2](https://github.com/serVmik/python-project-83/assets/56305558/39503faf-41fe-4936-91a6-68aafb190ea0)
#### The application saves verified sites.
![urls_3](https://github.com/serVmik/python-project-83/assets/56305558/52a36c71-5c0f-4ead-bb4d-e39735f5671d)
