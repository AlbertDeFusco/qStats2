#!/usr/bin/env python
import glob

from qstats.job import Job

def sumSU(jobs):
  suCharged = 0.
  for job in jobs:
    suCharged = suCharged + job.su

  return suCharged

def avgWait(jobs):
  wait=0.
  for job in jobs:
    wait = wait + job.wait

  maxWait=max([job.wait for job in jobs])

  return (wait/len(jobs)),maxWait

def avgNCPU(jobs):
  ncpus=0.
  for job in jobs:
    ncpus = ncpus + job.cpus

  return ncpus/len(jobs)

# Make dictionaries (hastables) based on the 'key'.
# key can be any of the above attributes and must be provided
# as a string, like 'queue', 'user', 'reqwall'
# Stat can be 'JOBEND','JOBSTART','JOBCANCEL' or just ignored.
def collect(myStats,key,stat=None):
  collected = {}
  for job in myStats:
    if stat != None:
      try:
        if job.status == stat:
          value = job.__dict__[key]
          if value in collected:
            collected[value].append(job)
          else:
            collected[value] = [job]
      except:
        pass
    else:
      try:
        value = job.__dict__[key]
        if value in collected:
          collected[value].append(job)
        else:
          collected[value] = [job]
      except:
        pass
  return collected


# Read the event logs
# The input is a list of globular-aware file names with paths, like
# ['stats/events.*Feb*2014','stats/events.*Mar*2014']
# Rename requests that routed queues be renamed to the base routing queue
def getJobs(files,Rename=False):
  theFiles = [glob.glob(thisFile) for thisFile in files]
  #make one list
  theStats = [y for x in theFiles for y in x]
  Stats = list()
  for f in theStats:
    with open(f) as myFile:
      [Stats.append(Job(l.split(),Rename)) for l in (line.strip() for line in myFile) if l]
  return Stats

# each queue has a different charge factor to convert
# from cpu-hours to Service Units
def getSUCharged(queue,runtime,cpus,qos,gpus=0.):
  qosFac=1.0
  if(qos=='low'):
    qosFac=0.25

  if (queue == 'idist' or queue=='ndist' or queue=='distributed'
      or queue=='idist_short'):
    return runtime*cpus*qosFac*1.0
  elif (queue=='ishared' or queue=='nshared' or queue=='shared'):
    return runtime*cpus*qosFac*0.5
  elif (queue=='ishared_large' or queue=='nshared_large' or queue=='shared_large'
      or queue=='idist_big' or queue=='ndist_big' or queue=='dist_big'
      or queue=='idist_small' or queue=='ndist_small' or queue=='dist_small'
      or queue=='idist_fast' or queue=='ndist_fast' or queue=='dist_fast'):
    return runtime*cpus*qosFac*1.5
  elif (queue=='dist_amd' or queue=='shared_amd'):
    return runtime*cpus*qosFac*0.75
  elif (queue=='gpu' or queue=='gpu_short' or queue=='gpu_long'):
    return runtime*qosFac*8.0
  else:
    return 0.0
