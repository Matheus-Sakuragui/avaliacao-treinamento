SELECT 'CREATE DATABASE sdb' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sdb');
\connect sdb;
CREATE SCHEMA IF NOT EXISTS stemplate;