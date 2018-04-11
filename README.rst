Scalation Kernel
================

Overview
--------

The **Scalation Kernel** project provides a lightweight
`Scala <http://www.scala-lang.org>`__ +
`ScalaTion <http://cobweb.cs.uga.edu/~jam/scalation.html>`__ kernel for
`Jupyter <https://jupyter.readthedocs.io/en/latest/>`__ notebooks. More
information is available on the `project
page <https://github.com/scalation/scalation_kernel>`__.

-  GitHub Project Page: https://github.com/scalation/scalation_kernel/
-  PyPI Release Page: https://pypi.python.org/pypi/scalation-kernel/

Installation
------------

Prerequisites
~~~~~~~~~~~~~

-  Java 8 (>= 8)
-  Scala 2.12 (>= 2.12)

Installation requires a recent ScalaTion distribution (>= 1.3) from
`here <http://cobweb.cs.uga.edu/~jam/scalation.html>`__. Once you have
ScalaTion, make sure the ``SCALATION_JARS`` environment variable is set
appropriately before continuing. This can be done individually, as seen
here:

It is important to note that this is the most important step, if the
environment variable is not correct, the program will not run properly.

Steps (Terminal):
~~~~~~~~~~~~~~~~~

-  Find where you downloaded your copy of ScalaTion.
-  Use ``pwd`` command to get the path location.
-  Copy the path to use in the next steps.

::

    $ export SCALATION_JARS=/path/to/scalation_mathstat.jar
    $ export SCALATION_JARS=/path/to/scalation_modeling.jar:$SCALATION_JARS

It can also be done with a single command if you know the path to the
``scalation_models`` directory:

::

    $ export SCALATION_JARS=$(find /path/to/scalation_models/lib | grep .jar | paste -sd ":" -)

To install **Scalation Kernel** from PyPI, you can use the following
commands:

::

    $ python3 -m pip install -U scalation_kernel
    $ python3 -m scalation_kernel.install

More installation options are presented in the `Installation
Guide <https://github.com/scalation/scalation_kernel/blob/master/docs/INSTALL.md>`__,
including deployment options for Python virtual environments and Docker
containers.

Using ScalaTion Kernel
----------------------

The dropdown menu in Jupyter labeled **New** should show an option to
create a ScalaTion notebook using the installed kernel.

A `User
Guide <https://github.com/scalation/scalation_kernel/blob/master/docs/USER.md>`__
is currently under development. A complete draft is planned for the next
minor release. Until then, please see the collection of `example
notebooks <https://github.com/scalation/scalation_kernel/tree/master/notebooks>`__
for usage examples.

Contributors
------------

-  Michael E. Cotterell mepcott@uga.edu
-  Dat Le-Phan datlephan@uga.edu

License
-------

Copyright (c) 2017 Michael E. Cotterell and the University of Georgia.
This software is free and open source under an `MIT
License <https://github.com/scalation/scalation_kernel/blob/master/LICENSE.md>`__.
The content and opinions expressed on this Web page do not necessarily
reflect the views of nor are they endorsed by the University of Georgia
or the University System of Georgia.
