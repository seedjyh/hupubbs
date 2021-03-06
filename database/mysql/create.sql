-- 数据库
CREATE DATABASE IF NOT EXISTS `hupubbs` DEFAULT CHARACTER SET utf8;

USE `hupubbs`;

-- 用户表user
CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `url_id` VARCHAR(32) NOT NULL,
    `nickname` VARCHAR(128) NOT NULL,
    `signature` VARCHAR(1024) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`url_id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 版块表plate
CREATE TABLE IF NOT EXISTS `plate` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL,
    `url` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`name`),
    UNIQUE KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 主题表thread
CREATE TABLE IF NOT EXISTS `thread` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `url_id` VARCHAR(32) NOT NULL,
    `plate_id` bigint(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `post_time` TIMESTAMP NOT NULL,
    `title` VARCHAR(1024) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`url_id`),
    FOREIGN KEY (`plate_id`) REFERENCES `plate`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 回帖表reply
CREATE TABLE IF NOT EXISTS `reply` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `thread_id` bigint(20) NOT NULL,
    `url_id` VARCHAR(20) NOT NULL,
    `user_id` bigint(20) NOT NULL,
    `post_time` TIMESTAMP NOT NULL,
    `i_like_sum` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`thread_id`) REFERENCES `thread`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
    UNIQUE KEY (`thread_id`, `url_id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
