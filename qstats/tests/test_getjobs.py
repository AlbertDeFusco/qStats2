#!/usr/bin/env python

from qstats import utils

def test_getjobs():
    theJobs = utils.getJobs(['data/events.Sun_Oct_25_2015'])
    assert len(theJobs) == 2123
