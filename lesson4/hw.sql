USE vk;
-- Заполнить все таблицы БД vk данными (по 10-100 записей в каждой таблице).
-- в файле vk_tables_data.sql

-- Написать скрипт, возвращающий список имен (только firstname) пользователей без повторений в алфавитном порядке.
SELECT DISTINCT firstname FROM users ORDER by firstname 

-- Первые пять пользователей пометить как удаленные.
UPDATE users SET is_deleted = 1 ORDER BY id LIMIT 5
-- SELECT * from users

-- Написать скрипт, удаляющий сообщения «из будущего» (дата больше сегодняшней).
-- SELECT * FROM messages WHERE created_at > NOW()
DELETE FROM messages WHERE created_at > NOW()

-- 	Написать название темы курсового проекта.
-- Тема: Разработка базы данных "Онлайн библиотека"
/* 
 * 
 * 
 * 
 * 
 */