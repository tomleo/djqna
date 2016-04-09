from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.dispatch import receiver


class Vote(models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    user = models.ForeignKey(User, blank=True, null=True)  # Ensure this is not blank at the application level
    is_positive = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType)  # Qestion or Answer
    object_id = models.PositiveIntegerField()  # pk of Question or Answer
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


@receiver(post_save, sender=Vote)
def update_object_vote_counts(sender, **kwargs):
    """
    Update Object Vote Counts
    """
    # import pdb; pdb.set_trace()
    vote = kwargs.get('instance')
    obj = vote.content_object
    if vote.is_positive:
        obj.up_votes = obj.up_votes+1
    else:
        obj.down_votes = obj.down_votes+1
    obj.save(skip_vote_update=True)


# TODO: add pinned class
# Allow moderators to pin votes and answers so they appear first in lists
#
# content_object (question or answer)
# user fk (person who pinned the object)
# order positiveintegerfield (order of pin in list of pins)
#
# Will also have to update model managers so that Pins show up first

class ObjectWithVotesMixin(object):

    def update_vote_counts(self, save=True):
        self.up_votes = self.votes.filter(is_positive=True).count()
        self.down_votes = self.votes.filter(is_positive=False).count()
        if save:
            self.save()

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = timezone.now()
        self.last_modified = timezone.now()
        skip_vote_update = kwargs.pop('skip_vote_update', None)
        if not skip_vote_update:
            self.update_vote_counts(save=False)
        super(ObjectWithVotesMixin, self).save(*args, **kwargs)


class Question(ObjectWithVotesMixin, models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    text = models.TextField()
    votes = GenericRelation(Vote)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.title


class Answer(ObjectWithVotesMixin, models.Model):
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    text = models.TextField()
    question = models.ForeignKey(Question, blank=True, null=True)
    votes = GenericRelation(Vote)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s' % self.title
