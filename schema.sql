DO $$ BEGIN
    CREATE TYPE entity_type AS ENUM ('user', 'guild');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS entities (
    id BIGINT PRIMARY KEY,
    prefix varchar(10) NOT NULL default 'x-',
    entity_type entity_type NOT NULL
);

CREATE TABLE IF NOT EXISTS blacklist (
    id BIGINT REFERENCES entities(id) ON DELETE CASCADE,
    name text NOT NULL,
    entity_type entity_type NOT NULL,
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
);

CREATE TABLE IF NOT EXISTS errors (
    id SERIAL PRIMARY KEY,
    command text NOT NULL,
    user_id BIGINT NOT NULL,
    guild_id BIGINT,
    traceback text NOT NULL,
    error_time timestamp with time zone NOT NULL default now(),
    developer_message_id BIGINT
);

DO $$ BEGIN
        CREATE TYPE a_status AS ENUM ('RELEASING', 'COMPLETED');
    EXCEPTION
        WHEN duplicate_object THEN null;
END$$;

DO $$ BEGIN
        CREATE TYPE season AS ENUM ('WINTER', 'SPRING', 'SUMMER', 'FALL');
    EXCEPTION
        WHEN duplicate_object THEN null;
END$$;

DO $$ BEGIN
        CREATE TYPE media_type AS ENUM ('ANIME', 'MANGA');
    EXCEPTION
        WHEN duplicate_object THEN null;
END$$;

DO $$ BEGIN
        CREATE TYPE source AS ENUM ('ORIGINAL', 'MANGA', 'LIGHT_NOVEL', 'VISUAL_NOVEL', 'VIDEO_GAME', 'OTHER', 'NOVEL', 'DOUJINSHI', 'ANIME', 'WEB_NOVEL', 'LIVE_ACTION', 'GAME', 'COMIC', 'MULTIMEDIA_PROJECT', 'PICTURE_BOOK');
    EXCEPTION
        WHEN duplicate_object THEN null;
END$$;

DO $$ BEGIN
        CREATE TYPE format AS ENUM ('TV', 'TV_SHORT', 'MOVIE', 'SPECIAL', 'OVA', 'ONA', 'MUSIC', 'MANGA', 'NOVEL', 'ONE_SHOT');
    EXCEPTION
        WHEN duplicate_object THEN null;
END$$;

/*
CREATE TABLE media {
    id_al PRIMARY KEY,
    id_mal INT NOT NULL UNIQUE,
    title_english TEXT,
    title_romaji TEXT,
    title_native TEXT NOT NULL,
    media_type media_type NOT NULL,
    format format NOT NULL,
    a_status a_status NOT NULL,
    description TEXT NOT NULL,
    season season NOT NULL,
    season_year INT NOT NULL,
    start_date DATE,
    end_date DATE,
    episodes INT,
    chapters INT,
    volumes INT,
    country_of_origin varchar(2),
    is_licensed BOOLEAN NOT NULL,
    source media_source NOT NULL,
    cover_image TEXT,
    banner_image TEXT,
    genres TEXT[],
    synonyms TEXT[],
    tags TEXT[],
    popularity INT,
    favourites INT,
    is_locked BOOLEAN NOT NULL,
    studios TEXT[],
    is_adult BOOLEAN NOT NULL,
    site_url TEXT NOT NULL,
    created_on TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
}

CREATE TABLE airing {
    id SERIAL PRIMARY KEY,
    anime_id INT REFERENCES media(id_al) ON DELETE CASCADE,
    episode INT NOT NULL,
    airing_at TIMESTAMP WITH TIME ZONE NOT NULL,
}

CREATE TABLE airing_reminders {
    webhook_url TEXT NOT NULL PRIMARY KEY,
    anime_id INT REFERENCES media(id_al) ON DELETE CASCADE;
    reminder_time TIMESTAMP WITH TIME ZONE NOT NULL REFERENCES airing(airing_at) ON UPDATE CASCADE ON DELETE CASCADE;
}

CREATE RULE delete_old_update AS ON UPDATE to media
    DO DELETE FROM media WHERE created_on < now() - interval '3 days';

CREATE RULE delete_old_insert AS ON INSERT to media
    DO DELETE FROM media WHERE created_on < now() - interval '3 days';
*/