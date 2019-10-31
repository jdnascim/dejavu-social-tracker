#!/bin/bash

# bak the old database
mv mongo_data_dir bak/mongo_$(date +'%Y%m%d')

# bak the old solr
mv solr-cores bak/solr_$(date +'%Y%m%d')

# add new solr-cores
cp -R new-solr-cores/solr-cores solr-cores

# set required ownership
chmod -R 777 solr-cores

# delete old containers
docker stop $(docker ps -qa)

# delete old containers
docker rm $(docker ps -qa)

# create user
./create_user.sh
