--****PLEASE ENTER YOUR DETAILS BELOW****
--T2-rm-insert.sql

--Student ID: 32722656
--Student Name: Diong Chen Xi
--Unit Code: FIT3171
--Applied Class No: Tutorial 05

/* Comments for your marker:
1. It takes 15-25 minutes to finish a 3km run/walk.
2. It takes 30-40 minutes to finish a 5km run.
3. It takes 50-70 minutes to finish a 10km run.
4. It takes 70-100 minutes to finish a 21.1km half marathon.
5. It takes 240-300 minutes to finish a 42.2km marathon.
*/

-- Task 2 Load the EMERCONTACT, COMPETITOR, ENTRY and TEAM tables with your own
-- test data following the data requirements expressed in the brief

-- =======================================
-- EMERCONTACT
-- =======================================
--Entry 1
--Contact for 3 competitors
INSERT INTO emercontact VALUES (
    '0123456789',
    'Mickey',
    'Mouse'
);
--Entry 2
--Contact for 5 competitors
INSERT INTO emercontact VALUES (
    '0234567891',
    'Minnie',
    'Mouse'
);
--Entry 3
--Contact for 3 competitors
INSERT INTO emercontact VALUES (
    '0345678912',
    'Donald',
    'Duck'
);
--Entry 4
--Contact for 3 competitors
INSERT INTO emercontact VALUES (
    '0456789123',
    'Daisy',
    'Duck'
);
--Entry 5
--Contact for 1 competitor
INSERT INTO emercontact VALUES (
    '0567891234',
    'Goofy',
    'Dog'
);

