from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email

class InquiryForm(FlaskForm):

    username = StringField(
        "ユーザー名",
        validators=[DataRequired(message="入力が必要です。")]
    )
    
    email = StringField(
        "メールアドレス",
        validators=[DataRequired(message="入力が必要です。"),Email(message="メールアドレスの形式で入力してください。")]
    )

    message = TextAreaField(
        "メッセージ",
        validators=[DataRequired(message="入力が必要です。")]
    )

    submit = SubmitField(("送信"))