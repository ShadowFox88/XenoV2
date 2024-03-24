CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    prefix varchar(10) NOT NULL default 'x-'
);

DO $$ BEGIN
    CREATE TYPE blacklist_type AS ENUM ('user', 'guild');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS blacklist (
    id BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    name text NOT NULL,
    type blacklist_type NOT NULL,
    blacklisted_on timestamp with time zone NOT NULL default now(),
    blacklisted_until timestamp with time zone NOT NULL default now() + interval '3 years',
    blacklist_active boolean NOT NULL default true
);

CREATE TABLE IF NOT EXISTS guilds (
    id BIGINT PRIMARY KEY,
    prefix varchar(10) NOT NULL
);