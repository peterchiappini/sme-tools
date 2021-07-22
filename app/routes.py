from app import app
import random
from flask import render_template, flash, redirect, url_for
from app.forms import PolynomialLongDiv
from app.forms import SyntheticDivision
from app.forms import VerticalAddition
from app.forms import VerticalSubtraction
from app.forms import IntegerLongDiv
from app.forms import GraphPlotter
from app.forms import FactorTree
from app.forms import NumberLine

import subprocess
import os
from pathlib import Path
from app import tools
import sympy as sym
from shutil import copyfile


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/num_line_inequality', methods=['GET', 'POST'])
def num_line_inequality():
    form = NumberLine()
    if form.validate_on_submit():
        first, last, a, relation = sym.sympify(form.first.data), sym.sympify(form.last.data), \
                                   sym.sympify(form.a.data), str(form.relation.data)

        path = Path('.') / 'app/static'
        filename = f"number_line"
        copyfile("app/static/num_line_template.tex", f"app/static/{filename}" + ".tex")

        with open(f"app/static/{filename}" + ".tex", "a") as file:
            file.write(tools.number_line_inequality(first, last, a, relation) + "\\end{document}")

        # Compile LaTeX file to a pdf
        p = subprocess.Popen(["xelatex", "--shell-escape", f"{filename}.tex"], cwd=path)
        p.wait()

        # Convert the pdf to an svg
        if os.path.exists(f'{filename}.svg'):
            os.remove(f'{filename}.svg')
        subprocess.call(["pdf2svg", f'{filename}.pdf', f'{filename}.svg'], cwd=path)

        # Clean up files
        files_to_remove = [".aux", ".log", ".pdf", ".tex"]
        for extension in files_to_remove:
            os.remove(path / f'{filename}{extension}')

        flash(f'/static/{filename}.svg')
        return redirect('/num_line_inequality')
    return render_template('num_line_inequality.html', title='Number Line Inequality', form=form)


@app.route('/factor_tree', methods=['GET', 'POST'])
def factor_tree():
    form = FactorTree()
    if form.validate_on_submit():
        n = sym.sympify(form.function.data)

        path = Path('.') / 'app/static'
        filename = f"factor_tree"
        copyfile("app/static/factor_tree_template.tex", f"app/static/{filename}" + ".tex")

        with open(f"app/static/{filename}" + ".tex", "a") as file:
            file.write(tools.factor_tree(n) + "\\end{document}")

        # Compile LaTeX file to a pdf
        p = subprocess.Popen(["xelatex", "--shell-escape", f"{filename}.tex"], cwd=path)
        p.wait()

        # Convert the pdf to an svg
        if os.path.exists(f'{filename}.svg'):
            os.remove(f'{filename}.svg')
        subprocess.call(["pdf2svg", f'{filename}.pdf', f'{filename}.svg'], cwd=path)

        # Clean up files
        files_to_remove = [".aux", ".log", ".pdf", ".tex"]
        for extension in files_to_remove:
            os.remove(path / f'{filename}{extension}')

        flash(f'/static/{filename}.svg')
        return redirect('/factor_tree')
    return render_template('factor_tree.html', title='Factor Tree', form=form)


@app.route('/plotter', methods=['GET', 'POST'])
def plotter():
    form = GraphPlotter()
    if form.validate_on_submit():
        f = sym.sympify(form.function.data)
        if form.validate_on_submit():
            f = sym.sympify(form.function.data)

            path = Path('.') / 'app/static'
            filename = f"graph"
            copyfile("app/static/plotter_template.tex", f"app/static/{filename}" + ".tex")

            with open(f"app/static/{filename}" + ".tex", "a") as file:
                file.write(tools.create_graph(f) + "\\end{document}")

            # Compile LaTeX file to a pdf
            p = subprocess.Popen(["xelatex", "--shell-escape", f"{filename}.tex"], cwd=path)
            p.wait()

            # Convert the pdf to an svg
            if os.path.exists(f'{filename}.svg'):
                os.remove(f'{filename}.svg')
            subprocess.call(["pdf2svg", f'{filename}.pdf', f'{filename}.svg'], cwd=path)

            # Clean up files
            files_to_remove = [".aux", ".log", ".pdf", ".tex"]
            for extension in files_to_remove:
                os.remove(path / f'{filename}{extension}')

            flash(f'/static/{filename}.svg')
        return redirect('/plotter')
    return render_template('plotter.html', title='Graph a Function', form=form)


@app.route('/int_long_div', methods=['GET', 'POST'])
def int_long_div():
    form = IntegerLongDiv()
    if form.validate_on_submit():
        a = sym.sympify(form.dividend.data)
        d = sym.sympify(form.divisor.data)
        flash('{}'.format(tools.int_long_division(a, d)))
        return redirect('/int_long_div')
    return render_template('int_long_div.html', title='Integer Long Division', form=form)


@app.route('/poly_long_div', methods=['GET', 'POST'])
def poly_long_div():
    form = PolynomialLongDiv()
    if form.validate_on_submit():
        a = sym.sympify(form.dividend.data)
        d = sym.sympify(form.divisor.data)
        flash('{}'.format(tools.poly_long_division(a, d)))
        return redirect('/poly_long_div')
    return render_template('poly_long_div.html', title='Polynomial Long Division', form=form)


@app.route('/synth_div', methods=['GET', 'POST'])
def synth_div():
    form = SyntheticDivision()
    if form.validate_on_submit():
        a = sym.sympify(form.dividend.data)
        d = sym.sympify(form.divisor.data)
        flash('{}'.format(tools.synthetic_division(a, d)))
        return redirect('/synth_div')
    return render_template('synth_div.html', title='Synthetic Division', form=form)


@app.route('/vert_add', methods=['GET', 'POST'])
def vert_add():
    form = VerticalAddition()
    if form.validate_on_submit():
        a = [int(k) for k in list(sym.sympify(form.addends.data))]
        flash('{}'.format(tools.vertical_addition(*a)))
        return redirect('/vert_add')
    return render_template('vert_add.html', title='Vertical Addition', form=form)


@app.route('/vert_sub', methods=['GET', 'POST'])
def vert_sub():
    form = VerticalSubtraction()
    if form.validate_on_submit():
        a = [int(k) for k in list(sym.sympify(form.subtrahends.data))]
        flash('{}'.format(tools.vertical_subtraction(*a)))
        return redirect('/vert_sub')
    return render_template('vert_sub.html', title='Vertical Subtraction', form=form)
