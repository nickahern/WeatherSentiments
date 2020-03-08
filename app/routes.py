from app import app
from flask import render_template, flash, redirect
from app.forms import PredictionForm

from flask import render_template
from app import app
from twitterClient import TwitterClient

client = TwitterClient()

@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def main():
    form = PredictionForm()
    if form.validate_on_submit():
        prediction = client.predict(form.precip.data, form.snow.data, form.tavg.data, form.tmax.data, form.tmin.data)
        flash('Login requested for user {}, remember_me={}, {}'.format(
            form.precip.data, form.snow.data, love))
        return redirect('/main')
    return render_template('index.html', form=form)