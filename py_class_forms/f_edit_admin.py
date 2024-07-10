from py_class_forms.f_new_users import NewUser


class EditAdmin(NewUser):
    def __init__(self, *args, **kwargs):
        super(EditAdmin, self).__init__(*args, **kwargs)
        delattr(self, 'email')
        delattr(self, 'institution')
        delattr(self, 'jobTitle')
        # self.name.label = "Nombre administrador"
