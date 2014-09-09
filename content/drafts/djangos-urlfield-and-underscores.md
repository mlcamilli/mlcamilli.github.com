Title: Django's URLField and Underscores
Date: 2014-08-27
Category:Django 
Tags:django,urlfield,validator,regex
Slug: django's-urlfield-and-underscores
Author: Matt Camilli
Description: 


A week ago The Engine Room was faced with a problem. A customer was trying to
add a blog to our system with a subdomain that had an underscore in it. While
a frowned upon convention(as domains cannot have underscores) it is still
a valid url. The problem arose because Django's default URLField does not allow
any underscores, and threw ValidationErrors upon saves. After finding the
[Django Issue](https://code.djangoproject.com/ticket/18517) addressing this
bug, we found out that it is intentional and that the project will not be
fixing it as URLFields abide by official rules (RFC 1034/1035). 

While this is all well and dandy we still needed the ability to add blog urls
with underscores in their subdomains. The solution was to implement our own
URLField, which would be identical to Django's with the exception of a more
fine tuned validator. 

```python
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit
import re


class BetterURLValidator(RegexValidator):
    """
    This validator allows underscores within the subdomains of URLS
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)?'  # subdomain...
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.))|' # domain
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    message = _('Enter a valid URL')

    def __call__(self, value):
        try:
            super(BetterURLValidator, self).__call__(value)
        except ValidationError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                value = force_text(value)
                scheme, netloc, path, query, fragment = urlsplit(value)
                try:
                    netloc = netloc.encode('idna').decode('ascii')  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(BetterURLValidator, self).__call__(url)
            else:
                raise
        else:
            url = value
```



```python
from django.db import models
from .validators import BetterURLValidator


class BetterURLField(models.URLField):
    """
    This field allows underscores in the subdomains of URLS
    """
    default_validators = [BetterURLValidator()]

    def __init__(self, verbose_name=None, name=None, **kwargs):
        super(BetterURLField, self).__init__(verbose_name, name, **kwargs)
```
