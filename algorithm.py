import asyncio
import random
import math
from decimal import Decimal
import pandas as pd
import numpy as np
from constant import name
from constant import data_x as x
from constant import data_y as y

df = pd.read_excel('distance.xlsx', index_col=0, header=0)
np = df.to_numpy()

class Map:
    def __init__(self):
        self.cities = []
    def add_city(self, index):
        self.cities.append((x[index], y[index]))
    def remove_city(self, index):
        self.cities.pop(index)
class SimulatedAnnealing:
    def __init__(self, map, initial_temperature, cooling_factor, delay, cost_per_km):
        self.map = map
        self.delay = delay
        self.initial_temperature = initial_temperature
        self.cooling_factor = cooling_factor
        self.cost_per_km = cost_per_km
        self.isRunning = True
    result = []
    current_solution = []
    def get_cities(self):
        return self.map.cities
    def convert_solution_to_name(self, solution):
        list_name = []
        for index in solution:
            city = self.map.cities[index]
            i = x.index(city[0])
            list_name.append(name[i])
        return list_name
    def distance_real(self, city1, city2):
        index1 = name.index(city1)
        index2 = name.index(city2)
        return float(np[index1][index2])
    def caculate_distance(self, solution):
        name_list = self.convert_solution_to_name(solution)
        print(name_list)
        total_distance = 0
        for i in range(len(name_list) - 1):
            city1 = name_list[i]
            city2 = name_list[i + 1]
            print(self.distance_real(city1, city2))
            total_distance += self.distance_real(city1, city2)
        total_distance += self.distance_real(name_list[-1], name_list[0])
        print(self.distance_real(name_list[-1], name_list[0]))
        print(total_distance)
        return round(total_distance, 2)
    def caculate_cost(self, total_distance):
        return total_distance * self.cost_per_km
    # Tạo một giải pháp ban đầu
    def initial_solution(self):
        solution = list(range(len(self.map.cities)))
        random.shuffle(solution)
        return solution

    # Sinh một giải pháp mới
    def generate_new_solution(self, current_solution):
        # Lựa chọn hai vị trí ngẫu nhiên
        i = random.randint(0, len(current_solution) - 1)
        j = random.randint(0, len(current_solution) - 1)
        # Hoán đổi hai thành phố ở hai vị trí đó
        new_solution = current_solution[:]
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        return new_solution

    # Thuật toán Simulated Annealing
    async def provide_result(self):
        await asyncio.sleep(self.delay)
        return self.result
    async def solve(self):
        # Khởi tạo giải pháp ban đầu
        current_solution = self.initial_solution()
        # Lưu trữ giải pháp tốt nhất
        best_solution = current_solution[:]
        # Khởi tạo nhiệt độ ban đầu
        temperature = self.initial_temperature
        # Lặp lại cho đến khi nhiệt độ giảm đến giá trị nhỏ
        i = 0
        while temperature > 1e-5 and self.isRunning == True:
            i += 1
            self.current_solution = current_solution[:]
            await asyncio.sleep(self.delay)
            # Lưu trữ giải pháp hiện tại
            temp_str = round(Decimal(temperature), 8)
            temp_solution = current_solution[:]
            temp_solution.append(current_solution[0])
            result = [i, temp_str, self.convert_solution_to_name(temp_solution), self.caculate_distance(current_solution), self.caculate_cost(self.caculate_distance(current_solution))]
            
            # Sinh một giải pháp mới
            new_solution = self.generate_new_solution(current_solution)
            # Tính toán sự khác biệt về chi phí giữa hai giải pháp
            delta = self.caculate_distance(new_solution) - self.caculate_distance(current_solution)
            # Nếu giải pháp mới tốt hơn giải pháp hiện tại, chấp nhận giải pháp mới
            if delta < 0:
                current_solution = new_solution[:]
                # Kiểm tra xem giải pháp mới có tốt hơn giải pháp tốt nhất hiện tại hay không
                if self.caculate_distance(current_solution) < self.caculate_distance(best_solution):
                    best_solution = current_solution[:]
                # Nếu giải pháp mới không tốt hơn giải pháp hiện tại
                else:
                # Tính xác suất chấp nhận giải pháp mới dựa trên nhiệt độ hiện tại
                    p = math.exp(-delta / temperature)
                    # Nếu xác suất chấp nhận giải pháp mới lớn hơn một giá trị ngẫu nhiên, chấp nhận giải pháp mới
                    if random.random() < p:
                        current_solution = new_solution[:]    
            # Giảm nhiệt độ
            temperature = temperature*self.cooling_factor
            temp_str = round(Decimal(temperature), 8)
            result.append(temperature)
            self.result.append(result)
