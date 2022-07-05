#! /bin/bash
# work dir : ./

rm ./data/other/extent_bashrc
mv ./data/other/* ./site
cd ./site/schoollunchweb
python3 manage.py collectstatic
cd ../

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
cd ..

# remove the non-using data and print the static path
# work dir : ./
sudo rm -r ./data
echo "*********************************"
echo "the /static/ path is : "`pwd`"/site/schoollunchweb/static/"
echo "*********************************"
