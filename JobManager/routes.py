from flask import Flask, url_for, render_template, redirect, flash, request, abort, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message, Mail
from JobManager.forms import LoginForm, RegistrationForm, PostForm, ApplyForm, SearchForm
from JobManager.models import User, Job
from JobManager.__init__ import app, bcrypt, db, mail, socketio
from flask_socketio import SocketIO, send
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
import os
from oauthlib.oauth2 import WebApplicationClient
import requests

twitter_blueprint = make_twitter_blueprint(api_key='Wxheh706myGRPdIzg1UG8NCmD', api_secret='z2gPTdT8v1pCTNEX7xxtf0bbqLwLJgfiqgdgDa03GTf7M5m13T')
app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in successfully with {form.email.data}.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect Username or Password. Please try again.', 'danger ')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/features")
def features():
    return render_template('features.html')


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, description=form.description.data, experience=form.experience.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/faq")
def faq():
    return render_template('faq.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/candidates")
@login_required
def candidates():
    users = User.query.order_by(User.id)
    return render_template('portfolio.html', users=users)


@app.route("/user_<string:username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Job.query.filter_by(author=user).order_by(Job.date_posted.desc())
    return render_template('user_profile.html', jobs=jobs, user=user)

@app.route("/post_job", methods=['GET', 'POST'])
@login_required
def post_job():
    form = PostForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, job_content=form.job_content.data, job_experience=form.job_experience.data,
                  author=current_user, location=form.location.data, type=form.type.data, tag=form.tag.data, website=form.website.data, close=form.close.data)
        db.session.add(job)
        db.session.commit()
        flash(f'Created Job {form.title.data}!', 'success')
        return redirect(url_for('all_jobs'))
    return render_template('post_job.html', form=form)


@app.route("/apply_<string:job_id>", methods=['GET', 'POST'])
@login_required
def apply(job_id):
    joba = Job.query.get_or_404(job_id)
    form = ApplyForm()
    email = form.email.data
    msg = Message(f'Name: {form.name.data} Email: {form.email.data} Applying for {joba.title }Why {form.name.data} should get the job: {form.apply.data}', sender=email, recipients=['babhinav.117@gmail.com'])
    if form.validate_on_submit():
        mail.send(msg)
        flash('Applied for this job!', 'success')
        return redirect(url_for('all_jobs'))
    return render_template('apply.html', form=form, joba=joba)


@app.route("/send_mail", methods=["GET", "POST"])
def send_mail():
    msg = Message('Test Message IAjijIJIjIAJIJAI', sender=['babhinav.117@gmail.com'], recipients=['babhinav.117@gmail.com'])
    mail.send(msg)
    flash(f'Sent messsage to babhinav.117@gmail.com!', 'success')


@app.route("/job_<string:job_id>")
@login_required
def job(job_id):
    job = Job.query.get_or_404(job_id)
    print(job.title)
    return render_template('job.html', job=job)


@app.route("/termsofuse")
def termsofuse():
    return render_template('termsofuse.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/buy')
def buy():
    flash('Bought memebership!', 'success')
    return redirect(url_for('index'))


@app.route("/all_jobs", methods=['GET', 'POST'])
@login_required
def all_jobs():
    jobs = Job.query.order_by(Job.date_posted.desc())
    return render_template('all_jobs.html', jobs=jobs)


@app.route("/account")
@login_required
def account():
    return render_template('account.html')


@app.route("/credit_card")
@login_required
def credit_card():
    return render_template('credit_card.html')


@socketio.on('message')
def handle_message(msg):
    flash(msg, 'success')
    send(msg, broadcast=True)

#twitter_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    account_info = twitter.get('account/settings.json')
    account_info_json = account_info.json()

    flash('<h1>Your Twitter name is @{}'.format(account_info_json['screen_name']), 'success')


@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):

    account_info = blueprint.session.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['screen_name']

        query = User.query.filter_by(username=username)

        try:
            user = query.all()
        except NoResultFound:
            user = User(username=username, email=os.urandom(5)+'@gmail.com', password=os.urandom(10))
            db.session.add(user)
            db.session.commit()

        login_user(user)

        return redirect(url_for('index'))



GOOGLE_CLIENT_ID = "729359465370-2lecb3omgnvnqt62mpt8s4m6m5qfi98n.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "amv7zkPAVQCFjK9dPE7AI4-L"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/google_login")
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/google_login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400


    user = User(
        username=users_name, email=users_email, password=os.urandom(10)
    )



    if not User.query.get(users_name):
        user = User(
            username=users_name, email=users_email, password=os.urandom(10), picture=picture, description=unique_id
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for("index"))

