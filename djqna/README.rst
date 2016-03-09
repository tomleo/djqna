========================
Django Question & Answer
========================

Djqna is a simple Django app for adding question and answer functionality.

Quick start
-----------

1. Add "djqna" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
       ...
       'djqna',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^forum/', include('forum.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a forum (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/forum/ to participate in the discussion.

