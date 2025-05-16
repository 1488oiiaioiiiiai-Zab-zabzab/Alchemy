from flask import Flask, render_template, redirect
from data import db_session
from data.users_py import UserC
from data.jobs_py import JobsC
from data.departments_py import DepartmentC
from forms.users_forms import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/alch1.db")
    app.run()


@app.route("/")
def tables_with_jobs():
    session = db_session.create_session()
    jobs = session.query(JobsC).all()
    return render_template("tables_jobs.html", jobs=jobs)


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


if __name__ == "__main__":
    main()
