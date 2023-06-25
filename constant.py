import numpy as np


# data_x = np.array([200, 250, 425, 230, 730, 310, 370, 420, 460, 386, 410, 448, 492, 473, 538, 521, 461, 373, 580, 553, 776, 534])
# data_y = np.array([50, 250, 280, 630, 380, 520, 440, 410, 345, 543, 507, 489, 471, 430, 421, 489, 526, 604, 562, 690, 997, 522])

# cities = [{'x': data_x[i], 'y': data_y[i]} for i in range(len(data_x))]

# cities_name = []

name = ["Củ Chi", "Hooc Môn", "Quận 12", "Bình Chánh", "Bình Tân", "Tân Phú", "Tân Bình", "Gò Vấp", "Bình Thạnh", "Thành phố Thủ Đức", "Quận 6", "Quận 11", "Quận 5", "Quận 10", "Quận 3", "Quận 1", "Quận 4", "Quận 8", "Quận 7", "Nhà Bè", "Cần Giờ"]

data_x = [200, 250, 425, 155, 300, 353, 395, 430, 510, 700, 365, 388, 437, 430, 465, 490, 507, 360, 555, 522, 738]
data_y = [950, 750, 745, 515, 510, 585, 615, 680, 615, 640, 495, 528, 510, 544, 563, 547, 520, 445, 470, 361, 93]
data_xy = [{"x" : data_x[i], "y" : data_y[i]} for i in range(len(data_x))]