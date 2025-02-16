from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# Template HTML untuk tampilan tabel histori AC
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Riwayat Perawatan AC</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Riwayat Perawatan AC - {{ kode_ac }}</h2>
    {% if history %}
    <table>
        <tr>
            <th>Kode AC</th>
            <th>Tanggal</th>
            <th>Teknisi</th>
            <th>Jenis Perawatan</th>
            <th>Keterangan</th>
        </tr>
        {% for row in history %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
        <p>Data tidak ditemukan untuk kode AC: {{ kode_ac }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return {"message": "API Flask berjalan dengan sukses!"}

@app.route('/ac-history/<kode_ac>', methods=['GET'])
def ac_history(kode_ac):
    try:
        # Koneksi ke database
        conn = sqlite3.connect("ac_maintenance.db")
        cursor = conn.cursor()

        # Query untuk mengambil histori perawatan berdasarkan kode AC
        cursor.execute("""
            SELECT kode_ac, tanggal, teknisi, jenis_perawatan, keterangan
            FROM maintenance_history
            WHERE kode_ac = ?
            ORDER BY tanggal DESC
            LIMIT 6
        """, (kode_ac,))

        rows = cursor.fetchall()
        conn.close()

        # Render data dalam bentuk HTML tabel
        return render_template_string(HTML_TEMPLATE, kode_ac=kode_ac, history=rows)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
