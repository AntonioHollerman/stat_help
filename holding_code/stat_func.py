from typing import List
import openpyxl
from statistics import stdev, mean
from math import factorial, e, pi, erf
from scipy.special import erfinv
from scipy.stats import t, norm
import math


def find_frequency(ranges: List[tuple], num_list: List[int]):
    """
    Calculates the frequency of numbers within specified ranges.

    Given a list of ranges and a list of numbers, this function counts the occurrences
    of numbers within each range and  returns a dictionary with the range tuples as keys
    and the corresponding frequencies as values.

    :param ranges: A list of tuples representing the ranges.
    :type ranges: List[tuple]
    :param num_list: A list of numbers.
    :type num_list: List[int]
    :return: A dictionary with the range tuples as keys and their frequencies as values.
    :rtype: dict
    """
    answers = {}
    for low, high in ranges:
        to_append = 0
        for num in num_list:
            if (num >= low) and (num <= high):
                to_append += 1
        answers[(low, high)] = to_append
    return answers


def process_excel_file(file_path: str, row_wanted: int = 0, single_row: bool = False, group_data: bool = False,
                       only_numbers: bool = False, probability_data=False)\
        -> List[int | float] | dict | tuple:
    """
    Process an Excel file and perform various data processing tasks based on the provided parameters.

    Parameters:
        file_path (str): The file path of the Excel file to be processed.
        row_wanted (int, optional): The index of the specific row to extract data from (default: 0).
        single_row (bool, optional): Specifies whether to extract data from a single row (default: False).
        group_data (bool, optional): Specifies whether to group data by columns (default: False).
        only_numbers (bool, optional): Specifies whether to include only numeric values in the processed data
        (default: False).
        probability_data (bool, optional): Specifies whether to process probability data and return as a dictionary
        (default: False).

    Returns:
        Union[List[Union[int, float]], dict, tuple]:
            - If probability_data is True: Returns a tuple containing a dictionary (data_processed), a list of variables
             (variables),
              and a list of probabilities (probabilities).
            - If group_data is True: Returns a dictionary (data_processed) where the keys are column names and the
            values are lists of
              corresponding column values.
            - If single_row is True: Returns a sorted list (data_processed) containing values from the specified row.
            - If only_numbers is True: Returns a list (data_processed) containing only the numeric values from the Excel
             file.

    """
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    data = list(ws.iter_rows(values_only=True))
    if probability_data:
        data_processed = {}
        variables, probabilities = [], []
        for row in data:
            for index, item in enumerate(row):
                if not(type(item) is int or type(item) is float):
                    break
                elif (type(item) is int or type(item) is float) and (row[index] == row[-1]):
                    variable, probability = row
                    data_processed[variable] = probability
                    variables.append(variable)
                    probabilities.append(probability)
        return data_processed, variables, probabilities
    if group_data:
        data_processed = {}
        for index, row in enumerate(data):
            if index == 0:
                for col in row:
                    data_processed[col] = []
            for i, col_val in enumerate(row):
                data_processed[data[i]].append(col_val)
        wb.close()
        return data_processed
    if single_row:
        data_processed = []
        for row in data:
            if type(row[row_wanted]) == float or type(row[row_wanted]) == int:
                data_processed.append(row[row_wanted])
        data_processed.sort()
        wb.close()
        return data_processed
    if only_numbers:
        data_processed = []
        for row in data:
            for i in row:
                if type(i) is int:
                    data_processed.append(i)
        wb.close()
        return data_processed


def stem_plot(data: list | tuple):
    """
        Display a stem plot of the given data.

        Parameters:
            data (list or tuple): The data to be displayed in the stem plot.

        Returns:
            None (prints the stem plot)

        Example:
            >>> stem_plot([14, 27, 38, 45, 56, 69, 71, 84, 97])
            1 | 4
            2 | 7
            3 | 8
            4 | 5
            5 | 6
            6 | 9
            7 | 1
            8 | 4
            9 | 7
        """
    data.sort()
    current_num = data[0] // 10
    print(f'{current_num} | ', end="")
    for num in data:
        if num // 10 != current_num:
            current_num = num // 10
            to_print = num - (10 * current_num)
            print(f"\n{current_num} | {to_print}", end="")
        else:
            to_print = num - (10 * current_num)
            print(f'{to_print}', end="")


