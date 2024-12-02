from flask import Flask, request, jsonify
from ollama import chat, ChatResponse

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_html():
    try:
        # Parse input from the POST request
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400

        prompt = data['prompt']

        # Call the LLM with the provided prompt
        response: ChatResponse = chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        
        # Extract and return the generated content
        generated_content = response.message.content
        return jsonify({"generated_content": generated_content}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

