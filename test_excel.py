import pandas as pd

file_path = r"D:\2025\ITS Ekatalog\riwayat-ac-elektro\Flask Github\flask-ac-api\Riwayat Perawatan AC Elektro.xlsx"

try:
    df = pd.read_excel(file_path, sheet_name="sheet1")
    print("✅ File berhasil dibaca!")
    print(df.head(10))  # Tampilkan 10 baris pertama
except Exception as e:
    print("❌ Gagal membaca file. Pesan error:", str(e))
import sqlite3

# Buat atau hubungkan ke database SQLite
conn = sqlite3.connect("ac_maintenance.db")
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kode_ac TEXT NOT NULL,
        tanggal TEXT NOT NULL,
        teknisi TEXT NOT NULL,
        jenis_perawatan TEXT NOT NULL,
        keterangan TEXT
    )
""")

# Konversi nama kolom agar cocok dengan database
df.rename(columns={
    "KodeAC": "kode_ac",
    "Tanggal": "tanggal",
    "Teknisi": "teknisi",
    "Jenis Perawatan": "jenis_perawatan",
    "Keterangan": "keterangan"
}, inplace=True)

# Konversi tanggal ke format string agar bisa masuk ke SQLite
df["tanggal"] = df["tanggal"].astype(str)

# Masukkan data ke dalam database
data_tuples = list(df.itertuples(index=False, name=None))
cursor.executemany("""
    INSERT INTO maintenance_history (kode_ac, tanggal, teknisi, jenis_perawatan, keterangan)
    VALUES (?, ?, ?, ?, ?)
""", data_tuples)

# Simpan perubahan dan tutup koneksi
conn.commit()
conn.close()

print("✅ Data berhasil dimasukkan ke dalam database SQLite!")
