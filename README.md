# Tech documentation

A project to attempt to create a solid tool for documenting code internally for tech companies.

## Running the application

Both frontend and backend need to run simultaneously

#### Running the backend server

```bash
make backend
```

#### Running the frontend server

```bash
make frontend
```

#### Launching the Database

MongoDB is used. To install follow the steps [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/).

Using brew, all you need to do is run:
```bash
brew tap mongodb/brew
brew install mongodb-community@4.0
```

Then to run the database:

```bash
make db
```

To setup the database and insert data, run 

```bash
make db_setup
```

To see the documents in the document collection, run

```bash
make db_show
```

To clean the database document collection, run

```bash
make db_clean
```

#### Check out the app

Visit http://localhost:8080/

## Development

### Saving python resources 

```bash
pip freeze > backend/requirements.txt
```

### Installing python resources

```bash
pip install -r backend/requirements.txt
```

## Miscallaneous 

### Tech and library used

* pyGithub
