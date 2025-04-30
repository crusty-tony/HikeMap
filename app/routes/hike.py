from app import app
from app.utils.secrets import getSecrets
import requests
from flask import render_template, flash, redirect, url_for
import requests
from flask_login import current_user
from app.classes.data import Hike
from app.classes.forms import HikeForm
from flask_login import login_required
import datetime as dt


@app.route('/hike/map')
@login_required
def hikeMap():

    hikes = Hike.objects()

    return render_template('hikelocator.html',hikes=hikes)

@app.route('/hike/list')
@login_required
def hikeList():

    hikes = Hike.objects()

    return render_template('hikes.html',hikes=hikes)


@app.route('/hike/<hikeID>')
@login_required
def hike(hikeID):

    thisHike = Hike.objects.get(id=hikeID)

    return render_template('hike.html',hike=thisHike)


@app.route('/hike/delete/<hikeID>')
@login_required
def hikeDelete(hikeID):
    deleteHike = Hike.objects.get(id=hikeID)

    deleteHike.delete()
    flash('The Hike was deleted.')
    return redirect(url_for('hikeList'))

def updateLatLon(hike):
    # get your email address for the secrets file
    secrets=getSecrets()
    # call the maps API with the address
    url = f"https://nominatim.openstreetmap.org/search?street={hike.streetAddress}&city={hike.city}&state={hike.state}&postalcode={hike.zipcode}&format=json&addressdetails=1&email={secrets['MY_EMAIL_ADDRESS']}"
    # get the response from the API
    r = requests.get(url)
    # Find the lat/lon in the response
    try:
        r = r.json()
    except:
        flash("unable to retrieve lat/lon")
        return(hike)
    else:
        if len(r) != 0:
            # update the database
            hike.update(
                lat = float(r[0]['lat']),
                lon = float(r[0]['lon'])
            )
            flash(f"hike lat/lon updated")
            return(hike)
        else:
            flash('unable to retrieve lat/lon')
            return(hike)

@app.route('/hike/new', methods=['GET', 'POST'])
@login_required
def hikeNew():
    form = HikeForm()

    if form.validate_on_submit():

        newHike = Hike(
            name = form.name.data,
            streetAddress = form.streetAddress.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            description = form.description.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow,
        )
        newHike.save()

        newHike = updateLatLon(newHike)

        import requests

        return redirect(url_for('hike',hikeID=newHike.id))

    return render_template('hikeform.html',form=form)

@app.route('/hike/edit/<hikeID>', methods=['GET', 'POST'])
@login_required
def hikeEdit(hikeID):
    editHike = Hike.objects.get(id=hikeID)

    if current_user != editHike.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('hike',hikeID=hikeID))

    form = HikeForm()
    if form.validate_on_submit():
        editHike.update(
            name = form.name.data,
            streetAddress = form.streetAddress.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,            
            description = form.description.data,
            modifydate = dt.datetime.utcnow,
        )
        editHike = updateLatLon(editHike)
        return redirect(url_for('hike',hikeID=hikeID))

    form.name.data = editHike.name
    form.streetAddress.data = editHike.streetAddress
    form.city.data = editHike.city
    form.state.data = editHike.state
    form.zipcode.data = editHike.zipcode
    form.description.data = editHike.description

    return render_template('hikeform.html',form=form)
