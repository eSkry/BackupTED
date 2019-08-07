## Конфигурация демона

### Linux systemd
1. В файле `backupted.service` изменить путь к скрипту в переменной ExecStart на необходимый
1. Фаил `backupted.service` скопировать в `/etc/systemd/system/`
1. Выполнить `systemctl daemon-reload`
1. Затем `systemctl start backupted`
