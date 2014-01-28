#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: g.rusakov@adriver.ru
# 
import os
import os.path
import argparse
import datetime
import time
import sys

# По умолчанию модуль argparse также имеет опцию -h или --help для вывода удобночитаемого хелпа.
# 
# Задаем опции, которые будут устанавливать критерии мониторинга.

parser = argparse.ArgumentParser(description='\033[1mCheck time change file or directory for Nagios\033[0m')
parser.add_argument('-w', '--wtime', action="store", type=int,
                    help='Устанавливает количество недель не позже которых должна быть изменена директория/файл')
parser.add_argument('-d', '--dtime', action="store", type=int,
                    help='Устанавливает количество дней не позже которых должна быть изменена директория/файл')
parser.add_argument('--htime', action="store", type=int,
                    help='Устанавливает количество часов не позже которых должна быть изменена директория/файл')
parser.add_argument('-m', '--mtime', action="store", type=int,
                    help='Устанавливает количество минут не позже которых должна быть изменена директория/файл')
parser.add_argument('--dir', action="store",
                    help='Путь до каталога')
parser.add_argument('--file', action="store",
                    help='Путь до файла')

args = parser.parse_args()

# Для доступа к Namespace словарю используем vars(). Результатом будет хэш.
variables = vars(args)

# Проверяем существование директории или файла. В случае ошибки возвращаем CRITICAL
if os.path.exists(variables['dir'] or variables['file']) != True:
  print "CRITICAL - Directory or file %s does not exists." % variables['dir'] or variables['file']
  sys.exit(2)

if variables['dir']:
  # Проверяем что проверяемая директория является директорей и что она создана
  if os.path.isdir(variables['dir']) != True:
    print "UNKNOWN - Tested directory %s must be directory or dir not created" % variables['dir']
    sys.exit(3)

  # Проверяем директорию на пустоту
  if not os.listdir(variables['dir']):
    print "CRITICAL - Directory %s created but empty. Fix it." % variables['dir']
    sys.exit(2)

elif variables['file']:
  if os.path.getsize(variables['file']) == 0:
    print "CRITICAL - File %s is empy" % variables['file']
    sys.exit(2)

# Количество секунд в дне, неделе, часе, минуте
if variables['dtime']:
  date = 86400 * variables['dtime']
elif variables['wtime']:
  date = 604800 * variables['wtime']
elif variables['htime']:
  date = 3600 * variables['htime']
elif variables['mtime']:
  date = 60 * variables['mtime']

# Функция для проверки времени изменения файла/каталога. Выводит количество секунд с момента изменения
def time_change(filename):
  return (int(time.time()) - int(os.path.getmtime(filename))) # / 60 / 60

# Переводим секунды в часы для удобночитаемого вида
hours_ago = time_change(variables['dir'] or variables['file']) / 60 / 60

# Переводим секунды в минуты 
minutes_ago = time_change(variables['dir'] or variables['file']) / 60

# Проверяем время измения файла. Возвращаем CRITICAL, в другом случае OK.
if time_change(variables['dir'] or variables['file']) > date:
  print "CRITICAL - Directory or file %s not modified" % (variables['dir'] or variables['file'])
  print "Hours: %s Minutes: %s" % (hours_ago,minutes_ago)
  sys.exit(2)
else: 
  print "OK - %s" % ( variables['dir'] or variables['file'] )
  sys.exit(0)
  