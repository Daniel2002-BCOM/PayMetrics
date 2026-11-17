
def calculate_salary(basic_salary, hra_percent,
                     bonus_percent, deduction_percent):

    hra = basic_salary * hra_percent / 100
    bonus = basic_salary * bonus_percent / 100

    gross_salary = basic_salary + hra + bonus

    deductions = basic_salary * deduction_percent / 100

    net_salary = gross_salary - deductions

    annual_salary = net_salary * 12

    return {
        "Basic Salary": basic_salary,
        "HRA": hra,
        "Bonus": bonus,
        "Gross Salary": gross_salary,
        "Deductions": deductions,
        "Net Salary": net_salary,
        "Annual Salary": annual_salary
    }
if __name__ == "__main__":
    result = calculate_salary(30000, 20, 10, 5)

    print(result)