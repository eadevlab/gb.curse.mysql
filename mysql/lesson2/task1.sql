/*
Задание 1
Установите СУБД MySQL. Создайте в домашней директории файл .my.cnf, задав в нем логин и пароль, который указывался при установке.
 */
-- готово
/*
Задание 2
Создайте базу данных example, разместите в ней таблицу users, состоящую из двух столбцов, числового id и строкового name.
 */

create database example;
use example;


CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(128) NOT NULL,
PRIMARY KEY (`id`)
);

/*
Задание 3
Создайте дамп базы данных example из предыдущего задания, разверните содержимое дампа в новую базу данных sample.
 */

mysqldump -u dev -p -f example > ./dump.sql
mysql -u dev -p
create database sample;
exit;
mysql -u dev -p sample < ./dump.sql 

/*
Задание 4
(по желанию) Ознакомьтесь более подробно с документацией утилиты mysqldump. Создайте дамп единственной таблицы help_keyword базы данных mysql. Причем добейтесь того, чтобы дамп содержал только первые 100 строк таблицы.
 */

mysqldump -u dev -p794613 mysql help_keyword --where="1 limit 100" > mysql_hk_dump.sql
