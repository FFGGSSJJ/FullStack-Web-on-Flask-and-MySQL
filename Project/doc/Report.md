# Project Report

- **team033-Key of Sky**
- Guanshujie Fu (gf9)
- Haina Lou (hainal2)
- Keyi Shen (keyis2)
- Xiaomin Qiu (xchou2)


## Title

**uMovies**

## framework
1. Introdution
- intro of our project. briefly talk what we do / not do in final version
- functionalities
2. Project Stages (and changes from the proposal in detail)
- data processing 
- database design (ER dirgram...) 
- database implementation
- advanced database programs (trigger, procedure, indexing)
- frontend design and implementation
- creative component
3. technical challenge
4. future work
5. final division of labor

## I. Introduction
In this project, we aim to create a platform where Movie lovers can easily find movies they like. It is an online database of information mainly related to films, including 45000 movie lists and almost cover all varieties of film genres. Based on user features, eligible films movies will be recommended to them automatically by our recommendation system and we also provide them with watchlist to record what they want to watch. If users click on the results of movies searching, they can see basic information of movies, including movie posters, rating information, overview, releasing data and so on.
## II. Project Stages
This section describes our work, application functionality, changes from the proposal in detail.
### 1. Data processing
We choose a movie dataset on [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download) as the source of data. In the proposal, we planned to base the database entirely on real data, but during the design process we found that the real data was too large and missing real user information, so we made the necessary adjustments to the data information based on the ER diagram. To make our design simpler and clearer, we added some new attributes, such as comments, account_info, tags, and dropped some unnecessary key attributes in the proposal, such as cast, crew, plot keywords, budget, revenue, etc. The dataset contains 26 million ratings from 270,000 users for all 45,000 movies so we drop some of datat with null value, and finally only fliter 7k+ movies and relative ratings. Of course, other extra operations are need to fit the database design. For example, we need to decompose the original dataset into different tables and do some transitions on data. (like convert timestamp to readable time) In this part, we use Pandas library to process data and generate the data randomly in account_info and watch_list tables to meet the requirements in the ER diagram.

### 2. Database design
In our project, we design a database with four tables: movie_info(describe basic information of movies stored in our database), account_info(user profile inserted when user register up), comments(showing users' comments toward movie and containing rating information used to compute ratings about the movie), watch_list(information of users' recent movies which they want to watch) genre(genre name with corresponding genre id) and movie_genre(movie id with corresponding genre id).

In the original design of ER diagram, we have five tables: account_info, comments, watch_list, movie_info and recommendation. However, the recommendation table is more like a relation and should be generated based on different conditions of users. Therefore, we did not create table at the beginning but generate tables in our stored procedure which I will describe later. In addition, we add tables about the information of genres, which can be used to create genre filter to help search movies in the search interface. And also when deciding what information needs to be included in the table, I remove columns like imdb_id in raw data for the sake of little practical use which is different with original design. Besides, in our original design, we can know the rating of one movie directly. However, the raw data does not provide that, it just has all users' ratings toward one movie. Therefore, to accomplish the functionality of showing movies' rating, we write advanced query to generate ratings for every movie in our database. Other tables all remain the same as our original design.
### 3. Database implementation & Advanced database programs
To implement a more advanced database program, we use a stored procedure and trigger to our database.  

**Stored procedure**

Stored procedure is used to generate a table which provides data for recommendation system and contains all other similar users' movies information in their watch list. The similarity is ensured by searching all other users in our database in account_info table, which have same tags information as the user which is now logged in. In this way, we can find all similar users movie preference which can be used to compute Euclidean distance later. In order to search all the rows of account_info table to find users with 3 same tags, I use cursors to fetch three tags and if it meets the requirement, the average rating, movie_id, userID information for that user will be inserted into our newly created recommendation table. Besides, I also use advanced query to add movies in current user's watch list into our recommend table. 

 
**Trigger**

