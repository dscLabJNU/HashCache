set -x 
set -e
./gradlew core:java8:distDocker
docker push diomwu/java8action:HashCache