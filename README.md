# YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit
# Problem Statement
  The task is to build a Streamlit app that permits users to analyze data from multiple YouTube channels. Users can input a YouTube channel ID to access data like channel information, video details, and user engagement. The app should facilitate storing the data in a MongoDB database and allow users to collect data from up to 10 different channels. Additionally, it should offer the capability to migrate selected channel data from the data lake to a SQL database for further analysis. The app should enable searching and retrieval of data from the SQL database, including advanced options like joining tables for comprehensive channel information.

# Technology Stack Used
1) Python.
2) MySQL.
3) MongoDB.
4) Google Client Library.
5) Youtube API key.

# Approach
1) Start by setting up a Streamlit application using the python library "streamlit", which provides an easy-to-use interface for users to enter a YouTube channel ID, view channel details, and select channels to migrate.
2) Establish a connection to the YouTube API V3, which allows me to retrieve channel and video data by utilizing the Google API client library for Python.
3) Store the retrieved data in a MongoDB data lake, as MongoDB is a suitable choice for handling unstructured and semi-structured data. This is done by firstly writing a method to retrieve the previously called api call and storing the same data in the database in 3 different collections.
4) Transferring the collected data from multiple channels namely the channels,videos and comments to a SQL data warehouse, utilizing a SQL database like MySQL or PostgreSQL for this purpose.
5) Utilize SQL queries to join tables within the SQL data warehouse and retrieve specific channel data based on user input. For that the SQL table previously made has to be properly given the the foreign and the primary key.
6) The retrieved data is displayed within the Streamlit application, leveraging Streamlit's data visualization capabilities to create charts and graphs for users to analyze the data.

# Requirement Libraries to Install
pip install google-api-python-client, pymongo, mysql-connector-python, sqlalchemy, pymysql, pymysql, pandas, numpy, plotly-express, streamlit.

# E T L Process
# a) Extract Data
  - Utilize the YouTube API developer console to extract data from specific YouTube channels using their channel IDs.
# b) Process and Transform the data
  - After extracting the data, process and select the required details, transforming it into JSON format.
# c) Load data
  - Store the JSON format data in the MongoDB database, providing a data lake for further analysis and storage.
  - Optionally, migrate the data from the MongoDB database to a MySQL database for more structured storage and querying.

By following this ETL process, the project can efficiently extract YouTube channel data, transform it into a suitable format, and load it into databases for analysis and insights.

# E D A Process and Framework
# a) Access MySQL DB
  - Create a connection to the MySQL server using the pymysql library.
  - Access the specified MySQL database and tables containing the extracted data.
# b) Filter the data
  - Filter and process the collected data from the tables based on the given requirements using SQL queries.
  - Transform the processed data into a DataFrame format using the pandas library.
# c) Visualization
  - Create a Dashboard using Streamlit, providing a user-friendly interface for data analysis.
  - Implement dropdown options on the Dashboard, allowing users to select a specific question or analysis criteria.
  - Utilize SQL queries and DataFrame operations to analyze the data based on user selections.
  - Display the output in both DataFrame tables and Bar charts using plotly-express.

By following this EDA process and utilizing the Streamlit framework, users can interactively explore the YouTube data, visualize insights, and gain valuable information from the collected data.

# User Guide
# Step 1. Data Collection Zone
  1) Search Channel ID:
       - Go to the YouTube channel's home page and find the channel ID.
       - Copy the channel ID and paste it into the input box provided in the "Data Collection Zone."
  2) Get Data and Store:
       - Click the "Get Data and Store" button in the "Data Collection Zone" to extract data from the specified YouTube channel using the YouTube API.
       - The data will be stored in the MongoDB database as part of the data lake.

# Step 2. Data Migration Zone
  1) Select Channel Name:
       - In the "Data Migration Zone," select the channel name from the available options. These options will be populated based on the channels stored in the 
         MongoDB database.
  2) Migrate to MySQL:
       - Click the "Migrate to MySQL" button to migrate the specific channel's data from the MongoDB database to the MySQL database.
       - This step provides a structured storage option for further data analysis and querying.
    
# Step 3. Channel Data Analysis Zone
  1) Select a Question:
      - In the "Channel Data Analysis Zone," you will find a dropdown menu with various predefined questions.
  2) Get Results:
      - Choose a question from the dropdown menu to get the analysis results.
  3) The results can be displayed in two formats:
      - DataFrame Format: View the results in a tabular format.
      - Bar Chart Format: Visualize the results using bar charts for better insights.
  4) Interact with the Dashboard:
      - The Streamlit app provides a user-friendly dashboard that allows interactive exploration of the YouTube data.
      - Use the dropdown options and buttons to interact with the app and explore different aspects of the data.

# How to Run the Application
1) Install Dependencies:
      - Ensure you have Python and the required libraries installed as mentioned in the "Setup and Requirements" section of the README file.
        Start MongoDB:
      - Ensure that your MongoDB server is running on localhost and port 27017.
2) Set up MySQL:
      - Configure your MySQL database with the appropriate credentials (host, user, password, database) for data migration.
3) Run the Application:
      - Execute the command streamlit run app.py in your terminal to start the Streamlit app.
4) Access the Dashboard:
      - The Streamlit app will open in your default browser. You can now access and interact with the dashboard.
