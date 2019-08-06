/*
    example data

    truncate table wordsinposts;
    truncate table wordsdesc;
    truncate table posts;
*/

INSERT INTO `posts`(`postsNewsId`,`postsType`,`postsTitle`,`postsPublishTime`,`postsMain`) 
VALUES('k00000',1,'高知県','2019-05-22 11:30:00','知らない')

INSERT INTO `wordsdesc`(`wordsMain`,`wordsDesc`,`wordsHash`) 
VALUES('Amplified','Digest',MD5('Amplified'))

INSERT INTO `wordsinposts`(`postsId`,`wordsId`)
VALUES(1,1)