Phonebook APIs
--------------

Test from [hackajob.co](https://hackajob.co).

## Requirements
- [Docker](https://www.docker.com/)

## Running it locally - development
```sh 
$ docker-compose up --build api
`````

## Running tests
```sh 
$ docker-compose up --build test
```

## API

### Create one
This method allows you to create phone book entry
```curl
curl -i -X POST 0.0.0.0:8080/entries --user user:pass -d '{"addresses":[{"id":1,"value":"Room67\n14TottenhamCourtRoad\nLondon\nEngland\\W1T1JY"}],"emails":[{"id":1,"value":"john.doe@example.com"}],"first_name":"John","id":1,"last_name":"Doe","phones":[{"id":1,"value":"12345678"},{"id":2,"value":"87654321"}]}'
```

### Get one
This method allows you to select one phone book entry
```curl
curl -i 0.0.0.0:8080/entries/2 --user user:pass
```

### Delete one
This method allows you to delete one phone book entry
```curl
curl -i -X DELETE 0.0.0.0:8080/entries/2 --user user:pass
```