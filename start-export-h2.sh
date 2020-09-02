#!/bin/bash

echo '======= Executing [ export-data-h2.sql ] ...'
PGPASSWORD=postgres psql -h localhost -U postgres -d prevejodb -f export-data-h2.sql

cat export-veiculos.sql >> /tmp/data-h2.sql

echo '======= Output file generated at: [ /tmp/data-h2.sql ]'

echo '======= Done! Press to exit'
read test

