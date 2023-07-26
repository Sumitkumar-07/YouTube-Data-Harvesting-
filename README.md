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
# Home Page
  - The home page provides an overview of the application, its domain, technologies used, and a brief description of its functionality.
  - The YouTube logo is displayed at the top of the page.

# Extract and Transform Page
  - Access the "Extract and Transform" page from the navigation menu on the sidebar.
  - Extract Tab
     - Enter YouTube Channel ID:
         - To start data extraction, enter the channel ID in the input box.
         - To find the channel ID, go to the YouTube channel's home page, right-click, select "View page source," and find the "channel_id" in the source code. 
           Copy and paste it into the input box.
     - Extract Data:
         - Click the "Extract Data" button to retrieve the details of the specified YouTube channel using the YouTube Data API.
         - The extracted data will be displayed in a table format, showing information such as the channel name, subscribers, views, total videos, and more.
     - Upload to MongoDB:
         - After extracting the data, you can click the "Upload to MongoDB" button to store the extracted data in a MongoDB database as part of the data lake
  - Transform Tab
     - Select a Channel to Begin Transformation:
         - In the "Transform" tab, you can select a YouTube channel from the dropdown menu.
         - The dropdown menu will be populated with channel names retrieved from the MongoDB database.
     - Submit: 
         - After selecting a channel, click the "Submit" button to start the data transformation process.

# View Page
   - Access the "View" page from the navigation menu on the sidebar.
     - Select a Question: 
         - Choose a question from the dropdown menu to get insights and analytics from the transformed data.
     - Questions and Analytics:
         - The dropdown menu contains predefined questions with corresponding analytics for YouTube channel data.
         - The answers to the questions are displayed in table format for easy viewing and understanding.
   - Visualization:
         - Some questions have associated visualizations, such as bar charts, to provide graphical representation and better insights into the data.
         - The visualizations are interactive, allowing you to hover over data points for more details.


# How to Run the Application
1) Install Dependencies:
      - Ensure you have Python installed along with the required libraries as mentioned in the "Imports" section of the code.
2) Set Up MongoDB:
      - Make sure you have MongoDB installed and running on localhost and port 27017.
3) Set Up MySQL:
      - Configure your MySQL database with the appropriate credentials (host, user, password, database) for data migration.
4) API Key:
     - Replace the api_key variable with your own YouTube Data API key.
5) Start the Streamlit App:
     - Run the application by executing the command streamlit run app.py in your terminal.
6) Interact with the App:
     - The application will open in your default web browser.
     - Use the navigation menu on the sidebar to access different pages: "Home," "Extract and Transform," and "View."
     - Follow the instructions on each page to extract data, transform and load it into the database, and view analytics.
