import csv
import json

from connect import connect, create_table
# 1. Add a new contact

def add_contact():
    first_name = input("Enter first name: ").strip()
    phone = input("Enter phone number: ").strip()

    if not first_name or not phone:
        print("Name and phone cannot be empty!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO contacts (first_name, phone)
            VALUES (%s, %s)
            """,
            (first_name, phone)
        )

        conn.commit()
        print("Contact added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error adding contact:", e)

    finally:
        cur.close()
        conn.close()


# 2. Import contacts from CSV

def import_csv():
    filename = input("Enter CSV filename: ").strip()

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            conn = connect()
            cur = conn.cursor()

            try:
                for row in reader:
                    first_name = row.get("first_name", "").strip()
                    phone = row.get("phone", "").strip()

                    if first_name and phone:
                        cur.execute(
                            """
                            INSERT INTO contacts (first_name, phone)
                            VALUES (%s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (first_name, phone)
                        )

                conn.commit()
                print("CSV imported successfully!")

            except Exception as e:
                conn.rollback()
                print("Import error:", e)

            finally:
                cur.close()
                conn.close()

    except FileNotFoundError:
        print("File not found!")

    except Exception as e:
        print("Error:", e)


# 3. Update contact by ID

def update_contact():
    contact_id = input("Enter contact ID: ").strip()
    new_name = input("Enter new first name: ").strip()
    new_phone = input("Enter new phone: ").strip()

    if not contact_id.isdigit():
        print("ID must be a number!")
        return

    if not new_name or not new_phone:
        print("Name and phone cannot be empty!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE contacts
            SET first_name = %s, phone = %s
            WHERE id = %s
            RETURNING id
            """,
            (new_name, new_phone, int(contact_id))
        )

        result = cur.fetchone()
        conn.commit()

        if result:
            print("Contact updated successfully!")
        else:
            print("Contact not found.")

    except Exception as e:
        conn.rollback()
        print("Update error:", e)

    finally:
        cur.close()
        conn.close()


# 4. Search by name

def search_by_name():
    name = input("Enter first name: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT id, first_name, phone
            FROM contacts
            WHERE first_name ILIKE %s
            """,
            ("%" + name + "%",)
        )

        contacts = cur.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("No contacts found.")

    except Exception as e:
        print("Search error:", e)

    finally:
        cur.close()
        conn.close()


# 5. Search by phone prefix

def search_by_prefix():
    prefix = input("Enter phone prefix: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT id, first_name, phone
            FROM contacts
            WHERE phone LIKE %s
            """,
            (prefix + "%",)
        )

        contacts = cur.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("No contacts found.")

    except Exception as e:
        print("Search error:", e)

    finally:
        cur.close()
        conn.close()


# 6. Delete contact by ID

def delete_contact_by_id():
    contact_id = input("Enter contact ID: ").strip()

    if not contact_id.isdigit():
        print("ID must be a number!")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            DELETE FROM contacts
            WHERE id = %s
            RETURNING id
            """,
            (int(contact_id),)
        )

        result = cur.fetchone()
        conn.commit()

        if result:
            print("Contact deleted successfully!")
        else:
            print("Contact not found.")

    except Exception as e:
        conn.rollback()
        print("Delete error:", e)

    finally:
        cur.close()
        conn.close()


# 7. Show all contacts

def show_contacts():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT id, first_name, phone
            FROM contacts
            ORDER BY id
            """
        )

        contacts = cur.fetchall()

        if contacts:
            print("\n--- PHONEBOOK CONTACTS ---")

            for contact in contacts:
                print(
                    f"ID: {contact[0]}, "
                    f"Name: {contact[1]}, "
                    f"Phone: {contact[2]}"
                )
        else:
            print("PhoneBook is empty.")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# 8. Search by pattern using FUNCTION

def search_by_pattern():
    pattern = input("Enter name or phone pattern: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT *
            FROM get_contacts_by_pattern(%s)
            """,
            (pattern,)
        )

        contacts = cur.fetchall()

        if contacts:
            print("\n--- SEARCH RESULTS ---")

            for contact in contacts:
                print(contact)
        else:
            print("No contacts found.")

    except Exception as e:
        print("Search error:", e)

    finally:
        cur.close()
        conn.close()


