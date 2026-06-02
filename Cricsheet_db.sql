# CREATE DATABASE
CREATE DATABASE IF NOT EXISTS cricsheet_db;
USE cricsheet_db;

# MATCHES TABLE
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

);

# INNINGS TABLE
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

    FOREIGN KEY (match_id)
    REFERENCES matches(match_id)

);