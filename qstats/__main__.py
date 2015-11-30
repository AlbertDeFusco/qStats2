#!/usr/bin/env python

from qstats.utils import getJobs, Collect
import sys

def main(args=None):

    if args is None:
        stats_dir = sys.argv[1]
        year=sys.argv[2]

    theJobs = getJobs([stats_dir+'/*'+year])
    print "%%%%%%%% Report for " + year + " %%%%%%%%"
    print


    print "--- Summary"
    groups = Collect(theJobs,'group','JOBEND')
    jobs=[(group,len(groups[group]),sum(groups[group])) for group in groups.keys()]
    jobs.sort(key=lambda tup: tup[2])
    njobs=0
    ncpuh=0
    for job in jobs:
      print "%18s: %7d jobs; %12.2f cpu-hours" % job
      njobs=njobs+job[1]
      ncpuh=ncpuh+job[2]
    print "--------------------------------------------------------"
    print "%10s  %5d jobs; %10.2f cpu-hours" % ("",njobs,ncpuh)
    print



    queues = Collect(theJobs,'queue','JOBEND')
    for queue in sorted(queues.keys()):
      groups = Collect(queues[queue],'group')
      print "--- " + queue.upper()

      jobs=[(group,len(groups[group]),sum(groups[group])) for group in groups.keys()]
      jobs.sort(key=lambda tup: tup[2])
      njobs=0
      ncpuh=0
      for job in jobs:
        print "%18s: %7d jobs; %12.2f cpu-hours" % job
        njobs=njobs+job[1]
        ncpuh=ncpuh+job[2]
      print "--------------------------------------------------------"
      print "%10s  %5d jobs; %10.2f cpu-hours" % ("",njobs,ncpuh)
      print

if __name__ == '__main__':
    main()
