import numpy as np

# Tên các địa điểm có sẵn   
name = ["Củ Chi", "Hooc Môn", "Quận 12", "Bình Chánh", "Bình Tân", "Tân Phú", "Tân Bình", "Gò Vấp", "Bình Thạnh", "Thành phố Thủ Đức", "Quận 6", "Quận 11", "Quận 5", "Quận 10", "Quận 3", "Quận 1", "Quận 4", "Quận 8", "Quận 7", "Nhà Bè", "Cần Giờ"]

# Tọa độ các địa điểm trên trục toạ độ x, y (limit 1000: 1000)
data_x = [200, 250, 425, 155, 300, 353, 395, 430, 510, 700, 365, 388, 437, 430, 465, 490, 507, 360, 555, 522, 738]
data_y = [950, 750, 745, 515, 510, 585, 615, 680, 615, 640, 495, 528, 510, 544, 563, 547, 520, 445, 470, 361, 93]
data_xy = [{"x" : data_x[i], "y" : data_y[i]} for i in range(len(data_x))]