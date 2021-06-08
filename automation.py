#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
start_time = datetime.now()


# In[2]:


# Load the dataset directly from the source
import pandas as pd
covid_data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

# Modify the data into 2 tables
covid_deaths = pd.concat([covid_data.iloc[:,:4],pd.DataFrame(covid_data['population']),covid_data.iloc[:,4:25]], axis = 1)
covid_vaccinations = pd.concat([covid_data.iloc[:,:4],covid_data.iloc[:,25:44],covid_data.iloc[:,45:]],axis =1)
# Save them as csv
covid_deaths.to_csv('D:\JupyterNotebooks\covid_analysis_project\data\covid_deaths.csv',index = False)
covid_vaccinations.to_csv('D:\JupyterNotebooks\covid_analysis_project\data\covid_vaccinations.csv',index = False)


# In[3]:


# Open a connection to SQL
import pyodbc 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=GSVIVOBOOK;'
                      'Database=Covid Analysis Project;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


# In[4]:


# Set a SQL query to update the table covid_deaths
import_covid_deaths = '''
USE [Covid Analysis Project];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[covid_deaths]') AND type in (N'U'))
DROP TABLE [dbo].[covid_deaths];


SET ANSI_NULLS ON;

SET QUOTED_IDENTIFIER ON;

CREATE TABLE [dbo].[covid_deaths](
[iso_code] [nvarchar](255) NULL,
[continent] [nvarchar](255) NULL,
[location] [nvarchar](255) NULL,
[date] [date] NULL,
[population] [float] NULL,
[total_cases] [float] NULL,
[new_cases] [float] NULL,
[new_cases_smoothed] [float] NULL,
[total_deaths] [float] NULL,
[new_deaths] [float] NULL,
[new_deaths_smoothed] [float] NULL,
[total_cases_per_million] [float] NULL,
[new_cases_per_million] [float] NULL,
[new_cases_smoothed_per_million] [float] NULL,
[total_deaths_per_million] [float] NULL,
[new_deaths_per_million] [float] NULL,
[new_deaths_smoothed_per_million] [float] NULL,
[reproduction_rate] [float] NULL,
[icu_patients] [float] NULL,
[icu_patients_per_million] [float] NULL,
[hosp_patients] [float] NULL,
[hosp_patients_per_million] [float] NULL,
[weekly_icu_admissions] [float] NULL,
[weekly_icu_admissions_per_million] [float] NULL,
[weekly_hosp_admissions] [float] NULL,
[weekly_hosp_admissions_per_million] [float] NULL
) ON [PRIMARY];

BULK INSERT [covid_deaths]
FROM 'D:\JupyterNotebooks\covid_analysis_project\data\covid_deaths.csv'
WITH(FORMAT ='CSV',FIRSTROW = 2)
'''

# And execute it
cursor.execute(import_covid_deaths)
conn.commit()


# In[5]:


# Setting a SQL query to update the table covid_vaccinations
import_covid_vaccinations = '''
USE [Covid Analysis Project];

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[covid_vaccinations]') AND type in (N'U'))
DROP TABLE [dbo].[covid_vaccinations];

SET ANSI_NULLS ON;

SET QUOTED_IDENTIFIER ON;


CREATE TABLE [dbo].[covid_vaccinations](
[iso_code] [nvarchar](255) NULL,
[continent] [nvarchar](255) NULL,
[location] [nvarchar](255) NULL,
[date] [date] NULL,
[new_tests] [float] NULL,
[total_tests] [float] NULL,
[total_tests_per_thousand] [float] NULL,
[new_tests_per_thousand] [float] NULL,
[new_tests_smoothed] [float] NULL,
[new_tests_smoothed_per_thousand] [float] NULL,
[positive_rate] [float] NULL,
[tests_per_case] [float] NULL,
[tests_units] [varchar](50) NULL,
[total_vaccinations] [float] NULL,
[people_vaccinated] [float] NULL,
[people_fully_vaccinated] [float] NULL,
[new_vaccinations] [float] NULL,
[new_vaccinations_smoothed] [float] NULL,
[total_vaccinations_per_hundred] [float] NULL,
[people_vaccinated_per_hundred] [float] NULL,
[people_fully_vaccinated_per_hundred] [float] NULL,
[new_vaccinations_smoothed_per_million] [float] NULL,
[stringency_index] [float] NULL,
[population_density] [float] NULL,
[median_age] [float] NULL,
[aged_65_older] [float] NULL,
[aged_70_older] [float] NULL,
[gdp_per_capita] [float] NULL,
[extreme_poverty] [float] NULL,
[cardiovasc_death_rate] [float] NULL,
[diabetes_prevalence] [float] NULL,
[female_smokers] [float] NULL,
[male_smokers] [float] NULL,
[handwashing_facilities] [float] NULL,
[hospital_beds_per_thousand] [float] NULL,
[life_expectancy] [float] NULL,
[human_development_index] [float] NULL
) ON [PRIMARY];


BULK INSERT [covid_vaccinations]
FROM 'D:\JupyterNotebooks\covid_analysis_project\data\covid_vaccinations.csv'
WITH(FORMAT ='CSV',FIRSTROW = 2)
'''

