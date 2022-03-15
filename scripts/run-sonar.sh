#!/bin/bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -p 9092:9092 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube
# docker rm -f sonarqube