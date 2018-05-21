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
article = "despite heroic profit report by two of the fang -- Facebook Inc. -lrb- fb and Amazon.com Inc. -lrb- amzn -- stock have a very rough week the Dow Jones Industrial average fall 230 point or 1.28 to 17,773.64 while the S&P 500 lose 26 point of 1.26 to 2065.30 the Nasdaq Composite index lose 2.67 to 4775.36 as Facebook and Amazon suck the air and much of the profitability out of the room in the technology sector the other half of the fang Apple Inc. -lrb- aapl and alphabet Inc. -lrb- googl take it on the chin after disappointing investor and Apple in particular be struggle with the law of large number a phenomenon that Amazon and Facebook will eventually have to deal with the overall market be still very expensive and three of the four fang -lrb- than aapl remain in a bubble but here what I really want to talk to you about today but the real story over the first four month of the year be the pullback in the U.S. dollar and the recovery in oil price from they low the U.S. dollar index hit 93 this week down from 98.85 at the begin of the year the drop in the dollar be a major contributor to higher oil price -lrb- oil be trade in dollar around the world West Texas Intermediate -lrb- crude close the week at $ up sharply from the mid earlier this year this rally be far from enough to save the many oil and gas company that file for bankruptcy in the United States -lrb- and count and the many more that will but it be better than a poke in the eye the question of course be whether the rally will continue the answer to that question largely depend on what happen to the dollar higher oil price will lead to more production the next leg in any sustained rally will require additional dollar weakness of course the dollar weaken this year because the Fed be weak -- weak in mind weak in will weak in intellect and weak in character Janet Yellen and she confederacy of dunce refuse to normalize interest rate because they paint we economy into a trap every level of we economy be bury in too much debt -- both the public and private sector no doubt higher interest rate will cause problem for overleveraged government business and consumer but leave interest rate at near zero encourage capital to be misallocate to unproductive activity such as consumption housing ill-advised m&a transaction that temporarily enrich short-term orient shareholder and executive overprice stock buyback and other form of speculation that do nothing to enhance the productive capacity of the economy further low interest rate do not lead economic actor to spend more money like the Fed model forecast but instead cause they to act more cautiously and save in sum current policy backfire and produce slower growth and more debt it must be reverse even though it will cause some short-term pain because that be the only way to produce better long-term result but we must take the world as it be not as we would like it to be and the world as it be feature a feckless Fed that be not go to raise rate aggressively at most we may see one interest rate hike this year investor be foolishly root for the Fed and other central bank to chicken out and do nothing the reaction last week to the Bank of Japan decision not to take addition action to lower interest rate further below zero be a case in point -- market sell off market want central bank to take additional ease measure even though they be work they should be careful what they wish for Central bank lower interest rate -lrb- in Europe and Japan means lower they further below zero and buy asset -lrb- in Europe means buy corporate bond and in Japan means buy equity be destroy normal market function the normal function of government and corporate bond market in Europe and Japan have be destroy by central bank buy trillion of dollar of bond these market no longer send meaningful pricing signal and have no liquidity while they influence on equity market be less direct sooner or later central bank will corrupt these market as well we clearly have a bond bubble around the world -lrb- the U.S. as a result of central bank buy trillion of dollar of government bond in they QE program if central bank start buy more equity we could see a similar phenomenon in stock market we know that some central bank like the swiss own large amount of stock like Apple Inc. -lrb- aapl the Bank of Japan own large chunk of the japanese stock market if these practice spread market could become even more distorted than they already be Stock price might stay high but at what cost Central bank be solve the problem of slow economic growth by engage in these practice -- they be corrupt market and make thing worse they need to stop valeant pharmaceutical International Ltd. -lrb- vrx finally file its year-end financial on Friday as expect the report reveal a company with serious problem in addition to disclose that two more state be investigate its unsavory business practice it reveal a even more leveraged balance sheet than expect the company lose more money in the fourth quarter of 2015 than previously disclose and report higher amount of goodwill and intangible asset than expect valeant be a house of card that its new CEO who break he contract with he previous employer to join the company will not be able to fix vrx share drop after the report be release and I believe it be go lower as the company struggle to stay alive investor should buy long-dated put as a low-risk way to profit from this company financial and moral carnage Michael valeant pharmaceutical shorts have return more than 700 to date and he plan more to get in on they click here to be subscribe to Michael sure money investor service twice each week he tell you what head up and what head down and how to make money on both you also get he latest investor briefing on how to profit from `` stock join the conversation click here to jump to comment"
keywords = functions.getKeywords()
print(sfu.analyze_article(article, keywords, nlp))
nlp.close()