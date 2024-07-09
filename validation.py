import re

# Validar o CPF
def is_valid_cpf(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # 1º dígito verificador
    sum = 0
    for i in range(9):
        sum += int(cpf[i]) * (10 - i)
    check_digit1 = 11 - (sum % 11)
    if check_digit1 >= 10:
        check_digit1 = 0

    # 2º dígito verificador
    sum = 0
    for i in range(10):
        sum += int(cpf[i]) * (11 - i)
    check_digit2 = 11 - (sum % 11)
    if check_digit2 >= 10:
        check_digit2 = 0

    return cpf[-2:] == f"{check_digit1}{check_digit2}"

# Validar o CNPJ
def is_valid_cnpj(cnpj):
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    # 1º dígito verificador
    sum = 0
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        sum += int(cnpj[i]) * weights1[i]
    check_digit1 = 11 - (sum % 11)
    if check_digit1 >= 10:
        check_digit1 = 0

    # 2º dígito verificador
    sum = 0
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        sum += int(cnpj[i]) * weights2[i]
    check_digit2 = 11 - (sum % 11)
    if check_digit2 >= 10:
        check_digit2 = 0

    return cnpj[-2:] == f"{check_digit1}{check_digit2}"

# Verificar se o CPF/CNPJ é válido
def is_valid_cpf_cnpj(value):
    clean_value = re.sub(r'\D', '', value)
    if len(clean_value) == 11:
        if is_valid_cpf(clean_value):
            return clean_value
        else:
            return "CPF inválido: Falha na verificação dos dígitos."
    elif len(clean_value) == 14:
        if is_valid_cnpj(clean_value):
            return clean_value
        else:
            return "CNPJ inválido: Falha na verificação dos dígitos."
    return "CPF/CNPJ inválido: Número incorreto de dígitos."
