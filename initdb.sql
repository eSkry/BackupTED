BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `sync` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`syncid`	INTEGER,
	`date`	NUMERIC,
	`source`	TEXT,
	`dest`	TEXT,
	`zip_name`	TEXT
);
COMMIT;
