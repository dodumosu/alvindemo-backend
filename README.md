# alvin-backend-demo
A demo API in Flask

This is a demo API using Flask. In the repository, there's a template settings file named `settings.ini-template`.
Make a copy of this to `settings.ini` in the same folder, and edit the settings you find therein.

There's also a `Procfile` (useful for environments like Heroku), although there's just one process defined in it.

You'll need a PostgreSQL server and a Redis server (for the rate limiting, although it isn't active). If using Heroku, activate the relevant addons.

Setup
Local: clone this repository and create a virtualenv using Python 3.10.x. Install dependencies using the command `pip install -r requirements.txt`. You might want to activate the virtualenv to make life easier. I know I do. Again, copy `settings.ini-template` to `settings.ini` and change the values as necessary.
Heroku: simply push to the `main` branch for your app. You don't need to copy the template settings file, but you *do* need to create environment variables with the same names and the relevant values (skip `DATABASE_URL` and `REDIS_URL` as they're provided automatically by Heroku when you add the Heroku Postgres and Heroku Redis addons).

Whether on Heroku or locally, you'll need to run the migrations to set up the database. Make sure your user has the right to create and alter tables.
Local: `FLASK_APP=wsgi.py flask db migrate`
Heroku (with the Heroku CLI installed): `heroku run FLASK_APP=wsgi.py flask db migrate`

Running the app:
Local: installing Honcho (a Foreman clone) makes things a snap. If it's installed in your virtualenv, simply run `honcho start` in the source folder. If not, the command under the `web` process in the `Procfile` is your friend.
Heroku: will start it up automatically.

Creating a user:
You need to create a user to play around with the app.
Local: run `FLASK_APP=wsgi.py flask users create email:<value> phone:<value>`
Heroku: just use the `heroku run` prefix with the same command.
You'll get prompted for the password.

Playing with the API
There are some categories from the last migration (it's a data migration, with some dummy data). The API doesn't have a way to create categories.

Endpoints
There's some (woefully incomplete) API documentation served up at `/doc/api-spec.json`. Should look good with maybe ReDoc or Swagger-UI.

Login endpoint: `/auth/login`, POST
Will return a 24H long access JWT bearer token.
Category list: `/categories/`
Will return the available categories.

Message push endpoint: `/messages/`, POST
Armed with your JWT bearer token (`Authorization: Bearer <token>` in headers), you can push a message using the parameters (please use a JSON body) `sender` (phone number) and `body`.
A valid text body is `Amount: USD 10.00 description: snacks`. The `amount:` and `description:` markers are important. The currency should match the one from your settings. So you'd POST something like:
```json
{
    "sender": "12345",
    "body": "amount: KES 15.00 description: savings for Valentine's"
}
```

Transaction list endpoint: `/transactions/`
Armed with your JWT bearer token, you can request transactions. You can optionally send as query parameters `start` and `end` (each optional, in `DD-MM-YYYY` format) to limit transactions.

Transaction aggregate endpoint: `/transactions/aggregate`
As above, but there's a required `operation` parameter, which is one of `count`, `average`, `total`, `min` or `max`.

Transaction update endpoint: `/transactions/<id>`, PUT
You can update the category of a transaction by providing a `category` JSON parameter, which can be either the id of a category or its name.
