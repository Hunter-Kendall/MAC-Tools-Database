import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host = "localhost",
    user = "Hunter",
    password = "EthoxySM2636" )
print(conn)

print("2) Create a cursor")
c = conn.cursor()
print(c)
print("3) Select the database to use")
c.execute("DROP DATABASE  MAC_Tools")
c.execute("CREATE DATABASE MAC_Tools")
c.execute("USE MAC_Tools")
print(c)
c.execute("DROP TABLE IF EXISTS Tool")
c.execute("DROP TABLE IF EXISTS InvoiceLine")
c.execute("DROP TABLE IF EXISTS Invoice")
c.execute("DROP TABLE IF EXISTS Customer")
c.execute("DROP TABLE IF EXISTS Payments")
c.execute("DROP TABLE IF EXISTS Paymentlog")

c.execute('''CREATE TABLE Tool
             (toolnumber VARCHAR(15) NOT NULL, 
             name VARCHAR(100) NOT NULL,
             onhand INT NOT NULL CHECK(onhand >= 0),
             barcode VARCHAR(20),
             unitprice DECIMAL(6, 2),
             PRIMARY KEY(toolnumber))''')

c.execute('''CREATE INDEX idx_tool ON Tool (toolnumber)''')

c.execute('''CREATE TABLE Customer
             (customerid VARCHAR(4) NOT NULL,
             firstname VARCHAR(25) NOT NULL, 
             lastname VARCHAR(25) NOT NULL, 
             company VARCHAR(25) NOT NULL,
             address VARCHAR(32) NOT NULL,
             city VARCHAR(32) NOT NULL,
             state CHAR(2) NOT NULL,
             postalcode VARCHAR(5) NOT NULL,
             phone CHAR(10) NOT NULL,
             fax VARCHAR(15),
             email VARCHAR(32),
             PRIMARY KEY(customerid)
             )''')
c.execute('''CREATE INDEX idx_company ON Customer (company)''')

c.execute('''CREATE TABLE Payments
             (customerid VARCHAR(4) NOT NULL UNIQUE, 
             amountowed DECIMAL(7, 2) NOT NULL CHECK(amountowed >= 0),
             paymentid VARCHAR(4) NOT NULL,
             nextpayment DATE,
             PRIMARY KEY(paymentid),
             CONSTRAINT FK_customerid FOREIGN KEY (customerid) 
             REFERENCES Customer(customerid) 
             ON DELETE NO ACTION ON UPDATE NO ACTION
             )''')
c.execute('''CREATE TABLE Paymentlog
             (paymentid VARCHAR(4) NOT NULL, 
             lastpayed DATETIME NOT NULL,
             amount DECIMAL(7,2) NOT NULL,
             PRIMARY KEY(paymentid, lastpayed),
             CONSTRAINT FK_paymentid FOREIGN KEY (paymentid) 
             REFERENCES Payments(paymentid) 
             ON DELETE NO ACTION ON UPDATE NO ACTION)''')

c.execute("CREATE INDEX idx_log ON Paymentlog (lastpayed)")

  




c.execute('''CREATE TABLE Invoice 
             (invoiceid INT NOT NULL, 
             customerid VARCHAR(4) NOT NULL,
             invoicedate DATE NOT NULL, 
             billingaddress VARCHAR(32), 
             billingcity VARCHAR(32),
             billingstate CHAR(2),
             billingpostalcode VARCHAR(5),
             total DECIMAL(6, 2) NOT NULL,
             PRIMARY KEY(invoiceid),
             CONSTRAINT FK_customerids FOREIGN KEY (customerid) 
             REFERENCES Customer(customerid) 
             ON DELETE CASCADE ON UPDATE NO ACTION
             )''')

c.execute('''CREATE INDEX idx_invoice ON Invoice (invoiceid)''')

c.execute('''CREATE TABLE InvoiceLine
             (invoicelineid INT NOT NULL AUTO_INCREMENT, 
             invoiceid INT NOT NULL,
             toolnumber VARCHAR(15) NOT NULL, 
             quantity INT NOT NULL, 
             unitprice DECIMAL(6, 2) NOT NULL, 
             PRIMARY KEY (invoicelineid),
             CONSTRAINT FK_invoiceid FOREIGN KEY (invoiceid) 
             REFERENCES Invoice(invoiceid) 
             ON DELETE CASCADE ON UPDATE CASCADE,
             CONSTRAINT FK_toolnumber FOREIGN KEY (toolnumber) 
             REFERENCES Tool(toolNumber) 
             ON DELETE NO ACTION ON UPDATE NO ACTION
             )
             ''')



