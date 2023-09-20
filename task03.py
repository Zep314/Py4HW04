# Возьмите задачу о банкомате из семинара 2. Разбейте её на отдельные операции
# - функции. Дополнительно сохраняйте все операции поступления и снятия средств
# в список.

# Напишите программу банкомат.
# - Начальная сумма равна нулю
# - Допустимые действия: пополнить, снять, выйти
# - Сумма пополнения и снятия кратны 50 у.е.
# - Процент за снятие — 1.5% от суммы снятия, но не менее 30 и не более 600 у.е.
# - После каждой третей операции пополнения или снятия начисляются проценты - 3%
# - Нельзя снять больше, чем на счёте
# - При превышении суммы в 5 млн, вычитать налог на богатство 10% перед каждой
# операцией, даже ошибочной
# - Любое действие выводит сумму денег
from datetime import datetime

# Константы для работы программы
PUSH_SUMM_MULTIPLE = 50  # Кратность пополнения/снятия
PERCENT_FOR_OPERATION = 1.5  # Процент от суммы за снятие
MIN_SUMM_FOR_OPERATION = 30  # Минимальная сумма, которая берется за снятие
MAX_SUMM_FOR_OPERATION = 600  # Максимальная сумма, которая берется за снятие
BONUS_PERCENT = 3  # Процент начисления за COUNT_OPERATION_FOR_BONUS операций
COUNT_OPERATION_FOR_BONUS = 3  # Количество операций, требующихся для получения бонуса
LUXURY_SUMM = 5_000_000  # Сумма, при которой будет вычитаться налог на богатство
LUXURY_PERCENT = 10  # Процент налога на богатство


def print_info():
    print("""Программа - банкомат
    Доступные команды:
    /push <number> - пополнить счет на <number> денег 
    /pop <number> - снять со счета <number> денег
    /list - показать операции по счету
    /exit - выход из программы
    """)


def add_bonus(money):
    """
    Вычисление бонуса за операцию, и добавление его на счет
    :param money:
    :return:
    """
    global account
    global operation_count
    if operation_count % COUNT_OPERATION_FOR_BONUS == 0:
        account += int(money) * BONUS_PERCENT / 100


def luxury_tax():
    """
    Вычисляем налог на роскошь
    :return:
    """
    global account
    if account > LUXURY_SUMM:
        account -= account * LUXURY_PERCENT / 100


def push_account(money):
    """
    Функция пополнения счета, в соответствии с заданием
    :param money:
    :return:
    """
    global account
    global history
    global operation_count
    try:
        luxury_tax()  # Налог на роскошь
        if (int(money) % PUSH_SUMM_MULTIPLE == 0) and (int(money) > 0):  # Проверка на корректность ввода
            account += int(money)  # Пополнение счета
            add_bonus(money)  # Добавление бонуса
            history[datetime.now()] = ('Пополнение счета', int(money), float(account))
        else:
            print(f"Пополнять счет можно положительной суммой, кратной {PUSH_SUMM_MULTIPLE}")
    except ValueError:
        print("Ошибка ввода")


def pop_account(money):
    """
    Функция списания со счета
    :param money:
    :return:
    """
    global account
    global history
    global operation_count
    try:
        luxury_tax()  # Налог на роскошь
        if (int(money) % PUSH_SUMM_MULTIPLE == 0) and (int(money) > 0) and ((account - int(money)) >= 0):
            account -= int(money)  # Списание со счета
            percent_fo_operation = int(money) * PERCENT_FOR_OPERATION / 100  # Процент за списание
            if percent_fo_operation < MIN_SUMM_FOR_OPERATION:
                percent_fo_operation = MIN_SUMM_FOR_OPERATION
            if percent_fo_operation > MAX_SUMM_FOR_OPERATION:
                percent_fo_operation = MAX_SUMM_FOR_OPERATION
            account -= percent_fo_operation
            add_bonus(money)  # Добавление бонуса
            history[datetime.now()] = ('Списание со счета', int(money), account)
        else:
            print(f"Снимать со счета можно положительную сумму, не превышая баланса, "
                  f"и кратной {PUSH_SUMM_MULTIPLE}")
    except ValueError:
        print("Ошибка ввода")


def list_operations():
    """
    Вывод журнала операций на печать
    :return:
    """
    global history
    for key_, value_ in history.items():
        print(f'{key_}: {value_[0]}, {value_[1]:0.2f}. Баланс: {value_[2]:0.2f}')


if __name__ == '__main__':  # Сама программа
    print_info()  # Приветственное слово
    my_exit = False
    account = 0  # Баланс счета
    operation_count = 1  # Счетчик операций
    history = {}  # Журнал операций

    while not my_exit:  # Главный цикл программы
        print(f'Баланс счета: {account:0.2f}')
        inp = input(">>> ")  # Приглашение
        match inp.lower().split(' ')[0]:
            case "/exit":  # Выход
                my_exit = True
            case "/push":  # Пополнение счета
                push_account(inp.lower().split(' ')[1])
                operation_count += 1
            case "/pop":  # Снятие со счета
                pop_account(inp.lower().split(' ')[1])
                operation_count += 1
            case "/list":  # Вывод журнала на печать
                list_operations()
            case _:
                print('Неизвестная команда')
    print('Работа завершена')

# Результат работы:
# /home/user/Work/Python/dz4/Py4HW04/venv/bin/python /home/user/Work/Python/dz4/Py4HW04/task03.py
# Программа - банкомат
#     Доступные команды:
#     /push <number> - пополнить счет на <number> денег
#     /pop <number> - снять со счета <number> денег
#     /list - показать операции по счету
#     /exit - выход из программы
#
# Баланс счета: 0.00
# >>> /push 10000
# Баланс счета: 10000.00
# >>> /push 30
# Пополнять счет можно положительной суммой, кратной 50
# Баланс счета: 10000.00
# >>> /push 1000000
# Баланс счета: 1040000.00
# >>> /pop 300
# Баланс счета: 1039670.00
# >>> /push 6000000
# Баланс счета: 7039670.00
# >>> /pop 1000000
# Баланс счета: 5365103.00
# >>> /list
# 2023-05-29 19:02:39.290953: Пополнение счета, 10000.00. Баланс: 10000.00
# 2023-05-29 19:03:03.509521: Пополнение счета, 1000000.00. Баланс: 1040000.00
# 2023-05-29 19:03:08.988826: Списание со счета, 300.00. Баланс: 1039670.00
# 2023-05-29 19:03:19.218869: Пополнение счета, 6000000.00. Баланс: 7039670.00
# 2023-05-29 19:03:27.894247: Списание со счета, 1000000.00. Баланс: 5365103.00
# Баланс счета: 5365103.00
# >>> /exit
# Работа завершена
#
# Process finished with exit code 0
