from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector

app = Flask(__name__)

db = connector.connect(
    host     = "localhost",
    user     = "root",
    passwd   = "",
    database = "db_photowae"
)
if db.is_connected():
    print("Berhasil Terhubung ke Database")

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/list/')
def halaman_awal():
    cur = db.cursor()
    cur.execute("select * from reservasi")
    res = cur.fetchall()
    cur.close()
    return render_template('index.html', hasil=res)

@app.route('/reservasi/')
def tambah_data():
    return render_template('pesan.html')

@app.route('/pesan/', methods=['POST'])
def pesan():
    nama = request.form['nama']
    kontak = request.form['kontak']
    tgl_reservasi = request.form['tgl_reservasi']
    jam = request.form['jam']
    paket = request.form['paket']
    cur = db.cursor()
    cur.execute('INSERT INTO reservasi (nama, kontak, tgl_reservasi, jam, paket) VALUES (%s, %s, %s, %s, %s)', (nama, kontak, tgl_reservasi, jam, paket))
    db.commit()
    return redirect(url_for('halaman_awal'))


@app.route('/hapus/<nama>', methods=['GET'])
def hapus_data(nama):
    cur = db.cursor()
    cur.execute('DELETE from reservasi where nama=%s', (nama,))
    db.commit()
    return redirect(url_for('halaman_awal'))

if __name__ == '__main__':
    app.run()

