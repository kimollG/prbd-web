from flask import Flask, request, Response, render_template, url_for
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
        'content': lambda: ((x, None, None) for x in companiesFilter(con.companies)),
        'page': 'GeneralList.html',
        'title': 'Companies',
        'need_back': True},
    'Aggregated': {
        'content': con.aggregate,
        'page': 'aggregated.html',
        'title': 'General data'},
    'NewVacancy': {'action': 'new_vacancy',
                   'positions': [
                        Position(description='Position', type='text', name='position'),
                        Position(description='Description', type='text', name='description'),
                        Position(description='Salary', type='number', name='salary'),              # companies names
                        SelectPosition(description='Company', name='company',
                                       content=lambda: (x[1] for x in con.companies()))
                   ],
                   'title': 'Add new vacancy',
                   'page': 'GeneralForm.html'},
    'ShowVacancies': {'content': lambda: ((x[0], '(details)', 'vacancy_'+str(x[1])) for x in con.vacancies()),
                      'title': 'Available vacancies',
                      'page': 'GeneralList.html',
                      'need_back': True},
    'List of people': {'FOO': lambda: generalFilter(con.all_people(), 1, isReducing=True),
                       'title':'People, looking for job'}}


@app.route('/')
def index():
    return render_template('GeneralList.html',
                           content=lambda: (('', menuItems[x]['title'], x) for x in menuItems.keys()),
                           title='Vacancies web-site')


@app.route('/favicon.ico/')
def favicon():
    return 'aaaa'


@app.route('/<path>/')
def default_routing(path):
    # print(path)
    # dcompare(path,'aggregated')
    items = menuItems.keys()
    if path in items:
        params = menuItems[path]
        return render_template(params['page'], **params)
    else:
        -1  # render_template('error.html',message = '404')


@app.route('/vacancy_<vid>/')
def detailed_vacancy(vid):
    if int(vid) in con.id_check('vacancy'):
        vac_info, requirements = con.detailed_vacancy(int(vid))
        print(requirements)
        return render_template('GeneralSingleElement.html', vac_info=vac_info, requirements=requirements, title='vacancy')
    else:
        render_template('error.html', message='no vacancy')
    # except:
    #     render_template('error.html', message='no vacancy')


@app.route('/List of people/')
def people():
    return render_template('GeneralList.html',
                           title='People, looking for employment',
                           content=lambda: ((x[1:], '(details)', 'person/?p=' + str(x[0])) for x in con.all_people()),
                           need_back=True)


@app.route('/person/', methods=['GET'])
def person():
    a = int(request.args['p'])
    person = con.person(a)
    render_template()

    return render_template('error.html', message='oops')


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
            SelectPosition(description='Company', name='company', value=vac_info[0],  content=lambda:companies_names)
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
