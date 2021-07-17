# coding=utf-8
import sympy as sym
from math import sqrt


def sgn(a, lead=False):
    if lead:
        if a == 1:
            return ""
        if a == -1:
            return " - "
        return "%s" % a
    if a == -1:
        return " - "
    if a < -1:
        return " - %s " % abs(a)
    if a != 1:
        return " + %s " % abs(a)
    return " + "


def coefficients(p, x=sym.symbols('x')):
    """
    finds the coefficients of a polynomial p
    returns them as a list from the constant upward
    """
    r = p
    l = []
    while r != 0:
        l.append(r.subs(x, 0))
        r = sym.simplify((r - r.subs(x, 0)) / x)
    return l


def show_zeros(p, var):
    coeffs = coefficients(p, var)
    coeffs.reverse()
    exps = [k for k in range(len(coeffs))]
    exps.reverse()

    ret = ""
    lead = True
    for a, k in zip(coeffs, exps):
        if var ** k != 1:
            if k != 0:
                ret += sgn(a, lead) + sym.latex(var ** k)
            else:
                ret += sgn(a, lead)
        else:
            if a > 0:
                ret += "+ %s" % a
            else:
                ret += "%s" % a
        lead = False

    return ret


def first_n_terms(p, n, var=sym.symbols('x')):
    p = sym.Poly(p, var)
    coeffs = p.all_coeffs()

    ret = sum([coeffs[k] * var ** (len(coeffs) - k - 1) for k in range(0, min(n, len(coeffs)))])

    return sym.latex(ret)


def poly_long_division(a, d, var=sym.symbols('x')):
    """
    function a / d:
    require d ≠ 0
     q ← 0
     r ← a       # At each step a = d × q + r
     while r ≠ 0 AND degree(r) ≥ degree(d):
        t ← lead(r)/lead(d)     # Divide the leading terms
        q ← q + t
        r ← r − t * d
     return (q, r)

    :param a: Some whole number
    :param d: Some other whole number
    :param var: The variable, defaults to x
    :return: LaTeX for a/d
    """

    q = sym.div(a, d)[0]
    n = len(coefficients(d, var))

    ret = "$$\\require{enclose}\\begin{array}{r}%s \\phantom{)} \\\\[-3pt] %s \\enclose{longdiv}{%s \\phantom{)}} " \
          % (sym.latex(q), sym.latex(d), show_zeros(a, var))

    remainders = []
    subtract_me = []
    q = 0
    r = a  # At each step n = d × q + r

    while r != 0 and sym.degree(r) >= sym.degree(d):
        t = sym.LT(r, gens=var) / sym.LT(d, gens=var)  # Divide the leading terms
        q = q + t
        r = sym.expand(sym.sympify(r - t * d))

        subtract_me.append(sym.latex(sym.expand(t * d)) + "\\phantom{ }")

        remainders.append(first_n_terms(r, n, var) + "\\phantom{ ) }")

    # Spacing :-0
    poly = ""
    poly2 = ""
    space = [""]
    space2 = ["", ""]
    coeffs_a = sym.Poly(a, var).all_coeffs()
    coeffs_a.reverse()
    for k, s in enumerate(subtract_me):
        poly = poly + "+" + "%s %s" % (abs(coeffs_a[k]), sym.latex(var ** k) if k != 0 else "")
        space.append("\\phantom{%s )}" % poly)

    for k, r in enumerate(remainders):
        poly2 = poly2 + "+" + "%s %s" % (abs(coeffs_a[k]), sym.latex(var ** k) if k != 0 else "")
        space2.append("\\phantom{%s )}" % poly2)

    space.pop()
    space2.pop()
    space2.pop()

    for s, r in zip(subtract_me, remainders):
        ret += "\\\\ \\underline{-(%s)} %s \\\\ %s %s " % (s, space.pop(), r, space2.pop())

    ret += "\\end{array}$$"
    return ret


def synthetic_division(f, g):
    x = sym.symbols('x')
    f = sym.Poly(f, x)
    g = sym.Poly(g, x)

    coeffs_f = f.all_coeffs()
    coeffs_g = g.all_coeffs()
    d = -coeffs_g[1]

    ret = "\\begin{array}{" + "r" * (len(coeffs_f) + 1) + "}"

    first_row = [d] + coeffs_f
    first_row_string = "\\fbox{$%s$} & " % d + " & ".join([str(c) for c in coeffs_f])

    third_row = [coeffs_f[0]]
    second_row = []
    for k in range(len(coeffs_f) - 1):
        second_row.append(d * third_row[k])
        third_row.append(coeffs_f[k + 1] + d * third_row[k])

    second_row_string = "&& " + " & ".join([str(c) for c in second_row])
    third_row_string = "& " + " & ".join([str(c) for c in third_row[:-1]]) + "& \\fbox{$%s$}" % third_row[-1]

    ret += first_row_string + " \\\\ " + second_row_string + " \\\\ \\hline " + third_row_string + " \\end{array}"

    return ret


def num_digit(n, k):
    if len(str(n)) > k:
        return int(str(n)[len(str(n)) - k - 1])
    return 0


def vertical_addition(*addends):
    addends = sorted(list(addends), reverse=True)
    total = [digit for digit in str(sum(addends))]
    carries = [0] * (max([len(str(addend)) for addend in addends]) + 1)

    for k in range(len(carries) - 2, -1, -1):
        carries[k] = int((carries[k + 1] + sum([num_digit(addend, len(carries) - 2 - k) for addend in addends])) / 10)

    carries = ["" if carry == 0 else str(carry) for carry in carries]

    addends = [[digit for digit in str(addend)] for addend in addends]

    addends[0] = ["\\overset{%s}{%s}" % (carry, digit) for (carry, digit) in
                  zip(carries, ["\\phantom{0}"] + addends[0])]

    vert_add = "\\begin{align}" + "\,".join(addends[0]) + "\\\\"

    for addend in addends[1:-1]:
        vert_add += "\,".join(addend) + "\\\\"

    spacing = "\\phantom{0} " * (len(addends[0]) - len(addends[-1]))

    vert_add += "+" + spacing + " \\quad " + "\,".join(addends[-1]) \
                + "\\\\ \\hline " + "%s" % "\,".join(total) + "\\end{align}"

    return vert_add


