# Automated Generation System of Streaming Broadcast Highlights using Machine Learning
## Project Details
Type: Undergrad, team project <br />
Course Name: Capston Design Project  <br />
Date : 01-11-2021 ~ 06-24-2021  <br />

## Project Description
The purpose of this project was to address the labor-intensive and inefficient workflow involved in editing live broadcasts lasting an average of 5 to 6 hours into condensed highlight reels of 10 to 20 minutes. The goal was to develop a personal broadcasting highlight auto-extraction system that not only resolves the challenges of this editing process but also allows viewers to easily access highlights of their preferred broadcasts. <br />
The project focused on creating a personal broadcasting highlight auto-extraction system using machine learning. The system predicts highlight segments in the extended broadcast durations, ranging from less popular to popular streamers, based on the analysis of chat data characteristics. <br />
For the collection of chat and voice data from personal broadcasts, energy levels were compared in segments of voice data to determine highlight selections. The chat traffic data and energy data for voice segments were then applied to a Peak Detection Algorithm using the moving average method. The algorithm extracted individual highlight points, which were merged and identified as highlight segment points. <br />
Prior to analyzing the characteristics of chat data in highlight segments, an analysis of the linguistic features of real-time chat was conducted. The average syllables and words per chat, as well as the average number of Korean characters per chat, were analyzed to understand the linguistic characteristics. Subsequently, linguistic elements from chats tagged as highlights and those not tagged as non-highlight segments were compared and analyzed. Based on the results, a chat feature set forming the basis for machine learning was constructed. <br />
The analyzed chat feature set was used to apply machine learning models. Various machine learning models, including Simple RNN, LSTM, Bi-LSTM, GRU, KNN, and SVM, were trained and compared in the tensorflow environment. The LSTM model, showing the highest accuracy, was ultimately utilized for highlight predictions.<br />
Through web development, the system accepts new video URL addresses, extracting highlight segments from the corresponding video. Additionally, various statistical data for the video is presented on the web interface.

## Project Skill Set
- Language: Python, Javascript
- Libraries : pandas, nltk, regex, konlpy, requests, liborsa, matplotlib, sklearn.linear_model, tensorflow, keras, react

