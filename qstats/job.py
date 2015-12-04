#!/usr/bin/env python
import time

class Job(object):
# the constructor takes two arguemnts
# stats  is a list of job stats as read by getJobs below
# Rename requests that routed queues be renamed to the base routing queue
  def __init__(self,stats,Rename=False):
    try:
      if stats[4] == 'JOBCANCEL':
        raise TypeError
      # epoch times; be careful! I have found cases where
      # they come out as 0
      if (int(stats[14]) == 0) or (int(stats[15]) == 0) or (int(stats[12]) == 0) or (int(stats[55]) == 0):
        raise ValueError
      if (int(stats[14]) < 0) or (int(stats[15]) < 0) or (int(stats[12]) < 0) or (int(stats[55]) < 0):
        raise ValueError

      # The status of this event entry
      self.status=stats[4]

      # user information
      self.user=stats[7]
      self.group=stats[8]
      self.account=stats[28]

      # job information
      self.jobID=stats[3]

      #requested resources
      self.queue=stats[11].replace("[","").replace("]","").replace(":1","")
      if(Rename):
        if(self.queue == 'idist' or self.queue=='ndist'):
            self.queue = 'distributed'
        if(self.queue == 'idist_small' or self.queue == 'ndist_small'):
            self.queue = 'dist_small'
        if(self.queue == 'idist_big' or self.queue == 'ndist_big'):
            self.queue = 'dist_big'
        if(self.queue == 'ishared_large' or self.queue == 'nshared_large'):
            self.queue = 'shared_large'
        if(self.queue == 'ishared' or self.queue == 'nshared'):
            self.queue = 'shared'
        if(self.queue == 'gpu_long' or self.queue == 'gpu_short'):
            self.queue = 'gpu'

      self.memory=stats[37]
      self.partition=stats[33]
      self.features=stats[22].replace("[","").replace("]","")
      self.qos=stats[26].split(":")[0]
      self.qosDelivered=stats[26].split(":")[1]
      self.rsv=stats[43]

      self.nodes=int(stats[5])
      if self.nodes==0:
        self.nodes=1

      self.cpus=int(stats[6])
      self.ppn=self.cpus/self.nodes
      self.reqwall=int(stats[9])/60./60.

      # epoch times; be careful! I have found cases where
      # they come out as 0
      self.start=int(stats[14])
      self.end=int(stats[15])
      self.submit=int(stats[12])
      self.eligible=int(stats[55])

      self.cputime=(self.end - self.start) * self.cpus/60./60.

      self.runtime=self.cputime/self.cpus
      self.queued=self.eligible/60./60.

      self.wait=(self.start - self.submit) /60./60.
      self.blocked=(self.start - self.submit - self.eligible) / 60./60.

      self.blocked = 0

      self.submitTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.submit))
      self.startTime  = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.start))
      self.endTime  = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.end))

      self.submitDate = time.strftime("%Y-%m-%d", time.gmtime(self.submit))
      self.startDate  = time.strftime("%Y-%m-%d", time.gmtime(self.start))
      self.endDate  = time.strftime("%Y-%m-%d", time.gmtime(self.end))

      self.su=getSUCharged(self.queue,self.runtime,self.cpus,self.qos)

    except ValueError:
      pass

    except TypeError:
      pass

    except:
      #there are cases where a line in the event log has no
      # reasonable information or when a value (like an epoch time)
      # is incorrect. I'm just ignoring those lines
      pass


  # When adding two job objects a new job object is returned
  # where newJob.cputime is the sum of the two jobs.
  # All other attributes come from one of the two objects.
  def __add__(self,other):
    try:
      return self.cputime+other.cputime
    except:
      return 0.0
  def __radd__(self,other):
    try:
      return other + self.cputime
    except:
      return self
