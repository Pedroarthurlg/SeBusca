import os
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image
from tag.models import Tag
from recipes.models import Recipe

class LeilaoManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=False
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id')


class Leilao(models.Model):
    objects = LeilaoManager()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    valor = models.IntegerField(verbose_name=_('Prazo'))
    
    freelancer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.SET_NULL, null=True
    )
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        leilao_from_db = leilao.objects.filter(
            title__iexact=self.title
        ).first()

        if leilao_from_db:
            if leilao_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('leilao')
        verbose_name_plural = _('leiloes')
