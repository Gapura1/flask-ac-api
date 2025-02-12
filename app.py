import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def get_maintenance_history(kode_ac):
    try:
        # Hubungkan ke database SQLite
        conn = sqlite3.connect("ac_maintenance.db")
        cursor = conn.cursor()

        # Ambil data berdasarkan Kode AC
        cursor.execute("SELECT * FROM maintenance_history WHERE kode_ac = ? ORDER BY tanggal DESC LIMIT 6", (kode_ac,))
        rows = cursor.fetchall()

        # Tutup koneksi database
        conn.close()

        # Jika tidak ada data ditemukan
        if not rows:
            return {"error": "No records found for this AC."}

        # Format data menjadi JSON
        history = [
            {
                "kode_ac": row[1],
                "tanggal": row[2],
                "teknisi": row[3],
                "jenis_perawatan": row[4],
                "keterangan": row[5]
            }
            for row in rows
        ]

        return {"history": history}
    
    except Exception as e:
        return {"error": str(e)}

@app.route("/ac-history/<kode_ac>", methods=["GET"])
def api_get_history(kode_ac):
    return jsonify(get_maintenance_history(kode_ac))

if __name__ == "__main__":
    app.run(debug=True)
