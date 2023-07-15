--****PLEASE ENTER YOUR DETAILS BELOW****
--T5-rm-alter.sql

--Student ID: 32722656
--Student Name: Diong Chen Xi
--Unit Code: FIT3171
--Applied Class No: Tutorial 05

/* Comments for your marker:



*/

--5(a)
CREATE OR REPLACE TRIGGER check_multiple_enrolment BEFORE
    INSERT ON entry
    FOR EACH ROW
DECLARE
    new_carn_date   event.carn_date%TYPE;
    carn_date_found NUMBER;
BEGIN
    SELECT
        carn_date
    INTO new_carn_date
    FROM
        event
    WHERE
        event_id = :new.event_id;

    SELECT
        COUNT(*)
    INTO carn_date_found
    FROM
             entry
        JOIN event
        ON entry.event_id = event.event_id
    WHERE
        comp_no = :new.comp_no;

    IF ( carn_date_found > 0 ) THEN
        raise_application_error(-20000, 'Competitor cannot be enrolled in multiple events in the same carnival');
    END IF;
END;
/ 

-- Test Harness for 5(a) --
SET ECHO ON;

--Prior state
SELECT
    *
FROM
    entry;

--Test trigger - Competitor already enrolled in an event in the carnival - Failed
INSERT INTO entry VALUES (
    2,
    4,
    NULL,
    NULL,
    1,
    NULL,
    NULL,
    NULL,
    NULL
);

--Post state
SELECT
    *
FROM
    entry;

--Test trigger - Competitor not enrolled in any event in the carnival - Success
INSERT INTO entry VALUES (
    1,
    4,
    NULL,
    NULL,
    11,
    NULL,
    NULL,
    NULL,
    NULL
);

--Post state
SELECT
    *
FROM
    entry;

ROLLBACK;

SET ECHO OFF;

--5(b)
ALTER TABLE eventtype ADD eventtype_record NUMBER(5, 2);

COMMENT ON COLUMN eventtype.eventtype_record IS
    'The fastest record for the event';

ALTER TABLE eventtype ADD eventtype_recordholder NUMBER(5);

COMMENT ON COLUMN eventtype.eventtype_recordholder IS
    'The record holder for the event';

CREATE OR REPLACE TRIGGER update_elapsed_time_and_records BEFORE
    UPDATE OF entry_finishtime ON entry
    FOR EACH ROW
DECLARE
    elapsedtime entry.entry_elapsed_time%TYPE;
    event_type eventtype.eventtype_code%type;
    current_record eventtype.eventtype_record%type;
BEGIN
    elapsedtime := round((:new.entry_finishtime - :old.entry_starttime)*24*60,2);
    :new.entry_elapsed_time := elapsedtime;
    
    SELECT eventtype_code INTO event_type FROM eventtype WHERE eventtype_code = (SELECT eventtype_code FROM event WHERE event_id = :new.event_id);
    SELECT eventtype_record INTO current_record FROM eventtype WHERE eventtype_code = event_type;
    IF((current_record is null) or (current_record > elapsedtime)) THEN
        UPDATE eventtype 
        SET eventtype_record = elapsedtime, eventtype_recordholder = :new.comp_no
        WHERE eventtype_code = event_type;
    END IF;
END;
/

-- Test harness for 5(b)
SET ECHO ON;
--Prior state
SELECT
    to_char(entry_finishtime,'HH:MI:SS'), entry_elapsed_time
FROM
    entry
WHERE event_id = 1 and entry_no = 1;

SELECT * FROM eventtype;

--Test trigger -Current record is null
UPDATE entry
SET
    entry_finishtime = TO_DATE('10:02:50', 'HH:MI:SS')
WHERE
        event_id = 1
    AND entry_no = 1;

--Post state
SELECT
    to_char(entry_finishtime,'HH:MI:SS'), entry_elapsed_time
FROM
    entry
WHERE event_id = 1 and entry_no = 1;
SELECT * FROM eventtype;

--Prior state
SELECT
    to_char(entry_finishtime,'HH:MI:SS'), entry_elapsed_time
FROM
    entry
WHERE event_id = 1 and entry_no = 2;
SELECT * FROM eventtype;

--Test trigger -Slower than current record -Not updated
UPDATE entry
SET
    entry_finishtime = TO_DATE('10:04:50', 'HH:MI:SS')
WHERE
        event_id = 1
    AND entry_no = 2;
    
--Post state
SELECT
    to_char(entry_finishtime,'HH:MI:SS'), entry_elapsed_time
FROM
    entry
WHERE event_id = 1 and entry_no = 2;
SELECT * FROM eventtype;

--Prior state
SELECT
    to_char(entry_finishtime,'HH:MI:SS'), entry_elapsed_time
FROM
    entry
WHERE event_id = 1 and entry_no = 2;
SELECT * FROM eventtype;

--Test trigger -Faster than current record -Record updated
UPDATE entry
SET
    entry_finishtime = TO_DATE('10:01:50', 'HH:MI:SS')
WHERE
        event_id = 1
    AND entry_no = 2;
    
--Post state
SELECT
    to_char(entry_finishtime,'HH:MI:SS'), entry_elapsed_time
FROM
    entry
WHERE event_id = 1 and entry_no = 2;
SELECT * FROM eventtype;

ROLLBACK;

SET ECHO OFF;

--5(c)
CREATE OR REPLACE PROCEDURE event_registration (
    in_comp_no IN NUMBER,
    in_carn_date IN DATE,
    in_eventtype_desc IN VARCHAR2,
    in_team_name IN VARCHAR2,
    out_message OUT VARCHAR2
) AS
    var_carn_date_found NUMBER;
    var_event_name_found NUMBER;
    var_team_name_found NUMBER;
