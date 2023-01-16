#!/bin/bash

for dir in */; do
  if [ -f "$dir/gradlew" ]; then
    cd "$dir"
    ./gradlew clean
    rm -rf .gradle
    cd ..
  fi
done