## Plan B Backend

If our ERP dude doesn't finish th1 1C-based backend version, we'll use this FastAPI-based version.

## API 

### Registration 

Routing: /user/register <br>
Request type: POST <br><br>

Example request: 

```
{
	"login": "ivanov_ivan",
	"password": "password"
}
```

Exemple responses <br>

If everything is fine: 

```
{
	"status": 200,
	"token": "DNX0WfPEhlxi...",
	"description": "You have been successfully registered"
}
```


If user's name is already in use: 

```
{
  "status": 221,
  "description": "There is already a user with such name!"
}
```

### Authorization 


Routing: /user/auth <br>
Request type: POST <br>

Example request: 

```
{
	"login": "ivanov",
	"password": "ivan"
}
```


Example responses. 

If everything is fine:

```
{
	"status": 200,
	"token": "dQ4osHiTU1D8kLe...",
	"description": "You have been authorized!"
}
```


If user's password or login is incorrect 

```
{
    "status": 403,
    "description": "Access denied!"
}
```

### Data download 

Routing: /data/synch/download <br> 
Request type: POST

Example request: 

```
{
    "token": "DNX0WfPEhlxiEWVtcuvp..."
}
```


Example responses: 

If everything is fine

```
{
	"status": 200,
	"data": [
		"{'login': 'login'}"
	],
	"description": "Here's your data"
}
```

If token is incorrect: 

```
{
    "status": 403,
    "description": "Access denied!"
}
```

### Data Upload

Routing: /data/synch/upload <br>
Request type: POST <br>

Example request: 

```
{
"token": "DNX0WfPEhlxiEWVtcuvpVCXv7baHgvlCc8TppfTDclnjzgLas6KnhnKpedNsSOJfTW8Kaa4aAaMzoAFoQlwjB9HXbx6tu7TmkzW23lZbAu1LizNfhdc1GhdskqsR0cz9rwDiigJv4sSAtFeum7sN4suVRv1CBa1E1z0BF4q6w0BGOAw6aAQBc8JDiEtC1Pi6rS9JMtCtZvco9jUeCGC2wSH4APvqwROrM6PnCdALwutkpDVGFzmaQcm3x7AH6y",
"data": {"login": "login"}
}
```

Example responses: 

If everything is fine

```
{
	"status": 200,
	"description": "The data has been updated!"
}
```


If token is incorrect 

```
{
    "status": 403,
     "description": "Access denied!"
}
```