BEGIN
    SELECT COUNT(*) INTO var_carn_date_found from carnival WHERE carn_date = in_carn_date;
    
    SELECT COUNT(*) INTO var_event_name_found from eventtype WHERE eventtype_desc = in_eventtype_desc;
    
    SELECT COUNT(*) INTO var_team_name_found from team WHERE team_name = in_team_name and carn_date = in_carn_date;
    
    IF (var_carn_date_found = 0) THEN
        out_message := 'Invalid carnival date given, registration cancelled';
    ELSE
        IF (var_event_name_found = 0) THEN
            out_message := 'Invalid event name given, registration cancelled';
        ELSE
            IF(var_team_name_found = 0) THEN
                INSERT INTO entry VALUES(
                (SELECT event_id from event WHERE carn_date = in_carn_date AND eventtype_code = (SELECT eventtype_code from eventtype where eventtype_desc = in_eventtype_desc)),
                (SELECT COUNT(*) from entry WHERE event_id = (SELECT event_id from event WHERE carn_date = in_carn_date AND eventtype_code = (SELECT eventtype_code from eventtype where eventtype_desc = in_eventtype_desc))) + 1,
                null,
                null,
                in_comp_no,
                (SELECT team_id from team WHERE team_name = in_team_name),
                null
                );
                INSERT INTO team VALUES(
                (SELECT COUNT(*) from team)+1,
                in_team_name,
                in_carn_date,
                (SELECT COUNT(*) from entry WHERE team_id = (SELECT team_id FROM team where team_name = in_team_name and carn_date = in_carn_date))+1,
                (SELECT event_id from event WHERE carn_date = in_carn_date and eventtype_code = (SELECT eventtype_code from eventtype WHERE eventtype_desc = in_eventtype_desc)),
                (SELECT entry_no from entry WHERE event_id = (SELECT event_id from event WHERE carn_date = in_carn_date and eventtype_code = (SELECT eventtype_code from eventtype WHERE eventtype_desc = in_eventtype_desc)) and comp_no = in_comp_no),
                null
                );
                UPDATE entry
                SET team_id = (SELECT team_id from team WHERE team_name = in_team_name)
                WHERE comp_no = in_comp_no and event_id = (SELECT event_id from event WHERE carn_date = in_carn_date and eventtype_code = (SELECT eventtype_code from eventtype WHERE eventtype_desc = in_eventtype_desc));
                out_message := 'Registration successful, new team created where applicant is the leader';
            ELSE
                UPDATE team
                SET team_no_members = (SELECT COUNT(*) FROM entry WHERE team_id = (SELECT team_id from team where team_name = in_team_name and carn_date = in_carn_date))+1
                WHERE team_id = (SELECT team_id from team where team_name = in_team_name and carn_date = in_carn_date);
                UPDATE entry
                SET team_id = (SELECT team_id from team where team_name = in_team_name and carn_date = in_carn_date)
                WHERE event_id =(SELECT event_id from event WHERE carn_date = in_carn_date and eventtype_code = (SELECT eventtype_code from eventtype WHERE eventtype_desc = in_eventtype_desc))
                AND entry_no = (SELECT entry_no from entry WHERE event_id = (SELECT event_id from event WHERE carn_date = in_carn_date and eventtype_code = (SELECT eventtype_code from eventtype WHERE eventtype_desc = in_eventtype_desc)) and comp_no = in_comp_no);
                out_message := 'Registration successful';
                INSERT INTO entry VALUES(
                (SELECT event_id from event WHERE carn_date = in_carn_date AND eventtype_code = (SELECT eventtype_code from eventtype where eventtype_desc = in_eventtype_desc)),
                (SELECT COUNT(*) from entry WHERE event_id = (SELECT event_id from event WHERE carn_date = in_carn_date AND eventtype_code = (SELECT eventtype_code from eventtype where eventtype_desc = in_eventtype_desc))) + 1,
                null,
                null,
                in_comp_no,
                (SELECT team_id from team WHERE team_name = in_team_name and carn_date = in_carn_date),
                null
                );
                out_message := 'Registration successful, applicant registered in existing team';
            END IF;
        END IF;
    END IF;     
END event_registration;
/

-- Test Harness for 5(c)
--Prior state
select * from team;

--execute the procedure
DECLARE
    output VARCHAR2(200);
BEGIN
    --call the procedure - invalid since carnival doesn't exist
    event_registration(1,to_date('23/MAY/2022','DD/MON/YYYY'),'21.1 Km Half Marathon','Manticore',output);
    dbms_output.put_line(output);
END;
/

--execute the procedure
DECLARE
    output VARCHAR2(200);
BEGIN
    --call the procedure - invalid since event doesn't exist
    event_registration(1,to_date('05/FEB/2022','DD/MON/YYYY'),'1 Km short run','Manticore',output);
    dbms_output.put_line(output);
END;
/

--execute the procedure
DECLARE
    output VARCHAR2(200);
BEGIN
    --call the procedure - success, team exists, add competitor to team
    event_registration(11,to_date('24/SEP/2021','DD/MON/YYYY'),'5 Km Run','Manticore',output);
    dbms_output.put_line(output);
END;
/

--Post state
select * from team;
select * from entry;

rollback;

--execute the procedure
DECLARE
    output VARCHAR2(200);
BEGIN
    --call the procedure - success, team does not exist, register team
    event_registration(1,to_date('05/FEB/2022','DD/MON/YYYY'),'21.1 Km Half Marathon','Test',output);
    dbms_output.put_line(output);
END;
/

--Post state
select * from team;
select * from entry;

rollback;