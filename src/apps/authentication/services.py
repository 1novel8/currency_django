from apps.authentication.exceptions import EmailAlreadyInUse
from apps.user.models import User


class AuthenticationService:
    def create_user(self, email: str, username: str, password: str) -> None:
        if not self.is_email_free(email=email):
            raise EmailAlreadyInUse()
        User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

    def is_email_free(self, email: str) -> bool:
        return User.objects.filter(email=email).count() == 0
