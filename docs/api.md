#INCOMPLETE DOCS, DO NOT EXPECT THIS TOO WORK

#Using the Papertrade API

##Ease of use for those getting started
The papertrade API is a smart, intuiive RESTful API built with Flask. Traders can create, login, buy, sell, and manage their portfolios all using simple requests, a great way for people just getting started with APIs or programming

##Built by developers, for developers
While easy to use, the papertrade API is also extremely powerful and gives developers the tool to build complex trading bots with just a few lines of code


##Quick Start

#Registering an account
```
HTTP Method: POST
URL: api.com/register
Headers: {
  email: email,
  username: username,
  startingcash: startingcash,
  password: password
}
```

Response:
```
{
    "message": "Succesfully created user tanujks with starting cash of 1000000"
}
```
#Logging in and ret
