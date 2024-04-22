## OnSiteIQ Django API

### Run tests
Run the sanity checks, including 
- Black formatting
- flake8 linting
- mypy type checking
- unit tests
with the test profile
```
docker-compose up test
```

### Run app
Run the app with no profile specified
```commandline
docker-compose up -d
```

### Existing users
Created with a management command as part of the docker build

| Username    | Password    | Permissions                             |
|-------------|-------------|-----------------------------------------|
| admin       | admin       | create, approve, reject, view, add_note |
| adjudicator | adjudicator | approve, reject, view, add_note         |
| contributor | contributor | view, add_note                          |
| viewer      | contributor | view                                    |


### Authenticate with a User with
##### Request
```
POST localhost:8654/authenticate/login/
{
  "username": <username>,
  "password": <password>
}
```
##### Response
```
{
    "token": <token>
}
```

### Interact with applicants
The following endpoints use TokenAuthentication, so the header
```
Authorization: Token <token>
```
will need to be added using the token from the authentication/login/ response

#### Create applicant
##### Request
```
POST localhost:8654/applicants/
{
    "first_name": <first_name>, // required, less than 50 chars
    "last_name": <last_name>, // required, less than 50 chars
    "email": <email>, // required, valid email
}
```
##### Response
```
{
    "applicant_id": <applicant_id>
}
```

#### View applicant
#### Request
```
GET localhost:8654/applicants/<applicant_id>/
```
#### Response
```
{
    "first_name": <first_name>,
    "last_name": <last_name>,
    "email": <email>,
    "status": <Pending|Approved|Rejected>,
    "notes": [...{
        "text": <note_text>,
        "created_by": <username>,
        "created_at": <time>
    }]
}
```

### Approve applicant
#### Request
```
POST localhost:8654/applicants/<applicant_id>/approve/
```

### Reject applicant
#### Request
```
POST localhost:8654/applicants/<applicant_id>/reject/
```

### Add applicant note
#### Request
```
POST localhost:8654/applicants/<applicant_id>/notes/
{
    "text": <note_text>" //required, no blank allowed
}
```
