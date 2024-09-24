from flask import Flask, render_template, url_for, request, redirect
import db_connection as c

app = Flask(__name__)

@app.route("/")
def function():
    if c.connection and c.connection.is_connected:
        with c.connection.cursor() as cursor:
            query = "SELECT * FROM countries;"
            result = cursor.execute(query)
            rows = cursor.fetchall()
            countries = ""
            for row in rows:
                countries += f'<option value="{row[0]}">{row[1]}</option>\n'
            
            query = "SELECT * FROM states;"
            result = cursor.execute(query)
            rows = cursor.fetchall()
            states = ""
            for row in rows:
                states += f'<option value="{row[0]}">{row[1]}</option>\n'
            
            query = "SELECT * FROM cities;"
            result = cursor.execute(query)
            rows = cursor.fetchall()
            cities = ""
            for row in rows:
                cities += f'<option value="{row[0]}">{row[1]}</option>\n'
    cursor.close()
    return render_template("index.html", countries=countries, states=states, cities=cities)

@app.route("/submit_user", methods=["get","post"])
def submit_user():
    if request.method == "POST":
        if c.connection and c.connection.is_connected:
            data = request.form
            user = data.get("username")
            pwd = data.get("pwd")
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            street = data.get("street")
            number = data.get("building_number")
            zone = data.get("zone")
            country = data.get("country")
            state = data.get("state")
            city = data.get("city")
            zip = data.get("zip")
            with c.connection.cursor() as cursor:
                #Insert user values
                query = f"""INSERT INTO addresses
                (street, building_number, zone, city_id, state_id, country_id, zip_code)
                VALUES
                ('{street}',{number},'{zone}',{city},{state},{country},{zip});"""
                result = cursor.execute(query)
                query = "SELECT id FROM addresses ORDER BY id DESC LIMIT 1"
                result = cursor.execute(query)
                address = cursor.fetchall()[0][0]
                query = f"""INSERT INTO users
                (username, email, pwd, first_name, last_name, address_id)
                VALUES
                ('{user}','{email}','{pwd}','{first_name}','{last_name}',{address})"""
                result = cursor.execute(query)
    c.connection.commit()
    cursor.close()
    return render_template("registered_confirmation.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
# Configurar una clave secreta para sesiones
app.secret_key = 'your_secret_key'

@app.route("/")
def home():
    if 'user_id' in session:  # Si hay una sesión activa, mostrar el perfil
        return redirect(url_for("profile"))
    return render_template("login.html")  # Si no, ir a login

# Ruta para el inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with c.connection.cursor() as cursor:
            query = "SELECT id, username, pwd FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user and user[2] == password:  # Verifica si la contraseña coincide
                # Crear una sesión para el usuario
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for("profile"))
            else:
                return "Invalid username or password"
    return render_template("login.html")

# Ruta para mostrar el perfil del usuario si la sesión está activa
@app.route("/profile")
def profile():
    if 'user_id' in session:  # Verificar si el usuario está autenticado
        return f"Welcome {session['username']}, this is your profile."
    return redirect(url_for("login"))

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Eliminar la sesión del usuario
    session.pop('username', None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True, port=5000)      

@app.route('/products', methods=['GET'])
def products():
    product_type = request.args.get('type')  # Obtener el tipo de producto del filtro
    query = "SELECT name, description, price, product_type FROM products"
    
    if product_type:
        query += f" WHERE product_type = '{product_type}'"
    
    with c.connection.cursor() as cursor:
        cursor.execute(query)
        products = cursor.fetchall()
    
    return render_template('products.html', products=products)
@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    with c.connection.cursor() as cursor:
        query = f"SELECT name, description, price, product_type, image_url, material, color FROM products WHERE product_id = {product_id};"
        cursor.execute(query)
        product = cursor.fetchone()
    
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404
