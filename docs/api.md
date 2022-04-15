# INCOMPLETE DOCS, DO NOT EXPECT THIS TOO WORK

# Using the Papertrade API

## Ease of use for those getting started
The papertrade API is a smart, intuitive RESTful API built with Flask. Traders can create, login, buy, sell, and manage their portfolios all using simple requests, a great way for people just getting started with APIs or programming to learn

## Built by developers, for developers
While easy to use, the papertrade API is also extremely powerful and gives developers the tool to build complex trading bots with just a few lines of code


# Quick Start

## Registering an account
**Example Request:**
```
POST api.com/register {email: 'johnsmith@gmail.com', username: 'JohnSmith', startingcash: 10000, password: '12345'}
```

**Example Response:**

```
{
    "message": "Successfully created user johnsmith with starting cash of 1000000"
}
```

**HTTP Method:** `POST`

**URL:** `api.com/register`

**Required Arguments:** `None`

**Headers:** *(red denotes required header)*

```diff
{
-  email: string,
- username: string,
+ displayname: string,
- startingcash: float,
- password: string,
}
```

## Logging in and getting a token
**Example Request:**
```
POST api.com/login {username: 'JohnSmith', password: '12345'}
```

**Example Response:**
```
{
	"token": 'hJSJKDGhsudoghdsuighsIUDGHSUIDGhSUDIGhsiuh31257089HSG'
}
```
    
**HTTP Method:** `POST`

**URL:** `api.com/login`

**Required Arguments:** `None`

**Headers:** *(red denotes required header)*

```diff
{
- username: string,
- password: string,
}
```

