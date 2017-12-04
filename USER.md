# User Guide

## Table of Contents

<!-- toc -->

- [Creating a ScalaTion Notebook](#creating-a-scalation-notebook)
- [Using the ScalaTion Big Data Framework](#using-the-scalation-big-data-framework)
- [Basic Plotting](#basic-plotting)
  * [`::plotv`](#plotv)
  * [`::plotm`](#plotm)
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
* `V` - a ScalaTion vector
* `--title TITLE` - plot title
* `--xlabel XLABEL` -  x-axis label
* `--ylabel YLABEL` - y-axis label

### `::plotm`

The `::plotm` command plots columns from one or more ScalaTion matrices.

```
::plotm  [--title TITLE] [--xlabel XLABEL] [--ylabel YLABEL] M [M ...]
```
* `M` - a ScalaTion matrix
* `--title TITLE` - plot title
* `--xlabel XLABEL` -  x-axis label
* `--ylabel YLABEL` - y-axis label

## Formatters

Coming soon.

<hr>

Copyright (c) 2017 Michael E. Cotterell and the University of Georgia.
This software is free and open source under an
[MIT License](https://github.com/scalation/scalation_kernel/blob/master/LICENSE.md).
The content and opinions expressed on this Web page do not necessarily
reflect the views of nor are they endorsed by the University of Georgia or
the University System of Georgia.

