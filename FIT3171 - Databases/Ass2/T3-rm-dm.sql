--****PLEASE ENTER YOUR DETAILS BELOW****
--T3-rm-dm.sql

--Student ID: 32722656
--Student Name: Diong Chen Xi
--Unit Code: FIT3171
--Applied Class No: Tutorial 05

/* Comments for your marker:

*/

--3(a)
DROP SEQUENCE competitor_seq;

DROP SEQUENCE team_seq;

CREATE SEQUENCE competitor_seq START WITH 100 INCREMENT BY 1;

CREATE SEQUENCE team_seq START WITH 100 INCREMENT BY 1;

--3(b)
--Recording emergency contact Jack Kai into the database
INSERT INTO emercontact VALUES (
    '0476541234',
    'Jack',
    'Kai'
);
--Recording competitor Daniel Kai into the database
INSERT INTO competitor VALUES (
    competitor_seq.NEXTVAL,
    'Daniel',
    'Kai',
    'M',
    TO_DATE('12/SEP/2000', 'DD/MON/YYYY'),
    'daniel.kai2000@thismail.com',
    'Y',
    '1111111126',
    'P',
    '0476541234'
);

INSERT INTO entry VALUES (
    (
        SELECT
            event_id
        FROM
            event
        WHERE
                carn_date = (
                    SELECT
                        carn_date
                    FROM
                        carnival
                    WHERE
                        upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                )
            AND eventtype_code = (
                SELECT
                    eventtype_code
                FROM
                    eventtype
                WHERE
                    upper(eventtype_desc) = upper('21.1 Km Half Marathon')
            )
    ),
    (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            event_id = (
                SELECT
                    event_id
                FROM
                    event
                WHERE
                        carn_date = (
                            SELECT
                                carn_date
                            FROM
                                carnival
                            WHERE
                                upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                        )
                    AND eventtype_code = (
                        SELECT
                            eventtype_code
                        FROM
                            eventtype
                        WHERE
                            upper(eventtype_desc) = upper('21.1 Km Half Marathon')
                    )
            )
    ) + 1,
    NULL,
    NULL,
    competitor_seq.CURRVAL,
    NULL,
    (
        SELECT
            char_id
        FROM
            charity
        WHERE
            upper(char_name) = upper('Beyond Blue')
    )
);
--Recording competitor Annabelle Kai into the database
INSERT INTO competitor VALUES (
    competitor_seq.NEXTVAL,
    'Annabelle',
    'Kai',
    'F',
    TO_DATE('23/SEP/1999', 'DD/MON/YYYY'),
    'annabelle.kai1999@thismail.com',
    'Y',
    '1111111127',
    'P',
    '0476541234'
);

INSERT INTO entry VALUES (
    (
        SELECT
            event_id
        FROM
            event
        WHERE
                carn_date = (
                    SELECT
                        carn_date
                    FROM
                        carnival
                    WHERE
                        upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                )
            AND eventtype_code = (
                SELECT
                    eventtype_code
                FROM
                    eventtype
                WHERE
                    upper(eventtype_desc) = upper('21.1 Km Half Marathon')
            )
    ),
    (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            event_id = (
                SELECT
                    event_id
                FROM
                    event
                WHERE
                        carn_date = (
                            SELECT
                                carn_date
                            FROM
                                carnival
                            WHERE
                                upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                        )
                    AND eventtype_code = (
                        SELECT
                            eventtype_code
                        FROM
                            eventtype
                        WHERE
                            upper(eventtype_desc) = upper('21.1 Km Half Marathon')
                    )
            )
    ) + 1,
    NULL,
    NULL,
    competitor_seq.CURRVAL,
    NULL,
    (
        SELECT
            char_id
        FROM
            charity
        WHERE
            upper(char_name) = upper('Amnesty International')
    )
);

COMMIT;

