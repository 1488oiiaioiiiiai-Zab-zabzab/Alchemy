from flask import Flask, render_template, redirect, request, abort
import sqlite3
from data import db_session
from data.users_py import UserC
from data.jobs_py import JobsC
from data.departments_py import DepartmentC
from forms.users_forms import RegisterForm, LoginForm
from forms.job_forms import AddJobForm
from forms.dep_forms import AddDepForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

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


@app.route("/deps")
def tables_with_deps():
    session = db_session.create_session()
    deps = session.query(DepartmentC).all()
    return render_template("tables_deps.html", jobs=deps)

@app.route("/adddep", methods=['GET', 'POST'])
@login_required
def adddep():
    try:
        form = AddDepForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            try:
                if not db_sess.query(UserC).filter(UserC.id == int(form.chief.data)).first():
                    return render_template('add_dep.html', title='Добавление Департамента',
                                           form=form,
                                           message="Шеф указан не верно, такого пользователя нет")
            except ValueError:
                return render_template('add_dep.html', title='Добавление Департамента',
                                       form=form,
                                       message="Щеф это int")
            try:
                for x in form.members.data.split(", "):
                    if not db_sess.query(UserC).filter(UserC.id == int(x)).first():
                        return render_template('add_dep.html', title='Добавление Департамента',
                                               form=form,
                                               message=f"Участник {x} указан не верно, такого пользователя нет")
            except ValueError:
                return render_template('add_dep.html', title='Добавление Департамента',
                                       form=form,
                                       message="Участник это int")
            print(True)
            dep = DepartmentC()
            dep.title=form.title.data
            dep.members=form.members.data
            dep.chief=form.chief.data
            dep.email=form.email.data
            try:
                dep.users_orm_rel=current_user
                current_user.deps_orm_rel.append(dep)
                db_sess.merge(current_user)
            except Exception as e:
                print(e)
                try:
                    dep.users_orm_rel = current_user
                except Exception as e:
                    print(e)
                    try:
                        current_user.deps_orm_rel.append(dep)
                        db_sess.merge(current_user)
                    except Exception as e:
                        print(e)
                        pass
                try:
                    current_user.deps_orm_rel.append(dep)
                    db_sess.merge(current_user)
                except Exception as e:
                    print(e)
                    try:
                        dep.users_orm_rel = current_user
                    except Exception as e:
                        print(e)
                        pass
            print(True)
            db_sess.add(dep)
            db_sess.commit()
            print(True)
            return redirect('/deps')
        return render_template('add_dep.html', title='Добавление Департамента', form=form)
    except Exception as e:
        return render_template('add_dep.html', title='Добавление Департамента', form=form,
                               messege=f"Алхимия ругается на orm rel: {e} \n потыкайте на кнопку отправки формы несколько раз \n может помочь")



@app.route("/reddep/<int:id>", methods=['GET', 'POST'])
@login_required
def reddep(id):
    print("""""")
    form = AddDepForm()
    db_sess = db_session.create_session()
    dep = db_sess.query(DepartmentC).filter(DepartmentC.id == id).first()
    if not dep:
        print("департимент не найден")
        abort(404)
    else:
        if request.method == "GET":
            if current_user.id == 1 or dep.users_orm_rel == current_user:
                form.title.data = dep.title
                form.members.data = dep.members
                form.email.data = dep.email
                form.chief.data = dep.chief
            else:
                print(2)
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            try:
                if not db_sess.query(UserC).filter(UserC.id == int(form.chief.data)).first():
                    return render_template('add_dep.html', title='Редактирование Департамента',
                                           form=form,
                                           message="Шеф указан не верно, такого пользователя нет")
            except ValueError:
                return render_template('add_dep.html', title='Редактирование Департамента',
                                       form=form,
                                       message="Щеф это int")
            try:
                for x in form.members.data.split(", "):
                    if not db_sess.query(UserC).filter(UserC.id == int(x)).first():
                        return render_template('add_dep.html', title='Редактирование Департамента',
                                               form=form,
                                               message=f"Участник {x} указан не верно, такого пользователя нет")
            except ValueError:
                return render_template('add_dep.html', title='Редактирование Департамента',
                                       form=form,
                                       message="Участник это int")
            dep = db_sess.query(DepartmentC).filter(DepartmentC.id == id).first()
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            dep.chief = form.chief.data
            print(dep.title, dep.members, dep.email, dep.chief)
            db_sess.commit()
            return redirect('/deps')
        return render_template('add_dep.html', title='Редактирование Департамента', form=form)


