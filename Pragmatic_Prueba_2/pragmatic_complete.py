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
    # print("Enter the three lines of the input:")

    # for i in range(3):
    #     list_of_cubes.append(int(input()))

    list_of_cubes = [78, 59, 52, 29, 28, 0]
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
    print(f"cubes: {cubes}")
    print(f"cubes list: {cubes_list}")
    print(f'upper_i{upper_i} lower_i{lower_i}')
    print(f'upper: {cubes_list[upper_i]} lower: {cubes_list[lower_i]}')
    if upper_i < lower_i:
        return "Impossible"
    if cubes_list[upper_i] not in solution:
        print(f"appending {cubes_list[upper_i]}")
        solution.append(cubes_list[upper_i])
        cubes_rest = cubes - cubes_list[upper_i][0]
        print(f'cubes_rest: {cubes_rest}')
        print(f'current_index: {cubes_list[upper_i][0]}')

        if cubes_rest == 0:
            print(f"The complete solution is... {solution}")
            return solution

        elif (cubes_rest < 10 and cubes_rest != 5):
            print(f"deleting: {cubes_list[upper_i]}")
            solution.pop()
            print("Here is not the way")
        else:
            lower_i_second_lvl, upper_i_second_lvl = min_and_max_header(cubes_list, cubes_rest)
            print("Calling inner function...")
            partial_solution = recursive(cubes_rest, lower_i_second_lvl, upper_i_second_lvl, cubes_list, solution)

            if partial_solution != "Impossible":
                print("Returning solution from inner... ")
                return partial_solution
            else:
                print(f"Deleting value: {cubes_list[upper_i]}")
                solution.pop()

    else:
        pass
        print(f"repeated value catched: {cubes_list[upper_i]}")
    print("Calling outter function...")
    return recursive(cubes, lower_i, upper_i - 1, cubes_list, solution)


if __name__ == '__main__':
    main()
