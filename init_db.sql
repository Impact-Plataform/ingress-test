CREATE TABLE IF NOT EXISTS applications
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    apply_id   TEXT,
    name       TEXT,
    email      TEXT,
    phone      TEXT,
    essay      TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)