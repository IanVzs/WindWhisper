if [ ! -d "/home/$USER/env" ]; then
    echo "mkdir ~/env"
    mkdir ~/env
fi
if [ ! -d "/home/$USER/env/web" ]; then
    echo "virtualenv ~/env/web"
    virtualenv ~/env/web
fi

source /home/$USER/env/web/bin/activate
