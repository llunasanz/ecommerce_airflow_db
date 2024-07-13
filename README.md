# ecommerce_airflow_db
A data pipeline for information gathering and saving using Apache Airflow.

## Tasks overview

This project gathers information about items published on an ecommerce site, saves it in a database, and launches alerts if established criteria are met. The pipeline is implemented using Airflow and runs daily.

The pipeline interacts with the public API to collect data. Here are some useful links:
- [List of categories](https://api.mercadolibre.com/sites/MLA/categories)
- [Specific category information](https://api.mercadolibre.com/categories/MLA1577)
- [Search API for a given category](https://api.mercadolibre.com/sites/MLA/search?category=MLA1577#json)
    - `curl -i -H "Accept: application/json" "https://api.mercadolibre.com/sites/MLA/search?category=MLA1577#json"`
- [Specific item information](https://api.mercadolibre.com/items/MLA830173972)

### Data pipeline creation
The goal is to retrieve the 50 most relevant published items for the category "MLA-MICROWAVES" (category id MLA1577) from Mercadolibre. For each item, the following information is gathered:
- "id"
- "site\_id"
- "title"
- "price"
- "sold\_quantity"
- "thumbnail"

This data is stored in a database with an additional field "created\_date". The pipeline is implemented using an Airflow DAG.

### Alert system
An alert is sent via email if any item has earned more than $7,000,000 (price x sold\_quantity) during the data gathering task. The email contains all the gathered data for each qualifying item.

### Acceptance criteria
- The pipeline must successfully accomplish its goals.
- The code must be deployable or runnable locally.
- Include unit and end-to-end testing, following TDD principles.
- Include additional metadata or data lineage information.
- Incorporate automation wherever possible.
- Provide clear design and documentation.


# Setup

## Create an .env file
Run the following command in your terminal to create an .env file, replacing placeholders with your desired values: `vim .env`

Example of .env file:
```
AIRFLOW_UID=501
AIRFLOW_USER=your_airflow_user
AIRFLOW_PASSWORD=our_airflow_password
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_user_password
POSTGRES_DB=your_postgres_db
POSTGRES_HOST=localhost
POSTGRES_HOST_CONN=postgres
```
## Step-by-step up
### Start Airflow and Postgres
Run the following command to start Airflow and Postgres: `make up_airflow`

This command includes docker compose up airflow-init and docker compose up.

### Access Airflow
Open your web browser and navigate to http://localhost:8080 to log in.

### Connect to Postgres
To find the current port allocated for Postgres, run: `docker ps`

Use the information from the .env file to connect to the database. The connection process to Airflow is automated using: `make connect_airflow_to_db`. This runs the bash script `./src/connect_airflow_to_db.sh`.

## Running everything together
To run Airflow and connect to the database automatically, use: `make up_and_connect`. This runs the `docker compose up` commands in detached mode and runs the sh that make the Postgres conneciton when Airflow is up.

## Shut down Airflow
To stop Airflow, cancel the running process and execute: `make down_airflow`.
