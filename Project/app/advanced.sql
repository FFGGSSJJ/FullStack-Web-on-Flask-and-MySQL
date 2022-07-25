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
    15;

-- ave rating for different genre
SELECT
    g.genre_name,
    avg(temp1.average_rating) as ave_genre_rating
From
    movie_genre m_g
    join (
        SELECT
            c.movie_id,
            avg(c.rating) as average_rating
        FROM
            comments c
            join movie_info m on c.movie_id = m.movie_id
        GROUP BY
            c.movie_id
        ORDER BY
            average_rating DESC
    ) as temp1 on temp1.movie_id = m_g.movie_id
    join genre g on g.genre_id = m_g.genre_id
GROUP BY
    g.genre_id
LIMIT
    15;