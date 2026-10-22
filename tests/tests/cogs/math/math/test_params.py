from typing import ClassVar

import pytest


class Params:
    decorators: ClassVar[list] = [
        pytest.param(
            "en",
            "Enter the command and a mathematical operation for me to solve it.",
            "To use: +math (mathematical expression)",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Digite o comando e uma operação matemática para eu resolvê-la.",
            "Para usar: +math (expressão matemática)",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    temp: ClassVar[list] = [
        pytest.param("en", "asdf", marks=pytest.mark.en, id="en"),
        pytest.param("pt_BR", "asdf", marks=pytest.mark.pt_BR, id="pt_BR"),
    ]

    error: ClassVar[list] = [
        pytest.param(
            "en",
            "Unknown symbol or function: `blablabla`.",
            marks=pytest.mark.en,
            id="en",
        ),
        pytest.param(
            "pt_BR",
            "Símbolo ou função desconhecida: `blablabla`.",
            marks=pytest.mark.pt_BR,
            id="pt_BR",
        ),
    ]

    # ---------- Grupos consolidados ----------
    basic_arithmetic: ClassVar[list] = [
        pytest.param("en", "2 + 3", "5", marks=pytest.mark.en, id="en_add"),
        pytest.param("pt_BR", "2 + 3", "5", marks=pytest.mark.pt_BR, id="pt_BR_add"),
        pytest.param("en", "10 - 4", "6", marks=pytest.mark.en, id="en_sub"),
        pytest.param("pt_BR", "10 - 4", "6", marks=pytest.mark.pt_BR, id="pt_BR_sub"),
        pytest.param("en", "5 * 6", "30", marks=pytest.mark.en, id="en_mul"),
        pytest.param("pt_BR", "5 * 6", "30", marks=pytest.mark.pt_BR, id="pt_BR_mul"),
        pytest.param("en", "21 / 7", "3", marks=pytest.mark.en, id="en_div"),
        pytest.param("pt_BR", "21 / 7", "3", marks=pytest.mark.pt_BR, id="pt_BR_div"),
        pytest.param("en", "3 ^ 4", "81", marks=pytest.mark.en, id="en_pow"),
        pytest.param("pt_BR", "3 ^ 4", "81", marks=pytest.mark.pt_BR, id="pt_BR_pow"),
        pytest.param("en", "10 % 3", "1", marks=pytest.mark.en, id="en_mod"),
        pytest.param("pt_BR", "10 % 3", "1", marks=pytest.mark.pt_BR, id="pt_BR_mod"),
    ]

    math_functions: ClassVar[list] = [
        pytest.param("en", "sin(pi / 2)", "1", marks=pytest.mark.en, id="en_sin"),
        pytest.param("pt_BR", "sin(pi / 2)", "1", marks=pytest.mark.pt_BR, id="pt_BR_sin"),
        pytest.param("en", "cos(0)", "1", marks=pytest.mark.en, id="en_cos"),
        pytest.param("pt_BR", "cos(0)", "1", marks=pytest.mark.pt_BR, id="pt_BR_cos"),
        pytest.param("en", "tan(pi / 4)", "1", marks=pytest.mark.en, id="en_tan"),
        pytest.param("pt_BR", "tan(pi / 4)", "1", marks=pytest.mark.pt_BR, id="pt_BR_tan"),
        pytest.param("en", "sqrt(16)", "4", marks=pytest.mark.en, id="en_sqrt"),
        pytest.param("pt_BR", "sqrt(16)", "4", marks=pytest.mark.pt_BR, id="pt_BR_sqrt"),
        pytest.param("en", "log(100)", "4.605170185988092", marks=pytest.mark.en, id="en_log"),
        pytest.param("pt_BR", "log(100)", "4.605170185988092", marks=pytest.mark.pt_BR, id="pt_BR_log"),
        pytest.param("en", "log(1024, 2)", "10", marks=pytest.mark.en, id="en_log_base"),
        pytest.param("pt_BR", "log(1024, 2)", "10", marks=pytest.mark.pt_BR, id="pt_BR_log_base"),
        pytest.param("en", "exp(1)", "2.718281828459045", marks=pytest.mark.en, id="en_exp"),
        pytest.param("pt_BR", "exp(1)", "2.718281828459045", marks=pytest.mark.pt_BR, id="pt_BR_exp"),
        pytest.param("en", "abs(-5)", "5", marks=pytest.mark.en, id="en_abs"),
        pytest.param("pt_BR", "abs(-5)", "5", marks=pytest.mark.pt_BR, id="pt_BR_abs"),
        pytest.param("en", "round(3.14159)", "3", marks=pytest.mark.en, id="en_round"),
        pytest.param("pt_BR", "round(3.14159)", "3", marks=pytest.mark.pt_BR, id="pt_BR_round"),
        pytest.param("en", "floor(3.8)", "3", marks=pytest.mark.en, id="en_floor"),
        pytest.param("pt_BR", "floor(3.8)", "3", marks=pytest.mark.pt_BR, id="pt_BR_floor"),
        pytest.param("en", "ceil(3.2)", "4", marks=pytest.mark.en, id="en_ceil"),
        pytest.param("pt_BR", "ceil(3.2)", "4", marks=pytest.mark.pt_BR, id="pt_BR_ceil"),
    ]

    bignumber: ClassVar[list] = [
        pytest.param("en", "bignumber(0.1) + bignumber(0.2)", "0.3", marks=pytest.mark.en, id="en_big_add"),
        pytest.param("pt_BR", "bignumber(0.1) + bignumber(0.2)", "0.3", marks=pytest.mark.pt_BR, id="pt_BR_big_add"),
        pytest.param(
            "en",
            "bignumber(1) / bignumber(3)",
            "0.3333333333333333333333333333333333333333333333333333333333333333",
            marks=pytest.mark.en,
            id="en_big_div",
        ),
        pytest.param(
            "pt_BR",
            "bignumber(1) / bignumber(3)",
            "0.3333333333333333333333333333333333333333333333333333333333333333",
            marks=pytest.mark.pt_BR,
            id="pt_BR_big_div",
        ),
        pytest.param(
            "en",
            "bignumber(factorial(1234))",
            "5.108498e+3280",
            marks=pytest.mark.en,
            id="en_big_fact",
        ),
        pytest.param(
            "pt_BR",
            "bignumber(factorial(1234))",
            "5.108498e+3280",
            marks=pytest.mark.pt_BR,
            id="pt_BR_big_fact",
        ),
        pytest.param(
            "en",
            "bignumber(2) ^ bignumber(1024)",
            "1.797693e+308",
            marks=pytest.mark.en,
            id="en_big_pow",
        ),
        pytest.param(
            "pt_BR",
            "bignumber(2) ^ bignumber(1024)",
            "1.797693e+308",
            marks=pytest.mark.pt_BR,
            id="pt_BR_big_pow",
        ),
    ]

    stats: ClassVar[list] = [
        pytest.param("en", "sum([1, 2, 3, 4, 5])", "15", marks=pytest.mark.en, id="en_sum"),
        pytest.param("pt_BR", "sum([1, 2, 3, 4, 5])", "15", marks=pytest.mark.pt_BR, id="pt_BR_sum"),
        pytest.param("en", "mean([1, 2, 3, 4, 5])", "3", marks=pytest.mark.en, id="en_mean"),
        pytest.param("pt_BR", "mean([1, 2, 3, 4, 5])", "3", marks=pytest.mark.pt_BR, id="pt_BR_mean"),
        pytest.param("en", "median([3, 7, 1, 9, 2])", "3", marks=pytest.mark.en, id="en_median"),
        pytest.param("pt_BR", "median([3, 7, 1, 9, 2])", "3", marks=pytest.mark.pt_BR, id="pt_BR_median"),
        pytest.param(
            "en",
            "std([10, 12, 23, 23, 16, 23, 21, 16])",
            "5.237229365663817",
            marks=pytest.mark.en,
            id="en_std",
        ),
        pytest.param(
            "pt_BR",
            "std([10, 12, 23, 23, 16, 23, 21, 16])",
            "5.237229365663817",
            marks=pytest.mark.pt_BR,
            id="pt_BR_std",
        ),
        pytest.param(
            "en",
            "variance([10, 12, 23, 23, 16, 23, 21, 16])",
            "27.428571428571427",
            marks=pytest.mark.en,
            id="en_var",
        ),
        pytest.param(
            "pt_BR",
            "variance([10, 12, 23, 23, 16, 23, 21, 16])",
            "27.428571428571427",
            marks=pytest.mark.pt_BR,
            id="pt_BR_var",
        ),
    ]

    matrix: ClassVar[list] = [
        pytest.param("en", "[1, 2, 3] + [4, 5, 6]", "[5, 7, 9]", marks=pytest.mark.en, id="en_mat_add"),
        pytest.param("pt_BR", "[1, 2, 3] + [4, 5, 6]", "[5, 7, 9]", marks=pytest.mark.pt_BR, id="pt_BR_mat_add"),
        pytest.param("en", "[1, 2, 3] * 2", "[2, 4, 6]", marks=pytest.mark.en, id="en_mat_scalar"),
        pytest.param("pt_BR", "[1, 2, 3] * 2", "[2, 4, 6]", marks=pytest.mark.pt_BR, id="pt_BR_mat_scalar"),
        pytest.param("en", "[1, 2, 3, 4] .* [2, 2, 2, 2]", "[2, 4, 6, 8]", marks=pytest.mark.en, id="en_mat_elem"),
        pytest.param(
            "pt_BR", "[1, 2, 3, 4] .* [2, 2, 2, 2]", "[2, 4, 6, 8]", marks=pytest.mark.pt_BR, id="pt_BR_mat_elem"
        ),
        pytest.param("en", "det([1, 2; 3, 4])", "-2", marks=pytest.mark.en, id="en_det"),
        pytest.param("pt_BR", "det([1, 2; 3, 4])", "-2", marks=pytest.mark.pt_BR, id="pt_BR_det"),
        pytest.param(
            "en",
            "[1, 2; 3, 4] * [2, 0; 0, 2]",
            "[[2, 4], [6, 8]]",
            marks=pytest.mark.en,
            id="en_mat_mul",
        ),
        pytest.param(
            "pt_BR",
            "[1, 2; 3, 4] * [2, 0; 0, 2]",
            "[[2, 4], [6, 8]]",
            marks=pytest.mark.pt_BR,
            id="pt_BR_mat_mul",
        ),
        pytest.param(
            "en",
            "[1, 2; 3, 4] ^ 2",
            "[[7, 10], [15, 22]]",
            marks=pytest.mark.en,
            id="en_mat_pow",
        ),
        pytest.param(
            "pt_BR",
            "[1, 2; 3, 4] ^ 2",
            "[[7, 10], [15, 22]]",
            marks=pytest.mark.pt_BR,
            id="pt_BR_mat_pow",
        ),
        pytest.param(
            "en",
            "transpose([1, 2, 3; 4, 5, 6])",
            "[[1, 4], [2, 5], [3, 6]]",
            marks=pytest.mark.en,
            id="en_transpose",
        ),
        pytest.param(
            "pt_BR",
            "transpose([1, 2, 3; 4, 5, 6])",
            "[[1, 4], [2, 5], [3, 6]]",
            marks=pytest.mark.pt_BR,
            id="pt_BR_transpose",
        ),
        pytest.param("en", "size([1, 2, 3; 4, 5, 6])", "[2, 3]", marks=pytest.mark.en, id="en_size"),
        pytest.param("pt_BR", "size([1, 2, 3; 4, 5, 6])", "[2, 3]", marks=pytest.mark.pt_BR, id="pt_BR_size"),
        pytest.param(
            "en",
            "inv([1, 2; 3, 4])",
            "[[-2, 1], [1.5, -0.5]]",
            marks=pytest.mark.en,
            id="en_inv",
        ),
        pytest.param(
            "pt_BR",
            "inv([1, 2; 3, 4])",
            "[[-2, 1], [1.5, -0.5]]",
            marks=pytest.mark.pt_BR,
            id="pt_BR_inv",
        ),
    ]

    complex: ClassVar[list] = [
        pytest.param("en", "2 + 3i", "2+3i", marks=pytest.mark.en, id="en_cplx_add"),
        pytest.param("pt_BR", "2 + 3i", "2+3i", marks=pytest.mark.pt_BR, id="pt_BR_cplx_add"),
        pytest.param("en", "conj(2 + 3i)", "2-3i", marks=pytest.mark.en, id="en_conj"),
        pytest.param("pt_BR", "conj(2 + 3i)", "2-3i", marks=pytest.mark.pt_BR, id="pt_BR_conj"),
        pytest.param("en", "re(2 + 3i)", "2", marks=pytest.mark.en, id="en_re"),
        pytest.param("pt_BR", "re(2 + 3i)", "2", marks=pytest.mark.pt_BR, id="pt_BR_re"),
        pytest.param("en", "im(2 + 3i)", "3", marks=pytest.mark.en, id="en_im"),
        pytest.param("pt_BR", "im(2 + 3i)", "3", marks=pytest.mark.pt_BR, id="pt_BR_im"),
        pytest.param("en", "i * i", "-1", marks=pytest.mark.en, id="en_i_i"),
        pytest.param("pt_BR", "i * i", "-1", marks=pytest.mark.pt_BR, id="pt_BR_i_i"),
        pytest.param("en", "sqrt(-1)", "i", marks=pytest.mark.en, id="en_sqrt_neg"),
        pytest.param("pt_BR", "sqrt(-1)", "i", marks=pytest.mark.pt_BR, id="pt_BR_sqrt_neg"),
    ]

    combinatorics: ClassVar[list] = [
        pytest.param("en", "factorial(10)", "3.6288e+6", marks=pytest.mark.en, id="en_fact"),
        pytest.param("pt_BR", "factorial(10)", "3.6288e+6", marks=pytest.mark.pt_BR, id="pt_BR_fact"),
        pytest.param("en", "combinations(10, 3)", "120", marks=pytest.mark.en, id="en_comb"),
        pytest.param("pt_BR", "combinations(10, 3)", "120", marks=pytest.mark.pt_BR, id="pt_BR_comb"),
        pytest.param("en", "permutations(5, 2)", "20", marks=pytest.mark.en, id="en_perm"),
        pytest.param("pt_BR", "permutations(5, 2)", "20", marks=pytest.mark.pt_BR, id="pt_BR_perm"),
        pytest.param("en", "bellNumbers(5)", "52", marks=pytest.mark.en, id="en_bell"),
        pytest.param("pt_BR", "bellNumbers(5)", "52", marks=pytest.mark.pt_BR, id="pt_BR_bell"),
        pytest.param("en", "catalan(4)", "14", marks=pytest.mark.en, id="en_catalan"),
        pytest.param("pt_BR", "catalan(4)", "14", marks=pytest.mark.pt_BR, id="pt_BR_catalan"),
    ]

    string: ClassVar[list] = [
        pytest.param(
            "en",
            '"Hello, " + "World!"',
            '"Hello, World!"',
            marks=pytest.mark.en,
            id="en_concat",
        ),
        pytest.param(
            "pt_BR",
            '"Hello, " + "World!"',
            '"Hello, World!"',
            marks=pytest.mark.pt_BR,
            id="pt_BR_concat",
        ),
        pytest.param("en", '"Hello" == "Hello"', "true", marks=pytest.mark.en, id="en_eq"),
        pytest.param("pt_BR", '"Hello" == "Hello"', "true", marks=pytest.mark.pt_BR, id="pt_BR_eq"),
    ]

    user_defined: ClassVar[list] = [
        pytest.param(
            "en",
            "x = 5; y = x * 2 + 3; f(x) = x^2 + 2*x + 1; f(3)",
            "16",
            marks=pytest.mark.en,
            id="en_var_func",
        ),
        pytest.param(
            "pt_BR",
            "x = 5; y = x * 2 + 3; f(x) = x^2 + 2*x + 1; f(3)",
            "16",
            marks=pytest.mark.pt_BR,
            id="pt_BR_var_func",
        ),
        pytest.param(
            "en",
            "g(a, b) = a * b; g(4, 5)",
            "20",
            marks=pytest.mark.en,
            id="en_func",
        ),
        pytest.param(
            "pt_BR",
            "g(a, b) = a * b; g(4, 5)",
            "20",
            marks=pytest.mark.pt_BR,
            id="pt_BR_func",
        ),
    ]

    logic: ClassVar[list] = [
        pytest.param("en", "true and false", "false", marks=pytest.mark.en, id="en_and"),
        pytest.param("pt_BR", "true and false", "false", marks=pytest.mark.pt_BR, id="pt_BR_and"),
        pytest.param("en", "true or false", "true", marks=pytest.mark.en, id="en_or"),
        pytest.param("pt_BR", "true or false", "true", marks=pytest.mark.pt_BR, id="pt_BR_or"),
        pytest.param("en", "not false", "true", marks=pytest.mark.en, id="en_not"),
        pytest.param("pt_BR", "not false", "true", marks=pytest.mark.pt_BR, id="pt_BR_not"),
        pytest.param("en", "5 > 3", "true", marks=pytest.mark.en, id="en_gt"),
        pytest.param("pt_BR", "5 > 3", "true", marks=pytest.mark.pt_BR, id="pt_BR_gt"),
        pytest.param("en", "2 <= 2", "true", marks=pytest.mark.en, id="en_leq"),
        pytest.param("pt_BR", "2 <= 2", "true", marks=pytest.mark.pt_BR, id="pt_BR_leq"),
        pytest.param(
            "en",
            "x = 10; x > 5 ? 'High' : 'Low'",
            '"High"',
            marks=pytest.mark.en,
            id="en_ternary",
        ),
        pytest.param(
            "pt_BR",
            "x = 10; x > 5 ? 'High' : 'Low'",
            '"High"',
            marks=pytest.mark.pt_BR,
            id="pt_BR_ternary",
        ),
    ]

    range: ClassVar[list] = [
        pytest.param("en", "sum(range(1, 11))", "66", marks=pytest.mark.en, id="en_range_sum"),
        pytest.param("pt_BR", "sum(range(1, 11))", "66", marks=pytest.mark.pt_BR, id="pt_BR_range_sum"),
        pytest.param("en", "sum(range(0, 102, 2))", "2652", marks=pytest.mark.en, id="en_range_even"),
        pytest.param("pt_BR", "sum(range(0, 102, 2))", "2652", marks=pytest.mark.pt_BR, id="pt_BR_range_even"),
        pytest.param("en", "prod(range(1, 7))", "5040", marks=pytest.mark.en, id="en_range_prod"),
        pytest.param("pt_BR", "prod(range(1, 7))", "5040", marks=pytest.mark.pt_BR, id="pt_BR_range_prod"),
        pytest.param("en", "mean(range(0, 55, 5))", "27.5", marks=pytest.mark.en, id="en_range_mean"),
        pytest.param("pt_BR", "mean(range(0, 55, 5))", "27.5", marks=pytest.mark.pt_BR, id="pt_BR_range_mean"),
    ]

    complex_expressions: ClassVar[list] = [
        pytest.param(
            "en",
            "sin(cos(pi / 3)) + log(exp(1))",
            "1.479425538604203",
            marks=pytest.mark.en,
            id="en_nested",
        ),
        pytest.param(
            "pt_BR",
            "sin(cos(pi / 3)) + log(exp(1))",
            "1.479425538604203",
            marks=pytest.mark.pt_BR,
            id="pt_BR_nested",
        ),
        pytest.param(
            "en",
            "[1, 2, 3, 4] .^ 2",
            "[1, 4, 9, 16]",
            marks=pytest.mark.en,
            id="en_power_elem",
        ),
        pytest.param(
            "pt_BR",
            "[1, 2, 3, 4] .^ 2",
            "[1, 4, 9, 16]",
            marks=pytest.mark.pt_BR,
            id="pt_BR_power_elem",
        ),
        pytest.param(
            "en",
            "sqrt(sum([1, 2, 3, 4].^2))",
            "5.477225575051661",
            marks=pytest.mark.en,
            id="en_sqrt_sum",
        ),
        pytest.param(
            "pt_BR",
            "sqrt(sum([1, 2, 3, 4].^2))",
            "5.477225575051661",
            marks=pytest.mark.pt_BR,
            id="pt_BR_sqrt_sum",
        ),
        pytest.param(
            "en",
            "mean([sin(0), sin(pi/2), sin(pi)])",
            "0.333333333333333",
            marks=pytest.mark.en,
            id="en_mean_sin",
        ),
        pytest.param(
            "pt_BR",
            "mean([sin(0), sin(pi/2), sin(pi)])",
            "0.333333333333333",
            marks=pytest.mark.pt_BR,
            id="pt_BR_mean_sin",
        ),
    ]

    advanced: ClassVar[list] = [
        pytest.param("en", "norm([3, 4], 2)", "5", marks=pytest.mark.en, id="en_norm"),
        pytest.param("pt_BR", "norm([3, 4], 2)", "5", marks=pytest.mark.pt_BR, id="pt_BR_norm"),
        pytest.param("en", "cross([1, 0, 0], [0, 1, 0])", "[0, 0, 1]", marks=pytest.mark.en, id="en_cross"),
        pytest.param("pt_BR", "cross([1, 0, 0], [0, 1, 0])", "[0, 0, 1]", marks=pytest.mark.pt_BR, id="pt_BR_cross"),
        pytest.param("en", "dot([1, 2, 3], [4, 5, 6])", "32", marks=pytest.mark.en, id="en_dot"),
        pytest.param("pt_BR", "dot([1, 2, 3], [4, 5, 6])", "32", marks=pytest.mark.pt_BR, id="pt_BR_dot"),
        pytest.param("en", "kron([1, 2], [3, 4])", "[3, 4, 6, 8]", marks=pytest.mark.en, id="en_kron"),
        pytest.param("pt_BR", "kron([1, 2], [3, 4])", "[3, 4, 6, 8]", marks=pytest.mark.pt_BR, id="pt_BR_kron"),
        pytest.param(
            "en",
            "simplify('2x + x')",
            "3 * x",
            marks=pytest.mark.en,
            id="en_simplify",
        ),
        pytest.param(
            "pt_BR",
            "simplify('2x + x')",
            "3 * x",
            marks=pytest.mark.pt_BR,
            id="pt_BR_simplify",
        ),
        pytest.param(
            "en",
            "derivative('2x^2 + 3x + 4')",
            "4 * x + 3",
            marks=pytest.mark.en,
            id="en_derivative",
        ),
        pytest.param(
            "pt_BR",
            "derivative('2x^2 + 3x + 4')",
            "4 * x + 3",
            marks=pytest.mark.pt_BR,
            id="pt_BR_derivative",
        ),
        pytest.param(
            "en",
            "sqrtm([[4, 1], [1, 4]])",
            "[[1.984059392534428, 0.25200858496555], [0.25200858496555, 1.984059392534428]]",
            marks=pytest.mark.en,
            id="en_sqrtm",
        ),
        pytest.param(
            "pt_BR",
            "sqrtm([[4, 1], [1, 4]])",
            "[[1.984059392534428, 0.25200858496555], [0.25200858496555, 1.984059392534428]]",
            marks=pytest.mark.pt_BR,
            id="pt_BR_sqrtm",
        ),
    ]

    units: ClassVar[list] = [
        pytest.param("en", "unit(5, 'cm')", "5 cm", marks=pytest.mark.en, id="en_unit_create"),
        pytest.param("pt_BR", "unit(5, 'cm')", "5 cm", marks=pytest.mark.pt_BR, id="pt_BR_unit_create"),
        pytest.param(
            "en",
            "5 inch to cm",
            "12.699999999999999 cm",
            marks=pytest.mark.en,
            id="en_inch_cm",
        ),
        pytest.param(
            "pt_BR",
            "5 inch to cm",
            "12.699999999999999 cm",
            marks=pytest.mark.pt_BR,
            id="pt_BR_inch_cm",
        ),
        pytest.param("en", "3.2kg to g", "3200 g", marks=pytest.mark.en, id="en_kg_g"),
        pytest.param("pt_BR", "3.2kg to g", "3200 g", marks=pytest.mark.pt_BR, id="pt_BR_kg_g"),
        pytest.param("en", "unit(10, 'm/s')", "10 m/s", marks=pytest.mark.en, id="en_unit_composite"),
        pytest.param("pt_BR", "unit(10, 'm/s')", "10 m/s", marks=pytest.mark.pt_BR, id="pt_BR_unit_composite"),
    ]

    large_matrices: ClassVar[list] = [
        pytest.param(
            "en",
            "ones(100, 100) * ones(100, 100)",
            marks=pytest.mark.en,
            id="en_ones_100",
        ),
        pytest.param(
            "pt_BR",
            "ones(100, 100) * ones(100, 100)",
            marks=pytest.mark.pt_BR,
            id="pt_BR_ones_100",
        ),
        pytest.param(
            "en",
            "zeros(1000, 1000)",
            marks=pytest.mark.en,
            id="en_zeros_1000",
        ),
        pytest.param(
            "pt_BR",
            "zeros(1000, 1000)",
            marks=pytest.mark.pt_BR,
            id="pt_BR_zeros_1000",
        ),
        pytest.param(
            "en",
            "identity(500)",
            marks=pytest.mark.en,
            id="en_identity_500",
        ),
        pytest.param(
            "pt_BR",
            "identity(500)",
            marks=pytest.mark.pt_BR,
            id="pt_BR_identity_500",
        ),
    ]
