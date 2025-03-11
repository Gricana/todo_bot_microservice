import hashlib
import time

from django.db import models


class HashAutoField(models.CharField):
    """
    The custom field of the model that generates a unique hash as a primary key.
    Used to automatically create unique values of the primary key.

    Attributes:
        - Blank: The value can be empty.
        - Unique: The value should be unique.
        - Primary_key: This field is the primary key.
    """

    def __init__(self, *args, **kwargs):
        """
        Field initialization.
        """
        kwargs['blank'] = True
        kwargs['unique'] = True
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Generates a hash-meaning before preserving the object of the model.

        Parameters:
            Model_instance (Models.model): A copy of the model to which the field is attached.
            Add (Bool): a flag indicating that the object is added to the database.

        Returns:
            STR: Hesh value for the primary key.
        """
        value = getattr(model_instance, self.attname)
        if not value and add:
            value = self.generate_pk(model_instance)
            setattr(model_instance, self.attname, value)
        return value

    @staticmethod
    def generate_pk(instance):
        """
        Generates a unique hash for the primary key.

        Parameters:
            Instance (Models.model): A copy of the model for which the key is generated.

        Returns:
            STR: a unique hash consisting of 36 characters.
        """
        pk_template = f"{instance.__class__.__name__}_{time.time()}"
        return hashlib.sha256(pk_template.encode()).hexdigest()[:36]
