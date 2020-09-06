from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class AddVirtualAssistant(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    job = SelectField("job", choices=[], coerce=int, validators=[DataRequired()])
    photo = FileField("photo", validators=[DataRequired(), FileAllowed(['jpg','jpeg','png'])])

class UpdateVirtualAssistant(AddVirtualAssistant):
    id = IntegerField("id", validators=[DataRequired()])
