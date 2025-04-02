# Aku
# Вариант 1 (Steam)
# Класс обрабатывающий датафрейм и выводящий на экран статистику в виде гистограммы

import getpass
from datetime import date, datetime
import pandas as pd
import os
import matplotlib.pyplot as plt

def log(func):
    def wrapper(*args, **kwargs):
        original_result = func(*args, **kwargs)

        user_name = getpass.getuser()
        funs_name = func.__name__
        formatted_date = date.today().strftime("%d %m %Y")
        formatted_time = datetime.now().strftime("%H:%M:%S")

        if os.path.isfile("logs.csv"):
            print('Файл существует')
            # Читаем существующий файл и добавляем новую запись
            file_df = pd.read_csv("logs.csv")
            df = pd.DataFrame([[len(file_df), user_name, funs_name, formatted_date, formatted_time]],
                              columns=['id', 'user_name', 'funs_name', 'formatted_date', 'formatted_time'])
            df.to_csv("logs.csv", mode='a', index=False, header=False)  # Дописываем запись без заголовков
        else:
            print('Файл не существует')
            # Создаем новый файл с заголовками и первой записью
            df = pd.DataFrame([[0, user_name, funs_name, formatted_date, formatted_time]],
                              columns=['id', 'user_name', 'funs_name', 'formatted_date', 'formatted_time'])
            df.to_csv("logs.csv", index=False)  # Сохраняем с заголовками

        return original_result
    return wrapper


class Graphical_statistics:
    def __init__(self):
        self.file_path = "steam_players.csv"
        self.dataframe = None

    @log
    def load_dataframe(self):
        if os.path.isfile(self.file_path):
            self.dataframe = pd.read_csv(self.file_path)
            print("Данные успешно загружены:")
            print(self.dataframe.head())
        else:
            print("Файл не найден!")

    @log
    def show_statistics(self):
        if self.dataframe is not None:
            print("Статистика по файлу:")
            print(self.dataframe.describe())
            print("Количество значений по странам:")
            print(self.dataframe['country'].value_counts())
        else:
            print("Датафрейм не загружен!")

    @log
    def plot_histogram(self):
        if self.dataframe is not None:
            if 'country' in self.dataframe.columns:
                # Убираем пропуски и подсчитываем количество игроков по странам
                country_counts = self.dataframe['country'].dropna().value_counts()
                
                # Фильтруем страны (там где >= 1000 игроков в гистограмму не вошли)
                filtered_counts = country_counts[country_counts >= 1000]

                # Переводим количество игроков в тысячи
                filtered_counts = filtered_counts / 1000

                # Построение гистограммы
                filtered_counts.plot(kind='bar', color='skyblue')
                plt.title('Количество игроков Steam') 
                plt.xlabel('Страны')  
                plt.ylabel('Количество игроков (тыс.)')  
                plt.tight_layout()  
                plt.show()
            else:
                print("Столбец 'country' не найден в датафрейме!")
        else:
            print("Датафрейм не загружен!")



processor = Graphical_statistics()
processor.load_dataframe()  
processor.show_statistics()  
processor.plot_histogram() 
