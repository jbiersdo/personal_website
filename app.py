from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///john_website.db'		# Tells app where the database is located

with app.app_context():
	db = SQLAlchemy(app)	# todo database intialization.

class Todo(db.Model):
	"""Class for task 'to do' SQLAlchemy Table"""
	id = db.Column(db.Integer, primary_key=True) 	# Integer that references the ID of each entry.
	content	= db.Column(db.String(200), nullable=False)	# Holds content for each task.
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id

class Grocery(db.Model):
	"""Class for Grocery item SQLAlchemy Table"""
	id = db.Column(db.Integer, primary_key=True) 	# Integer that references the ID of each entry.
	description	= db.Column(db.String(200), nullable=False)	# Holds description for each item.
	quant = db.Column(db.String(50), nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id

class MagicCard(db.Model):
	"""Class for establishing each Magic Card SQLAlchemy Table"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), nullable=False)
	quant = db.Column(db.Integer, nullable=False)
	mana = db.Column(db.String(40), nullable=False)
	art_large = db.Column(db.String(40), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def main_page():
	return render_template('main.html')

@app.route('/bio/')
def bio():
	return render_template('bio.html')

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

@app.route('/mtg_col/', methods=['GET', 'POST'])
def mtg_col():
	if request.method == "POST":
		input_name = request.form['name']	# Stores name input from user
		api_name = 'https://api.scryfall.com/cards/named?fuzzy=' + input_name.replace(' ', '+')
		magic = requests.get(api_name).json()
		
		card_quant = request.form['quant']
		card_name = magic['name']
		card_large_art = magic['image_uris']['large']
		
		mana_cost = magic['mana_cost']
		mana_symbols = re.findall('{*.}', mana_cost)

		symbols = requests.get('https://api.scryfall.com/symbology').json()
		mana_img = []
		for element in mana_symbols:
			for symbol in symbols['data']:
				if element == symbol['symbol']:
					mana_img.append(symbol['svg_uri'])
				
		new_card = MagicCard(name=card_name, quant=card_quant, mana=','.join(mana_img), art_large=card_large_art)

		try:
			db.session.add(new_card)
			db.session.commit()
			return redirect('/mtg_col/')
		except:
			return "There was an issue adding your item."
	else:
		cards = MagicCard.query.order_by(MagicCard.name).all()
		return render_template('mtg_col.html', cards=cards)

@app.route('/delete_mtg_col/<int:id>')
def delete_mtg_col(id):
	card_to_delete = MagicCard.query.get_or_404(id)

	try:
		db.session.delete(card_to_delete)
		db.session.commit()
		return redirect('/mtg_col/')
	except:
		return 'There was a problem deleting that item'

@app.route('/update_mtg_col/<int:id>', methods=['GET', 'POST'])
def update_mtg_col(id):
	card = MagicCard.query.get_or_404(id)
	
	if request.method == 'POST':
		card.quant = request.form['quant']

		try:
			db.session.commit()
			return redirect('/mtg_col/')
		except:
			return 'There was an issue updating your item'
	else:
		return render_template('update_mtg_col.html', card=card)

if __name__ == '__main__':
	app.run(debug = True)