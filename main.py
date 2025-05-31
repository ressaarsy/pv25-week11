import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QScrollArea,
    QStatusBar, QDockWidget, QTextEdit, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AplikasiCRUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi CRUD - Week 11")
        self.setMinimumSize(825, 500)

        self.data = []

        self.lbl_nama = QLabel("Nama:")
        self.lbl_nama.setFont(QFont("Arial", 10))
        self.inp_nama = QLineEdit()
        self.inp_nama.setPlaceholderText("Masukkan nama")

        self.btn_tempel = QPushButton("Tempel dari Clipboard")
        self.btn_tempel.clicked.connect(self.tempel_clipboard)

        self.lbl_alamat = QLabel("Alamat:")
        self.lbl_alamat.setFont(QFont("Arial", 10))
        self.inp_alamat = QLineEdit()
        self.inp_alamat.setPlaceholderText("Masukkan alamat")

        self.btn_tambah = QPushButton("Tambah")
        self.btn_tambah.clicked.connect(self.tambah_data)

        self.btn_ubah = QPushButton("Ubah")
        self.btn_ubah.clicked.connect(self.ubah_data)

        self.btn_hapus = QPushButton("Hapus")
        self.btn_hapus.clicked.connect(self.hapus_data)

        layout_form = QVBoxLayout()
        layout_form.setSpacing(10)
        layout_form.addWidget(self.lbl_nama)
        layout_form.addWidget(self.inp_nama)
        layout_form.addWidget(self.btn_tempel)
        layout_form.addWidget(self.lbl_alamat)
        layout_form.addWidget(self.inp_alamat)
        layout_form.addWidget(self.btn_tambah)
        layout_form.addWidget(self.btn_ubah)
        layout_form.addWidget(self.btn_hapus)
        layout_form.addStretch()

        form = QWidget()
        form.setLayout(layout_form)

        scroll_form = QScrollArea()
        scroll_form.setWidgetResizable(True)
        scroll_form.setWidget(form)
        scroll_form.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.tbl = QTableWidget()
        self.tbl.setColumnCount(2)
        self.tbl.setHorizontalHeaderLabels(["Nama", "Alamat"])
        self.tbl.setSelectionBehavior(self.tbl.SelectRows)
        self.tbl.cellClicked.connect(self.pilih_baris)
        self.tbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splt = QSplitter(Qt.Horizontal)
        splt.addWidget(scroll_form)
        splt.addWidget(self.tbl)
        splt.setStretchFactor(1, 2)

        dock = QDockWidget("Bantuan", self)
        self.txt_bantuan = QTextEdit()
        self.txt_bantuan.setReadOnly(True)
        self.txt_bantuan.setText(
            "Petunjuk:\n"
            "- Isi nama dan alamat\n"
            "- Klik Tambah untuk simpan\n"
            "- Klik baris di tabel lalu Ubah atau Hapus\n"
            "- Gunakan tombol 'Tempel dari Clipboard' untuk menempel data dari luar"
        )
        dock.setWidget(self.txt_bantuan)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        status = QStatusBar()
        status.setStyleSheet("QStatusBar{padding-right:12px;}")
        lbl_kredit = QLabel("Muh. Ressa A.M | NIM: F1D022137")
        status.addPermanentWidget(lbl_kredit)
        self.setStatusBar(status)

        isi = QWidget()
        layout_utama = QVBoxLayout()
        layout_utama.addWidget(splt)
        isi.setLayout(layout_utama)
        self.setCentralWidget(isi)

    def tempel_clipboard(self):
        teks = QApplication.clipboard().text()
        self.inp_nama.setText(teks)

    def tambah_data(self):
        nama = self.inp_nama.text().strip()
        alamat = self.inp_alamat.text().strip()
        if nama and alamat:
            self.data.append((nama, alamat))
            self.refresh_tbl()
            self.kosongkan_input()

    def ubah_data(self):
        baris = self.tbl.currentRow()
        if baris >= 0:
            nama = self.inp_nama.text().strip()
            alamat = self.inp_alamat.text().strip()
            self.data[baris] = (nama, alamat)
            self.refresh_tbl()
            self.kosongkan_input()

    def hapus_data(self):
        baris = self.tbl.currentRow()
        if baris >= 0:
            del self.data[baris]
            self.refresh_tbl()
            self.kosongkan_input()

    def pilih_baris(self, baris, kolom):
        nama, alamat = self.data[baris]
        self.inp_nama.setText(nama)
        self.inp_alamat.setText(alamat)

    def refresh_tbl(self):
        self.tbl.setRowCount(0)
        for i, (nama, alamat) in enumerate(self.data):
            self.tbl.insertRow(i)
            self.tbl.setItem(i, 0, QTableWidgetItem(nama))
            self.tbl.setItem(i, 1, QTableWidgetItem(alamat))

    def kosongkan_input(self):
        self.inp_nama.clear()
        self.inp_alamat.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AplikasiCRUD()
    win.show()
    sys.exit(app.exec_())
