# Data Visualization of Parents and Teens Survey Data from [Pulse](https://www.pulsepeers.com/)

[Pulse](https://www.pulsepeers.com/) is a start-up company building solutions to support Teens' mental health. This is an exploratory data analysis that observed trends in
survey data among different demographics. Data visualization dashboards were designed and created to facilitate the analysis using [Plotly Dash](https://dash.plotly.com/).


## Data Cleaning & Wrangling
Since the survey data were all text and were recorded from multiple surveys with different format, data were cleaned and standardized with following in mind:
- Count the number of Teens in the family and compute Median age of the teens in each family entry
- Since multiple-choice survey questions had no priority in order of entry, One-Hot Encoding was used to creates binary columns indicating the presence or absence of each category for each survey response for ease of further data analysis and queries.

## Data Visualization
[An interactive dashboard with multiple navigation links](https://clarechao.pythonanywhere.com/) using *dash-boostrap-component* was designed and created using [Plotly Dash Framework](https://dash.plotly.com/).

The dashboard is divided into six main pages:
  - **Parents Demographics**: this page provides a demographic analysis of parents participating the survey, including gender, age, marital status, ethnicity, geographical distribution by state, and level of parents' involvement in Teens' life vs. level of comfort Teens share with parents.
  - **Parents' Concern**:
    - One way to show what parents are concerned about was through horizontal bar chart, which is effective to present categorical data from surveys with multiple selections
    - For each category of parents' concern, a cross-filtered bar chart of where parents seek advice was live-updated to observe trend or correlation among different demographic groups
  - **Parents Survey Summary**: horizontal bar charts were used to present categorical data and 1-D map using *plotly.imshow* to show how comfortable parents are to use AI tools for their Teens' development.
  - **Teens Demographics**: this page provides a demographic analysis of teens participating the survey, including gender, grade, how well teens express their emotion for each grade, and how often Teens talk to caregivers vs how helpful the advice are to Teens.
  - **Teens' Emotion**: for each category of how teens handle strong emotion, a distribution of who teens reach out to talk when struggling are live-updated. One can cycle through *Grade* to observe any trend/correlation.
  - **Teens' Social Media Use**: Two KPIs, *percent of teens feeling comfortable sharing on social media* and *Top social media platform*, are shown with how Teens think about the impact of social media use in his/her life. A circle chart, a customized chart using *plotly.graph_object*, was created as a visually-clear way (instead of another bar chart) to how Teens feel about the impact of social media.

## Overview

[Live Demo of the interactive dashboard](https://www.dropbox.com/scl/fi/cy0yvkli2xefq66qy4aya/dashboard_demo.mov?rlkey=a9uvxmhdehi1mfpswbmvrgm93&st=1ofcl8u1&dl=0)

## Tools that I used to build

The dashboard was built using Python, Plotly Dash Framework, and CSS. It is hosted by [PythonAnywhere](https://www.pythonanywhere.com/).

![Static Badge](https://img.shields.io/badge/Python-%233776AB?style=for-the-badge&logo=python&logoColor=%23FFDC0F)

![Static Badge](https://img.shields.io/badge/Plotly-%233F4F75?style=for-the-badge&logo=plotly&logoColor=%23EEEEEE)

![Static Badge](https://img.shields.io/badge/CSS-%23663399?style=for-the-badge&logo=CSS&logoColor=%23FFFFFF)

![Static Badge](https://img.shields.io/badge/PythonAnywhere-%231D9FD7?style=for-the-badge&logo=PythonAnywhere&logoColor=%23FFFFFF)

## Contact

For feedback and suggestion, please contact [Shih-ying (Clare) Chao](https://www.linkedin.com/in/shihyinghuang).




