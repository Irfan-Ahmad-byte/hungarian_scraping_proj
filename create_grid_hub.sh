docker network create grid
docker run -d -p 4442-4444:4442-4444 --net grid --name selenium-hub selenium/hub:4.2.2-20220609
