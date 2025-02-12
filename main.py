from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# Dados de usuário (em um ambiente real, isso viria de um banco de dados)
data = {
    'user': 'admin',
    'password': 'admin',
    'cookie': '123456789'
}



def set_cookie(response, key, value, max_age=None):
    """Define um cookie na resposta."""
    response.set_cookie(key, value, max_age=max_age, secure=True, httponly=True, samesite='Lax')
    return response

def get_cookie(request, key):
    """Recupera o valor de um cookie."""
    return request.cookies.get(key)

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        # Recupera o cookie 'user' se existir
        user_cookie = get_cookie(request, 'cookie')
        if user_cookie:
            return jsonify({'message': f'Usuário autenticado: {user_cookie}'}), 200
        else:
            return jsonify({'message': 'Nenhum usuário autenticado'}), 200

    if request.method == 'POST':
        # Verifica se os parâmetros foram fornecidos
        if not request.json or 'user' not in request.json or 'password' not in request.json:
            return jsonify({'error': 'Missing parameters'}), 400

        user = request.json['user']
        password = request.json['password']

        # Verifica as credenciais
        if user == data['user'] and password == data['password']:
            # Cria uma resposta com uma mensagem de sucesso
            response = make_response(jsonify({'success': 'Logged in'}), 200)
            # Define o cookie 'user' com o nome do usuário
            response = set_cookie(response, 'cookie', data['cookie'], max_age=100)  # Cookie expira em 1 hora
            return response
        else:
            return jsonify({'error': 'Unauthorized'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """Rota para logout (remove o cookie)."""
    response = make_response(jsonify({'success': 'Logged out'}), 200)
    response.delete_cookie('cookie')  # Remove o cookie 'user'
    return response

if __name__ == '__main__':
    app.run(debug=True)