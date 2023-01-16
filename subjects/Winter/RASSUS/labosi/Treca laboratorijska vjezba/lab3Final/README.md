# Install 

run ./build.sh to download all pacakges automatically or go manually inside each folder and install them with InteliJ

# Environment

java 17
docker latest

# Run

- run docker compose commands defined in lab docker-compose -f docker-compose-infrastructure.yml up, docker-compose -f docker-compose-services.yml up

- open in browser localhost:8081, localhost:8082, localhost:8083, localhost:8888/application/default, localhost:8761 (defined in docker files)

# Gitlab

- create repo lab3config (only config in the end matters) with file application.properties which contains temperatura.jedinica=C, 
change in config --> application context with yours git repo 

- when commit to K is executed, create curl http post request to *localhost:8083/actuator/refresh* to apply force reload