Considering practical use, We use trigger to remind users to use passwords longer than 5 characters and think up unique account names in our database when user is registering up, because longer passwords are safer and unique account name can help prevent fraud in the real world. Before register up successfully, we will use trigger to check if account_name and password meet our requirements. If not, trigger will update the id to negative. Then our system will check it and delete negative account telling the user registration is failed and ask him to use different account name and longer passwords. 
### 5. Frontend design and implementation
We designed innovative and comprehensive frontend interfaces for our application. 

Starting from the initial pages, we provide both login and register interfaces. With the use of jquery and javascript, we directly lead the user to the home page after he/her registers or logs in successfully.

The homepage is especially designed with mainly 2 sections. The recommendation section will show the movies recommended based on the system and the ranking section shows the movies with high ratings. The movie item is also specially designed with css framework which contains the poster image as background and movie title appears with cursor moves onto it. We also provide comprehensive navigation and menu bars on all the pages which makes the interaction direct. 

The user page will provide the information of the user that he/her entered at registration. It contains user name, user id and prefered genres. Root user can link from this page to root operation interface.

The search page provide two methods for searching, the name search and genre filter. This page is designed with only one search button and it will link to the search result page that lists movie items. User can check each movie items by clicking on the item directly that will jump to the movie introduction page.

### 6. Creative component
One of the creative components in our design is the recommender system, it combines the stored procedure and the User based collaborative filtering recommendation system which can provides the user with personalized Recommendations.

The design has three steps to Improve recommendation quality. First, as we mentioned before, we use the stored procedure to Find the users with the same tags as the new users.  This step not only reduce the size of the training data, but also increase the accuracy. Then we use the Euclidean distance of the ratings in the watch list to describe the similarities between the users. Through this way, we select 10 most similar users. The last step is to select 10 movies with the highest ratings in the watchlist of the 10 similar users. Also, we need to make sure the recommend movies have not been watched by the new user. 

Compared with the recommender system in proposal, the final application is more accurate and personalized. It not only applies the stored procedure to find similar users based on the preference tags entered by the user during registration, but also used machine learning algorithms to further improve accuracy and narrow the selection range, which provides users with more personalized recommendations.

## III.Technical Challenges
#### 1. Timeliness of data.
   - The dataset we use is an ensemble of data collected from TMDb and GroupLens and The consists of movies released on or before July 2017 according to the description of the dataset. In most cases, this is not a problem. But it gives the poster paths of movies, so we want to access them and display the posters on our website. All of the poster paths are offered by TMDb API and should be valid. 
   - However, we find that most of them are invaild when we try. Finally, we find that there are some updates after the release date of the dataset so poster paths may be outdated. In this case, we use the TMDb API by ourselves to fetch the latest poster paths. It is an unexpected work but a meaningful attempt. We find that TMDb API provides us with a rich source of data beyond the dataset we use.

#### 2. Uncertainty of Data
   - Due to the stochasticity of real user data, we cannot guarantee that all users have filled in certain attributes that need to be used by the recommender system. Therefore, we need to apply different kinds of recommender methods for users with different types of missing information, which greatly increases the complexity of the system. We should discuss possible anomalies in user data more carefully at the beginning and adjust the algorithm design according to this to reduce the testing and debugging time.

#### 3. Webpage render performance

- As our home page will call the recommendation system implemented in our backend side, we notice that this will lead to long render time. This is caused by the poster path that we used to grab the poster image. As the database we utilizes is out of date, most of the post path is invlaid and hence we need to use python script to find the new path which might cost some time to render.

   
#### 4. Long stored procedure running time 
   - The biggest technical challenge I encounter in this database implementation is the long waiting time for running stored procedure once in my database. I need 8 seconds to generate the recommendation table which means after user register up in our system, he needs to wait 8s to see the personal homepage which contains the recommendation movie result. To try to improve the performance, I add indexing to tags(the searching conditions) and it improves a little. In the future, we might try to figure out how to improve the performance of our advanced database program by adding efficient indexing and changing our logic in the stored procedure.
   
