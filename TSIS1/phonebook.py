
import psycopg2
import config
import csv
import json


def connect():
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )


# 1. Search contacts by name, email or phone
def search_contacts():
    text = input("Enter name, email or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (text,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 2. Filter contacts by group
def filter_by_group():
    group = input("Enter group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filter_contacts_by_group(%s)", (group,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# 3. Add another phone to a contact
def add_phone():
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    phone_type = input("Enter phone type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (name, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()


# 4. Move contact to a group
def move_to_group():
    name = input("Enter contact name: ")
    group = input("Enter group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()


# 5. Show contacts with pagination and sorting
def show_contacts():
    page = 0
    limit = 2

    while True:
        print("\nSort by: name, birthday, date_added")
        sort = input("Enter sorting option: ").lower().strip()

        if sort not in ["name", "birthday", "date_added"]:
            sort = "name"

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_page(%s, %s, %s)",
            (limit, page * limit, sort)
        )

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
        conn.close()

        choice = input("Next / Previous / Quit: ").lower().strip()

        if choice == "next":
            page += 1
        elif choice == "previous":
            if page > 0:
                page -= 1
        elif choice == "quit":
            break


# 6. Export all contacts to JSON
def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email, birthday, group_id FROM contacts")
    contacts = cur.fetchall()

    data = []

    for contact in contacts:
        contact_id = contact[0]

        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s",
            (contact_id,)
        )
        phones = cur.fetchall()

        cur.execute(
            "SELECT name FROM groups WHERE id = %s",
            (contact[4],)
        )
        group = cur.fetchone()

        data.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,
            "group": group[0] if group else "Other",
            "phones": [
                {"phone": p[0], "type": p[1]} for p in phones
            ]
        })

    with open("contacts.json", "w") as file:
        json.dump(data, file, indent=4)

    cur.close()
    conn.close()

    print("Contacts exported successfully")


# 7. Import contacts from JSON
def import_json():
    with open("contacts.json", "r") as file:
        data = json.load(file)

    conn = connect()
    cur = conn.cursor()

    for contact in data:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            answer = input(
                name + " already exists. Overwrite? (yes/no): "
            )

            if answer.lower() != "yes":
                continue

            contact_id = existing[0]

            cur.execute(
                "DELETE FROM phones WHERE contact_id = %s",
                (contact_id,)
            )
        else:
            contact_id = None

        group_name = contact.get("group", "Other")

        cur.execute(
            "SELECT id FROM groups WHERE name = %s",
            (group_name,)
        )
        group = cur.fetchone()

        if group:
            group_id = group[0]
        else:
            cur.execute(
                "INSERT INTO groups (name) VALUES (%s) RETURNING id",
                (group_name,)
            )
            group_id = cur.fetchone()[0]

        phones = contact.get("phones", [])
        first_phone = phones[0]["phone"] if phones else ""

        if existing:
            cur.execute("""
                UPDATE contacts
                SET phone = %s, email = %s,
                    birthday = %s, group_id = %s
                WHERE id = %s
            """, (
                first_phone,
                contact.get("email"),
                contact.get("birthday"),
                group_id,
                contact_id
            ))
        else:
            cur.execute("""
                INSERT INTO contacts
                (name, phone, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                name,
                first_phone,
                contact.get("email"),
                contact.get("birthday"),
                group_id
            ))
            contact_id = cur.fetchone()[0]

        for p in phones:
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, p["phone"], p["type"]))

    conn.commit()
    cur.close()
    conn.close()

    print("JSON import completed")


# 8. Import contacts from CSV
def import_csv():
    with open("contacts.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        print("Columns:", reader.fieldnames)

        rows = list(reader)
        print("Number of rows:", len(rows))

        for row in rows:
            print("Contact:", row)

        conn = connect()
        cur = conn.cursor()

        for row in rows:
            name = row["name"]
            phone = row["phone"]
            phone_type = row["type"]
            group_name = row["group"]

            cur.execute(
                "SELECT id FROM groups WHERE name = %s",
                (group_name,)
            )
            group = cur.fetchone()

            if group:
                group_id = group[0]
            else:
                cur.execute(
                    "INSERT INTO groups (name) VALUES (%s) RETURNING id",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]

            cur.execute(
                "SELECT id FROM contacts WHERE name = %s",
                (name,)
            )
            contact = cur.fetchone()

            if contact:
                contact_id = contact[0]
                cur.execute("""
                    UPDATE contacts
                    SET phone = %s, email = %s,
                        birthday = %s, group_id = %s
                    WHERE id = %s
                """, (
                    phone, row["email"], row["birthday"],
                    group_id, contact_id
                ))
            else:
                cur.execute("""
                    INSERT INTO contacts
                    (name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    name, phone, row["email"],
                    row["birthday"], group_id
                ))
                contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO NOTHING
            """, (contact_id, phone, phone_type))

        conn.commit()
        cur.close()
        conn.close()

    print("CSV import completed")

# Main menu
def menu():
    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Search contacts")
        print("2. Filter by group")
        print("3. Add phone")
        print("4. Move to group")
        print("5. Show contacts")
        print("6. Export JSON")
        print("7. Import JSON")
        print("8. Import CSV")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            add_phone()
        elif choice == "4":
            move_to_group()
        elif choice == "5":
            show_contacts()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            import_csv()
        elif choice == "0":
            break
        else:
            print("Invalid option")


menu()
