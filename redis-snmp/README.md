DESCRIPTION
===

snmp-persist скрипт, который подключается к redis к нужному порту и хосту и получает окружение
через команду info. После чего посекционно считывает его, создавая индексированный snmp-ответ.

Например:

	# Server
	redis_version:2.6.16
	redis_git_sha1:00000000
	redis_git_dirty:0
	redis_mode:standalone
	os:Linux 3.2.0-0.bpo.4-amd64 x86_64
	arch_bits:64
	multiplexing_api:epoll
	gcc_version:4.4.5
	process_id:22405
	run_id:9654323ec85c897974c9f7fe38f3a2fc41578add
	tcp_port:6380
	uptime_in_seconds:3890694
	uptime_in_days:45
	hz:10
	lru_clock:471399

Результатом будет hash:

	redis_version: 2.6.16

С помощью python pass-persist добавляем посекционно.

Получается:

	.oid.1 - Server
	.oid.1.1 - 2.6.16

Используя дефолтную конфигурацию мы можем обращаться к фиксированным oid. Работает только с redis 2.6.X

Версия 0.1.Х умеет только дефолтный кофниг с неизменными ключами. 

USAGE
===

	pass_persist some_redis_oid /usr/bin/env python -u /usr/local/bin/redis-snmp-persist.py -H redis_host -p redis_port -o 1