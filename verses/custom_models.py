from django.db import models

class Text (models.TextField):
    def db_type(self, connection):
        return 'TEXT'

    def rel_db_type(self, connection):
        return 'TEXT'