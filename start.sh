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


if [ -z "$DB_ADDR" ]; then
	fail 'Parameter DB_ADDR not set'
fi
if [ -z "$DB_PORT" ]; then
	fail 'Parameter DB_PORT not set'
fi
if [ -z "$DB_NAME" ]; then
	fail 'Parameter DB_NAME not set'
fi
if [ -z "$DB_SCHEMA" ]; then
	fail 'Parameter DB_SCHEMA not set'
fi
if [ -z "$DB_USER" ]; then
	fail 'Parameter DB_USER not set'
fi
if [ -z "$DB_PASS" ]; then
	fail 'Parameter DB_PASS not set'
fi

cd /integration

echo '======= Starting migration...'
python3 main.py

echo '======= Exporting data...'
PGPASSWORD=postgres pg_dump -d prevejodb -h localhost -U postgres -a -b -n $DB_SCHEMA -f /tmp/output.sql

cd /tmp

echo 'begin;' > /tmp/push.sql
cat /integration/cleanup.sql >> /tmp/push.sql
cat /tmp/output.sql >> /tmp/push.sql
echo 'commit;' >> /tmp/push.sql

PGPASSWORD=$DB_PASS psql -q -h $DB_ADDR -p $DB_PORT -d $DB_NAME -U $DB_USER -f /tmp/push.sql
#PGPASSWORD=$DB_PASS pg_restore -h $DB_ADDR -p $DB_PORT -d $DB_NAME -U $DB_USER --single-transaction /tmp/output.sql

echo '======= Done!'
