from views import CreateMixin, UpdateMixin, DestroyMixin, RetrieveMixin, ListingMixin
# from views_buyer import *

import json 


'''Роли_ покупатель, продавец, админ'''

''' Покупатель '''
class Buyer(RetrieveMixin, DestroyMixin, ListingMixin):
    pass

''' Продавец '''
class SalesMan(CreateMixin, RetrieveMixin, DestroyMixin, UpdateMixin, ListingMixin):
    pass

''' Администратор '''
class Admin(RetrieveMixin, DestroyMixin, UpdateMixin, ListingMixin):
    pass


class Order:
    def __init__(self):
        self.orders = []
        self.role = Buyer()
        self.count = 0
        self.total = 0

    def create_order(self, id_):
        result = self.role.get_detail(id_=id_)
        
        if result['status'] == 200:
            if id_ in self.orders: return 'Товар уже есть в корзине'
            self.orders.append(id_)
            self.count +=1 
            self.total += result['msg'][-1]
            return 'Добавлено в корзину'
        
        return f'Нет продукта с ID {id_}'

    def list_of_orders(self):
        if not self.orders: return f'Нет заказов'
        
        [print(self.role.get(i)) for i in self.orders]
        return f'Кол-во машин: {self.count}\nОбщая сумма заказа: {self.total}'

    def delete_order(self, id_):
        if not self.orders: return f'Нет заказов'
        result = self.role.get_detail(id_=id_)
        if id_ in self.orders:
            self.orders.remove(id_)
            self.count -= 1
            self.total -= result['msg'][-1]
            return f'Продукт с ID {id_} был убран с корзины'
        return f'Продукт с ID {id_} не найден'

    def to_buy(self, sum_user):
        if not self.orders: return f'Нет заказов'

        if sum_user >= self.total:
            [self.role.delete(i) for i in self.orders]
            self.orders.clear()
            self.total = 0
            self.count = 0
            return 'Покупка завершена'

        return 'У вас недостаточно средств'

    @staticmethod
    def listing():
        return ListingMixin.listing()

    


class Product:
    def __init__(self):
        self.products = []
        self.role = SalesMan()
        
    def create_order(self, id_):
        result = self.role.get_detail(id_=id_)

        if result['status'] == 200:
            self.products.append(id_)
            self.count +=1 
            self.total += result['msg'][-1]
            return 'Добавлено в корзину'
        
        return f'Нет продукта с ID {id_}'

    def list_of_orders(self):
        if not self.products: return f'Нет заказов'
        
        [print(self.role.get(i)) for i in self.products]
        return f'Кол-во машин: {self.count}\nОбщая сумма заказа: {self.total}'

    def delete_order(self, id_):
        if not self.products: return f'Нет заказов'
        if id_ in self.products:
            self.products.remove(id_)
            return f'Продукт с ID {id_} был убран с корзины'
        return f'Продукт с ID {id_} не найден'


    def to_buy(self, sum_user):
        if not self.products: return f'Нет заказов'

        if sum_user >= self.total:
            [self.role.delete(i) for i in self.products]
            self.products.clear()
            self.total = 0
            self.count = 0
            return 'Покупка завершена'

        return 'У вас недостаточно средств'

    @staticmethod
    def listing():
        return ListingMixin.listing()

def input_menu():
    while True:
        print('Войти в аккаунт как:\n1-пПкупатель\t2-Продавец\t3-Администратор\n'+'='*100)
        choice_ = input('Enter a command: ')
        if choice_ == '1':
            menu_buyer()
        elif choice_ == '2':
            menu_salesman()
        elif choice_ == '3':
            pass
        else: print('The command not found')
        print('='*100)


