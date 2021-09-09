# Plants API

This project is an ApI for plants collection, their biological names and nature. Users are able to create a new plant record, update a plant record, delete a plant by id, or get all avalialble plants. The endpoint to get all plants has options to paginate the response and to search by plant name. If no pagination options are provided, the response defaults to 20 plant records per page. This projects demonstrates my skill in structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## User Guidelines

If you are interested in consuming these endpoints, then endevour to update the frontend to match the endpoints you choose and the programmed behavior.

You should feel free to expand on the project in any way you can dream up to extend your skills. For instance, you could add additional plant information to each entry or create individual plant views including more information about the plant, your personal comments on the nature of the plant.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend (To be added)

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb plantsdb_test
createdb plantsdb_test
psql plantsdb_test < plants.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET /plants

- General:
  - Returns a list of plant objects, success value, and total number of plants
  - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/plants`

```{
  "count": 12,
  "plants": [
    {
      "id": 1,
      "is_poisonous": true,
      "name": "Hydrangea",
      "primary_color": "blue",
      "scientific_name": "Hydrangea macrophylla"
    },
    {
      "id": 2,
      "is_poisonous": true,
      "name": "Oleander",
      "primary_color": "pinik",
      "scientific_name": "Nerium oleander"
    },
    {
      "id": 3,
      "is_poisonous": true,
      "name": "Water Hemlock",
      "primary_color": "white",
      "scientific_name": "Cicuta"
    },
    {
      "id": 4,
      "is_poisonous": false,
      "name": "Bamboo",
      "primary_color": "green",
      "scientific_name": "Bamboosa aridinarifolia"
    },
    {
      "id": 5,
      "is_poisonous": false,
      "name": "Carrot",
      "primary_color": "orange",
      "scientific_name": "Daucas carota"
    },
    {
      "id": 6,
      "is_poisonous": false,
      "name": "Lemon",
      "primary_color": "yellow",
      "scientific_name": "Citrus limonium"
    },
    {
      "id": 7,
      "is_poisonous": true,
      "name": "Foxglove",
      "primary_color": "purple",
      "scientific_name": "Digitalis"
    },
    {
      "id": 8,
      "is_poisonous": true,
      "name": "Lily of the Valley",
      "primary_color": "white",
      "scientific_name": "Convallaria majalis"
    },
    {
      "id": 9,
      "is_poisonous": true,
      "name": "Dieffenbachia",
      "primary_color": "green",
      "scientific_name": "Dieffenbachia seguine"
    },
    {
      "id": 10,
      "is_poisonous": false,
      "name": "Tomato",
      "primary_color": "red",
      "scientific_name": "Lycopersican esculentum"
    },
    {
      "id": 11,
      "is_poisonous": false,
      "name": "Spinach",
      "primary_color": "green",
      "scientific_name": "Lactuca sativa"
    },
    {
      "id": 12,
      "is_poisonous": false,
      "name": "Orange",
      "primary_color": "orange",
      "scientific_name": "Citrus aurantium"
    }
  ],
  "success": true
}
```

#### POST /plants

- General:
  - Creates a new plant using the submitted title, author and rating. Returns the id of the created plant, success value, total plants, and plant list based on current page number to update the frontend.
- `curl http://127.0.0.1:5000/plants?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`

```
{
  "created": 13,
  "plants": [
    {
      "id": 1,
      "is_poisonous": true,
      "name": "Hydrangea",
      "primary_color": "blue",
      "scientific_name": "Hydrangea macrophylla"
    },
    {
      "id": 2,
      "is_poisonous": true,
      "name": "Oleander",
      "primary_color": "pinik",
      "scientific_name": "Nerium oleander"
    },
    {
      "id": 3,
      "is_poisonous": true,
      "name": "Water Hemlock",
      "primary_color": "white",
      "scientific_name": "Cicuta"
    }
  ],
  "success": true,
  "total_plants": 13
}
```

#### DELETE /plants/{plant_id}

- General:
  - Deletes the plant of the given ID if it exists. Returns the id of the deleted plant, success value, total plants, and plant list based on current page number to update the frontend.
- `curl -X DELETE http://127.0.0.1:5000/plants/16?page=2`

```
{
  "deleted": 13,
  "plants": [
    {
      "id": 1,
      "is_poisonous": true,
      "name": "Hydrangea",
      "primary_color": "blue",
      "scientific_name": "Hydrangea macrophylla"
    },
    {
      "id": 2,
      "is_poisonous": true,
      "name": "Oleander",
      "primary_color": "pinik",
      "scientific_name": "Nerium oleander"
    },
    {
      "id": 3,
      "is_poisonous": true,
      "name": "Water Hemlock",
      "primary_color": "white",
      "scientific_name": "Cicuta"
    },
    {
      "id": 4,
      "is_poisonous": false,
      "name": "Bamboo",
      "primary_color": "green",
      "scientific_name": "Bamboosa aridinarifolia"
    },
    {
      "id": 5,
      "is_poisonous": false,
      "name": "Carrot",
      "primary_color": "orange",
      "scientific_name": "Daucas carota"
    },
    {
      "id": 6,
      "is_poisonous": false,
      "name": "Lemon",
      "primary_color": "yellow",
      "scientific_name": "Citrus limonium"
    },
    {
      "id": 7,
      "is_poisonous": true,
      "name": "Foxglove",
      "primary_color": "purple",
      "scientific_name": "Digitalis"
    },
    {
      "id": 8,
      "is_poisonous": true,
      "name": "Lily of the Valley",
      "primary_color": "white",
      "scientific_name": "Convallaria majalis"
    },
    {
      "id": 9,
      "is_poisonous": true,
      "name": "Dieffenbachia",
      "primary_color": "green",
      "scientific_name": "Dieffenbachia seguine"
    },
    {
      "id": 10,
      "is_poisonous": false,
      "name": "Tomato",
      "primary_color": "red",
      "scientific_name": "Lycopersican esculentum"
    },
    {
      "id": 11,
      "is_poisonous": false,
      "name": "Spinach",
      "primary_color": "green",
      "scientific_name": "Lactuca sativa"
    },
    {
      "id": 12,
      "is_poisonous": false,
      "name": "Orange",
      "primary_color": "orange",
      "scientific_name": "Citrus aurantium"
    }
  ],
  "success": true,
  "total_plants": 12
}
```

#### PATCH /plants/{plant_id}

- General:
  - If provided, updates the name of the specified plant. Returns the success value and id of the modified plant.
- `curl http://127.0.0.1:5000/plants/13 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`

```
{
  "id": 13,
  "success": true
}
```

## Deployment N/A

## Authors

Yours truly, Chingsley

## Acknowledgements

The awesome team at Udacity and all Developers extraordinaires!
