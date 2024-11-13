import os
import re
import sys
import uuid
import time
import random
import socket
import base64
import shutil
import ctypes
import sqlite3
import asyncio
import requests
import threading
import urllib.parse
import pandas as pd
from datetime import datetime
from PyQt6 import QtWidgets, QtCore, QtGui
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def check_internet():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def check_internet_sockets():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setWindowTitle('Emrah Abi Program')

        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.gap_of_bottom = int(self.screen_height / 100 * 7)
        self.gap_of_sides = int(self.screen_width / 100 * 1)
        self.gap_of_top = int(self.screen_width / 100 * 2)
        self.one_four_of_width = int((self.screen_width - self.gap_of_sides) / 4)
        self.one_four_of_height = int((self.screen_height - self.gap_of_top) / 4)
        self.full_screen_height_with_gap = int(self.screen_height - self.gap_of_bottom)

        print(self.one_four_of_width, self.one_four_of_height, self.gap_of_bottom, self.gap_of_bottom)

        self.setGeometry(0, 0, self.screen_width, self.full_screen_height_with_gap)

        program_validated = self.validated()
        if program_validated:
            self.home()
        else:
            self.home_validate()

    def home_validate(self):
        self.validation_screen()
        self.show()

    def home(self):
        self.create_table_search()
        self.create_search_section_search()
        self.navigation_bar()
        self.show()

    def validation_screen(self):
        input_width = 260
        input_height = 30
        input_x = (self.width() - input_width) // 2
        input_y = (self.height() - (input_height + 50)) // 2

        self.license_input = QtWidgets.QTextEdit(self)
        self.license_input.setPlaceholderText("Lutfen Lisans Anahtarinizi Girin")
        self.license_input.setGeometry(input_x, input_y, input_width, input_height)

        button_width = 100
        button_height = 30
        button_x = (self.width() - button_width) // 2
        button_y = input_y + input_height + 20

        self.validate_button = QtWidgets.QPushButton("Dogrula", self)
        self.validate_button.setGeometry(button_x, button_y, button_width, button_height)
        self.validate_button.clicked.connect(self.validate_license)


    def create_table_search(self):
        three_four_of_width = int(self.one_four_of_width * 3)
        three_four_of_height = int(self.one_four_of_height * 3)
        half_one_four_width = int(self.one_four_of_width / 2)
        widget_height = 40

        self.table_widget_srch = QtWidgets.QTableWidget(self)
        self.table_widget_srch.setColumnCount(9)
        self.comboBox2 = QtWidgets.QComboBox(self)
        self.comboBox2.setGeometry(self.gap_of_sides, self.gap_of_top, three_four_of_width, widget_height)
        self.comboBox2.addItem("Turkey")
        self.comboBox2.addItem("Greece")
        self.comboBox2.currentIndexChanged.connect(self.on_combobox_changed2)
        self.table_widget_srch.setHorizontalHeaderLabels(["ETA", "Ship Name", "Type", "Port", "Name of Company", "Company Role", "Adress", "Port Loco", "Status"])

        self.table_widget_srch.setGeometry(self.gap_of_sides, self.gap_of_top + widget_height + 20, three_four_of_width, three_four_of_height)

        self.import_button_srch = QtWidgets.QPushButton("Clear Table", self)
        self.import_button_srch.clicked.connect(self.clear_table)
        self.import_button_srch.setGeometry(self.gap_of_sides + self.one_four_of_width + half_one_four_width, three_four_of_height + int(self.gap_of_top*3), self.one_four_of_width + half_one_four_width, widget_height)

        self.export_button_srch = QtWidgets.QPushButton("Export to Excel", self)
        self.export_button_srch.clicked.connect(self.export_to_excel)
        self.export_button_srch.setGeometry(self.gap_of_sides, three_four_of_height + int(self.gap_of_top*3), self.one_four_of_width + half_one_four_width, widget_height)


    def create_search_section_search(self):
        three_four_of_width = int(self.one_four_of_width * 3)
        three_four_of_height = int(self.one_four_of_height * 3)
        half_one_four_width = int(self.one_four_of_width / 2)

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.addItem("Please Select")
        self.comboBox.addItem("ALL PORTS - ALL")

        self.comboBox.setGeometry(three_four_of_width + int(self.gap_of_sides*2), self.gap_of_top, self.one_four_of_width - 40, 40)


        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)

        #self.search_button_srch = QtWidgets.QPushButton("Verileri Getir", self)
        #self.search_button_srch.setGeometry(588, 100, 254, 40)

    def navigation_bar(self):
        extractAction = QtGui.QAction("&View Ports", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Let you able to see the ships which will visit selected port")
        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&View Ports")
        fileMenu.addAction(extractAction)


    def export_to_excel(self):
        row_count = self.table_widget_srch.rowCount()
        column_count = self.table_widget_srch.columnCount()

        data = []

        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.table_widget_srch.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("-")
            data.append(row_data)

        df = pd.DataFrame(data, columns=["ETA", "Ship Name", "Type", "Port", "Name of Company", "Company Role", "Adress", "Port Loco", "Status"])

        current_datetime = datetime.now().strftime("%Y_%m_%d_%H%M")

        excel_file_name = f"{current_datetime}.xlsx"
        db_file_name = f"{current_datetime}.db"

        excel_file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Excel File", excel_file_name,
                                                                   "Excel Files (*.xlsx)")

        if excel_file_path:
            df.to_excel(excel_file_path, index=False)
            QtWidgets.QMessageBox.information(self, "Export Successful", "Data has been exported successfully!")

            db_directory = "dbs"
            db_file_path = os.path.join(db_directory, db_file_name)

            os.makedirs(db_directory, exist_ok=True)

            conn = sqlite3.connect(db_file_path)

            df.to_sql('my_table', conn, if_exists='replace', index=False)

            conn.close()


    def clear_table(self):
        self.table_widget_srch.setRowCount(0)


    def on_combobox_changed2(self):
        if self.comboBox2.currentText() == "Greece":
            QtWidgets.QMessageBox.information(self, "Information", "Greece is not added yet!")
        else:
            print("ok")

    def on_combobox_changed(self):
        selected_item = self.comboBox.currentText()
        if selected_item == "ALL PORTS - ALL":
            self.load_data_from_api()

    def load_data_from_api(self):
        if check_internet():
            print("yes internet")
            GET_URL = "http://1*9.***.***.***/get_combined/"
            headers = {
                "username": "sefakusr",
                "apikey": "i:UGcuNoiW71F%]>o~kNigV{%*`=^|5kxsPHfJk%}3k%4tpaK<p{p3A$)bWbBb@y",
                "usrfingerprint": "1***22**4***9***"
            }

            try:
                response = requests.get(GET_URL, headers=headers, timeout=10)
                response.raise_for_status()

                ships_data = response.json()

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                ships_data = []
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
                ships_data = []
            except ValueError as json_err:
                print("Response content is not valid JSON:", response.text)
                ships_data = []

            self.table_widget_srch.setRowCount(0)

            column_keys = ["eta", "ship_name", "comp_type", "port", "name_of_company", "company_role", "address", "port_loco"]

            for ship in ships_data:
                row_position = self.table_widget_srch.rowCount()
                self.table_widget_srch.insertRow(row_position)

                row_data = []
                for key in column_keys:
                    row_data.append(ship.get(key, "-") if ship.get(key) else "-")

                row_data.append("Not Arrived")

                for i, data in enumerate(row_data):
                    self.table_widget_srch.setItem(row_position, i, QtWidgets.QTableWidgetItem(data))

            self.table_widget_srch.resizeColumnsToContents()
            self.table_widget_srch.resizeRowsToContents()
        else:
            print("no internet")
            QtWidgets.QMessageBox.critical(self, "Error", "Network connection is not available")


    @staticmethod
    def generate_key(variable_str):
        salt = b'\x0b\x1c\xd8\x7f\xea\xbb\x91\x93'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(variable_str.encode()))
        return key

    @staticmethod
    def encrypt_license_key(license_key, variable_key):
        key = MyApp.generate_key(variable_key)
        cipher_suite = Fernet(key)
        encrypted_license = cipher_suite.encrypt(license_key.encode())
        return encrypted_license

    @staticmethod
    def decrypt_license_key(encrypted_license, variable_key):
        key = MyApp.generate_key(variable_key)
        cipher_suite = Fernet(key)
        decrypted_license = cipher_suite.decrypt(encrypted_license).decode()
        return decrypted_license


    def validated(self):
        db_file_name = "accounts.db"
        db_directory = "user"
        db_file_path = os.path.join(db_directory, db_file_name)

        os.makedirs(db_directory, exist_ok=True)

        conn = sqlite3.connect(db_file_path)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY,
            license TEXT NULL, 
            fingerprint TEXT NULL,
            crypted_license TEXT NULL
        );''')
        conn.close()

        conn = sqlite3.connect(db_file_path)
        c = conn.cursor()

        c.execute("SELECT * FROM account")
        rows = c.fetchall()
        print(rows)
        conn.close()

        if len(rows) > 0 and len(rows) < 2:
            user_serial = str(uuid.getnode())
            database_license_key = rows[0][1]
            database_crypted_key = rows[0][3]
            decrypted_license = MyApp.decrypt_license_key(database_crypted_key, user_serial)
            if database_license_key == decrypted_license:
                return True
            else:
                return False
        else:
            return False

    def validate_license(self):
        db_file_name = "accounts.db"
        db_directory = "user"
        db_file_path = os.path.join(db_directory, db_file_name)

        os.makedirs(db_directory, exist_ok=True)

        conn = sqlite3.connect(db_file_path)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY,
            license TEXT NULL, 
            fingerprint TEXT NULL,
            crypted_license TEXT NULL
        );''')
        conn.close()

        conn = sqlite3.connect(db_file_path)
        c = conn.cursor()

        c.execute("SELECT * FROM account")
        rows = c.fetchall()
        print(rows)
        conn.close()
        if check_internet():
            if len(rows) < 1:
                GET_URL = "http://2**.***.***.***:8000/check_license/"
                headers = {
                    "apikey": str(self.license_input.toPlainText())
                }

                input_license = self.license_input.toPlainText()
                print(input_license)
                try:
                    response = requests.post(GET_URL, headers=headers, json={"license": input_license})
                    if response.status_code == 200:
                        license_valid = response.json().get("exists", False)
                        if license_valid:
                            user_serial = str(uuid.getnode())

                            url = "http://207.154.212.109:8000/update_license/"
                            data = {
                                "apikey": str(self.license_input.toPlainText()),
                                "usrfingerprint": user_serial
                            }

                            encrypted_license = ""

                            try:
                                response = requests.post(url, json=data)

                                if response.status_code == 200:
                                    print("License updated successfully:", response.json())
                                    QtWidgets.QMessageBox.information(self, "Validation Result", "License is valid!")
                                    encrypted_license = MyApp.encrypt_license_key(input_license, user_serial)
                                    self.license_input.hide()
                                    self.validate_button.hide()
                                    self.home()                                
                                    self.table_widget_srch.show()  
                                    self.comboBox2.show()
                                    self.import_button_srch.show()
                                    self.export_button_srch.show()
                                    self.comboBox.show()
                                else:
                                    QtWidgets.QMessageBox.information(self, "Validation Result",
                                                                      f"Error updating license: {response.status_code}, {response.json()}")
                            except requests.RequestException as e:
                                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update license: {str(e)}")

                            try:
                                conn = sqlite3.connect(db_file_path)
                                cursor = conn.cursor()
                                cursor.execute(
                                    "INSERT INTO account (license, fingerprint, crypted_license) VALUES (?, ?, ?)",
                                    (input_license, user_serial, encrypted_license))
                                conn.commit()
                                conn.close()
                            except sqlite3.Error as e:
                                QtWidgets.QMessageBox.critical(self, "Database Error",
                                                               f"Failed to insert license: {str(e)}")
                                return


                        else:
                            QtWidgets.QMessageBox.warning(self, "Validation Result", "License is invalid!")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Validation Result",
                                                      "Error checking license: " + str(response.status_code))
                except requests.RequestException as e:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to connect to license server: {str(e)}")
            else:
                pass
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Network connection is not avaible")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())
