from datetime import datetime

import forex_python.converter
import forex_python.bitcoin


class CurrencyConverter:
    __slots__ = 'cur', 'btc', 'RATES', 'file_path'

    def __init__(self):
        self.cur = forex_python.converter.CurrencyRates()
        self.btc = forex_python.bitcoin.BtcConverter()
        # Все доступные курсы.
        self.RATES = list(self.cur.get_rates('USD')) + ['BTC']
        # Путь к файлу историй.
        self.file_path = 'history.txt'

    # Метод для проверки корректного курса.
    def _check_rate(self, rate: str) -> bool:
        if rate.upper() in self.RATES:
            return True
        else:
            return False

    # Метод для проверки корректных денег.
    @staticmethod
    def _check_money(money: str) -> bool:
        try:
            if float(money) >= 0:
                return True
            else:
                return False
        except ValueError:
            return False

    # Метод для проверки корректной даты.
    @staticmethod
    def _check_date(date: str) -> bool:
        try:
            datetime.strptime(date, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    # Метод для ввода курса.
    def _input_valid_rate(self, print_text: str) -> str:
        while True:
            rate = input(print_text)
            if self._check_rate(rate):
                return rate.upper()
            else:
                print("Error: Вы ввели неверную аббревиатуру.")

    # Метод для ввода денег.
    def _input_valid_money(self) -> float:
        while True:
            money = input('Введите деньги (по умолчанию 1): ')
            if money == '':
                return 1
            elif self._check_money(money):
                return float(money)
            else:
                print("Error: Строка не является числом или число отрицательное.")

    # Метод для ввода даты.
    def _input_valid_date(self) -> datetime:
        while True:
            date = input("Введите дату (дд.мм.гггг): ")
            if date == '':
                return datetime.today()
            elif self._check_date(date):
                return datetime.strptime(date, '%d.%m.%Y')
            else:
                print('Error: Вы ввели неверную дату.')

    # Метод для конвертации валют.
    def converter(self) -> float:
        rate1 = self._input_valid_rate('Введите первый курс: ')
        rate2 = self._input_valid_rate('Введите второй курс: ')
        money1 = self._input_valid_money()
        while True:
            try:
                if rate1 == 'BTC':
                    money2 = round(self.btc.convert_btc_to_cur(money1, rate2), 6)
                    date = datetime.today()
                elif rate2 == 'BTC':
                    money2 = round(self.btc.convert_to_btc(money1, rate1), 6)
                    date = datetime.today()
                else:
                    date = self._input_valid_date()
                    money2 = round(self.cur.convert(rate1, rate2, money1, date), 6)
            except forex_python.converter.RatesNotAvailableError:
                print("Error: Вы ввели неверную дату или дата слишком старая.")
            else:
                self.input_to_file(f'{rate1} => {rate2}\t{money1}'
                                   f' => {money2}\t{date.strftime("%d.%m.%Y")}')
                return money2

    # Метод для ввода данных в файл.
    def input_to_file(self, text: str):
        with open(self.file_path, 'a') as file:
            file.write(f'{text}\n')

    # Метод для вывода данных файла на экран.
    def output_file(self):
        try:
            with open(self.file_path, 'r') as file:
                print(f'\n{"-"*10}{self.file_path}{"-"*10}')
                for line in file:
                    print(line.rstrip())
        except FileNotFoundError:
            print('Файл еще не создан.')

    # Метод для очистки данных из файла.
    def clear_file(self):
        with open(self.file_path, 'w') as file:
            pass

    # Метод для манипуляции.
    def menu(self):
        try:
            while True:
                print(f'{"-"*15}Меню{"-"*15}')
                print('0\tВыход;')
                print('1\tКурсы;')
                print('2\tПолучить историю;')
                print('3\tОчистить историю;')
                print('4\tВывести все доступные курсы.')
                print('-'*34)
                remote = input('Введите пункт: ')
                if remote == '1':
                    print(f'Деньги: {self.converter()}')
                elif remote == '2':
                    self.output_file()
                elif remote == '3':
                    self.clear_file()
                elif remote == '4':
                    print(', '.join(self.RATES))
                elif remote == '0':
                    exit(0)
                else:
                    print('Error: Вы ввели неверное число.')
                print()
        # Перехват исключения, если был неправильный выход из программы.
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    cc = CurrencyConverter()
    cc.menu()
