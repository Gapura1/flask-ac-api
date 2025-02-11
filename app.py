from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ac_maintenance.db')
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

@app.route('/ac-history/<kode_ac>', methods=['GET'])
def get_ac_history(kode_ac):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kode_ac, tanggal, teknisi, jenis_perawatan, keterangan 
        FROM maintenance_history 
        WHERE kode_ac = ? 
        ORDER BY tanggal DESC 
        LIMIT 6
    """, (kode_ac,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        return jsonify({"error": "No records found for this AC."}), 404
    
    result = [{
        "kode_ac": row["kode_ac"],
        "tanggal": row["tanggal"],
        "teknisi": row["teknisi"],
        "jenis_perawatan": row["jenis_perawatan"],
        "keterangan": row["keterangan"]
    } for row in records]

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
