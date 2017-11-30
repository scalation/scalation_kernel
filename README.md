# scalation_kernel

This project provides a [Scala+ScalaTion](http://cobweb.cs.uga.edu/~jam/scalation.html)
kernel for [Jupyter](http://jupyter.org). It uses the system's or container's
Scala installation for the underlying REPL. This implementation uses
```ipykernel``` and ```pexpect``` to allow the kernel to easily interact with
the REPL. 

![Screenshot](https://i.imgur.com/BlgAPsq.png)

## Quick Setup

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

## General Installation Instructions

### Dependencies

If you are not using the quick setup script, then make sure the following
dependencies are satisfied before continuing (reccommended versions are
given in parentheses):
* Java >= 8 (1.8.0_152; 9.0.1)
* Scala >= 2.12.4 (2.12.4)
* Python >= 3.6.3 (3.6.3)
  * `jupyter` >= 1.0.0
  * `jupyter-client` >= 5.1.0
  * `jupyter-console` >=5.2.0
  * `jupyter-core` >= 4.4.0

### Install ScalaTion Kernel from PyPI using PIP

A relatively stable version of ScalaTion Kernel is hosted [here](https://pypi.python.org/pypi?:action=display&name=scalation-kernel) on PyPI.
If you already have a Jupyter installation and the required prerequisites,
then run the following commands to install the PyPI version of 
ScalaTion Kernel using PIP: 

```
$ python3 -m pip install scalation_kernel
$ python3 -m scalation_kernel.install
```

### Install ScalaTion Kernel from GitHub using PIP

The development version of ScalaTion Kernel is hosted [here](https://github.com/scalation/scalation_kernel/) on GitHub. 
If you already have a Jupyter installation and the required prerequisites,
then run the following commands to install the developer version of 
ScalaTion Kernel using PIP:

```
$ git clone https://github.com/scalation/scalation_kernel.git
$ python3 -m pip install -e scalation_kernel
$ python3 -m scalation_kernel.install
```

### Run Jupyter with ScalaTion Kernel

Before you run Jupyter, you need to make sure the following environment
variables are set with the full paths to the ScalaTion JAR files:
```
$ export SCALATION_MATHSTAT_JAR=/path/to/scalation_mathstat_2.12-1.3.jar
$ export SCALATION_MODELING_JAR=/path/to/scalation_modeling_2.12-1.3.jar
```

To run Jupyter, you might use the following command:
```
$ python3 -m jupyter notebook
```

## Using the ScalaTion kernel

**Notebook**: The *New* menu in the notebook should show an option for a
"ScalaTion" notebook.