## IV. Future Work
#### 1. Explore more data.
   - During fetching the poster paths, we find much other data can be used as the cornerstone to extend the features of our application. For example, TMDb API offers data on actors and actresses, crew members. So we can display the relative members of movies on website and search movies by the members. Also, more interesting ranking list can be created.
#### 2. Try NoSQL.
   - Since NoSQL is more flexible and extendable than relational database and can easily scale across multiple servers. We can try to add and modify more attributes and distribute data on different servers to be close to the practical situation. 
   - Further, we can even use graph database when we want to add following/followed-by features for users into our application. For example, with graph database, we can easily explore the paths of following relation with no more than 3 or 5 hops. It’s also beneficial to advanced recommendation. Also, we can analyse the relationships between actors, actresses and crew members as what we do in the homework.

#### 3. Improve the Quality of Ratings.
   - We could combine the Bayesian classification algorithm and the idea of weighted average to improve the quality of movie ratings.
   - In our design we used the average of all user ratings as the final score of the movie and developed the ranking based on this data. However, there is a problem with average scores, which cannot directly define a movie as good or bad if only one or very few people rate it.
   - Therefore, to avoid malicious scoring, we can use the concept of absolute number of votes to dilute the bias of only a few people scoring. For movies with small audiences such as literary films, we can add the average score of all movies as one of the factors to be considered in order to avoid the absolute number of votes pulling down the rating. This will make our overall rating of movies more scientific and provide more effective data for the recommender system.

## V. Division of Labor
We basically follow the division of labor in our proposal. Haina and Xiaomin do the backend work and Guanshujie and Keyi do the frondend work.

Specifically, Keyi fetch and clean the original data. Xiaomin genreates some random data based on the processed data. Haina designs and implements the database on GCP. Haina and Xiaomin develop the advanced database programs including trigger and stored procedures together. Guanshujie designs and implements all of the web pages. And Keyi helps Guanshujie to build the interface between HTML and MySQL.

Everything goes well in our project, even if we are in three different time zones and are busy with different things at the end of semester. We think that it is important to have a clear timeline and work distribution at the beginning of the project. During the project, the communication between teammates is necessary. Even if we are different time zones, we keep in touch via Zoom meeting everyday when we do the Stage 5 and 6. Besides, we are all enthusiastic and are with strong ability so that we can solve problems together and adjust the work distribution flexibly.

## Topics (copied from course web)
1. Please list out changes in your project directions if the final project is different from your original proposal (based on your stage 1 proposal submission).
2. Discuss what you think your application achieved or failed to achieve regarding its usefulness.
3. Discuss if you changed the schema or source of the data for your application
4. Discuss what you change to your ER diagram and/or your table implementations. What are some differences between the original design and the final design? Why? What do you think is a more suitable design? 
5. Discuss what functionalities you added or removed. Why?
6. Explain how you think your advanced database programs complement your application.
7. Each team member should describe one technical challenge that the team encountered.  This should be sufficiently detailed such that another future team could use this as helpful advice if they were to start a similar project or where to maintain your project. 
8. Are there other things that changed comparing the final application with the original proposal?
9. Describe future work that you think, other than the interface, that the application can improve on
10. Describe the final division of labor and how well you managed teamwork. 

## Rubric (copied from course web)
This stage is worth 10%. You are graded by completeness and correctness. The rubric is as follows:

1. Each missing section of the report (-1%), if there are no changes or nothing to discuss, state it.
The report is not well-written or does not provide enough details (-4%)
 2. Missing video (-2%)
Too short, too long video (-1%)
The video does not provide a comprehensive overview of the application (-2%)
3. The report should be placed in the doc folder. The doc folder should also contain a readme file containing the link to the video. (-1% if missing either component in the folder)
4. You should tag your release. Failure to tag your release will result in a 1% deduction.
5. Failure to submit your CATME survey will result in a 1% deduction from the stage.
