# scalation_kernel

This project provides a Scala+ScalaTion kernel for Jupyter. It uses the system
or container's Scala installation.

## TODO

* Add ScalaTion to class path.

## Python Dependencies

Below are the Python packages that this project directly depends on:

* pexpect (>=4.2.1)
* ipykernel (>=4.6.1)

## Installation

To install the developer version of ```scalation_kernel``` using PIP:
```
$ git clone https://github.com/scalation/scalation_kernel.git
$ python3 -m pip install -e scalation_kernel
$ python3 -m scalation_kernel.install
```

## Run Jupyter

To run Jupyter, you might use the following command:
```
$ python3 -m jupyter notebook
```

## Using the ScalaTion kernel

**Notebook**: The *New* menu in the notebook should show an option for a
ScalaTion notebook.

