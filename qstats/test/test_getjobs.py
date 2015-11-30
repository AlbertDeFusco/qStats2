#!/usr/bin/env python

from qstats import utils

theJobs = utils.getJobs(['data/events.Sun_Oct_25_2015'])

groups = utils.Collect(theJobs,'group','JOBEND')
print groups.keys()
