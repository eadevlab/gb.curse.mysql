-- выбираем бд
USE vk;
-- посты пользователя
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	id SERIAL PRIMARY KEY,
	user_id BIGINT UNSIGNED NOT NULL,
	media_id BIGINT UNSIGNED NULL, -- медиа контента может и не быть в посте
	shared_post_id BIGINT UNSIGNED NULL, -- 
	content TEXT NULL,
	created_at DATETIME DEFAULT NOW(),
	updated_at DATETIME ON UPDATE NOW(),
	views_cnt INT UNSIGNED, -- закешированное количество просмотров --	
	likes_cnt INT UNSIGNED, -- закешированное количество лайков --

    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (media_id) REFERENCES media(id) ON UPDATE CASCADE ON DELETE SET NULL
	
);

ALTER TABLE posts ADD CONSTRAINT fk_shared_post_id
    FOREIGN KEY (shared_post_id) REFERENCES posts(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- стена пользователя
DROP TABLE IF EXISTS user_wall;
CREATE TABLE user_wall (
	id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    post_id BIGINT UNSIGNED NOT NULL,
	
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON UPDATE CASCADE ON DELETE CASCADE
);


-- комментарии к постам пользователя
DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
	id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    post_id BIGINT UNSIGNED NOT NULL,
	content TEXT NULL,
	likes_cnt INT UNSIGNED, -- закешированное количество лайков
	created_at DATETIME DEFAULT NOW(),
	updated_at DATETIME ON UPDATE NOW(),

	FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS friend_groups;
CREATE TABLE friend_groups (
	id SERIAL PRIMARY KEY,
	user_id BIGINT UNSIGNED NOT NULL,
	name VARCHAR(255),
	color VARCHAR(6),
	FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE friend_requests
ADD group_id BIGINT UNSIGNED NULL,
ADD CONSTRAINT fk_group_id FOREIGN KEY(group_id) REFERENCES friend_groups(id);