--3(c)
--Recording team Kai Speedstars into the database
INSERT INTO team VALUES (
    team_seq.NEXTVAL,
    'Kai Speedstars',
    TO_DATE('29/MAY/2022', 'DD/MON/YYYY'),
    (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            team_id = (
                SELECT
                    team_id
                FROM
                    team
                WHERE
                    upper(team_name) = upper('Kai Speedstars')
            )
    ) + 1,
    (
        SELECT
            event_id
        FROM
            event
        WHERE
                carn_date = (
                    SELECT
                        carn_date
                    FROM
                        carnival
                    WHERE
                        upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                )
            AND eventtype_code = (
                SELECT
                    eventtype_code
                FROM
                    eventtype
                WHERE
                    upper(eventtype_desc) = upper('21.1 Km Half Marathon')
            )
    ),
    (
        SELECT
            entry_no
        FROM
            entry
        WHERE
                comp_no = (
                    SELECT
                        comp_no
                    FROM
                        competitor
                    WHERE
                            upper(comp_fname) = upper('Annabelle')
                        AND upper(comp_lname) = upper('Kai')
                )
            AND event_id = (
                SELECT
                    event_id
                FROM
                    event
                WHERE
                        carn_date = (
                            SELECT
                                carn_date
                            FROM
                                carnival
                            WHERE
                                upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                        )
                    AND eventtype_code = (
                        SELECT
                            eventtype_code
                        FROM
                            eventtype
                        WHERE
                            upper(eventtype_desc) = upper('21.1 Km Half Marathon')
                    )
            )
    ),
    (
        SELECT
            char_id
        FROM
            charity
        WHERE
            upper(char_name) = upper('Beyond Blue')
    )
);
--Setting Annabelle into Team Kai Speedstars
UPDATE entry
SET
    team_id = team_seq.CURRVAL
WHERE
    comp_no = (
        SELECT
            comp_no
        FROM
            competitor
        WHERE
                upper(comp_fname) = upper('Annabelle')
            AND upper(comp_lname) = upper('Kai')
    );

COMMIT;

--3(d)
--Changing Daniel Kai's entry from '21.1 Km Half Marathon' to '10 Km Run'
UPDATE entry
SET
    event_id = (
        SELECT
            event_id
        FROM
            event
        WHERE
                carn_date = (
                    SELECT
                        carn_date
                    FROM
                        carnival
                    WHERE
                        upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                )
            AND eventtype_code = (
                SELECT
                    eventtype_code
                FROM
                    eventtype
                WHERE
                    upper(eventtype_desc) = upper('10 Km Run')
            )
    ),
    entry_no = (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            event_id = (
                SELECT
                    event_id
                FROM
                    event
                WHERE
                        carn_date = (
                            SELECT
                                carn_date
                            FROM
                                carnival
                            WHERE
                                upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                        )
                    AND eventtype_code = (
                        SELECT
                            eventtype_code
                        FROM
                            eventtype
                        WHERE
                            upper(eventtype_desc) = upper('10 Km Run')
                    )
            )
    ) + 1
WHERE
    comp_no = (
        SELECT
            comp_no
        FROM
            competitor
        WHERE
                upper(comp_fname) = upper('Daniel')
            AND upper(comp_lname) = upper('Kai')
    );
--Updating Annabelle Kai's entry number since Daniel Kai has withdrawn from the '21.1 Km Half Marathon'
ALTER TABLE team DISABLE CONSTRAINT entry_team;

UPDATE entry
SET
    entry_no = (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            event_id = (
                SELECT
                    event_id
                FROM
                    event
                WHERE
                        carn_date = (
                            SELECT
                                carn_date
                            FROM
                                carnival
                            WHERE
                                upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                        )
                    AND eventtype_code = (
                        SELECT
                            eventtype_code
                        FROM
                            eventtype
                        WHERE
                            upper(eventtype_desc) = upper('21.1 Km Half Marathon')
                    )
            )
    )
