import sys
from PyQt5.QtWidgets import QApplication
from bank_storage import init_files
from login_window import LoginWindow

def main():
    init_files()

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()