from flask import Flask, request

app = Flask(__name__)

@app.route('/execute-command', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    # Execute the command on the server
    # Replace the following line with your actual command execution logic
    result = f"Command received and executed: {command}"
    return {'result': result}

if __name__ == '__main__':
    app.run(host='10.0.2.15', port=5000)
