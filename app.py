from flask import Flask, render_template, url_for, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///john_website.db'		# Tells app where the database is located

with app.app_context():
	db = SQLAlchemy(app)	# todo database intialization.

class Todo(db.Model):
	"""Class for task 'to do' object"""
	id = db.Column(db.Integer, primary_key=True) 	# Integer that references the ID of each entry.
	content	= db.Column(db.String(200), nullable=False)	# Holds content for each task.
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id

class Grocery(db.Model):
	"""Class for Grocery item object"""
	id = db.Column(db.Integer, primary_key=True) 	# Integer that references the ID of each entry.
	description	= db.Column(db.String(200), nullable=False)	# Holds description for each item.
	quant = db.Column(db.String(50), nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def main_page():
	return render_template('main.html')

@app.route('/resume/')
def resume():
	return render_template('resume.html')

@app.route('/to_do_list/', methods=['POST', 'GET'])
def todo_list():
	if request.method == "POST":
		task_content = request.form['content']
		new_task = Todo(content=task_content)

		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect('/to_do_list/')
		except:
			return "There was an issue adding your task."
	else:
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template('todo.html', tasks=tasks)

@app.route('/delete_todo/<int:id>')
def delete_todo(id):
	task_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/to_do_list/')
	except:
		return 'There was a problem deleting that task'

@app.route('/update_todo/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
	task = Todo.query.get_or_404(id)
	
	if request.method == 'POST':
		task.content = request.form['content']

		try:
			db.session.commit()
			return redirect('/to_do_list/')
		except:
			return 'There was an issue updating your task'
	else:
		return render_template('update_todo.html', task=task)

@app.route('/grocery/', methods=['POST', 'GET'])
def grocery_list():
	if request.method == "POST":
		item_description = request.form['description']
		item_quant = request.form['quant']
		new_item = Grocery(description=item_description, quant=item_quant)

		try:
			db.session.add(new_item)
			db.session.commit()
			return redirect('/grocery/')
		except:
			return "There was an issue adding your item."
	else:
		items = Grocery.query.order_by(Grocery.date_created).all()
		return render_template('grocery.html', items=items)

@app.route('/delete_grocery/<int:id>')
def delete_grocery(id):
	item_to_delete = Grocery.query.get_or_404(id)

	try:
		db.session.delete(item_to_delete)
		db.session.commit()
		return redirect('/grocery/')
	except:
		return 'There was a problem deleting that item'

@app.route('/update_grocery/<int:id>', methods=['GET', 'POST'])
def update_grocery(id):
	item = Grocery.query.get_or_404(id)
	
	if request.method == 'POST':
		item.description = request.form['description']
		item.quant = request.form['quant']

		try:
			db.session.commit()
			return redirect('/grocery/')
		except:
			return 'There was an issue updating your item'
	else:
		return render_template('update_grocery.html', item=item)

if __name__ == '__main__':
	app.run(debug = True)