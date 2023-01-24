from django.conf import settings

class DatabaseAppsRouter(object):
    """
    A router class that routes database operations for certain apps to a specified database
    as defined in settings.DATABASE_APPS_MAPPING. If an app is not in the DATABASE_APPS_MAPPING,
    it falls back to the 'default' database.
    """

    def db_for_read(self, model, **hints):
        """
        Point all read operations to the specific database.
        """
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Points all write operations to the specific database.
        """
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between apps involved in the same database.
        """
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True

