from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


class Model:
    def __init__(self):
        self.model = None
        self.tranformer = None
        self.x_data = self._get_train_data()[0]
        self.y_data = self._get_train_data()[1]

    @staticmethod
    def _get_train_data():
        '''
        Получаем данные для обучения модели
        :return:
        X - матрица признаков
        y - вектор таргетов
        '''
        df = pd.read_json('clear_data.txt')
        district_vector = pd.get_dummies(df['district'])
        prepare_df = pd.concat([df, district_vector], axis=1).drop(columns=['district'])
        prepare_df['floor_to_max'] = prepare_df['max_floor'] - prepare_df['floor']
        X = prepare_df[
            ['room_number', 'floor', 'general_area', 'living_area', 'kitchen_area', 'Ленинский', 'Орджоникидзевский',
             'Правобережный', 'floor_to_max']]
        y = prepare_df['price']
        return X, y

    def fit(self):
        logging.info('Обучаю модель...')
        transformer = StandardScaler()
        transformer.fit(self.x_data)
        x_transform = transformer.transform(self.x_data)
        self.tranformer = transformer
        logging.info('Трансформации сохранены')
        model = RandomForestRegressor()
        model.fit(x_transform, self.y_data)
        logging.info('Модель обучена успешно!')
        self.model = model

    @staticmethod
    def _get_dummies(district_name):
        '''
        Векторизирует название района
        :param district_name: название района
        :return: district_dict
        '''
        district_dict = {
            'Ленинский': 0,
            'Орджоникидзевский': 0,
            'Правобережный': 0
        }
        district_dict[district_name] += 1
        return district_dict

    def predict(self, object: dict):
        '''
        Метод возвращающий предсказание для объекта по признакам
        Список признаков:
        - room_number
        - district
        - floor
        - max_floor
        - general_area
        - living_area
        - kitchen_area
        :param object: dict - признаки объекта
        :return: price predict - предсказание цены
        '''
        if (self.model is None) or (self.tranformer is None):
            self.fit()
        logging.info('Выполняю предобработку данных')
        object['floor_to_max'] = object['max_floor'] - object['floor']
        if (object['district'] is None) or (object['district'] == ''):
            with open('room_number_to_common_district.txt', 'r') as file:
                room_number_to_common_district = json.load(file)
            object['district'] = room_number_to_common_district[object['room_number']]
        dummies = self._get_dummies(object['district'])
        for elem in dummies:
            object[elem] = dummies[elem]
        logging.info('Предсказываю цену объекта')
        feauture_names = [
            'room_number',
            'floor',
            'general_area',
            'living_area',
            'kitchen_area',
            'Ленинский',
            'Орджоникидзевский',
            'Правобережный',
            'floor_to_max'
        ]
        object_for_predict = pd.DataFrame([[object[feature] for feature in feauture_names]], columns=feauture_names)
        trasform_object_for_predict = self.tranformer.transform(object_for_predict)
        predicted_price = self.model.predict(trasform_object_for_predict)
        return {'predicted_price': predicted_price[0]}


if __name__ == '__main__':
    test_object = {
        'room_number': 1,
        'floor': 4,
        'max_floor': 10,
        'general_area': 40.4,
        'living_area': 19.0,
        'kitchen_area': 12.0,
        'district': 'Орджоникидзевский'
    }
    model = Model()
    print(model.predict(test_object))
