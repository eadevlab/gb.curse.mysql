/*
 * Составьте список пользователей users, которые осуществили хотя бы один заказ orders в интернет магазине.
*/
-- сначала надо добавить данные в orders
INSERT INTO orders (user_id) VALUES
(1), (2), (2), (6);

select * from orders;

select DISTINCT u.id, u.name from users as u
right join orders as o on u.id  = o.user_id;

/*
 * Выведите список товаров products и разделов catalogs, который соответствует товару.
 * 
 */
select p.id, p.name, p.description,p.price,c.name as catalog_name from products as p 
left join catalogs as c ON p.catalog_id = c.id;

/*
 * (по желанию) Пусть имеется таблица рейсов flights (id, from, to) и таблица городов cities (label, name).
 * Поля from, to и label содержат английские названия городов, поле name — русское. 
 * Выведите список рейсов flights с русскими названиями городов.
 */
DROP TABLE IF EXISTS flights;
create table flights (
	id SERIAL PRIMARY KEY,
	`from` varchar(255) NOT NULL,
  	`to` varchar(255) NOT NULL
);

INSERT INTO flights (`from`,`to`) VALUES
('moscow', 'omsk'),
('novgorod','kazan'),
('irkutsk', 'moscow'),
('omsk','irkutsk'),
('moscow','kazan');

DROP TABLE IF EXISTS cities;
create table cities (
	label varchar(255) NOT NULL,
  	name varchar(255) NOT NULL
);

INSERT INTO cities VALUES
('moscow', 'Москва'),
('irkutsk', 'Иркутск'),
('novgorod', 'Новгород'),
('kazan', 'Казань'),
('omsk', 'Омск');


select f.id, c1.name as `from`, c2.name as `to` from flights as f
inner join cities as c1 on c1.label = f.from
inner join cities as c2 on c2.label = f.to
order by f.id;

