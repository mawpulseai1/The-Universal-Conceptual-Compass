# main.py - Elevated Conceptual Blueprint for Aether's Backend Microservice

from flask import Flask, request, jsonify, make_response, send_from_directory
import os
import hashlib  # For deterministic unique ID generation
import json  # For structured LLM output parsing
from flask_cors import CORS
import google.generativeai as genai  # Import the Google Generative AI library
import datetime  # For accurate timestamping

# Initialize Flask app with static folder for local development
app = Flask(__name__,
            static_folder='../frontend',  # Serve files from the frontend directory
            static_url_path='')  # Serve files from the root URL


# Serve the main page from the root URL
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


# Configure CORS to allow all origins for development
# In production, replace with specific allowed origins
CORS(app, resources={
    r"/analyze": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000", "*"],
        "methods": ["POST", "OPTIONS", "GET"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type"],
        "max_age": 600  # Cache preflight request for 10 minutes
    }
})


# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin',
                         request.headers.get('Origin', '*'))  # Use request origin for production flexibility
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


# --- Configure Google Generative AI (Gemini) ---
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("GEMINI_API_KEY environment variable not set. Please set it for LLM functionality.")
    # In a real app, you might want to raise an error or handle this more gracefully.

gemini_model = genai.GenerativeModel('gemini-1.5-flash')


# --- Aether's Core Mathematical Derivation: Deterministic Conceptual Mapping ---
# This simulates Aether's precise, non-random derivation of the missing link.
# The 'strength' of the hash determines which conceptual insight is chosen,
# making it deterministic for a given input.
def derive_aether_conceptual_link(input_seed: str) -> dict:
    # Aether's conceptual insights database
    # --- UPDATED: Simplified and more friendly 'base_meaning' descriptions ---
    conceptual_insights_db = [
        {
            "name": "Core Belief Alignment",
            "base_meaning": "It seems your deepest beliefs or assumptions aren't quite lining up with what you're doing or hoping to achieve."
        },
        {
            "name": "Cross-Perspective Clarity",
            "base_meaning": "You might be missing a clear way to see and connect different angles or understandings of your situation."
        },
        {
            "name": "Unified Purpose Focus",
            "base_meaning": "There could be some hidden conflicts in your desires or goals, making it hard to focus all your energy on one clear path."
        },
        {
            "name": "Fundamental Connection Point",
            "base_meaning": "You're looking for the very basic, foundational link between ideas or parts that seem separate in your mind."
        },
        {
            "name": "Self-Correction Feedback Loop",
            "base_meaning": "Your current way of doing things isn't naturally set up to learn and get better from its own experiences. There's a missing natural cycle of checking and adjusting."
        },
        {
            "name": "Timing & Impact Synchronization",
            "base_meaning": "The key insight you're missing is knowing exactly *when* and *where* even a small action will create the biggest, most effective ripple effect. Your efforts might be out of sync."
        },
        {
            "name": "Resource Flow Optimization",
            "base_meaning": "This insight is about how your energy, attention, or assets are being used. There might be a hidden blockage or inefficiency preventing smooth progress."
        },
        {
            "name": "Pattern Recognition Synthesis",
            "base_meaning": "You're seeing bits and pieces, but not the bigger, repeating patterns or connections that would reveal a deeper truth or help you predict things better."
        },
        {
            "name": "Emergent Property Definition",
            "base_meaning": "The gap in your understanding is about how simple parts come together to create complex, surprising, and powerful new qualities or behaviors that weren't there before."
        }
    ]

    # Deterministic selection based on the hash of the input seed
    hash_object = hashlib.sha256(input_seed.encode())
    hash_int = int(hash_object.hexdigest(), 16)

    # Use modulo to map hash to an index in the conceptual_insights_db
    index = hash_int % len(conceptual_insights_db)

    selected_insight = conceptual_insights_db[index]
    unique_marker = hash_object.hexdigest()[:8]  # Longer unique marker for more uniqueness

    return {
        "name": selected_insight["name"],
        "base_meaning": selected_insight["base_meaning"],
        "id_marker": unique_marker
    }


