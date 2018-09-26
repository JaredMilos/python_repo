# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    wisher = models.ForeignKey(User, related_name = "wishes", on_delete=models.CASCADE)
    granted_flag = models.IntegerField()
    granted_at = models.DateTimeField(auto_now_add = True)
    likes_sum = models.IntegerField()
    liked_by = models.ManyToManyField(User, related_name = "likes")