SELECT 'Name:','Studied in:','Specialisation:' from DUAL;

SELECT p.name , i.name, e.profile
from person p
join education e on p.person_id = e.person_id
join institution i on e.institution_id = i.institution_id;


SELECT 'Position:','Salary:','Company:' from Dual;

SELECT position,salary, enterprise.name FROM vacancy RIGHT JOIN enterprise
ON vacancy.enterprise_id = enterprise.enterprise_id; 