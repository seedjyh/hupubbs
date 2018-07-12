-- 数据库
CREATE DATABASE IF NOT EXISTS `hupubbs` DEFAULT CHARACTER SET utf8;

USE `hupubbs`;

-- 用户表user
CREATE TABLE IF NOT EXISTS `user` (
    `id` VARCHAR(32) NOT NULL,
    `nickname` VARCHAR(128) NOT NULL,
    `prosign` VARCHAR(1024) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 主题表thread
CREATE TABLE IF NOT EXISTS `thread` (
    `id` VARCHAR(32) NOT NULL,
    `user_id` VARCHAR(32) NOT NULL,
    `post_time` TIMESTAMP NOT NULL,
    `title` VARCHAR(1024) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

-- 回帖表reply
CREATE TABLE IF NOT EXISTS `reply` (
    `id` VARCHAR(32) NOT NULL,
    `thread_id` VARCHAR(32) NOT NULL,
    `user_id` VARCHAR(32) NOT NULL,
    `post_time` TIMESTAMP NOT NULL,
    `i_like_sum` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`thread_id`) REFERENCES `thread`(`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;
