#!/usr/bin/env python

from qstats import utils

def test_collect_queue():
    theJobs = utils.getJobs(['data/events.Sun_Oct_25_2015'])
    groups = utils.collect(theJobs,'queue','JOBEND')
    assert len(groups.keys()) == 16

def test_collect_group():
    theJobs = utils.getJobs(['data/events.Fri_Sep_04_2015'])
    groups = utils.collect(theJobs,'group').keys()
    assert len(groups) == 26
