CREATE TABLE USER_INFO(
   	email TEXT PRIMARY KEY UNIQUE,
    hl_options TEXT NOT NULL,
    sl_options TEXT NOT NULL,
    subject_conf BOOLEAN NOT NULL,
    career_path TEXT NOT NULL,
    career_conf BOOLEAN NOT NULL
);

