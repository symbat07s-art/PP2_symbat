# TSIS 1 — Extended PhoneBook Management

## Files
- `schema.sql` — creates groups and phones tables and extends contacts.
- `functions.sql` — search, group filter, and pagination functions.
- `procedures.sql` — add-phone and move-to-group procedures.
- `phonebook.py` — console application.
- `connect.py` and `config.py` — PostgreSQL connection settings.
- `contacts.csv` — example CSV format.

## Setup
1. Install the Python package if needed:
   `pip install psycopg2-binary`
2. Open `config.py` and replace `YOUR_PASSWORD` with your PostgreSQL password.
3. Open pgAdmin and select the same `phonebook` database used for Practice 8.
4. Run `schema.sql`.
5. Run `functions.sql`.
6. Run `procedures.sql`.
7. Run the program from this folder:
   `python phonebook.py`

## CSV columns
The CSV header must be:
`name,email,birthday,group,phone,phone_type`

Birthday format: `YYYY-MM-DD`.
Phone type must be: `home`, `work`, or `mobile`.

The old `contacts.phone` column is kept for compatibility with Practice 8. Its existing values are copied to the new `phones` table as mobile numbers.
