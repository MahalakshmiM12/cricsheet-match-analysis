import pandas as pd
import glob
import os
from sqlalchemy import create_engine

# CREATE ENGINE CONNECTION

def create_engine_connection():

    engine = create_engine(
    "mysql+pymysql://4QgRrEsQzcSAcSR.root:I11vnAFvBTMIcx4w@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/cricsheet_db",
    connect_args={
        "ssl": {"ssl": {}}
    },
    pool_recycle=3600
)

    return engine

# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    engine = create_engine_connection()


    # ==========================================
    # CLEANED FOLDER PATH
    # ==========================================

    CLEANED_FOLDER = (
        r"D:\Guvi_Project\Mini-Projects\02Project_DS_Cricsheet Match Analysis\cleaned"
    )


    # ==========================================
    # GET CSV FILES FROM CLEANED FOLDER
    # ==========================================

    match_files = glob.glob(

        os.path.join(
            CLEANED_FOLDER,
            "*_matches.csv"
        )
    )

    innings_files = glob.glob(

        os.path.join(
            CLEANED_FOLDER,
            "*_innings.csv"
        )
    )


    print(f"Found {len(match_files)} match files")

    print(f"Found {len(innings_files)} innings files")


    # ==========================================
    # LOAD MATCHES
    # ==========================================

    for file in match_files:

        print(f"\nLoading Match File: {file}")

        df = pd.read_csv(file)


        # Rename date column
        if "date" in df.columns:

            df.rename(
                columns={"date": "match_date"},
                inplace=True
            )


        # Handle NULL values
        df = df.astype(object).where(
            pd.notnull(df),
            None
        )


        # Select columns
        df = df[[

            "match_id",

            "match_type",

            "team1",

            "team2",

            "venue",

            "match_date",

            "winner",

            "toss_winner",

            "toss_decision"

        ]]


        # Insert into SQL
        df.to_sql(

            name="matches",

            con=engine,

            if_exists="append",

            index=False,

            chunksize=5000

        )

        print("Inserted into matches table")


    # ==========================================
    # LOAD INNINGS
    # ==========================================

    for file in innings_files:

        print(f"\nLoading Innings File: {file}")

        df = pd.read_csv(file)


        # Rename over column
        if "over" in df.columns:

            df.rename(
                columns={"over": "over_number"},
                inplace=True
            )


        # Handle NULL values
        df = df.astype(object).where(
            pd.notnull(df),
            None
        )


        # Select columns
        df = df[[

            "match_id",

            "match_type",

            "inning_team",

            "over_number",

            "ball",

            "batsman",

            "bowler",

            "runs_batted",

            "extras",

            "total_runs",

            "wicket"

        ]]


        # Insert into SQL
        df.to_sql(

            name="innings",

            con=engine,

            if_exists="append",

            index=False,

            chunksize=5000

        )

        print("Inserted into innings table")


    print("\nAll CSV data inserted successfully!")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    load_data()