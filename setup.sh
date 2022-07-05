#! /bin/bash
# work dir : ./

# change personal value
# templates -> base.html
# other -> mysqldb_docker.yml
# other -> extent_bashrc
cd ./data
python3 change_personal_value.py
cd ../
mkdir site
cd site

# setup the schoollunchweb's file
# work dir : ./site
django-admin startproject schoollunchweb
cd schoollunchweb

# work dir : ./site/schoollunchweb
python3 manage.py startapp users_additional_information
python3 manage.py startapp accounts_pages
python3 manage.py startapp foods_and_orders
cd ../../

# copy all the file
# work dir : ./
cat ./data/users_additional_information/models.py > ./site/schoollunchweb/users_additional_information/models.py
cat ./data/users_additional_information/admin.py > ./site/schoollunchweb/users_additional_information/admin.py
mv ./data/templates ./site/schoollunchweb
cat ./data/schoollunchweb/urls.py > ./site/schoollunchweb/schoollunchweb/urls.py
cat ./data/schoollunchweb/settings.py > ./site/schoollunchweb/schoollunchweb/settings.py
cat ./data/schoollunchweb/__init__.py > ./site/schoollunchweb/schoollunchweb/__init__.py
cat ./data/foods_and_orders/admin.py > ./site/schoollunchweb/foods_and_orders/admin.py
cat ./data/foods_and_orders/forms.py > ./site/schoollunchweb/foods_and_orders/forms.py
cat ./data/foods_and_orders/models.py > ./site/schoollunchweb/foods_and_orders/models.py
cat ./data/foods_and_orders/urls.py > ./site/schoollunchweb/foods_and_orders/urls.py
cat ./data/foods_and_orders/views.py > ./site/schoollunchweb/foods_and_orders/views.py
mv ./data/foods_and_orders/admin_pages > ./site/schoollunchweb/foods_and_orders/
mv ./data/foods_and_orders/food_pages > ./site/schoollunchweb/foods_and_orders/
mv ./data/foods_and_orders/manager_pages > ./site/schoollunchweb/foods_and_orders/
mv ./data/foods_and_orders/order_pages > ./site/schoollunchweb/foods_and_orders/
mv ./data/foods_and_orders/state_pages > ./site/schoollunchweb/foods_and_orders/
cat ./data/accounts_pages/admin.py > ./site/schoollunchweb/accounts_pages/admin.py
cat ./data/accounts_pages/forms.py > ./site/schoollunchweb/accounts_pages/forms.py
cat ./data/accounts_pages/models.py > ./site/schoollunchweb/accounts_pages/models.py
cat ./data/accounts_pages/urls.py > ./site/schoollunchweb/accounts_pages/urls.py
cat ./data/accounts_pages/views.py > ./site/schoollunchweb/accounts_pages/views.py
mv ./data/accounts_pages/users_pages ./site/schoollunchweb/accounts_pages
mv ./data/uwsgi.ini ./site/schoollunchweb
cat ./data/other/extent_bashrc >> ~/.bashrc
source ~/.bashrc
rm ./data/other/extent_bashrc
mv ./data/other/* ./site
cd ./site

# start the mysql in docker
# work dir : ./site
docker pull mysql
docker-compose -f mysqldb_docker.yml up -d
sleep 70

# set django up and run the uwsgi
# work dir : ./site
python3 ./schoollunchweb/manage.py makemigrations
python3 ./schoollunchweb/manage.py migrate
python3 ./schoollunchweb/manage.py createsuperuser
python3 ./schoollunchweb/manage.py shell < ./schoollunchweb_init.py
python3 ./schoollunchweb/manage.py migrate
cd schoollunchweb
uwsgi -d --ini uwsgi.ini
cd ..
python3 timejob.py &