#!/bin/bash
set -e
fail() { : "${error:?$1}"; }



RETRIES=30

until PGPASSWORD=postgres psql -h localhost -U postgres -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
        RETRIES=$((RETRIES-=1))
        echo "======== Waiting for postgres server, $RETRIES remaining attempts..."
        sleep 1
done

if [ "$RETRIES" == "0" ]; then
        echo '======= Database did not initialized in time'
        exit 1
fi

echo ''
echo '======= Database initialized'

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
	EXPORT_TYPE='dump'
fi


echo "======= Export type: [ $EXPORT_TYPE ]"

if [ "$EXPORT_TYPE" == "db" ]; then
	if [ -z "$DB_ADDR" ] || [ -z "$DB_PORT" ] || [ -z "$DB_NAME" ] || [ -z "$DB_SCHEMA" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ]; then
		fail 'Missing database parameters!'
	else
		./start-export-db.sh
	fi
fi

if [ "$EXPORT_TYPE" == "h2" ]; then
	./start-export-h2.sh
fi

if [ "$EXPORT_TYPE" == "dump" ]; then
	./start-export-dump.sh
fi