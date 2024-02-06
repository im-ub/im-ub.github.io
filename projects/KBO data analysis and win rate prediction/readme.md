# KBO data analysis and win rate prediction
## Project Details
Type: Undergrad Major, team project <br />
Course Name: Data Mining ad Application <br />
Date : 09-10-2020 ~ 12-10-2020  <br />

## Project Description
Each institution or media outlet that conducts sports analysis predicts different values, leading viewers to have misguided expectations. To address this situation, we aimed to provide guidance indicators for predictions through data mining.<br/>
We secured data from the Korea Baseball Organization (KBO) record room through web scraping and reconstructed team data through individual record analysis to understand team trends and analyze player data, enabling us to grasp the overall tendencies of the teams. Additionally, we aimed to assess offensive and defensive capabilities by analyzing data for hitters and pitchers.<br/>
For analysis techniques, we utilized correlation analysis, multiple regression analysis, PCA analysis, and neural network analysis.<br/>

**Player and Team Data Analysis Results**

For hitters' data, we conducted correlation analysis, multiple regression analysis, and PCA analysis with salary, revealing a high correlation between salary and home runs. Similarly, we conducted the same analysis for pitchers and found a high correlation between salary and strikeouts in pitcher data.<br/>
We created radar charts using data from teams that advanced beyond the playoffs to visualize the analysis results of each team. With radar charts, we could easily compare the strengths and weaknesses of each team at a glance.<br/>

**Win Rate Prediction**

Using team data, we conducted multiple regression analysis and principal component regression analysis for win rate prediction. However, low R-squared values or unsatisfactory results prompted us to apply other analysis techniques. Consequently, we attempted Multilayer Feed Forward Neural Network analysis, which yielded high values, leading us to consider the prediction successful.<br/>
Based on this analysis, we could easily grasp team-by-team analysis and compatibility between teams. There are expected benefits such as predicting winning teams to gain advantages in contracts.<br/>

## Project Skill Set
- Language: Python
- Libraries : BeautifulSoup, requests, pandas, matplotlib
