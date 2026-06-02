import os
import json
import pandas as pd
from glob import glob
from tqdm import tqdm


# =====================================
# BASE PATH
# =====================================

BASE_PATH = r"D:\Guvi_Project\Mini-Projects\02Project_DS_Cricsheet Match Analysis\data_files"

# CLEANED OUTPUT FOLDER
OUTPUT_FOLDER = r"D:\Guvi_Project\Mini-Projects\02Project_DS_Cricsheet Match Analysis\cleaned"

# CREATE FOLDER IF NOT EXISTS
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =====================================
# FORMAT FOLDERS
# =====================================

FORMAT_FOLDERS = {
    "t20s_json": "T20",
    "odis_json": "ODI",
    "ipl_json": "IPL",
    "tests_json": "TEST"
}


# =====================================
# PROCESS SINGLE FOLDER
# =====================================

def process_folder(folder_name, match_type):

    folder_path = os.path.join(BASE_PATH, folder_name)

    json_files = glob(os.path.join(folder_path, "*.json"))

    if not json_files:
        print(f"No files found in {folder_name}")
        return

    print(f"\nProcessing {match_type} → {len(json_files)} files")

    matches_list = []
    innings_list = []


    # =====================================
    # PROCESS JSON FILES
    # =====================================

    for file in tqdm(json_files):

        try:

            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            info = data.get("info", {})

            match_id = os.path.basename(file).replace(".json", "")

            teams = info.get("teams", [None, None])

            toss = info.get("toss", {})

            outcome = info.get("outcome", {})


            # =====================================
            # MATCHES TABLE
            # =====================================

            matches_list.append({

                "match_id": match_id,
                "match_type": match_type,

                "team1": teams[0] if len(teams) > 0 else None,

                "team2": teams[1] if len(teams) > 1 else None,

                "venue": info.get("venue"),

                "date": info.get("dates", [None])[0],

                "winner": outcome.get("winner"),

                "toss_winner": toss.get("winner"),

                "toss_decision": toss.get("decision")

            })


            # =====================================
            # INNINGS TABLE
            # =====================================

            innings = data.get("innings", [])


            for inning in innings:

                # HANDLE BOTH JSON STRUCTURES

                if "team" in inning:

                    inning_team = inning.get("team")

                    overs = inning.get("overs", [])

                else:

                    inning_name = list(inning.keys())[0]

                    inning_data = inning[inning_name]

                    inning_team = inning_data.get("team")

                    overs = inning_data.get("overs", [])


                for over_data in overs:

                    over_number = over_data.get("over")


                    for ball_index, delivery in enumerate(
                        over_data.get("deliveries", []),
                        start=1
                    ):


                        # HANDLE OLD + NEW JSON FORMATS

                        if (
                            isinstance(delivery, dict)
                            and len(delivery) == 1
                            and isinstance(list(delivery.values())[0], dict)
                        ):

                            ball_number = list(delivery.keys())[0]

                            ball_data = delivery[ball_number]

                        else:

                            ball_number = ball_index

                            ball_data = delivery


                        if not isinstance(ball_data, dict):
                            continue


                        runs = ball_data.get("runs", {})


                        innings_list.append({

                            "match_id": match_id,

                            "match_type": match_type,

                            "inning_team": inning_team,

                            "over": over_number,

                            "ball": ball_number,

                            "batsman": ball_data.get("batter"),

                            "bowler": ball_data.get("bowler"),

                            "runs_batted": runs.get("batter", 0),

                            "extras": runs.get("extras", 0),

                            "total_runs": runs.get("total", 0),

                            "wicket": 1 if "wickets" in ball_data else 0

                        })

        except Exception as e:

            print(f"Error in {file}: {e}")


    # =====================================
    # DATAFRAME CREATION
    # =====================================

    matches_df = pd.DataFrame(matches_list)

    innings_df = pd.DataFrame(innings_list)


    # =====================================
    # SAVE CSV FILES INSIDE CLEANED FOLDER
    # =====================================

    matches_output = os.path.join(
        OUTPUT_FOLDER,
        f"{match_type}_matches.csv"
    )

    innings_output = os.path.join(
        OUTPUT_FOLDER,
        f"{match_type}_innings.csv"
    )

    matches_df.to_csv(matches_output, index=False)

    innings_df.to_csv(innings_output, index=False)


    print(
        f"{match_type} Done → "
        f"Matches: {len(matches_df)}, "
        f"Balls: {len(innings_df):,}"
    )


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    for folder, match_type in FORMAT_FOLDERS.items():

        process_folder(folder, match_type)

    print("\nAll formats processed successfully!")