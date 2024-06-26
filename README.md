# Logistic Transportation System
This project is to determine the country where it is suitable to allocate a new store based on the economic and social status, and running costs for delivering logistics. To achieve this result, we develop a program with optimal algorithms to determine the recommended location of new stores in the country for Moonbucks’s business expansion.

In the first part of the project, we analyze the local economic and social situations of the Moonbucks stores in selected countries around the world. With that, we utilized the trie algorithm to identify the positive, negative, neutral words in the articles. A sentiment analysis is performed to determine whether the article is positively or negatively sentimental. From this insight, we could conclude whether the stores in that particular country have positive or negative economic and social situations for business expansion. The data gained is used to plot bar charts using Plotly to summarize the large set of data in simple visual form based on each category in frequency distribution. 

As Moonbucks decided to have a local central distribution center in each country, the delivery routes for each truck shall be calculated to ensure the delivery is optimized. By using the greedy algorithm, we determined the location of the store in the center. This store shall be the distribution center of at least 5 local stores in the particular country. The shortest delivery route for each truck to make an optimal delivery is then plotted. After that, the program keeps track of the total distance the truck will be making for the delivery for each country. 

The running costs for delivering logistics is also considered for the expansion of business in a country. Based on the calculation done, we used the recommendation algorithm to rank the countries based on the total journey made for deliveries of each country. With the ranking of countries, the location of new stores is recommended for business expansion.

Team members:\
Phang Kean Seng\
Fu Yik Lyn\
Wang Yixiang\
Muhammad Amirul Hakiem bin Sabarudin\
Richie Lau Zhe Chie\
Wan Nazreena binti Wan Ahmed
