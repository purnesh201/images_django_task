from django import forms
from .models import User, images
from django.core.files.images import get_image_dimensions


class userForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput,help_text='Atleast 8 characters having 1 digit and 1 special character')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name',)
    last_name = forms.CharField(label='Last Name',)
    email = forms.EmailField(label='Email',)
    username = forms.CharField(label='User Name',)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']

        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First Name cannot have numbers")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']

        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last Name cannot have numbers")
        return lastname
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if "gmail" != email.split("@")[1].split('.')[0]:
            raise forms.ValidationError("Please use .gmail email ")
        return email

    def clean_password2(self):
        pas = self.cleaned_data['password']
        cd =   self.cleaned_data['password2']
        MIN_LENGTH=8
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            
        if pas and cd:
            if pas != cd:
                raise forms.ValidationError('Passwords don\'t match.')
            else:
                if len(pas)<MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast %d characters"%MIN_LENGTH)
                if pas.isdigit():
                    raise forms.ValidationError("Password should not be all numeric")
                if pas.isalpha():
                    raise forms.ValidationError("Password should have atleast one digit")
                if not any(char in special_characters for char in pas):
                    raise forms.ValidationError("Password should have atleast one Special Character")


class loginForm(forms.Form):
    class Meta:
        model = User
        fields = ('username','password')

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class imageForm(forms.ModelForm):
    class Meta:
        model = images
        fields = ('name', 'image')

        labels = {
            'name': ('Image Name'),
            'image': ('Image Upload')}
        widgets ={
            'image': forms.FileInput({'placeholder': 'Upload Image'}),
            'name': forms.TextInput({'placeholder': 'Image Name'})}

    def clean_name(self):
        name = self.cleaned_data['name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name cannot have digits")
        if any(char in special_characters for char in name):
            raise forms.ValidationError("Name should not have Special Characters")
        print ("Verified Everything clearly------------2332---")
        return name
    
    def clean_image(self):
        image = self.cleaned_data['image']

        try:
            w, h = get_image_dimensions(image)

            # # validate dimensions
            max_width = max_height = 2000
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(image) > (20 * 1024 *1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20mb.')
            print ("Verified Everything clearly---------------")

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        
        print ("Verified Everything clearly-----returning----------")

        return image


