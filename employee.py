import mysql.connector


class Employee:
    def __init__(self, emp_id, first_name, last_name, position, salary, username, password, phone_number):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.salary = salary
        self.username = username
        self.password = password
        self.phone_number = phone_number


class Database:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(host="localhost", user="root", password="232003", database="employee")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            position VARCHAR(50),
            salary DECIMAL(10, 2),
            username VARCHAR(50),
            password VARCHAR(50),
            phone_number VARCHAR(20)
        )
        """
        employee_login_table_query = """
           CREATE TABLE IF NOT EXISTS employee_login (
               id INT AUTO_INCREMENT PRIMARY KEY,
               username VARCHAR(50) UNIQUE,
               password VARCHAR(50)
           )
           """
        self.cursor.execute(query)
        self.cursor.execute(employee_login_table_query)
        self.conn.commit()

    def employee_register(self, employee):
        existing_employee = self.display_employee()
        employee_ids = [e.emp_id for e in existing_employee]

        if employee.emp_id in employee_ids:
            print("Employee with ID " + str(employee.emp_id) + " already exists. Update or use a different ID.")
        else:
            query = "INSERT INTO employees (emp_id, first_name, last_name, position, salary, username, password, " \
                    "phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                employee.emp_id,
                employee.first_name,
                employee.last_name,
                employee.position,
                employee.salary,
                employee.username,
                employee.password,
                employee.phone_number
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Employee added successfully!")

    def display_employee(self):
        query = "SELECT emp_id, first_name, last_name, position, salary, phone_number FROM employees"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        employees = []
        for result in results:
            emp_id, first_name, last_name, position, salary, phone_number = result
            employee = Employee(emp_id, first_name, last_name, position, salary, "", "", phone_number)
            employees.append(employee)

        return employees

    def update_employee_details(self, emp_id):
        query = "SELECT emp_id, first_name, last_name, position, salary, password, phone_number FROM employees " \
                "WHERE emp_id = %s"
        self.cursor.execute(query, (emp_id,))
        result = self.cursor.fetchone()
        if result:
            emp_id, first_name, last_name, position, salary, password, phone_number = result
            return Employee(emp_id, first_name, last_name, position, salary, "", password, phone_number)
        else:
            return None

    def update_employee(self, employee):
        existing_employee = self.update_employee_details(employee.emp_id)
        if existing_employee:
            query = """
            UPDATE employees
            SET first_name = %s, last_name = %s, position = %s, salary = %s, username = %s, password = %s, 
                phone_number = %s 
            WHERE emp_id = %s
            """
            values = (
                employee.first_name,
                employee.last_name,
                employee.position,
                employee.salary,
                employee.username,
                employee.password,
                employee.phone_number,
                employee.emp_id
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Employee details updated successfully!")
        else:
            print("No employee found with ID " + str(employee.emp_id) + ". Update aborted.")

    def delete_employee(self, emp_id):
        existing_employee = self.display_employee()
        employee_ids = [employee.emp_id for employee in existing_employee]

        if emp_id in employee_ids:
            query = "DELETE FROM employees WHERE emp_id = %s"
            self.cursor.execute(query, (emp_id,))
            self.conn.commit()
            print("Employee with ID " + str(emp_id) + " has been deleted.")
        else:
            print("No employee found with ID " + str(emp_id) + ". Deletion aborted.")

    def employee_login(self, username, password):
        query = "SELECT emp_id, password FROM employees WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            employee_id = result[0]
            return employee_id
        else:
            return None


def main():
    db = Database(host="localhost", user="username", password="password", database="employee")

    while True:
        print("EMPLOYEE MANAGEMENT SYSTEM")
        print("1. Employee Register  2.Employee login   3. Admin Login   4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            emp_id = int(input("Enter Employee ID: "))
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            position = input("Enter Position: ")
            salary = float(input("Enter Salary: "))
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            phone_number = input("Enter Phone Number: ")

            new_employee = Employee(emp_id, first_name, last_name, position, salary, username, password, phone_number)
            db.employee_register(new_employee)
            print("Employee added successfully!")

        elif choice == "2":
            print("Employee Login")

            username = input("Enter your username: ")
            password = input("Enter your password: ")

            employee_id = db.employee_login(username, password)

            if employee_id:
                print("Employee ID", employee_id, "Welcome")
                existing_employee = db.update_employee_details(employee_id)
                while True:
                    print("1. Update My Details  2. Logout")
                    employee_choice = input("Enter your choice: ")

                    if employee_choice == "1":
                        existing_employee = db.update_employee_details(employee_id)
                        if existing_employee:
                            print("Updating details for Employee ID: " + str(existing_employee.emp_id))
                            first_name = input("Enter First Name : ")
                            last_name = input("Enter Last Name : ")
                            username = input("Enter Username :")
                            password = input("Enter Password:")
                            phone_number = input("Enter Phone Number: ")

                            updated_employee = Employee(employee_id, first_name, last_name, existing_employee.position,
                                                        existing_employee.salary, username, password, phone_number)
                            db.update_employee(updated_employee)
                            print("Employee details updated successfully!")
                        else:
                            print("No employee found with ID " + str(employee_id) + ". Update aborted.")
                    elif employee_choice == "2":
                        print("Logging out...")
                        break

                    else:
                        print("Invalid choice. Please select a valid option.")
            else:
                print("Invalid username or password.")

        elif choice == "3":
            print("Admin Login")
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if username == "hr" and password == "1234":
                print("Welcome HR")
                while True:
                    print("EMPLOYEE MANAGEMENT SYSTEM")
                    print("1.Update Employee 2. Delete Employee   3. Display Employees   4. Exit")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        emp_id_to_update = int(input("Enter Employee ID to update: "))
                        existing_employee = db.update_employee_details(emp_id_to_update)

                        if existing_employee:
                            print("Updating details for Employee ID: " + str(existing_employee.emp_id))
                            first_name = input("Enter First Name (" + existing_employee.first_name + "): ")
                            last_name = input("Enter Last Name (" + existing_employee.last_name + "): ")
                            position = input("Enter Position (" + existing_employee.position + "): ")
                            salary = input("Enter Salary (" + str(existing_employee.salary) + "): ")
                            phone_number = input("Enter Phone Number (" + existing_employee.phone_number + "): ")

                            if password == "":
                                password = existing_employee.password

                            updated_employee = Employee(emp_id_to_update, first_name, last_name, position, salary,
                                                        existing_employee.username, password, phone_number)
                            db.update_employee(updated_employee)
                            print("Employee details updated successfully!")
                        else:
                            print("No employee found with ID " + str(emp_id_to_update) + ". Update aborted.")
                            
                    elif choice == "2":
                        emp_id_to_delete = int(input("Enter Employee ID to delete: "))
                        db.delete_employee(emp_id_to_delete)

                    elif choice == "3":
                        employees = db.display_employee()
                        if employees:
                            print("Employee Information:")
                            for employee in employees:
                                print("ID: " + str(employee.emp_id))
                                print("First Name: " + employee.first_name)
                                print("Last Name: " + employee.last_name)
                                print("Position: " + employee.position)
                                print("Salary: " + str(employee.salary))
                                print("Phone Number: " + employee.phone_number)
                                print("------------")
                        else:
                            print("No employees found.")

                    elif choice == "4":
                        print("Exiting...")
                        break

                    else:
                        print("Invalid choice. Please select a valid option.")
            else:
                print("Invalid username or password.")
        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")


main()
