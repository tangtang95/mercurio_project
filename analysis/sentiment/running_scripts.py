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
article = "this year have be something of a tease for gold investor -- but we gold price prediction for 2017 see the yellow metal go much higher gold price start the year on a tear by July the spot price of gold have reach $ a ounce a 28.72 jump from the start of 2016 many gold analyst be convinced this rapid rise in gold price signal the start of a new gold bull market but then gold reverse direction since that July 6 peak gold price have slip 15 to $ raise question about whether gold bear market -- which start in September 2011 -- be really over and Wall Street gold price prediction for 2017 have clarify little several bank analyst include those at credit Suisse Group AG -lrb- ADR cs Societe Generale -lrb- ADR scgly and UBS Group AG -lrb- UBS all have average gold price forecast for 2017 of $ or higher but Dutch bank ABN Amro Group NV 2017 gold price prediction see the yellow metal slide below $ a ounce while the gold price forecast of UK trading firm IG Group holding Plc. put it below $ by the end of the year and the 2017 gold price prediction from Citigroup Inc. -lrb- c be basically flat -- a slight drop early in the year follow by a slight gain in the latter part of the year do Miss why now be the best Time to buy gold in five year but for long-term gold investor what matter right now be that we close to the end of the 2011 bear market whether the turnaround start in January or later in 2017 do matter that much consider the gain that lie ahead First of all the current gold bear market at 62 month be well beyond the average age of 50 month it due to reverse gold price be also near a typical bear bottom the bear market that start in 2011 have shave 39 off the price of gold the median of gold bear market loss since 1970 be 42.7 -- pretty close to where we be now but use the low of $ a ounce set at the end of 2015 the deepest loss of the current gold bear market be exactly 44 this suggest that even if the ultimate low for gold price lie in 2017 it will be that much lower on the other hand the next gold bull market will prove extremely profitable -- as this next chart show join the conversation click here to jump to comment"
keywords = functions.getKeywords()
print(sfu.analyze_article(article, keywords, nlp))
nlp.close()