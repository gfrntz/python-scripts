DESCRIPTION
===
Nagios plugin for jenkins

USAGE
===

Monitoring job build state

    python check_job_state.py --hostname JENKINS_URL --jobname JOBNAME
    CRITICAL - Job build not successful
    See more http://builserver:8080/job/JOBNAME
    echo $?
    2



Monitoring job build time

	check_job_state.py -H http://buildserver:8080 --jobname JOBNAME -mt 10
	CRITICAL - Job run more than 10 minutes. Build 12 min
