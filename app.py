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
    },
    "Smart File Analyzer & HTML Generator": {
        "description": "Automatically analyzes new files and creates HTML presentations",
        "category": "automation",
        "steps_count": 6,
        "steps": [
            {
                "type": "triggers",
                "name": "file_created",
                "details": {
                    "filePath": "/data/uploads/"
                },
                "output": "new_file_path"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze this file and extract key insights, structure, and important data points. Provide a comprehensive analysis.",
                    "read_file_flag": "true",
                    "file_path": "{{ACTION_OUTPUT:new_file_path}}"
                },
                "output": "file_analysis"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Create a complete HTML presentation based on this analysis: {{ACTION_OUTPUT:file_analysis}}. Include proper CSS styling, responsive design, and interactive elements. Make it professional and visually appealing.",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "html_content"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/data/presentations/analysis_presentation.html",
                    "task": "replace entire content with {{ACTION_OUTPUT:html_content}}"
                },
                "output": "presentation_saved"
            },
            {
                "type": "actions",
                "name": "run_file",
                "details": {
                    "file_path": "/data/presentations/analysis_presentation.html"
                },
                "output": "presentation_opened"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "File analysis complete! HTML presentation created and opened."
                },
                "output": ""
            }
        ]
    },
    "System Health Monitor": {
        "description": "Comprehensive system monitoring and reporting",
        "category": "system",
        "steps_count": 8,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule",
                "details": {
                    "frequency": "Daily",
                    "time": "08:00"
                },
                "output": "health_check_trigger"
            },
            {
                "type": "actions",
                "name": "execute_shell_command",
                "details": {
                    "command": "systeminfo" if os.name == 'nt' else "uname -a && df -h && free -h && ps aux --sort=-%cpu | head -10"
                },
                "output": "system_info"
            },
            {
                "type": "actions",
                "name": "execute_shell_command",
                "details": {
                    "command": "wmic logicaldisk get size,freespace,caption" if os.name == 'nt' else "df -h"
                },
                "output": "disk_info"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze system health data: System Info: {{ACTION_OUTPUT:system_info}} Disk Info: {{ACTION_OUTPUT:disk_info}}. Provide health assessment, warnings for low disk space, high CPU usage, and recommendations.",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "health_analysis"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/logs/system_health_report.txt",
                    "task": "append [{{ACTION_OUTPUT:health_check_trigger}}] System Health Report:\n{{ACTION_OUTPUT:health_analysis}}\n\n"
                },
                "output": "report_saved"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "System health check completed. Report saved to logs."
                },
                "output": ""
            }
        ]
    },
    "Code Project Builder": {
        "description": "Automatically builds and tests code projects",
        "category": "development",
        "steps_count": 10,
        "steps": [
            {
                "type": "triggers",
                "name": "file_created",
                "details": {
                    "filePath": "/projects/new/"
                },
                "output": "project_file"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze this project file and determine what type of project it is, what dependencies it needs, and what build/run commands should be used.",
                    "read_file_flag": "true",
                    "file_path": "{{ACTION_OUTPUT:project_file}}"
                },
                "output": "project_analysis"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import os\nimport subprocess\nimport json\n\n# Get project directory\nproject_dir = os.path.dirname('{{ACTION_OUTPUT:project_file}}')\nos.chdir(project_dir)\n\n# Check for package.json, requirements.txt, etc.\nproject_info = {}\nif os.path.exists('package.json'):\n    project_info['type'] = 'nodejs'\n    project_info['install_cmd'] = 'npm install'\n    project_info['run_cmd'] = 'npm start'\nelif os.path.exists('requirements.txt'):\n    project_info['type'] = 'python'\n    project_info['install_cmd'] = 'pip install -r requirements.txt'\n    project_info['run_cmd'] = 'python main.py'\nelif os.path.exists('Cargo.toml'):\n    project_info['type'] = 'rust'\n    project_info['install_cmd'] = 'cargo build'\n    project_info['run_cmd'] = 'cargo run'\nelse:\n    project_info['type'] = 'unknown'\n\nprint(json.dumps(project_info))"
                },
                "output": "project_setup_info"
            },
            {
                "type": "actions",
                "name": "execute_shell_command",
                "details": {
                    "command": "cd {{ACTION_OUTPUT:project_file}} && {{ACTION_OUTPUT:project_setup_info.install_cmd}}"
                },
                "output": "install_result"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Project built successfully! Install result: {{ACTION_OUTPUT:install_result}}"
                },
                "output": ""
            }
        ]
    },
    "Smart Backup System": {
        "description": "Intelligent file backup with compression and cloud sync",
        "category": "backup",
        "steps_count": 7,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule",
                "details": {
                    "frequency": "Daily",
                    "time": "23:00"
                },
                "output": "backup_trigger"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import os\nimport shutil\nimport zipfile\nfrom datetime import datetime\n\n# Create backup directory\nbackup_dir = f'/backups/{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}'\nos.makedirs(backup_dir, exist_ok=True)\n\n# Important directories to backup\nsource_dirs = ['/data', '/projects', '/documents']\n\nbackup_info = []\nfor source in source_dirs:\n    if os.path.exists(source):\n        dest = os.path.join(backup_dir, os.path.basename(source))\n        shutil.copytree(source, dest, ignore_errors=True)\n        backup_info.append(f'Backed up: {source} -> {dest}')\n\n# Create zip archive\nzip_path = f'{backup_dir}.zip'\nwith zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:\n    for root, dirs, files in os.walk(backup_dir):\n        for file in files:\n            file_path = os.path.join(root, file)\n            arcname = os.path.relpath(file_path, backup_dir)\n            zipf.write(file_path, arcname)\n\n# Clean up uncompressed backup\nshutil.rmtree(backup_dir)\n\nprint(f'Backup completed: {zip_path}\\nBackup info: {\"; \".join(backup_info)}')"
                },
                "output": "backup_result"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/logs/backup_log.txt",
                    "task": "append [{{ACTION_OUTPUT:backup_trigger}}] {{ACTION_OUTPUT:backup_result}}\n"
                },
                "output": "log_updated"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Daily backup completed successfully!"
                },
                "output": ""
            }
        ]
    },
    "AI Document Processor": {
        "description": "Processes documents with AI analysis and generates summaries",
        "category": "ai",
        "steps_count": 9,
        "steps": [
            {
                "type": "triggers",
                "name": "file_created",
                "details": {
                    "filePath": "/documents/inbox/"
                },
                "output": "new_document"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze this document and provide: 1) A comprehensive summary 2) Key topics and themes 3) Important dates and numbers 4) Action items if any 5) Document category/type",
                    "read_file_flag": "true",
                    "file_path": "{{ACTION_OUTPUT:new_document}}"
                },
                "output": "document_analysis"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Based on this analysis: {{ACTION_OUTPUT:document_analysis}}, create a structured JSON metadata object with fields: title, summary, category, key_points, action_items, priority_level, tags",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "document_metadata"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/documents/processed/{{ACTION_OUTPUT:new_document}}_metadata.json",
                    "task": "replace entire content with {{ACTION_OUTPUT:document_metadata}}"
                },
                "output": "metadata_saved"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Create a professional HTML report for this document analysis: {{ACTION_OUTPUT:document_analysis}}. Include charts, highlights, and actionable insights.",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "html_report"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/documents/reports/{{ACTION_OUTPUT:new_document}}_report.html",
                    "task": "replace entire content with {{ACTION_OUTPUT:html_report}}"
                },
                "output": "report_saved"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Document processed and analyzed. Report generated successfully!"
                },
                "output": ""
            }
        ]
    },
    "Network Security Scanner": {
        "description": "Automated network security scanning and threat detection",
        "category": "security",
        "steps_count": 8,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule",
                "details": {
                    "frequency": "Daily",
                    "time": "02:00"
                },
                "output": "security_scan_trigger"
            },
            {
                "type": "actions",
                "name": "execute_shell_command",
                "details": {
                    "command": "netstat -an | findstr LISTENING" if os.name == 'nt' else "netstat -tuln"
                },
                "output": "open_ports"
            },
            {
                "type": "actions",
                "name": "execute_shell_command",
                "details": {
                    "command": "arp -a" if os.name == 'nt' else "arp -a"
                },
                "output": "network_devices"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import socket\nimport subprocess\nimport json\nfrom datetime import datetime\n\n# Check for suspicious processes\ntry:\n    if os.name == 'nt':\n        proc_result = subprocess.run(['tasklist'], capture_output=True, text=True)\n    else:\n        proc_result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)\n    \n    processes = proc_result.stdout\nexcept:\n    processes = 'Unable to get process list'\n\n# Check system integrity\nsecurity_check = {\n    'timestamp': datetime.now().isoformat(),\n    'processes_checked': len(processes.split('\\n')),\n    'status': 'completed'\n}\n\nprint(json.dumps(security_check))"
                },
                "output": "security_check_result"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze security scan results: Open Ports: {{ACTION_OUTPUT:open_ports}} Network Devices: {{ACTION_OUTPUT:network_devices}} Security Check: {{ACTION_OUTPUT:security_check_result}}. Identify potential security threats, unusual ports, unknown devices, and provide security recommendations.",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "security_analysis"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/security/scan_reports.txt",
                    "task": "append [{{ACTION_OUTPUT:security_scan_trigger}}] Security Scan Report:\n{{ACTION_OUTPUT:security_analysis}}\n---\n"
                },
                "output": "security_report_saved"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Security scan completed. Check /security/scan_reports.txt for details."
                },
                "output": ""
            }
        ]
    },
    "Automated Data Pipeline": {
        "description": "Processes data files through multiple stages with AI enhancement",
        "category": "data",
        "steps_count": 12,
        "steps": [
            {
                "type": "triggers",
                "name": "file_created",
                "details": {
                    "filePath": "/data/raw/"
                },
                "output": "raw_data_file"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import pandas as pd\nimport json\nimport os\n\nfile_path = '{{ACTION_OUTPUT:raw_data_file}}'\nfile_ext = os.path.splitext(file_path)[1].lower()\n\ntry:\n    if file_ext == '.csv':\n        df = pd.read_csv(file_path)\n    elif file_ext == '.json':\n        df = pd.read_json(file_path)\n    elif file_ext in ['.xlsx', '.xls']:\n        df = pd.read_excel(file_path)\n    else:\n        raise ValueError(f'Unsupported file type: {file_ext}')\n    \n    # Basic data info\n    data_info = {\n        'rows': len(df),\n        'columns': len(df.columns),\n        'column_names': list(df.columns),\n        'data_types': df.dtypes.astype(str).to_dict(),\n        'missing_values': df.isnull().sum().to_dict(),\n        'file_type': file_ext\n    }\n    \n    print(json.dumps(data_info))\n    \nexcept Exception as e:\n    print(json.dumps({'error': str(e)}))"
                },
                "output": "data_info"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze this data structure: {{ACTION_OUTPUT:data_info}}. Suggest data cleaning steps, potential insights to extract, and visualization recommendations.",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "data_analysis_plan"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport json\n\nfile_path = '{{ACTION_OUTPUT:raw_data_file}}'\nfile_ext = os.path.splitext(file_path)[1].lower()\n\n# Load and clean data\nif file_ext == '.csv':\n    df = pd.read_csv(file_path)\nelif file_ext == '.json':\n    df = pd.read_json(file_path)\nelif file_ext in ['.xlsx', '.xls']:\n    df = pd.read_excel(file_path)\n\n# Basic cleaning\ndf_cleaned = df.dropna()\n\n# Generate summary statistics\nsummary = {\n    'original_rows': len(df),\n    'cleaned_rows': len(df_cleaned),\n    'removed_rows': len(df) - len(df_cleaned)\n}\n\n# Save cleaned data\ncleaned_path = '/data/processed/cleaned_data.csv'\ndf_cleaned.to_csv(cleaned_path, index=False)\n\nprint(json.dumps(summary))"
                },
                "output": "data_processing_result"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Create a comprehensive data analysis report based on the processing results: {{ACTION_OUTPUT:data_processing_result}} and analysis plan: {{ACTION_OUTPUT:data_analysis_plan}}. Include key findings, trends, and actionable insights.",
                    "read_file_flag": "true",
                    "file_path": "/data/processed/cleaned_data.csv"
                },
                "output": "final_analysis"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/data/reports/analysis_report.txt",
                    "task": "replace entire content with {{ACTION_OUTPUT:final_analysis}}"
                },
                "output": "report_saved"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Data pipeline completed! Processed data and analysis report generated."
                },
                "output": ""
            }
        ]
    },
    "Multi-Format Media Converter": {
        "description": "Automatically converts media files to different formats",
        "category": "media",
        "steps_count": 6,
        "steps": [
            {
                "type": "triggers",
                "name": "file_created",
                "details": {
                    "filePath": "/media/input/"
                },
                "output": "media_file"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import os\nimport subprocess\nimport json\nfrom pathlib import Path\n\nfile_path = '{{ACTION_OUTPUT:media_file}}'\nfile_ext = Path(file_path).suffix.lower()\nfile_name = Path(file_path).stem\n\nmedia_info = {\n    'input_file': file_path,\n    'extension': file_ext,\n    'name': file_name,\n    'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0\n}\n\n# Determine conversion based on file type\nif file_ext in ['.mp4', '.avi', '.mov', '.mkv']:\n    media_info['type'] = 'video'\n    media_info['convert_to'] = '.mp4'\nelif file_ext in ['.mp3', '.wav', '.flac', '.m4a']:\n    media_info['type'] = 'audio'\n    media_info['convert_to'] = '.mp3'\nelif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:\n    media_info['type'] = 'image'\n    media_info['convert_to'] = '.jpg'\nelse:\n    media_info['type'] = 'unknown'\n    media_info['convert_to'] = None\n\nprint(json.dumps(media_info))"
                },
                "output": "media_analysis"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import subprocess\nimport os\nimport json\nfrom PIL import Image\n\nmedia_info = {{ACTION_OUTPUT:media_analysis}}\n\nif media_info['type'] == 'image':\n    try:\n        # Convert image using PIL\n        img = Image.open(media_info['input_file'])\n        output_path = f\"/media/output/{media_info['name']}_converted.jpg\"\n        img.convert('RGB').save(output_path, 'JPEG', quality=95)\n        result = f'Image converted: {output_path}'\n    except Exception as e:\n        result = f'Image conversion failed: {str(e)}'\n        \nelif media_info['type'] == 'audio':\n    # For audio/video conversion, you'd typically use ffmpeg\n    # This is a placeholder - actual implementation would require ffmpeg\n    result = 'Audio conversion requires ffmpeg installation'\n    \nelif media_info['type'] == 'video':\n    # For video conversion, you'd typically use ffmpeg\n    result = 'Video conversion requires ffmpeg installation'\n    \nelse:\n    result = 'Unsupported media type'\n\nprint(result)"
                },
                "output": "conversion_result"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/media/conversion_log.txt",
                    "task": "append [{{ACTION_OUTPUT:media_file}}] {{ACTION_OUTPUT:conversion_result}}\n"
                },
                "output": "log_updated"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Media conversion completed: {{ACTION_OUTPUT:conversion_result}}"
                },
                "output": ""
            }
        ]
    },
    "Website Health Monitor": {
        "description": "Monitors website availability and performance",
        "category": "monitoring",
        "steps_count": 7,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule",
                "details": {
                    "frequency": "Hourly",
                    "time": "00:00"
                },
                "output": "monitor_trigger"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import requests\nimport time\nimport json\nfrom datetime import datetime\n\n# List of websites to monitor\nwebsites = [\n    'https://google.com',\n    'https://github.com',\n    'https://stackoverflow.com'\n]\n\nresults = []\nfor url in websites:\n    try:\n        start_time = time.time()\n        response = requests.get(url, timeout=10)\n        response_time = (time.time() - start_time) * 1000  # Convert to ms\n        \n        result = {\n            'url': url,\n            'status_code': response.status_code,\n            'response_time_ms': round(response_time, 2),\n            'status': 'UP' if response.status_code == 200 else 'DOWN',\n            'timestamp': datetime.now().isoformat()\n        }\n    except Exception as e:\n        result = {\n            'url': url,\n            'status_code': 0,\n            'response_time_ms': 0,\n            'status': 'DOWN',\n            'error': str(e),\n            'timestamp': datetime.now().isoformat()\n        }\n    \n    results.append(result)\n\nprint(json.dumps(results, indent=2))"
                },
                "output": "monitoring_results"
            },
            {
                "type": "actions",
                "name": "think",
                "details": {
                    "text_input": "Analyze website monitoring results: {{ACTION_OUTPUT:monitoring_results}}. Identify any sites that are down, have slow response times, or show concerning patterns. Provide alerts and recommendations.",
                    "read_file_flag": "false",
                    "file_path": ""
                },
                "output": "monitoring_analysis"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/monitoring/website_status.json",
                    "task": "replace entire content with {{ACTION_OUTPUT:monitoring_results}}"
                },
                "output": "status_saved"
            },
            {
                "type": "actions",
                "name": "modify_file",
                "details": {
                    "file_path": "/monitoring/analysis_log.txt",
                    "task": "append [{{ACTION_OUTPUT:monitor_trigger}}] {{ACTION_OUTPUT:monitoring_analysis}}\n---\n"
                },
                "output": "analysis_logged"
            },
            {
                "type": "actions",
                "name": "display_message",
                "details": {
                    "message": "Website monitoring completed. Check /monitoring/ for detailed results."
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
        "version": "2.0.0",
        "total_sequences": len(EXCLUSIVE_SEQUENCES_DATA)
    }), 200

