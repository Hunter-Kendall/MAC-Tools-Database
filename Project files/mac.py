import scanner
import mysql.connector

import pandas as pd
from datetime import date
from datetime import datetime as dt
import datetime
import xml.etree.ElementTree as xtree

scan = scanner.Scan()
inventory_sheet = pd.DataFrame(columns=['Toolnumber', 'Quantity'])


def open_database():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "Hunter",
        password = "EthoxySM2636" )
    cur = conn.cursor()
    cur.execute("USE MAC_tools")
    return conn



def create_customer(fname, lname, comp, addr, city, state, zipcode, phone, email = None, fax = None ):
    conn = open_database()
    cur = conn.cursor()
    cur.execute("SELECT count(customerid) FROM Customer")
    customerid = cur.fetchone()[0] + 1
    cur.execute("SELECT count(paymentid) FROM Payments")
    paymentid = cur.fetchone()[0] + 1

    cur.execute(f"INSERT INTO Customer VALUES ('{customerid}', '{fname}', '{lname}', '{comp}', '{addr}', '{city}', '{state}', '{zipcode}','{phone}', %s, %s)", (fax, email, ))
    cur.execute(f"INSERT INTO Payments VALUES ('{customerid}', {0.00}, '{paymentid}', NULL)")

    conn.commit()
    conn.close()


    print("Added customer:", customerid, fname, lname, comp, addr, city, state, zipcode, phone)
def itter(crt):
    total = 0.0
    for t, q, p in crt:
        total += float(p) * float(q)

    return total

def purchase(tools, qty, customerid):
    conn = open_database()
    cur = conn.cursor()
    price = []
    for i in tools:
        s = "SELECT unitprice FROM Tool WHERE toolnumber = %s "
        tn = (i,)
        cur.execute(s, tn)

        price.append(cur.fetchone()[0])

    cart = zip(tools, qty, price)
    cart = list(cart)


    cur.execute("SELECT COUNT(invoiceid) FROM Invoice")
    invoiceid = cur.fetchone()[0] + 1
    total = itter(cart)
    billinfo = "SELECT address, city, state, postalcode FROM Customer WHERE customerid = %s"
    cid = (customerid,)
    cur.execute(billinfo, cid)
    d = cur.fetchone()

    cur.execute(f"INSERT INTO Invoice VALUES ({invoiceid},'{customerid}', '{date.today()}', '{d[0]}', '{d[1]}', '{d[2]}', '{d[3]}', {total})")

    for t, q, p in cart:
        cur.execute(f"INSERT INTO InvoiceLine VALUES (NULL, {invoiceid}, '{t}', {q}, {p * q})")

        quantity = "SELECT onhand FROM Tool WHERE toolnumber = %s"
        tnum = (t,)
        cur.execute(quantity, tnum)
        qty = cur.fetchone()
        upd_q = qty[0] - q

        upd = f"UPDATE tool SET onhand = {upd_q} WHERE toolnumber = '{t}'"
        cur.execute(upd)

    cur.execute(f"SELECT amountowed FROM payments where paymentid = {customerid}")
    owed = float(cur.fetchone()[0])


    cur.execute(f"UPDATE Payments SET amountowed = {total + owed} WHERE customerid = '{customerid}'")
    conn.commit()
    conn.close()
    print("Purchase Complete!")




def payment( customerid, amountpayed: float, d_time = dt.now()):

    conn = open_database()
    cur = conn.cursor(buffered=True)
    cur.execute(f"SELECT paymentid FROM payments WHERE customerid = '{customerid}'")
    paymentid = cur.fetchone()[0]
    #print("pay:", paymentid)
    cur.execute(f"INSERT INTO Paymentlog VALUES ('{paymentid}', '{d_time}', {amountpayed})")
    cur.execute(f"SELECT amountowed FROM Payments NATURAL JOIN Paymentlog WHERE paymentid = '{paymentid}'")
    current_amount = cur.fetchone()[0]

    #print("float:", float(current_amount), amountpayed)
    updated_amount = round(float(current_amount) - amountpayed, 2)
    #print(updated_amount)
    date1 = date.today()
    nextpay = date1 + datetime.timedelta(days=14)
    #print(nextpay)

    cur.execute(f"UPDATE Payments SET amountowed = {updated_amount}, nextpayment = '{nextpay}' WHERE customerid = '{customerid}'")
    print(f"Paid: {amountpayed}, {updated_amount} left in account." )
    conn.commit()
    conn.close()

def add_tool(toolnum: str, name: str, qty: int, price: float):
    conn = open_database()
    cur = conn.cursor()
    scaner = input("Would you like to scan? [y/n]:").upper()
    if scaner == "Y":
        bc = scan.main()
    else:
        bc = None
    cur.execute(f"INSERT INTO Tool VALUES ('{toolnum}', '{name}', {qty}, %s, {price})", (bc,))
    print("Added:", toolnum)
    conn.commit()
    conn.close()

