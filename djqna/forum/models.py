from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Vote(models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    user = models.ForeignKey(User, blank=True, null=True) # Ensure this is not blank at the application level
    is_positive = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType) # Qestion or Answer
    object_id = models.PositiveIntegerField() # pk of Question or Answer
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        super(Vote, self).save(*args, **kwargs)

    def to_string(self):
        return u"%s for %s" % ("+1" if self.is_positive else "-1", self.user.get_full_name())

    def __unicode__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()

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
    user = models.ForeignKey(User)
    text = models.TextField()
    votes = GenericRelation(Vote)
    up_votes = models.PositiveIntegerField(editable=False, default=0)
    down_votes = models.PositiveIntegerField(editable=False, default=0)

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        self.up_votes = self.votes.filter(is_positive=True).count()
        self.down_votes = self.votes.filter(is_positive=False).count()
        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    text = models.TextField()
    votes = GenericRelation(Vote)
    up_votes = models.PositiveIntegerField(editable=False, default=0)
    down_votes = models.PositiveIntegerField(editable=False, default=0)

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        self.up_votes = self.votes.filter(is_positive=True).count()
        self.down_votes = self.votes.filter(is_positive=False).count()
        super(Answer, self).save(*args, **kwargs)