@app.route("/deldep/<int:id>")
@login_required
def deldep(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(DepartmentC).filter(DepartmentC.id == id).first()
    if dep and (current_user == dep.users_orm_rel or current_user.id == 1):
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/deps")


@app.route("/r/<int:id>", methods=['GET', 'POST'])
@login_required
def redjob(id):
    form = AddJobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(JobsC).filter(JobsC.id == id).first()
    if not job:
        print(1)
        abort(404)
    else:
        if request.method == "GET":
            if current_user.id == 1 or job.users_orm_rel == current_user:
                form.jn.data = job.job
                print(job.job)
                form.ws.data = job.work_size
                print(job.work_size)
                form.n.data = job.start_date
                print(job.start_date, job.end_date, job.collaborators, job.is_finished)
                form.c.data = job.end_date
                form.col.data = job.collaborators
                form.f.data = job.is_finished
                form.tl.data = job.team_leader
            else:
                print(2)
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            job = db_sess.query(JobsC).filter(JobsC.id == id).first()
            if job:
                try:
                    if not db_sess.query(UserC).filter(UserC.id == int(form.tl.data)).first():
                        return render_template('add_job.html', title='Редактирование работы',
                                               form=form,
                                               message="Тимлидер указан не верно, такого пользователя нет")
                except ValueError:
                    return render_template('add_job.html', title='Редактирование работы',
                                           form=form,
                                           message="Тимлид это int")
                try:
                    for x in form.col.data.split(", "):
                        if not db_sess.query(UserC).filter(UserC.id == int(x)).first():
                            return render_template('add_job.html', title='Редактирование работы',
                                                   form=form,
                                                   message=f"Помощник {x} указан не верно, такого пользователя нет")
                except ValueError:
                    return render_template('add_job.html', title='Редактирование работы',
                                           form=form,
                                           message="Помощник это int")

                try:
                    ws = int(form.ws.data)
                except ValueError:
                    return render_template('add_job.html', title='Редактирование работы',
                                           form=form,
                                           message="Время работы это int")
                job.job = form.jn.data
                job.work_size = ws
                job.team_leader = int(form.tl.data)
                job.collaborators = form.col.data
                job.is_finished = form.f.data
                _id = job.id
                print(_id)
                db_sess.commit()
                con = sqlite3.connect("db/alch1.db")
                cur = con.cursor()
                cur.execute(f"""UPDATE table_jobs SET start_date = datetime("{form.n.data}") WHERE id ={_id} """)
                cur.execute(f"""UPDATE table_jobs SET end_date = datetime("{form.c.data}") WHERE id ={_id} """)
                con.commit()
                con.close()
                return redirect('/')
            else:
                print(3)
                abort(404)
        return render_template('add_job.html', title='Редактирование работы', form=form)


@app.route("/deljob/<int:id>")
@login_required
def deljob(id):
    db_sess = db_session.create_session()
    job = db_sess.query(JobsC).filter(JobsC.id == id).first()
    if job and (job.users_orm_rel == current_user or current_user.id == 1):
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    try:
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

            job = JobsC(
                job=form.jn.data,
                work_size=ws,
                team_leader=int(form.tl.data),
                collaborators=form.col.data,
                is_finished=form.f.data
            )
            job.users_orm_rel=current_user
            db_sess.add(job)
            db_sess.commit()
            _id = db_sess.query(JobsC).all()[-1].id
            print(_id)
            con = sqlite3.connect("db/alch1.db")
            cur = con.cursor()
            cur.execute(f"""UPDATE table_jobs SET start_date = datetime("{form.n.data}") WHERE id ={_id} """)
            cur.execute(f"""UPDATE table_jobs SET end_date = datetime("{form.c.data}") WHERE id ={_id} """)
            con.commit()
            job = db_sess.query(JobsC).all()[-1]
            try:
                job.users_orm_rel = current_user
                current_user.jobs_orm_rel.append(job)
                db_sess.merge(current_user)
            except Exception as e:
                print(e)
                try:
                    job.users_orm_rel = current_user
                except Exception as e:
                    print(e)
                    try:
                        current_user.jobs_orm_rel.append(job)
                        db_sess.merge(current_user)
                    except Exception as e:
                        print(e)
                        pass
                try:
                    current_user.jobs_orm_rel.append(job)
                    db_sess.merge(current_user)
                except Exception as e:
                    print(e)
                    try:
                        job.users_orm_rel = current_user
                    except Exception as e:
                        print(e)
                        pass
            db_sess.commit()
            con.close()
            return redirect('/')
        return render_template('add_job.html', title='Добавление работы', form=form)
    except Exception as e:
        return render_template('add_job.html', title='Добавление работы', form=form,
                               messege=f"Алхимия ругается на orm rel: {e} \n потыкайте на кнопку отправки формы несколько раз \n может помочь")

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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    main()
