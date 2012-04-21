# Proto

## Setup

First...

1. Install distribute: `curl http://python-distribute.org/distribute_setup.py | python`
2. Install pip: `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python`
3. Install virtualenvwrapper by following these instructions: <http://www.doughellmann.com/docs/virtualenvwrapper/#introduction>

Then...

1. Clone the repository: `git clone git@github.com:sdornan/proto.git`
2. Install the requirements: `pip install -r requirements/development.txt`
3. Create an empty `site_media/uploads` folder in the project base directory
4. Create the database: `python manage.py development syncdb` and follow the prompts
5. Run the development server: `python manage.py development runserver`

## Details

The wiki and forums are the two main components I spent time on. There are also news articles with a threaded commenting system, a modified/cleaned up version of django-threadedcomments. 

You can create a news article in the admin at `/admin/` to check out the threaded commenting.

Wiki versioning is done using django-reversion, and the wiki history page allows you to generate a diff between version. Creating a new type of wiki model is as simple as creating a Wiki model subclass that inherits from the base Wiki model. In this case, `games` is the app that contains the Wiki object subclasses. Dynamic routing and views happen by introspecting the wiki models' class name. Wiki objects use a base template in the `wiki` app, unless an overriding template exists in the same app as the Wiki model subclass.

You can create a wiki page for a game, as an example, by going to `/wiki/create/game/`. You can view then view all of the Wiki objects at `/wiki/`, or of particular type at `/wiki/game/` for example.

If you have Elasticsearch running (install with `brew install elasticsearch`) and do `manage.py development update_index`, it will handle autocompletion in the site's search field using Haystack.

It has a fully functioning API using Tastypie. You can access the list of model endpoints at `/api/v1/?format=json`.

## Sharing Apps Between Sites

Each of the folders in the `proto/` directory are Django apps. Installing an app to a site is as simple as appending the app to the list named `INSTALLED_APPS` in the settings file. They don't have to be in the project folder; they could also live in separate repositories and be installed via pip like the third-party packages listed in the requirements files.

Base templates for apps are in each app's `templates/` directory. These can be overridden at the site level by putting a file in the base `templates/` directory with the same name and relative path as the base template that you want to override. This also works for image, CSS and Javascript files, which are in the `static/` directory.

For example, if you want to override the forums app's `forums_list.html` template (`/proto/forums/templates/forums_list.html`) at the site level, you would put the overriding template in the site's template directory. In proto's case, this would be `/templates/forums/forums_list.html`.

You could also extend any of the models and views, or reroute URLs, contained in the apps at the site level.