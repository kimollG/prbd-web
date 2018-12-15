import mysql.connector


class Connector:
    def __init__(self, db='vacancies'):
        self.__mydb__ = mysql.connector.connect(
            host="127.0.0.1",
            user='root',
            passwd='sqlpswd',
            auth_plugin='mysql_native_password',
            database=db
        )
        self.__mycursor__ = self.__mydb__.cursor()

    def aggregate(self):
        with open('scripts/aggregate.sql', mode='r') as f:
            content = filter(lambda a: a != '', ' '.join(map(lambda line: line.rstrip(), f.readlines())).split(';'))

        res_list = list()
        x = 0
        for line in content:
            x += 1
            self.__mycursor__.execute(line)
            res = self.__mycursor__.fetchall()
            if x % 2 == 1:
                res[0] = [*res[0], 'True']
            res_list.extend(res)

        return res_list


    def institutions(self,iid=None):
        if iid is not None:
            self.__mycursor__.execute("SELECT * FROM institution where institution_id = %s", [iid, ])
            return self.__mycursor__.fetchall()[0]
        self.__mycursor__.execute("SELECT * FROM institution")
        return (list(x) for x in self.__mycursor__.fetchall())


    def companies(self,cid = None):
        if cid is not None:
            self.__mycursor__.execute("SELECT * FROM ENTERPRISE where enterprise_id = %s",[cid,])
            return self.__mycursor__.fetchall()[0]
        self.__mycursor__.execute("SELECT * FROM ENTERPRISE")
        ret = (list(x) for x in self.__mycursor__.fetchall())
        return ret

    def add_vacancy(self, vacancy):
        self.__mycursor__.execute('''INSERT INTO vacancy 
            VALUES(default,(SELECT enterprise_id FROM enterprise WHERE name LIKE(%s)),%s,%s,%s)''',
                                  (vacancy.comp_name, vacancy.salary, vacancy.position, vacancy.description))
        self.__mydb__.commit()

    def add_requirement(self, vid, experience, education):
        self.__mycursor__.execute('insert into requirement values(default,%s,%s,%s)', (vid, experience, education))
        self.__mydb__.commit()

    def vacancies(self, filter_company=None):
        query = "SELECT e.name,e.city , v.salary, v.position,v.vacancy_id FROM VACANCY v join enterprise e on v.enterprise_id = e.enterprise_id "
        if filter_company:
            query += " WHERE enterprise_id = (SELECT enterprise_id from enterprise where name like(%s))"
        self.__mycursor__.execute(query, filter_company)
        ret = list()
        for select_result in self.__mycursor__.fetchall():
            ret.append((list(select_result)[:-1], select_result[-1]))
        return ret

    def id_check(self, table):
        query = 'select ' + table + '_id from ' + table
        self.__mycursor__.execute(query)
        return (x[0] for x in self.__mycursor__.fetchall())

    def detailed_vacancy(self, vacancy_id):
        print(vacancy_id)
        vacancy_query = '''select (select name from enterprise where enterprise_id = v.enterprise_id),
                            salary, position, description from vacancy v where vacancy_id = %s'''
        self.__mycursor__.execute(vacancy_query, (vacancy_id,))
        vac_info = self.__mycursor__.fetchone()
        requirement_query = '''select work_experience_requirement, education_requirement 
                                from requirement where vacancy_id = %s   '''
        self.__mycursor__.execute(requirement_query, (vacancy_id,))
        requirements = self.__mycursor__.fetchall()
        return vac_info, requirements

    def update(self, vid, company, salary, position, description):
        query = '''update vacancy
                    set enterprise_id = (SELECT enterprise_id FROM enterprise WHERE name LIKE(%s)), salary = %s, position = %s, description = %s 
                    where vacancy_id = %s'''
        self.__mycursor__.execute(query, (company, salary, position, description, vid))
        self.__mydb__.commit()

    def remove_vacancy(self, vid):
        for query in ' delete from requirement where vacancy_id = %s;', 'delete from vacancy where vacancy_id = %s':
            self.__mycursor__.execute(query, (int(vid),))
            self.__mydb__.commit()

    def all_people(self):
        query = 'select * from person'
        self.__mycursor__.execute(query)
        return self.__mycursor__.fetchall()

    def person(self, person_id):
        query = 'select name from person where person_id = %s'

        education_query = '''select i.*, degree, profile, enter_date,graduation_date
                            from education
                            join institution i
                            on education.institution_id = i.institution_id
                            where person_id = %s'''
        experience_query= '''select  e.enterprise_id, e.name, we.position, ifnull(we.enrollment,'-'), ifnull(we.dismission,'-')
                            from work_experience we
                            join enterprise e on we.enterprise_id = e.enterprise_id
                            where person_id = %s'''
        person = list()
        for x in query, education_query, experience_query:
            self.__mycursor__.execute(x, [person_id, ])
            person.append(self.__mycursor__.fetchall())
        return person


if __name__ == '__main__':
    c = Connector()
    c.__mycursor__.execute("SELECT * FROM ENTERPRISE")
    print(c.__mycursor__.fetchall())
    # self.__mycursor__.execute()