#filling the tool relation

file = open("example_data/tools.csv")

for record in file:
    toolnum,desc,qty,bc,price = record.split(",")
    toolnum = str(toolnum)
    desc = str(desc)
    qty = int(qty)
    if bc == "NULL":
        bc = None
    else:
        bc = str(bc)
    price = float(price)
    print(toolnum,desc,qty,bc,price)
    c.execute(f"INSERT INTO Tool VALUES ('{toolnum}', '{desc}', {qty}, %s, {price})", (bc,))

file.close()
conn.commit()

#filling the customer relation
filea = open("example_data/customers.csv")

for record in filea:
    cid, fname, lname, comp, addr, city, state, pcode, phone, fax, em = record.split(",")
    cid = str(cid)
    fname = str(fname)
    lname = str(lname)
    comp = str(comp)
    addr = str(addr)
    city = str(city)
    state = str(state)
    pcode = str(pcode)
    phone = str(phone)
    if fax == "NULL":
        fax = None
    else:
        fax = str(fax)

    if em == "NULL":
        email = None
    else:
        email = None


    print(cid, fname, lname, comp, addr, city, state, pcode, phone, fax, email)
    c.execute(f"INSERT INTO Customer VALUES ('{cid}', '{fname}', '{lname}', '{comp}', '{addr}', '{city}', '{state}', '{pcode}', '{phone}',%s, %s )", (fax,email, ))
filea.close()
conn.commit()
#filling invoice

fileb = open("example_data/invoice.csv")

for record in fileb:
    iid,cid,idate,ba,bc,bs,bpc,total = record.split(",")
    iid = int(iid)
    cid = str(cid)
    idate = idate
    ba = str(ba)
    bc = str(bc)
    bs = str(bs)
    bpc = str(bpc)
    total = float(total)

    print(iid,cid,idate,ba,bc,bs,bpc,total)
    c.execute(f"INSERT INTO Invoice VALUES ({iid}, '{cid}', '{idate}', '{ba}', '{bc}', '{bs}', '{bpc}', {total})")

fileb.close()
conn.commit()
#filling invoicelineid
filec = open("example_data/invoiceline.csv")

for record in filec:
    ilid,iid,tn,qty,up = record.split(",")
    ilid= int(ilid)
    iid = int(iid)
    tn = str(tn)
    qty = int(qty)
    up = float(up)

    print(ilid,iid,tn,qty,up)
    c.execute(f"INSERT INTO Invoiceline VALUES ({ilid}, {iid}, '{tn}', {qty}, {up})")

filec.close()
conn.commit()
# filling payments
filed = open("example_data/payments.csv")

for record in filed:
    cid, ao, pid, np = record.split(",")
    cid = str(cid)
    ao = float(ao)
    pid = str(pid)
    np = np


    print(cid, ao, pid, np)
    c.execute(f"INSERT INTO Payments VALUES ('{cid}', {ao}, '{pid}', '{np}')")

filed.close()
conn.commit()
#filling paymentlog
filee = open("example_data/paymentlog.csv")

for record in filee:
    pid, dt, ap = record.split(",")
    pid = str(pid)
    dt = str(dt)
    print(dt)
    ap = float(ap)






    print(pid, dt, ap)
    c.execute(f"INSERT INTO Paymentlog(paymentid, lastpayed, amount) VALUES ('{pid}', '{dt}', {ap})")

filee.close()


c.execute('''CREATE VIEW AllCustomerPayments AS
                 SELECT Customer.customerid, firstname, lastname,Paymentlog.paymentid, amountowed, MAX(lastpayed) AS last_payed
                 FROM Paymentlog NATURAL JOIN Payments, Customer
                 WHERE Customer.customerid = Payments.customerid AND Payments.paymentid = Paymentlog.paymentid
                 GROUP BY Customer.customerid
                 ''')
conn.commit()
conn.close()
