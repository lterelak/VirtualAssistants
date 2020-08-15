from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import FileField
from wtforms import StringField
from wtforms import IntegerField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired


class AddVirtualAssistant(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    job = SelectField("job", choices=[], coerce=int, validators=[DataRequired()])
    photo = FileField("photo", validators=[DataRequired()])

class UpdateVirtualAssistant(AddVirtualAssistant):
    id = IntegerField("id", validators=[DataRequired()])
    photo = FileField()