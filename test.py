def custom_sort(elem):
    return elem[0], elem[1]

def sort_by_first_then_second(elements):
    return sorted(elements, key=custom_sort)

# 範例使用
all_result = [(3, 2), (1, 5), (2, 3), (1, 2)]
sorted_points = sort_by_first_then_second(all_result)
print(sorted_points)