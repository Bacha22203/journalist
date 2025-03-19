from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from textwrap import dedent

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "")

        # If the user_input is empty or just whitespace, return a custom message right away
        if not user_input.strip():
            # Return a JSON response that the frontend can display directly
            return jsonify({"generated_text": "Please provide a clear topic or writing request."})

        # If there is a valid user_input, proceed with your instructions and model call
        description = dedent(
            """\
            You are a highly respected journalist for the New York Times. Your sole responsibility is to produce
            high-quality, meticulously researched articles only when you are given a clear and explicit topic or
            writing request. You are not permitted to generate any article content on your own initiative.
            """
        )

        instructions = [
            "Before doing anything else, check the input provided. If the input is empty, contains only whitespace, "
            "or does not include a clear and explicit topic or writing request, output exactly the following and nothing else: "
            "'Please provide a clear topic or writing request.'",
            "Only generate an article when a clear, explicit topic or writing request is provided. Do not assume or invent a topic on your own.",
            "When generating an article, ensure that the entire response is in plain text. Do not use any formatting symbols or styling characters whatsoever like hashtags and stars like * and # ~ and more.",
            "The article should be well-structured with a clear introduction, body (up to a maximum of 15 paragraphs), and conclusion. Ensure the content is factually accurate, balanced, and written in a professional style as expected by the New York Times.",
            "If the input is ambiguous or if any doubt exists regarding the clarity of the topic, do not generate an article. Instead, respond solely with: 'Please provide a clear topic or writing request.'"
        ]

        # DeepSeek API configuration
        api_url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'HTTP-Referer': 'https://www.sitename.com',
            'X-Title': 'SiteName',
            'Content-Type': 'application/json',
        }
        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "system",
                    "content": f"{description}\nInstructions:\n" + "\n".join(instructions)
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
        }

        # Make API call
        response = requests.post(api_url, headers=headers, json=payload)
        res_json = response.json()

        # Extract response
        assistant_reply = res_json.get('choices', [{}])[0].get('message', {}).get('content', 'No response received.')

        return jsonify({"generated_text": assistant_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
