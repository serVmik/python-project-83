[![Python CI](https://github.com/serVmik/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/serVmik/python-project-83/actions/workflows/pyci.yml)
[![Actions Status](https://github.com/serVmik/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/serVmik/python-project-83/actions)
<a href="https://codeclimate.com/github/serVmik/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/e4d435f6369fc2ca0214/maintainability" />
</a> <a href="https://codeclimate.com/github/serVmik/python-project-83/test_coverage"><img src="https://api.codeclimate.com/v1/badges/e4d435f6369fc2ca0214/test_coverage" /></a>

**Application description:**  
[Page Analyzer is a site](https://python-project-83-production-f22f.up.railway.app)
that analyzes websites for 
[SEO](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F_%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)
suitability.  
It application uses the Python library 
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
for parse websites.  
The results of the checks of websites are parsing: 
h1, title, description and code status. 
The application saves it.  

**How to start using the app:**  
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

Next, create the 'page_analyzer' database and tables. 
'make schema-db' command will create the tables only in the 'page_analyzer' database:
```
$ sudo -u postgres createdb --owner=postgres page_analyzer  
$ make schema-db
```
You may change database in file 'Makefile'.  

You need to set a password for the user, for example for the 'postgres' ROLE.  
```
$ sudo -u postgres psql  
postgres=# ALTER ROLE postgres PASSWORD 'password';
```
Create '.env' file in the root folder and add the following variables to it.  
Set the secret key.  
Enter user password.
```  
SECRET_KEY={secret_key}  
DATABASE_URL=postgresql://postgres:{password}@localhost:5432/page_analyzer  
```  
Run the application local:  
```
$ make dev  
```
Go to the browser address http://localhost:5000/  
Enter a verified address.

![index_1](https://github.com/serVmik/python-project-83/assets/56305558/3c4c0cfd-4e86-428a-bc2d-8421e6b2187a)
Run a check.  
![urls_1](https://github.com/serVmik/python-project-83/assets/56305558/e7d5c494-a2ea-4c8c-a7c7-2ebc9dc6f0b4)
Get results.
![urls_2](https://github.com/serVmik/python-project-83/assets/56305558/853397fc-68e7-4c74-90cd-04ba46b5d056)
The application saves the added sites.
![urls_3](https://github.com/serVmik/python-project-83/assets/56305558/f8907e89-7abc-4ce9-ac1f-fe5a2cc7fac6)
