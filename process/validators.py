from django.core import validators

def validate_url_list(url_list):
    for url in url_list:
        validators.URLValidator()(url)
