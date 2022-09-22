import json


DATA_CAR_FILE_JSON = 'data_cars.json'


def get_data():
    '''
    for get list of data from json file
    '''
    with open(DATA_CAR_FILE_JSON) as file:
        if not file: return [] 
        return json.load(file)

class CreateMixin:
    @staticmethod
    def create_product():
        data = get_data()
        list_of_id = [i['id'] for i in data] # список всех существующих ID
        id_ = 1

        while id_ in list_of_id: id_ += 1 # Если уже есть такое ID, то икременция продолжиться

        product_ = dict(id=id_, 
                        brand= input('Введите бренд: '),
                        model = input('Введите модель: '),
                        release = int(input('Введите дату релиза: ')),
                        volume = int(input('Введите объем: ')),
                        color = input('Введите цвет: '),
                        body = input('Выберите тип кузова:\n1-седан\t2-универсал\t3-купе\n4-минивен\t5-внедорожник\t6-пикап'),
                        mileage = int(input('Введите пробег: ')),
                        price = round(float(input('Введите цену: ')), 1))

        if product_['body']=='1': product_['body']='Седан' 
        elif product_['body']=='2': product_['body']='Универсал'
        elif product_['body']=='3': product_['body']='Купе'
        elif product_['body']=='4': product_['body']='Минивен'
        elif product_['body']=='5': product_['body']='Внедорожник'
        elif product_['body']=='6': product_['body']='Пикап'
        else: 
            print('Ошибка в вводе данных "тип кузова"')
            CreateMixin.create_product()

        data.append(product_)
        json.dump(data, open(DATA_CAR_FILE_JSON, 'w'))
        return {'status:': 201, 'msg:': product_}


class UpdateMixin:
    @staticmethod
    def update():
        '''
        update one product in data
        '''
        data = get_data()
        id_ = int(input('Enter the ID of the product you want to CHAGE: '))
        product = list(filter(lambda x: x['id']==id_, data))
        if not product: return {'status': 404, 'msg': 'NOT FOUND'}
        index_ = data.index(product[0])

        data[index_]['brand']= input('Введите бренд: '),
        data[index_]['model']= input('Введите модель: '),
        data[index_]['releasse']= int(input('Введите дату релиза: ')),
        data[index_]['volume']= int(input('Введите объем: ')),
        data[index_]['color']= input('Введите цвет: '),
        data[index_]['body']= input('Выберите тип кузова:\n1-седан\t2-универсал\t3-купе\n4-минивен\t5-внедорожник\t6-пикап'),
        data[index_]['mileage']= int(input('Введите пробег: ')),
        data[index_]['price']=  round(float(input('Введите цену: ')), 1)

        if data[index_]['body']=='1': data[index_]['body']='Седан' 
        elif data[index_]['body']=='2': data[index_]['body']='Универсал'
        elif data[index_]['body']=='3': data[index_]['body']='Купе'
        elif data[index_]['body']=='4': data[index_]['body']='Минивен'
        elif data[index_]['body']=='5': data[index_]['body']='Внедорожник'
        elif data[index_]['body']=='6': data[index_]['body']='Пикап'
        else: 
            print('Ошибка в вводе данных "тип кузова"')
            UpdateMixin.update()

        if False in data[index_].values():
            print('Ошибка в вводе данных "тип кузова"')
            UpdateMixin.update()

        json.dump(data, open(DATA_CAR_FILE_JSON, 'w'))
        return {'status': 206, 'msg': 'UPDATED!'}


class RetrieveMixin:
    def get(self, id_):
        data = get_data()
        product = list(filter(lambda x: x['id']==id_, data))
        if not product: return {'status': 404, 'msg': 'NOT FOUND'}
        return product[0]
        
    def get_detail(self, id_):
        '''
        get one product from data
        '''
        data = get_data()
        product = list(filter(lambda x: x['id']==id_, data))
        if not product: return {'status': 404, 'msg': 'NOT FOUND'}

        index_ = data.index(product[0])
        return {'status': 200, 'msg': [data[index_]['brand'],
                                        data[index_]['body'],
                                        data[index_]['price']]} 


