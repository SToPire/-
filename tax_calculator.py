# 月基础工资
base = 30000
# 月社保基数
insurance_base = base
# 年终奖
bonus = 120000
# 公积金个人缴存比例
housing_ratio = 0.12

# 个税起征点（月）
tax_threshold = 5000
# 个税税率
tax_rate = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]
# 个税速算扣除数
tax_quick_deduction = [0, 2520, 16920, 31920, 52920, 85920, 181920]
# 个税档位
tax_level = [0, 36000, 144000, 300000, 420000, 660000, 960000]

# 年终奖税率
bonus_rate = [0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45]
# 年终奖速算扣除数
bonus_quick_deduction = [0, 210, 1410, 2660, 4410, 7160, 15160]
# 年终奖档位
bonus_level = [0, 3000, 12000, 25000, 35000, 55000, 80000]

# 社保基数上限
insurance_upper = 36921
# 社保基数下限
insurance_lower = 7384

def calc_monthly_salary(base, salary_m_after_tax, insurance, housing):
    sum = 0
    tax = 0

    for i in range(1, 13):
        new_sum = sum + salary_m_after_tax
        new_tax = tax
        for j in range(len(tax_level)):
            if new_sum > tax_level[j] and (j == len(tax_level) - 1 or new_sum <= tax_level[j + 1]):
                new_tax = new_sum * tax_rate[j] - tax_quick_deduction[j]
                break

        salary_m = base - insurance - housing - (new_tax - tax)
        print('{:02}月：{:.2f}（税前） - {:.2f}（社保） - {:.2f}（公积金） - {:.2f}（个税） = {:.2f}'.format(i, base, insurance, housing, new_tax - tax, salary_m))

        tax = new_tax
        sum = new_sum


if __name__ == '__main__':
    # 月社保基数
    insurance_base = insurance_base if insurance_base < insurance_upper else insurance_upper
    insurance_base = insurance_base if insurance_base > insurance_lower else insurance_lower

    # 养老保险
    pension = insurance_base * 0.08
    # 医疗保险
    health = insurance_base * 0.02
    # 失业保险
    unemployment = insurance_base * 0.005
    # 工伤保险
    injury = insurance_base * 0
    # 生育保险
    birth = insurance_base * 0
    # 社保总额
    insurance = pension + health + unemployment + injury + birth
    # 个人公积金
    housing = insurance_base * housing_ratio

    # 月应税工资
    tax_salary_m = max(0, base - insurance - housing - tax_threshold)
    # 年应税工资
    tax_salary_y = tax_salary_m * 12

    tax = 0
    bonus_tax = 0

    for i in range(len(tax_level)):
        if tax_salary_y > tax_level[i] and (i == len(tax_level) - 1 or tax_salary_y <= tax_level[i + 1]):
            tax = tax_salary_y * tax_rate[i] - tax_quick_deduction[i]
            break

    for i in range(len(bonus_level)):
        if (bonus / 12) > bonus_level[i] and (i == len(bonus_level) - 1 or (bonus / 12) <= bonus_level[i + 1]):
            bonus_tax = bonus * bonus_rate[i] - bonus_quick_deduction[i]
            break

    # 税前工资
    salary_y = base * 12 + bonus
    # 税后工资
    salary_y_after_tax = salary_y - tax - bonus_tax - insurance * 12 - housing * 12
    # 税后工资（含公积金）
    salary_y_after_tax_housing = salary_y_after_tax + housing * 12 * 2

    print('税前工资：{:.2f} * 12 + {:.2f} = {:.2f}'.format(base, bonus, salary_y))
    print('个税：{:.2f}（基础）+ {:.2f}（年终） = {:.2f}'.format(tax, bonus_tax, tax + bonus_tax))
    print('税后工资：{:.2f} - {:.2f}（总个税） - {:.2f}（总社保） - {:.2f}（总个人公积金） = {:.2f}'.format(salary_y, tax + bonus_tax, insurance * 12, housing * 12, salary_y_after_tax))
    print('双边公积金：{:.2f} * 12 * 2 = {:.2f}'.format(housing, housing * 12 * 2))
    print('税后工资（含公积金）：{:.2f} + {:.2f} = {:.2f}'.format(salary_y_after_tax, housing * 12 * 2, salary_y_after_tax + housing * 12 * 2))

    calc_monthly_salary(base, tax_salary_m, insurance, housing)
