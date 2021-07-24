def moving_avarage():
    numbers = [1, 2, 3, 7, 9]
    window_size = 1

    i = 0
    moving_averages = []
    while i < len(numbers) - window_size + 1:
        this_window = numbers[i : i + window_size]

        window_average = sum(this_window) / window_size
        moving_averages.append(window_average)
        i += 1

    print(moving_averages)

moving_avarage()