import os

from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import redirect

from Position import Position, SelectPosition
import connector
from DataFilter import companiesFilter, generalFilter
from collections import namedtuple

vacancy = namedtuple('vacancy', ['comp_name', 'salary', 'description', 'position'])


def compare(s1, s2):
    for x in zip(s1, s2):
        if x[0] != x[1]:
            print(x[0], x[1])


app = Flask(__name__)
app.secret_key = "WEmwU"
con = connector.Connector()
menuItems = {
    'Companies': {
        'content': lambda: ((x, '(details)', 'company/?id='+str(link)) for x, link in companiesFilter(con.companies)),
        'page': 'GeneralList.html',
        'title': 'Companies',
        'after_line': {'u': 'Total:', 'p': ' {} companies'.format(con.number_of_companies())},
        'need_back': True},
    'Aggregated': {
        'content': con.aggregate,
        'page': 'aggregated.html',
        'title': 'General data'},
    'NewVacancy': {'action': 'new_vacancy',
                   'positions': [
                       Position(description='Position', type='text', name='position'),
                       Position(description='Description', type='text', name='description'),
                       Position(description='Salary', type='number', name='salary'),  # companies names
                       SelectPosition(description='Company', name='company',
                                      content=lambda: (x[1] for x in con.companies()))
                   ],
                   'title': 'Add new vacancy',
                   'page': 'GeneralForm.html'},
    'ShowVacancies': {'content': lambda: ((x[0], '(details)', 'vacancy_' + str(x[1])) for x in con.vacancies()),
                      'title': 'Available vacancies',
                      'page': 'GeneralList.html',
                      'after_line': {'u': 'Total:', 'p': ' {} vacancies'.format(con.number_of_vacancies())},
                      'need_back': True},
    'List of people': {'FOO': lambda: generalFilter(con.all_people(), 1, isReducing=True),
                       'title': 'People, looking for job'},
    'FindPerson': {

        'title': 'Search for employee',
        'content':
            {'selections': [{'name': 'education',
                                            'vals': [
                                            {'name': x[0], 'val': x[1]} for x in con.institutions()
                                            ]+[{'name': -1, 'val': '-'}], 'desc': 'education: '},
                            {'name': 'work',
                             'vals': [
                                    {'name': x[0], 'val': x[1]} for x in con.companies()
                                    ]+[{'name': -1, 'val': '-'}], 'desc': 'work experience: '}]},
        'page': 'GeneralFind.html',
        'need_back': True
    }}



@app.route('/')
def index():
    return render_template('GeneralList.html',
                           content=lambda: (('', menuItems[x]['title'], x) for x in menuItems.keys()),
                           title='Vacancies web-site', after_line=False)


@app.route('/favicon.ico/')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static')+'/img', 'favicon.ico',
                                            mimetype='image/vnd.microsoft.icon')

@app.route('/institutions/', methods=['GET'])
def institutions():
    if 'id' in request.args.keys():
        inst = con.institutions(iid=request.args['id'])
        return render_template('GeneralSingleElement.html', title=inst[1], content=[
            {'type': 'line', 'data': [{'text': 'address:'}, *({'text': x} for x in inst[2:])]},
            {'type': 'line', 'data': [{'text': 'edit', 'link': 'edit'}]},
            {'type': 'line', 'data': [{'text': 'remove', 'link': 'remove'}]}
        ])
    insts = con.institutions()

    return render_template('error.html', message='wring')


@app.route('/<path>/')
def default_routing(path):
    items = menuItems.keys()
    if path in items:
        params = menuItems[path]
        return render_template(params['page'], **params)
    else:
        return render_template('error.html', message='something went wrong')


@app.route('/vacancy_<vid>/')
def detailed_vacancy(vid):
    if int(vid) in con.id_check('vacancy'):
        vac_info, requirements = con.detailed_vacancy(int(vid))
        print(requirements)
        content = [
            {'type': 'line', 'data': [{'text': x} for x in vac_info[:3]]},
        ]
        if vac_info[3]:
            content.append(
                {'type': 'line', 'data': [{'text': 'Description: {}'.format(vac_info[3])}]})
        content.extend([
            {'type': 'line', 'data': [{'text': 'Requirements: '}]},
            {'type': 'list', 'data': [[{'text': 'education: {}, work experience: {}'.format(req[0], req[1])}] for req in requirements]},
            {'type': 'list', 'data': [
                [{'link': l, 'text': t}] for (t, l) in {'add requirement': 'newreq',
                                                                             'edit vacancy': 'edit',
                                                                             'remove vacancy': 'remove'}.items()]}
        ])
        return render_template('GeneralSingleElement.html', vac_info=vac_info, requirements=requirements,
                               content=content, title='vacancy')
    else:
        render_template('error.html', message='no vacancy')


@app.route('/List of people/')
def people():
    return render_template('GeneralList.html',
                           title='People, looking for employment',
                           content=lambda: ((x[1:], '(details)', 'person/?p=' + str(x[0])) for x in con.all_people()),
                           need_back=True,
                           after_line=False)


