SETUP
-----

1.  Clone the repository
2.  `pip install -r requirements/development.txt`
3.  Create an empty `site_media/uploads` folder in the project base directory
4.  `python manage.py development syncdb` and follow prompts
6.  `python manage.py development runserver`

The wiki and forums are the two main components I spent time on. There are also news articles with a threaded commenting system, a modified/cleaned up version of django-threadedcomments. 

You can create a news article in the admin at `/admin/` to check out the threaded commenting.

Wiki versioning is done using django-reversion, and the wiki history page allows you to generate a diff between version. Creating a new type of wiki model is as simple as creating a Wiki model subclass that simply inherits from the base Wiki model. Dynamic routing and views happen by introspecting the wiki models' class name.

You can create a wiki page for a game, as an example, by going to `/wiki/create/game/`.

If you have elasticsearch running and do `manage.py development update_index`, it will also do autocompletion in the search field with haystack.
