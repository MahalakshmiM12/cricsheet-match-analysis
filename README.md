Cricsheet Match Data Analysis (Python + SQL + Power BI)
A comprehensive cricket data analysis project that processes 4,776,439 ball-by-ball delivery records across T20, ODI, IPL, and TEST formats from Cricsheet.org, performs deep SQL analysis, and creates interactive visualizations. This project demonstrates end-to-end data engineering and analysis skills — from raw JSON parsing to a live Power BI dashboard.

Features
Data Parsing: Automated JSON to structured CSV conversion using Pandas and tqdm for all four cricket formats
Database Management: TiDB Cloud (MySQL 8 compatible) with optimized schema design and Foreign Key relationships
SQL Analysis: 20 advanced analytical queries covering window functions, ranking, joins, and subqueries
EDA Visualizations: 10 charts using Matplotlib, Seaborn, and Plotly (9 static PNG + 1 interactive HTML)
Power BI Dashboard: 6 interactive visuals with a match-type slicer for T20 · ODI · IPL · TEST filtering
Performance Optimized: Bulk inserts with chunksize=5000 for efficient 4.77M row loading

Tech Stack
Python — Core programming language (3.10+)
Pandas — Data processing and manipulation
SQLAlchemy + PyMySQL — Database ORM and connection management
Matplotlib / Seaborn — Static visualizations and charts
Plotly — Interactive visualizations
TiDB Cloud — MySQL 8 compatible cloud database
mysql-connector-python — Direct MySQL connection
tqdm — Progress tracking during JSON parsing

Data Source
The cricket data is sourced from Cricsheet.org — a free, open-source ball-by-ball cricket dataset maintained by Stephen Rushe. It provides JSON format match data for international and domestic cricket. You can download the raw JSON files from cricsheet.org/downloads and place them inside the data_files/ folder before running the pipeline.

How to Run this Project
git clone https://github.com/MahalakshmiM12/cricsheet-match-analysis.git
cd cricsheet-match-analysis
pip install -r requirements.txt
python cricsheet_data.py
python db.py
python bulk_insert_data.py
python eda.py

Power BI Dashboard
The complete Power BI dashboard is available in:
cricket_dashboard.pbix
