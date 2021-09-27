-- cikeys db password for user westongc_weston = COMP350f21
create database reservation;
use reservation;

create table employee(
empid int auto_increment,
fname varchar(50),
lname varchar(50),
PRIMARY KEY(empid)
);
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
create table customer(
cust_id int auto_increment,
usrname VARCHAR(50),
fname varchar(50),
lname varchar(50),
pmt_type ENUM("CC", "CASH", "CHECK"),
pmt_info varchar(50),
PRIMARY KEY(cust_id)
);

insert into customer(cust_id, usrname, fname, lname, pmt_type, pmt_info) VALUES (0, "JSmith1", "John", "Smith", "CC", "1234567891204312");
select * from customer;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
create table hotel_room(
roomnum int AUTO_INCREMENT,
rtype ENUM("KING", "QUEEN", "JUNIOR"),
smoke boolean,
PRIMARY KEY(roomnum)
);


insert into hotel_room(roomnum, rtype, smoke) VALUES (0, "JUNIOR", 0);
insert into hotel_room(roomnum, rtype, smoke) VALUES (0, "QUEEN", 0);
insert into hotel_room(roomnum, rtype, smoke) VALUES (0, "KING", 1);
select * from hotel_room;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
create table hotel_reservation(
rid int auto_increment,
roomnum int,
cust_id int,
checkin date,
checkout date,
PRIMARY KEY(rid),
FOREIGN KEY(cust_id) REFERENCES customer(cust_id)
);

drop table hotel_reservation;
insert into hotel_reservation(rid, roomnum, cust_id, checkin, checkout) VALUES (0, 1, 1, "2021-10-1", "2021-10-2");
select * from hotel_reservation;

-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
create table spa_service(
stype ENUM("SERVICE1", "SERVICE2", "SERVICE3"),
start_time time,
end_time time,
PRIMARY KEY(stype)
);
drop table spa_service;
insert into spa_service(stype, duration) values ("SERVICE1", 1);
insert into spa_service(stype, duration) values ("SERVICE2", 2);
insert into spa_service(stype, duration) values ("SERVICE3", 3);
select * from spa_service;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
create table spa_reservation(
rid int auto_increment,
roomnum int,
cust_id int,
spa_start date,
start_time time,
end_time time,
stype ENUM("SERVICE1", "SERVICE2", "SERVICE3"),
PRIMARY KEY(rid),
FOREIGN KEY(roomnum) REFERENCES hotel_room(roomnum),
FOREIGN KEY(cust_id) REFERENCES customer(cust_id),
FOREIGN KEY(stype) REFERENCES spa_service(stype)
);

insert into spa_reservation(rid, roomnum, cust_id, spa_start, start_time, end_time) VALUES (0, 1, 1, "2021-10-1", "12:00:00", "14:00:00");
select * from spa_reservation;
drop table spa_reservation;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
create view h_res_private as 
SELECT rid, h.roomnum, c.usrname, c.fname, c.lname, checkin, checkout, h.rtype, h.smoke, c.pmt_type, c.pmt_info from hotel_reservation r
join hotel_room h on h.roomnum = r.roomnum
join customer c on c.cust_id = r.cust_id;

drop view h_res_private;
select * from h_res_private;

-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
delimiter //		
create procedure isreserved(IN roomnum int, IN checkin DATE, in checkout DATE)	-- sanity check before creating hotel/spa reservation
ir: BEGIN
	DECLARE DAYS INT;
    DECLARE ERR INT;
		SELECT DATEDIFF(checkout, checkin) INTO DAYS;
        IF DAYS < 0 THEN
            LEAVE ir;
		ELSE
			SELECT * FROM hotel_reservation r where (r.roomnum = roomnum AND (r.checkout > checkin)); 
		end if;
END//
delimiter ;

drop procedure isreserved;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
-- get cust_id from username
-- get service duration from stype


-- delimiter //
-- create procedure make_spa_reservation(IN usrname VARCHAR(50), IN roomnum int, IN start_date DATE, IN start_time TIME, IN stype VARCHAR(8))	
-- 	BEGIN
-- 	DECLARE ERR INT;
-- 	DECLARE duration double;
--     DECLARE cust_id int;
--     DECLARE roomnum int;
--     DECLARE reserved int;
-- 			SELECT c.cust_id into cust_id from customer c where c.usrname = usrname;
-- 			call isreserved(roomnum, checkin, checkout);		-- check if there is a current hotel reservation under this customer and use that room if exists
-- 			SELECT FOUND_ROWS() into reserved;
-- 			if reserved > 0 THEN
-- 				SELECT r.roomnum into roomnum from hotel_reservation where h.cust_id = cust_id;
-- 			ELSE -- if no current hotel reservation, join hotel_room with hotel_reservation and do intersection on hotel_room to see what is available and pick first result for roomnum
-- 			SELECT distinct roomnum from hotel_room h 
--             SELECT s.duration into duration from spa_service s where s.stype = stype;
-- 	
-- 	INSERT INTO spa_reservation VALUES (0, roomnum
-- END//
-- delimiter ;    

-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
delimiter //
create procedure make_hotel_reservation(IN usrname VARCHAR(50), IN roomnum INT, IN checkin DATE, IN checkout DATE)
	BEGIN
    DECLARE cust_id INT;
    DECLARE reserved INT;
    SELECT c.cust_id into cust_id from customer c where c.usrname = usrname;
		 INSERT INTO hotel_reservation (rid, roomnum, cust_id, checkin, checkout) VALUES (0, roomnum, cust_id, checkin, checkout);
	
END//
delimiter ;

INSERT INTO hotel_reservation VALUES (0, 2, 1, "2021-11-11", "2021-11-13");
delete from hotel_reservation where roomnum = 2;
call make_hotel_reservation("JSmith1", 2, "2021-11-11", "2021-11-13"); -- success!!
select * from hotel_reservation;
drop procedure make_hotel_reservation;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
delimiter //
create procedure cancel_hotel_reservation(IN usrname VARCHAR(50), IN checkin DATE) -- remove current reservation if necessary
BEGIN
	DECLARE cust_id int;
    SELECT c.cust_id into cust_id from customer c where c.usrname = usrname;
	DELETE FROM hotel_reservation r where r.cust_id = cust_id AND r.checkin = checkin;
END//
delimiter ;
select * from hotel_reservation;
call cancel_hotel_reservation("JSmith1", "2021-10-1");
drop procedure cancel_hotel_reservation;
-- -----------------------------------------------------------------------------------------------------------------------------------------------------------------
delimiter //
create procedure cancel_spa_reservation(IN cust_id int, spa_start date, spa_end date) -- remove current reservation if necessary
BEGIN
	DELETE FROM spa_reservation s where s.cust_id = cust_id AND s.spa_start = spa_start AND s.spa_end = spa_end;
END//
delimiter ;


call isreserved(1, "2021-10-1", "2021-10-5");
call isreserved(1, "2021-9-28", "2021-10-2"); 
call isreserved(1, "2021-10-1", "2021-10-2");
call isreserved(1, "2021-1-1","2021-1-1");

-- TESTING -----------------------------------
call make_hotel_reservation("JSmith1", 2, "2021-11-11", "2021-11-13"); -- success!!
select * from hotel_reservation;
delete from hotel_reservation where roomnum =2;
call isreserved(2, "2021-11-11", "2021-11-13");
call cancel_hotel_reservation("JSmith1", "2021-11-11");
select * from hotel_reservation;
select * from h_res_private;





