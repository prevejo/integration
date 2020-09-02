#!/bin/bash

echo '======= Generating DB output file...'
PGPASSWORD=postgres pg_dump -d prevejodb -h localhost -U postgres -a -b -n $DB_SCHEMA -f /tmp/output.sql

cd /tmp

echo 'begin;' > /tmp/push.sql
cat /integration/cleanup.sql >> /tmp/push.sql
cat /tmp/output.sql >> /tmp/push.sql
echo 'commit;' >> /tmp/push.sql

echo "======= Pushing DB output file to $DB_ADDR:$DB_PORT..."
PGPASSWORD=$DB_PASS psql -q -h $DB_ADDR -p $DB_PORT -d $DB_NAME -U $DB_USER -f /tmp/push.sql
#PGPASSWORD=$DB_PASS pg_restore -h $DB_ADDR -p $DB_PORT -d $DB_NAME -U $DB_USER --single-transaction /tmp/output.sql

echo '======= Done!'