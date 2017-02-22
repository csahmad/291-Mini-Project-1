-- Data prepared by Harley Vanselow, vanselow@ualberta.ca, and published on 4/2/2017
-- Expansion pack 1: 291 TAs
-- Expansion pack 2: passwords (by Jessica Prieto for Mini Project 1)
insert into users values (100, 'kam100', 'Ehsan Kamalloo','ehsan@aol.ca','Edmonton',-7);
insert into users values (101, 'esh101', 'Esha','Esha@mail.com','Edmonton',-7);
insert into users values (102, 'mal102', 'Curtis Malainey','cujo@aol.com','Cochrane',-7);
insert into users values (103, 'sar103', 'Saeed Sarabchi','saeed@aol.com','Edmonton',-7);
insert into users values (104, 'kam104', 'Ehsaner Kamallooer','looer@send.ca','Edmonton',-7);
insert into users values (105, 'far105', 'Sara Farazi','sara@gmail.com','Edmonton',-7);

insert into users values (200, 'gen200', 'Genji','g@ow.com','Edmonton',-7);
insert into users values (201, 'mcc201', 'McCree','mcree@ow.com','Edmonton',-7);
insert into users values (202, 'pha202', 'Pharah','phar@ow.com','Edmonton',-7);
insert into users values (203, 'rea201', 'Reaper','reap@ow.com','Edmonton',-7);
insert into users values (204, 'sol204', 'Soldier76','76@ow.com','Edmonton',-7);
insert into users values (205, 'som205', 'Sombra','sombra@ow.com','Edmonton',-7);
insert into users values (206, 'tra206', 'Tracer','trace@ow.com','Edmonton',-7);
insert into users values (207, 'bas207', 'Bastion','bastion@ow.com','Edmonton',-7);
insert into users values (208, 'han208', 'Hanzo','hanzo@ow.com','Edmonton',-7);
insert into users values (209, 'jun209', 'Junkrat','junk@ow.com','Edmonton',-7);
insert into users values (210, 'mei210', 'Mei','mei@ow.com','Edmonton',-7);
insert into users values (211, 'tor211', 'Torbjorn','torb@ow.com','Edmonton',-7);
insert into users values (212, 'wid212', 'Widowmaker','widow@ow.com','Edmonton',-7);
insert into users values (213, 'dva213', 'DVa','dva@ow.com','Edmonton',-7);
insert into users values (214, 'rei214', 'Reinhardt','rien@ow.com','Edmonton',-7);
insert into users values (215, 'roa215', 'Roadhog','hog@ow.com','Edmonton',-7);
insert into users values (216, 'win216', 'Winston','win@ow.com','Edmonton',-7);
insert into users values (217, 'zar217', 'Zarya','zarya@ow.com','Edmonton',-7);
insert into users values (218, 'ana218', 'Ana','ana@ow.com','Edmonton',-7);
insert into users values (219, 'luc219', 'Lucio','lucio@ow.com','Edmonton',-7);
insert into users values (220, 'mer220', 'Mercy','mercy@ow.com','Edmonton',-7);
insert into users values (221, 'sym221', 'Symmetra','symm@ow.com','Edmonton',-7);
insert into users values (222, 'zen222', 'Zenyatta','zen@ow.com','Edmonton',-7);
insert into users values (223, 'doo223', 'Doomfist','df@ow.com','Edmonton',-7);
insert into users values (300, 'doe300', 'john doe','jd@ua.com','Edmonton',-7);

insert into follows values (100,102,'15-JAN-2017');
insert into follows values (105,102,'20-SEP-2014');
insert into follows values (102,101,'15-OCT-2016');
insert into follows values (103,105,'11-NOV-2016');
insert into follows values (103,100,'05-JUN-2016');
insert into follows values (100,105,'02-FEB-2017');
insert into follows values (102,105,'14-SEP-2016');
insert into follows values (101,102,'15-OCT-2016');
insert into follows values (101,103,'15-OCT-2010');
insert into follows values (101,105,'15-OCT-2010');


insert into follows values (200,222,'15-OCT-2010');
insert into follows values (200,220,'15-NOV-2010');
insert into follows values (208,200,'15-OCT-2010');

