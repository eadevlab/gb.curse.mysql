use vk;
/*
 * Пусть задан некоторый пользователь. 
 * Из всех друзей этого пользователя найдите человека, который больше всех общался с нашим пользователем.
 */
-- user id = 1
SELECT
from_user_id,
(select CONCAT(firstname,' ',lastname) from users WHERE id = messages.from_user_id) as from_name,
COUNT(*) as cnt FROM messages 
WHERE to_user_id = 1 and from_user_id in ( select initiator_user_id from friend_requests where target_user_id = 1 and status = 'approved' and confirmed_at < NOW()
UNION 
select target_user_id from friend_requests WHERE initiator_user_id = 1 and status = 'approved' and confirmed_at < NOW())
GROUP BY from_user_id 
ORDER BY cnt desc
LIMIT 1;
-- 4 Norene West 3

-- select * from friend_requests where (target_user_id = 1 or initiator_user_id = 1) and status = 'approved' and confirmed_at < NOW()

-- select initiator_user_id from friend_requests where target_user_id = 1 and status = 'approved' and confirmed_at < NOW()
-- UNION 
-- select target_user_id from friend_requests WHERE initiator_user_id = 1 and status = 'approved' and confirmed_at < NOW();

/*
 * Подсчитать общее количество лайков, которые получили пользователи младше 11 лет.
 */
-- select user_id, (YEAR(NOW())-YEAR(birthday) - (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(birthday , '%m%d'))) as age from profiles where (YEAR(NOW())-YEAR(birthday) - (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(birthday , '%m%d'))) < 11

select count(*) as likes from likes
where user_id in (select user_id from profiles where (YEAR(NOW())-YEAR(birthday) - (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(birthday , '%m%d'))) < 11);
-- 2
/**
 * Определить кто больше поставил лайков (всего): мужчины или женщины.
 */
select (select IF(gender='m','мужчины','женщины') from profiles where user_id = likes.user_id) as gender, count(*) as likes_cnt from likes
group by gender
order by likes_cnt desc;
-- limit 1;
-- Больше лайков поставили женщины
