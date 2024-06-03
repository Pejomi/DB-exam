# DB-Exam
Created by the group Pejomi (Peter, Jonas, Mie)

## About the project
This project is a database exam project for the course "Databases" at the Cphbusiness Lyngby campus. Below you will find a description of the project, the database design, and the deployment.

## Business scenario 
**SafeWay**  is a company working with artificial intelligence and machine learning to provide tools for investigating and predicting car accidents.

Their service is based on a large dataset of car accidents in the UK, which includes information about the weather, road conditions, time of day, the driver involved and other factors leading up to the accident.

With the data they want to provide a services such as a chatbot that can answer questions about car accidents, a machine learning model that can predict the likelihood of a car accident given certain conditions, and a simulation environment for training autonomous cars.

## Application domain
For the current domain of the application the focus has been limitid to concentrate on managing data for storing in databases. 

### Users
The application are meant for two types of users:
- **Admins**: Admins can access all chat history and the traffic accident data set.

- **Users**: Users can access their own chat history and search in the traffic accident data set.

### Functionalities
For the chatbot service, the following functionalities are required:

**Functional requirements:**
- **Chat history**: The chat history should be stored in a database.
- **Search**: The user should be able to search in the traffic accident data set.
- **Search criteria**: The user should be able to search with a large amount of criteria in the traffic accident data set.
- **Data set**: The traffic accident data set should be stored in a database.

**Non-functional requirements:**
- **Performance**: The application should be able to handle a large amount of users and data.
- **User-friendly**: The app should be user-friendly and easy to use.

--- 

Below is a diagram of the overall architecture of the application:

![alt text](img/structure.png)

## Database Design
For the database design, we have chosen to implement three different types of databases: 

- Document
- Relational 
- Graph database

### Document database
The document database is implemented using MongoDB. The database is designed to store the chat history for the chatbot service. 

The database "chatbot" consists of a collection called "messages". The collection stores the chat history between the user and the chatbot. Below is an example of a document in the "messages" collection.


```json
{
    "email": "alice@gmail.com",
    "title": "Car accident",
    "message": [
        {
            "role": "user",
            "content": "What should I do if I'm in a car accident?"
        },
        {
            "role": "chatbot",
            "content": "You should call the police and your insurance company"
        }
    ]
}
```
Our database is deployed on MongoDB Atlas with a cluster in the cloud in which consists of 3 replica sets.

### Relational database
The relational database is implemented using MSSQL. The database is designed to store the traffic accident data set.

Below is a diagram of the relational database design:

![alt text](img/sql-database-diagram.png)

### Graph database
The graph database is implemented using Neo4j. The database is designed to store the relationships between the different entities in the traffic accident data set.

## Current status
The focus has been on the database design and the implementation of the three database types: Document, Relational and Graph database. 

The streamlit app contains a simple user interface where the user can search in the traffic accident data set. The user can search with a large amount of criteria such as the weather, road conditions, time of day, and the driver involved. 

![alt text](img/sql-search.png)

The user can also access their own chat history with the chatbot and admin can access all chat history.

![alt text](img/saved-messages.png)

Some features such as proper response from chatbot and machine learning model are not implemented yet. These features will be implemented in the future.

## Setup project

### Download datasets
Download the datasets from the link below and place them in a folder called "data" in the root of the project.

#### Traffic accident in UK data set
The data set contains information about car accidents in the UK. The data set is used to populate the relational database and the graph database. [Link to the data set](https://www.kaggle.com/datasets/tsiaras/uk-road-safety-accidents-and-vehicles?select=Accident_Information.csv)


### Clean data
In the main.py file you will have to out comment the line 19-21: 

```python
merge_data.merge_data()
data = pd.read_csv('data/merged_information.csv', encoding='ISO-8859-1')
clean_data.clean_data(data)
```
    
Then run the main.py file only **ONCE** to clean the data. After the data is cleaned you can uncomment the lines 19-21 and run the main.py file again to populate the databases. (If you haven't already setup your MSSQL database you have to do that first before running the main.py file again.)
    
```python
python main.py
```

### Setup databases

#### MongoDB
To setup the MongoDB database you will need to create a database called "chatbot" and a collection called "messages" either on your local machine or on MongoDB Atlas.

Then create a .env file in the root of the project and add the variable "MONGODB" with your connection string to the file as shown below:

```env
MONGODB="your_mongodb_connection_string"
```

#### MSSQL
To setup the MSSQL database you will need to create a database called "exam_schema_v3" in your local MSSQL server.

In your .env file add the variable "MSSQL_SERVER" with your server name as shown below:

```env
MSSQL_SERVER="server_name"
```

Run the main.py file to populate the MSSQL database with the traffic accident data set.
    
```python
python main.py
```

#### Neo4j
To setup the Neo4j database you will need to create a database with your desired name in your local Neo4j server. Make sure to have the Neo4j server running when you run the application.

## Run streamlit app
To run the streamlit app, you need to have streamlit installed. If you don't have streamlit installed, you can install it by running the following command:

```bash
pip install streamlit
```

After installing streamlit, you can run the streamlit app by running the following commands:

```bash
cd streamlit_app 
```

```bash
streamlit run app.py
```

## Technologies
The following technologies have been used in the project:
- MongoDB
- MSSQL
- Neo4j
- Streamlit
- Python
