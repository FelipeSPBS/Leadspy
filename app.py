from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, Users, Pixel  # db deve ser o mesmo objeto aqui

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o db com o aplicativo
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário criado com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        name = request.form['name']
        pixel_code = request.form['pixel_code']
        redirect_link = request.form['redirect_link']
        track_pageview = request.form.get('track_pageview') == 'on'
        track_purchase = request.form.get('track_purchase') == 'on'

        new_pixel = Pixel(user_id=current_user.id, name=name, pixel_code=pixel_code,
                          redirect_link=redirect_link, track_pageview=track_pageview,
                          track_purchase=track_purchase, is_active=True)
        db.session.add(new_pixel)
        db.session.commit()
        
        flash('Pixel criado com sucesso!', 'success')
        return redirect(url_for('index'))

    pixels = Pixel.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', pixels=pixels)

@app.route('/toggle/<int:pixel_id>', methods=['POST'])
@login_required
def toggle_pixel(pixel_id):
    pixel = Pixel.query.get(pixel_id)
    if pixel:
        pixel.is_active = not pixel.is_active
        db.session.commit()
        flash('O redirecionamento foi atualizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/r/<pixel_name>')
def redirect_to_pixel(pixel_name):
    pixel = Pixel.query.filter_by(name=pixel_name).first()
    
    if pixel:
        # Rastrear visualização
        if pixel.track_pageview:
            print(f'Visualização rastreada para o pixel: {pixel.name}')
            
        # Rastrear compra se desejado
        if pixel.track_purchase:
            print(f'Compra rastreada para o pixel: {pixel.name}')

        # Retornar HTML com JavaScript para redirecionamento e passar o pixel
        return render_template('redirect.html', redirect_url=pixel.redirect_link, pixel=pixel)
    
    flash(f'Pixel "{pixel_name}" não encontrado.', 'danger')
    return render_template('pixel_not_found.html', pixel_name=pixel_name), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
    app.run(debug=True)
