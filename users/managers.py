import six
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

import datetime
import time

#
# def conf_code_generator(user, timestamp):
#     return (
#             six.text_type(user.pk) + six.text_type(timestamp) +
#             six.text_type(user.email)
#     )
#
#
# user = User.objects.get(id=1)
#
# dt = datetime.datetime.now()
# timestamp = time.mktime(dt.timetuple())


from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # return {
    #     'token': str(refresh.access_token)
    # }
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }