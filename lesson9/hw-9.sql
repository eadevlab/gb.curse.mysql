-- Транзакции, переменные, представления
/*
 * В базе данных shop и sample присутствуют одни и те же таблицы, учебной базы данных. 
 * Переместите запись id = 1 из таблицы shop.users в таблицу sample.users. Используйте транзакции.
 */


START TRANSACTION;
TRUNCATE sample.users; 
INSERT INTO sample.users (id, name) select id, name from shop.users where id = 1;
COMMIT;

-- select * from sample.users;
-- select id, name from shop.users where id = 1;

/*
 * Создайте представление, которое выводит название name товарной позиции из таблицы products и соответствующее название каталога name из таблицы catalogs.
 */
use shop;

CREATE OR REPLACE VIEW products_categories AS
SELECT p.name AS product, c.name AS category FROM products p
JOIN catalogs AS c ON p.catalog_id = c.id;

select * from products_categories;

/*
 * Пусть имеется таблица с календарным полем created_at.
 * В ней размещены разряженые календарные записи за август 2018 года '2018-08-01', '2018-08-04', '2018-08-16' и 2018-08-17. 
 * Составьте запрос, который выводит полный список дат за август, выставляя в соседнем поле значение 1, 
 * если дата присутствует в исходном таблице и 0, если она отсутствует. 
 */
DROP TABLE IF EXISTS tmp_dates;
CREATE TABLE tmp_dates (
	id SERIAL PRIMARY KEY,
	created_at DATE
);

INSERT INTO tmp_dates (created_at) VALUES
('2018-08-01'),('2018-08-04'),('2018-08-16'),('2018-08-17');


-- SELECT LAST_DAY('2018-08-01');

-- Процедуря для генерации временного промежутка
-- DROP PROCEDURE IF EXISTS generate_daterange;
CREATE OR REPLACE PROCEDURE generate_daterange(date_start DATE, date_end DATE)
BEGIN 
    DROP TEMPORARY TABLE IF EXISTS tmp_month_days;
	CREATE TEMPORARY TABLE tmp_month_days (d DATE); 
	WHILE date_start <= date_end DO
	insert into tmp_month_days(d) VALUES(date_start);
	SET date_start = DATE_ADD(date_start, INTERVAL 1 DAY);
	END WHILE;
	SELECT tmd.d, IF(td.id IS NOT NULL, 1, 0) as date_exists from tmp_month_days tmd
	LEFT JOIN tmp_dates td on tmd.d = td.created_at
	ORDER BY tmd.d;
END;

CALL generate_daterange('2018-08-01',LAST_DAY('2018-08-08'));
-- SELECT * FROM (CALL generate_daterange('2018-08-01',LAST_DAY('2018-08-08')));

/*
 * Пусть имеется любая таблица с календарным полем created_at.
 * Создайте запрос, который удаляет устаревшие записи из таблицы, оставляя только 5 самых свежих записей.
*/
DROP TABLE IF EXISTS tmp_dates;
CREATE TABLE tmp_dates (
	id SERIAL PRIMARY KEY,
	created_at DATE
);

INSERT INTO tmp_dates (created_at) VALUES
('2022-09-01'),('2022-09-02'),('2022-09-03'),('2022-09-04'),('2022-09-05'),('2022-09-06'),('2022-09-07'),('2022-09-08'),('2022-09-09'),('2022-09-10');

select * from tmp_dates;
delete from tmp_dates WHERE id not in (select id from tmp_dates td order by created_at desc limit 5);

select * from tmp_dates;


-- Хранимые процедуры и функции, триггеры
/*
 * Создайте хранимую функцию hello(), которая будет возвращать приветствие, в зависимости от текущего времени суток.
 * С 6:00 до 12:00 функция должна возвращать фразу "Доброе утро", 
 * с 12:00 до 18:00 функция должна возвращать фразу "Добрый день", 
 * с 18:00 до 00:00 — "Добрый вечер",
 * с 00:00 до 6:00 — "Доброй ночи".
 */
-- SELECT DATE_FORMAT(NOW(), '%H');
CREATE OR REPLACE PROCEDURE hello()
BEGIN 
	SET @current_hour = DATE_FORMAT(NOW(), '%H');
	SELECT CASE 
		WHEN @current_hour > 6 and @current_hour <= 12 THEN 'Доброе утро'
		WHEN @current_hour > 12 and @current_hour <= 18 THEN 'Добрый день'
		WHEN @current_hour > 18 and @current_hour <= 0 THEN 'Добрый вечер'
		WHEN @current_hour > 0 and @current_hour <= 6 THEN 'Доброй ночи'
	END as hello_message;
END;

CALL hello();

/*
 * В таблице products есть два текстовых поля: name с названием товара и description с его описанием.
 * Допустимо присутствие обоих полей или одно из них. Ситуация, когда оба поля принимают неопределенное значение NULL неприемлема.
 * Используя триггеры, добейтесь того, чтобы одно из этих полей или оба поля были заполнены.
 * При попытке присвоить полям NULL-значение необходимо отменить операцию. 
 */
use shop;

drop trigger if exists validate_product_row_insert;
drop trigger if exists validate_product_row_update;

