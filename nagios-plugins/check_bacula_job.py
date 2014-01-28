#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: chainwolf@gmail.com
# 
# ver 0.1.0
#
# модуль psycopg2 для коннекта к postgres БД
# модуль sys для вывода кода выполнения
# модуль time для перевода из date в timestamp
# модуль argparse для указания времени изменения джоба
# 
import psycopg2
import sys
import time
import argparse

# задаем
parser = argparse.ArgumentParser(description='\033[1mCHow long bacula job works?\033[0m')
parser.add_argument('-w', action="store", type=int, required=True,
                    help='How many hours?')
parser.add_argument('-c', action="store", type=int, required=True,
                    help='How many hours?')
# парсим
args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)


# получаем время сейчас в timestamp
time_now = time.time()

# коннектимся к базе бакулы
con = psycopg2.connect(host='bacula-pgsql-host', database='bacula', user='bacula', password='bacula')
# устанавливаем курсор. Зачем это? Видимо вначало.
cur = con.cursor()
# Получаем имя джоба и его время запуска
cur.execute("SELECT Job.Name, Job.StartTime FROM Job WHERE Job.JobStatus = 'R';")
# Фетчим все в res. Результатом будет массив массивов. 
# [('boom2_adriver_x', datetime.datetime(2014, 1, 19, 0, 10, 1))]
# 
# datetime в случае вывода будет:
# print res[0][1]
# 2014-01-19 00:10:01
# 
res = cur.fetchall()

WARNING = []
CRITICAL = []

for i in res:
	timeStamp = time.mktime(i[1].timetuple())
	jobWorks = (int(time_now) - int(timeStamp)) / 60 / 60
	if jobWorks > variables['c']:
		CRITICAL.append(i[0])
	elif jobWorks > variables['w']:
		WARNING.append(i[0])

	
if len(CRITICAL) > 0:
	print "CRITICAL - Job %s works more than %s hours" % (', '.join(CRITICAL + WARNING),variables['c'])
	print "CRIT: %s WARN: %s " % (', '.join(CRITICAL),', '.join(WARNING))
	sys.exit(2)
elif len(WARNING) > 0:
	print "WARNING - Job %s works more than %s hours" % (', '.join(WARNING),variables['w'])
	sys.exit(1)
else:
	print "OK - Bacula works well"
	sys.exit(0)
	

