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

