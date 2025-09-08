# coding=utf-8
import sympy as sym
from math import sqrt
from sympy.core.function import _coeff_isneg
import random

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


def constant_sign(x, leading=False):
    """
    Gives the string x with the appropriate sign in front
    Useful for making strings involving adding a bunch of terms together
    leading tells whether the constant is first, so shouldn't have a plus sign in that case
    constant_sign(3) gives "+3"
    constant_sign(3, True) gives "3"
    constant_sign(-3) gives "-3"
    constant_sign(sympify(1) / 2) gives "+ \frac{1}{2}"
    etc.
    """
    if x >= 0 and not leading:
        return " + %s" % sym.latex(x)
    elif x >= 0 and leading:
        return sym.latex(x)
    elif x < 0:
        return sym.latex(x)


def pmsign(x, leading=False):
    """
    Gives the string x with the appropriate sign in front
    Useful for making strings involving adding a bunch of terms together
    leading tells whether the constant is first, so shouldn't have a plus sign in that case
    constant_sign(3 * x) gives "+3x"
    constant_sign(3 * x ** 2, Leading=True) gives "3x^2"
    constant_sign(-3) gives "-3"
    constant_sign(x / 2) gives "+ \frac{x}{2}"
    etc.
    """
    x = sym.sympify(x)
    if leading:
        if abs(x) == 1:
            return "" if x > 0 else "-"
        else:
            return sym.latex(x)
    if _coeff_isneg(x):
        return "- %s" % (sym.latex(abs(x)) if x != -1 else "")
    else:
        return "+ %s" % (sym.latex(x) if x != 1 else "")


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


def poly_slicer(poly, first_n_terms=None, show_zeros=True, ghost_terms=True, underline=False,
                x=sym.symbols('x')):
    """Helper Function for Polynomial long division"""
    if show_zeros:
        terms = sym.Poly(poly, x).all_terms()
    else:
        terms = sym.Poly(poly, x).terms()

    first_n_terms = len(terms) if (first_n_terms is None or first_n_terms > len(terms)) else first_n_terms

    if underline:
        if len(terms) == 1 and terms[0][0][0] == 0:
            first_term = constant_sign(terms[0][1], leading=True)
        else:
            first_term = pmsign(terms[0][1], leading=True)
        poly_string = f"\\underline{{ \\left({first_term}{sym.latex(x ** terms[0][0][0])}"

        for term in terms[1:first_n_terms]:
            poly_string += f"{constant_sign(term[1])}" \
                           f"{sym.latex(x ** term[0][0]) if term[0][0] != 0 else ''}"

        poly_string += " \\right)}"
    else:
        if len(terms) == 1 and terms[0][0][0] == 0:
            first_term = constant_sign(terms[0][1], leading=True)
        else:
            first_term = pmsign(terms[0][1], leading=True)
        poly_string = f"{first_term}" \
                      f"{sym.latex(x ** terms[0][0][0]) if terms[0][0][0] != 0 else ''}"

        for term in terms[1:first_n_terms]:
            poly_string += f"{constant_sign(term[1])}" \
                           f"{sym.latex(x ** term[0][0]) if term[0][0] != 0 else ''}"

    if ghost_terms:
        poly_string += f"\\phantom{{ {'{{}}' if not underline else ''} "
        for term in terms[first_n_terms:]:
            poly_string += f"{constant_sign(term[1])}" \
                           f"{sym.latex(x ** term[0][0]) if term[0][0] != 0 else ''}"
        poly_string += " }"

    return poly_string


