#!/bin/bash

echo '======= Generating DB dump file...'
PGPASSWORD=postgres pg_dump -d prevejodb -h localhost -U postgres -a -b -n transporte -f /tmp/output.sql

cd /tmp

echo 'begin;' > /tmp/data-postgis.sql
cat /integration/cleanup.sql >> /tmp/data-postgis.sql
cat /tmp/output.sql >> /tmp/data-postgis.sql
echo 'commit;' >> /tmp/data-postgis.sql

echo '======= Output file generated at: [ /tmp/data-postgis.sql ]'

echo '======= Done! Press to exit'
read test

