# -*- coding: utf-8 -*-
'''
Files used to run some temporary scripts regarding utilies, like files 
operation that need to be done only once

This is an example of how to use sentiment_function
'''
import utilities.functions as functions
import sentiment.sentiment_function as sfu
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'C:\Users\User.LAPTOP-FG37H74P\Desktop\stanford-corenlp-full-2018-02-27\stanford-corenlp-full-2018-02-27')
article = "TripAdvisor Inc (NASDAQ:TRIP) released its quarterly earnings on Tuesday which impressed investors despite profits being down from a year ago. Adjusted per-share earnings of $0.30 were nearly double the $0.16 that analysts were expecting from the company this quarter.Revenues for the period also came in above estimates as TripAdvisor accumulated $378 million in sales, well above the $360.9 million that was expected.Another metric that is key to TripAdvisor is its user reviews and opinions, which were up 26% from last year. Across all of its websites, the company also saw a growth in monthly unique visitors, with traffic up by 12%.Investors were very excited by the results as TripAdvisor’s stock was up 20% in after-hours trading. The stock remains a great buy today as it has generated strong growth over the years, with revenues increasing 65% over the past four years. Outside of its most recent fiscal year, TripAdvisor has also been doing a good job of staying in the black, averaging a profit margin of over 14% during the previous four years.The website has grown in popularity and it has become the authority for online travel reviews. And as the economy continues to grow and with disposable income on the rise, more people will be traveling and in search of places to stay and visit.However, it hasn’t been all smooth sailing for the stock as over the past five years it has declined nearly 30%, although year-to-date the share price has risen 14%. These results are a good sign for the stock and suggest that it still has a lot of potential to grow, making it a great long-term buy."
keywords = functions.getKeywords()
print(sfu.analyze_article(article, keywords, nlp))
nlp.close()