def predict_salary(salary_from, salary_to):
    salary_interval = (salary_from, salary_to)

    if all(salary_interval):
        average_salary = sum(salary_interval) / 2
    elif salary_interval[0]:
        average_salary = salary_interval[0] * 1.2
    else:
        average_salary = salary_interval[1] * 0.8
    return int(average_salary)
