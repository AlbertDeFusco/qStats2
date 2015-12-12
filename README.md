# qStats
This package provides functionality to make reports from [Moab Workload Trace files](http://docs.adaptivecomputing.com/mwm/archive/6-0/16.3.3workloadtrace.php)

## Usage
This package provides a command line tool called `qstats` that generates usage reports for Moab trace files in a specified directory. The `data` directory has several samples files.

```
usage: qstats [-h] [-y YEAR] [-q] stats_dir

Moab Queue usage report

positional arguments:
  stats_dir             Directory of Moab Event Stats

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR
  -q, --by-queue        Show each queue

```

## Installation

To install using [setuptools](https://pythonhosted.org/setuptools/setuptools.html) in *develop* mode.

```
python setup.py develop --user
```


To build the conda package.

```
conda install conda-build anaconda-client
conda build .
```

The output of conda build will have a path to the zipped build file. It can be installed locally with

```
conda install --use-local /path/to/zip
```

or uploaded to [anaconda.org](anaconda.org) and installed over the web.
