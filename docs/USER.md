# User Guide

## Table of Contents

<!-- toc -->

- [Creating a ScalaTion Notebook](#creating-a-scalation-notebook)
- [Using the ScalaTion Big Data Framework](#using-the-scalation-big-data-framework)
- [Basic Plotting](#basic-plotting)
  * [`::plotv`](#plotv)
    + [Arguments](#arguments)
    + [Example](#example)
  * [`::plotm`](#plotm)
    + [Arguments](#arguments-1)
    + [Example](#example-1)
- [Formatters](#formatters)

<!-- tocstop -->

## Creating a ScalaTion Notebook

The *New* menu in Jupyter should show an option to create a ScalaTion
notebook using the installed kernel. 

## Using the ScalaTion Big Data Framework

Coming soon.

## Basic Plotting

Currently, there are two functions which facilitate the plotting of
ScalaTion vectors and matrices. We will discuss them one by one and
understand their use cases.

### `::plotv`

The `::plotv` command plots one or more ScalaTion vectors.

```
::plotv  [--title TITLE] [--xlabel XLABEL] [--ylabel YLABEL] V [V ...]
```

#### Arguments

* `V` - a ScalaTion vector
* `--title TITLE` - plot title
* `--xlabel XLABEL` -  x-axis label
* `--ylabel YLABEL` - y-axis label
* `--bar` - creates a bar graph
* `--xkcd` - draws a graph in the art style of xkcd (Default: Line graph)
* `--scatter` - creates a scatter plot

#### Example

The following example plots a vector representing the function `y = x + e` where
`e` is i.i.d. according to Normal distribution with mean zero and variance
ten:

````
import scalation.linalgebra.VectorD
import scalation.random.Normal
val e = Normal(0, 10)
val v = VectorD((0 until 100).map(_ + e.gen))
::plotv v
````

![PlotV Example](https://imgur.com/bvz2vV9.png)

### `::plotm`

The `::plotm` command plots columns from one or more ScalaTion matrices.


```
::plotm  [--title TITLE] [--xlabel XLABEL] [--ylabel YLABEL] M [M ...]
```

#### Arguments

* `M` - a ScalaTion matrix
* `--title TITLE` - plot title
* `--xlabel XLABEL` -  x-axis label
* `--ylabel YLABEL` - y-axis label

#### Example

The following example plots a matrix where each column represents the function
 `y_j = x + (100 * j) + e` where `e` is i.i.d. according to Normal distribution 
with mean zero and variance one hundred:

````
import scalation.linalgebra.{MatrixD, VectorD}
import scalation.random.Normal
val e = Normal(0, 100)
def y(j: Int)(x: Double) = x + (100 * j) + e.gen
def makeCol(j: Int) = VectorD((0 until 100).map(y(j)(_)))
val m = MatrixD((0 to 3).map(makeCol(_)))
::plotm m
````

![PlotM Example](https://imgur.com/dSPN0t5.png)

## Formatters

Coming soon.

<hr>

Copyright (c) 2017 Michael E. Cotterell and the University of Georgia.
This software is free and open source under an
[MIT License](https://github.com/scalation/scalation_kernel/blob/master/LICENSE.md).
The content and opinions expressed on this Web page do not necessarily
reflect the views of nor are they endorsed by the University of Georgia or
the University System of Georgia.

