'''사용자 데이터 수신을 위한 form'''

from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from wtforms.validators import DataRequired

class FileUploadForm(FlaskForm):
    files = MultipleFileField('첨부파일', validators=[DataRequired()])