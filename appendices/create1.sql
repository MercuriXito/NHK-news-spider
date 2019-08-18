/*
    Mysql 5.6
    Set up the database and tables

DROP TABLE IF EXISTS DangoInPosts;
DROP TABLE IF EXISTS EasyPosts;
DROP TABLE IF EXISTS DangoMeans;

truncate table EasyPosts;
truncate table DangoMeans;

DROP DATABASE IF EXISTS nhknews;

注意在linux下mysql也是严格区分大小写的。
*/

CREATE DATABASE IF NOT EXISTS nhknews DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; 

USE nhknews;

-- 新闻表
CREATE TABLE IF NOT EXISTS EasyPosts(
    postId INT AUTO_INCREMENT, -- 虽然和postNewsId作用类似，但是还是担心postNewsId会出现问题
    postNewsId VARCHAR(40) UNIQUE NOT NULL, -- nhk网站上自带的posts的id，依次为主键
    postTitle VARCHAR(200) NOT NULL, -- title
    postPublishTime DATETIME NOT NULL, -- publishTime
    postContent VARCHAR(3000), -- content
    postType TINYINT NOT NULL, -- posts类型，预留给非easynews
    hasImg BOOLEAN DEFAULT 0 NOT NULL,
    hasAudio BOOLEAN DEFAULT 0 NOT NULL,
    imgName VARCHAR(200),
    audioName VARCHAR(200),
    PRIMARY KEY(postId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
/* img 和 audio 如果有那么对应的属性为True，统一的名字是 postNewsId + MD5(title) */
/* 在mysql中设置字段类型为boolean。mysql会自动变成tinyint(1), 所以default value 为0/1。 */

-- 名词解释表
CREATE TABLE IF NOT EXISTS DangoMeans(
    dangoId INT AUTO_INCREMENT,
    totalHash VARCHAR(32) NOT NULL, -- 这个hash的方法是 dango + mean 字段再hash
    dango VARCHAR(200),
    mean VARCHAR(1000),
    PRIMARY KEY(dangoId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 名词解释和新闻的关联表
CREATE TABLE IF NOT EXISTS DangoInPosts(
    id INT AUTO_INCREMENT,
    postId INT,
    dangoId INT,
    PRIMARY KEY(id),
    FOREIGN KEY (postId) REFERENCES EasyPosts(postId),
    FOREIGN KEY (dangoId) REFERENCES DangoMeans(dangoId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;