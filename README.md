# Kicker Scraper Repo

Websitescrape to gather data from German news websitese dw.com/dw. The project aims to create a database out of:
  * articles
  * keywords
  * article meta: author, post date, recomendations


# Setup Databases

The Scrapper can utilize two kinds of databases:
-mongodb
-redis
Both are NoSQL Databases, which can operate on different system and can be used to store and query documents. Because of the ease of use of NoSQL and the possibilitys of flexible choosing the of amount data to store behind keys in a NoSQL database, these both were choosen for this porject. 

Several different hardware architectures were avialbe at the beginning of the project (RaspberryPi ARM32 and Normal Ubuntu Server 64bit), so different implementations were needed.


## Setting up the database structure

Setting up the mongodb is straight forward.

1. Follow the steps to install and start a localhost:27017 mongodb server [Link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
2. Run mongo.py within the src/db folder

Setting up redis is a bit more tedious:
1. Install redis according to the [project website](https://redis.io/topics/quickstart)
2. Install redis-py with pip [Link](https://pypi.org/project/redis/). If you use conda follow [Link](https://anaconda.org/anaconda/redis)






