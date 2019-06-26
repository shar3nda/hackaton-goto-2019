from flask import Flask, flash, redirect, render_template, request, session
import os
from sheets_parser import parse
from algorithm import houses_disp, activity
import re
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('template.html', my_string="Добро пожаловать на сайт распределения",
                               my_list=["Расселение детей по домам",
                                        "Распределение по отрядам", "Создание команд для вечерних активностей"])


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect('/')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route('/siteinfo')
def siteinfo():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('information.html')


@app.route('/resettlement', methods=['POST', 'GET'])
def resettlement():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            houses = request.form.get('houses')
            houses = houses.split()
            h = {}
            for i in range(len(houses)):
                tmp, tmp2 = map(int, houses[i].split("-"))
                h[tmp2] = tmp
            data = parse()
            houses_string = houses_disp(data, h)
            print(houses_string)
            return render_template('resettlement.html')
        else:
            return render_template('resettlement.html')


@app.route('/candle')
def candle():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('candle.html')


@app.route('/activities', methods=['POST', 'GET'])
def activities():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            teams = request.form.get('teams')
            string = activity(parse(), int(teams))
            print(string)
        return render_template('activities.html')


@app.route('/settings')
def settings():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('settings.html')


@app.route('/piece')
def piece():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('piece.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
