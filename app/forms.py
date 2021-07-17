from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PolynomialLongDiv(FlaskForm):
    divisor = StringField('Divisor', validators=[DataRequired()])
    dividend = StringField('Dividend', validators=[DataRequired()])
    submit = SubmitField('Get LaTeX')


class IntegerLongDiv(FlaskForm):
    divisor = StringField('Divisor', validators=[DataRequired()])
    dividend = StringField('Dividend', validators=[DataRequired()])
    submit = SubmitField('Get LaTeX')


class SyntheticDivision(FlaskForm):
    divisor = StringField('Divisor', validators=[DataRequired()])
    dividend = StringField('Dividend', validators=[DataRequired()])
    submit = SubmitField('Get LaTeX')


class VerticalAddition(FlaskForm):
    addends = StringField('Addends', validators=[DataRequired()])
    submit = SubmitField('Get LaTeX')


class VerticalSubtraction(FlaskForm):
    subtrahends = StringField('Subtrahends', validators=[DataRequired()])
    submit = SubmitField('Get LaTeX')


class GraphPlotter(FlaskForm):
    function = StringField('Function(s)', validators=[DataRequired()])
    submit = SubmitField('Get Image')


class FactorTree(FlaskForm):
    function = StringField('Number', validators=[DataRequired()])
    submit = SubmitField('Get Image')
