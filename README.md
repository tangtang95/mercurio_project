# Mercurio

## Setup:
- install [Anaconda3](https://www.anaconda.org/)
- install [scrapy](https://www.scrapy.org) library from Anaconda3 Environments
- install [selenium](https://www.seleniumhq.org) library from Anaconda3 Environments
- install [fake-user-agent](https://github.com/alecxe/scrapy-fake-useragent) library from the terminal of the environment
    - ``` pip install scrapy-fake-useragent ```
- install stem from terminal of the environment using:
    - ``` pip install stem ```
- install scrapyd for deploying and running scrapy Spider
    - ``` pip install scrapyd ```
    - ``` pip install git+https://github.com/scrapy/scrapyd-client ```
    
## To read before writing report
- Write each sentence on a separete line. This minimazes merge conflicts.
- Split different chapters into their own files and call them with \include{file} command.
- git config core.autocrlf true    
- Do not write in first person (neither singular or plural), use passive!!!!!!!

## How to deploy the scrapy project:
1. start the server (check scrapy.cfg for the server ip) with the command "scrapyd" wherever you want
2. if your server is remote, then you should first make a port forwarding to the server
```bash
ssh -L localport:localhost:serverport username@ipaddress
#example: ssh -L 9000:localhost:6800 mercurio@192.168.0.2
```
3. first of all make sure you are on the parent folder of your project, then to deploy the project:
```bash
#this command will send your project on the url indicated on the scrapy.cfg file
scrapyd-deploy -p scrapingProject
```
4. if you want to check all the spiders available, use:
```bash
scrapyd-client spiders -p scrapingProject
```
5. to run a spider use:
```bash
scrapyd-client schedule -p scrapingProject spidername
#you can also use the API of scrapyd:
#curl http://localhost:9000/schedule.json -d project=scrapingProject -d spider=spidername
```
6. to cancel a spider:
```bash
curl http://localhost:9000/cancel.json -d project=scrapingProject -d job=jobstring
#the value of jobstring can be found when the spider has just been scheduled or on the website localhost:9000
```
For more information check:
- https://stackoverflow.com/questions/45750739/scrapyd-client-command-not-found
- https://github.com/scrapy/scrapyd-client
- https://scrapyd.readthedocs.io/en/latest/overview.html

## How to interrogate the database through ssh
- list of commands:
```bash
#access into the DB
mysql -uroot -p

#select a database
use databasename;

#show tables
show tables;

#query example
select * from nametable where ....
```

## Proxy IP Rotation Setup (only for Unix OS):
- install tor from terminal (using apt or homebrew)
- install privoxy from terminal (using apt or homebrew)
- add ControlPort 9051 and a password (in the project, the default password is "password") in the tor config file:
```bash
echo "ControlPort 9051" >> /etc/tor/torrc
echo HashedControlPassword $(tor --hash-password "password" | tail -n 1) >> /etc/tor/torrc
``` 
- if the path of tor is already in the PATH variable then you should be able to run tor by just using the command "tor"
- to check if tor works (needs to install *netcat* using apt or homebrew):
```bash
echo -e 'AUTHENTICATE "password"' | nc 127.0.0.1 9051
``` 
- add forwarding port in privoxy config file:
```bash
echo "forward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config
``` 
- if necessary copy the privoxy config file in the privoxy bash/batch file directory and then run it from there
- to check if everything works (needs to install *curl* using apt or homebrew):
```bash
#to request a new ip use this
echo -e 'AUTHENTICATE "password"\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051

curl -x 127.0.0.1:8118 http://icanhazip.com/
```
- for more information go to this [link](https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b)

## Scraping sites:
- [Bloomberg](https://www.bloomberg.com)
- [New York Times](https://www.nytimes.com) (dealbook exist from Feb 2012)
- [This is Money](https://www.thisismoney.co.uk)
- [CNN Money](http://money.cnn.com)
- [Market Watch](https://www.marketwatch.com)
- [Reuters](https://www.reuters.com)
- [Investing](https://www.investing.com)
- [Money Mourning](https://moneymorning.com)

## Datasets:
- https://github.com/philipperemy/financial-news-dataset
- https://github.com/philipperemy/Reuters-full-data-set

## Further info
You can use this for search sites by sites similiraty. Good sites to search from are marketwatch and 4traders
- http://www.moreofit.com/similar-to/www.marketwatch.com/Top_10_Sites_Like_Marketwatch/
