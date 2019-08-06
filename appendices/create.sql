/*
    Mysql 5.6
    Set up the database and tables

DROP TABLE IF EXISTS wordsinposts;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS wordsdesc;

truncate table posts;
truncate table wordsdesc;

DROP DATABASE IF EXISTS nhknews;
*/

CREATE DATABASE IF NOT EXISTS nhknews DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; 

USE nhknews;

-- 新闻表
CREATE TABLE IF NOT EXISTS posts(
    postsId UNSIGNED INT AUTO_INCREMENT,
    postsNewsId VARCHAR(40) UNIQUE NOT NULL,
    postsType TINYINT NOT NULL,
    postsTitle VARCHAR(200) NOT NULL,
    postsPublishTime DATETIME NOT NULL,
    postsMain VARCHAR(2000),
    PRIMARY KEY(postsId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 名词解释表
CREATE TABLE IF NOT EXISTS wordsdesc(
    wordsId INT AUTO_INCREMENT,
    wordsHash VARCHAR(32) NOT NULL,
    wordsMain VARCHAR(200),
    wordsDesc VARCHAR(1000),
    PRIMARY KEY(wordsId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 名词解释和新闻的关联表
CREATE TABLE IF NOT EXISTS wordsinposts(
    wordsInPostsId INT AUTO_INCREMENT,
    postsId INT,
    wordsId INT,
    PRIMARY KEY(wordsInPostsId),
    FOREIGN KEY (postsId) REFERENCES posts(postsId),
    FOREIGN KEY (wordsId) REFERENCES wordsDesc(wordsId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;