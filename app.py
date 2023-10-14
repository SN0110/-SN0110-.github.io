from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))

@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/continue', methods=['GET','POST'])
def continue_page():
    if request.method == 'POST':
        content = request.form ['notes']
        if content:
            new_note = Note(content=content)
            db.session.add(new_note)
            db.session.commit()   
    return render_template('continue.html')

@app.route('/delete/<int:note_id>', methods=['GET'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect('/')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)
    if request.method == 'POST':
        new_content = request.form['new_content']
        if new_content:
            note.content = new_content
            db.session.commit()
            return redirect('/')
    return render_template('edit.html', note=note)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)


