#!/bin/bash
git pull
cd build
docker-compose build sprout
docker-compose up -d
docker restart sprout