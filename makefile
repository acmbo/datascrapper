#IMG_NAME = jmoddev
#COMMAND_RUN=docker run \
#	  --name ${IMG_NAME} \
#	  --rm \
# 	  -it \
#	  -p 127.0.0.1:8000:8000
#old: 
#	$(COMMAND_RUN) --detach=false ${IMG_NAME} /bin/bash  


.ONESHELL: # Applies to every targets in the file!


start:
	$(info Initialize Redis Server)
	cd src/db && sudo redis-server redis.conf --dbfilename "redis_dw_db.rdb" --daemonize yes --logfile dw_db.log
	cd .. && python3 slug.py
	#python src/db/redis_db_back.py #Placeholder for backup creation
	
	

stop:
	$(info Stopping Redis) 
	redis-cli -p 6378 save 
	redis-cli -p 6378 shutdown 

save:
	redis-clis -p 6378 save 
	

init:
	/etc/init.d/redis-server start

connect:
	$(info Initialize Redis Server)
	cd src/db && sudo redis-server redis.conf --dbfilename "redis_dw_db.rdb" --daemonize yes --logfile dw_db.log

	
	
