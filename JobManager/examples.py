from flask import Flask, url_for, render_template, redirect, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message, Mail
from JobManager.forms import LoginForm, RegistrationForm, PostForm, ApplyForm
from JobManager.models import User, Job
from JobManager.__init__ import app, bcrypt, db, mail

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route("/home")
def home():
    jobs = Job.query.order_by(Job.date_posted.desc())
    return render_template('home.html', jobs=jobs)


@app.route("/apply", methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyForm()
    email = form.email.data
    name = form.name.data
    apply = form.apply.data
    msg = Message(f'Name: {form.name.data} Email: {form.email.data} Why {form.name.data} should get the job: {form.apply.data}', sender=email, recipients=['babhinav.117@gmail.com'])
    if form.validate_on_submit():
        mail.send(msg)
        flash('Applied for this job!', 'success')
        return redirect(url_for('all_jobs'))
    return render_template('apply.html', form=form)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Job.query.filter_by(author=user) \
        .order_by(Job.date_posted.desc())
    return render_template('user_posts.html', jobs=jobs, user=user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in successfully with {form.email.data}.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Username or Password. Please try again.', 'danger ')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/all_jobs")
@login_required
def all_jobs():
    jobs = Job.query.order_by(Job.date_posted.desc())
    return render_template('all_jobs.html', jobs=jobs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('home'))


@app.route("/jobs/new", methods=['GET', 'POST'])
@login_required
def new_job():
    form = PostForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, job_content=form.job_content.data, job_experience=form.job_experience.data, author=current_user)
        db.session.add(job)
        db.session.commit()
        flash(f'Created Job {form.title.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_job.html', form=form)


@app.route("/job/<int:job_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.job_content = form.job_content.data
        job.job_experience = form.job_experience.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('dashboard', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.job_content.data = job.job_content
        form.job_experience.data = job.job_experience
    return render_template('new_job.html', form=form)


@app.route("/job/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_post(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500