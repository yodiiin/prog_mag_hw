import pickle
import re
from datetime import datetime


"""DESCRIPTORS"""
class NameDescriptor:
    def __set_name__(self, owner, name): # name - просто какой-то атрибут
        self.private = '__' + name
        self.public = name        
    
    def __get__(self, instance, owner):
        return getattr(instance, self.private)

    def __set__(self, instance, value):
        if isinstance(value, str) and value.isalpha():
            setattr(instance, self.private, value.strip())
        else:
            raise ValueError('Неверный формат имени. Имя должно содержать только буквы')


class PhoneDescriptor:
    def __set_name__(self, owner, name):
        self.private = '__' + name
        self.public = name    

    def __get__(self, instance, owner):
        return getattr(instance, self.private)

    def __set__(self, instance, value):
        """ Телефон может быть в формате:
        +7 (912) 345-67-89 / +7 (495) 123-45-67
        89123456789 / 84732123456
        +7-473-212-34-56 / 8-912-345-67-89
        """
        if re.match(r'(?:\b|\B\+7)(?:\+7|8)?[\s\-]?\(?\d{3,4}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b', value):
            setattr(instance, self.private, value)
        else:
            raise ValueError('Неверный формат телефона: ведите мобильный или домашний телефон, начинающийся с +7... или 8...')


class AgeDescriptor:
    def __set_name__(self, owner, name):
        self.private = '__' + name
        self.public = name    

    def __get__(self, instance, owner):
        return getattr(instance, self.private)

    def __set__(self, instance, value):
        """Возраст:
        1. целое число
        2. в диапазоне от 1 до 30"""
        if isinstance(value, int) and (0 < value <= 30):  # возраст может быть только целым и в диапазоне от 1 до 30
            setattr(instance, self.private, value)
        else:
            raise ValueError('Возраст не может быть отрицательным или больше 30.')


"""CLASSES"""
class Client:
    name = NameDescriptor()
    phone = PhoneDescriptor()

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.pets = [] # хранит экземпляры класса Pet

    def add_pet(self, pet):
        self.pets.append(pet)

    def get_pets(self):
        return self.pets


class Pet:
    name = NameDescriptor()
    age = AgeDescriptor()

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.appointments = {}
        self.current_appointment = None
    
    def set_appointment(self, date):
        try:
            appointment_date = datetime.strptime(date, "%d.%m %H:%M") # проверка на реалистичные даты и время встроена в модуль
            self.current_appointment = appointment_date
        except ValueError:
            raise ValueError('Неверный формат или значение даты. Дата должна быть в формате ДД.ММ ЧЧ:ММ')

    def complete_appointment(self, comments):
        if self.current_appointment is None:
            raise ValueError('Нет текущей записи на прием.')
        self.appointments[self.current_appointment] = comments
        self.current_appointment = None

    def get_appointments(self):
        return self.appointments

    def has_upcoming_appointment(self):
        return self.current_appointment is not None


