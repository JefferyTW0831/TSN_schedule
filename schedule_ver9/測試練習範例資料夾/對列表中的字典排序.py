
#使用 lambda 函數進行複雜排序

def main():
    students = [
        {'name': 'John', 'age': 25, 'grade': 88},
        {'name': 'Jane', 'age': 22, 'grade': 92},
        {'name': 'Dave', 'age': 30, 'grade': 85}
    ]
    sorted_students = sorted(students, key=lambda x: x['age'])
    print(sorted_students)

main()