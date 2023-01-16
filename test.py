# from datetime import datetime, timedelta
#
# weeks = []
# year = 2023
#
# for i in range(1, 53):
#     week_start = datetime.strptime(f'{year}-W{i}-1', '%Y-W%U-%w')
#     week_end = week_start + timedelta(days=6)
#     week_str = f'w23-{i}' + ' ' + week_start.strftime('%d-%m-%Y') + ' to ' + week_end.strftime('%d-%m-%Y')
#     weeks.append(week_str)
#
# print(weeks)
#
# current_year = datetime.now().year
# print(current_year)
#
# def test(value):
#     result = True if value else False
#     return result
#
# a= ''
# print(a == None)
import itertools
list1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
list2 = [10, 20, 30]
# result = [[i]+[j] for j in list2 for i in list1]
result = [i+[j] for i, j in itertools.product(list1, list2)]
print(result)
