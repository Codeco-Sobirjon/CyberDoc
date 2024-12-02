

def custom_user_has_student_role(user):
    return user.groups.filter(id=2).exists()


def custom_user_has_author_role(user):
    return user.groups.filter(id=1).exists()
