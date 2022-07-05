import re

# change base.html
file = open('./templates/base.html','r').read()
file = re.sub(r'{class_number}',input('your class number > '),file)
open('./templates/base.html','w').write(file)

mysql_root_passwd = input('your mysql root password > ')
your_database_name = input('your database name > ')
your_database_user = input('your database user > ')
your_database_password = input('your database password > ')


# change mysqldb_docker.yml
file = open('./other/mysqldb_docker.yml','r').read()
file = re.sub(r'{your_mysql_root_passwd}',mysql_root_passwd,file)
file = re.sub(r'{your_database_name}',your_database_name,file)
file = re.sub(r'{your_database_user}',your_database_user,file)
file = re.sub(r'{your_database_password}',your_database_password,file)
open('./other/mysqldb_docker.yml','w').write(file)

# change extent_bashrc
file = open('./other/extent_bashrc','r').read()
file = re.sub(r'{your_django_secret_key}',mysql_root_passwd,file)
file = re.sub(r'{your_database_name}',your_database_name,file)
file = re.sub(r'{your_database_user}',your_database_user,file)
file = re.sub(r'{your_database_password}',your_database_password,file)
open('./other/extent_bashrc','w').write(file)

