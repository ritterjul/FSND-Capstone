# Swim Results

## Motivation

This API provides an interface for accessing results of swimming meets.

## Local Development

Developers should have Python3, pip3 and Heroku CLI installed. 

### Backend Dependencies 

Once you have a Python virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

### Testing

Once you have the Python virtual environment configured you can test that the application is behaving as expected by running: 

```bash
sh run_tests.sh
```

Note that you have to adapt the DATABASE_URL in run_tests.sh to your local settings.

### Running the server

Once you have the Python virtual environment configurated and the Heroku CLI connected to your account you can deploy the app on Heroku by:
- creating a Heroku app which returns a heroku_git_url
- Initializing a Git repository and connecting to Heroku
- Adding a postgresql addon to the Heroku app
- Staging, commiting and pushing your changes
- Running the database migrations

```bash
heroku create <app_name>
git init
git remote add heroku <heroku_git_url>
heroku addons:create heroku-postgresql:hobby-dev --app <app_name>
git add ...
git commit ...
git push heroku master
heroku run python manage.py db upgrade --app <app_name>
```

## API Reference

### Base URL
The backend is hosted at https://swimresults.herokuapp.com/

### Authentication
The API requires authentication for all endpoints except the landing page.
There are three different roles with different permissions:
- Swimmer: A person that swims at meets
- Coach: A person that coaches swimmers
- Official: A person that organizes swim meets

#### Swimmer role
Dummy user:
- e-mail: swimmer@swimresults.com
- password: Swimmer1

A swimmer has the permissions to
- Get all swimmers/meets
- Get details for swimmers/meets
- Get results (for swimmers/meets)

#### Coach role
Dummy user:
- e-mail: coach@swimresults.com
- password: CoachCoach1

A coach has all the permissions a swimmer has and additionaly to
- Create a new swimmer
- Edit details for a swimmer
- Delete a swimmer

#### Official role
Dummy user:
- e-mail: official@swimresults.com
- password: Official1

An official has all the permissions a swimmer has and additionaly to
- Create a new meet
- Edit details for a meet
- Delete a meet

### Error Handling

There are four types of errors the API will return:
- 400 - bad request
- 401 - unauthorized
- 403 - forbidden
- 404 - resource not found
- 405 - method not allowed

### Endpoints

#### GET '/swimmers'
- Fetches a list of all swimmers.
- Request: 
    - Authorization header with permission 'get:swimmers'.
- Response: 
    - JSON object with a key swimmers, that contains a list where every element is a dictionary with keys "id", "gender", "first name", "last name" and "year of birth".
- Sample response:
```
{
    "success": true,
    "swimmers": [
        {
            "first name": "Juliane",
            "gender": "F",
            "id": 155849,
            "last name": "Ritter",
            "year of birth": 1994
        },
        {
            "first name": "Stefanie",
            "gender": "F",
            "id": 155848,
            "last name": "Kitschke",
            "year of birth": 1994
        }
    ]
}
```

