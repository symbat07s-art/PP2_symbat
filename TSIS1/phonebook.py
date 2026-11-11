import csv
import json
from connect import connect


def get_group_id(cur, group_name):
    if not group_name:
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact(name, email, birthday, group_name, phone_list):
    conn = connect()
    cur = conn.cursor()

    try:
        group_id = get_group_id(cur, group_name)
        first_phone = phone_list[0]["phone"] if phone_list else ""

        cur.execute(
            """
            INSERT INTO contacts (name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (name, first_phone, email or None, birthday or None, group_id)
        )
        contact_id = cur.fetchone()[0]

        for item in phone_list:
            cur.execute(
                """
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO NOTHING
                """,
                (contact_id, item["phone"], item.get("type", "mobile"))
            )

        conn.commit()
        print("Contact added.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def search_contacts():
    query = input("Enter name, email, or phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts found.")

    except Exception as error:
        conn.rollback()
        print("Search error:", error)

    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group_name = input("Enter group name: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM filter_contacts_by_group(%s)",
            (group_name,)
        )
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts in this group.")

    except Exception as error:
        conn.rollback()
        print("Filter error:", error)

    finally:
        cur.close()
        conn.close()


def sort_contacts():
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")
    choice = input("Sort by: ").strip()

    sort_options = {
        "1": "c.name",
        "2": "c.birthday",
        "3": "c.date_added"
    }

    if choice not in sort_options:
        print("Invalid choice.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY """ + sort_options[choice]
        )

        rows = cur.fetchall()
        for row in rows:
            print(row)

    except Exception as error:
        conn.rollback()
        print("Sort error:", error)

    finally:
        cur.close()
        conn.close()


def show_contacts_paginated():
    try:
        limit = int(input("Contacts per page: "))
        if limit < 1:
            print("Enter a positive number.")
            return
    except ValueError:
        print("Enter a valid number.")
        return

    page = 0

    while True:
        conn = connect()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, page * limit)
            )
            rows = cur.fetchall()

            print("\nPage", page + 1)
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No contacts on this page.")

        except Exception as error:
            conn.rollback()
            print("Pagination error:", error)
            cur.close()
            conn.close()
            return

        cur.close()
        conn.close()

        print("\nN - next page | P - previous page | Q - quit")
        choice = input("Choose: ").strip().lower()

        if choice == "n":
            if rows:
                page += 1
            else:
                print("There are no more contacts.")
        elif choice == "p":
            if page > 0:
                page -= 1
            else:
                print("This is the first page.")
        elif choice == "q":
            break
        else:
            print("Invalid choice.")


def add_phone():
    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    phone_type = input("Type (home/work/mobile): ").strip().lower()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def move_to_group():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
        conn.commit()
        print("Contact moved.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        cur.close()
        conn.close()


def export_json():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.id
            """
        )
        contacts = cur.fetchall()
        result = []

        for contact in contacts:
            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s",
                (contact[0],)
            )
            phone_rows = cur.fetchall()

            result.append({
                "name": contact[1],
                "email": contact[2],
                "birthday": str(contact[3]) if contact[3] else None,
                "group": contact[4],
                "date_added": str(contact[5]) if contact[5] else None,
                "phones": [
                    {"phone": phone[0], "type": phone[1]}
                    for phone in phone_rows
                ]
            })

        with open("contacts_export.json", "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

        print("Exported to contacts_export.json.")

    except Exception as error:
        print("Export error:", error)

    finally:
        cur.close()
        conn.close()


def import_json():
    filename = input("JSON file name: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)
    except Exception as error:
        print("File error:", error)
        return

    conn = connect()
    cur = conn.cursor()

    try:
        for item in contacts:
            name = item.get("name", "").strip()
            if not name:
                continue

            cur.execute(
                "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s) LIMIT 1",
                (name,)
            )
            existing = cur.fetchone()

            if existing:
                choice = input(
                    name + " already exists. Skip or overwrite? (s/o): "
                ).strip().lower()

                if choice == "s":
                    continue
                elif choice == "o":
                    contact_id = existing[0]
                    group_id = get_group_id(cur, item.get("group"))
                    phone_list = item.get("phones", [])
                    first_phone = phone_list[0]["phone"] if phone_list else ""

                    cur.execute(
                        """
                        UPDATE contacts
                        SET phone = %s, email = %s, birthday = %s, group_id = %s
                        WHERE id = %s
                        """,
                        (
                            first_phone,
                            item.get("email"),
                            item.get("birthday"),
                            group_id,
                            contact_id
                        )
                    )
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
                else:
                    print("Skipped:", name)
                    continue
            else:
                group_id = get_group_id(cur, item.get("group"))
                phone_list = item.get("phones", [])
                first_phone = phone_list[0]["phone"] if phone_list else ""

                cur.execute(
                    """
                    INSERT INTO contacts (name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        name,
                        first_phone,
                        item.get("email"),
                        item.get("birthday"),
                        group_id
                    )
                )
                contact_id = cur.fetchone()[0]
                phone_list = item.get("phones", [])

            for phone_item in phone_list:
                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone) DO NOTHING
                    """,
                    (
                        contact_id,
                        phone_item["phone"],
                        phone_item.get("type", "mobile")
                    )
                )

        conn.commit()
        print("JSON import completed.")

    except Exception as error:
        conn.rollback()
        print("Import error:", error)

    finally:
        cur.close()
        conn.close()


def import_csv():
    filename = input("CSV file name: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row.get("name", "").strip()
                if not name:
                    continue

                group_id = get_group_id(cur, row.get("group", "Other"))
                phone = row.get("phone", "").strip()
                phone_type = row.get("phone_type", "mobile").strip().lower()

                cur.execute(
                    """
                    INSERT INTO contacts (name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        name,
                        phone,
                        row.get("email") or None,
                        row.get("birthday") or None,
                        group_id
                    )
                )
                contact_id = cur.fetchone()[0]

                if phone:
                    cur.execute(
                        """
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (contact_id, phone) DO NOTHING
                        """,
                        (contact_id, phone, phone_type)
                    )

        conn.commit()
        print("CSV import completed.")

    except Exception as error:
        conn.rollback()
        print("CSV import error:", error)

    finally:
        cur.close()
        conn.close()


def main():
    while True:
        print("\n===== TSIS 1 PHONEBOOK =====")
        print("1. Search contacts")
        print("2. Filter by group")
        print("3. Sort contacts")
        print("4. Show contacts with pages")
        print("5. Add phone number")
        print("6. Move contact to group")
        print("7. Import CSV")
        print("8. Export JSON")
        print("9. Import JSON")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            search_contacts()
        elif choice == "2":
            filter_by_group()
        elif choice == "3":
            sort_contacts()
        elif choice == "4":
            show_contacts_paginated()
        elif choice == "5":
            add_phone()
        elif choice == "6":
            move_to_group()
        elif choice == "7":
            import_csv()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
