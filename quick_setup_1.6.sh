#!/usr/bin/env bash

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ScalaTion Kernel Quick Setup Script for ScalaTion 1.6
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# @author  Michael Cotterell
# @version 1.1.x
# @see     LICENSE.md (MIT style license file).
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# usage: bash quick_setup_1.6.sh venv-dir [--pypi]
#
# arguments:
#   venve-dir  directory to use for virtual environment (create if needed)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# This script uses the Python 3 virtual environment in `venv-dir` to start
# Jupyter with support for the ScalaTion 1.6 big data framework. It quickly
# sets up Jupyter, ScalaTion, and ScalaTion Kernel so that users can rapidly
# get started with ScalaTion in Jupyter notebooks.  
#
# ## Initial Run
# The first time the script is run, it may need to create some directories and
# download some dependencies. For example, if `venv-dir` does not exist, then
# the script attempts to create it using Python's `venv` module. Additional
# dependencies that are downloaded by this script are saved and or installed 
# into the virtual environment provided by `venv-dir` and do not alter the 
# script's initial Python environment. This script downloads the latest 
# ScalaTion 1.6 distribution and adds paths to its JAR files to the 
# `SCALATION_JARS` environment variable. Lastly, the script starts Jupyter
# with support for the ScalaTion 1.6 big data framework.
#
# ## Subsequent Runs
# If `venv-dir` already exists and contains the needed dependencies, then this
# script simply starts Jupyter with support for the ScalaTion 1.6 big data
# framework.
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# @see http://jupyter.readthedocs.io/en/latest/
# @see http://cobweb.cs.uga.edu/~jam/scalation.html
# @see https://github.com/scalation/scalation_kernel
# @see https://docs.python.org/3/library/venv.html
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# NO USER MODIFICATIONS NEEDED AFTER THIS POINT;
# However, we encourage interested users to inspect the script to see what it
# is doing.

function display_title {
    echo "ScalaTion Kernel Quick Setup Script"
}

function display_usage {
    display_title
    echo "usage: $0 venv-dir [--pypi]"
    echo "See script contents for more information."
}

function download_dep {
    DEP_ID=$1    # short name / id
    DEP_NAME=$2  # descriptive name
    DEP_TAR=$3   # url for tar.gz file
    DEP_DIR=$4   # directory
    DEP_TMP="${DEP_ID}.tar.gz"
    echo "Downloading ${DEP_NAME}..."
    wget "${DEP_TAR}" --progress=bar -O "${DEP_TMP}"
    mkdir -p "${DEP_DIR}"
    tar zxf "${DEP_TMP}" -C "${DEP_DIR}" --strip-components=1
    rm -rf "${DEP_TMP}"
}

function check_scalation {
    DEP_ID="scalation"
    DEP_NAME="ScalaTion 1.6"
    DEP_TAR="http://cobweb.cs.uga.edu/~jam/scalation_${SCALATION_VER}.tar.gz"
    DEP_DIR="${DEP_ID}"
    echo "Checking for ${DEP_NAME}..."
    [[ ! -d "${DEP_DIR}" ]] && download_dep "$DEP_ID" "$DEP_NAME" "$DEP_TAR" "$DEP_DIR"
}

function check_deps_quick {

    echo "Checking for Python (need >= 3.3) ..."
    ! [[ -x `command -v python3` ]] && echo "Not found! Cannot continue." && exit 1
    echo $(which python3)
    echo $(python3 --version)

    echo "Checking for Java (need >= 8) ..."
    ! [[ -x `command -v java` ]] && echo "Not found! Cannot continue." && exit 1
    echo $(which java)
    echo $(java -version)

    echo "Checking for Scala (need >= 2.12.8) ..."
    ! [[ -x `command -v scala` ]] && echo "Not found! Cannot continue." && exit 1
    echo $(which scala)
    echo $(scala -version)

#    echo "Checking for SBT ..."
#    ! [[ -x `command -v sbt` ]] && echo "Not found! Cannot continue." && exit 1
#    echo $(which sbt)

    read -p "Are you sure you want to continue? [y/n] " -n 1 -r
    echo    # (optional) move to a new line
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
	[[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
    fi
    
}

# display usage?
[[ ($# -ne 1) || ($# == "--help") || ($# == "-h") ]] && display_usage && exit 1

check_deps_quick

SCALATION_VER="1.6"
SCALATION_TAR="http://cobweb.cs.uga.edu/~jam/scalation_${SCALATION_VER}.tar.gz"
SCALATION_DIR="scalation"
VIRTUALENV="$1"

# setup virtualenv if needed
if [ ! -d "$VIRTUALENV" ]; then
    echo "Creating a Python 3 virtual environment in ${VIRTUALENV}..."
    python3 -m venv "$VIRTUALENV"
fi

# activate virtualenv
echo "Activating the Python 3 virtual environment in ${VIRTUALENV}..."
cd "${VIRTUALENV}"
source "bin/activate"

check_scalation

# setup environment variables
export SCALATION_JARS=$(find scalation*/lib | grep .jar | paste -sd ":" -)

# install python packages if needed
python3 -m pip install --upgrade pip

# install kernel
python3 -m pip install -e ..
python3 -m scalation_kernel.install

# run jupyter
python3 -m jupyter notebook

