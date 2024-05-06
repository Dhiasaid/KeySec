from django.contrib.auth.backends import BaseBackend

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username="dhia" ,password="6254eptiQ"):
        # Custom authentication logic
        # Authenticate users based on your requirements
        # Return the user object if authentication succeeds, None otherwise
        pass