def get_median(data: list | tuple | set, give_average: bool = False):
    """
    Calculate the median of the given data.

    Parameters:
        data (list, tuple, or set): The data from which to calculate the median.
        give_average (bool, optional): Specifies whether to return the average of the middle two values for even-sized data
            (default: False).

    Returns:
        float or list: The median value(s) of the data.
            - If the data has an odd number of elements, the function returns a single float representing the median.
            - If the data has an even number of elements and give_average is False, the function returns a list containing
              the two middle values.
            - If the data has an even number of elements and give_average is True, the function returns the average of the
              two middle values as a float.

    Example:
        >>> get_median([3, 1, 7, 2, 5])
        3
        >>> get_median([3, 1, 7, 2, 5, 4])
        [3, 4]
        >>> get_median([3, 1, 7, 2, 5, 4], give_average=True)
        3.5
    """
    data_len = len(data)
    data.sort()
    if data_len % 2 == 1:
        return data[data_len//2]
    else:
        if give_average:
            return (data[data_len//2-1] + data[data_len//2]) / 2
        else:
            return data[data_len//2-1: data_len//2+1]


def weighted_mean(data: list | tuple | set, weight: dict):
    """
    Calculate the weighted mean of the given data using the provided weights.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the weighted mean.
        weight (dict): A dictionary mapping values in the data to their respective weights.

    Returns:
        float: The weighted mean of the data.

    Example:
        >>> data_ = [('A', 5), ('B', 7), ('C', 4)]
        >>> weight_ = {'A': 0.3, 'B': 0.5, 'C': 0.2}
        >>> weighted_mean(data, weight)
        5.5
    """
    numerator = 0
    denominator = 0
    for row in data:
        unweighted_value = row[1]
        value_weight = weight[row[0]]
        numerator += unweighted_value * value_weight
        denominator += unweighted_value
    return numerator / denominator


def get_mode(data: list | tuple | set):
    """
    Calculate the mode(s) of the given data.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the mode(s).

    Returns:
        list: A list containing the mode(s) of the data.

    Example:
        >>> get_mode([1, 2, 3, 2, 4, 3, 5, 3])
        [2, 3]
        >>> get_mode(['apple', 'banana', 'apple', 'orange', 'banana'])
        ['apple', 'banana']
    """
    nums_mapped = {}
    for num in data:
        if num in nums_mapped:
            nums_mapped[num] += 1
        else:
            nums_mapped[num] = 1
    holding_answer = []
    largest_value = 0
    for num, times_expressed in nums_mapped.items():
        if times_expressed == 1:
            continue
        elif times_expressed > largest_value:
            largest_value = times_expressed
            holding_answer = [num]
        elif times_expressed == largest_value:
            largest_value = times_expressed
            holding_answer.append(num)
        else:
            continue
    return holding_answer


def get_mid_range(data: list | tuple | set):
    """
    Calculate the mid-range of the given data.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the mid-range.

    Returns:
        float: The mid-range of the data.

    Example:
        >>> get_mid_range([3, 1, 7, 2, 5])
        4.0
        >>> get_mid_range([-10, 0, 10])
        0.0
    """
    smallest_num = min(data)
    largest_num = max(data)
    return (largest_num + smallest_num) / 2


def get_range(data: list | tuple | set):
    """
    Calculate the range of the given data.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the range.

    Returns:
        int or float: The range of the data.

    Example:
        >>> get_range([3, 1, 7, 2, 5])
        6
        >>> get_range([-10, 0, 10])
        20
    """
    return max(data) - min(data)


def get_stadev(data: list | tuple | set):
    """
    Calculate the standard deviation of the given data.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the standard deviation.

    Returns:
        float: The standard deviation of the data.
    """
    divisor = len(data) - 1
    numerator = 0
    data_mean = round(mean(data), 1)
    for num in data:
        numerator += (num - data_mean) ** 2
    return (numerator / divisor) ** 0.5


def get_variance(data: list | tuple):
    """
    Calculate the variance of the given data.

    Parameters:
        data (list or tuple): The data for which to calculate the variance.

    Returns:
        float: The variance of the data.

    Example:
        >>> get_variance([1, 2, 3, 4, 5])
        2.5
        >>> get_variance([10, 20, 30, 40, 50])
        250.0
    """
    return stdev(data) ** 2


def significant_values_analysis(data: list | tuple | set):
    """
    Perform significant values analysis on the given data.

    Parameters:
        data (list, tuple, or set): The data for which to perform the analysis.

    Returns:
        tuple: A tuple containing three lists: low_values, neither_values, and high_values.

    Example:
        >>> significant_values_analysis([1, 2, 3, 4, 5, 10, 20, 30, 40, 50])
        ([1, 2], [3, 4, 5, 10, 20, 30], [40, 50])
        >>> significant_values_analysis([-10, 0, 5, 10, 15])
        ([-10, 0], [5, 10, 15], [])
    """
    data_mean = mean(data)
    data_stadev = stdev(data)
    sig_low = data_mean - (data_stadev * 2)
    sig_high = data_mean + (data_stadev * 2)
    low_values, high_values, neither_values = [], [], []

    for num in data:
        if num <= sig_low:
            low_values.append(num)
        elif num >= sig_high:
            high_values.append(num)
        else:
            neither_values.append(num)
    return low_values, neither_values, high_values


def mean_abs_dev(data: list | tuple | set):
    """
    Calculate the mean absolute deviation of the given data.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the mean absolute deviation.

    Returns:
        float: The mean absolute deviation of the data.

    Example:
        >>> mean_abs_dev([1, 2, 3, 4, 5])
        1.2
        >>> mean_abs_dev([-10, 0, 10])
        6.666666666666667
    """
    data_mean = mean(data)
    data_len = len(data)
    numerator = 0
    denominator = data_len
    for num in data:
        numerator += abs(num - data_mean)
    return numerator / denominator


def z_score(data: list | tuple | set, num: int):
    """
    Calculate the z-score of a given number in relation to the data.

    Parameters:
        data (list, tuple, or set): The data used to calculate the z-score.
        num (int): The number for which to calculate the z-score.

    Returns:
        float: The z-score of the number in relation to the data.

    Example:
        >>> z_score([1, 2, 3, 4, 5], 3)
        0.0
        >>> z_score([10, 20, 30, 40, 50], 35)
        0.7071067811865476
    """
    data_mean = mean(data)
    data_stadev = stdev(data)
    return (num - data_mean) / data_stadev


def percentile_value(data: list | tuple | set, num: int):
    """
    Calculate the percentile value of a given number in relation to the data.

    Parameters:
        data (list, tuple, or set): The data used to calculate the percentile value.
        num (int): The number for which to calculate the percentile value.

    Returns:
        float: The percentile value of the number in relation to the data.

    Example:
        >>> percentile_value([1, 2, 3, 4, 5], 3)
        60.0
        >>> percentile_value([10, 20, 30, 40, 50], 35)
        80.0
    """
    data.sort()
    numerator = 0
    for value in data:
        if value > num:
            numerator += 1
        else:
            break
    return (numerator / len(data)) * 100


def five_num_summary(data: list | tuple | set):
    """
    Calculate the five-number summary of the given data.

    Parameters:
        data (list, tuple, or set): The data for which to calculate the five-number summary.

    Returns:
        list: The five-number summary of the data, containing the minimum, first quartile (Q1),
              median (Q2), third quartile (Q3), and maximum.

    Example:
        >>> five_num_summary([1, 2, 3, 4, 5])
        [1, 2.5, 3, 4.5, 5]
        >>> five_num_summary([10, 20, 30, 40, 50])
        [10, 25.0, 30, 45.0, 50]
    """
    data.sort()
    values_returned = []
    values_returned.append(data[0])
    values_returned.append(get_median(data[0:len(data)//2], True))
    values_returned.append(get_median(data, True))
    values_returned.append(get_median(data[len(data)//2:], True))
    values_returned.append(data[-1])
    return values_returned


def permutation(n: int, r: int):
    """
    Calculate the number of permutations of selecting r items from a set of n items.

    Parameters:
        n (int): The total number of items in the set.
        r (int): The number of items to be selected.

    Returns:
        int: The number of permutations.

    Example:
        >>> permutation(5, 3)
        60
        >>> permutation(10, 2)
        90
    """
    numerator = factorial(n)
    denominator = factorial(n-r)
    return numerator / denominator


def combination(n: int, r: int):
    """
    Calculate the number of combinations of selecting r items from a set of n items.

    Parameters:
        n (int): The total number of items in the set.
        r (int): The number of items to be selected.

    Returns:
        int: The number of combinations.

    Example:
        >>> combination(5, 3)
        10
        >>> combination(10, 2)
        45
    """
    numerator = factorial(n)
    denominator = factorial(r) * factorial(n-r)
    return numerator / denominator


def float_to_fraction(decimal_):
    """
    Convert a decimal number to a fraction in the form of numerator / denominator.

    Parameters:
        decimal_ (float): The decimal number to be converted.

    Returns:
        str: The fraction representation of the decimal number.

    Example:
        >>> float_to_fraction(0.5)
        '1 / 2'
        >>> float_to_fraction(0.75)
        '3 / 4'
    """
    index = 1
    while decimal_ * index != round(decimal_ * index):
        index += 1
    numerator = round(decimal_ * index)
    denominator = index
    return f'{numerator} / {denominator}'


def prob_dis_mean(data):
    """
    Calculate the mean of a probability distribution.

    Parameters:
        data (dict or list): The probability distribution represented as a dictionary
                             or a list of value-probability pairs.

    Returns:
        float: The mean of the probability distribution.

    Example:
        >>> prob_dis_mean({1: 0.3, 2: 0.5, 3: 0.2})
        1.9
        >>> prob_dis_mean([(1, 0.3), (2, 0.5), (3, 0.2)])
        1.9
    """
    if type(data) is dict:
        values_processed = [x_val * x_prob for x_val, x_prob in data.items()]
    else:
        values_processed = [x_val * x_prob for x_val, x_prob in data]
    return sum(values_processed)


def prob_distribution(data):
    """
    Calculate the standard deviation of a probability distribution.

    Parameters:
        data (dict or list): The probability distribution represented as a dictionary
                             or a list of value-probability pairs.

    Returns:
        float: The standard deviation of the probability distribution.

    Example:
        >>> prob_distribution({1: 0.3, 2: 0.5, 3: 0.2})
        0.7483314773547883
        >>> prob_distribution([(1, 0.3), (2, 0.5), (3, 0.2)])
        0.7483314773547883
    """
    if type(data) is dict:
        values_processed = [x_val ** 2 * x_prob for x_val, x_prob in data.items()]
    else:
        values_processed = [x_val ** 2 * x_prob for x_val, x_prob in data]
    return (sum(values_processed) - prob_dis_mean(data) ** 2) ** 0.5


def prob_variance(data):
    """
    Calculate the variance of a probability distribution.

    Parameters:
        data (dict or list): The probability distribution represented as a dictionary
                             or a list of value-probability pairs.

    Returns:
        float: The variance of the probability distribution.

    Example:
        >>> prob_variance({1: 0.3, 2: 0.5, 3: 0.2})
        0.4433333333333334
        >>> prob_variance([(1, 0.3), (2, 0.5), (3, 0.2)])
        0.4433333333333334
    """
    return prob_distribution(data) ** 2


def binom_prob(n, x, p, or_less: bool = False, or_more: bool = False):
    """
    Calculate the probability of a binomial distribution.

    Parameters:
        n (int): The number of trials.
        x (int): The number of successful outcomes.
        p (float): The probability of success in a single trial.
        or_less (bool): If True, calculate the probability of "x or less" successful outcomes.
        or_more (bool): If True, calculate the probability of "x or more" successful outcomes.

    Returns:
        float: The probability of the specified binomial event.

    Example:
        >>> binom_prob(5, 3, 0.4)
        0.34559999999999994
        >>> binom_prob(5, 3, 0.4, or_less=True)
        0.9104
        >>> binom_prob(5, 3, 0.4, or_more=True)
        0.34559999999999994
    """
    if or_more:
        ans = 0
        for i in range(x, n + 1):
            first_value = factorial(n) / (factorial(n - i) * factorial(i))
            second_value = p ** i
            third_value = (1 - p) ** (n - i)
            ans += first_value * second_value * third_value
        return ans
    elif or_less:
        ans = 0
        for i in range(0, x + 1):
            first_value = factorial(n) / (factorial(n - i) * factorial(i))
            second_value = p ** i
            third_value = (1 - p) ** (n - i)
            ans += first_value * second_value * third_value
        return ans
    else:
        first_value = factorial(n) / (factorial(n - x) * factorial(x))
        second_value = p ** x
        third_value = (1 - p) ** (n - x)
        return first_value * second_value * third_value


def area_of_norm_dis(z, right_cumulative=False):
    """
    Calculate the area under the standard normal distribution curve.

    Parameters:
        z (float): The z-score.
        right_cumulative (bool): If True, calculate the area to the right of z.

    Returns:
        float: The area under the standard normal distribution curve.

    Example:
        >>> area_of_norm_dis(1.5)
        0.9331927987311419
        >>> area_of_norm_dis(1.5, right_cumulative=True)
        0.06680720126885809
    """
    if not right_cumulative:
        return 0.5 * (1 + erf(z / 2 ** 0.5))
    else:
        return 1 - (0.5 * (1 + erf(z / 2 ** 0.5)))


def area_of_norm_dis_range(z_1, z_2):
    """
    Calculate the area under the standard normal distribution curve between two z-scores.

    Parameters:
        z_1 (float): The lower z-score.
        z_2 (float): The upper z-score.

    Returns:
        float: The area under the standard normal distribution curve between z_1 and z_2.

    Example:
        >>> area_of_norm_dis_range(-1, 1)
        0.682689492137086
        >>> area_of_norm_dis_range(1, -1)
        0.682689492137086
    """
    if z_1 > z_2:
        return area_of_norm_dis(z_1) - area_of_norm_dis(z_2)
    else:
        return area_of_norm_dis(z_2) - area_of_norm_dis(z_1)


def norm_dis_eq(z):
    """
    Calculate the value of the standard normal distribution at a given z-score.

    Parameters:
        z (float): The z-score.

    Returns:
        float: The value of the standard normal distribution at the given z-score.

    Example:
        >>> norm_dis_eq(0)
        0.3989422804014327
        >>> norm_dis_eq(1)
        0.24197072451914337
    """
    return (e ** (-0.5 * z ** 2)) / ((2 * pi) ** 0.5)


def calculate_z_score_of_norm_dis(probability):
    """
    Calculate the z-score corresponding to a given probability in the standard normal distribution.

    Parameters:
        probability (float): The probability.

    Returns:
        float: The z-score corresponding to the given probability.

    Example:
        >>> calculate_z_score_of_norm_dis(0.5)
        0.0
        >>> calculate_z_score_of_norm_dis(0.95)
        1.959963984540054
    """
    z = (2 ** 0.5) * erfinv(2 * probability - 1)
    return z


def z_score_eq(x, mean_, deviation):
    """
    Calculate the z-score for a given value in a normal distribution.

    Parameters:
        x (float): The value.
        mean_ (float): The mean of the distribution.
        deviation (float): The standard deviation of the distribution.

    Returns:
        float: The z-score.

    Example:
        >>> z_score_eq(75, 70, 5)
        1.0
        >>> z_score_eq(80, 70, 5)
        2.0
    """
    return (x - mean_) / deviation


def z_score_to_x(z, mean_, deviation):
    """
    Convert a z-score to the corresponding value in a normal distribution.

    Parameters:
        z (float): The z-score.
        mean_ (float): The mean of the distribution.
        deviation (float): The standard deviation of the distribution.

    Returns:
        float: The corresponding value.

    Example:
        >>> z_score_to_x(1.0, 70, 5)
        75.0
        >>> z_score_to_x(2.0, 70, 5)
        80.0
    """
    return mean_ + (z * deviation)


def central_limit_prob(x, n, mean_, deviation, right_cumulative=False):
    """
    Calculate the probability of a value in a sample mean distribution using the central limit theorem.

    Parameters:
        x (float): The value for which to calculate the probability.
        n (int): The sample size.
        mean_ (float): The mean of the population.
        deviation (float): The standard deviation of the population.
        right_cumulative (bool): Whether to calculate the right cumulative probability. Defaults to False.

    Returns:
        float: The probability of the value.

    Example:
        >>> central_limit_prob(75, 100, 70, 5)
        0.841344746068543
        >>> central_limit_prob(80, 100, 70, 5, right_cumulative=True)
        0.15865525393145707
    """
    z = (x - mean_) / (deviation / (n ** 0.5))
    return area_of_norm_dis(z, right_cumulative=right_cumulative)


def central_limit_prob_range(x_1, x_2, n, mean_, deviation):
    """
    Calculate the probability of a range of values in a sample mean distribution using the central limit theorem.

    Parameters:
        x_1 (float): The starting value of the range.
        x_2 (float): The ending value of the range.
        n (int): The sample size.
        mean_ (float): The mean of the population.
        deviation (float): The standard deviation of the population.

    Returns:
        float: The probability of the range of values.

    Example:
        >>> central_limit_prob_range(70, 75, 100, 70, 5)
        0.3413447460685429
    """
    if x_1 > x_2:
        return central_limit_prob(x_1, n, mean_, deviation) - central_limit_prob(x_2, n, mean_, deviation)
    else:
        return central_limit_prob(x_2, n, mean_, deviation) - central_limit_prob(x_1, n, mean_, deviation)


def approx_binom_dis_prob(x, n, p, left_cumulative=None, right_cumulative=None):
    """
    Approximate the probability of a binomial distribution using the normal distribution.

    Parameters:
        x (int): The number of successes.
        n (int): The number of trials.
        p (float): The probability of success.
        left_cumulative (bool, optional): Calculate the left cumulative probability. Defaults to None.
        right_cumulative (bool, optional): Calculate the right cumulative probability. Defaults to None.

    Returns:
        float: The approximate probability.

    Example:
        >>> approx_binom_dis_prob(3, 10, 0.5, left_cumulative=True)
        0.171875
    """
    if ((n * p) < 5) or n * ((n * (1 - p)) < 5):
        return -1
    mean_ = n * p
    dev = (n * p * (1 - p)) ** 0.5
    if left_cumulative:
        x += 0.5
        z = (x - mean_) / dev
        return area_of_norm_dis(z)
    elif right_cumulative:
        x -= 0.5
        z = (x - mean_) / dev
        return area_of_norm_dis(z, right_cumulative=True)
    else:
        z_1 = ((x + 0.5) - mean_) / dev
        z_2 = ((x - 0.5) - mean_) / dev
        return area_of_norm_dis_range(z_1, z_2)


def critical_value(confidence_level):
    """
    Calculates the critical value for a given confidence level in a two-tailed test.

    Args:
    - confidence_level: The desired level of confidence (between 0 and 1).

    Returns:
    - critical_value: The critical value associated with the confidence level.
    """
    alpha = 1 - ((1 - confidence_level) / 2)
    return calculate_z_score_of_norm_dis(alpha)


def margin_of_error(confidence_level, x, n):
    """
    Calculates the margin of error and the confidence interval for a given confidence level.

    Args:
    - confidence_level: The desired level of confidence (between 0 and 1).
    - x: The number of successes or events of interest.
    - n: The total sample size.

    Returns:
    - lower_bound: The lower bound of the confidence interval.
    - upper_bound: The upper bound of the confidence interval.
    """
    p = x / n
    q = 1 - p
    E = critical_value(confidence_level) * (((p * q) / n)**0.5)
    return p-E, p+E


def n_with_proportion(confidence_level, p, E):
    """
    Calculates the required sample size for estimating a proportion with a given margin of error and confidence level.

    Args:
    - confidence_level: The desired level of confidence (between 0 and 1).
    - p: The estimated proportion.
    - E: The desired margin of error.

    Returns:
    - n: The required sample size.
    """
    numerator = (critical_value(confidence_level) ** 2) * (p * (1 - p))
    denominator = E ** 2
    return numerator / denominator


def e_for_margin_error(confidence_level, x, n):
    p = x / n
    q = 1 - p
    return critical_value(confidence_level) * (((p * q) / n)**0.5)


def find_t_distribution(n, confidence_level):
    """
    Finds the critical value for the Student's t-distribution.

    Args:
    - n: Sample size.
    - confidence_level: Confidence level (between 0 and 1).

    Returns:
    - critical_value: The critical value for the Student's t-distribution.
    """
    significance = 1 - confidence_level
    critical_value_ = t.ppf(1 - significance/2, n - 1)
    return critical_value_


def e_mar_err_with_t(confidence_level, s, n):
    """
    Calculates the margin of error (E) for estimating a proportion with a given confidence level.

    Args:
    - confidence_level: The desired level of confidence (between 0 and 1).
    - x: The number of successes or events of interest.
    - n: The total sample size.

    Returns:
    - E: The margin of error.
    """
    return find_t_distribution(n, confidence_level) * (s / n**0.5)


def mar_err_with_t(confidence_level, s, n, mean_):
    """
    Calculates the confidence interval bounds based on the mean and margin of error (E) using the t-distribution.

    Args:
    - confidence_level: The desired level of confidence (between 0 and 1).
    - s: The sample standard deviation.
    - n: The sample size.
    - mean_: The sample mean.

    Returns:
    - lower_bound: The lower bound of the confidence interval.
    - upper_bound: The upper bound of the confidence interval.
    """
    E = e_mar_err_with_t(confidence_level, s, n)
    return mean_ - E, mean_ + E


def sample_size_estimated_mean(confidence_level, s, E):
    """
    Calculates the required sample size for estimating a mean with a given margin of error and confidence level.

    Args:
    - confidence_level: The desired level of confidence (between 0 and 1).
    - s: The sample standard deviation.
    - E: The desired margin of error.

    Returns:
    - n: The required sample size.
    """
    numerator = critical_value(confidence_level) * s
    denominator = E
    return (numerator / denominator) ** 2


def t_statistic_two_means(sample_mean1, sample_std1, sample_size1, sample_mean2, sample_std2, sample_size2,
                          equal_var=False):
    """
    Finds the test statistic t for comparing two means in independent samples without the population mean.

    Args:
    - sample_mean1: Sample mean of the first sample.
    - sample_std1: Sample standard deviation of the first sample.
    - sample_size1: Sample size of the first sample.
    - sample_mean2: Sample mean of the second sample.
    - sample_std2: Sample standard deviation of the second sample.
    - sample_size2: Sample size of the second sample.
    - equal_var: Boolean indicating whether to assume equal variances (default: True).

    Returns:
    - t_statistic: The test statistic t.
    """
    if equal_var:
        pooled_std = math.sqrt(((sample_size1 - 1) * sample_std1 ** 2 + (sample_size2 - 1) * sample_std2 ** 2) /
                               (sample_size1 + sample_size2 - 2))
        t_statistic = (sample_mean1 - sample_mean2) / (pooled_std * math.sqrt(1 / sample_size1 + 1 / sample_size2))
    else:
        t_statistic = (sample_mean1 - sample_mean2) / math.sqrt(sample_std1 ** 2 / sample_size1 + sample_std2 ** 2 /
                                                                sample_size2)

    return t_statistic


def p_value_two_means(t_statistic, df, alternative='two-sided'):
    """
    Finds the p-value for comparing two means in independent samples.

    Args:
    - t_statistic: The test statistic t.
    - df: Degrees of freedom.
    - alternative: The alternative hypothesis type (default: 'two-sided').
                   Options: 'two-sided', 'less', 'greater'.

    Returns:
    - p_value: The p-value for the two-sample means test.
    """
    if alternative == 'two-sided':
        p_value = 2 * (1 - t.cdf(abs(t_statistic), df))
    elif alternative == 'less':
        p_value = t.cdf(t_statistic, df)
    elif alternative == 'greater':
        p_value = 1 - t.cdf(t_statistic, df)
    else:
        raise ValueError("Invalid alternative hypothesis type.")
    return p_value


def e_value_two_means(sample_std1, sample_size1, sample_std2, sample_size2, confidence_level):
    """
    Finds the margin of error (E) for comparing two means in independent samples.

    Args:
    - sample_std1: Sample standard deviation of the first sample.
    - sample_size1: Sample size of the first sample.
    - sample_std2: Sample standard deviation of the second sample.
    - sample_size2: Sample size of the second sample.
    - confidence_level: The desired level of confidence (between 0 and 1).

    Returns:
    - margin_of_error: The margin of error (E).
    """
    z = abs(norm.ppf((1 - confidence_level) / 2))  # For a two-tailed test
    margin_of_error_ = z * math.sqrt((sample_std1 ** 2 / sample_size1) + (sample_std2 ** 2 / sample_size2))

    return margin_of_error_


def mar_err_two_means(mean1, mean2, E):
    """
    Calculates the confidence interval bounds based on the difference between two means and the margin of error (E).

    Args:
    - mean1: The first mean.
    - mean2: The second mean.
    - E: The margin of error.

    Returns:
    - lower_bound: The lower bound of the confidence interval.
    - upper_bound: The upper bound of the confidence interval.
    """
    means_sub = mean1 - mean2
    return means_sub - E, means_sub + E
