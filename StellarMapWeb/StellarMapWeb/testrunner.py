from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """
    TestRunner that skips the creation and destruction of the test databases.
    This is useful if you have a custom database setup and don't want to use the test databases.
    """
    def setup_databases(self, **kwargs):
        """
        Overrides the default behavior of creating test databases.
        """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """
        Overrides the default behavior of destroying test databases.
        """
        pass
