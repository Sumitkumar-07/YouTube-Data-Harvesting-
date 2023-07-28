# Important points
 - Get your own YouTube Api key from google and put that in code to get the output.
 - Give your correct credentials for Mongodb and Mysql connection.
    - For Mongodb :-
       - check the connection string given.
    - For Mysql :-
       - Check for host, username, password, database name.

# Execution of program
 - On clicking the button "Upload to mongodb" it may takes some time for uploading.
 - And same with Mysql while pressing the button "Transform Data" it takes some time.
 # Reason:-
  - It depends on several factors :-
     - Data Size: If the data being extracted from the YouTube API is large, it may take time to process and insert the data into MongoDB and MySQL. This is especially true if there are a large number of videos and comments to be fetched.
     - Network Latency: The time taken to upload data to remote databases like MongoDB and MySQL can be influenced by network latency. If there is high network latency or slow internet connectivity, it can impact the upload speed.
     - Data Transformation: Data transformation processes, such as converting data types, formatting, or cleaning data, can also add to the processing time.
     - Indexing: If the target database tables have indexes on certain columns, inserting data can take longer due to the overhead of updating the indexes.
     - Database Performance: The performance of the target databases (MongoDB and MySQL) can affect the upload process. If the databases are running on underpowered hardware or handling heavy loads, it can slow down data insertion.
     - Hardware Resources: The server's hardware resources, including CPU, RAM, and disk speed, can impact the upload performance.
     - API Quotas: The YouTube Data API may have rate limits or quotas for the number of requests that can be made within a specific time frame. If the application exceeds these limits, it may need to wait before making additional requests. 
