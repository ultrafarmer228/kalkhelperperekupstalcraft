
import sys
from PyQt5 import QtWidgets
from output import Ui_MainWindow
import re

# Определение функции load_prices для загрузки цен из файла
def load_prices():
    try:
        with open("prices.txt", "r") as file:
            prices = [float(line.strip() or 0) for line in file.readlines()]
            return prices
    except FileNotFoundError:
        print("Файл с ценами не найден. Используются стандартные цены.")
        return [0, 0, 0, 0, 0, 0, 0, 0]
    except Exception as e:
        print(f"Ошибка при чтении файла с ценами: {e}")
        return [0, 0, 0, 0, 0, 0, 0, 0]
        

# Определение функции get_password для получения пароля из файла
def get_password():
    try:
        with open('password.txt', 'r') as file:
            passwords = [line.strip() for line in file.readlines()]
            return passwords
    except FileNotFoundError:
        return None



# Определение функции save_password для сохранения пароля в файле
def save_password(password):
    with open('saved_password.txt', 'w') as file:
        file.write(password)

# Определение класса PasswordDialog для окна ввода пароля
class PasswordDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Введите пароль")

        self.layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Введите пароль:")
        self.layout.addWidget(self.label)

        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password_edit)

        self.submit_button = QtWidgets.QPushButton("Подтвердить")
        self.submit_button.clicked.connect(self.check_password)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    # Определение функции check_password для проверки введенного пароля
    def check_password(self):
        password = self.password_edit.text()
        stored_passwords = get_password()
        if password in stored_passwords:
            save_password(password)
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный пароль")



# Определение класса MyApplication
class MyApplication(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализируем интерфейс

        # Получаем цены из файла
        self.prices = load_prices()

        # Добавляем обработчики событий
        self.pushButton.clicked.connect(self.calculate_price)
        self.pushButton_2.clicked.connect(self.copy_price_to_clipboard)
        self.lineEdit.returnPressed.connect(self.calculate_price)
        self.lineEdit_2.returnPressed.connect(self.calculate_price)
        self.lineEdit_3.returnPressed.connect(self.calculate_price)
        self.lineEdit_4.returnPressed.connect(self.calculate_price)
        self.lineEdit_5.returnPressed.connect(self.calculate_price)
        self.lineEdit_6.returnPressed.connect(self.calculate_price)
        self.lineEdit_7.returnPressed.connect(self.calculate_price)
        self.lineEdit_8.returnPressed.connect(self.calculate_price)

    # Определение функции calculate_price для расчета общей стоимости
    def calculate_price(self):
        try:
            # Получаем количество товаров из интерфейса
            quantities = [int(widget.text() or 0) for widget in [self.lineEdit, self.lineEdit_2, self.lineEdit_3,
                                                                  self.lineEdit_4, self.lineEdit_5, self.lineEdit_6,
                                                                  self.lineEdit_7, self.lineEdit_8]]
            total_price = sum(qty * price for qty, price in zip(quantities, self.prices))

            # Выводим результат на экран
            self.label_5.setText(f"Вы должны заплатить: {int(total_price)}")

        except ValueError as e:
            print("Ошибка:", e)
            print("Пожалуйста, введите число.")

    # Функция для копирования текста из QLabel в буфер обмена
    def copy_price_to_clipboard(self):
        text_to_copy = self.label_5.text()  
        price = re.search(r'\d+\.?\d*', text_to_copy)  
        if price:
            clipboard = QtWidgets.QApplication.clipboard()  
            clipboard.setText(price.group())  

def get_saved_password():
    try:
        with open('saved_password.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    saved_password = get_saved_password()
    stored_passwords = get_password()

    if saved_password in stored_passwords:
        # Если сохраненный пароль найден в списке допустимых паролей, открываем приложение без запроса пароля
        window = MyApplication()
        window.show()
        sys.exit(app.exec_())
    else:
        # Иначе отображаем окно ввода пароля
        password_dialog = PasswordDialog()
        if password_dialog.exec_() == QtWidgets.QDialog.Accepted:
            window = MyApplication()
            window.show()
            sys.exit(app.exec_())
        else:
            sys.exit(0)

