create database vacancies;
connect vacancies;
CREATE TABLE person (
    person_id INT  AUTO_INCREMENT,
	name VARCHAR(40) NOT NULL,
	PRIMARY KEY (person_id)
	);
	
CREATE TABLE enterprise (
	enterprise_id INT  AUTO_INCREMENT,
	name VARCHAR(40) NOT NULL,
	address VARCHAR(40),
	city VARCHAR(40) NOT NULL,
	PRIMARY KEY(enterprise_id)
	);
	
CREATE TABLE vacancy (
    vacancy_id INT  AUTO_INCREMENT,
	enterprise_id INT,
	salary DECIMAL(10,2),
	position VARCHAR(40) NOT NULL,
	description TEXT,
	PRIMARY KEY (vacancy_id),
	FOREIGN KEY (enterprise_id) REFERENCES enterprise(enterprise_id) ON DELETE CASCADE ON UPDATE CASCADE
	);
	
CREATE TABLE institution (
    institution_id INT  AUTO_INCREMENT,
	name VARCHAR(40) NOT NULL,
	address VARCHAR(40),
	city VARCHAR(40),
	PRIMARY KEY(institution_id)
);

CREATE TABLE education (
    institution_id INT,
	person_id INT,
	degree VARCHAR(40),
	profile VARCHAR(40) NOT NULL,
	graduation DATE,
	CONSTRAINT PK_Education PRIMARY KEY (institution_id, person_id),
	FOREIGN KEY (institution_id) REFERENCES institution(institution_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE ON UPDATE CASCADE
);
	
CREATE TABLE work_experience (
    person_id INT,
	enterprise_id INT,
	position VARCHAR(40) NOT NULL,
	enrollment DATE,
	dismission DATE,
	CONSTRAINT PK_Work_expirience PRIMARY KEY (person_id,enterprise_id),
	FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (enterprise_id) REFERENCES enterprise(enterprise_id) ON DELETE CASCADE ON UPDATE CASCADE
	);

CREATE TABLE requirement (
	requirement_id INT,
	vacancy_id INT,
	work_experience_requirement TEXT,
	education_requirement TEXT,
	PRIMARY KEY (requirement_id),
	FOREIGN KEY (vacancy_id) REFERENCES vacancy(vacancy_id)
);