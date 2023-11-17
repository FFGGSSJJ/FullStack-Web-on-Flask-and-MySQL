# Design Descriptions

![uml](../doc/pictures/uml.png)

## Relational Schema

#### Account_info

Account_info (account_id: INT [PK], account_name:  VARCHAR(20), account_pwd: VARCHAR(20), age: INT, account_type: INT, tag: SET(64))

#### Movie_info

Movie_info (movie_id: INT[PK], title: VARCHAR(50), release_time: VARCHAR(20), genre: SET(64), avg_rating: INT, poster_url: VARCHAR(255), IMDB_id: VARCHAR(20), overview: VARCHAR(255))

#### Watch_list

Watch_list (dream_id: INT [PK], account_id: INT [FK to Account_info.account_id], movie_id: INT [FK to Movie_info.movie_id], adding_date Date)

#### Comments

Comments (comment_id: INT [PK], movie_id: INT [FK to Movie_info.movie_id], account_id: INT [FK to Account_info.account_id], comment_date: Date, Message: VARCHAR(255), Rating: INT)

#### Recommendation

Recommendation (recommend_id: INT [PK], movie_id: INT [FK to Movie_info.movie_id], account_id: INT [FK to Account_info.account_id], recommend_date Date)

## Assumptions of the ER/UML diagram
For account information table, we assume that users will enter basic information about themselves while signing up and Account_info table stores information about all registered users. Tag is a set format column field which we will use to get recommendation movie lists.  

We assume that for every account, we have a watch list which user can add several dream movie entries. This table contains specific ID for every records and also adding date. One account can have multiple movies which users would like to watch in the Watch list and one entry in the list corresponding to one account.

Besides, we assume that for one user(one account), he/she can add multiple comments for one movie or several movies. Every single comment will be a seperate record which contains information of comment_date, leaving message and rating score. And we also assume that each comment will link to exactly one movie in our movie database.

We assume that to achieve recommendation function, we have our recommendation entity, one user can get several recommendations from our system and each recommendation record contains one movie, the recommendation table also contains specific ID and the Date of recommendation.  

Last but not the least, for Movie_info table, which contains the most of information of our movie database, we assume that recommendation and watch list entity will both get information from movie info table and one entry in those two tables is related to one movie in Movie_info table. We assume that we can get release_time, genres, avg_rating which is the average score from all rating records, poster_url which we can show it on our website, and overview.

## Description of each relationship and its cardinality 

#### contain

It is the relation between ***Account Info*** and ***Watch List***. For each user, he/she can have multiple watch lists that record movies that he/she want to watch and hence each account should contain multile watch list(s).

#### get_info1

It is the relation between ***Watch List*** and ***Movie Info***. For all movie in the ***Watch List***, users can query the detailed information about this specific movie and only one movie info can be queried since movie is unique. Hence, there exists a query relation.

#### get_info2

It is the relation between ***Recommendation*** and ***Movie Info***. For movie that is recommended by each recommendation, user can also query the details about this moive through the movie id. Hence, there exists a query relation.

#### link

It is the relation between ***Movie Info*** and ***Comments***. For the movie that is commented by a user, this comment should be correlated to a movie that is specified by the unique movie id. Hence, a link will exist between these two entities.

#### get_recommendation

It is the relation between ***Account*** and ***Recommendation***. For each account, it will get multiple recommendations from the system and hence the relation is many to one.

#### add_comment

It is the relation between ***Account*** and ***Comments***. For each account, the user can add comments to movies that is specified by the movie id and each user can add multiple comments to one same movie. Hence, the relation add_comment exists and should be one to many.





