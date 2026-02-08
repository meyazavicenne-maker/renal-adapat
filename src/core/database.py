import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "renal_drugs.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=20)
    # Enable Write-Ahead Logging for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

def search_drugs(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    wildcard = f"%{query}%"
    cursor.execute("SELECT id, name FROM drugs WHERE name LIKE ? ORDER BY name LIMIT 50", (wildcard,))
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return results

def get_drug_details(drug_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM drugs WHERE id = ?", (drug_id,))
    row = cursor.fetchone()
    
    
    # Create tables if they don't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            drug_id INTEGER PRIMARY KEY,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(drug_id) REFERENCES drugs(id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_id INTEGER,
            viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(drug_id) REFERENCES drugs(id)
        )
    """)
    
    conn.close()
    return dict(row) if row else None

# --- Favorites ---

def toggle_favorite(drug_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM favorites WHERE drug_id = ?", (drug_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM favorites WHERE drug_id = ?", (drug_id,))
        is_fav = False
    else:
        cursor.execute("INSERT INTO favorites (drug_id) VALUES (?)", (drug_id,))
        is_fav = True
        
    conn.commit()
    conn.close()
    return is_fav

def is_favorite(drug_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorites WHERE drug_id = ?", (drug_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_favorites():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.*, 1 as is_favorite 
        FROM drugs d
        JOIN favorites f ON d.id = f.drug_id
        ORDER BY d.name
    """)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

# --- History ---

def add_to_history(drug_id):
    conn = get_db_connection()
    # Keep only last 50 entries
    # 1. Insert new
    conn.execute("INSERT INTO history (drug_id) VALUES (?)", (drug_id,))
    
    # 2. Cleanup old (keep last 50)
    conn.execute("""
        DELETE FROM history 
        WHERE id NOT IN (
            SELECT id FROM history ORDER BY viewed_at DESC LIMIT 50
        )
    """)
    
    conn.commit()
    conn.close()

def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query to get unique drugs sorted by last view time
    cursor.execute("""
        SELECT d.*, MAX(h.viewed_at) as last_viewed
        FROM history h
        JOIN drugs d ON h.drug_id = d.id
        GROUP BY d.id
        ORDER BY last_viewed DESC
    """)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def update_drug(drug_id, updates):
    """
    Updates drug fields.
    updates: dict of field_name -> new_value
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Filter allowed fields to prevent injection or errors
    allowed_fields = ["name", "clinical_use", "dose_normal", "dose_renal_impairment"]
    
    set_clauses = []
    values = []
    
    for field, value in updates.items():
        if field in allowed_fields:
            set_clauses.append(f"{field} = ?")
            values.append(value)
            
    if not set_clauses:
        conn.close()
        return False
        
    values.append(drug_id)
    sql = f"UPDATE drugs SET {', '.join(set_clauses)} WHERE id = ?"
    
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return True

def clear_history():
    conn = get_db_connection()
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()
