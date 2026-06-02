import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
import os


# ==================================
# DATABASE CONNECTION
# ==================================

def create_connection():

    engine = create_engine(
        "mysql+pymysql://4QgRrEsQzcSAcSR.root:I11vnAFvBTMIcx4w@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/cricsheet_db",
        connect_args={
            "ssl": {"ssl": {}}
        },
        pool_recycle=3600
    )

    return engine


# ==================================
# LOAD DATA
# ==================================

def load_data(engine):

    # MATCH TABLES
    matches = pd.read_sql("SELECT * FROM matches", engine)
    innings = pd.read_sql("SELECT * FROM innings", engine)

    print("Matches:", len(matches))
    print("Innings:", len(innings))

    return matches, innings

# ==================================
# CREATE VISUALIZATIONS
# ==================================

def create_visualizations():

    engine = create_connection()

    matches, innings = load_data(engine)

    os.makedirs("presentation", exist_ok=True)

    sns.set_style("whitegrid")


    # ==================================
    # 1 MATCH DISTRIBUTION
    # ==================================

    plt.figure(figsize=(8,6))

    match_counts = matches["match_type"].value_counts()

    plt.pie(
        match_counts.values,
        labels=match_counts.index,
        autopct='%1.1f%%'
    )

    plt.title("Match Distribution by Format")

    plt.savefig("presentation/1_match_distribution.png")

    plt.close()


    # ==================================
    # 2 TOP BATSMEN
    # ==================================

    top_batsmen = (
        innings.groupby("batsman")["runs_batted"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(14,8))

    sns.barplot(
        x=top_batsmen.values,
        y=top_batsmen.index
    )

    plt.title("Top 10 Batsmen by Runs")

    plt.xlabel("Runs")

    plt.ylabel("Batsman")

    plt.tight_layout()

    plt.savefig(
        "presentation/2_top_batsmen.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    # ==================================
    # 3 TOP BOWLERS
    # ==================================

    top_bowlers = (
        innings.groupby("bowler")["wicket"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12,7))

    sns.barplot(
        x=top_bowlers.values,
        y=top_bowlers.index
    )

    plt.title("Top 10 Bowlers by Wickets")

    plt.tight_layout()

    plt.savefig("presentation/3_top_bowlers.png")

    plt.close()


    # ==================================
    # 4 RUNS DISTRIBUTION
    # ==================================

    plt.figure(figsize=(10,6))

    sns.histplot(
        innings["runs_batted"],
        bins=20,
        kde=True
    )

    plt.title("Runs Distribution")

    plt.savefig("presentation/4_runs_distribution.png")

    plt.close()


    # ==================================
    # 5 CORRELATION HEATMAP
    # ==================================

    plt.figure(figsize=(8,6))

    numeric_cols = innings[
        ["runs_batted", "extras", "total_runs", "wicket"]
    ]

    sns.heatmap(
        numeric_cols.corr(),
        annot=True,
        cmap="coolwarm"
    )

    plt.title("Correlation Heatmap")

    plt.savefig("presentation/5_correlation_heatmap.png")

    plt.close()


    # ==================================
    # 6 TOSS ANALYSIS
    # ==================================

    toss = matches["toss_decision"].value_counts()

    plt.figure(figsize=(8,6))

    sns.barplot(
        x=toss.index,
        y=toss.values
    )

    plt.title("Toss Decision Analysis")

    plt.savefig("presentation/6_toss_analysis.png")

    plt.close()


    # ==================================
    # 7 VENUE ANALYSIS
    # ==================================

    venue = matches["venue"].value_counts().head(10)

    plt.figure(figsize=(15,8))

    sns.barplot(
        x=venue.values,
        y=venue.index
    )

    plt.title("Top Venues")

    plt.tight_layout()

    plt.savefig("presentation/7_venue_analysis.png")

    plt.close()


    # ==================================
    # 8 TEAM PERFORMANCE
    # ==================================

    team_runs = (
        innings.groupby("inning_team")["total_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(14,8))

    sns.barplot(
        x=team_runs.values,
        y=team_runs.index
    )

    plt.title("Top Teams by Runs")

    plt.tight_layout()

    plt.savefig("presentation/8_team_runs.png")

    plt.close()


    # ==================================
    # 9 RUN RATE BY FORMAT
    # ==================================

    run_rate = (
        innings.groupby("match_type")["total_runs"]
        .mean()
    )

    plt.figure(figsize=(8,6))

    sns.barplot(
        x=run_rate.index,
        y=run_rate.values
    )

    plt.title("Average Runs by Format")

    plt.savefig("presentation/9_run_rate_format.png")

    plt.close()


    # ==================================
    # 10 INTERACTIVE PLOTLY
    # ==================================

    batsman_runs = (
        innings.groupby("batsman")["runs_batted"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig = px.bar(
        batsman_runs,
        x="runs_batted",
        y="batsman",
        title="Top Batsmen Interactive"
    )

    fig.write_html(
        "presentation/10_plotly_chart.html"
    )

    print("EDA Visualizations Created Successfully!")


# ==================================
# MAIN
# ==================================

if __name__ == "__main__":

    create_visualizations()