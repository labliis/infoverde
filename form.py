from wtforms import Form, StringField, PasswordField, validators, HiddenField

def length_honeypot(form,field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe de estar vacio')
class Login(Form):
    userName = StringField('',
                           [
                               validators.DataRequired(),
                               validators.length(min=4, max=25,message="ingrese usuario valido!.")]
                           )
    password = PasswordField('Password')
    honeypot = HiddenField('',[length_honeypot])