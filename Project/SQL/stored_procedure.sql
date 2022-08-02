CREATE PROCEDURE recommend(IN search_userID INT) BEGIN DECLARE done INT default 0;

DECLARE user_tag1 INT;

DECLARE user_tag2 INT;

DECLARE user_tag3 INT;

DECLARE curr_user INT;

DECLARE curr_tag1 INT;

DECLARE curr_tag2 INT;

DECLARE curr_tag3 INT;

DECLARE usesr_cursor CURSOR FOR
SELECT
    DISTINCT userID
FROM
    account_info
WHERE
    userID != search_userID;

DECLARE CONTINUE HANDLER FOR NOT FOUND
SET
    done = 1;

SET
    user_tag1 = (
        SELECT
            tag1
        FROM
            account_info
        WHERE
            account_info.userID = search_userID
    );

SET
    user_tag2 = (
        SELECT
            tag2
        FROM
            account_info
        WHERE
            account_info.userID = search_userID
    );

SET
    user_tag3 = (
        SELECT
            tag3
        FROM
            account_info
        WHERE
            account_info.userID = search_userID
    );

DROP TABLE IF EXISTS recommend_table;

CREATE TABLE recommend_table(
    userID INT,
    rating real,
    movie_id int,
    title VARCHAR(50)
);

OPEN usesr_cursor;

REPEAT FETCH usesr_cursor INTO curr_user;

SET
    curr_tag1 = (
        SELECT
            tag1
        FROM
            account_info
        WHERE
            account_info.userID = curr_user
    );

SET
    curr_tag2 = (
        SELECT
            tag2
        FROM
            account_info
        WHERE
            account_info.userID = curr_user
    );

SET
    curr_tag3 = (
        SELECT
            tag3
        FROM
            account_info
        WHERE
            account_info.userID = curr_user
    );

IF (curr_tag1 in (user_tag1, user_tag2, user_tag3))
and (curr_tag2 in (user_tag1, user_tag2, user_tag3))
and (curr_tag3 in (user_tag1, user_tag2, user_tag3)) THEN
INSERT INTO
    recommend_table (
        SELECT
            watch_list.userID,
            temp.average_rating,
            watch_list.movie_id,
            temp.title
        FROM
            watch_list
            join (
                SELECT
                    c.movie_id,
                    m.title,
                    avg(c.rating) as average_rating
                FROM
                    comments c
                    join movie_info m on c.movie_id = m.movie_id
                GROUP BY
                    c.movie_id
            ) as temp on watch_list.movie_id = temp.movie_id
        WHERE
            watch_list.userID = curr_user
    );

END IF;

UNTIL done
END REPEAT;

CLOSE usesr_cursor;

select
    *
from
    recommend_table
END