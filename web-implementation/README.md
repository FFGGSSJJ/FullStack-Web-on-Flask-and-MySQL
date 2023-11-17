### Title

**uMovies**

### Demo Video
<iframe width="560" height="315" src="https://mediaspace.illinois.edu/media/t/1_ubn4nkhy" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Summary

In this project, we aim to create a platform where Movie lovers can easily find movies they like. It is an online database of information mainly related to films, including 45000 movie lists and almost cover all varieties of film genres. Based on user features, eligible films movies will be recommended to them automatically by our system and we also provide them with watchlist to record what they want to watch. If users click on the results of movies searching, they can see basic information of movies, including movie posters, rating information, genres, releasing data and so on.

Our platform also provide a friendly communication environment and relatively fair rating system for movie lovers. Users can exchange their thoughts toward movies freely and other users can see it. Users can write comments, those comments will be saved in our database and users can also find their old comments. 

### Requirements

```
python >= 3.7
```

### Getting started
```bash
git clone https://github.com/FFGGSSJJ/CS411-team033.git
cd CS411-team033/Project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP = app
flask run
```

### Setting up GCP
Create a `app.yaml` file in the root folder with the following content:
```yaml
runtime: python37 # or another supported version

instance_class: F1

env_variables:
  MYSQL_USER: <user_name> # please put in your credentials
  MYSQL_PASSWORD: <user_pw> # please put in your credentials
  MYSQL_DB: <database_name> # please put in your credentials
  MYSQL_HOST: <database_ip> # please put in your credentials

handlers:
# Matches requests to /images/... to files in static/images/...
- url: /img
  static_dir: static/img

- url: /script
  static_dir: static/script

- url: /styles
  static_dir: static/styles
```

### Setting up the deployment

```bash
curl https://sdk.cloud.google.com | bash
gcloud components install app-engine-python
gcloud config set project cs411-su22
gcloud auth login
gcloud app deploy
```

### For my teammates

*Thank you all for your hardwork with such excellent result.* 
