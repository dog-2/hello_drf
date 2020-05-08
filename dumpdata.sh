#!/bin/bash 
TARGET_DIR=$1
pushd .
cd $TARGET_DIR
python manage.py dumpdata --exclude auth --exclude contenttypes --exclude=sessions > data.json
popd