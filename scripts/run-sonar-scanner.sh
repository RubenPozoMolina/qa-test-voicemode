#!/bin/bash
export pwd=`pwd`
echo $pwd
docker run \
    --rm \
    --network host \
    -e SONAR_HOST_URL="http://localhost:9000" \
    -e SONAR_LOGIN=$sonarToken \
    -v "${pwd}:/usr/src" \
    sonarsource/sonar-scanner-cli