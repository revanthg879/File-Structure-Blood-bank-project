import os
from datetime import datetime

DATA_FILE = "donors.txt"
INDEX_FILE = "donors_index.txt"
TEMP_INDEX_FILE = "temp_index.txt"
TEMP_DATA_FILE = "temp_donor.txt"
DELIMITER = "|"

if not os.path.exists(DATA_FILE):
    open(DATA_FILE, "w").close()

if not os.path.exists(INDEX_FILE):
    open(INDEX_FILE, "w").close()

# Function to validate donor ID (must be a four-digit integer)
def validate_donor_id(donor_id):
    if not donor_id.isdigit() or len(donor_id) != 4:
        print("⚠️Invalid donor ID. Donor ID must be a four-digit integer.")
        return False
    return True

# Function to validate donor age (must be an integer between 16 and 60)
def validate_donor_age(donor_age):
    if not donor_age.isdigit() or int(donor_age) < 16 or int(donor_age) > 60:
        print("⚠️Invalid donor age. Donor age must be between 16 and 60.")
        return False
    return True 

# Function to validate phone number (must be a 10-digit integer)
def validate_phone_number(phone_number):
    if not phone_number.isdigit() or len(phone_number) != 10:
        print("⚠️Invalid phone number. Phone number must be a 10-digit integer.")
        return False
    return True

# Function to validate blood group
def validate_blood_group(blood_group):
    valid_blood_groups = ['O+', 'A+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-']
    if blood_group not in valid_blood_groups:
        print("⚠️Invalid blood group. Please enter a valid blood group from the list: O+, A+, B+, AB+, A-, O-, B-, AB-")
        return False
    return True

# Function to validate the last donation date
def validate_last_donation_date(last_donation_date):
    date_formats = ["%d-%m-%Y", "%d/%m/%Y"]
    for date_format in date_formats:
        try:
            datetime.strptime(last_donation_date, date_format)
            return True
        except ValueError:
            continue
    print("⚠️Invalid last donation date. Please enter a valid date in the format DD-MM-YYYY or DD/MM/YYYY.")
    return False

# Function to add a new donor
def add_donor():
    donor_id = input("\nEnter donor ID: ")

    if not validate_donor_id(donor_id):
        return

    # Check if the donor ID already exists
    with open(INDEX_FILE, "r") as index_file:
        for line in index_file:
            existing_donor_id = line.strip().split(DELIMITER)[0]
            if donor_id == existing_donor_id:
                print("\n⚠️ Oops! Donor ID already exists.")
                print("Please enter a different ID.")
                return

    donor_name = input("Enter donor name: ")
    donor_address = input("Enter donor address: ")
    donor_age = input("Enter donor age: ")

    if not validate_donor_age(donor_age):
        return add_donor()  # Retry

    blood_group = input("Enter blood group: ")

    if not validate_blood_group(blood_group):
        return add_donor()  # Retry

    phone_number = input("Enter phone number: ")

    if not validate_phone_number(phone_number):
        return add_donor()  # Retry

    last_donation_date = input("Enter last donation date (DD-MM-YYYY): ")

    if not validate_last_donation_date(last_donation_date):
        return add_donor()  # Retry

    with open(DATA_FILE, "a") as data_file, open(INDEX_FILE, "a") as index_file:
        data_line = f"{donor_id}{DELIMITER}{donor_name}{DELIMITER}{donor_address}{DELIMITER}{donor_age}{DELIMITER}{blood_group}{DELIMITER}{phone_number}{DELIMITER}{last_donation_date}\n"
        data_file.write(data_line)

        # Write the index record with the byte offset
        byte_offset = data_file.tell()
        index_record = f"{donor_id}{DELIMITER}{byte_offset}\n"
        index_file.write(index_record)

    print("\n✅ Donor added successfully.")

# Function to display all donors
def display_donors():
    print("\n📋Donor List:\n")
    with open(DATA_FILE, "r") as data_file:
        for line in data_file:
            donor_data = line.strip().split(DELIMITER)
            print(f"Donor ID: {donor_data[0]}")
            print(f"Name: {donor_data[1]}")
            print(f"Address: {donor_data[2]}")
            print(f"Age: {donor_data[3]}")
            print(f"Blood Group: {donor_data[4]}")
            print(f"Phone Number: {donor_data[5]}")
            print(f"Last Donation Date: {donor_data[6]}")
            print("-" * 40)

# Function to delete a donor using donor ID
def delete_donor():
    donor_id = input("\nEnter the donor ID to delete: ")

    if not validate_donor_id(donor_id):
        return

    with open(INDEX_FILE, "r") as index_file:
        for line in index_file:
            record = line.strip().split(DELIMITER)
            if donor_id == record[0]:
                address = record[1]
                break
        else:
            print("\n⚠️ Oops! Donor ID not found.")
            return

    with open(DATA_FILE, "r") as data_file:
        for line in data_file:
            if line.strip().split(DELIMITER)[0] == donor_id:
                print("\n🔎 Donor information:")
                print(line)
                break

    confirm = input("Are you sure you want to delete this donor? (y/n): ")
    if confirm.lower() != "y":
        print("Deletion canceled.")
        return

    with open(DATA_FILE, "r") as data_file, open("temp_donor.txt", "w") as temp_file:
        for line in data_file:
            if line.strip().split(DELIMITER)[0] != donor_id:
                temp_file.write(line)

    # Replace the original data file with the temporary file
    os.remove(DATA_FILE)
    os.rename("temp_donor.txt", DATA_FILE)

    # Remove the donor's index from the index file
    with open(INDEX_FILE, "r") as index_file, open("temp_index.txt", "w") as temp_index_file:
        for line in index_file:
            if line.strip().split(DELIMITER)[0] != donor_id:
                temp_index_file.write(line)

    # Replace the original index file with the temporary index file
    os.remove(INDEX_FILE)
    os.rename("temp_index.txt", INDEX_FILE)

    print("\n🗑️ Donor deleted successfully.")


