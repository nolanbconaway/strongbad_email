-- clear everything out
PRAGMA writable_schema = 1;
delete from sqlite_master where type in ('table', 'index', 'trigger', 'view');
PRAGMA writable_schema = 0;
VACUUM;
PRAGMA INTEGRITY_CHECK;

DROP TABLE IF EXISTS email;
CREATE TABLE email (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  homestarrunner_url TEXT NOT NULL, -- http://homestarrunner.com/sbemail{id}.html
  hrwiki_url TEXT NOT NULL
);

CREATE UNIQUE INDEX email_id on email (id);
CREATE INDEX email_title on email (title);
