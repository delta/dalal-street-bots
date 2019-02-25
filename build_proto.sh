#!/bin/bash

if [ ! -d dalalstreetbots/proto_build ]; then
    mkdir dalalstreetbots/proto_build
fi
rm -rf dalalstreetbots/proto_build/*
python3 -m grpc_tools.protoc -I./proto --python_out=dalalstreetbots/proto_build/ --grpc_python_out=dalalstreetbots/proto_build/ ./proto/*.proto
python3 -m grpc_tools.protoc -I./proto --python_out=dalalstreetbots/proto_build/ ./proto/actions/*.proto
python3 -m grpc_tools.protoc -I./proto --python_out=dalalstreetbots/proto_build/ ./proto/datastreams/*.proto
python3 -m grpc_tools.protoc -I./proto --python_out=dalalstreetbots/proto_build/ ./proto/models/*.proto

egrep -rl "^from (actions|datastreams|models)" dalalstreetbots/proto_build/ | grep ".py" \
    | xargs sed -r -i.bak 's/^from (actions|datastreams|models) import/from proto_build.\1 import/g'

find . -type f -name "*.bak" -exec rm {} \;
