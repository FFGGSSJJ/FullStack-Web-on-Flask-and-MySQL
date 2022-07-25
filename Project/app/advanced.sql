-- compute average rating for different movies 
SELECT
    c.movie_id,
    title,
    avg(c.rating) as average_rating,
    release_date,
    homepage,
    poster_path
FROM
    comments c
    join movie_info m on c.movie_id = m.movie_id
WHERE
    release_date > '2010-1-1'
GROUP BY
    c.movie_id
ORDER BY
    average_rating DESC
LIMIT
    15 --compute numbers of comments with rating more than 2 for each user
SELECT
    account_info.userID,
    account_name,
    COUNT(movie_id) AS NumMov
FROM
    account_info
    LEFT OUTER JOIN comments ON account_info.userID = comments.userID
WHERE
    account_name LIKE "B%"
    and comments.rating >= 2
GROUP BY
    account_info.userID
ORDER BY
    NumMov DESC
LIMIT
    15;