from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired


class AdminForm(FlaskForm):

    username = StringField(
        "管理者名",
        validators=[DataRequired(message="入力が必要です。")]
    )
    
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(message="入力が必要です。")]
    )

    submit = SubmitField(("ログイン"))

class ArticlePost(FlaskForm):

    post_title = StringField(
        "タイトル",
        validators=[DataRequired(message="入力が必要です。")]
    )

    post_contents = TextAreaField(
        "本文",
        validators=[DataRequired(message="入力が必要です。")]
    )

    submit = SubmitField(("投稿する"))





