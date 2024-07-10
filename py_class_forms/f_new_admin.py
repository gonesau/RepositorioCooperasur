from flask_wtf.form import _Auto
from py_class_forms.f_new_users import NewUser


class NewAdmin(NewUser):
    def __init__(self, *args, **kwargs):
        super(NewAdmin, self).__init__(*args, **kwargs)
        delattr(self, 'institution')
        delattr(self, 'jobTitle')
        # delattr(self, 'email')
