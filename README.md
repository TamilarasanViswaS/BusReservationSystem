                          Bus Reservation System
Step 1................................................................
first you will create database and tables i will give the query in below,
next you will download mysql-connector-python package in pycharm
(go to settings -> project -> project interpreter -> +(Add the package and install mysql-connector-python))
you will finished step2,step3,step4 next run the BusTicket.py file in pycharm.
This only Backend project


step 2................................................................

create database Bus;
use bus;

step 3................................................................

create table travels(
id integer primary key auto_increment,
travelsName varchar(30),
seat integer
);

step 4................................................................

create table booked(
userName varchar(30),
ticketNo varchar(30),
cancelTicketNo varchar(30),
travelsName varchar(30),
date varchar(30),
name varchar(30),
age integer
);