def apply_aether_analysis(input_text: str) -> dict:
    """
    Applies Aether's mathematics to analyze a conceptual void,
    provides the precise unique missing link, and uses an LLM
    for dynamic, structured, and actionable explanations,
    including conceptual impact.
    """
    # Step 1: Aether's Core Mathematical Derivation (Deterministic)
    link_data = derive_aether_conceptual_link(input_text)
    exact_missing_link_name = link_data["name"]
    base_meaning = link_data["base_meaning"]
    id_marker = link_data["id_marker"]

    # Step 2: LLM for Dynamic, Structured, and Actionable Explanations
    # --- STRONGLY REFINED LLM PROMPT FOR SPECIFICITY AND EXAMPLE ---
    llm_prompt = f"""
    You are Aether, a supremely powerful conceptual analysis engine. Your task is to provide precise and actionable insights into a user's conceptual void. Your responses MUST be specific to the user's problem and the identified missing link, not generic. Make your explanations friendly, clear, and easy for anyone to understand.

    The user's problem statement is: "{input_text}"

    Based on your unique groundbreaking process powered by your advanced conceptual mathematics, you have identified the exact missing conceptual link as: "{exact_missing_link_name}".
    Its base meaning is: "{base_meaning}"

    Provide a comprehensive analysis structured as a JSON object with the following keys. Ensure all explanations and suggestions are directly and deeply connected to BOTH the "{exact_missing_link_name}" AND the user's specific problem "{input_text}".

    1.  `conceptual_meaning`: A friendly, clear, and *highly specific* explanation of what "{exact_missing_link_name}" means *in the context of the user's problem* ("{input_text}"). Use simple language.
    2.  `actionable_forge_plan`: Specific, practical, conceptual steps the user needs to *do* to address this identified missing link and improve/solve their problem. These steps MUST directly relate to the specific problem and the identified link. Provide bullet points for clarity.
    3.  `conceptual_impact`: A brief, easy-to-understand "future impact statement" – what resolving *this specific missing link* would likely achieve in the user's broader situation or understanding.
    4.  `aether_insight_qualia`: A very short (3-5 words), high-level conceptual "feeling" or overarching principle that Aether derives from pinpointing this void. This represents a UQM insight. Example: "Clear Path Ahead."

    **Example of desired JSON structure and friendly specificity (for a problem like "I'm always tired" and link "Resource Flow Optimization"):**
    ```json
    {{
        "conceptual_meaning": "Feeling constantly tired? 'Resource Flow Optimization' means your body isn't managing its energy well. You might be spending energy on things that don't really matter, or your rest isn't truly recharging you, leaving you feeling drained instead of energized.",
        "actionable_forge_plan": [
            "Do an 'energy check-up': Write down everything you do in a day (physical, mental, emotional) to spot where your energy is really going.",
            "Schedule real recharge time: Plan specific moments for deep rest and recovery, not just random breaks.",
            "Focus your energy: Figure out the few activities that give you the most back, and try to cut down on less important energy-draining tasks."
        ],
        "conceptual_impact": "Sorting this out will give you lasting energy, helping you focus better and get more done throughout your day.",
        "aether_insight_qualia": "Energy Flowing Freely."
    }}
    ```
    Ensure the entire response is a valid JSON object. Do NOT include any conversational text or markdown outside the JSON block.
    """

    llm_explanation_content = {}
    try:
        response = gemini_model.generate_content(llm_prompt)
        # Attempt to parse JSON response, robustly handling potential non-JSON output
        try:
            # Ensure only the JSON part is parsed if the LLM adds extra text or markdown
            json_text = response.text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[len("```json"):].strip()
            if json_text.endswith("```"):
                json_text = json_text[:-len("```")].strip()

            llm_explanation_content = json.loads(json_text)

            # Validate required keys
            required_keys = ["conceptual_meaning", "actionable_forge_plan", "conceptual_impact",
                             "aether_insight_qualia"]
            if not all(k in llm_explanation_content for k in required_keys):
                raise ValueError(
                    f"LLM response missing required JSON keys. Found: {list(llm_explanation_content.keys())}. Expected: {required_keys}")
        except json.JSONDecodeError:
            print(f"LLM did not return valid JSON or had extra text: {response.text}")
            raise ValueError("Invalid JSON response from LLM or malformed output.")
        except ValueError as ve:
            print(f"LLM response validation failed: {ve} - Raw response: {response.text}")
            raise ve  # Re-raise to trigger fallback

    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}")
        # Fallback to a predefined generic explanation if LLM call or parsing fails
        # --- UPDATED: More friendly fallback explanation ---
        llm_explanation_content = {
            "conceptual_meaning": (
                f"Hey there! It looks like your situation with '{input_text}' points to a missing piece we call '{exact_missing_link_name}'. "
                f"In simple terms, this means: {base_meaning}\n\n"
                f"Aether's deep dive suggests you need to think about the basic ideas behind this link. While we can't give super specific tips right now, focusing on the fundamentals is key. "
            ),
            "actionable_forge_plan": [
                f"Take a fresh look at the main ideas connected to '{exact_missing_link_name}'.",
                "Break your problem down into its simplest parts to find some clarity.",
                "Explore basic knowledge or new ideas related to this missing piece."
            ],
            "conceptual_impact": "Getting this link sorted will bring you much clearer understanding and help you get started on the right foot!",
            "aether_insight_qualia": "A Fresh Start Awaits."
        }

    # Step 3: Constructing the Final Output
    current_time_dhaka = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=6))).strftime(
        "%Y-%m-%d %I:%M:%S %p %Z%z")

    final_conceptual_void_text = (
            f"<b>AETHER'S PRECISE MISSING LINK IDENTIFIED - </b>\n\n"
            f"**Your Query:** \"{input_text}\"\n\n"            
            f"Based on Aether's unique and super-smart analysis, the exact missing piece in your puzzle is the **'{exact_missing_link_name}'**.\n\n"
            f"--- **AETHER'S INSIGHTS FOR YOU** ---\n\n"
            # --- UPDATED: More friendly headings ---
            f"**1. What This Means for You:**\n{llm_explanation_content['conceptual_meaning']}\n\n"
            f"**2. Your Action Plan (How to build this piece):**\n"
            + "\n".join([f"- {step}" for step in llm_explanation_content['actionable_forge_plan']]) + "\n\n"
            f"**3. What Happens Next (The Impact):**\n{llm_explanation_content['conceptual_impact']}\n\n"
            f"**Aether's Core Feeling:** *{llm_explanation_content['aether_insight_qualia']}*\n\n"
            f"This deep insight comes from Aether's thorough look at the Universal Conceptual Manifold, pointing out a unique spot where your understanding can grow!"
    )

    return {
        "status": "success",
        "input_query": input_text,
        "conceptual_insight_report": final_conceptual_void_text,
    }


