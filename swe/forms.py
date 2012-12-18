from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
from django.utils.safestring import mark_safe
from ajax_upload.widgets import AjaxClearableFileInput
from swe.models import SubjectList, Subject, ServiceList, ServiceType, WordCountRange, ManuscriptOrder


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name',
                            max_length=30,
                            )
    last_name = forms.CharField(label='Last Name',
                            max_length=30,
                            )
    #email is be treated as username in auth.models.User and separately written to active_email in UserProfile
    email = forms.EmailField(label='Email address', 
                            max_length = 30,
                            )
    password = forms.CharField(label='Password',
                            max_length = 30,
                            widget=forms.PasswordInput,
                            )
    password_confirm = forms.CharField(label='Re-type password',
                            max_length = 30,
                            widget=forms.PasswordInput,
                            )

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError('The passwords do not match')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        # email doubles used as username. Verify that it is unique in both fields.
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                return email

        raise forms.ValidationError("This email address is already registered.")
        return email

class LoginForm(forms.Form):
    email = forms.CharField(label='Email address',max_length=30)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)

class ConfirmForm(forms.Form):
    activation_key = forms.CharField(label='Activation Key', max_length=100)

class ActivationRequestForm(forms.Form):
    email = forms.CharField(label='Email address',max_length=30)

    def clean_email(self):
        email = self.cleaned_data['email']

        # Verify that email is on record.
        try:
            u = User.objects.get(username=email)
            # Verify that account is not already active.
            if u.is_active:
                raise forms.ValidationError("This account has already been activated.")
        except User.DoesNotExist:
            raise forms.ValidationError("This email address is not registered.")

        return email


class UploadManuscriptForm(forms.Form):
    step = forms.IntegerField(initial=1, widget = forms.widgets.HiddenInput())
    title = forms.CharField(label='Title (choose any name that helps you remember)', max_length=50, required=False)
    subject = forms.ChoiceField(
        label='Field of study', 
        choices=SubjectList.objects.get(is_active=True).get_subject_choicelist(), 
        )
    word_count = forms.ChoiceField(
        label='Word count (do not include references)',
        choices=ServiceList.objects.get(is_active=True).get_wordcountrange_choicelist(),
        )
    manuscript_file = forms.ImageField(widget=AjaxClearableFileInput())
    def clean_manuscript_file(self):
        content = self.cleaned_data['manuscript_file']
        content_type = content.content_type #.split('/')[0]
        if True: #content_type in settings.CONTENT_TYPES:
            if content._size > int(settings.MAX_UPLOAD_SIZE):
                raise forms.ValidationError(
                    u'Please keep file size under %s. Current file size is %s. You may need to remove images to reduce the file size. ' % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(u'File type %s is not supported' % content_type)
        return content


class SelectServiceForm(forms.Form):
    order_pk = None
    step = forms.IntegerField(widget = forms.widgets.HiddenInput(), initial=2)
    order = forms.IntegerField(widget = forms.widgets.HiddenInput())
    servicetype = forms.ChoiceField(label='Type of service')
    word_count_exact = forms.IntegerField(label = 'Number of words in the manuscript (excluding references)')
    def __init__(self, *args, **kwargs):
        # Order PK must be defined either in kwargs or POST data
        try:
            order_pk = kwargs['order_pk']
            del[kwargs['order_pk']]
        except KeyError:
            order_pk = None
        super(SelectServiceForm, self).__init__(*args, **kwargs)
        if order_pk == None:
            try:
                order_pk = self.data['order']
            except KeyError:
                raise Exception('Order number is not available.')
        self.fields['order'].initial = order_pk
        self.order_pk = order_pk
        manuscriptorder = ManuscriptOrder.objects.get(pk=self.order_pk)
        self.fields['servicetype'].choices = manuscriptorder.wordcountrange.get_pricepoint_choicelist()
        if manuscriptorder.wordcountrange.max_words is not None:
            # A definite word count range is already specified. Drop the field.
            del(self.fields['word_count_exact'])
            
    def clean_word_count_exact(self):
        manuscriptorder = ManuscriptOrder.objects.get(pk=self.order_pk)
        maximum_allowed = 1000000
        words = self.cleaned_data['word_count_exact']
        if manuscriptorder.wordcountrange.min_words is not None:
            if words < manuscriptorder.wordcountrange.min_words:            
                raise forms.ValidationError("This word count is not in the selected range.")
        if manuscriptorder.wordcountrange.max_words is not None:
            if words > manuscriptorder.wordcountrange.max_words:            
                raise forms.ValidationError("This word count is not in the selected range.")
        if words > maximum_allowed:
            raise forms.ValidationError("Please contact support submit a document of this length.")
        return words

class SubmitOrderFreeForm(forms.Form):
    step = forms.IntegerField(widget = forms.widgets.HiddenInput(), initial=3)
    order = forms.IntegerField(widget = forms.widgets.HiddenInput())
    invoice = forms.IntegerField(widget = forms.widgets.HiddenInput())
    def __init__(self, *args, **kwargs):
        # Order PK and Invoice PK must be defined either in kwargs or POST data
        try:
            order_pk = kwargs['order_pk']
            del[kwargs['order_pk']]
        except KeyError:
            order_pk = None
        try:
            invoice_pk = kwargs['invoice_pk']
            del[kwargs['invoice_pk']]
        except KeyError:
            invoice_pk = None
        super(SubmitOrderFreeForm, self).__init__(*args, **kwargs)
        if order_pk == None:
            try:
                order_pk = self.data['order']
            except KeyError:
                raise Exception('Order number is not available.')
        self.fields['order'].initial = order_pk
        if invoice_pk == None:
            try:
                invoice_pk = self.data['invoice']
            except KeyError:
                raise Exception('Invoice number is not available.')
        self.fields['invoice'].initial = invoice_pk

