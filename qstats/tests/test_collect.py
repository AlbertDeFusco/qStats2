#!/usr/bin/env python

from qstats import utils

def test_collect():
    theJobs = utils.getJobs(['data/events.Sun_Oct_25_2015'])
    groups = utils.Collect(theJobs,'group','JOBEND')
    assert len(groups.keys()) == 13
