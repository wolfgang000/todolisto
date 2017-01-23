#!/bin/bash
for i in "$@"
do
case $i in
    -t=*|--type=*)
    TYPE="${i#*=}"
    ;;
    *)
            # unknown option
    ;;
esac
done

cp config/gae/app.yaml ./app.yaml
cp config/gae/appengine_config.py ./appengine_config.py
pip install -r config/gae/requirements.txt -t lib/
#cd web_app/frontend/
#echo $TYPE
#npm install

#if [ "$TYPE" = "dev"  ];
#	then 
#		echo 'TRUE';
#		npm run build:dev;
#	else 
#		echo 'FALSE';
#		npm run build:prod;
#fi
#cd ..
#cp -R frontend/dist/* static/
#mv static/index.html templates/index.html
