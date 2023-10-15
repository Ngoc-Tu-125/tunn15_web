ALTER DATABASE tunn15_web OWNER TO tunn15;
GRANT ALL PRIVILEGES ON DATABASE tunn15_web TO tunn15;
GRANT ALL ON SCHEMA public TO tunn15;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tunn15;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tunn15;



Error when createsuperuser:
"""
django.db.utils.ProgrammingError: column web_app_customuser.id does not exist
LINE 1: SELECT "web_app_customuser"."id", "web_app_customuser"."pass...
"""

ALTER TABLE web_app_customuser ADD COLUMN id SERIAL PRIMARY KEY;
UPDATE web_app_customuser SET id = nextval('web_app_customuser_id_seq');




python manage.py migrate web_app 0007_previous_migration_name --fake

Delete Migration Files:
Once you've faked the migration, navigate to the migrations folder inside your app's directory (web_app/migrations/)
and delete the migration file(s) related to TechBlogPost that are causing issues.

python manage.py makemigrations
python manage.py migrate








SET client_encoding = 'UTF8';
SELECT * FROM web_app_homepagecontent;
