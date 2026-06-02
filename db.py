import mysql.connector
import pandas as pd
import glob


# DATABASE CONNECTION
def create_database():

    conn = mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="4QgRrEsQzcSAcSR.root",
        password="I11vnAFvBTMIcx4w",
        ssl_disabled=False
    )

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS cricsheet_db")

    print("Database created successfully!")

    cursor.close()
    conn.close()
    
def create_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="4QgRrEsQzcSAcSR.root",
        password="I11vnAFvBTMIcx4w",
        database="cricsheet_db",
        ssl_disabled=False
    )

# RECONNECT FUNCTION
def reconnect(conn):
    try:
        conn.ping(reconnect=True, attempts=3, delay=5)
    except:
        conn = create_connection()
    return conn


# CREATE TABLES
def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id VARCHAR(50) PRIMARY KEY,
        match_type VARCHAR(10),
        team1 VARCHAR(100),
        team2 VARCHAR(100),
        venue VARCHAR(200),
        match_date DATE,
        winner VARCHAR(100),
        toss_winner VARCHAR(100),
        toss_decision VARCHAR(20)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS innings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        match_id VARCHAR(50),
        match_type VARCHAR(10),
        inning_team VARCHAR(100),
        over_number INT,
        ball VARCHAR(10),
        batsman VARCHAR(100),
        bowler VARCHAR(100),
        runs_batted INT,
        extras INT,
        total_runs INT,
        wicket INT,
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database and tables created successfully!")


# MAIN
if __name__ == "__main__":

    create_database()   # first create DB
    create_tables()     # then tables
    

