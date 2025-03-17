from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, PasswordField,SubmitField
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from p4a.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists! Try another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('E-mail already exists! Try another one')

    name = StringField(label='', validators=[Length(2,20), DataRequired()])
    age = IntegerField(label='',validators=[DataRequired()])
    username = StringField(label='',validators=[Length(2,20), DataRequired()])
    email = StringField(label='', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='', validators=[Length(6,20), DataRequired()])
    password2 = PasswordField(label='', validators=[EqualTo('password1'), DataRequired()])
    image = FileField('Profile Picture', validators=[DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='', validators=[DataRequired()])
    password = PasswordField(label='', validators=[DataRequired()])
    submit = SubmitField(label='Log in')


class PetListForm(FlaskForm):
    name = StringField(label='', validators=[DataRequired()])
    age = IntegerField(label='', validators=[DataRequired()])
    breed = StringField(label='', validators=[DataRequired()])
    price = IntegerField(label='')
    seller_phone = StringField(label='', validators=[DataRequired()])
    status = StringField(label='', validators=[DataRequired()])
    description = StringField(label='', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired(),
                                           FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Submit')


class PetForYouForm(FlaskForm):

    grooming = SelectField('How much time are you willing to dedicate to grooming your dog daily?', choices=[
        ('0', 'Not willing'),
        ('0.5', 'Neutral'),
        ('1', 'Very willing'),
    ])

    grooming_preference = SelectField('Are you comfortable with regular brushing and grooming sessions for your dog?', choices=[
        ('0', 'Low preference'),
        ('0.5', 'Moderate preference'),
        ('1', 'High preference'),
    ])

    minimal_grooming = SelectField('Would you prefer a dog breed with minimal grooming needs?', choices=[
        ('0', 'Not important'),
        ('0.5', 'Neutral'),
        ('1', 'Very important'),
    ])

    shedding = SelectField('Are you okay with a dog that sheds moderately throughout the year?', choices=[
        ('0', 'Not okay'),
        ('0.5', 'Neutral'),
        ('1', 'Completely okay'),
    ])

    shedding_preference = SelectField('Is minimal shedding a priority for you when choosing a dog breed?', choices=[
        ('0', 'Low priority'),
        ('0.5', 'Moderate priority'),
        ('1', 'High priority'),
    ])

    manage_shedding = SelectField('How do you feel about managing loose hairs and shedding in your living space?', choices=[
        ('0', 'Not comfortable'),
        ('0.5', 'Neutral'),
        ('1', 'Very comfortable'),
    ])

    energy_level = SelectField('Describe your daily activity level – are you more active or prefer a relaxed lifestyle?', choices=[
        ('0', 'Sedentary'),
        ('0.5', 'Moderately Active'),
        ('1', 'Highly active'),
    ])

    daily_exercise = SelectField('How much time can you commit to daily exercise and playtime with your dog?', choices=[
        ('0', 'No time'),
        ('0.5', 'Moderate time'),
        ('1', 'Plenty of time'),
    ])

    outdoor_activities = SelectField('Do you prefer a dog with high energy levels for outdoor activities?', choices=[
        ('0', 'Not at all'),
        ('0.5', 'Neutral'),
        ('1', 'Absolutely'),
    ])

    trainability = SelectField('How important is it to you that your dog is easily trainable?', choices=[
        ('0', 'Not important'),
        ('0.5', 'Moderately important'),
        ('1', 'Very important'),
    ])

    obedience_training = SelectField('Are you willing to invest time in obedience training for your dog?', choices=[
        ('0', 'Not willing'),
        ('0.5', 'Neutral'),
        ('1', 'Very willing'),
    ])

    quick_learning = SelectField('Do you prefer a dog that quickly learns new commands and tricks?', choices=[
        ('0', 'Not important'),
        ('0.5', 'Neutral'),
        ('1', 'Very important'),
    ])

    demeanor = SelectField('Would you like a dog with a calm and laid-back demeanor?', choices=[
        ('0', 'Not at all'),
        ('0.5', 'Neutral'),
        ('1', 'Absolutely'),
    ])

    playful = SelectField('Are you looking for a playful and outgoing dog, or a more reserved companion?', choices=[
        ('0', 'Reserved companion'),
        ('0.5', 'Neutral'),
        ('1', 'Playful and outgoing'),
    ])

    reserved = SelectField('How do you envision the temperament of your ideal dog?', choices=[
        ('0', 'Not reserved at all'),
        ('0.5', 'Neutral'),
        ('1', 'Very reserved'),
    ])

    size_of_living_space = SelectField('What size of living space do you have available for your dog? (e.g., '
                                       'apartment, house with a yard)', choices=[
                                        ('0', 'Apartment'),
                                        ('0.5', 'House'),
                                        ('1', 'Farm'),
                                        ])

    preferred_size = SelectField('Are you comfortable with a larger-sized dog, or do you prefer a smaller companion?', choices=[
        ('0', 'Smaller companion'),
        ('0.5', 'Neutral'),
        ('1', 'Larger-sized dog'),
    ])

    indoor_space = SelectField('How much indoor space can your dog comfortably occupy in your home?', choices=[
        ('0', 'Limited space'),
        ('0.5', 'Moderate space'),
        ('1', 'Abundant space'),
    ])

    submit = SubmitField('Submit')


class AccessoryForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    description = StringField(label='Description', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired(),
                                           FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Submit')


class RateUserForm(FlaskForm):
    rating = RadioField('Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[DataRequired()])
    comment = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    image = FileField('Update Profile Picture')
    submit = SubmitField('Update Profile')