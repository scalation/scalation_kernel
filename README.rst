Scalation Kernel
================

Overview
--------

The **Scalation Kernel** project provides a lightweight
`Scala <http://www.scala-lang.org>`__
`ScalaTion <http://cobweb.cs.uga.edu/~jam/scalation.html>`__ kernel for
Jupyter notebooks. More information is available on the `project
page <https://github.com/scalation/scalation_kernel>`__.

Installation
------------

Installation requires a recent ScalaTion distribution (>= 1.3) from
`here <http://cobweb.cs.uga.edu/~jam/scalation.html>`__. To install
**Scalation Kernel** from PyPI, you can use the commands:

::

    $ python3 -m pip install -U scalation_kernel
    $ export SCALATION_MATHSTAT_JAR=/path/to/scalation_mathstat.jar
    $ export SCALATION_MODELING_JAR=/path/to/scalation_modeling.jar
    $ python3 -m scalation_kernel.install

More installation options are presented in the `Installation
Guide <https://github.com/scalation/scalation_kernel/blob/master/INSTALL.md>`__,
including deployment options for Python virtual environments and Docker
containers.

Using ScalaTion Kernel
----------------------

The *New* menu in Jupyter should show an option to create a ScalaTion
notebook using the installed kernel.

A `User
Guide <https://github.com/scalation/scalation_kernel/blob/master/USER.md>`__
is planned for the next minor release. Until then, see `example
notebooks <https://github.com/scalation/scalation_kernel/tree/master/notebooks>`__
for usage examples.

License
-------

This software is free and open source under an `MIT
License <https://github.com/scalation/scalation_kernel/blob/master/LICENSE>`__.
The content and opinions expressed on this Web page do not necessarily
reflect the views of nor are they endorsed by the University of Georgia
or the University System of Georgia.