@app.route('/company/', methods=['GET', 'POST'])
def company():
    cid = request.args['id']
    comp = con.companies(cid=cid)
    if 'f' in request.args.keys():
        op = request.args['f']
        print(op)
        if op == 'edit':
            pos = [
                Position(description='Name', type='text', name='name', value=comp[1]),
                Position(description='Address', type='text', name='address', value=comp[2]),
                Position(description='City', type='text', name='city', value=comp[3])
            ]
            return render_template('GeneralForm.html', action='?id={}&f=update'.format(cid),
                                   positions=pos,
                                   hidden={'name': 'id', 'value': comp[0]},
                                   title='Editing {}'.format(comp[1]))
        if op == 'update':
            id = request.form['id']
            name = request.form['name']
            city = request.form['city']
            address = request.form['address']
            con.update_company(id, name, city=city, address=address)
            return redirect('/company/?id={}'.format(id))
        if op == 'remove':
            con.remove_company(cid=cid)
            return redirect('/Companies')
    else:
        return render_template('GeneralSingleElement.html', title=comp[1], content=[
            {'type': 'line', 'data': [{'text': x} for x in comp[1:]]},
            {'type': 'line', 'data': [{'text': 'edit', 'link': '?id={}&f=edit'.format(str(cid))}]},
                {'type': 'line', 'data': [{'text': 'remove', 'link': '?id={}&f=remove'.format(str(cid))}]}
        ])


@app.route('/person/', methods=['GET'])
def person():
    a = int(request.args['p'])
    person = con.person(a)
    content = [{
        'type': 'line', 'data': [{'text': 'Name:'}, {'text': person[0][0][0]}]
    }]
    if len(person[1]) > 0:
        content.extend([{
            'type': 'line', 'data': [{'text': 'Education:'}]
        },
            {
                'type': "list", 'data': [({'text': x[1], 'link': '/institutions/?id=' + str(x[0])},
                                          {'text': x[4] + ' of ' + x[5] + ','},
                                          {'text': 'from ' + str(x[6]) + ' , graduated at ' + str(x[7])}) for x in
                                         person[1]]
            }])
    if len(person[2]) > 0:
        content.extend([
            {'type': 'line', 'data': [{'text': 'Work experience:'}]}, {
                'type': "list", 'data': [({'text': x[1], 'link': '/company/?id=' + str(x[0])},
                                          {'text': x[2] + ','},
                                          {'text': 'from ' + str(x[3]) + ' , to ' + str(x[4])}) for x in
                                         person[2]]
            }
        ])
    return render_template('GeneralSingleElement.html', title=person[0][0][0], content=content)


@app.route('/vacancy_<vid>/<operation>', methods=['GET', 'POST'])
def new_requirement(vid, operation):
    if operation == 'newreq':
        return render_template('new_requirement.html', vid=vid)

    elif operation == 'remove':
        con.remove_vacancy(vid=vid)
        return redirect('/showVacancies')

    elif operation == 'edit':
        vac_info, _ = con.detailed_vacancy(int(vid))
        companies_names = (x[1] for x in con.companies())
        pos = [
            Position(description='Position', type='text', name='position', value=vac_info[2]),
            Position(description='Description', type='text', name='description', value=vac_info[3]),
            Position(description='Salary', type='number', name='salary', value=int(vac_info[1])),
            SelectPosition(description='Company', name='company', value=vac_info[0], content=lambda: companies_names)
        ]
        return render_template('GeneralForm.html', action='update', positions=pos)

    elif operation == 'update':
        company = request.form['company']
        salary = request.form['salary']
        position = request.form['position']
        description = request.form['description']
        if con.update(vid, company, salary, position, description):
            return render_template('error.html', message='cant be updated')
        else:
            return redirect('/vacancy_' + vid)
    else:
        return render_template('error.html', message='incorrect operation')


@app.route('/add_vacancy', methods=['POST'])
def add_vacancy():
    if request.method == 'POST':
        company = request.form['company']
        salary = request.form['salary']
        position = request.form['position']
        description = request.form['description']
        try:
            con.add_vacancy(vacancy(comp_name=company, salary=salary, description=description, position=position))
            return redirect('/showVacancies')
        except:
            return render_template('error.html', message='Failed to add vacancy')


@app.route('/add_requirement', methods=['POST'])
def add_requirement():
    if request.method == 'POST':
        vid = request.form['addr']
        ed = request.form['education']
        ex = request.form['experience']
        try:
            con.add_requirement(vid=vid, education=ed, experience=ex)
            return redirect('/vacancy_' + vid)
        except:
            return render_template('error.html', message='Failed to add requirement')


@app.route('/FindPerson/res/', methods=['GET'])
def find_person():
    education = request.args['education']
    exp = request.args['work']
    if education == '-':
        education = False
    if exp == '-':
        exp = False
    if exp is False and education is False:
        res = con.all_people()
    else:
        res = con.all_people(filtering=[education,exp])
    m = menuItems['FindPerson']
    return render_template(m['page'], **m, find_res=res)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
