import sys, sqlite3, csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QDialog, QFormLayout, QDialogButtonBox, QStatusBar, QScrollArea, QTextEdit, QMainWindow,
    QDockWidget
)
from PyQt5.QtCore import Qt

class DialogEdit(QDialog):
    def __init__(self, id_data, judul, penulis, tahun):
        super().__init__()
        self.setWindowTitle("Edit Data Buku")
        self.setFixedSize(300, 180)
        self.id_data = id_data
        layout = QFormLayout()
        self.in_judul = QLineEdit(judul)
        self.in_penulis = QLineEdit(penulis)
        self.in_tahun = QLineEdit(tahun)
        layout.addRow("Judul:", self.in_judul)
        layout.addRow("Penulis:", self.in_penulis)
        layout.addRow("Tahun:", self.in_tahun)
        tombol = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        tombol.accepted.connect(self.accept)
        tombol.rejected.connect(self.reject)
        layout.addWidget(tombol)
        self.setLayout(layout)

    def get_data(self):
        return self.in_judul.text(), self.in_penulis.text(), self.in_tahun.text()

class AplBuku(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Data Buku")
        self.resize(800, 600)
        self.db()
        self.ui()
        self.load_data()

    def db(self):
        self.kon = sqlite3.connect("data.db")
        self.kur = self.kon.cursor()
        self.kur.execute("""
            CREATE TABLE IF NOT EXISTS buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                penulis TEXT,
                tahun INTEGER
            )
        """)
        self.kon.commit()

    def ui(self):
        pusat = QWidget()
        utama = QVBoxLayout()

        form = QHBoxLayout()
        self.nm = QLineEdit()
        self.pnls = QLineEdit()
        self.thn = QLineEdit()
        self.nm.setPlaceholderText("Judul Buku")
        self.pnls.setPlaceholderText("Penulis")
        self.thn.setPlaceholderText("Tahun")
        form.addWidget(self.nm)
        form.addWidget(self.pnls)
        form.addWidget(self.thn)

        tombol_baris = QHBoxLayout()
        self.tmp = QPushButton("Tempel dari Clipboard")
        self.tmp.clicked.connect(self.tempel)
        self.smpn = QPushButton("Simpan")
        self.smpn.clicked.connect(self.simpan)
        tombol_baris.addWidget(self.tmp)
        tombol_baris.addWidget(self.smpn)

        self.cari = QLineEdit()
        self.cari.setPlaceholderText("Cari judul...")
        self.cari.textChanged.connect(self.cari_data)

        self.tbl = QTableWidget()
        self.tbl.setColumnCount(4)
        self.tbl.setHorizontalHeaderLabels(["ID", "Judul", "Penulis", "Tahun"])
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbl.cellDoubleClicked.connect(self.edit_data)

        bawah = QHBoxLayout()
        self.hps = QPushButton("Hapus")
        self.hps.clicked.connect(self.hapus)
        self.exp = QPushButton("Export CSV")
        self.exp.clicked.connect(self.export)
        bawah.addWidget(self.hps)
        bawah.addWidget(self.exp)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        scroll_area = QScrollArea()
        isi_widget = QWidget()
        isi_layout = QVBoxLayout()
        isi_layout.addLayout(form)
        isi_layout.addLayout(tombol_baris)
        isi_layout.addWidget(self.cari)
        isi_layout.addWidget(self.tbl)
        isi_layout.addLayout(bawah)
        isi_widget.setLayout(isi_layout)
        scroll_area.setWidget(isi_widget)
        scroll_area.setWidgetResizable(True)

        utama.addWidget(scroll_area)

        # Footer
        self.footer = QLabel("Muh. Ressa Arsy Ma'rif | NIM: F1D022137")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("color: gray; font-size: 9pt; padding: 8px;")
        utama.addWidget(self.footer)

        pusat.setLayout(utama)
        self.setCentralWidget(pusat)

        # QDockWidget (Catatan)
        self.catatan = QTextEdit()
        self.catatan.setPlaceholderText("Catatan tambahan...")
        self.dock = QWidget()
        dock_layout = QVBoxLayout()
        dock_layout.addWidget(QLabel("Catatan"))
        dock_layout.addWidget(self.catatan)
        self.dock.setLayout(dock_layout)
        self.dock_area = QDockWidget("Catatan", self)
        self.dock_area.setWidget(self.dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_area)

    def load_data(self):
        self.tbl.setRowCount(0)
        self.kur.execute("SELECT * FROM buku")
        for baris in self.kur.fetchall():
            idx = self.tbl.rowCount()
            self.tbl.insertRow(idx)
            for kol, val in enumerate(baris):
                self.tbl.setItem(idx, kol, QTableWidgetItem(str(val)))

    def simpan(self):
        jdl, pns, th = self.nm.text(), self.pnls.text(), self.thn.text()
        if not (jdl and pns and th.isdigit()):
            QMessageBox.warning(self, "Peringatan", "Isi semua kolom dengan benar!")
            return
        self.kur.execute("INSERT INTO buku (judul, penulis, tahun) VALUES (?, ?, ?)", (jdl, pns, int(th)))
        self.kon.commit()
        self.nm.clear(); self.pnls.clear(); self.thn.clear()
        self.load_data()
        self.status.showMessage("Data disimpan", 3000)

    def tempel(self):
        teks = QApplication.clipboard().text()
        self.nm.setText(teks)
        self.status.showMessage("Judul ditempel dari clipboard", 3000)

    def cari_data(self, teks):
        self.tbl.setRowCount(0)
        self.kur.execute("SELECT * FROM buku WHERE judul LIKE ?", ('%' + teks + '%',))
        for baris in self.kur.fetchall():
            idx = self.tbl.rowCount()
            self.tbl.insertRow(idx)
            for kol, val in enumerate(baris):
                self.tbl.setItem(idx, kol, QTableWidgetItem(str(val)))

    def edit_data(self, baris, kol):
        id_data = int(self.tbl.item(baris, 0).text())
        j, p, t = self.tbl.item(baris, 1).text(), self.tbl.item(baris, 2).text(), self.tbl.item(baris, 3).text()
        dlg = DialogEdit(id_data, j, p, t)
        if dlg.exec_():
            jb, pb, tb = dlg.get_data()
            if not (jb and pb and tb.isdigit()):
                QMessageBox.warning(self, "Peringatan", "Data tidak valid!")
                return
            self.kur.execute("UPDATE buku SET judul=?, penulis=?, tahun=? WHERE id=?", (jb, pb, int(tb), id_data))
            self.kon.commit()
            self.load_data()
            self.status.showMessage("Data diperbarui", 3000)

    def hapus(self):
        baris = self.tbl.currentRow()
        if baris < 0:
            QMessageBox.warning(self, "Pilih data", "Pilih data yang akan dihapus.")
            return
        id_data = int(self.tbl.item(baris, 0).text())
        self.kur.execute("DELETE FROM buku WHERE id=?", (id_data,))
        self.kon.commit()
        self.load_data()
        self.status.showMessage("Data dihapus", 3000)

    def export(self):
        self.kur.execute("SELECT * FROM buku")
        data = self.kur.fetchall()
        with open("data_buku.csv", "w", newline="", encoding="utf-8") as f:
            tulis = csv.writer(f)
            tulis.writerow(["ID", "Judul", "Penulis", "Tahun"])
            tulis.writerows(data)
        QMessageBox.information(self, "Berhasil", "Data disimpan ke data_buku.csv")
        self.status.showMessage("Data diekspor", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AplBuku()
    win.show()
    sys.exit(app.exec_())