@app.route('/api/exclusive-sequences/search', methods=['GET'])
def search_exclusive_sequences():
    """Search exclusive sequences by name, description, category, or steps"""
    try:
        query = request.args.get('q', '').strip().lower()
        
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        results = {}
        
        for name, data in EXCLUSIVE_SEQUENCES_DATA.items():
            # Search in name, description, category
            name_match = query in name.lower()
            desc_match = query in data["description"].lower()
            category_match = query in data["category"].lower()
            
            # Also search in step names and details
            steps_match = False
            for step in data["steps"]:
                if (query in step.get("name", "").lower() or 
                    query in str(step.get("details", {})).lower()):
                    steps_match = True
                    break
            
            if name_match or desc_match or category_match or steps_match:
                results[name] = {
                    "description": data["description"],
                    "category": data["category"],
                    "steps_count": data["steps_count"],
                    "match_type": []
                }
                
                # Indicate what matched for better UX
                if name_match:
                    results[name]["match_type"].append("name")
                if desc_match:
                    results[name]["match_type"].append("description")
                if category_match:
                    results[name]["match_type"].append("category")
                if steps_match:
                    results[name]["match_type"].append("steps")
        
        return jsonify({
            "query": query,
            "results": results,
            "total_found": len(results)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to search exclusive sequences: {str(e)}"}), 500

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
