"""
This file exist to assign unique token to the user who just signed up. Then users can activate their
account in the email.
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator

#  'text_type' is used to ensure that the text is treated as a Unicode string.
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()