# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from models import *

import bcrypt

from datetime import datetime

from django.contrib import messages

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
 
def index(request):
    return render(request, "index.html")

def register(request):
    message_flag = 0

    if len(request.POST['first_name']) < 1:
        message_flag = 1
        messages.error(request, 'First Name field cannot be blank', extra_tags="first_name")
    elif len(request.POST['first_name']) == 1:
        message_flag = 1
        messages.error(request, 'First Name must be two or more characters', extra_tags="first_name")

    if len(request.POST['last_name']) < 1:
        message_flag = 1
        messages.error(request, 'Last Name field cannot be blank', extra_tags="last_name")
    elif len(request.POST['last_name']) == 1:
        message_flag = 1
        messages.error(request, 'Last Name must be two or more characters', extra_tags="last_name")

    if len(request.POST['email']) < 1:
        message_flag = 1
        messages.error(request, 'Email field cannot be blank', extra_tags="email")
    elif not EMAIL_REGEX.match(request.POST['email']):
        message_flag = 1
        messages.error(request, 'Email must be in email format', extra_tags="email")
    elif User.objects.filter(email__iexact=request.POST['email']).exists():
        message_flag = 1
        messages.error(request, 'This email is already registered', extra_tags="email")

    if len(request.POST['password']) < 1:
        message_flag = 1
        messages.error(request, 'Password field cannot be blank', extra_tags="password")
    elif len(request.POST['password']) < 8:
        message_flag = 1
        messages.error(request, 'Password must be 8 or more characters', extra_tags="password")

    if request.POST['password'] != request.POST['confirm_password']:
        message_flag = 1
        messages.error(request, 'Password confirmation does not match', extra_tags="password_confirm")

    if message_flag == 0:
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'].lower(), password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['log_reg_flag'] = 0
        request.session['first_name'] = request.POST['first_name']
        request.session['logged_in'] = True
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect("/wishes")
    else:
        return redirect("/")

def login(request):
    message_flag = 0
    if len(request.POST['email']) < 1:
        message_flag = 1
        messages.error(request, 'Email field cannot be blank', extra_tags="log_email")
    
    if len(request.POST['password']) < 1:
        message_flag = 1
        messages.error(request, 'Password field cannot be blank', extra_tags="log_password")

    if message_flag == 0:
        if User.objects.filter(email__iexact=request.POST['email']).exists():
            user = User.objects.get(email=request.POST['email'].lower())
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
                request.session['log_reg_flag'] = 1
                request.session['logged_in'] = True
                request.session['user_id'] = User.objects.get(email=request.POST['email']).id
                return redirect("/wishes")
            else:
                messages.error(request, 'Email and Password combo does not match', extra_tags="log_email")
                return redirect("/")
        else:
            messages.error(request, 'Email and Password combo does not match', extra_tags="log_email")
            return redirect("/")
    else:
        return redirect("/")

def wishes(request):
    if 'logged_in' not in request.session:
        return redirect("/")
    else:
        overall_granteds = Wish.objects.filter(granted_flag = 1).order_by('-granted_at')
        for wish in overall_granteds:
            if len(wish.liked_by.filter(id = request.session['user_id'])):
                wish.already_liked = True
            else:
                wish.already_liked = False
        context = {
            'user_wishes': Wish.objects.filter(wisher=request.session['user_id'], granted_flag=0).order_by("-created_at"),
            'wishes': Wish.objects.filter(granted_flag=1).order_by("-created_at"),
            'overall_granteds': overall_granteds
        }
        return render(request, "dashboard.html", context)

def make_wish(request):
    if 'logged_in' not in request.session:
        return redirect("/")
    else:
        return render(request, "make_wish.html")

def edit_wish(request, wid):
    if 'logged_in' not in request.session:
        return redirect("/")
    else:
        request.session['wish_item'] = Wish.objects.get(id=wid).item
        request.session['wish_desc'] = Wish.objects.get(id=wid).desc
        request.session['wish_id'] = Wish.objects.get(id=wid).id
        return render(request, "edit_wish.html")

def wish(request):
    message_flag = 0
    if len(request.POST['wish']) < 3:
        message_flag = 1
        messages.error(request, 'A wish must consist of at least 3 characters!', extra_tags="wish")
    
    if len(request.POST['desc']) < 1:
        message_flag = 1
        messages.error(request, 'A description must be provided!', extra_tags="desc")
    
    if message_flag == 0:
        user = User.objects.get(id=request.session['user_id'])
        print(user.id)
        Wish.objects.create(item=request.POST['wish'], desc=request.POST['desc'], wisher=user, granted_flag=0, likes_sum=0)
        request.session['logged_in'] = True
        return redirect("/wishes")
    else:
        return redirect("/make_wish")

def update(request, wid):
    message_flag = 0
    if len(request.POST['item']) < 3:
        message_flag = 1
        messages.error(request, 'A wish must consist of at least 3 characters!', extra_tags="wish")
    
    if len(request.POST['desc']) < 1:
        message_flag = 1
        messages.error(request, 'A description must be provided!', extra_tags="desc")
    
    if message_flag == 0:
        b = Wish.objects.get(id=wid)
        b.item=request.POST['item']
        b.desc=request.POST['desc']
        b.save()
        request.session['logged_in'] = True
        return redirect("/wishes")
    else:
        return redirect("/"+wid+"/edit_wish")

def destroy(request, wid):
    b = Wish.objects.get(id=wid)
    b.delete()
    return redirect("/wishes")

def granted(request, wid):
    b = Wish.objects.get(id=wid)
    b.granted_flag = 1
    b.granted_at = datetime.now()
    b.save()
    return redirect("/wishes")

def like(request, wid):
    user = User.objects.get(id=request.session['user_id'])
    b = Wish.objects.get(id=wid)
    b.liked_by.add(user)
    b.save()
    b.likes_sum = b.liked_by.count()
    b.save()
    return redirect("/wishes")

def stats(request):
    if 'logged_in' not in request.session:
        return redirect("/")
    else:
        request.session['granted_sum'] = Wish.objects.filter(granted_flag=1).count() 
        request.session['granted_wishes'] = Wish.objects.filter(wisher=request.session['user_id'], granted_flag=1).count() 
        request.session['pending_wishes'] = Wish.objects.filter(wisher=request.session['user_id'], granted_flag=0).count() 
        return render(request, "stats.html")

def logout(request):
    request.session.flush()
    return redirect("/")
