#!/bin/sh
# run with sudo
rm -f ./bin/*.jar
rm -rf $(find ./core -name build)
./gradlew :core:standalone:build
java -jar ./bin/openwhisk-standalone.jar -c ./bin/application.conf