def add_shipment(file:str):
    conn = open_database()
    cur = conn.cursor()
    f = open(file)
    for record in f:
        toolnum, desc, qty, bc, price = record.split(",")
        toolnum = str(toolnum)
        desc = str(desc)
        qty = int(qty)
        if bc == "NULL":
            bc = None
        else:
            bc = str(bc)
        price = float(price)
        print("Inserted:", toolnum, desc, qty, bc, price)
        cur.execute(f"INSERT INTO Tool VALUES ('{toolnum}', '{desc}', {qty}, %s, {price})", (bc,))

    f.close()
    conn.commit()
    conn.close()
def takeinventory_tn(toolnum: str, qty: int):
    global inventory_sheet
    inventory_sheet = inventory_sheet.append({'Toolnumber': toolnum, 'Quantity': qty}, ignore_index = True)
    print("Current Inventory Sheet:")
    print(inventory_sheet)
def takeinventory_bc(qty: int):
    conn = open_database()
    cur = conn.cursor()
    bc = scan.main()
    cur.execute(f"SELECT toolnumber FROM Tool Where barcode = '{bc}'")
    tn = cur.fetchone()[0]
    global inventory_sheet
    inventory_sheet = inventory_sheet.append({'Toolnumber': tn, 'Quantity': qty}, ignore_index=True)
    print("Current Inventory Sheet:")
    print(inventory_sheet)
def commit_inventory():
    conn = open_database()
    cur = conn.cursor(buffered=True)
    global inventory_sheet
    for idx, row in inventory_sheet.iterrows():
        cur.execute(f"SELECT toolnumber FROM Tool WHERE toolnumber = '{row['Toolnumber']}'")


        if cur.rowcount == 1:
            cur.execute(f"UPDATE Tool SET onhand = {row['Quantity']} WHERE toolnumber = '{row['Toolnumber']}'")
            print("Inventory taken.")
        else:
            print(f"{row['Toolnumber']} is not in MAC_Tools database.")
    conn.commit()
    inventory_sheet = pd.DataFrame(columns=['Toolnumber', 'Quantity'])
    conn.close()



def export_employee_data(filename, company):
    # Finds each of the specifed data of customers of companies
    # and creates an XML file with the information about all of them.
    conn = open_database()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Customer WHERE company = %s", (company, ))
    res = cur.fetchall()
    if len(res) > 0:
        # Create the empty Document
        root = xtree.Element(f"{company}")


        cur.execute("SELECT Customer.customerid, firstname, lastname, amountowed, nextpayment FROM Customer LEFT JOIN Payments ON Customer.customerid = Payments.customerid WHERE company = %s ORDER BY Customer.firstname", (company, ) )
        data = cur.fetchall()
        for i in data:
            root.append(employeeElement(i))
        # Create tree from the document
        tree = xtree.ElementTree(root)
        # Write XML file
        with open(filename, "wb") as xmlFile:
            tree.write(xmlFile)
        print(filename, "written...")
    else:
        print("Company does not exist")
    conn.close()
def employeeElement(data):
    element = xtree.Element("Employee")
    tag = xtree.SubElement(element, "customerid")
    tag.text = data[0]
    tag = xtree.SubElement(element, "first_name")
    tag.text = str(data[1])
    tag = xtree.SubElement(element, "Last_Name")
    tag.text = str(data[2])
    tag = xtree.SubElement(element, "amount_owed")
    tag.text = str(data[3])
    tag = xtree.SubElement(element, "Next_payment")
    tag.text = str(data[4])

    return element

def allcustomerspayments():
    conn = open_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM AllCustomerPayments")
        names = [x[0] for x in cur.description]
        rows = cur.fetchall()
        pd.set_option('display.max_columns', None)
        return print(pd.DataFrame(rows, columns=names))
    finally:
        if cur is not None:
            cur.close()



def company_list(company:str):
    conn = open_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT Customer.customerid, firstname, lastname, address, amountowed, nextpayment FROM Customer LEFT JOIN Payments ON Customer.customerid = Payments.customerid WHERE company = %s ORDER BY Customer.firstname", (company, ))
        names = [x[0] for x in cur.description]
        rows = cur.fetchall()
        pd.set_option('display.max_columns', None)
        return print(pd.DataFrame(rows, columns=names))
    finally:
        if cur is not None:
            cur.close()
def customerlog(customerid: str):
    conn = open_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT customerid, lastpayed, amount  FROM Paymentlog NATURAL JOIN Payments WHERE customerid = %s", (customerid, ))
        names = [x[0] for x in cur.description]
        rows = cur.fetchall()
        pd.set_option('display.max_columns', None)
        return print(pd.DataFrame(rows, columns=names))
    finally:
        if cur is not None:
            cur.close()
