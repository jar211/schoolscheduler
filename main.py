# semester [1,2]
# period [A1, A2, A3, A4, B5, B6, B7, B8]
# course category [english, math, science, language, history, seminary, arts]
# course category class
# preference order
# 1A1, 1A2, 1A3, 1A4, 1B5, 1B6, 1B7, 1B8
# class-assignment - person + class + semester-period

# set up empty class assignment
# set classes that can't be moved
import csv
import itertools
import logging


class Course(object):
    def __init__(self, category, course, instructor, period, preference, seats, state):
        self.category = category
        self.course = course
        self.instructor = instructor
        self.period = period
        self.preference = int(preference)
        self.seats = seats
        self.state = state

    def __str__(self):
        return self.category + ":" + self.course + ":" + self.instructor + \
               ":" + self.period + ":" + str(self.preference) + ":" + str(self.seats)


def load_courses() -> list:
    courses = list()
    with open('./data/courses.csv', newline='') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            courses.append(Course(row["category"], row["course"], row["instructor"]
                                  , row["period"], row["preference"], row["seats"], row["state"]))
    return courses


def split_courses_by_period(courses: list):
    a1, a2, a3, a4, b5, b6, b7, b8 = list(), list(), list(), list(), list(), list(), list(), list()
    for course in courses:
        if course.period == "a1":
            a1.append(course)
        elif course.period == "a2":
            a2.append(course)
        elif course.period == "a3":
            a3.append(course)
        elif course.period == "a4":
            a4.append(course)
        elif course.period == "b5":
            b5.append(course)
        elif course.period == "b6":
            b6.append(course)
        elif course.period == "b7":
            b7.append(course)
        elif course.period == "b8":
            b8.append(course)
    return a1, a2, a3, a4, b5, b6, b7, b8


def generate_combinations(a1: list, a2: list, a3: list, a4: list
                          , b5: list, b6: list, b7: list, b8: list, clean_list=True) -> list:
    # clean up combos based on "state" -
    # remove courses that can't be booked, remove courses from a period where a course has been registered
    if clean_list:
        a1 = clean_period_list(a1)
        a2 = clean_period_list(a2)
        a3 = clean_period_list(a3)
        a4 = clean_period_list(a4)
        b5 = clean_period_list(b5)
        b6 = clean_period_list(b6)
        b7 = clean_period_list(b7)
        b8 = clean_period_list(b8)
    combos = itertools.product(a1, a2, a3, a4, b5, b6, b7, b8)
    combinations = list(combos)
    logging.info("generate_combinations: Combinations generated: %s", len(combinations))
    return combinations


def clean_period_list(courses: list) -> list:
    clean_list = list()
    for course in courses:
        # ignore courses that are anything but "registered" or "open"
        if course.state == "registered":
            clean_list = list()  # blank out the list
            clean_list.append(course)
            return clean_list
        elif course.state == "open":
            clean_list.append(course)
    return clean_list


def get_valid_combinations(combinations: list) -> list:
    valid_combinations = list()
    for combo in combinations:
        if is_valid_combo(combo):
            valid_combinations.append(combo)
    logging.info("get_valid_combinations: Found valid combinations: %s", len(valid_combinations))
    return valid_combinations


def is_valid_combo(combination: list) -> bool:
    is_valid = True
    categories_found = list()
    for course in combination:
        categories_found.append(course.category)
    if len(set(categories_found)) != 8:
        is_valid = False
        return is_valid
    return is_valid


def rank_combinations(combinations: list) -> list:
    ranked_combinations = list()
    for combo in combinations:
        preference_rating = 0
        for course in combo:
            preference_rating = preference_rating + course.preference
        t = list(combo)
        t.append(preference_rating)
        combo = tuple(t)
        ranked_combinations.append(combo)
        ranked_combinations = sorted(ranked_combinations, key=lambda combo_line: combo_line[8], reverse=True)
    return ranked_combinations


def write_combinations(valid_combinations: list):
    with open('./data/combinations.csv', 'w', newline='') as file:
        csv_file = csv.writer(file)
        for combo in valid_combinations:
            csv_file.writerow(combo)


def main():
    courses = load_courses()
    a1, a2, a3, a4, b5, b6, b7, b8 = split_courses_by_period(courses)
    combinations = generate_combinations(a1, a2, a3, a4, b5, b6, b7, b8)
    valid_combinations = get_valid_combinations(combinations)
    ranked_combinations = rank_combinations(valid_combinations)
    write_combinations(ranked_combinations)
    return


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
