import csv
from connect import connect


def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    print("Contact added!")

    cur.close()
    conn.close()


def import_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    print("CSV imported successfully!")

    cur.close()
    conn.close()


def update_contact():
    name = input("Enter the current name: ")

    print("1. Update name")
    print("2. Update phone")

    choice = input("Choose what to update: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        new_name = input("Enter the new name: ")

        cur.execute(
            "UPDATE contacts SET name = %s WHERE name = %s",
            (new_name, name)
        )

    elif choice == "2":
        new_phone = input("Enter the new phone: ")

        cur.execute(
            "UPDATE contacts SET phone = %s WHERE name = %s",
            (new_phone, name)
        )

    else:
        print("Invalid choice")

    conn.commit()

    print("Contact updated!")

    cur.close()
    conn.close()

def search_contacts():
    print("1. Search by name")
    print("2. Search by phone prefix")

    choice = input("Choose search type: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")

        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s",
            ("%" + name + "%",)
        )

    elif choice == "2":
        prefix = input("Enter phone prefix: ")

        cur.execute(
            "SELECT * FROM contacts WHERE phone LIKE %s",
            (prefix + "%",)
        )

    else:
        print("Invalid choice")
        cur.close()
        conn.close()
        return

    results = cur.fetchall()

    for contact in results:
        print(contact)

    cur.close()
    conn.close()

def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose delete type: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")

        cur.execute(
            "DELETE FROM contacts WHERE name = %s",
            (name,)
        )

    elif choice == "2":
        phone = input("Enter phone: ")

        cur.execute(
            "DELETE FROM contacts WHERE phone = %s",
            (phone,)
        )

    else:
        print("Invalid choice")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("Contact deleted!")

    cur.close()
    conn.close()

def main():
    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Import contacts from CSV")
        print("2. Add contact")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            import_csv()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()