-- =======================================
-- COMPETITOR
-- =======================================
--10 are Monash student/staff
--5 are not Monash student/staff
--2 are under 18 years of age
--Entry 1
INSERT INTO competitor VALUES (
    1,
    'Oved',
    'Gitte',
    'F',
    TO_DATE('29/MAR/1984', 'DD/MON/YYYY'),
    'oved.gitte1984@thismail.com',
    'Y',
    '1111111111',
    'T',
    '0123456789'
);
--Entry 2
INSERT INTO competitor VALUES (
    2,
    'Darragh',
    'Randulf',
    'M',
    TO_DATE('28/MAR/1988', 'DD/MON/YYYY'),
    'darragh.randulf1988@thismail.com',
    'N',
    '1111111112',
    'F',
    '0123456789'
);
--Entry 3
INSERT INTO competitor VALUES (
    3,
    'Clint',
    'Baldovino',
    'M',
    TO_DATE('15/JUN/1997', 'DD/MON/YYYY'),
    'clint.baldovino19974@thismail.com',
    'Y',
    '1111111113',
    'F',
    '0123456789'
);
--Entry 4
INSERT INTO competitor VALUES (
    4,
    'Wilkin',
    'Patrick',
    'M',
    TO_DATE('11/MAR/2005', 'DD/MON/YYYY'),
    'wilkin.patrick2005@thismail.com',
    'N',
    '1111111114',
    'P',
    '0234567891'
);
--Entry 5
INSERT INTO competitor VALUES (
    5,
    'Christina',
    'Nia',
    'F',
    TO_DATE('09/AUG/1994', 'DD/MON/YYYY'),
    'christina.nia1994@thismail.com',
    'Y',
    '1111111115',
    'G',
    '0234567891'
);
--Entry 6
INSERT INTO competitor VALUES (
    6,
    'Shyam',
    'Valentin',
    'F',
    TO_DATE('06/DEC/2000', 'DD/MON/YYYY'),
    'shyam.valentin2000@thismail.com',
    'N',
    '1111111116',
    'F',
    '0234567891'
);
--Entry 7
INSERT INTO competitor VALUES (
    7,
    'Fridenot',
    'Alvis',
    'M',
    TO_DATE('10/APR/1993', 'DD/MON/YYYY'),
    'fridenot.alvis1993@thismail.com',
    'Y',
    '1111111117',
    'P',
    '0234567891'
);
--Entry 8
INSERT INTO competitor VALUES (
    8,
    'Armida',
    'Oswine',
    'F',
    TO_DATE('29/OCT/2002', 'DD/MON/YYYY'),
    'armida.oswine2002@thismail.com',
    'Y',
    '1111111118',
    'F',
    '0234567891'
);
--Entry 9
INSERT INTO competitor VALUES (
    9,
    'Nuadu',
    'Faustino',
    'M',
    TO_DATE('19/NOV/2007', 'DD/MON/YYYY'),
    'nuadu.faustino2007@thismail.com',
    'N',
    '1111111119',
    'G',
    '0345678912'
);
--Entry 10
INSERT INTO competitor VALUES (
    10,
    'Andi',
    'Neelima',
    'M',
    TO_DATE('14/OCT/1983', 'DD/MON/YYYY'),
    'andi.neelima1983@thismail.com',
    'Y',
    '1111111120',
    'F',
    '0345678912'
);
--Entry 11
INSERT INTO competitor VALUES (
    11,
    'Aten',
    'Helene',
    'F',
    TO_DATE('24/FEB/1999', 'DD/MON/YYYY'),
    'aten.helene1999@thismail.com',
    'Y',
    '1111111121',
    'T',
    '0345678912'
);
--Entry 12
INSERT INTO competitor VALUES (
    00012,
    'Tereza',
    'Desislav',
    'F',
    TO_DATE('14/MAR/2003', 'DD/MON/YYYY'),
    'tereza.desislav2003@thismail.com',
    'N',
    '1111111122',
    'G',
    '0456789123'
);
--Entry 13
INSERT INTO competitor VALUES (
    13,
    'Shaban',
    'Jawad',
    'M',
    TO_DATE('20/NOV/1982', 'DD/MON/YYYY'),
    'shaban.jawad@thismail.com',
    'Y',
    '1111111123',
    'T',
    '0456789123'
);
--Entry 14
INSERT INTO competitor VALUES (
    14,
    'Danna',
    'Liberatus',
    'F',
    TO_DATE('05/MAR/2003', 'DD/MON/YYYY'),
    'danna.liberatus2003@thismail.com',
    'N',
    '1111111124',
    'F',
    '0456789123'
);
--Entry 15
INSERT INTO competitor VALUES (
    15,
    'Aleksander',
    'Manius',
    'M',
    TO_DATE('16/MAY/1996', 'DD/MON/YYYY'),
    'aleksander.manius1996@thismail.com',
    'Y',
    '1111111125',
    'F',
    '0567891234'
);
-- =======================================
-- ENTRY
-- =======================================
--5 Carnivals (Events 1,2 : 24/09/2021, Events 3-5 : 01/10/2021, Events 6-9 : 05/02/2022, Events 10,11 : 14/03/2022, Events 12-14 : 29/05/2022) 
--Start times (07:45 Event 11; 08:00 Events 5,8,9,10,14; 08:30 Events 2,4,6,7,13; 08:45 Event 12; 09:00 Event 3; 09:30 Event 1)
ALTER TABLE entry DISABLE CONSTRAINT team_entry;
ALTER TABLE team DISABLE CONSTRAINT entry_team;
--Entry 1
INSERT INTO entry VALUES (
    1,
    1,
    TO_DATE('09:30:12', 'HH24:MI:SS'),
    TO_DATE('10:05:46', 'HH24:MI:SS'),
    1,
    1,
    1
);
--Entry 2
INSERT INTO entry VALUES (
    3,
    1,
    TO_DATE('09:00:08', 'HH24:MI:SS'),
    TO_DATE('09:36:12', 'HH24:MI:SS'),
    1,
    5,
    NULL
);
--Entry 3
INSERT INTO entry VALUES (
    6,
    1,
    TO_DATE('08:30:04', 'HH24:MI:SS'),
    TO_DATE('08:51:31', 'HH24:MI:SS'),
    1,
    4,
    NULL
);
--Entry 4
INSERT INTO entry VALUES (
    10,
    1,
    TO_DATE('08:00:45', 'HH24:MI:SS'),
    TO_DATE('08:20:23', 'HH24:MI:SS'),
    1,
    3,
    3
);
--Entry 5
INSERT INTO entry VALUES (
    12,
    1,
    TO_DATE('08:45:02', 'HH24:MI:SS'),
    TO_DATE('09:19:57', 'HH24:MI:SS'),
    1,
    NULL,
    NULL
);
--Entry 6
INSERT INTO entry VALUES (
    2,
    1,
    TO_DATE('08:30:29', 'HH24:MI:SS'),
    TO_DATE('09:24:11', 'HH24:MI:SS'),
    2,
    2,
    NULL
);
--Entry 7
INSERT INTO entry VALUES (
    4,
    1,
    TO_DATE('08:30:12', 'HH24:MI:SS'),
    TO_DATE('09:23:57', 'HH24:MI:SS'),
    2,
    NULL,
    NULL
);
--Entry 8
INSERT INTO entry VALUES (
    7,
    1,
    NULL,
    NULL,
    3,
    NULL,
    NULL
);
--Entry 9
INSERT INTO entry VALUES (
    11,
    1,
    TO_DATE('07:45:57', 'HH24:MI:SS'),
    TO_DATE('12:05:31', 'HH24:MI:SS'),
    3,
    NULL,
    NULL
);
--Entry 10
INSERT INTO entry VALUES (
    13,
    1,
    TO_DATE('08:30:38', 'HH24:MI:SS'),
    TO_DATE('09:40:21', 'HH24:MI:SS'),
    3,
    NULL,
    NULL
);
--Entry 11
INSERT INTO entry VALUES (
    1,
    2,
    TO_DATE('09:30:24', 'HH24:MI:SS'),
    TO_DATE('10:01:52', 'HH24:MI:SS'),
    4,
    1,
    1
);
--Entry 12
INSERT INTO entry VALUES (
    5,
    1,
    TO_DATE('08:00:05', 'HH24:MI:SS'),
    TO_DATE('09:18:23', 'HH24:MI:SS'),
    5,
    NULL,
    NULL
);
--Entry 13
INSERT INTO entry VALUES (
    8,
    1,
    TO_DATE('08:00:31', 'HH24:MI:SS'),
    TO_DATE('09:02:41', 'HH24:MI:SS'),
    5,
    NULL,
    NULL
);
--Entry 14
INSERT INTO entry VALUES (
    10,
    2,
    TO_DATE('08:00:58', 'HH24:MI:SS'),
    TO_DATE('08:17:25', 'HH24:MI:SS'),
    5,
    3,
    3
);
--Entry 15
INSERT INTO entry VALUES (
    14,
    1,
    TO_DATE('08:00:13', 'HH24:MI:SS'),
    TO_DATE('09:19:11', 'HH24:MI:SS'),
    5,
    NULL,
    NULL
);
--Entry 16
INSERT INTO entry VALUES (
    2,
    2,
    TO_DATE('08:30:47', 'HH24:MI:SS'),
    TO_DATE('09:28:57', 'HH24:MI:SS'),
    5,
    2,
    NULL
);
--Entry 17
INSERT INTO entry VALUES (
    3,
    2,
    TO_DATE('09:00:23', 'HH24:MI:SS'),
    TO_DATE('09:37:21', 'HH24:MI:SS'),
    6,
    5,
    NULL
);
--Entry 18
INSERT INTO entry VALUES (
    9,
    1,
    TO_DATE('08:00:46', 'HH24:MI:SS'),
    TO_DATE('09:32:11', 'HH24:MI:SS'),
    7,
    NULL,
    NULL
);
--Entry 19
INSERT INTO entry VALUES (
    11,
    2,
    TO_DATE('07:45:18', 'HH24:MI:SS'),
    TO_DATE('12:17:49', 'HH24:MI:SS'),
    7,
    NULL,
    NULL
);
--Entry 20
INSERT INTO entry VALUES (
    12,
    2,
    TO_DATE('08:45:57', 'HH24:MI:SS'),
    TO_DATE('09:16:53', 'HH24:MI:SS'),
    8,
    NULL,
    NULL
);
--Entry 21
INSERT INTO entry VALUES (
    2,
    3,
    TO_DATE('08:30:14', 'HH24:MI:SS'),
    TO_DATE('09:24:52', 'HH24:MI:SS'),
    9,
    2,
    NULL
);
--Entry 22
INSERT INTO entry VALUES (
    4,
    2,
    TO_DATE('08:30:22', 'HH24:MI:SS'),
    TO_DATE('09:25:08', 'HH24:MI:SS'),
    9,
    NULL,
    NULL
);
--Entry 23
INSERT INTO entry VALUES (
    6,
    2,
    TO_DATE('08:30:51', 'HH24:MI:SS'),
    TO_DATE('08:44:56', 'HH24:MI:SS'),
    10,
    4,
    NULL
);
--Entry 24
INSERT INTO entry VALUES (
    10,
    3,
    TO_DATE('08:00:11', 'HH24:MI:SS'),
    TO_DATE('08:16:13', 'HH24:MI:SS'),
    10,
    NULL,
    NULL
);
--Entry 25
INSERT INTO entry VALUES (
    13,
    2,
    TO_DATE('08:30:03', 'HH24:MI:SS'),
    TO_DATE('09:21:36', 'HH24:MI:SS'),
    10,
    NULL,
    NULL
);
--Entry 26
INSERT INTO entry VALUES (
    1,
    3,
    TO_DATE('09:30:44', 'HH24:MI:SS'),
    TO_DATE('10:04:33', 'HH24:MI:SS'),
    13,
    1,
    1
);
--Entry 27
INSERT INTO entry VALUES (
    5,
    2,
    TO_DATE('08:00:29', 'HH24:MI:SS'),
    TO_DATE('09:35:28', 'HH24:MI:SS'),
    14,
    NULL,
    NULL
);
--Entry 28
INSERT INTO entry VALUES (
    7,
    2,
    NULL,
    NULL,
    14,
    NULL,
    NULL
);
--Entry 29
INSERT INTO entry VALUES (
    11,
    3,
    TO_DATE('07:45:55', 'HH24:MI:SS'),
    TO_DATE('12:42:01', 'HH24:MI:SS'),
    14,
    NULL,
    NULL
);
--Entry 30
INSERT INTO entry VALUES (
    14,
    2,
    TO_DATE('08:00:24', 'HH24:MI:SS'),
    TO_DATE('09:11:26', 'HH24:MI:SS'),
    15,
    NULL,
    NULL
);

-- =======================================
-- TEAM
-- =======================================
--Entry 1
INSERT INTO team VALUES (
    1,
    'Manticore',
    TO_DATE('24/SEP/2021', 'DD/MON/YYYY'),
    3,
    1,
    1,
    1
);
--Entry 2
INSERT INTO team VALUES (
    2,
    'Leviathan',
    TO_DATE('24/SEP/2021', 'DD/MON/YYYY'),
    3,
    2,
    2,
    NULL
);
--Entry 3
INSERT INTO team VALUES (
    3,
    'Manticore',
    TO_DATE('01/OCT/2021', 'DD/MON/YYYY'),
    2,
    3,
    2,
    NULL
);
--Entry 4
INSERT INTO team VALUES (
    4,
    'Culebre',
    TO_DATE('14/MAR/2022', 'DD/MON/YYYY'),
    2,
    10,
    1,
    3
);
--Entry 5
INSERT INTO team VALUES (
    5,
    'Opinicus',
    TO_DATE('05/FEB/2022', 'DD/MON/YYYY'),
    2,
    6,
    2,
    NULL
);
ALTER TABLE entry ENABLE CONSTRAINT team_entry;
ALTER TABLE team ENABLE CONSTRAINT entry_team;

COMMIT;

