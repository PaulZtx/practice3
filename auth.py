from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)
users = {
    "admin": {
        "password_hash": hashlib.md5('superman'.encode()).hexdigest(),
        "last_login_attempt_time": 0,
        "login_attempts": 0
    }
}

MAX_LOGIN_ATTEMPTS = 3
RESET_INTERVAL = 60

@app.route('/')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username in users:
        stored_password = users[username]["password_hash"]
        last_attempt_time = users[username]["last_login_attempt_time"]
        login_attempts = users[username]["login_attempts"]
        
        current_time = time.time()
        if current_time - last_attempt_time > RESET_INTERVAL:
            users[username]["login_attempts"] = 0

        if login_attempts >= MAX_LOGIN_ATTEMPTS:
            time_left = int(RESET_INTERVAL - (current_time - last_attempt_time))
            return jsonify({"message": f"Превышено максимальное количество попыток входа. Пожалуйста, подождите {time_left} секунд."}), 429

        if hashlib.md5(password.encode()).hexdigest() == stored_password:
            users[username]["login_attempts"] = 0 
            users[username]["last_login_attempt_time"] = current_time 
            return jsonify({"message": "Авторизация успешна!"}), 200
        else:
            users[username]["login_attempts"] += 1
            users[username]["last_login_attempt_time"] = current_time 
            return jsonify({"message": "Неверные учетные данные."}), 401
    else:
        return jsonify({"message": "Пользователь не найден."}), 404

if __name__ == '__main__':
    app.run()