def poly_long_division(n, d, x=sym.symbols('x')):
    """
    function n / d:
        require d ≠ 0
        q ← 0
        r ← n       # At each step n = d × q + r
        while r ≠ 0 AND degree(r) ≥ degree(d):
        t ← lead(r)/lead(d)     # Divide the leading terms
         q ← q + t
         r ← r − t * d
    return (q, r)
    :return: LaTeX for polynomial long division n / d
    """
    n = sym.Poly(n, x)
    d = sym.Poly(d, x)

    q = sym.div(n, d)[0]

    long_div_string = f"\\require{{enclose}}" \
                      f"\\begin{{array}}{{r}}" \
                      f"{sym.latex(q.as_expr())} \\\\[-3pt] " \
                      f"{sym.latex(d.as_expr())} \\enclose{{longdiv}}{{{poly_slicer(n)}}}"

    term_length = len(d.all_terms())

    q = 0
    r = n
    while r != 0 and sym.degree(r) >= sym.degree(d):
        t = sym.LT(r) / sym.LT(d)
        q = q + t
        r = r - t * d

        if r == 0 or sym.degree(r) < sym.degree(d):
            long_div_string += f"\\\\[-3pt] -{poly_slicer(t * d, first_n_terms=term_length, underline=True)}" \
                               f"\\\\[-3pt] {poly_slicer(r, show_zeros=False)}"
        else:
            long_div_string += f"\\\\[-3pt] -{poly_slicer(t * d, first_n_terms=term_length, underline=True)}" \
                               f"\\\\[-3pt] {poly_slicer(r, first_n_terms=term_length)}"

    return f"$${long_div_string} \\end{{array}}$$"


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

    vert_add = "\\begin{align}" + "\\,".join(addends[0]) + "\\\\"

    for addend in addends[1:-1]:
        vert_add += "\\,".join(addend) + "\\\\"

    spacing = "\\phantom{0} " * (len(addends[0]) - len(addends[-1]))

    vert_add += "+" + spacing + " \\quad " + "\\,".join(addends[-1]) \
                + "\\\\ \\hline " + "%s" % "\\,".join(total) + "\\end{align}"

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
    return int(int(n) // (10 ** i)) % 10


def int_long_division(a, d):
    """
    :param a: Some whole number
    :param d: Some other whole number
    :return: LaTeX for a/d
    """

    q = int(a // d)

    ret = "$$\\require{enclose}\\begin{array}{r}%s \\\\[-3pt] %s \\enclose{longdiv}{%s}\kern-.2ex \\\\[-3pt]" \
          % (q, d, a)

    n = len(str(q))

    if n == 1:
        sb = ["\\underline{%s}" % (q * d)]
        sr = [a % d]
    else:
        b = [d * dig(q, i) for i in range(n)]

        r = [d % a] * n
        r[n - 1] = int(a // (10 ** (n - 2))) - (b[n - 1] * 10)
        for i in range(n - 2, -1, -1):
            r[i] = (r[i + 1] - b[i]) * 10 + dig(a, i - 1)
        r[0] = int(r[0] // 10)

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


def number_line_inequality(first, last, a, relation):
    negticks = ""
    ticks = ""

    for i in range(int(first), int(last) + 1):
        if i < 0:
            negticks += "%s," % i
        else:
            ticks += "%s," % i

    if negticks != "":
        negticks = negticks[:-1]
    if ticks != "":
        ticks = ticks[:-1]

    point = ""
    if int(sym.sympify(a)) != a:
        if a < 0:
            point = "\\draw[shift={(%s-.12,-3pt)},color=black] node[below] {\\tiny $%s$};" % (a, sym.latex(a))
        else:
            point = "\\draw[shift={(%s,-3pt)},color=black] node[below] {\\tiny $%s$};" % (a, sym.latex(a))

    if relation == ">" or relation == ">=":
        if relation == ">=":
            paren = "["
        else:
            paren = "("
        line = "\\begin{tikzpicture}" \
               "\\draw[latex-latex, thick] (%s, 0) -- (%s, 0);" \
               "\\foreach \\x in  {%s}" \
               "\\draw[shift={(\\x,0)},color=black,thick] (0pt,3.5pt) -- (0pt,-3.5pt);" \
               "\\foreach \\x in  {%s}" \
               "\\draw[shift={(\\x,0)},color=black,thick] (0pt,3.5pt) -- (0pt,-3.5pt);" \
               "\\foreach \\x in {%s}" \
               "\\draw[shift={(\\x-.12,-3pt)},color=black, thick] node[below] {\\small $\\x$};" \
               "\\foreach \\x in {%s}" \
               "\\draw[shift={(\\x,-3pt)},color=black, thick] node[below] {\\small $\\x$};" \
               "%s" \
               "\\draw[{%s-latex}, ultra thick, color=cyan] (%s,0) -- (%s,0);" \
               "\\end{tikzpicture}" % (
               first - .5, last + .5, negticks, ticks, negticks, ticks, point, paren, a - .03, last + .53)

    else:
        if relation == "<=":
            paren = "]"
        else:
            paren = ")"
        line = "\\begin{tikzpicture}" \
               "\\draw[latex-latex, thick] (%s, 0) -- (%s, 0);" \
               "\\foreach \\x in  {%s}" \
               "\\draw[shift={(\\x,0)},color=black,thick] (0pt,3.5pt) -- (0pt,-3.5pt);" \
               "\\foreach \\x in  {%s}" \
               "\\draw[shift={(\\x,0)},color=black,thick] (0pt,3.5pt) -- (0pt,-3.5pt);" \
               "\\foreach \\x in {%s}" \
               "\\draw[shift={(\\x-.12,-3pt)},color=black, thick] node[below] {\\small $\\x$};" \
               "\\foreach \\x in {%s}" \
               "\\draw[shift={(\\x,-3pt)},color=black, thick] node[below] {\\small $\\x$};" \
               "%s" \
               "\\draw[{latex-%s}, ultra thick, color=cyan] (%s,0) -- (%s,0);" \
               "\\end{tikzpicture}" % (first - .5, last + .5, negticks, ticks, negticks, ticks, point,
                                       paren, first - .53, a + .03)

    return line

