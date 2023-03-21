CREATE TABLE IF NOT EXISTS gdpr_metadata
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    purpose          VARCHAR,
    ttl              VARCHAR,
    target_table     VARCHAR,
    target_column    VARCHAR,
    origin           VARCHAR,
    start_time       VARCHAR,
    legally_required INTEGER
);




CREATE TABLE IF NOT EXISTS user_metadata
(
    user_id                  INTEGER,
    metadata_id              INTEGER,
    objection                INTEGER,
    automated_decisionmaking INTEGER,
    PRIMARY KEY (user_id, metadata_id),
    FOREIGN KEY (metadata_id) REFERENCES gdpr_metadata (id)
);

CREATE TABLE IF NOT EXISTS personal_data_processing
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    metadata_id INTEGER,
    process     VARCHAR,
    FOREIGN KEY (metadata_id) REFERENCES gdpr_metadata (id)
);