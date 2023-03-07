#!/bin/bash
source venv/bin/activate
echo ".read init_db.sql" | sqlite3 applications.db
python3 app/server.py --reload --host=0.0.0.0 --port=80
