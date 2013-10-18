DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cv.sqlite', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}
INSTALLED_APPS = (
    'geo',
)
SECRET_KEY = '123'

DDF_VALIDATE_ARGS = True
DDF_DEBUG_MODE = True  # default = False
DDF_IGNORE_FIELDS = ['version', 'last_modified_user', 'last_modified_date', 'security_hash']
DDF_FILL_NULLABLE_FIELDS = True
DDF_DEFAULT_DATA_FIXTURE = 'geo.tests.ddf_fixture.DataFixture'  # static_sequential, random, sequential,
