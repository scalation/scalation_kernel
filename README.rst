ScalaTion Kernel
================

| Copyright (c) 2017 Michael E. Cotterell and the University of Georgia
| https://github.com/scalation/scalation_kernel

.. image:: https://i.imgur.com/BlgAPsq.png

Overview
--------
The **Scalation Kernel** project provides a lightweight
`Scala <http://www.scala-lang.org>`_ +
`ScalaTion <http://cobweb.cs.uga.edu/~jam/scalation.html>`_ kernel for
Jupyter notebooks. 
More information is available on the `project page <https://github.com/scalation/scalation_kernel>`_.

Installation
------------
Installation requires a recent ScalaTion distribution (>= 1.3) from
`here <http://cobweb.cs.uga.edu/~jam/scalation.html>`_. To install
**``scalation_kernel``** from PyPI, you can use the commands::

    $ python3 -m pip install -U scalation_kernel
    $ export SCALATION_MATHSTAT_JAR=/path/to/scalation_mathstat.jar
    $ export SCALATION_MODELING_JAR=/path/to/scalation_modeling.jar
    $ python3 -m scalation_kernel.install

Using ScalaTion Kernel
----------------------
The *New* menu in Jupyter should show an option to create a ScalaTion
notebook using the installed kernel. 

A user guide is planned for the next minor release. Until then, see
the `example notebooks <https://github.com/scalation/scalation_kernel/tree/master/notebooks>`_
for usage examples.

License
-------

Copyright (c) 2017 - Michael E. Cotterell and the University of Georgia

All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The content and opinions expressed on this Web page do not necessarily reflect
the views of nor are they endorsed by the University of Georgia or the
University System of Georgia.

