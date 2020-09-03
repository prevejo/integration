#!/bin/bash

ALREADY_INITIALIZED='NO'
INITIALIZED_FILE='/tmp/INITIALIZED'

if [ -f "$INITIALIZED_FILE" ]; then
	ALREADY_INITIALIZED='YES'
else
	touch $INITIALIZED_FILE
fi


set -e
fail() { : "${error:?$1}"; }


RETRIES=30

until PGPASSWORD=postgres psql -h localhost -U postgres -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
        RETRIES=$((RETRIES-=1))
        echo "======= Waiting for postgres server, $RETRIES remaining attempts..."
        sleep 1
done

if [ "$RETRIES" == "0" ]; then
        echo '======= Database did not initialized in time'
        exit 1
fi

echo ''
echo '======= Database stated'


if [ "$ALREADY_INITIALIZED" == 'YES' ]; then
	echo '======= Database already initialized. Press to exit'
	read test
	exist 0
fi


echo 'create database prevejodb;' > /tmp/tmp.sql
PGPASSWORD=postgres psql -h localhost -U postgres -f /tmp/tmp.sql
echo 'create extension postgis;' > /tmp/tmp.sql
PGPASSWORD=postgres psql -h localhost -U postgres -d prevejodb -f /tmp/tmp.sql
rm -f /tmp/tmp.sql
PGPASSWORD=postgres psql -h localhost -U postgres -d prevejodb -f /integration/schema.sql


cd /integration

echo '======= Starting migration...'
python3 main.py

echo '======= Fetch data complete'


if [ -z "$EXPORT_TYPE" ]; then
	echo "======= No export type. Running only!"
	EXPORT_TYPE='none'
else
	echo "======= Export type: [ $EXPORT_TYPE ]"
fi


echo "EXPORT_TYPE=$EXPORT_TYPE" > $INITIALIZED_FILE


if [ "$EXPORT_TYPE" == "db" ]; then
	if [ -z "$DB_ADDR" ] || [ -z "$DB_PORT" ] || [ -z "$DB_NAME" ] || [ -z "$DB_SCHEMA" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ]; then
		fail 'Missing database parameters!'
	else
		./start-export-db.sh
	fi
elif [ "$EXPORT_TYPE" == "h2" ]; then
	./start-export-h2.sh
elif [ "$EXPORT_TYPE" == "dump" ]; then
	./start-export-dump.sh
else
	echo '======= Creating complete schema...'
	PGPASSWORD=postgres psql -h localhost -U postgres -d prevejodb -f /integration/schema-complete.sql

	echo '======= Running! Press to exit'
	read test
fi
