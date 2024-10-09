class EmailValidationRouter:
    """
    A router to control all database operations on models in the
    email_validation application.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'email_validation':
            return 'email_validation'  # SQLite database name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'email_validation':
            return 'email_validation'  # SQLite database name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'email_validation' or obj2._meta.app_label == 'email_validation':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'email_validation' if app_label == 'email_validation' else None