def dig(n, i):
    """
    returns the digit in the 10^i 's place of n
    :param n:
    :param i:
    :return:
    """
    if n < 10 ** i:
        return 0
    return (int(n) / (10 ** i)) % 10


def int_long_division(a, d):
    """
    :param a: Some whole number
    :param d: Some other whole number
    :return: LaTeX for a/d
    """

    q = a / d

    ret = "$$\\require{enclose}\\begin{array}{r}%s \\\\[-3pt] %s \\enclose{longdiv}{%s}\kern-.2ex \\\\[-3pt]" \
          % (q, d, a)

    n = len(str(q))

    if n == 1:
        sb = ["\\underline{%s}" % (q * d)]
        sr = [a % d]
    else:
        b = [d * dig(q, i) for i in range(n)]

        r = [d % a] * n
        r[n - 1] = (a / (10 ** (n - 2))) - (b[n - 1] * 10)
        for i in range(n - 2, -1, -1):
            r[i] = (r[i + 1] - b[i]) * 10 + dig(a, i - 1)
        r[0] = int(r[0] / 10)

        sb = []
        for bb in b:
            if len(str(bb)) > 1:
                sb.append(str(bb))
            else:
                sb.append("0" + str(bb))

        sb = ["\\underline{" + sb[i] + "\\phantom{0}" + "}" + "\\phantom{0}" * (i - 1) for i in range(n)]
        sr = [str(r[i]) + "\\phantom{0}" * (i - 1) for i in range(n)]

        sb[0] = "\\underline{%s}" % str(b[0])

    for i in range(1, n + 1):
        ret += "%s \\\\[-3pt] %s \\\\[-3pt]" % (sb[n - i], sr[n - i])
    ret += "\\end{array}$$"

    return ret.replace("{00\\", "{0\\")


def vertical_subtraction(a, b):
    a_digits = [int(digit) for digit in str(a)]
    b_digits = [int(digit) for digit in str(b)]
    c_digits = [digit for digit in str(a - b)]

    borrows = [""] * len(a_digits)
    double_borrows = [""] * len(a_digits)
    b_zeros = [0] * (len(a_digits) - len(b_digits)) + b_digits

    for i in range(1, len(a_digits)):
        if b_zeros[i] > a_digits[i]:
            borrows[i] = a_digits[i] + 10
            borrows[i - 1] = a_digits[i - 1] - 1

    new_a = [borrow if borrow != "" else a_dig for (a_dig, borrow) in zip(a_digits, borrows)]
    for i in range(1, len(a_digits)):
        if b_zeros[i] > new_a[i]:
            double_borrows[i] = new_a[i] + 10
            double_borrows[i - 1] = new_a[i - 1] - 1

    for k in range(len(borrows)):
        if borrows[k] == "" and double_borrows[k] != "":
            borrows[k] = double_borrows[k]
            double_borrows[k] = ""

    borrows = ["\\vphantom{\\cancel{0}} %s" % borrow if dborrow == ""
               else "\\overset{\\scriptstyle %s}{\\cancel{%s}}" % (dborrow, borrow)
               for (dborrow, borrow) in zip(double_borrows, borrows)]

    a_digits = [str(digit) for digit in str(a)]
    b_digits = [str(digit) for digit in str(b)]

    a_digits = ["\\;%s\\;" % digit if borrow == "\\vphantom{\\cancel{0}} "
                else "\\overset{%s}{\\cancel{%s}}" % (borrow, digit)
                for (borrow, digit) in zip(borrows, a_digits)]

    spacing = "\\phantom{0} \\; " * (len(str(a)) - len(str(b)))

    vert_sub = "$$\\require{cancel}\\begin{align}" + "".join(a_digits) + "\\\\" \
               + "- \\quad" + spacing + "\\;\\;".join(b_digits) + "\\;" "\\\\ \\hline "

    vert_sub += "\\hline " + "\\;\\;".join(c_digits) + "\\;" + "\\end{align}$$"

    return vert_sub


def create_graph(f, left=-8, right=8):
    ret = "\\begin{tikzpicture}" \
          "\\begin{axis}[standard]" \
          "\\path(axis cs:0,0) node[anchor=north east] {0}; " \
          "\\addplot[<->,ultra thick, color=blue, samples=150, domain=%s:%s]{%s};" \
          "\\end{axis}" \
          "\\end{tikzpicture}" % (left, right, str(f).replace("**", "^"))

    return ret


def factor_tree(number):
    global tree_text
    tree_text = ""

    def prime_factors_recursive(n, level):
        """Finds the prime factors of 'n' and generates text representation
             according to tikz forest package.
        """
        limit = int(sqrt(n)) + 1
        divisor = 2
        num = n
        level += 1
        global tree_text
        tree_text = tree_text + "["
        for divisor in range(2, limit):
            if num % divisor == 0:
                num /= divisor
                tree_text = tree_text + "%d [%d,circle, draw] " % (n, divisor)
                return n, (divisor, prime_factors_recursive(num, level))
        tree_text = tree_text + "%d,circle,draw" % n
        for i in range(level):
            tree_text = tree_text + "]"
        return n,

    prime_factors_recursive(number, 0)
    output = r'\begin{forest}' + tree_text + r'\end{forest}'
    return output
