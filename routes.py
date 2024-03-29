#this module contains all the routes for the app

from app import app , db
from flask import render_template, redirect , url_for , flash , get_flashed_messages # render_template is used to get render html pages
import forms # this imports the forms.py code here
# this tells the app that at '/' we need to run index()
from models import Task
from datetime import datetime



@app.route('/') #this is the decorator to the function index()
@app.route('/index',methods=['GET','POST']) # you can add more than one routes 
def index():
	tasks=Task.query.all()
	return render_template('index.html',current_title='NEW TITLE',tasks=tasks)
    # here you can add the required html and pass values to the html . We can use {{ }} to use passed values in the html file

@app.route('/add', methods=['GET','POST'])
def add():
    
	form=forms.AddTaskForm() # this creates instance of class AddTaskForm 

	if form.validate_on_submit():

		t=Task(title=form.title.data,date=datetime.utcnow())
		db.session.add(t)
		db.session.commit()
		flash('Task added successfully')
		return redirect(url_for('index'))

	return render_template('add.html',form=form,title='ABOUT') # the from is passed to the page using form variable

@app.route('/edit/<int:task_id>',methods=['GET','POST'])
def edit(task_id):
	task=Task.query.get(task_id)
	form=forms.AddTaskForm()
	
	if task:
		if form.validate_on_submit():
			task.title=form.title.data
			task.date=datetime.utcnow()
			db.session.commit()
			flash('Task Updated Successfully')
			return redirect(url_for('index'))

		form.title.data = task.title
		return render_template('edit.html',form=form,task_id=task_id)
	
	else:
		flash('Task Not Found')
	
	return redirect(url_for('index'))



@app.route('/delete/<int:task_id>',methods=['GET','POST'])
def delete(task_id):
	task=Task.query.get(task_id)
	form=forms.DeleteTaskForm()
	
	if task:
		if form.validate_on_submit():
			db.session.delete(task)
			db.session.commit()
			flash('Task Deleted Successfully')
			return redirect(url_for('index'))

	
		return render_template('delete.html',form=form,task_id=task_id,title=task.title)
	else:
		flash('Task Not Found')
	
	return redirect(url_for('index'))
