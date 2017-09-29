from django.db import models
from django.conf import settings

# Create your models here.
class RobinhoodUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    token = ""
    """
    for token consider this property approach to make the token setting stick
    @property
    def title(self):
        return self._title
    def save( self, *args, **kw  ):
        try:
            self._title
        except AttributeError:
            self._title= defaultdict()
        super( Category, self ).save( *args, **kw )
    """
    def __str__(self):
        return self.username