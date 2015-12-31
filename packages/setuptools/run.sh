#!/bin/bash


if [ -d ./dist ]; 
then 
    rm -rf ./dist
    echo "rm ./dist"
fi

if [ -d MANIFEST];
then 
    rm ./MANIFEST
    echo "rm MANIFEST"
fi

python setup.py sdist

cd ./dist
tar xvf appname-100.tar.gz


cd appname-100
sudo python setup.py install




