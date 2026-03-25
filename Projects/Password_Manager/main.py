import sys
import base64
import os
from hashlib import pbkdf2_hmac
from threading import Timer
import bcrypt
import pyperclip
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame
)
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary, or_
from sqlalchemy.orm import declarative_base, sessionmaker


# Создание БД
engine = create_engine("sqlite:///passwords.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Создание моделей пользователя и пароля
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(LargeBinary)
    salt = Column(LargeBinary)

class Password(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True)
    site = Column(String)
    username = Column(String)
    password = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(engine)

# Защита пароля
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def derive_key(password, salt):
    key = pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(key)

def get_cipher(password, salt):
    return Fernet(derive_key(password, salt))

# Интерфейс
FRONTEND = """
QWidget {
    background-color: #0f1115;
    color: #e6e6e6;
    font-size: 14px;
}

QLineEdit {
    background: #1a1d24;
    border: 1px solid #2a2f3a;
    border-radius: 10px;
    padding: 10px;
}

QLineEdit:focus {
    border: 1px solid #4a90e2;
}

QPushButton {
    background: #1f232b;
    border-radius: 8px;
    padding: 6px;
    min-width: 32px;
    min-height: 32px;
}

QPushButton:hover {
    background: #2d3340;
}

QPushButton#primary {
    background: #4a90e2;
}
QPushButton#primary:hover {
    background: #357bd8;
}

QPushButton#delete:hover {
    background: #e5484d;
}

QPushButton#copy:hover {
    background: #2f3f2f;
}

QPushButton#view:hover {
    background: #3a3f4b;
}

QTableWidget {
    background: #16181d;
    border-radius: 12px;
}
"""

# Окно регистрации
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(FRONTEND)
        self.showMaximized()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(400)
        card_layout = QVBoxLayout()

        title = QLabel("Создать аккаунт")
        title.setStyleSheet("font-size:20px;")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.pass_confirm = QLineEdit()
        self.pass_confirm.setPlaceholderText("Повтор пароля")
        self.pass_confirm.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Создать")
        btn.setObjectName("primary")
        btn.clicked.connect(self.register)

        card_layout.addWidget(title)
        card_layout.addWidget(self.login_input)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(self.pass_confirm)
        card_layout.addWidget(btn)

        card.setLayout(card_layout)
        layout.addWidget(card)

        self.setLayout(layout)

    def register(self):
        username = self.login_input.text()
        password = self.pass_input.text()
        confirm = self.pass_confirm.text()

        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        if session.query(User).filter_by(username=username).first():
            QMessageBox.warning(self, "Ошибка", "Пользователь уже есть")
            return

        session.add(User(
            username=username,
            password_hash=hash_password(password),
            salt=os.urandom(16)
        ))
        session.commit()

        QMessageBox.information(self, "OK", "Аккаунт создан")
        self.close()

# Окно входа
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(FRONTEND)
        self.showMaximized()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(400)
        card_layout = QVBoxLayout()

        title = QLabel("Password Manager Login")
        title.setStyleSheet("font-size:20px;")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Пароль")

        btn_login = QPushButton("Войти")
        btn_login.setObjectName("primary")
        btn_login.clicked.connect(self.login)

        btn_reg = QPushButton("Регистрация")
        btn_reg.clicked.connect(self.open_register)

        card_layout.addWidget(title)
        card_layout.addWidget(self.login_input)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(btn_login)
        card_layout.addWidget(btn_reg)

        card.setLayout(card_layout)
        layout.addWidget(card)

        self.setLayout(layout)

        self.user = None
        self.raw_password = None

    def login(self):
        user = session.query(User).filter_by(
            username=self.login_input.text()
        ).first()

        if user and check_password(self.pass_input.text(), user.password_hash):
            self.user = user
            self.raw_password = self.pass_input.text()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_register(self):
        self.reg = RegisterWindow()
        self.reg.show()

# Окно паролей
class PasswordManager(QWidget):
    def __init__(self, user, cipher_key):
        super().__init__()
        self.user = user
        self.cipher_key = cipher_key
        self.setStyleSheet(FRONTEND)
        self.showMaximized()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        side = QVBoxLayout()
        side.addWidget(QLabel("🔐 Password Manager"))
        side.addWidget(QLabel(self.user.username))
        side.addStretch()

        btn = QPushButton("Выйти")
        btn.clicked.connect(self.logout)
        side.addWidget(btn)

        content = QVBoxLayout()

        self.site = QLineEdit()
        self.site.setPlaceholderText("Сайт")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.Password)

        btn_gen = QPushButton("🔄")
        btn_gen.clicked.connect(self.generate_password)

        btn_save = QPushButton("Сохранить")
        btn_save.setObjectName("primary")
        btn_save.clicked.connect(self.save_password)

        row = QHBoxLayout()
        row.addWidget(self.password)
        row.addWidget(btn_gen)
        row.addWidget(btn_save)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск...")
        self.search.textChanged.connect(self.load_passwords)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Сайт", "Логин", "Пароль", "", "", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        content.addWidget(self.site)
        content.addWidget(self.username)
        content.addLayout(row)
        content.addWidget(self.search)
        content.addWidget(self.table)

        layout.addLayout(side, 1)
        layout.addLayout(content, 4)

        self.setLayout(layout)
        self.load_passwords()

    def generate_password(self):
        import random, string
        chars = string.ascii_letters + string.digits
        self.password.setText(''.join(random.choice(chars) for _ in range(14)))

    def save_password(self):
        enc = self.cipher_key.encrypt(self.password.text().encode()).decode()

        session.add(Password(
            site=self.site.text(),
            username=self.username.text(),
            password=enc,
            user_id=self.user.id
        ))
        session.commit()

        self.load_passwords()

    def load_passwords(self):
        query = session.query(Password).filter_by(user_id=self.user.id)
        text = self.search.text().strip()

        if text:
            query = query.filter(
                or_(
                    Password.site.ilike(f"%{text}%"),
                    Password.username.ilike(f"%{text}%")
                )
            )

        rows = query.all()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            decrypted = self.cipher_key.decrypt(row.password.encode()).decode()

            self.table.setItem(i, 0, QTableWidgetItem(row.site))
            self.table.setItem(i, 1, QTableWidgetItem(row.username))
            self.table.setItem(i, 2, QTableWidgetItem("••••••"))

            btn_show = QPushButton()
            btn_show.setObjectName("view")
            btn_show.setText("👁")
            btn_show.setToolTip("Показать пароль")
            btn_show.clicked.connect(
                lambda _, r=i, p=decrypted: self.toggle_row_password(r, p)
            )

            btn_copy = QPushButton()
            btn_copy.setObjectName("copy")
            btn_copy.setText("📋")
            btn_copy.setToolTip("Скопировать")
            btn_copy.clicked.connect(
                lambda _, p=decrypted: self.copy_password(p)
            )

            btn_delete = QPushButton()
            btn_delete.setObjectName("delete")
            btn_delete.setText("🗑")
            btn_delete.setToolTip("Удалить")
            btn_delete.clicked.connect(
                lambda _, rid=row.id: self.delete_password(rid)
            )

            self.table.setCellWidget(i, 3, btn_show)
            self.table.setCellWidget(i, 4, btn_copy)
            self.table.setCellWidget(i, 5, btn_delete)

    def toggle_row_password(self, row, password):
        item = self.table.item(row, 2)

        if item.text() == "••••••":
            self.table.setItem(row, 2, QTableWidgetItem(password))
        else:
            self.table.setItem(row, 2, QTableWidgetItem("••••••"))

    def copy_password(self, password):
        pyperclip.copy(password)
        QMessageBox.information(self, "Скопировано", "Пароль в буфере (60 сек)")
        Timer(60, lambda: pyperclip.copy("")).start()

    def delete_password(self, row_id):
        reply = QMessageBox.question(self, "Удалить?", "Ты уверен?")
        if reply == QMessageBox.Yes:
            session.query(Password).filter_by(id=row_id).delete()
            session.commit()
            self.load_passwords()

    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.show()

# Запуск приложения
app = QApplication(sys.argv)

login = LoginWindow()
login.show()
app.exec_()

if not login.user:
    sys.exit()

cipher = get_cipher(login.raw_password, login.user.salt)

window = PasswordManager(login.user, cipher)
window.show()

sys.exit(app.exec_())