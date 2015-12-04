#!/usr/bin/env python

from qstats.utils import getJobs, collect
import argparse

def cli():
    parser=argparse.ArgumentParser(description='Moab Queue usage report')

    parser.add_argument('stats_dir',help='Directory of Moab Event Stats')
    parser.add_argument('-y','--year',action='store')
    parser.add_argument('-q','--by-queue',action='store_true',help='Show each queue')

    return parser.parse_args()

def main(args=None):

    theJobs = getJobs([args.stats_dir+'/*'+args.year])
    print("%%%%%%%% Report for " + args.year + " %%%%%%%%")
    print()


    print("--- Summary")
    groups = collect(theJobs,'group','JOBEND')
    jobs=[(group,len(groups[group]),sum(groups[group])) for group in groups.keys()]
    jobs.sort(key=lambda tup: tup[2])
    njobs=0
    ncpuh=0
    for job in jobs:
      print("%18s: %7d jobs; %12.2f cpu-hours" % job)
      njobs=njobs+job[1]
      ncpuh=ncpuh+job[2]
    print("--------------------------------------------------------")
    print("%10s  %5d jobs; %10.2f cpu-hours" % ("",njobs,ncpuh))
    print()



    if(args.by_queue):
        queues = collect(theJobs,'queue','JOBEND')
        for queue in sorted(queues.keys()):
          groups = collect(queues[queue],'group')
          print("--- " + queue.upper())

          jobs=[(group,len(groups[group]),sum(groups[group])) for group in groups.keys()]
          jobs.sort(key=lambda tup: tup[2])
          njobs=0
          ncpuh=0
          for job in jobs:
            print("%18s: %7d jobs; %12.2f cpu-hours" % job)
            njobs=njobs+job[1]
            ncpuh=ncpuh+job[2]
          print("--------------------------------------------------------")
          print("%10s  %5d jobs; %10.2f cpu-hours" % ("",njobs,ncpuh))
          print()

if __name__ == '__main__':
    args=cli()
    main(args)