#### POST '/swimmers'
- Creates a new swimmer.
- Request: 
    - Authorization header with permission 'create:swimmer'. 
    - JSON object with keys "gender" (one of "F', "M", "X"), "first name" (string), "last name" (string), "year of birth" (integer) and optionally "id" (integer, must not yet exist as id in database!).
- Returns: 
    - JSON object with a key "id", whose value is the id of the created swimmer.
- Sample response:
```
{
    "success": true,
    "id": 2
}
```

#### GET '/swimmer/<int:swimmer_id>'
- Fetches details of a swimmer specified by swimmer_id.
- Request: 
    - Authorization header with permission 'get:swimmer-details'.
- Response: 
    - JSON object with a key swimmer, that contains a dictionary with keys "id", "gender", "first name", "last name" and "year of birth".
- Sample response:
```
{
    "success": true,
    "swimmer": {
        "first name": "Juliane",
        "gender": "F",
        "id": 155849,
        "last name": "Ritter",
        "year of birth": 1994
    }
}
```

#### GET '/swimmer/<int:swimmer_id>/results'
- Fetches results of a swimmer specified by swimmer_id.
- Request: 
    - Authorization header with permission 'get:swimmer-results'.
- Response: 
    - JSON object with a key results, that contains a list where every element is a dictionary with keys "id", "swimmer_id", "meet_id", "course", "distance", "stroke", "time".
- Sample response:
```
{
    "results": [
        {
            "course": "LCM",
            "distance": 50,
            "id": 1,
            "meet_id": 1,
            "stroke": "Free",
            "swimmer id": 155849,
            "time": "0:45.68"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 2,
            "meet_id": 1,
            "stroke": "Breast",
            "swimmer id": 155849,
            "time": "0:50.25"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 3,
            "meet_id": 1,
            "stroke": "Back",
            "swimmer id": 155849,
            "time": "0:48.41"
        }
    ],
    "success": true
}
```

#### PATCH '/swimmer/<int:swimmer_id>'
- Edits details of a swimmer specified by swimmer_id.
- Request: 
    - Authorization header with permission 'edit:swimmer'.
    - JSON object with any of the keys "gender" (one of "F', "M", "X"), "first name" (string), "last name" (string), "year of birth" (integer).
- Response: 
    - JSON object with a key swimmer, that contains a dictionary with keys "id", "gender", "first name", "last name" and "year of birth".
- Sample response:
```
{
    "success": true,
    "swimmer": {
        "first name": "Juliane",
        "gender": "F",
        "id": 155849,
        "last name": "Ritter",
        "year of birth": 1994
    }
}
```

#### DELETE '/swimmer/<int:swimmer_id>'
- Deletes a swimmer specified by swimmer_id.
- Request: 
    - Authorization header with permission 'delete:swimmer'.
- Response: 
    - JSON object with a key "id", whose value is the id of the deleted swimmer.
- Sample response:
```
{
    "success": true,
    "id": 2
}
```

#### GET '/meets'
- Fetches a list of all meets.
- Request: 
    - Authorization header with permission 'get:meets'.
- Response: 
    - JSON object with a key meets, that contains a list where every element is a dictionary with keys "id", "name", "start date", "end date", "city" and "country".
- Sample response:
```
{
    "meets": [
        {
            "city": "Berlin",
            "country": "Germany",
            "end date": "Sun, 06 Apr 2003 00:00:00 GMT",
            "id": 1,
            "name": "7. Volvo Lochner Cup",
            "start date": "Sun, 06 Apr 2003 00:00:00 GMT"
        },
        {
            "city": "Berlin",
            "country": "Germany",
            "end date": "Thu, 05 Feb 2004 00:00:00 GMT",
            "id": 2,
            "name": "8. Volvo-Lochner-Cup",
            "start date": "Thu, 05 Feb 2004 00:00:00 GMT"
        }
    ],
    "success": true
}
```

#### POST '/meets'
- Creates a new meet.
- Request: 
    - Authorization header with permission 'create:meet'. 
    - JSON object with keys "name" (string), "start date" (date), "end date" (date), "city" (string) and "country" (string).
- Returns: 
    - JSON object with a key "id", whose value is the id of the created meet.
- Sample response:
```
{
    "success": true,
    "id": 2
}
```

#### GET '/meet/<int:meet_id>'
- Fetches details of a meet specified by meet_id.
- Request: 
    - Authorization header with permission 'get:meet-details'.
- Response: 
    - JSON object with a key meet, that contains a dictionary with keys "id", "name", "start date", "end date", "city" and "country".
- Sample response:
```
{
    "meet": {
        "city": "Berlin",
        "country": "Germany",
        "end date": "Sun, 06 Apr 2003 00:00:00 GMT",
        "id": 1,
        "name": "7. Volvo Lochner Cup",
        "start date": "Sun, 06 Apr 2003 00:00:00 GMT"
    },
    "success": true
}
```

#### GET '/meet/<int:meet_id>/results'
- Fetches results of a meet specified by meet_id.
- Request: 
    - Authorization header with permission 'get:meet-results'.
- Response: 
    - JSON object with a key results, that contains a list where every element is a dictionary with keys "id", "swimmer_id", "meet_id", "course", "distance", "stroke", "time".
- Sample response:
```
{
    "results": [
        {
            "course": "LCM",
            "distance": 50,
            "id": 1,
            "meet_id": 1,
            "stroke": "Free",
            "swimmer id": 155849,
            "time": "0:45.68"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 2,
            "meet_id": 1,
            "stroke": "Breast",
            "swimmer id": 155849,
            "time": "0:50.25"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 3,
            "meet_id": 1,
            "stroke": "Back",
            "swimmer id": 155849,
            "time": "0:48.41"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 4,
            "meet_id": 1,
            "stroke": "Back",
            "swimmer id": 155848,
            "time": "0:47.50"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 5,
            "meet_id": 1,
            "stroke": "Breast",
            "swimmer id": 155848,
            "time": "0:54.56"
        },
        {
            "course": "LCM",
            "distance": 50,
            "id": 6,
            "meet_id": 1,
            "stroke": "Free",
            "swimmer id": 155848,
            "time": "0:45.59"
        }
    ],
    "success": true
}
```

#### PATCH '/meet/<int:meet_id>'
- Edits details of a meet specified by meet_id.
- Request: 
    - Authorization header with permission 'edit:meet'.
    - JSON object with any of the keys "name" (string), "start date" (date), "end date" (date), "city" (string) and "country" (string).
- Response: 
    - JSON object with a key meet, that contains a dictionary with keys "name" (string), "start date" (date), "end date" (date), "city" (string) and "country" (string).
- Sample response:
```
{
    "meet": {
        "city": "Berlin",
        "country": "Germany",
        "end date": "Sun, 06 Apr 2003 00:00:00 GMT",
        "id": 1,
        "name": "7. Volvo Lochner Cup",
        "start date": "Sun, 06 Apr 2003 00:00:00 GMT"
    },
    "success": true
}
```

#### DELETE '/meet/<int:meet_id>'
- Deletes a meet specified by meet_id.
- Request: 
    - Authorization header with permission 'delete:meet'.
- Response: 
    - JSON object with a key "id", whose value is the id of the deleted meet.
- Sample response:
```
{
    "success": true,
    "id": 2
}
```



