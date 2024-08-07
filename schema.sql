DO $$ BEGIN
    CREATE TYPE entity_type AS ENUM ('user', 'guild');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

<<<<<<< HEAD
CREATE TABLE IF NOT EXISTS entities (
=======
CREATE TABLE IF NOT EXISTS users (
>>>>>>> c16029a6b0d57be697520862db627724b9f44afb
    id BIGINT PRIMARY KEY,
    prefix varchar(10) NOT NULL default 'x-',
    type entity_type NOT NULL
);

<<<<<<< HEAD
=======





>>>>>>> c16029a6b0d57be697520862db627724b9f44afb
CREATE TABLE IF NOT EXISTS blacklist (
    id BIGINT REFERENCES entities(id) ON DELETE CASCADE,
    name text NOT NULL,
    type entity_type NOT NULL,
    blacklist_reason text NOT NULL default 'No reason provided',
    blacklisted_on timestamp with time zone NOT NULL default now(),
    blacklisted_until timestamp with time zone NOT NULL default now() + interval '888 years', -- Lifetime by default
    blacklist_active boolean NOT NULL default true
);

DO $$ BEGIN
    CREATE TYPE channel_type AS ENUM ('text', 'voice');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

<<<<<<< HEAD
=======




>>>>>>> c16029a6b0d57be697520862db627724b9f44afb
-- thanks Leo: https://github.com/DuckBot-Discord/duck-hideout-manager-bot/blob/main/schema.sql
DO $$
BEGIN
        CREATE TYPE archive_mode AS ENUM ('leave', 'inactive', 'manual');
    EXCEPTION
        WHEN duplicate_object THEN null;
END$$;

CREATE TABLE IF NOT EXISTS user_channels (
    owner BIGINT PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    channel_id BIGINT NOT NULL,
    channel_type channel_type NOT NULL,
    archive_mode archive_mode
)