CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    prefix nvarchar(10) NOT NULL default 'x-'
);

CREATE TYPE blacklist_type AS ENUM ('user', 'guild');

CREATE TABLE IF NOT EXISTS blacklist (
    id BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    name text NOT NULL,
    type blacklist_type NOT NULL,
    blacklisted_on timestamp with time zone NOT NULL default now()
    blacklisted_until timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS guilds (
    id BIGINT PRIMARY KEY,
    prefix nvarchar(10) NOT NULL
);