from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout,QMessageBox
# todo register window
from auth import login

class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bank App")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.do_login) # handle login def
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Create an account")
        #self.register_button.clicked.connect() # handle open register window
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def do_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        account = login(username, password)
        if account:
            QMessageBox.information(self, "Success", "Welcome, {username}!")
            # todo open main UI here
        else:
            QMessageBox.warning(self, "Error", "Incorrect email or password.")