# Function to search for a donor by ID
def search_donor():
    donor_id = input("\nEnter the donor ID to search🔎 : ")

    if not validate_donor_id(donor_id):
        return

    found = False

    with open(DATA_FILE, "r") as data_file:
        for line in data_file:
            donor_data = line.strip().split(DELIMITER)
            if donor_id == donor_data[0]:
                print("\nDonor Found:")
                print(f"Donor ID: {donor_data[0]}")
                print(f"Name: {donor_data[1]}")
                print(f"Address: {donor_data[2]}")
                print(f"Age: {donor_data[3]}")
                print(f"Blood Group: {donor_data[4]}")
                print(f"Phone Number: {donor_data[5]}")
                print(f"Last Donation Date: {donor_data[6]}")
                found = True
                break

    if not found:
        print("\n❌ Donor not found.")

# Function to modify a donor record
def modify_donor():
    donor_id = input("\nEnter the donor ID to modify: ")

    if not validate_donor_id(donor_id):
        return

    with open(DATA_FILE, "r") as data_file, open(INDEX_FILE, "r") as index_file:
        with open(TEMP_DATA_FILE, "w") as temp_data_file, open(TEMP_INDEX_FILE, "w") as temp_index_file:
            for data_line, index_line in zip(data_file, index_file):
                data_record = data_line.strip().split(DELIMITER)
                index_record = index_line.strip().split(DELIMITER)

                if donor_id == data_record[0]:
                    print("\nCurrent donor information:")
                    print(data_line.strip())

                    # Get the modified donor information
                    donor_name = input("\nEnter new donor name (leave empty to retain current): ")
                    donor_address = input("Enter new donor address (leave empty to retain current): ")
                    donor_age = input("Enter new donor age (leave empty to retain current): ")
                    blood_group = input("Enter new blood group (leave empty to retain current): ")
                    phone_number = input("Enter new phone number (leave empty to retain current): ")
                    last_donation_date = input("Enter new last donation date (DD-MM-YYYY) (leave empty to retain current): ")

                    # Use the current values if the input is empty
                    donor_name = donor_name if donor_name else data_record[1]
                    donor_address = donor_address if donor_address else data_record[2]
                    donor_age = donor_age if donor_age else data_record[3]
                    blood_group = blood_group if blood_group else data_record[4]
                    phone_number = phone_number if phone_number else data_record[5]
                    last_donation_date = last_donation_date if last_donation_date else data_record[6]

                    if not validate_donor_age(donor_age):
                        return modify_donor()  # Retry

                    if not validate_blood_group(blood_group):
                        return modify_donor()  # Retry

                    if not validate_phone_number(phone_number):
                        return modify_donor()  # Retry

                    if not validate_last_donation_date(last_donation_date):
                        return modify_donor()  # Retry

                    # Write the modified data record
                    modified_data_line = f"{donor_id}{DELIMITER}{donor_name}{DELIMITER}{donor_address}{DELIMITER}{donor_age}{DELIMITER}{blood_group}{DELIMITER}{phone_number}{DELIMITER}{last_donation_date}\n"
                    temp_data_file.write(modified_data_line)

                    # Write the modified index record
                    byte_offset = temp_data_file.tell()
                    modified_index_record = f"{donor_id}{DELIMITER}{byte_offset}\n"
                    temp_index_file.write(modified_index_record)

                    print("\n✅ ✏️Donor information updated successfully.")

                else:
                    # Write the original data and index records
                    temp_data_file.write(data_line)
                    temp_index_file.write(index_line)

    # Replace the original data and index files with the modified files
    os.replace(TEMP_DATA_FILE, DATA_FILE)
    os.replace(TEMP_INDEX_FILE, INDEX_FILE)

# Main program loop
while True:
    print("\n Blood Bank Management System")
    print("-" * 40)
    print("1. Add New Donor")
    print("2. Display All Donors")
    print("3. Delete Donor Using Donor Id")
    print("4. Search Donor")
    print("5. Modify Donor")
    print("6. Exit")
    choice = input("\nEnter your choice (1-6): ")

    if choice == "1":
        add_donor()
    elif choice == "2":
        display_donors()
    elif choice == "3":
        delete_donor()
    elif choice == "4":
        search_donor()
    elif choice == "5":
        modify_donor()
    elif choice == "6":
        print("\nThank you for using the Donor Management System. Goodbye!")
        break
    else:
        print("\n⚠️Invalid choice. Please enter a number from 1 to 6.")