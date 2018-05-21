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
article = "one trader mint million yesterday -lrb- thanks to Twitter and the short-selling firm Citron Research it all start when a trader who remains anonymous wake up and buy over 5,000 put contract of pharmacy benefit manager -lrb- Express script hold Co. -lrb- esrx at the time the contract be sell for $ apiece this be the largest option trade involve esrx stock yesterday and amount to $ `` be unclear of course who this option buyer be and what information they may have be privy to CNBC report last night no matter what prompt the trader to make this move Citron -- a short-selling company famous for target stock that be overvalue -- post the follow tweet about esrx at 1:00 p.m. call it the `` of the pharma industry Philidor be the specialty pharmaceutical company associate with valeant pharmaceutical International Inc. -lrb- vrx -- a corporation that be plague by scandal since August 2015 the two firm once partner to push Valeant high-price drug to patient instead of cheaper generic alternative so it seem those at Citron suspect esrx may be up to shady price practice of its own after the research firm scathing tweet esrx share fall 8 over the course of just one hour -- from $ at 12:30 p.m. down to $ at 1:30 p.m. meanwhile the price of option contract on Express script climb 122 from $ to $ by market close yesterday the anonymous early-morning trader have mint a cool $ million upon hearing this news Citron founder Andrew leave tell CNBC `` money that he be `` that someone -lsb- so heavily off of my work regardless of this disapproval however leave -- as founder of the short-selling firm -- should understand more than anyone else that option trading be all about such `` timing yesterday `` trader simply saw a prime opportunity and he take it money morning global credit strategist Michael E. Lewitt certainly understand the importance of timing trade too he be among the first to call Valeant epic downfall after all thanks to Lewitt extensive research predict how and when the big pharma leviathan would eventually fail he investor net 700 gain in the end and now he have he sight set on another fail company follow money morning on Facebook and Twitter join the conversation click here to jump to comment"
keywords = functions.getKeywords()
print(sfu.analyze_article(article, keywords, nlp))
nlp.close()