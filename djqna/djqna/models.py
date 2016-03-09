from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Vote(models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    is_positive = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType) # Qestion or Answer
    object_id = models.PositiveIntegerField() # pk of Question or Answer
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = datetime.now()
        self.last_modified = datetime.now()

# TODO: add pinned class
# Allow moderators to pin votes and answers so they appear first in lists
#
# content_object (question or answer)
# user fk (person who pinned the object)
# order positiveintegerfield (order of pin in list of pins)
#
# Will also have to update model managers so that Pins show up first


class Question(models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey()
    text = models.TextField()

    up_votes = models.PositiveIntegerField()
    down_votes = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = datetime.now()
        self.last_modified = datetime.now()

        # TODO: queue rabbitmq to do this task
        # TODO: reduce queries by using annotate to get up and down vote counts
        self.up_votes = Vote.objects.filter(content_type=self, is_positive=True).count()
        self.down_votes = Vote.objects.filter(content_type=self, is_positive=False).count()


class Answer(models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey()
    text = models.TextField()

    up_votes = models.PositiveIntegerField()
    down_votes = models.PositiveIntegerField()

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = datetime.now()
        self.last_modified = datetime.now()

        # TODO: queue rabbitmq to do this task
        # TODO: reduce queries by using annotate to get up and down vote counts
        self.up_votes = Vote.objects.filter(content_type=self, is_positive=True).count()
        self.down_votes = Vote.objects.filter(content_type=self, is_positive=False).count()

