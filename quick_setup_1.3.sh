#!/usr/bin/env bash

VIRTUALENV="virtualenv"

# setup virtualenv if needed
if [ ! -d "$VIRTUALENV" ]; then
    python3 -m virtualenv "$VIRTUALENV"
fi

# activate virtualenv
source "$VIRTUALENV/bin/activate"

# download ScalaTion if needed
if [ ! -d "scalation_1.3" ]; then
    wget http://cobweb.cs.uga.edu/~jam/scalation_1.3.tar.gz
    tar zxf scalation_1.3.tar.gz
fi

# setup environment variables
export SCALATION_JARS=$(find scalation*/scalation_models/lib | grep .jar | paste -sd ":" -)

# install python packages if needed
python3 -m pip install --upgrade pip
python3 -m pip install jupyter

# install kernel
python3 -m pip install -e .
python3 -m scalation_kernel.install

# run jupyter
python3 -m jupyter notebook

