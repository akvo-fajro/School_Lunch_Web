# School Lunch Web

## environment
`ubuntu 20.04 LTS` : use `/bin/bash` as default terminal  
`python 3.8.10` : this is install by default on ubuntu 20.04  

## install related package
```bash
# install all the package
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip
sudo pip3 install --upgrade pip
sudo pip3 install django
sudo pip3 install cryptography
sudo pip3 install PyMySQL
sudo pip3 install uwsgi
sudo pip3 install schedule

# install docker and docker compose
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo groupadd docker
sudo usermod -aG docker $USER

# install nginx
sudo apt install nginx -y
```

## setup django , mysql and uwsgi
```bash
git clone https://github.com/akvo-fajro/School_Lunch_Web.git
mv School_Lunch_Web site
cd site
chmod u+x setup.sh
./setup.sh
```

## setup nginx
> change /etc/nginx/nginx.conf
> comment out the conf.d/*.conf
```
...
# include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
...
```
`$ cd /etc/nginx/sites-available`  
`$ sudo vim deploy-at-root-proxy-pass.conf`  
```
server {
    listen 80;
    server_name _;
    charset utf-8;
    client_max_body_size 75M;
    location / {
        proxy_pass http://127.0.0.1:8003/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
    }
    location /static/ {
        alias {your_static_dir_path};
    }
}
```
`$ ln -s /etc/nginx/sites-available/deploy-at-root-proxy-pass.conf /etc/nginx/sites-enabled/`  
`$ sudo rm /etc/nginx/sites-enabled/default`  
> try `nginx -t` to check if everything is right
`$ sudo systemctl restart nginx`  

