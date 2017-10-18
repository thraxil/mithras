from smoketest import SmokeTest
from django.contrib.auth.models import User
from .check_migrations import migrations_have_applied


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = User.objects.all().count()
        # all we care about is not getting an exception
        self.assertTrue(cnt > -1)

    def test_migrations(self):
        self.assertTrue(migrations_have_applied())
