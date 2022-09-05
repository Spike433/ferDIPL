#!/bin/bash

cd microservices
directories=(aggregator-microservice config-server-microservice eureka-server humidity-microservice temperature-microservice)
for dir in "${directories[@]}"
do
	(cd $dir && gradle clean && rm -rf .gradle/)
done

