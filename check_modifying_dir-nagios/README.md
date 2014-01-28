DESCRIPTION
===
Nagios-плагин для мониторинга времени изменения директории. Например создался ли вчерашний бэкап и т.д.

    usage: check_rsnapshot_backup.py [-h] [--wtime WTIME] [--dtime DTIME] --dir DIR

    Check time change directory for Nagios

    optional arguments:
      -h, --help     show this help message and exit
      --wtime WTIME  Устанавливает количество недель
                     не позже которых должна быть
                     изменена директория
      --dtime DTIME  Устанавливает количество дней не
                     позже которых должна быть
                     изменена директория
      --dir DIR      Путь до каталога

Для корректной работы плагина необходимо удовлетворить все зависимости, которые есть в файле requirements.txt

    pip install -r requirements.txt


