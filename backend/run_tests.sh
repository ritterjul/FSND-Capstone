#!/bin/bash
sh setup.sh

export TEST_DATABASE="swimresults_test"
export DATABASE_URL="postgresql://juliane:POSTGRES@localhost:5432/swimresults_test"

export TEST_CLIENT_ID='30hrvqHZauJPg6GGh3SmtAFVTZD1WZgZ'
export TEST_CLIENT_SECRET='4Zp4MMSAzKeVN23QWu7LoYDmPoOxfdIq8D11XAxSCq_fJZUtC3DS5zpO_Na_cRM6'

export TEST_SWIMMER_CLIENT_ID='NW7r74pqej3sUhVN3aY7c8QCCGBAXjA1'
export TEST_SWIMMER_CLIENT_SECRET='gvsMyOU7Yyq3UJsJhlRkcwo5kCvwORUKX29hV4HmoNzJgS6j4ydWH7DUhD9utyqz'

export TEST_COACH_CLIENT_ID='Lbt56KQvzZxzZofe02e567QEcFh6T2l9'
export TEST_COACH_CLIENT_SECRET='I_mQvPGt3QbSX4s8m6ivIPxxjQAKE6dvIUKqfBERs5b5i2xbjFSpxsJDdF_Fzfav'

export TEST_OFFICIAL_CLIENT_ID='oSfiJDvdc9gPP7MgEh7McgbKfOV5RTHv'
export TEST_OFFICIAL_CLIENT_SECRET='bJnqCP0MKLbxlSYdLPvi1WvvjwRx4GV2yUpWDjRfnu6Ge4lTJSZDQP61HOBxXLyE'

dropdb $TEST_DATABASE
createdb $TEST_DATABASE
python manage.py db upgrade
psql $TEST_DATABASE -c "INSERT INTO swimmers (id, gender, first_name, last_name, birth_year) VALUES (155849, 'F', 'Juliane', 'Ritter', 1994);"
psql $TEST_DATABASE -c "INSERT INTO swimmers (id, gender, first_name, last_name, birth_year) VALUES (155848, 'F', 'Stefanie', 'Kitschke', 1994);"
psql $TEST_DATABASE -c "INSERT INTO meets (id, name, start_date, end_date, city, country) VALUES (1, '7. Volvo-Lochner-Cup', '06.04.2003', '06.04.2003', 'Berlin', 'Germany');"
psql $TEST_DATABASE -c "INSERT INTO meets (id, name, start_date, end_date, city, country) VALUES (2, 'Weddinger Herbst-Pokal', '2004-10-23', '2004-10-23', 'Berlin', 'Germany');"
psql $TEST_DATABASE -c "INSERT into results VALUES (1, 155849, 1, 'LCM', 50, 'Free', '00:00:45.68');"
psql $TEST_DATABASE -c "INSERT into results VALUES (2, 155849, 1, 'LCM', 50, 'Breast', '00:00:50.25');"
psql $TEST_DATABASE -c "INSERT into results VALUES (3, 155849, 1, 'LCM', 50, 'Back', '00:00:48.41');"
psql $TEST_DATABASE -c "INSERT into results VALUES (4, 155848, 1, 'LCM', 50, 'Back', '00:00:47.50');"
psql $TEST_DATABASE -c "INSERT into results VALUES (5, 155848, 1, 'LCM', 50, 'Breast', '00:00:54.56');"
psql $TEST_DATABASE -c "INSERT into results VALUES (6, 155848, 1, 'LCM', 50, 'Free', '00:00:44.36');"
psql $TEST_DATABASE -c "INSERT into results VALUES (7, 155849, 2, 'SCM', 100, 'Breast', '00:01:41.03');"

python test.py

