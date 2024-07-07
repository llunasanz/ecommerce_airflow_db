# ecommerce_airflow_db
Information gathering and saving using airflow

## Tasks definitions

It is required to gather information about items published in an ecommerce site, save it in a DB and launch alerts if established criteria are met. This pipeline should be implemented in Airflow and run daily.

Iteraction with the public API is required to collect the data. Here, there is some useful information to proceed:
- [List of categories](https://api.mercadolibre.com/sites/MLA/categories)
- [Specific category information](https://api.mercadolibre.com/categories/MLA1577)
- [Search API for a given category](https://api.mercadolibre.com/sites/MLA/search?category=MLA1577#json)
- [Specific item information](https://api.mercadolibre.com/items/MLA830173972)

### Data pipeline creation
From Mercadolibre site, get the 50 most relevant pusblished items for a particular category, "MLA-MICROWAVES" (category id MLA1577). For each item, it is necessary get the following info:
- "id"
- "site\_id"
- "title"
- "price"
- "sold\_quantity"
- "thumbnail"

Store all this data with an extra field "created\_date" in a Database. Is is necessary implement the pipeline using Airflow DAG.

### Send an alert to mail
Having the previous DAG developed, when any item has earned more than 7.000.000 $ (price x sold\_quantity) when the data gathering task is done, it has to send an email with all the gathered data for every item that reach the previous price.

### Acceptation criteria
- Pipeline has to accomplish its goals successfully.
- Code has to be deployable or runs locally.
- Unit/end to end testing has to be included, applying TDD principles.
- Inclusion of additional metadata or data lineage information.
- Put any form of automation.
- Providing design and documentation.