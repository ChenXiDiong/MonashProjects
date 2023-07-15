--****PLEASE ENTER YOUR DETAILS BELOW****
--T4-rm-alter.sql

--Student ID: 32722656
--Student Name: Diong Chen Xi
--Unit Code: FIT3171
--Applied Class No: Tutorial 05

/* Comments for your marker:
4b: Since a team may support many charities, the relation is now M:N. Therefore a new entity TEAM_CHARITY is introduced 
to correctly map the relation between team and charity. 

4c: A new entity ROLE is introduced to document the list of roles. When a competitor resgiters for a role in a carnival,
it is known that he/she is registered as an official in that carnival, therefore adding a role_id in the entry table is
sufficient to indicate that a certain competitor is registered as an official for a certain carnival.
*/

--4(a)
ALTER TABLE entry ADD entry_elapsed_time NUMBER(5, 2);

COMMENT ON COLUMN entry.entry_elapsed_time IS
    'The time elapsed for the competitor to finish the event';

UPDATE entry
SET
    entry_elapsed_time = round((entry_finishtime - entry_starttime) * 24 * 60, 2);

COMMIT;

--4(b)
DROP TABLE team_charity CASCADE CONSTRAINTS;

CREATE TABLE team_charity (
    team_id NUMBER(3) NOT NULL,
    char_id NUMBER(3) NOT NULL,
    carn_date DATE NOT NULL,
    tc_percentage NUMBER(3) NOT NULL
);

COMMENT ON COLUMN team_charity.team_id IS
    'Team identifier (unique)';
    
COMMENT ON COLUMN team_charity.char_id IS
    'Charity unique identifier';
    
COMMENT ON COLUMN team_charity.carn_date IS
    'Date of carnival (unique identifier)';
    
COMMENT ON COLUMN team_charity.tc_percentage IS
    'Percentage of raised funds that will be donated to the charity by the team';

ALTER TABLE team_charity
    ADD CONSTRAINT tc_pk PRIMARY KEY ( team_id,
                                       char_id,
                                       carn_date );

ALTER TABLE team DROP CONSTRAINT charity_team;

ALTER TABLE team DROP COLUMN char_id;

ALTER TABLE team_charity
    ADD CONSTRAINT team_tc FOREIGN KEY ( team_id )
        REFERENCES team ( team_id );

ALTER TABLE team_charity
    ADD CONSTRAINT charity_tc FOREIGN KEY ( char_id )
        REFERENCES charity ( char_id );

ALTER TABLE team_charity
    ADD CONSTRAINT carnival_tc FOREIGN KEY ( carn_date )
        REFERENCES carnival ( carn_date );

COMMIT;
     
--4(c)
DROP TABLE role CASCADE CONSTRAINTS;

CREATE TABLE role (
    role_id   NUMBER(3) NOT NULL,
    role_name VARCHAR2(30) NOT NULL
);

COMMENT ON COLUMN role.role_id IS
    'Role identifier(unique)';

COMMENT ON COLUMN role.role_name IS
    'Name of the role';

ALTER TABLE role ADD CONSTRAINT role_pk PRIMARY KEY ( role_id );

INSERT INTO role VALUES(
    1,
    'Time keeper'
);

INSERT INTO role VALUES(
    2,
    'Marshal'
);

INSERT INTO role VALUES(
    3,
    'Starter'
);

INSERT INTO role VALUES(
    4,
    'First aid'
);

ALTER TABLE entry ADD role_id NUMBER(3);

COMMENT ON COLUMN entry.role_id IS
    'Role identifier(unique)';
    
ALTER TABLE entry 
    ADD CONSTRAINT role_entry FOREIGN KEY ( role_id )
        REFERENCES role ( role_id );
        
COMMIT;