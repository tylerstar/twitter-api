# Twitter APIs
[![Build Status](https://travis-ci.com/tylerstar/twitter-api.svg?branch=master)](https://travis-ci.com/tylerstar/twitter-api)


A web server powered by Django that help you to fetch tweets via Twitter APIs.

## Description

This project include two APIs.

1. Fetch recent tweets by a hashtag
   
    Example request:
    ```curl -H "Accept: application/json" -X GET http://localhost:xxxx/hashtags/Python?limit=40```
    
    Example response:
    ```
    [{"account": {"fullname": "Raymond Hettinger",
                  "href": "/raymondh",
                  "id": 14159138},
      "date": "12:57 PM - 7 Mar 2018",
      "hashtags": ["#python"],
      "likes": 169,
      "replies": 13,
      "retweets": 27,
      "text": "Historically, bash filename pattern matching was known
               as \"globbing\".  Hence, the #python module
               called \"glob\".\n\n
               >>> print(glob.glob('*.py')\n\n
               If the function were being added today, it would probably
               be called os.path.expand_wildcards('*.py') which would be
               less arcane."},
      ...
    ]
    ```
   
2. Fetch user's recent tweets by twitter user's [screen_name](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/overview/user-object#:~:text=In%20case%20of%20Retweets%20and,using%20the%20id%20or%20screen_name%20.)

    Example request:
    ```curl -H "Accept: application/json" -X GET http://localhost:xxxx/users/twitter?limit=20```

    Example response:
    ```
    [{"account": {"fullname": "Twitter",
                  "href": "/Twitter",
                  "id": 783214},
      "date": "2:54 PM - 8 Mar 2018",
      "hashtags": ["#InternationalWomensDay"],
      "likes": 287,
      "replies": 17,
      "retweets": 70,
      "text": "Powerful voices. Inspiring women.\n\n#InternationalWomensDay
               https://twitter.com/i/moments/971870564246634496"},
       ...
    ] 
    ```
    
## Preview the APIs

A demo has been deployed, you can explorer this app through urls below:

1. Fetch tweets by hashtag `Python` and `limit=2`: 

    ```https://6078pizoxf.execute-api.ap-southeast-1.amazonaws.com/dev/hashtags/python?limit=2```

2. Fetch tweets by user `twitter` and return 30 tweets by default: 

    ```https://6078pizoxf.execute-api.ap-southeast-1.amazonaws.com/dev/users/twitter```

## Getting Started

### Dependencies

* Python version >= 3.6
* Twitter developer API key
* Unix/Linux OS

### Installing

1. Download the git repository
   
   ```git clone git@github.com:tylerstar/twitter-api.git```
   
2. Build the image
   
   ```cd twitter_api && docker-compose build```
   
### Configuration

Ensure to set the Twitter Developer API Bearer Token before running the program.
You can alter it in docker-compose.yml if you run the app via docker-compose

```TWITTER_TOKEN={YOUR TWITTER BEARER TOKEN}```

### Executing program

1. After downloading the repository and build the image, run the command 
(ensure the port 8000 has not been used or you can change the config inside the `docker-compose.yml`)

   ```docker-compose up```
   
2. You can also run the service through pre-built docker image from Docker Hub
   ```bash
   docker pull balyon/twitterapi
   ```

   ```bash
   docker run \
      -it \
      --rm  \
      -e TWITTER_TOKEN={YOUR TWITTER TOKEN} \
      -e DEBUG=True \
      -p 8000:8000 \
      balyon/twitterapi \
      python manage.py runserver 0.0.0.0:8000 
   ```
   
### Running tests

* This project has configured Travis CI, you can view the details through [build page](https://travis-ci.com/github/tylerstar/twitter-api)
* If you want to run the test locally, after you downloading the project and installed the dependencies, 
you can run command below to run the test

    ```cd twitterapi && python manage.py test && flake8```
   
### Deployment

* Ensure to set the environment `DEBUG=True` before deployment.

## Authors

[@tylerstar](https://github.com/tylerstar)

## Version History

* 0.1
    * Initial Release
