CREATE TABLE IF NOT EXISTS applications (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        essay TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )