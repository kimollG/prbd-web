connect vacancies;
INSERT INTO person VALUES(default,'Alex');
INSERT INTO person VALUES(default,'Ben');
INSERT INTO person VALUES(default,'Charles');
INSERT INTO person VALUES(default,'Dennis');

INSERT INTO enterprise VALUES(default,'Amazon','sample str. 21','Prague');
INSERT INTO enterprise VALUES(default,'FedEx','sample str. 15','Prague');
INSERT INTO enterprise VALUES(default,'AT&T','other str. 21','Chicago');
INSERT INTO enterprise VALUES(default,'Yandex','Ulitsa Lva Tolstogo 16','Moscow');

INSERT INTO institution VALUES(default,'MIT','Massachusetts Ave 71','Cambridge');
INSERT INTO institution VALUES(default,'VSU','Universitetskaya sq 1','Voronezh');

INSERT INTO vacancy VALUES(default,(SELECT enterprise_id FROM enterprise WHERE name LIKE('AT&T')),10000.0,
 'janitor','Well-payed job for a hard-working person');
 INSERT INTO vacancy VALUES(default,(SELECT enterprise_id FROM enterprise WHERE name LIKE('AT&T')),200000.0,
 'HR manager','Well-payed job for a hard-working person');
 INSERT INTO vacancy VALUES(default,(SELECT enterprise_id FROM enterprise WHERE name LIKE('Yandex')),15000.0,
 'QA trainee','30 hours per week');
 INSERT INTO vacancy VALUES(default,(SELECT enterprise_id FROM enterprise WHERE name LIKE('FedEx')),20000.0,
 'janitor',NULL);
 INSERT INTO vacancy VALUES(default,(SELECT enterprise_id FROM enterprise WHERE name LIKE('Amazon')),3000000.0,
 'Java Senior developer',NULL);
 
 INSERT INTO education VALUES(
 (SELECT institution_id FROM institution WHERE name LIKE('VSU')),
 (SELECT person_id FROM person WHERE name LIKE('Ben')),
 'bachelor','CS',DATE('2014-7-14'));
 INSERT INTO education VALUES(
 (SELECT institution_id FROM institution WHERE name LIKE('VSU')),
 (SELECT person_id FROM person WHERE name LIKE('Alex')),
 'master','CS',DATE('2001-7-20'));
 INSERT INTO education VALUES(
 (SELECT institution_id FROM institution WHERE name LIKE('MIT')),
 (SELECT person_id FROM person WHERE name LIKE('Charles')),
 'bachelor','physics',DATE('2005-7-15'));
 INSERT INTO education VALUES(
 (SELECT institution_id FROM institution WHERE name LIKE('VSU')),
 (SELECT person_id FROM person WHERE name LIKE('Dennis')),
 'master','mathematics',DATE('2001-7-20'));
 
 INSERT INTO work_experience VALUES(
 (SELECT person_id FROM person WHERE name LIKE('Alex')),
 (SELECT enterprise_id FROM enterprise WHERE name LIKE('FedEx')),
 'Team leader',DATE('2009-05-11'), DATE('2011-03-03'));
 INSERT INTO work_experience VALUES(
 (SELECT person_id FROM person WHERE name LIKE('Alex')),
 (SELECT enterprise_id FROM enterprise WHERE name LIKE('Amazon')),
 'Team leader',DATE('2011-05-11'), NULL);
 INSERT INTO work_experience VALUES(
 (SELECT person_id FROM person WHERE name LIKE('Ben')),
 (SELECT enterprise_id FROM enterprise WHERE name LIKE('Yandex')),
 'Team leader',DATE('2009-05-11'), DATE('2016-05-23'));