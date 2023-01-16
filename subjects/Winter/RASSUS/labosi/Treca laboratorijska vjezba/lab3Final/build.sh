#!/bin/bash

for dir in */; do
  if [ -f "$dir/gradlew" ]; then
    cd "$dir"
    ./gradlew bootBuildImage
    cd ..
  fi
done