def menu_buyer():
    flag1 = True

    with open('data_buyer.json') as file:
        data_buyer = json.load(file)
        print(data_buyer)

        while flag1:
            user_name = input('user_name: ')
            password = input('password: ')
            user = list(filter(lambda x: x['user_name']==user_name and x['password']==password, data_buyer))
            if not user:
                print('Неправильное имя или пароль')
                answer = input('Попробовать снова? (no?): ')
                if answer.lower() == 'no':
                    input_menu()
                continue
            index_ = data_buyer.index(user[0])
            user_sum = data_buyer[index_]['user_sum']
            orders = Order()   
            print('='*100+ f'\nДобро пожаловать {user_name}\n'+ '='*100)
            flag1 = False

    while True:
        print('Выберите команду\n1-сделать заказ\t2-удалить заказ\n',
                '3-список всех товаров\t4-список корзины\n',
                '5-совершить покупку\t6-пополнить кошелёк\n'+'7-выход\n'+
                '='*100)
                
        choice_ = input('Enter a command: ')
        
        print('='*100)
        if choice_ == '1':
            car_id = int(input('Введите ID продукта: '))
            print('='*100)
            print(orders.create_order(car_id))

        elif choice_ == '2':
            car_id = int(input('Введите ID продукта: '))
            print('='*100)
            print(orders.delete_order(car_id))

        elif choice_ == '3':
            print(orders.listing())

        elif choice_ == '4':
            print(orders.list_of_orders())

        elif choice_ == '5':
            data_buyer[index_]['user_sum'] -= orders.total
            print(orders.to_buy(user_sum))
            json.dump(data_buyer, open('data_buyer.json', 'w'))

        elif choice_ == '6':
            coin = round(float(input('Введите ID продукта: ')), 1)
            data_buyer[index_]['user_sum'] += coin
            print(orders.to_buy(user_sum))
            json.dump(data_buyer, open('data_buyer.json', 'w'))
        
        elif choice_ == '7':
            print('Работа завершена')
            print('='*100)
            break

        else: print('The command not found')

        print('='*100+'\n\n')
        

def menu_salesman():
    flag1 = True

    with open('data_buyer.json') as file:
        data_buyer = json.load(file)
        print(data_buyer)

        while flag1:
            user_name = input('user_name: ')
            password = input('password: ')
            user = list(filter(lambda x: x['user_name']==user_name and x['password']==password, data_buyer))
            if not user:
                print('Неправильное имя или пароль')
                answer = input('Попробовать снова? (no?): ')
                if answer.lower() == 'no':
                    input_menu()
                continue
            index_ = data_buyer.index(user[0])
            user_sum = data_buyer[index_]['user_sum']
            orders = Order()   
            print('='*100+ f'\nДобро пожаловать {user_name}\n'+ '='*100)
            flag1 = False






    while True:
        print('Выберите команду\n1-сделать заказ\t2-удалить заказ\n',
                '3-список всех товаров\t4-список корзины\n',
                '5-совершить покупку\t6-пополнить кошелёк\n'+'7-выход\n'+
                '='*100)
                
        choice_ = input('Enter a command: ')
        
        print('='*100)
        if choice_ == '1':
            car_id = int(input('Введите ID продукта: '))
            print('='*100)
            print(orders.create_order(car_id))

        elif choice_ == '2':
            car_id = int(input('Введите ID продукта: '))
            print('='*100)
            print(orders.delete_order(car_id))

        elif choice_ == '3':
            print(orders.listing())

        elif choice_ == '4':
            print(orders.list_of_orders())

        elif choice_ == '5':
            data_buyer[index_]['user_sum'] -= orders.total
            print(orders.to_buy(user_sum))
            json.dump(data_buyer, open('data_buyer.json', 'w'))

        elif choice_ == '6':
            coin = round(float(input('Введите ID продукта: ')), 1)
            data_buyer[index_]['user_sum'] += coin
            print(orders.to_buy(user_sum))
            json.dump(data_buyer, open('data_buyer.json', 'w'))
        
        elif choice_ == '7':
            print('Работа завершена')
            print('='*100)
            break

        else: print('The command not found')

        print('='*100)


    



#  регистрация

# class User:
#     def __init__(self, name, password):
#         self.username = name
#         self.__password = password

#     @property
#     def password(self):
#         raise Exception('Password write only')

#     @password.setter
#     def password(self, password):
#         if not isinstance(password, str):
#             raise Exception('Invalid value for password')

    

# def input_registr():
#     print('Войти в аккаунт: \nРегистрация: 2')
#     answer = input('Введите выбор: ')
#     if answer == '1': 
#         user_name = input('Введите имя пользователя: ')
#         user_password = input('Введите пароль пользователя: ')

#         if 

# while input_registr() == None:
#     input_registr()


# user1 = User('Bakr', '1234')
# print(user1.username)
# user1.password = '567'
# print(jhon._hashed_password)

input_menu()