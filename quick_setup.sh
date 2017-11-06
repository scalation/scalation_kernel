#!/usr/bin/env bash

VIRTUALENV="virtualenv"

# setup virtualenv if needed
if [ ! -d "$VIRTUALENV" ]; then
    python3 -m virtualenv "$VIRTUALENV"
fi

# activate virtualenv
source bin/activate

# download ScalaTion if needed
if [ ! -d "scalation_1.3" ]; then
    wget http://cobweb.cs.uga.edu/~jam/scalation_1.3.tar.gz
    tar zxf scalation_1.3.tar.gz
fi

# setup environment variables
export SCALATION_MATHSTAT_JAR="$(pwd)/scalation_1.3/scalation_models/lib/scalation_mathstat_2.12-1.3.jar"
export SCALATION_MODELING_JAR="$(pwd)/scalation_1.3/scalation_models/lib/scalation_modeling_2.12-1.3.jar"

# install jupyter and notebook if needed
python3 -m pip install --upgrade pip
python3 -m pip install jupyter
python3 -m pip install -e .
python3 -m scalation_kernel.install

# run jupyter
python3 -m jupyter notebook


