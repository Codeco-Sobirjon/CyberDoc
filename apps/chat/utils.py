

def custom_user_has_student_role(user):
    return user.groups.filter(name='Студент').exists()


def custom_user_has_author_role(user):
    return user.groups.filter(name='Автор').exists()