class Database:
    def __init__(self):
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def find_client_by_name(self, name):
        return [client for client in self.clients if client.name.lower() == name.lower()]

    def find_client_by_phone(self, phone):
        return [client for client in self.clients if client.phone == phone]

    def save(self, filename='vet_clinic.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
    
    def clear(self):
        self.clients = []
        self.save()
        print('База данных успешно очищена.\n')
        print('-------------------------------------\n')

    @staticmethod
    def load(filename='vet_clinic.pkl'):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return Database()


"""GAME"""
def game():
    database = Database.load()

    commands = [
        '1. Добавить нового клиента',
        '2. Найти клиента по имени',
        '3. Найти клиента по телефону',
        '4. Добавить питомца клиенту',
        '5. Записать питомца на прием',
        '6. Отметить прием как завершенный',
        '7. Посмотреть прошедшие приемы питомца',
        '8. Очистить базу данных',
        '9. Выйти из игры'
    ]
    print('****** База ветеринарной клиники загружается... *******\n')

    while True:
        """ Главное меню """
        print('Выберите команду из списка ниже:\n')
        print('\n'.join(commands))

        choice = input('\nВыберите действие: ')

        if choice == '1':
            while True: # будет просить ввести данные, пока не будут введены правильные
                try:
                    name = input('Введите имя клиента: ')
                    phone = input('Введите телефон клиента: ')
                    client = Client(name, phone)
                    database.add_client(client)
                    print('\nКлиент успешно добавлен в базу.\n')
                    break
                except ValueError as e:
                    print(f'Ошибка: {e}. Попробуйте снова.\n')
            print('-------------------------------------\n')

        elif choice == '2':
            name = input('Введите имя клиента для поиска: ')
            clients = database.find_client_by_name(name)
            if clients:
                for client in clients:
                    print(f'\tКлиент: {client.name}, Телефон: {client.phone}, Питомцы: {[pet.name for pet in client.get_pets()]}')
            else:
                print('\nКлиент не найден.\n')
            print('-------------------------------------\n')

        elif choice == '3':
            phone = input('Введите телефон клиента для поиска: ')
            clients = database.find_client_by_phone(phone)
            if clients:
                for client in clients:
                    print(f'\tКлиент: {client.name}, Телефон: {client.phone}, Питомцы: {[pet.name for pet in client.get_pets()]}')
            else:
                print('\nКлиент не найден.\n')
            print('-------------------------------------\n')

        elif choice == '4':
            phone = input('Введите телефон клиента: ')
            clients = database.find_client_by_phone(phone)
            if clients:
                client = clients[0]
                while True:
                    try:
                        pet_name = input('Введите имя питомца: ')
                        pet_age = int(input('Введите возраст питомца: '))
                        pet = Pet(pet_name, pet_age)
                        client.add_pet(pet)
                        print('\nПитомец успешно добавлен в базу.\n')
                        break
                    except ValueError as e:
                        print(f'Ошибка: {e}. Попробуйте снова.\n')
            else:
                print('\nКлиент не найден.\n')
            print('-------------------------------------\n')

        elif choice == '5':
            phone = input('Введите телефон клиента: ')
            clients = database.find_client_by_phone(phone)
            if clients:
                client = clients[0]
                if client.get_pets():
                    for idx, pet in enumerate(client.get_pets()):
                        print(f'{idx + 1}. {pet.name}, возраст: {pet.age}')
                    try:
                        pet_index = int(input('Выберите номер питомца для записи на прием: ')) - 1
                        appointment_date = input('Введите дату и время приема (ДД.ММ ЧЧ:ММ): ')
                        client.get_pets()[pet_index].set_appointment(appointment_date)
                        print(f'Питомец был успешно записан на прием на следующую дату: {appointment_date}\n')
                    except (ValueError, IndexError) as e:
                        print(f'Ошибка: {e}\n')
                else:
                    print('\nУ клиента нет питомцев.\n')
            else:
                print('\nКлиент не найден.\n')
            print('-------------------------------------\n')

        elif choice == '6':
            phone = input('Введите телефон клиента: ')
            clients = database.find_client_by_phone(phone)
            if clients:
                client = clients[0]
                if client.get_pets():
                    for idx, pet in enumerate(client.get_pets()):
                        print(f'{idx + 1}. {pet.name}, возраст: {pet.age}"')
                    try:
                        pet_index = int(input('Выберите номер питомца для завершения приема: ')) - 1
                        comments = input('Введите комментарий ветеринара: ')
                        client.get_pets()[pet_index].complete_appointment(comments)
                        print('\nПрием завершен.\n')
                    except (ValueError, IndexError) as e:
                        print(f'Ошибка: {e}\n')
                else:
                    print('\nУ клиента нет питомцев.\n')
            else:
                print('\nКлиент не найден.\n')
            print('-------------------------------------\n')

        elif choice == '7':
            phone = input('Введите телефон клиента: ')
            clients = database.find_client_by_phone(phone)
            if clients:
                client = clients[0]
                if client.get_pets():
                    for idx, pet in enumerate(client.get_pets()):
                        print(f'{idx + 1}. {pet.name}, возраст: {pet.age}')
                    try:
                        pet_index = int(input('Выберите номер питомца для просмотра проведенных приемов: ')) - 1
                        appointments = client.get_pets()[pet_index].get_appointments()
                        if appointments:
                            for date, comment in appointments.items():
                                print(f'\tДата: {date}\n\tКомментарий: {comment}\n')
                        else:
                            print('\nНет прошедших приемов.\n')
                    except (ValueError, IndexError) as e:
                        print(f'Ошибка: {e}\n')
                else:
                    print('\nУ клиента нет питомцев.\n')
            else:
                print('\nКлиент не найден.\n')
            print('-------------------------------------\n')

        elif choice == '8':
            confirm = input('Вы уверены, что хотите очистить базу данных? (да/нет): ')
            if confirm.lower() == 'да':
                database.clear()

        elif choice == '9':
            database.save()
            print('\nБаза данных была успешно сохранена. До свидания!\n')
            break

        else:
            print('Введена неверная команда. Пожалуйста, выберите правильную команду.\n')

if __name__ == "__main__":
    game()