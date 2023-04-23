from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from ..models import role, user, city, state, country
from django.contrib import messages
import re


def checkloginpassword(password):
    if(password):
        pattern_upper = re.compile('[A-Z]')
        pattern_lower = re.compile('[a-z]')
        pattern_digit = re.compile('\d')
        pattern_special = re.compile('[!@#$%^&*()]')

        # Check that password meets minimum length
        if len(password) < 8:
            return "Password must be at least 8 characters long."

        # Check that password contains at least one uppercase letter
        if not pattern_upper.search(password):
            return "Password must contain at least one uppercase letter."

        # Check that password contains at least one lowercase letter
        if not pattern_lower.search(password):
            return "Password must contain at least one lowercase letter."

        # Check that password contains at least one digit
        if not pattern_digit.search(password):
            return "Password must contain at least one digit."

        # Check that password contains at least one special character
        if not pattern_special.search(password):
            return "Password must contain at least one special character (!@#$%^&*())."

    # If password passes all checks, return True

        return True
    else:
        return "Wrong password"