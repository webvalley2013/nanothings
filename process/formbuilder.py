# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     nanothings is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.

# MODULES
from time import time
from os.path import join as j
from django import forms
from django.core.files.base import ContentFile
import requests
from .validators import validate_url_list
from .storage import tmpfs
from nanothings.settings import DEFAULT_INPUT_PATH


class URLListField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_url_list]
        super(URLListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value == None:
            return None

        return value.split("||")


class FormFactory(object):
    def __init__(self, process):
        self.process = process

    def _get_field(self, type, label):
        form_fields = {
            'int': forms.IntegerField(required=False, label=label),
            'string': forms.CharField(required=False, label=label),
            #'image': forms.ImageField(required=True),
            'url_list': URLListField(required=True, label=label)
        }
        return form_fields.get(type, form_fields['string'])

    def _get_form_class(self, fields_dict):
        return type(self.process.code.encode('ascii', 'ignore'), (NanoForm,), fields_dict)

    def build_form(self):
        dct = {}
        for d in self.process.inputs:
            dct[d['name']] = self._get_field(d['type'],d['label'])

        dct['DIRNAME'] = str(int(time()*1000))
        return self._get_form_class(dct)


class NanoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NanoForm, self).__init__(*args, **kwargs)

    def get_url_data(self, name):
        urls = super(NanoForm, self).clean()[name]
        paths = []
        for i, url in enumerate(urls):
            req = requests.get(url)
            if req.status_code == 200:
                # For those of you who can't interpret python this takes the extension of the file and it's obvious
                extension = req.headers["content-type"].split(";")[0].split('/')[1].strip()
                data = ContentFile(req.content)
                actual_name = tmpfs.save(j(DEFAULT_INPUT_PATH, self.DIRNAME, 'file_{0}.{1}'.format(i, extension)), data)
                paths.append(actual_name)

        return paths

    def save(self):
        cleaned_data = super(NanoForm, self).clean()
        for name, field in self.fields.items():
            if isinstance(field, URLListField):
                cleaned_data[name] = self.get_url_data(name)

        return cleaned_data
