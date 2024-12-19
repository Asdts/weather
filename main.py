from flask import Flask, request, jsonify
from backend.sdk.agents.base_agent import BaseAgent
from backend.sdk.llms.openAi_llm import OpenaiLLM
from backend.sdk.llms.groq_llm import GroqLLM

# Import all agent classes
from backend.sdk.agents.authHelper.agent import AuthHelperAgent
from backend.sdk.agents.comments.agent import LogCommentAgent
from backend.sdk.agents.errorHandler.agent import ErrorHandlerAgent
from backend.sdk.agents.logManagement.agent import LogAgent
from backend.sdk.agents.nlpQuery.agent import LogAgent as NLPQueryAgent
from backend.sdk.agents.recommendation.agent import RecommendationAgent
from backend.sdk.agents.summaries.agent import SummaryAgent

app = Flask(__name__)

# Global configuration for the LLM
current_llm = None
agents = {}

def configure_openai(api_key, model):
    global current_llm
    llm_config = {
        'model': model,
        'temperature': 0.7,
        'max_tokens': 150
    }
    current_llm = OpenaiLLM(llm_config)
    # current_llm.llm_config['api_key'] = api_key
    initialize_agents()

def configure_groq(api_key, model):
    global current_llm
    llm_config = {
        'model': model,
        'temperature': 0.7,
        'max_tokens': 150
    }
    current_llm = GroqLLM(llm_config, api_key)
    # current_llm.llm_config['api_key'] = api_key
    initialize_agents()

def initialize_agents():
    global agents
    if not current_llm:
        raise ValueError("LLM is not configured.")

    agents['auth_helper'] = AuthHelperAgent(llm=current_llm)
    agents['log_comment'] = LogCommentAgent(llm=current_llm)
    agents['error_handler'] = ErrorHandlerAgent(llm=current_llm)
    agents['log_management'] = LogAgent(llm=current_llm)
    agents['nlp_query'] = NLPQueryAgent(llm=current_llm)
    agents['recommendation'] = RecommendationAgent(llm=current_llm)
    agents['summary'] = SummaryAgent(llm=current_llm)

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/configure', methods=['POST'])
def configure():
    data = request.json
    llm_type = data.get('llm_type')
    api_key = data.get('api_key')
    model = data.get('model', 'default-model')

    if llm_type == 'openai':
        configure_openai(api_key, model)
        return jsonify({"message": "OpenAI LLM configured successfully"}), 200
    elif llm_type == 'groq':
        configure_groq(api_key, model)
        return jsonify({"message": "Groq LLM configured successfully"}), 200
    else:
        return jsonify({"error": "Invalid LLM type specified"}), 400

@app.route('/<agent_name>/act', methods=['POST'])
def agent_act(agent_name):
    if agent_name not in agents:
        return jsonify({"error": f"Agent '{agent_name}' not found."}), 404

    data = request.json
    try:
        required_params = {key: value for key, value in data.items() if value is not None}
        response = agents[agent_name].act(**required_params)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