WHERE
    comp_no = (
        SELECT
            comp_no
        FROM
            competitor
        WHERE
                upper(comp_fname) = upper('Annabelle')
            AND upper(comp_lname) = upper('Kai')
    );

UPDATE team
SET
    entry_no = (
        SELECT
            entry_no
        FROM
            entry
        WHERE
                event_id = (
                    SELECT
                        event_id
                    FROM
                        event
                    WHERE
                            carn_date = (
                                SELECT
                                    carn_date
                                FROM
                                    carnival
                                WHERE
                                    upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
                            )
                        AND eventtype_code = (
                            SELECT
                                eventtype_code
                            FROM
                                eventtype
                            WHERE
                                upper(eventtype_desc) = upper('21.1 Km Half Marathon')
                        )
                )
            AND comp_no = (
                SELECT
                    comp_no
                FROM
                    competitor
                WHERE
                        upper(comp_fname) = upper('Annabelle')
                    AND upper(comp_lname) = upper('Kai')
            )
    )
WHERE
    upper(team_name) = upper('Kai Speedstars');

ALTER TABLE team ENABLE CONSTRAINT entry_team;
--Updating Daniel Kai's entry to join Team Kai Speedstars
UPDATE entry
SET
    team_id = (
        SELECT
            team_id
        FROM
            team
        WHERE
            upper(team_name) = upper('Kai Speedstars')
    )
WHERE
    comp_no = (
        SELECT
            comp_no
        FROM
            competitor
        WHERE
                upper(comp_fname) = upper('Daniel')
            AND upper(comp_lname) = upper('Kai')
    );
--Updating the number of team members of Team Kai Speedstars
UPDATE team
SET
    team_no_members = (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            team_id = (
                SELECT
                    team_id
                FROM
                    team
                WHERE
                    upper(team_name) = upper('Kai Speedstars')
            )
    ) + 1
WHERE
    upper(team_name) = upper('Kai Speedstars');

COMMIT;

--3(e)
--Removing Daniel Kai's entry from the database
DELETE FROM entry
WHERE
    event_id IN (
        SELECT
            event_id
        FROM
            event
        WHERE
            carn_date = (
                SELECT
                    carn_date
                FROM
                    carnival
                WHERE
                    upper(carn_name) = upper('RM Autumn Series Caulfield 2022')
            )
    )
    AND comp_no = (
        SELECT
            comp_no
        FROM
            competitor
        WHERE
                upper(comp_fname) = upper('Daniel')
            AND upper(comp_lname) = upper('Kai')
    );
--Updating the number of team members in Team Kai Speedstars
UPDATE team
SET
    team_no_members = (
        SELECT
            COUNT(*)
        FROM
            entry
        WHERE
            team_id = (
                SELECT
                    team_id
                FROM
                    team
                WHERE
                    upper(team_name) = upper('Kai Speedstars')
            )
    ) - 1
WHERE
    team_id = (
        SELECT
            team_id
        FROM
            team
        WHERE
            upper(team_name) = upper('Kai Speedstars')
    );
--updating Annabelle Kai's team to none
UPDATE entry
SET
    team_id = NULL
WHERE
    team_id = (
        SELECT
            team_id
        FROM
            team
        WHERE
            upper(team_name) = upper('Kai Speedstars')
    );
--updating Annabelle Kai to support Beyond Blue
UPDATE entry
SET
    char_id = (
        SELECT
            char_id
        FROM
            charity
        WHERE
            upper(char_name) = upper('Beyond Blue')
    )
WHERE
    comp_no = (
        SELECT
            comp_no
        FROM
            competitor
        WHERE
                upper(comp_fname) = upper('Annabelle')
            AND upper(comp_lname) = upper('Kai')
    );
--disbanding 'Kai Speedstars'    
DELETE FROM team
WHERE
    upper(team_name) = upper('Kai Speedstars');

COMMIT;