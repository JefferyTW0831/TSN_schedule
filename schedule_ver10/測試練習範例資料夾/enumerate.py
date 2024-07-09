
result_sort_mode = {
    1:"123",
    2:"456"
}

def main():
    for amount, sort_type in enumerate(result_sort_mode.values(), start=1):
        print(amount)
        print(sort_type)

main()