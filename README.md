# COVID AUTOMATED DASHBOARD PROJECT
Hello, this is the repository for Covid-19 Automated Dashboard. I was initially inspired by Alex Freberg, but I then expanded the project to include some cool automation.

I have split this project up into 2 parts:

## PART I: Data Exploration ✅
In the first part, I followed Freberg's ideas in his videos [here](https://youtu.be/qfyynHBFOsM) and [here](https://youtu.be/QILNlRvJlfQ).

The tasks in this first part include:
1. ✅ Import and Explore the Data using SQL Server. 
2. ✅ Bonus: Connect the data with Excel to show query results (which will be used to as the data source for the dashboard).
3. ✅ Build [a static dashboard](https://public.tableau.com/views/CovidAnalysisProject/Dashboard1), using Tableau.<br>

<p align="center">
  <img src="https://user-images.githubusercontent.com/69233484/121325062-7ea61880-c93b-11eb-8388-19ec8a0b9806.png" alt="Static Dashboard" width="70%"/>
</p>

*Note: Everything in this part is located in their own folder `Data Exploration`*

## PART II: Automate Everything ⏳
As the name suggest, I have built upon the first part and automate every-single-part of the project so that the Dashboard will maintain itself without me lifting a finger.

Due to limitations with the tools I use, (eg: Tableau can only refreshes data if it comes from Google Sheets, but Google Sheets does not connect to SQL Server - at least seamlessly), I had to find several workarounds. <br>
That's why the tasks in **PART II** will look a bit different: 
1. ✅ Download and manipulate the data and save as 2 files (similar to **PART I**), using Python.
2. ✅ Import the data into SQL Server database (as 2 tables), using Python. Also: Must be done in a way that enables daily updates.
3. ✅ Query the necessary data and save query results to a Google Sheets, using Python. Also: Write an update log when the data is updated. <br>
*(The code for the first 3 steps is in `automation.py`.)*
4. ✅ Bonus: Commit and push all the changes (in the data files, update log, etc) to github, using a batch file. <br>
*(The code for step 4 is in `push_to_git.txt`.)*
5. ✅ Schedule all the previous steps to run daily, using Task Scheduler.
6. ⏳ Construct [a live Tableau dashboard](https://public.tableau.com/app/profile/giang.son/viz/Book1_16231166790080/Dashboard1) that feeds data from the Google Sheets. Tableau will then takes care of the daily data refresh. <br> *(I'm still waiting to see if it actually refreshes without my involvement*
7. ⏳ Bonus: Write a blog post about how I figured this entire thing out.

*Note:*
- *The files for **PART II** will reside in the root directory.*
- *A few of the steps (eg: import to SQL then query from the database) were only there because I was building upon **Part I**. In practice, this process could be simplified depending on the use case (eg: it's possible SQL can be skipped altogether).*


