# glidedog_metadata_api

<h3>A simple API written in Python using Django and django_rest_framework</h3>

##### this api is used to store metadata on a larger database. 
##### it uses a version increment system and insures nothing will be deleted from the database in order to track changes made through the versioning system

### Data must be passed into the API in JSON format with specific rules to allow the version incrementing to work properly

#### step 1: creating a dataset with tables and columns
##### URL path: .../dataset
######  - must be done in proper JSON format and only one dataset may be passed in at a time
######  - a dataset may contain as many tables and tables may contain as many columns as needed.
######  - Tables must be wrapped in [ ] and passed in as an array even when only adding one table
######  - Same goes for Columns [ ]
######  - when passing in tables and columns for a new dataset for the first time they MUST NOT contain a dataset field (this will be assigned automatically)

#### step 2:  Adding tables to an existing Dataset  (will cause an increment of the dataset)
#### URL path: .../table
######  - Same as before tables must be in proper JSON format and wrapped in [ ] even when adding only one table. along with the columns existing in that 
#### IMPORTANT:
######  - a "dataset": field must be added to and all tables MUST be assigned a dataset -->  "dataset": [ <dataset_id> ] in this format. the dataset field is a many to many relationship. therefor it's required to wrap the dataset in [ ] even though you will always only be passing in one number because the API is expecting a list of id's 
######  - apon sending the post request the dataset that was assigned will be marked  { "current": false },  then a new version of that existing dataset will be created first and the tables passed in will be assigned to the new version

#### step 3: adding Columns to an existing table
#### URL path: .../column
######  - Columns must be wrapped in [ ] even when sending one column.
######  - Columns must be assigned a table  -->  "table": <table_id>  it will be just a simple integer assigning the column to the table by its id  (many to one field)
######  - Adding a column will not cause any incrementing of the table or the dataset it is being added to

#### step 4: Truncating a Dataset
##### URL path: .../dataset/<dataset_id>/truncate
######  - when truncating a dataset you must pass in the new tables in the body of the request that are to be assigned to said Dataset with the same format as before
#### IMPORTANT:
######  - DO NOT add a "dataset": field when passing in the tables it will be assigned automatically to the new version of the dataset that is to be truncated
######  - also do not assign a table to the columns just like before

#### step 5: Truncating a Table
##### URL path: .../table/<table_id>/truncate
######  - when truncating a table columns must be passed in the body of the request to be added to the newly emptied out table after it has been truncated
#### IMPORTANT:
######  - ALL columns being passed in MUST contain the "table": field with the id of the table that is to be truncated
######  - truncating a table will increment its version as well as incrementing the version (only once) of the dataset it belongs to

#### step 5: Deleting a Dataset
##### URL path .../dataset/<dataset_id>
######  - doing a delete request of an entire dataset will simply mark "current": false  but will not delete the dataset from the database

#### step 6: Deleting a Table
##### URL path: .../table/<table_id>
######  - deleting a table will create and new dataset same as the dataset this table was assigned too with its version incremented and said table will no longer have relation with this new version of the dataset
######  - the table to be deleted will have its "current" field  changed from true to false --> "current": false

#### step 7: Adding a new table to an existing dataset without incrementing its version
##### URL path: /table/new
######  - just incase you forgot to add a certain table to a dataset apon its initial creation you can use this url to add tables to an existing dataset without triggering the version increment system
######  - tables sent in using this URL path must be one at a time with no [ ] wrapping just a simple JSON object { }

###### PS. the database can be manipluated any way you need to without triggering the increment in order to fix any mistakes made using the django admin