def invoice():
    conn = open_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM Invoice")
        names = [x[0] for x in cur.description]
        rows = cur.fetchall()
        pd.set_option('display.max_columns', None)
        return print(pd.DataFrame(rows, columns=names))
    finally:
        if cur is not None:
            cur.close()

def onhand():
    conn = open_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT toolnumber, name, onhand, unitprice FROM Tool WHERE onhand > 0")
        names = [x[0] for x in cur.description]
        rows = cur.fetchall()
        pd.set_option('display.max_columns', None)
        return print(pd.DataFrame(rows, columns=names))
    finally:
        if cur is not None:
            cur.close()



#Create_customer("Hunter", "Kendall","mac", "31 Saunders Lane", "Gillett", "PA", "16925", "570-529-1593" )
#Add_shipment("shipment.csv")
#Add_shipment("tools.csv")
#purchase(['CC3', 'CHP4LT'], [1, 2], 1)
#Payment(1, 15.90)
#Purchase(['CC3', 'CHP4LT'], [1, 2], 2)
#Payment(2, 17.00)

#Add_tool("sd6", "6in screw driver", 3, 25.99)

#Takeinventory_tn('SD6"C-O', 5)
#Takeinventory_tn('ABC', 5)
#Takeinventory_bc('0885911532143', 3)

#commit_inventory()

#export_employee_data('mac', 'mac')

#allcustomerspayments()
#company_list('mac')
#customerlog('1')
#invoice()
#onhand()
def print_options():
    print(" ")

    print(" ")
    print("  C - Create customer" )
    print("  A - Load new tools" )
    print("  T - Take on hand inventory" )
    print("  E - Export company information" )
    print("  P - Payment" )
    print("  O - Purchase")
    print("  V - Data Tables")
    print("  X - Exit" )
    print(" ")
def load_options():
    print("  S - Add shipment")
    print("  T - Add single tool")
def inventory_options():
    print("  B - Barcode scan")
    print("  T - Tool number")
    print("  C - Commit New inventory")
def view_options():
    print("  A - All customer payments")
    print("  E - List of customers at a company")
    print("  L - Payment log for customer")
    print("  I - Invoices")
    print("  O - Current on hand inventory")

def main():
    print()
    print( "MAC Tools Distributor DBMS")
    print()

    while True:
        print_options()
        option = input( "Option: ").upper()
        if option == "C":
            fname = input("First Name:")
            lname = input("Last Name:")
            comp = input("Company:")
            addr = input("Address:")
            city = input("City:")
            state = input("State:")
            zipcode = input("Zip:")
            phone = input("Phone Number:")
            fax = input("Fax (NONE if none):")
            if fax == "NONE":
                fax = None
            email = input("Email (NONE if none):")
            if email == "NONE":
                email = None
            create_customer(fname, lname, comp, addr, city, state, zipcode, phone, fax, email)
        elif option == "A":
            load_options()
            type = input( "Option: ").upper()
            if type == "S":
                file = input("File directory:")
                add_shipment(file)
            elif type == "T":
                tn = str(input("Tool Number:")).upper()
                name = input("Tool Name:").upper()
                qty = int(input("Quantity:"))
                price = float(input("Price:"))
                add_tool(tn, name, qty, price)
            else:
                print( "Invalid option")

        elif option == "T":
            inventory_options()
            type_a = input("Option:").upper()
            if type_a == "B":

                qty = int(input("Quantity on hand:"))
                takeinventory_bc(qty)
            elif type_a == "T":
                tn_ = str(input("Tool Number:").upper())
                qty_ = int(input("Quantity on hand:"))
                takeinventory_tn(tn_, qty_)
            elif type_a == "C":
                commit_inventory()
            else:
                print("Invalid Option")
        elif option == "E":
            fn = input("File name: " )
            company_ = input( "Company:" )
            export_employee_data( fn, company_ )

        elif option == "P":
            customerid = str(input("Customer ID:"))
            amount = float(input("Amount Payed (2 decimal places):"))
            payment(customerid, amount)

        elif option == "O":
            # try block to handle the exception

            tools = []
            amount = []
            cid = str(input("Customer ID:"))
            while True:
                inp = str(input("Enter Tool Numbers (Type STOP when done):").upper())
                if inp != "STOP":
                    tools.append(inp)
                    amount.append(int(input("Quantity:")))
                else:
                    break

            # if the input is not-integer
            purchase(tools, amount, cid)

        elif option == "V":
            view_options()
            type_b = input("Option:").upper()
            if type_b == "A":
                allcustomerspayments()
            elif type_b == "E":
                company = input("Company:")
                company_list(company)
            elif type_b == "L":
                c = str(input("Customer ID:"))
                customerlog(c)
            elif type_b == "I":
                invoice()
            elif type_b == "O":
                onhand()
            else:
                print("Invalid Option")

        elif option == "X":
            break
        else:
            print("Invalid Option")
            print_options()
    print("Program exit!")
    print()

if __name__ == "__main__":
    main()
