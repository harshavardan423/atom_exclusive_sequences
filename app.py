from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Exclusive sequences data
EXCLUSIVE_SEQUENCES_DATA = {
    "Premium Automation Suite": {
        "description": "Advanced automation workflows",
        "category": "premium",
        "steps_count": 5,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule",
                "details": {
                    "frequency": "Daily",
                    "time": "09:00"
                },
                "output": "trigger_result"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze daily metrics and prepare report",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "analysis_result"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "{{ACTION_OUTPUT:analysis_result}}"
                },
                "output": ""
            }
        ]
    },
    "AI Enhanced Pipeline": {
        "description": "AI-powered data processing",
        "category": "ai",
        "steps_count": 8,
        "steps": [
            {
                "type": "triggers", 
                "name": "file_created",
                "details": {
                    "filePath": "/data/input/"
                },
                "output": "file_trigger"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Process the uploaded file using AI",
                    "read_file_flag": "true",
                    "file_path": "{{ACTION_OUTPUT:file_trigger}}"
                },
                "output": "ai_processing"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/data/output/processed_results.txt",
                    "task": "append {{ACTION_OUTPUT:ai_processing}}"
                },
                "output": "file_saved"
            }
        ]
    },
    "Enterprise Security Flow": {
        "description": "Enterprise-grade security workflows",
        "category": "security", 
        "steps_count": 12,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule", 
                "details": {
                    "frequency": "Hourly",
                    "time": "00:00"
                },
                "output": "security_check"
            },
            {
                "type": "actions",
                "name": "execute_shell_command",
                "details": {
                    "command": "netstat -an | grep LISTEN"
                },
                "output": "network_status"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze network security: {{ACTION_OUTPUT:network_status}}",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "security_analysis"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Security Check: {{ACTION_OUTPUT:security_analysis}}"
                },
                "output": ""
            }
        ]
    }
}

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Exclusive Sequences API is running",
        "version": "1.0.0"
    }), 200

@app.route('/api/exclusive-sequences', methods=['GET'])
def list_exclusive_sequences():
    """Get all available exclusive sequences"""
    try:
        # Return sequences without the steps data for listing
        sequences = {}
        for name, data in EXCLUSIVE_SEQUENCES_DATA.items():
            sequences[name] = {
                "description": data["description"],
                "category": data["category"],
                "steps_count": data["steps_count"]
            }
        
        return jsonify({"sequences": sequences}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch exclusive sequences: {str(e)}"}), 500

@app.route('/api/exclusive-sequences/<sequence_name>', methods=['GET'])
def get_exclusive_sequence(sequence_name):
    """Get specific exclusive sequence with steps"""
    try:
        if sequence_name not in EXCLUSIVE_SEQUENCES_DATA:
            return jsonify({"error": f"Exclusive sequence '{sequence_name}' not found"}), 404
            
        sequence_data = EXCLUSIVE_SEQUENCES_DATA[sequence_name]
        steps = sequence_data["steps"]
        
        return jsonify({
            "name": sequence_name,
            "steps": steps,
            "source": "exclusive",
            "total_steps": len(steps),
            "description": sequence_data["description"],
            "category": sequence_data["category"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch exclusive sequence '{sequence_name}': {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)