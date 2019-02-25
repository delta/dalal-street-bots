#!/bin/sh

echo "################## Preparing submodule for running  ############"
git submodule init
git submodule update --recursive
echo "################## Building proto ############"
bash build_proto.sh
echo "################# Running bots server ###########"
cd dalalstreetbots
python3 main.py