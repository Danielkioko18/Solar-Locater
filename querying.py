# Name: John
# Date: 2023-12-01
# Time: 4:45


# Step 1: Importing the psycopg2 and pandas packages
import psycopg2
import pandas as pd


# Step 2: Creating a connection to the University Database (created in Module 5)
connection = psycopg2.connect(
    database="university_ddl",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432",
)


# Step 3: Creating the cursor object
cursor = connection.cursor()


# Step 3.5: Writing the query to be executed
query = """
    SELECT dept_name, ROUND(AVG(tot_cred), 2) AS dept_avg_credits
    FROM student
    GROUP BY dept_name
    ORDER BY dept_name;
"""


# Step 4: Executing the query
cursor.execute(query)


# Step 5: Storing the query results in a Pandas Dataframe
dataframe = pd.DataFrame(cursor.fetchall(), columns=['dept_name', 'dept_avg_credits'])


# Step 6: Exporting the obtained Pandas Dataframe to a CSV
dataframe.to_csv('dept_avg_credits.csv', index=False)


# Step 7: Commiting the changes
connection.commit()

# Step 8: Closing the Connection
connection.close()


# Showing message to the user
print("Querrying was successful You can see the csv file output")
