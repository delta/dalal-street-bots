#!/bin/sh

echo "################## Building proto ############"
bash build_proto.sh
echo "################# Running bots server ###########"
cd dalalstreetbots
python3 main.py
