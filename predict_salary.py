def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = (salary_from + salary_to) / 2
    elif salary_from:
        average_salary = salary_from * 1.2
    else:
        average_salary = salary_to * 0.8
    return int(average_salary)
