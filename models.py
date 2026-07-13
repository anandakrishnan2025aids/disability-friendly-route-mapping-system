# Database Models
import sqlite3
from datetime import datetime

DB_PATH = "accessibility.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Accessibility Points Table
    c.execute('''CREATE TABLE IF NOT EXISTS accessibility_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        status TEXT DEFAULT 'operational',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Routes Table
    c.execute('''CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        distance REAL,
        accessibility_score INTEGER,
        user_type TEXT,
        coordinates TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Facilities Table (Hospitals, Police, etc.)
    c.execute('''CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        address TEXT,
        phone TEXT,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        accessible BOOLEAN DEFAULT 1,
        open_24h BOOLEAN DEFAULT 0
    )''')
    
    # Obstacles Table (Real-time obstacle tracking)
    c.execute('''CREATE TABLE IF NOT EXISTS obstacles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        description TEXT,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        severity TEXT DEFAULT 'medium',
        status TEXT DEFAULT 'active',
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
