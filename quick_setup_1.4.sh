#!/usr/bin/env bash

function display_title {
    echo "ScalaTion Kernel Quick Setup Script"
}

function display_usage {
    display_title
    echo "Usage: $0 venv-dir"
}

function download_dep {
    DEP_ID=$1    # short name / id
    DEP_NAME=$2  # descriptive name
    DEP_TAR=$3   # url for tar.gz file
    DEP_DIR=$4   # directory
    DEP_TMP="${DEP_ID}.tar.gz"
    echo "Downloading ${DEP_NAME}..."
    wget "${DEP_TAR}" -q --show-progress -O "${DEP_TMP}"
    mkdir -p "${DEP_DIR}"
    tar zxf "${DEP_TMP}" -C "${DEP_DIR}" --strip-components=1
    rm -rf "${DEP_TMP}"
}

function check_scalation {
    DEP_ID="scalation"
    DEP_NAME="ScalaTion 1.4"
    DEP_TAR="http://cobweb.cs.uga.edu/~jam/scalation_${SCALATION_VER}.tar.gz"
    DEP_DIR="${DEP_ID}"
    echo "Checking for ${DEP_NAME}..."
    [[ ! -d "${DEP_DIR}" ]] && download_dep "$DEP_ID" "$DEP_NAME" "$DEP_TAR" "$DEP_DIR"
}

function check_deps_quick {

    echo "Checking for Java (need >= 8) ..."
    ! [[ -x `command -v java` ]] && echo "Not found! Cannot continue." && exit 1
    echo $(which java)
    echo $(java -version)

    echo "Checking for Scala (need >= 2.12.3) ..."
    ! [[ -x `command -v scala` ]] && echo "Not found! Cannot continue." && exit 1
    echo $(which scala)
    echo $(scala -version)

    echo "Checking for SBT ..."
    ! [[ -x `command -v sbt` ]] && echo "Not found! Cannot continue." && exit 1
    echo $(which sbt)

    read -p "Are you sure you want to continue? [y/n]" -n 1 -r
    echo    # (optional) move to a new line
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
	[[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
    fi
    
}

# display usage?
[[ ($# -ne 1) || ($# == "--help") || ($# == "-h") ]] && display_usage && exit 1

SCALATION_VER="1.4"
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

check_deps_quick
check_scalation

# setup environment variables
export SCALATION_JARS=$(find scalation*/scalation_models/lib | grep .jar | paste -sd ":" -)

# install python packages if needed
python3 -m pip install --upgrade pip

# install kernel
python3 -m pip install -e ..
python3 -m scalation_kernel.install

# run jupyter
python3 -m jupyter notebook

