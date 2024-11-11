DROP TABLE IF EXISTS child_groups;
DROP TABLE IF EXISTS parent_groups;

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name TEXT NOT NULL,
    admin_url TEXT UNIQUE NOT NULL, /* should be private */
    addition_url TEXT UNIQUE NOT NULL /* can be public */
);

CREATE TABLE channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL,
    group_id TEXT UNIQUE NOT NULL,
    bot_id TEXT UNIQUE,
    /*
    chan_type enum
    1: a channel that recieves only announcements -- no one within may send things.
    2: a channel that can recieve annonuncements, and select people can send announcements.
    3: a channel in which everyone can send announcements.
    */
    chan_type TEXT CHECK( chan_type in ('1', '2', '3') ) NOT NULL,
    organization INTEGER NOT NULL,
    FOREIGN KEY(organization) REFERENCES organizations(id)
);

CREATE TABLE allowlisted_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    channel INTEGER NOT NULL,
    FOREIGN KEY(channel) REFERENCES channels(id)
);