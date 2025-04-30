from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Advice, Comment
from app.classes.forms import AdviceForm, CommentForm
from flask_login import login_required
import datetime as dt


@app.route('/advice/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def adviceNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = AdviceForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new advice form. 
        # Advice() is a mongoengine method for creating a new advice. 'newAdvice' is the variable 
        # that stores the object that is the result of the Advice() method.  
        newAdvice = Advice(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            topic = form.topic.data,
            question = form.question.data,
            priority = form.priority.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newAdvice.save()

        # Once the new advice is saved, this sends the user to that advice using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a advice so we want 
        # to send them to that advice. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('advice',adviceID=newAdvice.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at adviceform.html to 
    # see how that works.
    return render_template('adviceform.html',form=form)

@app.route('/advice/<adviceID>', methods=['GET', 'POST'])
@login_required
def advice(adviceID):
    editAdvice = Advice.objects.get(id=adviceID)
    # if the user that requested to edit this advice is not the author then deny them and
    # send them back to the advice. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editAdvice.author:
        flash("You can't edit an advice you don't own.")
        return redirect(url_for('advice',adviceID=adviceID))
    # get the form object
    form = AdviceForm()
    # If the user has submitted the form then update the advice.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editAdvice.update(
            topic = form.topic.data,
            question = form.question.data,
            priority = form.priority.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated advice using a redirect.
        return redirect(url_for('advice',adviceID=adviceID))

    # if the form has NOT been submitted then take the data from the editAdvice object
    # and place it in the form object so it will be displayed to the user on the template.
    form.topic.data = editAdvice.topic
    form.question.data = editAdvice.question
    form.priority.data = editAdvice.priority


    # Send the user to the advice form that is now filled out with the current information
    # from the form.
    return render_template('adviceform.html',form=form)

@app.route('/advice/list')
@app.route('/advices')
# This means the user must be logged in to see this page
@login_required
def adviceList():
    # This retrieves all of the 'advices' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'advices'.
    advices = Advice.objects()
    # This renders (shows to the user) the advices.html template. it also sends the advices object 
    # to the template as a variable named advices.  The template uses a for loop to display
    # each advice.
    return render_template('advices.html',advices=advices)

@app.route('/advice/edit/<adviceID>', methods=['GET', 'POST'])
@login_required
def adviceEdit(adviceID):
    editAdvice = Advice.objects.get(id=adviceID)
    # if the user that requested to edit this advice is not the author then deny them and
    # send them back to the advice. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editAdvice.author:
        flash("You can't edit a advice you don't own.")
        return redirect(url_for('advice',adviceID=adviceID))
    # get the form object
    form = AdviceForm()
    # If the user has submitted the form then update the advice.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editAdvice.update(
            topic = form.topic.data,
            question = form.question.data,
            priority = form.priority.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated advice using a redirect.
        return redirect(url_for('advice',adviceID=adviceID))

    # if the form has NOT been submitted then take the data from the editAdvice object
    # and place it in the form object so it will be displayed to the user on the template.
    form.topic.data = editAdvice.topic
    form.question.data = editAdvice.question
    form.priority.data = editAdvice.priority


    # Send the user to the advice form that is now filled out with the current information
    # from the form.
    return render_template('adviceform.html',form=form)

@app.route('/comments/new/<adviceID>', methods=['GET', 'POST'])
@login_required
def commentsNew(adviceID):
    advice = Advice.objects.get(id=adviceID)
    form = CommentForm()
    if form.validate_on_submit():
        newComment = Comment(
            author = current_user.id,
            advice = adviceID,
            question = form.question.data
        )
        newComment.save()
        return redirect(url_for('advice',adviceID=adviceID))
    return render_template('commentform.html',form=form,advice=advice)

@app.route('/comments/edit/<commentID>', methods=['GET', 'POST'])
@login_required
def commentsEdit(commentID):
    editComment = Comment.objects.get(id=commentID)
    if current_user != editComment.author:
        flash("You can't edit a comment you didn't write.")
        return redirect(url_for('advice',adviceID=editComment.advice.id))
    advice = Advice.objects.get(id=editComment.advice.id)
    form = CommentForm()
    if form.validate_on_submit():
        editComment.update(
            question = form.question.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('advice',adviceID=editComment.advice.id))

    form.question.data = editComment.question

    return render_template('commentform.html',form=form,advice=advice)   

@app.route('/comments/delete/<commentID>')
@login_required
def commentsDelete(commentID): 
    deleteComment = Comment.objects.get(id=commentID)
    deleteComment.delete()
    flash('The comments was deleted.')
    return redirect(url_for('advice',adviceID=deleteComment.advice.id)) 