insert into follows values (205,200,'15-DEC-2010');
insert into follows values (205,201,'15-OCT-2010');
insert into follows values (205,202,'15-AUG-2016');
insert into follows values (205,203,'15-OCT-2010');
insert into follows values (205,204,'11-SEP-2016');
insert into follows values (205,206,'16-OCT-2010');
insert into follows values (205,207,'17-JUN-2010');
insert into follows values (205,208,'15-JUL-2015');
insert into follows values (205,209,'13-OCT-2010');
insert into follows values (205,210,'15-MAR-2010');
insert into follows values (205,211,'16-APR-2010');
insert into follows values (205,212,'25-OCT-2015');
insert into follows values (205,213,'15-OCT-2010');
insert into follows values (205,214,'25-APR-2014');
insert into follows values (205,215,'15-OCT-2014');
insert into follows values (205,216,'16-FEB-2010');
insert into follows values (205,217,'15-OCT-2016');
insert into follows values (205,218,'15-DEC-2014');
insert into follows values (205,219,'13-DEC-2016');
insert into follows values (205,220,'05-OCT-2010');
insert into follows values (205,221,'03-OCT-2013');
insert into follows values (205,222,'09-OCT-2012');

insert into follows values (203,212,'25-JAN-2016');
insert into follows values (203,205,'03-JAN-2010');
insert into follows values (212,205,'07-OCT-2016');
insert into follows values (213,219,'13-MAR-2010');
insert into follows values (218,214,'15-OCT-2012');
insert into follows values (214,218,'15-AUG-2016');
insert into follows values (209,202,'14-AUG-2016');
insert into follows values (209,201,'15-OCT-2016');
insert into follows values (209,214,'12-OCT-2015');
insert into follows values (209,210,'15-SEP-2014');
insert into follows values (218,220,'12-OCT-2016');

insert into follows values (216,102,'12-OCT-2016');
insert into follows values (216,105,'12-OCT-2016');
insert into follows values (216,210,'12-OCT-2016');
insert into follows values (216,200,'12-OCT-2016');

insert into follows values(300,105,'13-MAR-2010');
insert into follows values(300,210,'01-FEB-2017');
insert into follows values(300,200,'01-FEB-2017');

insert into follows values(205,300,'01-FEB-2017');
insert into follows values(209,300,'01-FEB-2017');
insert into follows values(212,300,'01-FEB-2017');
insert into follows values(223,300,'01-FEB-2017');

insert into tweets values (1, 101,'22-NOV-2015','291 lab sections are so much fun.',null,null);
insert into tweets values (2, 102,'25-DEC-2016','Hate to say it but #edgyidea.',null,null);
insert into tweets values (3, 102,'10-JAN-2017','Computer Engineering>Computer Science.',null,null);
insert into tweets values (4, 103,'10-JAN-2015','Testing my tweets.',null,null);
insert into tweets values (5, 104,'11-MAY-2016','I think bad things are bad #Agreeable',null,null);
insert into tweets values (6, 104,'12-MAY-2016','Good things should happend more #Agreeable',null,null);
insert into tweets values (7, 105,'12-APR-2015','#Dolphins are neat.',null,null);
insert into tweets values (8, 105,'24-APR-2015','#Dolphins my favorite sea dwelling mammal.',null,null);
insert into tweets values (9, 211,'01-JAN-2016','Aardvark pays off', null, null);
insert into tweets values (10, 201,'01-JAN-2016','Im the quick', null, null);
insert into tweets values (11, 212,'01-JAN-2016','*French sounds* #Talon', null, null);
insert into tweets values (12, 208,'01-JAN-2016','Super sad about killing bro', null, null);
insert into tweets values (13, 220,'01-JAN-2016','Heros never die!', null, null);
insert into tweets values (14, 221,'01-JAN-2016','Why does everyone melt? #BeamSniper', null, null);
insert into tweets values (15, 209,'01-JAN-2016','Robbing banks and whatnot', null, null);
insert into tweets values (16, 203,'01-JAN-2016','*Edge sounds* #Talon', null, null);
insert into tweets values (17, 216,'01-JAN-2016','Taser is better than fists.', null, null);
insert into tweets values (18, 205,'01-JAN-2016','Be right back', null, null);
insert into tweets values (19, 213,'01-JAN-2016','Is this easy mode?', null, null);
insert into tweets values (20, 104,'12-AUG-2015','(1)They will look up and shout "Save us!" #edmonton',null,null);
insert into tweets values (21, 104,'13-AUG-2015','(2)and Ill whisper "no."#edmonton',null,null);
insert into tweets values (22, 203,'12-JUN-2012','Hate dolphins #edgyidea #Dolphins',null,null);
insert into tweets values (23, 100,'26-DEC-2016','How could you say that #Outrage.',102,'25-DEC-2016');
insert into tweets values (24, 101,'26-DEC-2016','Unbelievable #Outrage.',102,'25-DEC-2016');
insert into tweets values (25, 103,'26-DEC-2016','Cool ideas, tell me more.',102,'25-DEC-2016');
insert into tweets values (26, 104,'26-DEC-2016','Im indifferent to this issue.',102,'25-DEC-2016');
insert into tweets values (27, 102,'27-DEC-2016','Thats just like,your opinion man...',101,'26-DEC-2016');
insert into tweets values (28, 100,'01-JAN-2016','Hello World', 103, '10-JAN-2015');
insert into tweets values (29, 217,'01-FEB-2016','Not for long', 213, '01-JAN-2016');

