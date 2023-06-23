from apps.core.utilities import generate_slug
from apps.user.models import User


def get_system_user() -> User:
    user_random_data = generate_slug(
        model=User,
        search_field='username',
        length=8
    )
    system_user_data = dict(
        username=user_random_data,
        first_name=user_random_data,
        last_name=user_random_data,
        email=f'{user_random_data}@mail.com'
    )
    sys_user, _ = User.objects.get_or_create(
        id=99999942,
        defaults=system_user_data
    )

    return sys_user
