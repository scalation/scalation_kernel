# Installation Guide

## Table of Contents

<!-- toc -->

- [General Instructions](#general-instructions)
- [Quick Setup Script](#quick-setup-script)
  * [Quick Setup using Git](#quick-setup-using-git)
  * [Quick Setup without Git](#quick-setup-without-git)
- [Docker Container](#docker-container)
- [Development Version](#development-version)
  * [Install ScalaTion Kernel from GitHub using PIP](#install-scalation-kernel-from-github-using-pip)

<!-- tocstop -->

## General Instructions

Installation requires a recent ScalaTion distribution (>= 1.3) from
[here](http://cobweb.cs.uga.edu/~jam/scalation.html). To install
**Scalation Kernel** from PyPI, you can use the commands:

```
$ python3 -m pip install -U pip
$ python3 -m pip install -U scalation_kernel
$ export SCALATION_MATHSTAT_JAR=/path/to/scalation_mathstat.jar
$ export SCALATION_MODELING_JAR=/path/to/scalation_modeling.jar
$ python3 -m scalation_kernel.install
```

After installing ScalaTion Kernel, you may want to test it out
with Jupyter. To run Jupyter, you might use the following command:

```
$ python3 -m jupyter notebook
```

## Quick Setup Script

**Use Case:** The user wants to rapidly deploy a local Jupyter instance with 
ScalaTion notebook support.

A quick setup script is provided that creates an independent Python 3 virtual 
environment using [`virtualenv`](https://virtualenv.pypa.io/en/stable/) and 
installs everything you need to get started with Jupyter, ScalaTion Kernel,
and ScalaTion 1.3. To inspect this script before you run it, see
[`quick_setup_1.3.sh`](quick_setup_1.3.sh). To download and run the script, you
have two options, outlined below, depending on whether or not you have Git 
installed. These instructions assume you are using one of Linux, MacOS, or 
Windows 10 (with 
[Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/about)).

### Quick Setup using Git

Open your terminal and run the following commands to setup and run everything
from a subdirectory called `scalation_kernel` (created for you):
```
$ git clone https://github.com/scalation/scalation_kernel.git
$ cd scalation_kernel
$ bash quick_setup_1.3.sh
```
The first time the script runs, it may take some time due to downloading
dependencies. Subsequent runs should launch Jupyter rather quickly.

### Quick Setup without Git

If you don't have Git installed, download the 
[`zip`](https://github.com/scalation/scalation_kernel/archive/master.zip) or
[`tar.gz`](https://github.com/scalation/scalation_kernel/archive/master.tar.gz)
file and extract it. By default, the directory should be named 
`scalation_kernel-master`. Open your terminal, change into the extracted
directory, and run the following commands to setup and run everything
from within this directory:
```
$ bash quick_setup_1.3.sh
```
The first time the script runs, it may take some time due to downloading
dependencies. Subsequent runs should launch Jupyter rather quickly.

## Docker Container

A [`Dockerfile`](docker/Dockerfile) is availble to those with [Docker](https://www.docker.com) installed.
Instructions on how to build and run the Docker image using the provided `Dockerfile` can be found [here](docker).

<hr>
The content and opinions expressed on this Web page do not necessarily reflect
the views of nor are they endorsed by the University of Georgia or the
University System of Georgia.

## Development Version

### Install ScalaTion Kernel from GitHub using PIP

The development version of ScalaTion Kernel is hosted [here](https://github.com/scalation/scalation_kernel/) on GitHub.
Installation requires a recent ScalaTion distribution (>= 1.3) from
[here](http://cobweb.cs.uga.edu/~jam/scalation.html). To install
the development version of **Scalation Kernel**, you can use the
following commands commands:

```
$ git clone https://github.com/scalation/scalation_kernel.git
$ python3 -m pip install -U pip
$ python3 -m pip install -e scalation_kernel
$ export SCALATION_MATHSTAT_JAR=/path/to/scalation_mathstat.jar
$ export SCALATION_MODELING_JAR=/path/to/scalation_modeling.jar
$ python3 -m scalation_kernel.install
```

After installing ScalaTion Kernel, you may want to test it out
with Jupyter. To run Jupyter, you might use the following command:

```
$ python3 -m jupyter notebook
```