# And execute it
cursor.execute(import_covid_vaccinations)
conn.commit()


# In[6]:


# Connect to Google Sheets using pygsheets library and the Google Sheets API with my credentials
import pygsheets
creds = 'D:\Coding\pygsheet_secret.json'
api = pygsheets.authorize(service_file=creds)

# Open the workbook that contains the final output
wb = api.open('Covid Tables')


# In[7]:


# Write the query for the table that will be in in sheet1
query1 = '''
SELECT 
    SUM(new_cases) AS total_cases, 
    SUM(new_deaths) AS total_deaths, 
    SUM(new_deaths)/SUM(new_cases)*100 AS total_death_percentage 
FROM [Covid Analysis Project].dbo.covid_deaths 
WHERE continent IS NOT NULL 
ORDER BY 1,2;
'''
# Execute it
table1 = pd.read_sql_query(query1,conn)

# Open Sheet1 and update the data
sheet1= wb.worksheet_by_title(f'Sheet1')
sheet1.set_dataframe(table1, (1,1))


# In[8]:


# Same as above
query2 = '''
SELECT 
    location, 
    MAX(total_deaths) AS total_death_count 
FROM [Covid Analysis Project].dbo.covid_deaths 
WHERE continent IS NULL AND location NOT IN ('World', 'European Union','International') 
GROUP BY location 
ORDER BY total_death_count DESC;
'''
table2 = pd.read_sql_query(query2,conn)

sheet2 = wb.worksheet_by_title(f'Sheet2')
sheet2.set_dataframe(table2, (1,1))


# In[9]:


# Same as above
query3 = '''
SELECT 
    location, 
    population, 
    MAX(total_cases) AS highest_cases_count, 
    MAX((total_cases/population))*100 AS highest_infection_rate 
FROM [Covid Analysis Project].dbo.covid_deaths 
WHERE continent IS NOT NULL 
GROUP BY location, population 
ORDER BY highest_infection_rate DESC;
'''
table3 = pd.read_sql_query(query3,conn)
table3.fillna(0, inplace = True)

sheet3 = wb.worksheet_by_title(f'Sheet3')
sheet3.set_dataframe(table3, (1,1))


# In[10]:


# Same as above
query4 = '''
SELECT 
    location, 
    population,
    date, 
    MAX(total_cases) AS highest_cases_count, 
    MAX((total_cases/population))*100 AS highest_infection_rate 
FROM covid_deaths 
WHERE continent IS NOT NULL 
GROUP BY location, population, date 
ORDER BY highest_infection_rate DESC;
'''
table4 = pd.read_sql_query(query4,conn)

# Here I only select data from a few countries to save Google Sheets from some heavy lifting (which makes it very slow)
highlight = ['United States', 'Vietnam','Mexico','China','India','United Kingdom']
table4 = table4[table4['location'].isin(highlight)]
table4.fillna(0, inplace = True)

sheet4 = wb.worksheet_by_title(f'Sheet4')
sheet4.set_dataframe(table4, (1,1))


# In[11]:


# Closing the connection
conn.close()


# In[12]:


# Append to our update log
end_time = datetime.now()
elapsed_time = end_time - start_time

date = end_time.strftime("%m/%d/%Y")
time = end_time.strftime("%H:%M")

datetime_message = 'Updated at: ' + time + ' on ' + date + '\n' 
runtime_message = 'Runtime: ' + str(elapsed_time) + '\n'+ "*"*50 + '\n'

with open('update_log.txt','a') as file:
    file.write(datetime_message+runtime_message)


# In[13]:

# Add the last update time to the spreadsheet (just for checking)
table5 = pd.DataFrame.from_dict({'last_update':[time,date]})
sheet5 = wb.worksheet_by_title(f'Sheet5')
sheet5.set_dataframe(table5, (1,1))