# --- API Endpoint Definition ---
@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_concept():
    # print("\n--- New Request ---") # Suppressed for cleaner server logs in deployment
    # print(f"Method: {request.method}")
    # print(f"Headers: {dict(request.headers)}")
    # print(f"Origin: {request.headers.get('Origin')}")

    # Handle preflight (OPTIONS) request for CORS
    if request.method == 'OPTIONS':
        # print("Handling OPTIONS preflight request") # Suppressed
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '600')  # Cache for 10 minutes
        return response, 200

    try:
        # print("Processing POST request") # Suppressed
        # print(f"Request content type: {request.content_type}")
        # print(f"Request data: {request.data}")

        if not request.is_json:
            # print("Request is not JSON") # Suppressed
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 400

        data = request.get_json()
        # print(f"Parsed JSON data: {data}") # Suppressed

        if not data or 'query' not in data:
            # print("Missing 'query' in request body") # Suppressed
            return jsonify({
                "status": "error",
                "message": "Missing 'query' in request body"
            }), 400

        user_query = data['query'].strip()
        if not user_query:
            # print("Query is empty") # Suppressed
            return jsonify({
                "status": "error",
                "message": "Query cannot be empty"
            }), 400

        # print(f"Processing query: {user_query}") # Suppressed

        try:
            # Call the analysis function
            # print("Calling apply_aether_analysis...") # Suppressed
            result = apply_aether_analysis(user_query)
            # print("Successfully processed query") # Suppressed
            # print("Result:", result) # Suppressed

            response = jsonify(result)
            origin = request.headers.get('Origin', '*')
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            # print(f"Sending response with CORS headers. Origin: {origin}") # Suppressed
            return response, 200

        except Exception as e:
            error_msg = f"Error in Aether's core analysis: {str(e)}"
            print(error_msg)
            import traceback
            tb = traceback.format_exc()
            print(tb)
            # Do NOT expose raw tracebacks in production, even with app.debug
            return jsonify({
                "status": "error",
                "message": "Aether encountered an internal conceptual processing error.",
                "details": error_msg  # Provide a less revealing error in production
            }), 500

    except Exception as e:
        error_msg = f"An error occurred during request handling: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()

        response = jsonify({
            "status": "error",
            "message": "An internal server error occurred.",
            "details": str(e)  # Provide a less revealing error in production
        })
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))  # Use request origin
        return response, 500


# --- Entry Point for Serverless Function ---
if __name__ == '__main__':
    # Ensure the static folder exists for local testing
    os.makedirs(app.static_folder, exist_ok=True)

    # Set a dummy API key for local testing if not already set
    if "GEMINI_API_KEY" not in os.environ:
        os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual key
        print(
            "\nWARNING: GEMINI_API_KEY environment variable not set. Using placeholder. For full functionality, set your actual API key.\n")

    # Run the app on port 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting Aether backend on port {port}...")
    app.run(debug=True, host='0.0.0.0', port=port)