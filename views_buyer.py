class CreateBuyerMixin:
    def _get_of_set_user_and_id(self):
        try:
            if(self.users or not self.users):
                pass

        except (NameError, AttributeError):
            self.users = []
            

    def create_user(self, **kwargs):
        self._get_of_set_user_and_id()
        list_of_user_names = [i['name'] for i in self.users]
        
        while True:
            product_ = dict(name= input('User_name'),
                            password= input('Password: '),
                            summa= round(float(input('Cash: ')), 1))
            if product_['name'] in list_of_user_names:
                print('Уже есть пользователь с таким именем')
            else: break

        self.users.append(product_)
        return {'STATUS:': 201, 'MSG:': product_}
