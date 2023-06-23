import asyncio
import random
import math
from decimal import Decimal
import pandas as pd
import numpy as np

x = [200, 250, 425, 155, 300, 353, 395, 430, 510, 700, 365, 388, 437, 430, 465, 490, 507, 360, 555, 522, 738]
y = [950, 750, 745, 515, 510, 585, 615, 680, 615, 640, 495, 528, 510, 544, 563, 547, 520, 445, 470, 361, 93]
name = ["Củ Chi", "Hooc Môn", "Quận 12", "Bình Chánh", "Bình Tân", "Tân Phú", "Tân Bình", "Gò Vấp", "Bình Thạnh", "Thành phố Thủ Đức", "Quận 6", "Quận 11", "Quận 5", "Quận 10", "Quận 3", "Quận 1", "Quận 4", "Quận 8", "Quận 7", "Nhà Bè", "Cần Giờ"]

data = [{"name": "Củ Chi", "x": 200, "y": 950}, {"name": "Hooc Môn", "x": 250, "y": 750}, {"name": "Quận 12", "x": 425, "y": 745}, {"name": "Bình Chánh", "x": 155, "y": 515}, {"name": "Bình Tân", "x": 300, "y": 510}, {"name": "Tân Phú", "x": 353, "y": 585}, {"name": "Tân Bình", "x": 395, "y": 615}, {"name": "Gò Vấp", "x": 430, "y": 680}, {"name": "Bình Thạnh", "x": 510, "y": 615}, {"name": "Thành phố Thủ Đức", "x": 700, "y": 640}, {"name": "Quận 6", "x": 365, "y": 495}, {"name": "Quận 11", "x": 388, "y": 528}, {"name": "Quận 5", "x": 437, "y": 510}, {"name": "Quận 10", "x": 430, "y": 544}, {"name": "Quận 3", "x": 465, "y": 563}, {"name": "Quận 1", "x": 490, "y": 547}, {"name": "Quận 4", "x": 507, "y": 520}, {"name": "Quận 8", "x": 360, "y": 445}, {"name": "Quận 7", "x": 555, "y": 470}, {"name": "Nhà Bè", "x": 522, "y": 361}, {"name": "Cần Giờ", "x": 738, "y": 93}]

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
            # Trả về giải pháp tốt nhất 
        # return best_solution
def random_city(number):
    cities = []
    for i in range(number):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        cities.append((x, y))
    return cities

def create_city():
    x = [200, 250, 425, 155, 300, 353, 395, 430, 510, 700, 365, 388, 437, 430, 465, 490, 507, 360, 555, 522, 738]
    y = [950, 750, 745, 515, 510, 585, 615, 680, 615, 640, 495, 528, 510, 544, 563, 547, 520, 445, 470, 361, 93]
    city = []
    for i in range(len(x)):
        city.append((x[i], y[i]))
    return city
def main():
    # Định nghĩa bản đồ
    cities = [
        (0, 0),
        (1, 2),
        (3, 1),
        (5, 3),
        (6, 5),
        (4, 6),
        (2, 5),
        (1, 4)
    ]
    map = Map(cities)
    # Khởi tạo thuật toán
    initial_temperature = 100
    cooling_factor = 0.25
    sa = SimulatedAnnealing(map, initial_temperature, cooling_factor)
    # Giải bài toán
    best_solution = sa.solve()
    print("Giải pháp tốt nhất:", best_solution)
    print("Chi phí tốt nhất:", sa.cost(best_solution))
    # Hiển thị kết quả