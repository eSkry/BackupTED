## BackupTED - Backup to external drive

### Zip password make
Генерация пароля происходит следующим образом:
1. Из файла `config.conf` берется пароль из переменной `zip_pass` (например `myPass`)
1. К данном пароль дубавляется соль, которая генерируется случайно и парль имеет вид `myPass_{salt}` (например myPass_gw42g45)
1. Соль сохраняется в таблице `sync`, столбец `zip_pass_salt`
