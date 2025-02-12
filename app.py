<<<<<<< HEAD
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Fungsi untuk mengambil data perawatan berdasarkan kode AC
def get_maintenance_history(kode_ac):
    try:
        # Hubungkan ke database SQLite
        conn = sqlite3.connect("ac_maintenance.db")
        cursor = conn.cursor()

        # Query untuk mengambil riwayat perawatan berdasarkan kode AC (maksimal 6 data terbaru)
        cursor.execute("""
            SELECT kode_ac, tanggal, teknisi, jenis_perawatan, keterangan
            FROM maintenance_history
            WHERE kode_ac = ?
            ORDER BY tanggal DESC
            LIMIT 6
        """, (kode_ac,))

        rows = cursor.fetchall()

        # Tutup koneksi database
        conn.close()

        # Jika tidak ada data ditemukan, kembalikan pesan error
        if not rows:
            return {"error": f"No records found for AC: {kode_ac}"}

        # Format data menjadi JSON
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
        return {"error": str(e)}

# API Endpoint untuk mendapatkan riwayat perawatan berdasarkan kode AC
@app.route("/ac-history/<kode_ac>", methods=["GET"])
def api_get_history(kode_ac):
    return jsonify(get_maintenance_history(kode_ac))

if __name__ == "__main__":
    app.run(debug=True)
=======
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
>>>>>>> f892fab6ec209db4ba7416fc7e7fdf2c0255adb1
