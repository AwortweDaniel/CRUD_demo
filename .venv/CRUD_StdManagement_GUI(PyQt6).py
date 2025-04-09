from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QFormLayout, QMessageBox

import sys
import mysql.connector


config = {
    'user': 'root',
    'port': 3306,
    'password': 'root',
    'host': 'localhost',
    'database': 'students_register'
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Data Management")
        self.resize(650, 500)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Email", "Course", "Department"])

        add_btn = QPushButton("Add Student")
        update_btn = QPushButton("Update Student")
        delete_btn = QPushButton("Delete Student")
        refresh_btn = QPushButton("Refresh Table")

        add_btn.clicked.connect(self.open_add_dialog)
        update_btn.clicked.connect(self.open_update_dialog)
        delete_btn.clicked.connect(self.open_delete_dialog)
        refresh_btn.clicked.connect(self.load_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_btn)
        button_layout.addWidget(update_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()

    def get_connection(self):
        return mysql.connector.connect(**config)

    def load_data(self):
        self.table.setRowCount(0)
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student_detail")
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        cursor.close()
        connection.close()

    def open_add_dialog(self):
        dialog = AddStudentDialog(self)
        dialog.exec()
        self.load_data()

    def open_update_dialog(self):
        dialog = UpdateStudentDialog(self)
        dialog.exec()
        self.load_data()

    def open_delete_dialog(self):
        dialog = DeleteStudentDialog(self)
        dialog.exec()
        self.load_data()


class AddStudentDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add Student")
        layout = QFormLayout()

        self.name = QLineEdit()
        self.contact = QLineEdit()
        self.email = QLineEdit()
        self.course = QLineEdit()
        self.department = QLineEdit()

        layout.addRow("Name", self.name)
        layout.addRow("Contact", self.contact)
        layout.addRow("Email", self.email)
        layout.addRow("Course", self.course)
        layout.addRow("Department", self.department)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_student)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def save_student(self):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "INSERT INTO student_detail (student_name, contact, email, course, department) VALUES (%s, %s, %s, %s, %s)"
        values = (self.name.text(), self.contact.text(), self.email.text(), self.course.text(), self.department.text())
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        QMessageBox.information(self, "Success", "Student added successfully")
        self.accept()



class UpdateStudentDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Update Student")
        layout = QFormLayout()

        self.name = QLineEdit()
        self.contact = QLineEdit()
        self.email = QLineEdit()
        self.course = QLineEdit()
        self.department = QLineEdit()

        layout.addRow("Student Name to Update", self.name)
        layout.addRow("New Contact", self.contact)
        layout.addRow("New Email", self.email)
        layout.addRow("New Course", self.course)
        layout.addRow("New Department", self.department)

        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.update_student)
        layout.addRow(update_btn)

        self.setLayout(layout)

    def update_student(self):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        name = self.name.text()

        fields = []
        values = []

        if self.contact.text():
            fields.append("contact = %s")
            values.append(self.contact.text())
        if self.email.text():
            fields.append("email = %s")
            values.append(self.email.text())
        if self.course.text():
            fields.append("course = %s")
            values.append(self.course.text())
        if self.department.text():
            fields.append("department = %s")
            values.append(self.department.text())

        if not fields:
            QMessageBox.warning(self, "Error", "Please fill at least one field to update.")
            return

        query = f"UPDATE student_detail SET {', '.join(fields)} WHERE student_name = %s"
        values.append(name)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        QMessageBox.information(self, "Success", "Student updated successfully")
        self.accept()


class DeleteStudentDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Delete Student")
        layout = QFormLayout()

        self.name = QLineEdit()
        layout.addRow("Student Name to Delete", self.name)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_student)
        layout.addRow(delete_btn)

        self.setLayout(layout)

    def delete_student(self):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "DELETE FROM student_detail WHERE student_name = %s"
        values = (self.name.text(),)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        QMessageBox.information(self, "Success", "Student deleted successfully")
        self.accept()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
