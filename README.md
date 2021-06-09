# Covid Analysis Project
Hello, this is the repository for Covid-19 analysis project, inspired by Alex Freberg.

I have split this project up into 2 parts:

## PART I: Data Exploration ✅
In the first part, I followed Freberg's ideas in his videos [here](https://youtu.be/qfyynHBFOsM) and [here](https://youtu.be/QILNlRvJlfQ). <br>
The tasks in this first part include:
1. Explore the Data using SQL. <br> Bonus: Connect the data with Excel to show query results (which will be used to as the data source for the dashboard)
2. Building [a dashboard using Tableau](https://public.tableau.com/views/CovidAnalysisProject/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link)<img src="https://user-images.githubusercontent.com/69233484/120920799-da2d9780-c6ea-11eb-89b5-adae8679e59f.png" alt="Dashboard" width="50%"/>

## PART II: Automate Everything ⏳
As the name suggest, I have built upon the first part and automate every-single-part of the project so that the Dashboard will maintain itself without me lifting a finger.<br>
Due to limitations with the tools I use, (eg: Tableau can only refreshes data if it comes from Google Sheets, but Google Sheets does not connect to SQL Server - at least seamlessly), I had to find several workarounds. That's why the tasks in **PART II** will look a bit different: 
1. Download and manipulate the data and save as 2 files (similar to **PART I**), using Python.
2. Import the data into SQL Server database, using Python. This must also done in a way that enables daily updates.
3. Save query results to a Google Sheets, using Python.
4. Construct a Tableau dashboard that feeds from the Google Sheets. Tableau will then takes care of the daily data refresh.

All the data, code, and final products of this project will be included in this directory.