class DestroyMixin:
    def delete(self, id_):
        '''
        delete product in data
        '''
        data = get_data()        
        product = list(filter(lambda x: x['id']==id_, data))
        if not product: return {'status': 404, 'msg': 'NOT FOUND'}
        index_ = data.index(product[0])
        data.pop(index_)
        json.dump(data, open(DATA_CAR_FILE_JSON, 'w'))
        return {'status': 204, 'msg': 'DELETED!'}


class ListingMixin:
    @staticmethod
    def listing():
        data=get_data()
        pillor_of_id = [len('id')]
        pillor_of_brand = [len('brand')]
        pillor_of_model = [len('model')]
        pillor_of_release = [len('release')]
        pillor_of_volume = [len('volume')]
        pillor_of_color = [len('color')]
        pillor_of_body = [len('body')]
        pillor_of_mileage = [len('mileage')]
        pillor_of_price = [len('price')]

        [pillor_of_id.append(len(str(i['id']))) for i in data]
        [pillor_of_brand.append(len(i['brand'])) for i in data]
        [pillor_of_model.append(len(i['model'])) for i in data]
        [pillor_of_release.append(len(str(i['release']))) for i in data]
        [pillor_of_volume.append(len(str(i['volume']))) for i in data]
        [pillor_of_color.append(len(i['color'])) for i in data]
        [pillor_of_body.append(len(i['body'])) for i in data]
        [pillor_of_mileage.append(len(str(i['mileage']))) for i in data]
        [pillor_of_price.append(len(str(i['price']))) for i in data]

        max_len_id = max(pillor_of_id)
        max_len_brand = max(pillor_of_brand)
        max_len_model = max(pillor_of_model)
        max_len_release = max(pillor_of_release)
        max_len_volume = max(pillor_of_volume)
        max_len_color = max(pillor_of_color)
        max_len_body = max(pillor_of_body)
        max_len_mileage = max(pillor_of_mileage)
        max_len_price = max(pillor_of_price)

        if not data: return 'HAVEN\'T PRODUCTS'

        def plus_minus():
            print('--'+'-'*max_len_id+'--'+
            '+'+'--'+'-'*max_len_brand +'--'+
            '+'+'--'+'-'*max_len_model +'--'+
            '+'+'--'+'-'*max_len_release +'--'+
            '+'+'--'+'-'*max_len_volume +'--'+
            '+'+'--'+'-'*max_len_color +'--'+
            '+'+'--'+'-'*max_len_body +'--'+
            '+'+'--'+'-'*max_len_mileage +'--'+
            '+'+'--'+'-'*max_len_price +'--')
        
        plus_minus()
        print('  ' +'id'+' '*(max_len_id-len('id')) + 
            '  |  '+'brand'+' '*(max_len_brand - len('brand'))+
            '  |  '+'model'+' '*(max_len_model - len('model'))+
            '  |  '+'release'+' '*(max_len_release - len('release'))+
            '  |  '+'volume'+' '*(max_len_volume - len('volume'))+
            '  |  '+'color'+' '*(max_len_color - len('color'))+
            '  |  '+'body'+' '*(max_len_body - len('body'))+
            '  |  '+'mileage'+' '*(max_len_mileage - len('mileage'))+
            '  |  '+'price'+' '*(max_len_price - len('price')))

        plus_minus()
        for elem in data:
            print('  ' +f'{elem["id"]}'+' '*(max_len_id - len(f'{elem["id"]}')) + 
                '  |  '+f'{elem["brand"]}'+' '*(max_len_brand - len(f'{elem["brand"]}'))+
                '  |  '+f'{elem["model"]}'+' '*(max_len_model - len(f'{elem["model"]}'))+
                '  |  '+f'{elem["release"]}'+' '*(max_len_release - len(f'{elem["release"]}'))+
                '  |  '+f'{elem["volume"]}'+' '*(max_len_volume - len(f'{elem["volume"]}'))+
                '  |  '+f'{elem["color"]}'+' '*(max_len_color - len(f'{elem["color"]}'))+
                '  |  '+f'{elem["body"]}'+' '*(max_len_body - len(f'{elem["body"]}'))+
                '  |  '+f'{elem["mileage"]}'+' '*(max_len_mileage - len(f'{elem["mileage"]}'))+
                '  |  '+f'{elem["price"]}'+' '*(max_len_price - len(f'{elem["price"]}')))

        plus_minus()
        return '\t\t\t\tLIST OF PRODUCTS'

data = get_data()
print(ListingMixin.listing())