#!/bin/bash
PWD=`pwd`
echo $PWD

cd $PWD && \
rm -rf ./docker/db/data/* && \
rm db/migrations/versions/*