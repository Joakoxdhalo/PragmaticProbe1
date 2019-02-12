def high(num):
    if num == 1:
        return 1
    else:
        return (num ** 2) + high(num - 1)


def low(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return (num ** 2) + low(num - 2)


def cubes_in_high(num):
    base = 2
    temp = high(base)
    cubes_list = []
    while(temp <= num):
        cubes_list.append([temp, "H", base])
        base = base + 1
        temp = high(base)

    return cubes_list


def cubes_in_low(num):
    base = 3
    temp = low(base)
    cubes_list = []
    while(temp <= num):
        cubes_list.append([temp, "L", base])
        base = base + 1
        temp = low(base)
    return cubes_list


def min_and_max_header(cubes_list, cubes):
    addition = 0
    min_header_index = int()
    max_header_index = int()

    for i in range(0, len(cubes_list), 1):
        if addition < cubes:
            header = cubes_list[i][0]
            addition = addition + header
            min_header_index = i
        else:
            break

    for i in range(0, len(cubes_list), 1):
        if cubes_list[i][0] <= cubes:
            max_header_index = i
        else:
            break
    return min_header_index, max_header_index


def main():
    list_of_cubes = []
    print("Enter the three lines of the input:")
    for i in range(3):
        list_of_cubes.append(int(input))
    final_result = ""
    case = 0

    for cubes in list_of_cubes:
        case += 1
        cubes_low = []
        cubes_high = []
        if cubes < 10 and cubes != 5:
            print("case {}: {}".format(case, "Impossible"))
            continue
        cubes_low = cubes_in_low(cubes)
        cubes_high = cubes_in_high(cubes)
        cubes_list = cubes_low + cubes_high
        cubes_list.sort(key=lambda x: x[0])
        lower_i, upper_i = min_and_max_header(cubes_list, cubes)
        list_solution = []
        result = recursive(cubes, lower_i, upper_i, cubes_list, list_solution)
        final_result = ""
        if result == "Impossible":
            print("case {}: {}".format(case, "Impossible"))
        else:
            for index in range(len(result)):
                final_result = "{} {}{}".format(final_result, result[index][2], result[index][1])
            print("case {}: {}".format(case, final_result))


def recursive(cubes, lower_i, upper_i, cubes_list, solution):
    for index in range(upper_i, lower_i - 1, -1):
        cubes_rest = cubes - cubes_list[index][0]
        solution.append(cubes_list[index])
        if cubes_rest == 0:
            return solution
        elif cubes_rest < 10 and cubes_rest != 5:
            solution.pop()
            continue
        else:
            lower_i, upper_i = min_and_max_header(cubes_list, cubes_rest)
            return recursive(cubes_rest, lower_i, upper_i, cubes_list, solution)
    return "Impossible"


if __name__ == '__main__':
    main()
