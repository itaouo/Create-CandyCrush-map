import math
import capture

def writeData(path):
    data = []
    with open(path + ".txt", "r", encoding="utf-8") as file:
        for line in file:
            # 去掉每行的換行符，然後用制表符分隔
            row = line.strip().split(" ")
            # 將字符串轉換為數字
            row = list(map(int, row))
            # 將行添加到二維陣列中
            data.append(row)
    return data

def sortCandy(data):
    sorted_data = sorted(data, key=lambda x: (x[0], x[1]))
    return sorted_data

def classify_y(data):
    min_y = data[0][1]
    max_y = data[0][1]
    max_width = 0
    candy_map = []
    
    while len(data):
        width = 0
        for i in data:
            if min_y > i[1]:
                min_y = i[1]
            if max_y < i[1]:
                max_y = i[1]
            if width == 0:
                sum_y = i[0]
                width = 1
                candy_map_row = [i[1:]]
            elif abs(sum_y/width - i[0]) < 20:
                sum_y += i[0]
                width += 1
                candy_map_row.append(i[1:])
            else:
                break
        # if width > max_width:
        #   max_width = width
        candy_map.append(candy_map_row)
        for i in range(width):
            data.pop(0)
    # if round((max_y-min_y)/80) > max_width:
    max_width = round((max_y-min_y)/80)
    print("qqq",max_y,min_y)
    return candy_map, max_width, min_y

def classify_x(data, width, min_y):
    candy_map = []
    for j in range(len(data)):
        temp_row = sortCandy(data[j])
        row = []
        print(temp_row)
        anchor = min_y
        for k in range(width):
            if k > len(temp_row) - 1:
                temp_row.insert(k, [anchor, -99])
            elif abs(temp_row[k][0] - anchor) > 20:
                temp_row.insert(k, [anchor, -99])
            else:
                anchor = temp_row[k][0]
            anchor += 80
        for k in range(width):
            row.append(temp_row[k][1])
        candy_map.append(row)
    return candy_map, len(data)

def classify(data):
    candy_map_y, width, min_y = classify_y(data)
    print(candy_map_y)
    candy_map_xy, length = classify_x(candy_map_y, width, min_y)
    return candy_map_xy, width, length
    

def main():
    for i in range(4, 5):
        data = writeData("outputs/data/" + str(i))
        data = sortCandy(data)
        candy_map, width, length = classify(data)
        print(candy_map, width, length)
        capture.writeData("outputs/init_maps/" + str(i), [[width, length]])
        capture.writeData("outputs/candy_maps/" + str(i), candy_map)
        
main()
