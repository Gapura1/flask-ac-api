from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Fungsi untuk mengambil data perawatan berdasarkan kode AC
def get_maintenance_history(kode_ac):
    try:
        # Hubungkan ke database SQLite
        db_path = os.path.join(os.getcwd(), "ac_maintenance.db")
        if not os.path.exists(db_path):
            print("⚠️ Database not found! Pastikan file ac_maintenance.db ada di server.")
            return {"error": "Database not found on server"}

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query untuk mengambil data
        cursor.execute("""
            SELECT kode_ac, tanggal, teknisi, jenis_perawatan, keterangan
            FROM maintenance_history
            WHERE kode_ac = ?
            ORDER BY tanggal DESC
            LIMIT 6
        """, (kode_ac,))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"error": f"No records found for AC: {kode_ac}"}

        history = [
            {
                "kode_ac": row[0],
                "tanggal": row[1],
                "teknisi": row[2],
                "jenis_perawatan": row[3],
                "keterangan": row[4]
            }
            for row in rows
        ]

        return {"history": history}
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"error": str(e)}

# Route API untuk mengambil data perawatan
@app.route('/ac-history/<kode_ac>', methods=['GET'])
def ac_history(kode_ac):
    return jsonify(get_maintenance_history(kode_ac))

# Menjalankan server di Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Menggunakan port dari environment Render
    from waitress import serve  # Pastikan waitress sudah diinstal
    print(f"🚀 Server berjalan di http://0.0.0.0:{port}")
    serve(app, host="0.0.0.0", port=port)
@app.route('/')
def home():
    return jsonify({"message": "API Flask berjalan dengan sukses!"})
