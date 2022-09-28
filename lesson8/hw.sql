use vk;
/*
 * Пусть задан некоторый пользователь. 
 * Из всех друзей этого пользователя найдите человека, который больше всех общался с нашим пользователем.
 */

select m.from_user_id, CONCAT(u.firstname, ' ', u.lastname) as from_name, count(*) as cnt from messages m 
join users u on u.id = m.from_user_id 
join friend_requests fr ON (m.to_user_id = fr.target_user_id and m.from_user_id  = fr.initiator_user_id) or (m.to_user_id = fr.initiator_user_id  and m.from_user_id  = fr.target_user_id)
where m.to_user_id  = 1 and fr.status = 'approved'
group by m.from_user_id 
order by cnt desc
limit 1;
-- 4 Norene West 3

/*
 * Подсчитать общее количество лайков, которые получили пользователи младше 11 лет.
 */
select count(*) as cnt from media m 
join likes l on m.id  = l.media_id 
join profiles p on m.user_id = p.user_id 
where (YEAR(NOW())-YEAR(p.birthday) - (DATE_FORMAT(CURRENT_DATE, '%m%d') < DATE_FORMAT(p.birthday , '%m%d'))) < 11

/**
 * Определить кто больше поставил лайков (всего): мужчины или женщины.
 */
select IF(p.gender='m','мужчины','женщины') as gender, count(*) as cnt from likes l 
join profiles p on p.user_id = l.user_id 
GROUP by gender
order by cnt desc
-- limit 1;
-- Больше лайков поставили женщины

