#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
# 
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import argparse
import sys

parser = argparse.ArgumentParser(description='\033[1mJenkins monitoring plugin\033[0m')
parser.add_argument('--jobname', action="store", 
                    help='Job name по которому ищем статус')
parser.add_argument('-H','--hostname', action="store", required=True,
                    help='Hostname jenkins сервера')
parser.add_argument('-mt','--max-time', action="store", 
                    help='Максимальное время выполнения job')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)
#print variables

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds

if len(variables['jobname']) > 0 and variables['max_time'] is None:
	hostname_url = "%s" % variables['hostname']
	J = Jenkins(hostname_url)
	job_status = J[variables['jobname']].get_last_build().get_status() 

	if 'FAILURE' in job_status:
	  print "CRITICAL - Job build not successful"
          print "See more %s/job/%s" % (variables['hostname'],variables['jobname'])
	  sys.exit(2)
	elif 'SUCCESS' in job_status:
	  print 'OK - Build ok'
	  sys.exit(0)
	else:
	  print 'UNKNOWN - Unknown state'
	  sys.exit(3)


if len(variables['max_time']) > 0:
        hostname_url = "%s" % variables['hostname']
        j = Jenkins(hostname_url)
        d,h,m,s = convert_timedelta(j['GB20-monitoring'].get_last_build().get_duration())
	if h:
		m+=h*60
	if m > int(variables['max_time']):
		print "CRITICAL - Job run more than %s minutes. Build %s min" % (variables['max_time'],m)
		print "See more %s/job/%s" % (variables['hostname'],variables['jobname']) 
		sys.exit(2)
	else:
		print "OK - Build time is ok"
		sys.exit(0)







