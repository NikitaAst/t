#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER test_u WITH PASSWORD 'test';
    CREATE DATABASE testdb OWNER test_u;
    GRANT ALL PRIVILEGES ON DATABASE testdb TO test_u;
EOSQL
