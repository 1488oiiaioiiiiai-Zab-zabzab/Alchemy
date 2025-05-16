from flask import Flask, render_template, redirect, request
from data import db_session
from data.users_py import UserC
from data.jobs_py import JobsC
from data.departments_py import DepartmentC
from forms.users_forms import RegisterForm, LoginForm
from forms.job_forms import AddJobForm
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(UserC).get(user_id)


def main():
    db_session.global_init("db/alch1.db")
    app.run()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(UserC).filter(UserC.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def tables_with_jobs():
    session = db_session.create_session()
    jobs = session.query(JobsC).all()
    return render_template("tables_jobs.html", jobs=jobs)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            if not db_sess.query(UserC).filter(UserC.id == int(form.tl.data)).first():
                return render_template('add_job.html', title='Добавление работы',
                                       form=form,
                                       message="Тимлидер указан не верно, такого пользователя нет")
        except ValueError:
            return render_template('add_job.html', title='Добавление работы',
                                   form=form,
                                   message="Тимлид это int")
        try:
            for x in form.col.data.split(", "):
                if not db_sess.query(UserC).filter(UserC.id == int(x)).first():
                    return render_template('add_job.html', title='Добавление работы',
                                           form=form,
                                           message=f"Помощник {x} указан не верно, такого пользователя нет")
        except ValueError:
            return render_template('add_job.html', title='Добавление работы',
                                   form=form,
                                   message="Помощник это int")

        try:
            ws = int(form.ws.data)
        except ValueError:
            return render_template('add_job.html', title='Добавление работы',
                                   form=form,
                                   message="Время работы это int")
        rs = True if "on" in request.form.getlist("rare") else False

        user = JobsC(
            job=form.jn.data,
            work_size=ws,
            team_leader=int(form.tl.data),
            collaborators=form.col.data,
            start_date=form.n.data,
            end_date=form.c.data,
            is_finished=rs
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(UserC).filter(UserC.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        try:
            age = int(form.age.data)
        except ValueError:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Возраст это int")
        user = UserC(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            position=form.position.data,
            speciality=form.speciality.data,
            age=age,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    main()
