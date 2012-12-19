from django import forms
from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models import UploadedFile


class AjaxUploadException(Exception):
    pass


class AjaxClearableFileInput(forms.ClearableFileInput):
    template_with_clear = ''  # We don't need this
    template_with_initial = '%(input)s'

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        if value:
            try:
                uploaded_file = UploadedFile.objects.get(file=value)
                filename = u'%s%s' % (settings.MEDIA_URL, value)
            except UploadedFile.DoesNotExist:
                filename = value
        else:
            filename = ''
        attrs.update({
            'class': attrs.get('class', '') + 'ajax-upload',
            'data-filename': filename,  # This is so the javascript can get the actual value
            'data-required': self.is_required or '',
            'data-upload-url': reverse('ajax-upload')
        })
        output = super(AjaxClearableFileInput, self).render(name, value, attrs)
        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        # If a file was uploaded or the clear checkbox was checked, use that.
        file = super(AjaxClearableFileInput, self).value_from_datadict(data, files, name)
        if file is not None:  # super class may return a file object, False, or None
            return file  # Default behaviour
        elif name in data:  # This means a file path was specified in the POST field
            file_path = data.get(name)
            if not file_path:
                return False  # False means clear the existing file
            elif file_path.startswith(settings.MEDIA_URL):
                # Strip and media url to determine the path relative to media root
                relative_path = file_path[len(settings.MEDIA_URL):]
                try:
                    uploaded_file = UploadedFile.objects.get(file=relative_path)
                except UploadedFile.DoesNotExist:
                    raise AjaxUploadException(u'%s %s' % (_('Invalid file path:'), relative_path))
                else:
                    return File(uploaded_file.file)
            else:
                # file might be in different location with different storage.
                pass 
                #raise AjaxUploadException(u'%s %s' % (_('File path not allowed:'), file_path))
        return None