--edgyidea retweets
insert into retweets values (105, 2,'25-DEC-2017');
insert into retweets values (101, 2,'25-DEC-2017');
insert into retweets values (100, 2,'25-DEC-2017');

--Test tweet retweets
insert into retweets values (100,4,'25-JUN-2017');
insert into retweets values (101,4,'25-JUN-2017');
insert into retweets values (102,4,'25-JUN-2017');
insert into retweets values (103,4,'25-JUN-2017');

--Dolphins are cool retweets
insert into retweets values (100,7,'21-MAY-2016');
insert into retweets values (101,7,'25-JUN-2017');
insert into retweets values (102,7,'18-JUL-2016');
insert into retweets values (103,7,'10-AUG-2017');
insert into retweets values (104,7,'26-SEP-2016');
insert into retweets values (219,7,'28-DEC-2016');

--Heroes never die retweets
insert into retweets values (200,13,'01-JAN-2016');
insert into retweets values (201,13,'01-JAN-2016');
insert into retweets values (202,13,'01-JAN-2016');
insert into retweets values (219,27,'28-DEC-2016');


insert into hashtags values ('edgyidea');
insert into hashtags values ('Agreeable');
insert into hashtags values ('Dolphins');
insert into hashtags values ('Outrage');
insert into hashtags values ('edmonton');

insert into mentions values (2, 'edgyidea');
insert into mentions values (22, 'edgyidea');
insert into mentions values (5, 'Agreeable');
insert into mentions values (6, 'Agreeable');
insert into mentions values (23, 'Outrage');
insert into mentions values (24, 'Outrage');
insert into mentions values (7,'Dolphins');
insert into mentions values (8,'Dolphins');
insert into mentions values (22,'Dolphins');
insert into mentions values(20,'edmonton');
insert into mentions values(21,'edmonton');
	

insert into lists values ('tas',100);
insert into lists values ('engineers',105);
insert into lists values ('overwatch',216);
insert into lists values ('talon',203);

insert into includes values ('engineers',102);

insert into includes values ('tas',100);
insert into includes values ('tas',101);
insert into includes values ('tas',102);
insert into includes values ('tas',103);
insert into includes values ('tas',104);
insert into includes values ('tas',105);
insert into includes values ('tas',216);

insert into includes values ('overwatch',200);
insert into includes values ('overwatch',201);
insert into includes values ('overwatch',202);
insert into includes values ('overwatch',204);
insert into includes values ('overwatch',206);
insert into includes values ('overwatch',207);
insert into includes values ('overwatch',208);
insert into includes values ('overwatch',210);
insert into includes values ('overwatch',211);
insert into includes values ('overwatch',213);
insert into includes values ('overwatch',214);
insert into includes values ('overwatch',216);
insert into includes values ('overwatch',217);
insert into includes values ('overwatch',218);
insert into includes values ('overwatch',219);
insert into includes values ('overwatch',220);
insert into includes values ('overwatch',221);
insert into includes values ('overwatch',222);

insert into includes values ('talon',102);
insert into includes values ('talon',203);
insert into includes values ('talon',205);
insert into includes values ('talon',209);
insert into includes values ('talon',212);
insert into includes values ('talon',215);
insert into includes values ('talon',223);




