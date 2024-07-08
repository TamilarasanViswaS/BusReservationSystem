import datetime
import random

from tabulate import tabulate
import mysql.connector

class BusTicket:
    def __init__(self):
        self.con=mysql.connector.connect(host="localhost",user="root",password="Stamilak47@#",database="Bus")
        self.res=self.con.cursor()
        self.sqlshow="select id,travelsName from travels"
        self.sqlSearchid="select seat,travelsName from travels where id=%s"
        self.saveBooked="insert into Booked values(%s,%s,'Booked',%s,CURRENT_TIMESTAMP,%s,%s)"

        self.reduceSeat="UPDATE travels SET seat = %s where travelsName=%s"
        self.logUsername=""
        self.logPassword=""
        self.re = ""
        self.date=""
        self.BookedDetails=dict()
        self.passwordofAdmin="123@#"
    def login(self):
        try:
            print(
                "---------------------------------------------LogIn----------------------------------------------------")
            self.logUsername = input("Enter your id : ")
            self.logPassword = input("Enter your Password : ")
            searchUsername = "select password from " + self.logUsername + ";"
            self.res.execute(searchUsername)
            fintUser = self.res.fetchall()[0][0]
            if self.logPassword == fintUser:
                searchUser = "select username from " + self.logUsername + ";"
                self.res.execute(searchUser)
                findlog = self.res.fetchall()[0][0]
                print("Wellcom ", findlog)
                choi = int(input("1.Booking\n2.Canselation\n"))
                if choi == 1:
                    self.Booked()
                elif choi == 2:
                    self.cancelation()
            else:
                print("your password is worng")
                self.forgotPassword()
        except mysql.connector.Error as err:
            print("*******************************************************************************")
            print("******************  Please enter Correct id and Password  *********************")
            print("*******************************************************************************")

    def forgotPassword(self):
        try:
            print(
                "--------------------------------------------- ForgotPassword ----------------------------------------------------")
            userId = input("Enter Your userId : ")
            userName = input("Enter Username : ")
            emailId = input("Enter Your Email : ")
            sqlforgot = "select password from " + userId + " where username=%s and email=%s"
            forgot = (userName, emailId)
            self.res.execute(sqlforgot, forgot)
            rel = self.res.fetchall()[0][0]
            print(rel)
            while True:
                changeCh = input("if you want to Change your password yes or no ")
                if changeCh.lower() == "yes":
                    enOldPass = input("Enter your Old Password : ")
                    if rel == enOldPass:
                        enNewPass = input("Enter New Password : ")
                        enNewComPass = input("Enter Comfirm Password : ")
                        if enNewPass == enNewComPass:
                            sqlPassChange = "update " + userId + " set password=%s where username=%s and email=%s"
                            changePass = (enNewPass, userName, emailId)
                            self.res.execute(sqlPassChange, changePass)
                            self.con.commit()
                            print(
                                "************************ Your Password is Changed Successfully *****************************")
                            break
                        else:
                            print(
                                "************************ Your Password and Comfirm Password is mismatch *****************************")
                    else:
                        print("************************ Your Old Password is Wrong *****************************")
                else:
                    break
        except mysql.connector.Error as err:
            print("*******************************************************************************")
            print("**********************  Please enter Correct Details  *************************")
            print("*******************************************************************************")

    def SignUp(self):
        try:
            print(
                "--------------------------------------------- Welcome To SignUp ----------------------------------------------------")
            alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

            userNameS = input("Create your User name : ")
            while True:
                passwordS = input("Create your Password : ")
                comfirmPasswordS = input("Create Comfirm your Password : ")
                character = "!@#$%&*"
                upperAlf = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                number = "1234567890"
                c = 0
                up = 0
                num = 0
                for i in character:
                    if i in passwordS:
                        c += 1
                for j in upperAlf:
                    if j in passwordS:
                        up += 1
                for h in number:
                    if h in passwordS:
                        num += 1
                if c >= 1 and up >= 1 and num >= 1 and len(passwordS) >= 8:
                    if passwordS == comfirmPasswordS:
                        for i in range(8):
                            random_alphabet = random.choice(alphabet)
                            if random_alphabet[0] not in "1234567890":
                                self.re += random_alphabet
                            else:
                                random_alphabet = random.choice(alphabet)
                                if random_alphabet[0] not in "1234567890":
                                    self.re += random_alphabet

                        print("Your login id : ", self.re)
                        while True:
                            email = input("Enter your email: ")
                            if "@gmail.com" in email:
                                createTable = "create table " + self.re + " (username varchar(30),password varchar(20),email varchar(40),processing varchar(40),bookingDate varchar(20),travelsName varchar(30),canceledTicketNo varchar(30),BookingId varchar(30))"
                                insertValues = "insert into " + self.re + " (username,password,email,bookingDate) values(%s,%s,%s,CURRENT_TIMESTAMP)"
                                firstUp = (userNameS, passwordS, email)
                                self.res.execute(createTable)
                                self.res.execute(insertValues, firstUp)
                                self.con.commit()
                                self.login()
                                break
                            else:
                                print("********************* Enter Valid EmailId ***********************")

                    else:
                        print("Your Password and Comfirm password are Mismach")
                else:
                    print("Create Password must one spacial Charecter,one Uppercase alpabet and one number")
                    break
        except mysql.connector.Error as err:
            print("*******************************************************************************")
            print("**********************  Please enter Correct Details  *************************")
            print("*******************************************************************************")

    def Booked(self):
        try:
            print(
                "--------------------------------------------- Booking Session ----------------------------------------------------")
            self.res.execute(self.sqlshow)
            result = self.res.fetchall()
            print("Available Travels \n", tabulate(result, headers=["id", "TravelsName"]))
            busch = int(input("Enter your bus id no to Book : "))
            secid = busch,
            self.res.execute(self.sqlSearchid, secid)
            aviTcket = self.res.fetchall()
            print("Available Ticket is : ", aviTcket[0][0])
            travelsNameSave = aviTcket[0][1]
            while True:
                bookedTickets = int(input("You want to Book How many Ticket : "))
                print(bookedTickets)
                if aviTcket[0][0] >= bookedTickets:
                    if bookedTickets <= 5:
                        for i in range(bookedTickets):
                            name = input("Enter your name : ")
                            age = int(input("Enter your age : "))
                            ticketN0 = random.randrange(100000, 999999)
                            passBooked = (self.logUsername, ticketN0, travelsNameSave, name, age)
                            self.res.execute(self.saveBooked, passBooked)
                            bookedHis = "insert into " + self.logUsername + " values(%s,'Booked','Booked','Booked',CURRENT_TIMESTAMP,%s,'Booked',%s)"
                            his = (name, travelsNameSave, ticketN0)
                            self.res.execute(bookedHis, his)
                            self.date = datetime.datetime.now()
                            self.con.commit()
                            self.BookedDetails.__setitem__(i, [ticketN0, self.date, travelsNameSave, name, age])

                        for view in range(bookedTickets):
                            print(
                                "*******************************************************************************************************************************")
                            print("Your TicketNo : ", self.BookedDetails[view][0], "\nBookingDateTime : ",
                                  self.BookedDetails[view][1], "\nTravels Name : ", self.BookedDetails[view][2],
                                  "\nName : ", self.BookedDetails[view][3], "\nAge : ", self.BookedDetails[view][4])
                            print(
                                "*******************************************************************************************************************************")
                        print(self.BookedDetails)
                        print("Your ", bookedTickets, " ticket Successfully Booked")

                        ti = aviTcket[0][0] - bookedTickets
                        update = (ti, travelsNameSave)
                        self.res.execute(self.reduceSeat, update)
                        self.con.commit()
                    else:
                        print("One person can book 5 tickets only")
                else:
                    print(aviTcket[0][0], " Tickets Only have")
                againBook = input("if you want to booking again yes or no : ")
                if againBook.lower() != "yes":
                    break
        except mysql.connector.Error as err:
            print("*******************************************************************************")
            print("**********************  Please enter Correct Details  *************************")
            print("*******************************************************************************")

    def cancelation(self):
        while True:
            try:
                ticketNoCan = int(input("Enter your TicketNo : "))
                q = "select Bookingid from " + self.logUsername + " where Bookingid='%s';"
                m=ticketNoCan,
                self.res.execute(q,m)
                rem1 = self.res.fetchall()[0][0]
                if rem1!= "":
                    cancelup = "update " + self.logUsername + " set password=%s,email=%s,processing=%s,canceledTicketNo='%s', BookingId=%s where BookingId='%s';"
                    c = ('canceled','canceled','canceled',ticketNoCan, 'canceled', ticketNoCan)
                    self.res.execute(cancelup, c)
                    self.con.commit()

                    travelsNamecan = "select travelsName from booked where ticketNo=%s"
                    st = ticketNoCan,
                    self.res.execute(travelsNamecan, st)
                    gettravelsName = self.res.fetchall()[0][0]

                    showSeatAvl = "select seat from travels where travelsName=%s"
                    tran = gettravelsName,
                    self.res.execute(showSeatAvl, tran)
                    traseat = self.res.fetchall()[0][0] + 1

                    updateTravelsNamecan = "update travels set seat=%s where travelsName=%s"
                    updateSeat = (traseat, gettravelsName)
                    self.res.execute(updateTravelsNamecan, updateSeat)
                    self.con.commit()
                    print("Successfully Canceled ")

                    bookedCancel1 = "update booked set ticketNo=%s , cancelTicketNo='%s' where ticketNo='%s'"
                    cancelBooked1 = ('Canceled', ticketNoCan, ticketNoCan)
                    self.res.execute(bookedCancel1, cancelBooked1)
                    self.con.commit()
                    yes = input("If you want to cancel another ticket yes or no ")
                    if yes.lower() != "yes":
                        break
            except:
                print("*ticket not found")
                break
    def admin(self):
        adminPassWord=input("Enter your password : ")
        if self.passwordofAdmin==adminPassWord:
            adminCh=int(input("1.Change Travels details\n2.Cancel Ticket\n3.Add Travels\n"))
            if adminCh==1:
                adminChin=int(input("1.Change Travels Name\n2.Change Travels Seat\n"))
                if adminChin==1:
                    try:
                        idShow = int(input("Enter bus Id : "))
                        sqlShow1 = "select travelsName from travels where id=%s"
                        vam = idShow,
                        self.res.execute(sqlShow1, vam)
                        s = self.res.fetchall()[0][0]
                        print("Your old Travels Name : ",s)
                        if s != "":
                            enNewName = input("Enter New Name : ")
                            sqlforNamech = "update travels set travelsName=%s where id=%s"
                            namech = (enNewName,idShow)
                            self.res.execute(sqlforNamech, namech)
                            self.con.commit()
                            print("*************************** Successfully Name Changed *****************************")
                    except:
                        print("*************************** Your Enter id is Not Found *****************************")
                elif adminChin==2:
                    try:
                        idShowSeat = int(input("Enter bus Id : "))
                        sqlShow1 = "select seat from travels where id=%s"
                        vam = idShowSeat,
                        self.res.execute(sqlShow1, vam)
                        s = self.res.fetchall()[0][0]
                        print("Your old Seat : ",s)
                        if s != "":
                            enNewSeat = int(input("Enter New Seat : "))
                            sqlforSeatch = "update travels set seat=%s where id=%s"
                            Seatch = (enNewSeat, idShowSeat)
                            self.res.execute(sqlforSeatch, Seatch)
                            self.con.commit()
                            print("*************************** Successfully Seat Changed *****************************")
                    except:
                        print("*************************** Your Enter id is Not Found *****************************")
            elif adminCh==2:
                self.cancelation()
            elif adminCh==3:
                trName=input("Enter Travels Name : ")
                enSeat=int(input("Enter Travels Seat : "))
                sqlInsert="insert into travels (travelsName,seat) values(%s,%s)"
                insertTravels=(trName,enSeat)
                self.res.execute(sqlInsert,insertTravels)
                self.con.commit()
                print("*************************** Successfully Added *****************************")
run=BusTicket()
while True:
    ch = int(input("1.Login\n2.SignUp\n3.Admin LogIn\n4.Exit\n"))
    if ch==1:
        run.login()
    elif ch==2:
        run.SignUp()
    elif ch==3:
        run.admin()
    else:
        break




