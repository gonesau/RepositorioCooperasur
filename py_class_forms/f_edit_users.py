from py_class_forms.f_new_users import NewUser


class EditUser(NewUser):

    def __init__(self, *args, **kwargs):
        super(EditUser, self).__init__(*args, **kwargs)
        # Elimina el campo tmpPswd de la clase EditUser
        # delattr(self, 'tmpPswd')
        delattr(self, 'email')

# Ejemplo de uso:
# edit_user_form = EditUser()
# print(edit_user_form.tmpPswd)  # Esto generará un AttributeError ya que tmpPswd no existe en EditUser