# 9. Insert or update using PROCEDURE

def upsert_contact_python():
    name = input("Enter first name: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL upsert_contact(%s, %s)",
            (name, phone)
        )

        conn.commit()
        print("Contact inserted or updated successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# 10. Insert many contacts using PROCEDURE

def bulk_insert_contacts():
    try:
        count = int(input("How many contacts do you want to add? "))

        if count <= 0:
            print("Enter a positive number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    contacts = []

    for i in range(count):
        print(f"\nContact {i + 1}")

        name = input("Enter first name: ").strip()
        phone = input("Enter phone: ").strip()

        contacts.append({
            "first_name": name,
            "phone": phone
        })

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            CALL insert_many_contacts(
                %s::jsonb,
                %s::jsonb
            )
            """,
            (json.dumps(contacts), "[]")
        )

        result = cur.fetchone()
        conn.commit()

        invalid_contacts = result[0]

        if invalid_contacts:
            print("\n--- INCORRECT CONTACTS ---")

            for contact in invalid_contacts:
                print(contact)
        else:
            print("All contacts processed successfully!")

    except Exception as e:
        conn.rollback()
        print("Bulk insert error:", e)

    finally:
        cur.close()
        conn.close()


# 11. Pagination using FUNCTION

def show_contacts_paginated():
    try:
        page = int(input("Enter page number: "))
        limit = int(input("Contacts per page: "))

        if page < 1 or limit < 1:
            print("Page and limit must be positive.")
            return

        offset = (page - 1) * limit

        conn = connect()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                SELECT *
                FROM get_contacts_paginated(%s, %s)
                """,
                (limit, offset)
            )

            contacts = cur.fetchall()

            if contacts:
                print("\n--- CONTACTS ---")

                for contact in contacts:
                    print(contact)
            else:
                print("No contacts on this page.")

        finally:
            cur.close()
            conn.close()

    except ValueError:
        print("Please enter valid numbers.")

    except Exception as e:
        print("Pagination error:", e)


# 12. Delete by name or phone using PROCEDURE

def delete_by_name_or_phone():
    print("\n1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose option: ").strip()

    name = None
    phone = None

    if choice == "1":
        name = input("Enter first name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

    elif choice == "2":
        phone = input("Enter phone: ").strip()

        if not phone:
            print("Phone cannot be empty.")
            return

    else:
        print("Invalid choice.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL delete_contact(%s, %s)",
            (name, phone)
        )

        conn.commit()
        print("Delete operation completed!")

    except Exception as e:
        conn.rollback()
        print("Delete error:", e)

    finally:
        cur.close()
        conn.close()


def main():
    create_table()

    while True:

        print("\n========== PHONEBOOK ==========")

        print("1. Add contact")
        print("2. Import contacts from CSV")
        print("3. Update contact")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact by ID")
        print("7. Show all contacts")

    
        print("8. Search by pattern")
        print("9. Insert or update contact")
        print("10. Insert many contacts")
        print("11. Show contacts with pagination")
        print("12. Delete by name or phone")

        print("\n0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_contact()

        elif choice == "2":
            import_csv()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            search_by_name()

        elif choice == "5":
            search_by_prefix()

        elif choice == "6":
            delete_contact_by_id()

        elif choice == "7":
            show_contacts()

        elif choice == "8":
            search_by_pattern()

        elif choice == "9":
            upsert_contact_python()

        elif choice == "10":
            bulk_insert_contacts()

        elif choice == "11":
            show_contacts_paginated()

        elif choice == "12":
            delete_by_name_or_phone()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()