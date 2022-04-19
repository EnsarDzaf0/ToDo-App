from django.db import models
from django.contrib.auth.models import User #user model od djanga

class Task(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # ako se user delete-a da izbrise sve taskove od usera
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  #string representation of the model
        return self.title

    class Meta:     #redanje po value od complete
        ordering = ['complete']
