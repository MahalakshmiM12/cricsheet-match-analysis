# 1 Top 10 Batsmen by Total Runs in ODI Matches
SELECT
    batsman,
    SUM(runs_batted) AS total_runs
FROM innings
WHERE match_id IN (
    SELECT match_id
    FROM matches
    WHERE match_type = 'ODI'
)
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;

#2 Leading Wicket-Takers in T20 Matches
SELECT
    bowler,
    COUNT(*) AS total_wickets
FROM innings
WHERE wicket = 1
AND match_id IN (
    SELECT match_id
    FROM matches
    WHERE match_type = 'T20'
)
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;

#3️ Team with Highest Win Percentage in Test Cricket
SELECT
    winner AS team,
    COUNT(*) * 100.0 /
    (
        SELECT COUNT(*)
        FROM matches
        WHERE match_type = 'TEST'
    ) AS win_percentage
FROM matches
WHERE match_type = 'TEST'
AND winner IS NOT NULL
GROUP BY winner
ORDER BY win_percentage DESC
LIMIT 1;

# 4 Total Number of Centuries Across All Match Types
SELECT
    batsman,
    match_id,
    SUM(runs_batted) AS total_runs
FROM innings
GROUP BY batsman, match_id
HAVING total_runs >= 100
ORDER BY total_runs DESC;

# 5 Matches with Narrowest Margin of Victory
SELECT
    match_id,
    winner,
    venue,
    match_date
FROM matches
WHERE winner IS NOT NULL
LIMIT 10;

# 6 Over-wise Total Runs Ranking
SELECT *
FROM (
    SELECT 
        match_id,
        over_number,
        SUM(total_runs) AS over_runs,

        RANK() OVER (
            PARTITION BY match_id
            ORDER BY SUM(total_runs) DESC
        ) AS rnk

    FROM innings
    GROUP BY match_id, over_number
) t
WHERE rnk = 1;

# 7 Strike Rate Using Window
SELECT 
    batsman,
    match_id,

    SUM(runs_batted) OVER (PARTITION BY match_id, batsman) AS runs,

    COUNT(*) OVER (PARTITION BY match_id, batsman) AS balls,

    (SUM(runs_batted) OVER (PARTITION BY match_id, batsman) * 100.0 /
     COUNT(*) OVER (PARTITION BY match_id, batsman)) AS strike_rate

FROM innings;

# 8 Cumulative Wickets
SELECT 
    match_id,
    inning_team,
    over_number,
    ball,
    wicket,

    SUM(wicket) OVER (
        PARTITION BY match_id, inning_team
        ORDER BY over_number, ball
    ) AS total_wickets

FROM innings;

# 9 Dense Rank (Tie Handling)
SELECT 
batsman,
SUM(runs_batted) AS total_runs,

DENSE_RANK() OVER(
ORDER BY SUM(runs_batted) DESC
) AS rank_position

FROM innings
GROUP BY batsman;

#10 Top 10 Batsmen (Total Runs)
SELECT batsman,
SUM(runs_batted) AS total_runs
FROM innings
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;

# 11 Toss Decision Analysis
SELECT
    toss_decision,
    COUNT(*) AS total_matches
FROM matches
GROUP BY toss_decision;

#12 Highest Individual Score
SELECT match_id, batsman,
SUM(runs_batted) AS runs
FROM innings
GROUP BY match_id, batsman
ORDER BY runs DESC
LIMIT 10;

# 13 Consistent Batsmen (Matches Played)
SELECT batsman,
COUNT(DISTINCT match_id) AS matches_played
FROM innings
GROUP BY batsman
ORDER BY matches_played DESC
LIMIT 10;

# 14 Top 10 Bowlers (Wickets)
SELECT bowler,
SUM(wicket) AS total_wickets
FROM innings
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;

# 15 Best Bowling in a Match
SELECT match_id, bowler,
SUM(wicket) AS wickets
FROM innings
GROUP BY match_id, bowler
ORDER BY wickets DESC
LIMIT 10;

# 16 Most Matches Played at Venue
SELECT venue,
COUNT(*) AS matches
FROM matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 10;

# 17 Highest Scoring Matches
SELECT match_id,
SUM(total_runs) AS total_runs
FROM innings
GROUP BY match_id
ORDER BY total_runs DESC
LIMIT 10;

# 18 Team-wise Runs
SELECT m.winner,
SUM(i.total_runs) AS total_runs
FROM innings i
JOIN matches m
ON i.match_id = m.match_id
GROUP BY m.winner
ORDER BY total_runs DESC;

#19 Player Performance by Venue
SELECT i.batsman,
m.venue,
SUM(i.runs_batted) AS runs
FROM innings i
JOIN matches m
ON i.match_id = m.match_id
GROUP BY i.batsman, m.venue
ORDER BY runs DESC
LIMIT 10;

#20 Wickets per Match (Consistency)
SELECT bowler,
COUNT(DISTINCT match_id) AS matches,
SUM(wicket) AS wickets,
SUM(wicket)/COUNT(DISTINCT match_id) AS avg_wickets
FROM innings
GROUP BY bowler
ORDER BY avg_wickets DESC
LIMIT 10;