DELIMITER $$
create trigger validate_product_row_insert before insert on shop.products 
for each row 
BEGIN 
	if((new.name is null or new.name = '') and (new.description is null or new.description = '')) THEN 
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ошибка! Поля name или description должны быть заполнены';
	end if;
END$$

create trigger validate_product_row_update before update on shop.products 
for each row 
BEGIN 
	if((new.name is null or new.name == '') and (new.description is null or new.description == '')) THEN 
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ошибка! Поля name или description должны быть заполнены';
	end if;
END$$
DELIMITER ;


/*
 * Напишите хранимую функцию для вычисления произвольного числа Фибоначчи.
 * Числами Фибоначчи называется последовательность в которой число равно сумме двух предыдущих чисел. 
 * Вызов функции FIBONACCI(10) должен возвращать число 55.
 */
-- SET max_sp_recursion_depth = 100;
-- DROP FUNCTION IF EXISTS FIBONACCI;
-- DELIMITER &&
-- CREATE OR REPLACE FUNCTION FIBONACCI(i INT) RETURNS INT DETERMINISTIC  BEGIN DECLARE a INT default 0; DECLARE b INT default 0; DECLARE c INT default 0;SET max_sp_recursion_depth=50; IF i = 1 OR i = 2 THEN SET c = 1; ELSE SET a = FIBONACCI(i-1);SET b = FIBONACCI(i-2);SET c = a + b; END IF; RETURN c; END&&
-- DELIMITER ;

-- С рекурсией не задалось
DELIMITER &&
CREATE OR REPLACE FUNCTION FIBONACCI(n INT)
RETURNS INT DETERMINISTIC 
BEGIN 
	DECLARE i INT DEFAULT 0;
	DECLARE j INT DEFAULT 1;
	DECLARE c INT DEFAULT 0;
	DECLARE s INT DEFAULT 0;
	IF n in (1,2) THEN
		RETURN 1;
	END IF;
	loop_tag: LOOP
		IF s >= n-1 THEN
			LEAVE loop_tag;
		END IF;
		SET c = i + j;
		SET i = j;
		SET j = c;
		SET s = s + 1;
	END LOOP loop_tag;
	RETURN c;
END&&
DELIMITER ;

-- inline
DELIMITER &&
CREATE OR REPLACE FUNCTION FIBONACCI(n INT) RETURNS INT DETERMINISTIC BEGIN DECLARE i INT DEFAULT 0;DECLARE j INT DEFAULT 1;DECLARE c INT DEFAULT 0;DECLARE s INT DEFAULT 0;IF n in (1,2) THEN RETURN 1;END IF;loop_tag: LOOP IF s >= n-1 THEN LEAVE loop_tag;END IF;SET c = i + j;SET i = j;SET j = c;SET s = s + 1;END LOOP loop_tag;RETURN c;END&&
DELIMITER ;

SELECT FIBONACCI(10);
--  55
-- Отказывается запускаться в dbeaver, через консоль и workbench отрабатывает нормально


-- Администрирование MySQL
/*
 * Создайте двух пользователей которые имеют доступ к базе данных shop. 
 * Первому пользователю shop_read должны быть доступны только запросы на чтение данных, 
 * второму пользователю shop — любые операции в пределах базы данных shop.
 */
-- sudo mysql
DROP USER IF EXISTS shop;
DROP USER IF EXISTS shop_read;

CREATE USER shop IDENTIFIED BY '794613';
CREATE USER shop_read IDENTIFIED BY '794613';
-- все привелегии
GRANT ALL PRIVILEGES ON shop.* TO shop;
GRANT SELECT ON shop.* TO shop_read;
-- exit
-- mysql -u shop_read -p794613
/*
MariaDB [(none)]> use shop;
Database changed
MariaDB [shop]> delete catalog;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '' at line 1
MariaDB [shop]> delete from catalog;
ERROR 1142 (42000): DELETE command denied to user 'shop_read'@'localhost' for table 'catalog'
*/

/*
 * Пусть имеется таблица accounts содержащая три столбца id, name, password, содержащие первичный ключ, имя пользователя и его пароль. 
 * Создайте представление username таблицы accounts, предоставляющий доступ к столбца id и name. 
 * Создайте пользователя user_read, который бы не имел доступа к таблице accounts, однако, мог бы извлекать записи из представления username.
 */
USE shop;
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
	id SERIAL PRIMARY KEY,
	name VARCHAR (128),
	password VARCHAR(256)
);

DROP VIEW IF EXISTS username;
CREATE VIEW username(id, name) AS SELECT id, name FROM accounts;

INSERT INTO accounts(name, password) VALUES ('user1', 'password1'),('user2', 'password2'),('user3', 'password3'),('user4', 'password4');

SELECT * fROM username;

-- sudo mysql
DROP USER IF EXISTS user_read;
CREATE USER user_read IDENTIFIED BY '794613';
GRANT SELECT ON shop.username TO user_read;
-- exit
-- mysql -u user_read -p794613
-- use shop;
/*
MariaDB [shop]> select * from accounts;
ERROR 1142 (42000): SELECT command denied to user 'user_read'@'localhost' for table 'accounts'
MariaDB [shop]> select * from username;
+----+-------+
| id | name  |
+----+-------+
|  1 | user1 |
|  2 | user2 |
|  3 | user3 |
|  4 | user4 |
+----+-------+
4 rows in set (0.001 sec)
*/
