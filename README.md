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
- for a more detailed information go to this [link](https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b)

Sites:
- [Bloomberg](https://www.bloomberg.com) (scrapy)
- [New York Times](https://www.nytimes.com) (dealbook exist from Feb 2012 -> scrapy + selenium)
- [Forbes](https://www.forbes.com) (selenium)
- [This is Money](https://www.thisismoney.co.uk) (scrapy)

Datasets:
- https://github.com/philipperemy/financial-news-dataset
- https://github.com/philipperemy/Reuters-full-data-set
