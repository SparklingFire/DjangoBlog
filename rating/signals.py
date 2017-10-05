from custom_user.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import (transaction, IntegrityError)
from django.db.models.signals import (post_save, pre_delete)
from django.dispatch import receiver
from articles.models import Article
from comments.models import Comment
from .models import (UserRatingModel, RatingModel)
from .models import (Vote)


@receiver(post_save, sender=Article)
@receiver(post_save, sender=Comment)
def create_rating_model(sender, instance, **kwargs):
    RatingModel.objects.create(content_object=instance, user_rating_model=instance.author.userratingmodel)


@receiver(post_save, sender=RatingModel)
@receiver(pre_delete, sender=Vote)
@receiver(pre_delete, sender=Article)
@receiver(pre_delete, sender=Comment)
def update_user_rating(sender, instance, **kwargs):
    try:
        if sender in (Article, Comment):
            try:
                instance.get_rating_model().user_rating_model.calculate_score()
            except AttributeError:
                pass

        elif sender == Vote:
            try:
                instance.rating_model.user_rating_model.calculate_score()
            except AttributeError:
                pass
        else:
            try:
                instance.user_rating_model.calculate_score()
            except AttributeError:
                pass
    except ObjectDoesNotExist:
        pass


@receiver(post_save, sender=CustomUser)
def create_user_rating_model(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            UserRatingModel.objects.create(user=instance)
    except IntegrityError:
        pass
