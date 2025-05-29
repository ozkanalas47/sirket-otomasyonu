from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QMessageBox, QTextEdit, QLineEdit, QInputDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from datetime import datetime


class SirketOtomasyon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alas  Şirket")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("Alas Şirket")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.button_container = QVBoxLayout()
        self.layout.addLayout(self.button_container)

        self.add_button("Çalışan Ekle", self.add_employee)
        self.add_button("Çalışanları Listele", self.list_employees)
        self.add_button("Gelir Detaylarını Görüntüle", self.view_income_details)
        self.add_button("Bütçeyi Görüntüle", self.view_budget)
        self.add_button("Masraf Gir", self.add_expense)

        self.info_label = QLabel("Alt bilgiler burada görüntülenecek.")
        self.info_label.setFont(QFont("Arial", 10))
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: black;")
        self.layout.addWidget(self.info_label)

    def add_button(self, text, method):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet(
            "background-color: #007ACC; color: white; padding: 10px; border-radius: 5px;"
        )
        button.clicked.connect(method)
        self.button_container.addWidget(button)

    def add_employee(self):

        try:
            ad = self.get_input("Çalışanın adı:")
            soyad = self.get_input("Çalışanın soyadı:")
            yas = self.get_input("Çalışanın yaşı:")
            cinsiyet = self.get_input("Çalışanın cinsiyeti:")
            maas = self.get_input("Çalışanın maaşı:")

            with open("calisanlar.txt", "a") as file:
                file.write(f"{ad} {soyad}, Yaş: {yas}, Cinsiyet: {cinsiyet}, Maaş: {maas} TL\n")

            QMessageBox.information(self, "Başarılı", "Çalışan başarıyla eklendi!")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Çalışan eklenirken bir hata oluştu: {str(e)}")

    def list_employees(self):

        try:
            with open("calisanlar.txt", "r") as file:
                employees = file.readlines()

            if not employees:
                raise FileNotFoundError

            employees_text = "\n".join([emp.strip() for emp in employees])


            self.list_window = QWidget()
            self.list_window.setWindowTitle("Çalışanlar")
            self.list_window.setGeometry(300, 300, 400, 300)

            layout = QVBoxLayout()
            text_area = QTextEdit()
            text_area.setText(employees_text)
            text_area.setReadOnly(True)
            text_area.setStyleSheet("color: black; font-size: 14px; background-color: white;")
            layout.addWidget(text_area)

            self.list_window.setLayout(layout)
            self.list_window.show()

        except FileNotFoundError:
            QMessageBox.warning(self, "Hata", "Çalışan listesi bulunamadı!")

    def view_income_details(self):

        try:
            with open("gelir_detay.txt", "r") as file:
                income_details = file.readlines()

            if not income_details:
                raise FileNotFoundError

            income_text = "\n".join([detail.strip() for detail in income_details])

            self.income_window = QWidget()
            self.income_window.setWindowTitle("Gelir Detayları")
            self.income_window.setGeometry(300, 300, 400, 300)

            layout = QVBoxLayout()
            text_area = QTextEdit()
            text_area.setText(income_text)
            text_area.setReadOnly(True)
            text_area.setStyleSheet("color: black; font-size: 14px; background-color: white;")
            layout.addWidget(text_area)

            self.income_window.setLayout(layout)
            self.income_window.show()

        except FileNotFoundError:
            QMessageBox.warning(self, "Hata", "Gelir detayları bulunamadı!")

    def view_budget(self):

        try:
            with open("butce.txt", "r") as file:
                budget = file.read().strip()

            QMessageBox.information(self, "Bütçe", f"Mevcut bütçe: {budget} TL")
        except FileNotFoundError:
            QMessageBox.warning(self, "Hata", "Bütçe dosyası bulunamadı!")

    def add_expense(self):

        try:
            masraf = int(self.get_input("Masraf tutarını giriniz:"))
            masraf_turu = self.get_input("Masraf türünü belirtiniz:")
            aciklama = self.get_input("Masraf ile ilgili açıklama giriniz:")

            with open("butce.txt", "r") as file:
                mevcut_butce = int(file.read().strip())

            mevcut_butce -= masraf

            with open("butce.txt", "w") as file:
                file.write(str(mevcut_butce))

            tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("masraflar.txt", "a") as file:
                file.write(f"{tarih} - {masraf_turu} - {masraf} TL - {aciklama}\n")

            QMessageBox.information(self, "Başarılı", f"Masraf kaydedildi. Yeni bütçe: {mevcut_butce} TL")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Masraf eklenirken bir hata oluştu: {str(e)}")

    def get_input(self, prompt):
        text, ok = QInputDialog.getText(self, "Giriş Yapın", prompt)
        if ok and text:
            return text
        else:
            raise ValueError(f"{prompt} zorunludur.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SirketOtomasyon()
    window.show()
    sys.exit(app.exec_())
