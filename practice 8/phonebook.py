import json
from connect import connect


def search_by_pattern():
    pattern = input("Enter part of a name or phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM get_contacts_by_pattern(%s)",
            (pattern,)
        )

        contacts = cur.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("No contacts found.")

    except Exception as e:
        conn.rollback()
        print("Search error:", e)

    finally:
        cur.close()
        conn.close()


def upsert_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL upsert_contact(%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact inserted or updated successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def insert_many_contacts():
    try:
        count = int(input("How many contacts do you want to enter? "))
        if count <= 0:
            print("Enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    contacts = []

    for i in range(count):
        print(f"Contact {i + 1}")
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()

        contacts.append({
            "name": name,
            "phone": phone
        })

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL insert_many_contacts(%s::jsonb, %s::jsonb)",
            (json.dumps(contacts), "[]")
        )

        result = cur.fetchone()
        conn.commit()

        invalid_contacts = result[0]

        if invalid_contacts:
            print("\nIncorrect contacts:")
            for contact in invalid_contacts:
                print(contact)
        else:
            print("All contacts were processed successfully.")

    except Exception as e:
        conn.rollback()
        print("Bulk insert error:", e)

    finally:
        cur.close()
        conn.close()


def show_contacts_paginated():
    try:
        page = int(input("Page number: "))
        limit = int(input("Contacts per page (1-100): "))

        if page < 1 or limit < 1:
            print("Page and limit must be positive.")
            return

        offset = (page - 1) * limit

    except ValueError:
        print("Please enter valid numbers.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        contacts = cur.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("No contacts on this page.")

    except Exception as e:
        conn.rollback()
        print("Pagination error:", e)

    finally:
        cur.close()
        conn.close()


def delete_by_name_or_phone():
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose: ").strip()

    name = None
    phone = None

    if choice == "1":
        name = input("Enter name: ").strip()
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
        print("Delete procedure executed.")

    except Exception as e:
        conn.rollback()
        print("Delete error:", e)

    finally:
        cur.close()
        conn.close()


def main():
    while True:
        print("\n===== PHONEBOOK - PRACTICE 8 =====")
        print("1. Search by pattern (FUNCTION)")
        print("2. Insert or update one contact (PROCEDURE)")
        print("3. Insert many contacts (PROCEDURE)")
        print("4. Show contacts with pagination (FUNCTION)")
        print("5. Delete by name or phone (PROCEDURE)")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            search_by_pattern()
        elif choice == "2":
            upsert_contact()
        elif choice == "3":
            insert_many_contacts()
        elif choice == "4":
            show_contacts_paginated()
        elif choice == "5":
            delete_by_name_or_phone()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
