from flask import Flask, jsonify, request
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
    
    "Google Sheets Downloader": {
        "description": "Automated sequence to download Google Sheets as CSV/Excel files with authentication, error handling, and user notifications",
        "category": "data",
        "steps_count": 6,
        "steps": [
            {
                "type": "triggers",
                "name": "schedule_trigger",
                "details": {
                    "frequency": "daily",
                    "time": "09:00"
                },
                "output": "trigger_timestamp"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import os\nimport pandas as pd\nfrom datetime import datetime\nimport requests\nfrom urllib.parse import urlparse\n\n# Configuration\nSHEET_URL = 'https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0'  # Replace with actual sheet URL\nOUTPUT_DIR = './downloads/sheets/'\nFILE_FORMAT = 'csv'  # Options: csv, xlsx\n\n# Create output directory\nos.makedirs(OUTPUT_DIR, exist_ok=True)\n\n# Extract sheet ID from URL\ndef extract_sheet_id(url):\n    if '/spreadsheets/d/' in url:\n        return url.split('/spreadsheets/d/')[1].split('/')[0]\n    return None\n\nsheet_id = extract_sheet_id(SHEET_URL)\nif not sheet_id:\n    raise ValueError('Invalid Google Sheets URL')\n\n# Generate download URL\nif FILE_FORMAT == 'csv':\n    download_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'\nelse:\n    download_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx'\n\nprint(f'Sheet ID: {sheet_id}')\nprint(f'Download URL: {download_url}')\n\ndownload_info = {\n    'sheet_id': sheet_id,\n    'download_url': download_url,\n    'format': FILE_FORMAT,\n    'output_dir': OUTPUT_DIR,\n    'timestamp': datetime.now().isoformat()\n}"
                },
                "output": "download_config"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import requests\nimport os\nfrom datetime import datetime\n\n# Get config from previous step\ndownload_url = download_info['download_url']\noutput_dir = download_info['output_dir']\nfile_format = download_info['format']\nsheet_id = download_info['sheet_id']\n\ntry:\n    # Make request to download the sheet\n    headers = {\n        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'\n    }\n    \n    response = requests.get(download_url, headers=headers, timeout=30)\n    response.raise_for_status()\n    \n    # Generate filename with timestamp\n    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n    filename = f'google_sheet_{sheet_id}_{timestamp}.{file_format}'\n    file_path = os.path.join(output_dir, filename)\n    \n    # Save the file\n    with open(file_path, 'wb') as f:\n        f.write(response.content)\n    \n    # Verify file was created and get size\n    file_size = os.path.getsize(file_path)\n    \n    download_result = {\n        'success': True,\n        'file_path': file_path,\n        'filename': filename,\n        'file_size_bytes': file_size,\n        'file_size_mb': round(file_size / (1024*1024), 2),\n        'download_time': datetime.now().isoformat(),\n        'status_code': response.status_code\n    }\n    \n    print(f'Successfully downloaded: {filename}')\n    print(f'File size: {download_result[\"file_size_mb\"]} MB')\n    print(f'Saved to: {file_path}')\n    \nexcept requests.exceptions.RequestException as e:\n    download_result = {\n        'success': False,\n        'error': f'Download failed: {str(e)}',\n        'error_type': 'network_error'\n    }\nexcept Exception as e:\n    download_result = {\n        'success': False,\n        'error': f'Unexpected error: {str(e)}',\n        'error_type': 'general_error'\n    }"
                },
                "output": "download_status"
            },
            {
                "type": "actions",
                "name": "run_py_code",
                "details": {
                    "code": "import pandas as pd\nimport json\n\n# Validate and analyze downloaded file if successful\nif download_status['success']:\n    try:\n        file_path = download_status['file_path']\n        \n        # Read and analyze the file\n        if file_path.endswith('.csv'):\n            df = pd.read_csv(file_path)\n        else:\n            df = pd.read_excel(file_path)\n        \n        # Generate file analysis\n        analysis = {\n            'rows': len(df),\n            'columns': len(df.columns),\n            'column_names': list(df.columns),\n            'data_types': df.dtypes.to_dict(),\n            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / (1024*1024), 2),\n            'has_null_values': df.isnull().any().any(),\n            'null_counts': df.isnull().sum().to_dict()\n        }\n        \n        # Add sample data preview (first 3 rows)\n        analysis['sample_data'] = df.head(3).to_dict('records')\n        \n        validation_result = {\n            'file_valid': True,\n            'analysis': analysis\n        }\n        \n        print(f'File validation successful!')\n        print(f'Rows: {analysis[\"rows\"]}, Columns: {analysis[\"columns\"]}')\n        print(f'Columns: {\", \".join(analysis[\"column_names\"][:5])}{\", ...\" if len(analysis[\"column_names\"]) > 5 else \"\"}')\n        \n    except Exception as e:\n        validation_result = {\n            'file_valid': False,\n            'error': f'File validation failed: {str(e)}'\n        }\nelse:\n    validation_result = {\n        'file_valid': False,\n        'error': 'Download failed, cannot validate file'\n    }"
                },
                "output": "file_validation"
            },
            {
                "type": "actions",
                "name": "generate_report",
                "details": {
                    "data": {
                        "download_config": "{{ACTION_OUTPUT:download_config}}",
                        "download_status": "{{ACTION_OUTPUT:download_status}}",
                        "file_validation": "{{ACTION_OUTPUT:file_validation}}",
                        "report_generated": "{{ACTION_OUTPUT:trigger_timestamp}}"
                    },
                    "format": "json"
                },
                "output": "download_report"
            },
            {
                "type": "actions",
                "name": "notify_user",
                "details": {
                    "user": "admin",
                    "message": "Google Sheets download completed. Status: {{ACTION_OUTPUT:download_status.success}}. File: {{ACTION_OUTPUT:download_status.filename}}. Report available at: {{ACTION_OUTPUT:download_report}}",
                    "method": "email"
                },
                "output": "notification_sent"
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
    },
    "Email to Task Manager": {
    "description": "Automatically creates tasks from emails with specific keywords and sends notifications",
    "category": "productivity",
    "steps_count": 7,
    "steps": [
        {
            "type": "triggers",
            "name": "schedule_trigger",
            "details": {
                "frequency": "every_15_minutes",
                "time": "00:00"
            },
            "output": "email_check_trigger"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import imaplib\nimport email\nimport json\nfrom datetime import datetime, timedelta\n\n# Email configuration (placeholder - would need actual credentials)\nemail_config = {\n    'server': 'imap.gmail.com',\n    'username': 'your_email@gmail.com',\n    'keywords': ['TODO', 'TASK', 'URGENT', 'ACTION REQUIRED']\n}\n\n# Simulate email checking (in real implementation, would connect to actual email)\nfound_emails = [\n    {\n        'subject': 'TODO: Review quarterly reports',\n        'sender': 'manager@company.com',\n        'body': 'Please review the Q4 reports by Friday',\n        'received': datetime.now().isoformat(),\n        'priority': 'high'\n    },\n    {\n        'subject': 'URGENT: Client meeting preparation',\n        'sender': 'client@example.com', \n        'body': 'Need presentation ready for Monday meeting',\n        'received': datetime.now().isoformat(),\n        'priority': 'urgent'\n    }\n]\n\nprint(json.dumps(found_emails))"
            },
            "output": "task_emails"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Process these emails and extract actionable tasks: {{ACTION_OUTPUT:task_emails}}. For each email, create a structured task with title, description, priority, due date, and assignee information.",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "processed_tasks"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/tasks/task_list.json",
                "task": "append {{ACTION_OUTPUT:processed_tasks}}"
            },
            "output": "tasks_saved"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.slack.com/api/chat.postMessage",
                "method": "POST",
                "headers": {"Authorization": "Bearer slack_token_here", "Content-Type": "application/json"},
                "body": "{\"channel\": \"#tasks\", \"text\": \"New tasks created from emails: {{ACTION_OUTPUT:processed_tasks}}\"}"
            },
            "output": "slack_notification"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "task_manager",
                "message": "Created {{ACTION_OUTPUT:task_emails.length}} new tasks from emails. Check task list for details.",
                "method": "email"
            },
            "output": "user_notified"
        }
    ]
},

"Form Submission to CRM Pipeline": {
    "description": "Processes form submissions, adds to CRM, sends welcome emails, and creates follow-up tasks",
    "category": "marketing",
    "steps_count": 9,
    "steps": [
        {
            "type": "triggers",
            "name": "file_created_trigger",
            "details": {
                "file_path": "/forms/submissions/"
            },
            "output": "new_submission"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Process this form submission data and extract contact information, interests, and lead scoring details.",
                "read_file_flag": "true",
                "file_path": "{{ACTION_OUTPUT:new_submission}}"
            },
            "output": "lead_data"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\nimport hashlib\nfrom datetime import datetime\n\n# Process lead data and create CRM record\nlead_info = {\n    'id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],\n    'source': 'website_form',\n    'timestamp': datetime.now().isoformat(),\n    'status': 'new_lead',\n    'score': 75,  # Default scoring\n    'next_action': 'send_welcome_email'\n}\n\nprint(json.dumps(lead_info))"
            },
            "output": "crm_record"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.hubspot.com/crm/v3/objects/contacts",
                "method": "POST", 
                "headers": {"Authorization": "Bearer hubspot_token", "Content-Type": "application/json"},
                "body": "{\"properties\": {{ACTION_OUTPUT:lead_data}}}"
            },
            "output": "crm_response"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Create a personalized welcome email based on this lead data: {{ACTION_OUTPUT:lead_data}}. Make it engaging and relevant to their interests.",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "welcome_email"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.sendgrid.com/v3/mail/send",
                "method": "POST",
                "headers": {"Authorization": "Bearer sendgrid_api_key", "Content-Type": "application/json"},
                "body": "{\"personalizations\": [{\"to\": [{{ACTION_OUTPUT:lead_data.email}}]}], \"from\": {\"email\": \"welcome@company.com\"}, \"subject\": \"Welcome!\", \"content\": [{\"type\": \"text/html\", \"value\": \"{{ACTION_OUTPUT:welcome_email}}\"}]}"
            },
            "output": "email_sent"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/crm/follow_up_tasks.json",
                "task": "append {\"lead_id\": \"{{ACTION_OUTPUT:crm_record.id}}\", \"task\": \"Follow up in 3 days\", \"due_date\": \"{{ACTION_OUTPUT:crm_record.timestamp}}\", \"priority\": \"medium\"}"
            },
            "output": "follow_up_created"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "sales_team",
                "message": "New lead processed: {{ACTION_OUTPUT:lead_data.name}}. CRM updated, welcome email sent, follow-up scheduled.",
                "method": "slack"
            },
            "output": "team_notified"
        }
    ]
},

"Social Media Monitor & Response": {
    "description": "Monitors social media mentions, analyzes sentiment, and creates response drafts",
    "category": "marketing",
    "steps_count": 8,
    "steps": [
        {
            "type": "triggers",
            "name": "schedule_trigger", 
            "details": {
                "frequency": "every_30_minutes",
                "time": "00:00"
            },
            "output": "social_check_trigger"
        },
        {
            "type": "actions",
            "name": "super_search_plus",
            "details": {
                "query": "site:twitter.com OR site:facebook.com OR site:linkedin.com \"YourBrandName\" OR \"@YourHandle\"",
                "niche": "social_media"
            },
            "output": "social_mentions"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Analyze these social media mentions for sentiment, urgency, and response requirements: {{ACTION_OUTPUT:social_mentions}}. Categorize as positive, negative, neutral, or urgent.",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "sentiment_analysis"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\nfrom datetime import datetime\n\n# Process sentiment analysis and create response priorities\nresponse_queue = []\nfor mention in {{ACTION_OUTPUT:sentiment_analysis}}:\n    if mention.get('sentiment') == 'negative' or mention.get('urgency') == 'high':\n        response_queue.append({\n            'priority': 'urgent',\n            'mention': mention,\n            'response_needed': True,\n            'escalate': True\n        })\n    elif mention.get('sentiment') == 'positive':\n        response_queue.append({\n            'priority': 'normal',\n            'mention': mention,\n            'response_needed': True,\n            'escalate': False\n        })\n\nprint(json.dumps(response_queue))"
            },
            "output": "response_queue"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Create appropriate response drafts for each high-priority social media mention: {{ACTION_OUTPUT:response_queue}}. Make responses professional, empathetic, and brand-appropriate.",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "response_drafts"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/social_media/pending_responses.json",
                "task": "replace entire content with {{ACTION_OUTPUT:response_drafts}}"
            },
            "output": "responses_saved"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "social_media_team",
                "message": "Found {{ACTION_OUTPUT:response_queue.length}} social mentions requiring response. Check pending_responses.json for drafts.",
                "method": "slack"
            },
            "output": "team_alerted"
        }
    ]
},

"Invoice Processing Workflow": {
    "description": "Processes invoices, extracts data, updates accounting system, and sends payment reminders",
    "category": "finance", 
    "steps_count": 10,
    "steps": [
        {
            "type": "triggers",
            "name": "file_created_trigger",
            "details": {
                "file_path": "/invoices/incoming/"
            },
            "output": "new_invoice"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Extract invoice data including vendor, amount, due date, invoice number, and line items from this document.",
                "read_file_flag": "true",
                "file_path": "{{ACTION_OUTPUT:new_invoice}}"
            },
            "output": "invoice_data"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\nimport re\nfrom datetime import datetime, timedelta\n\n# Process extracted invoice data\ninvoice_info = {\n    'processed_date': datetime.now().isoformat(),\n    'status': 'pending_approval',\n    'payment_due': (datetime.now() + timedelta(days=30)).isoformat(),\n    'approval_required': True if float({{ACTION_OUTPUT:invoice_data}}.get('amount', 0)) > 1000 else False\n}\n\nprint(json.dumps(invoice_info))"
            },
            "output": "processed_invoice"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.quickbooks.com/v3/company/invoices",
                "method": "POST",
                "headers": {"Authorization": "Bearer qb_token", "Content-Type": "application/json"},
                "body": "{\"invoice_data\": {{ACTION_OUTPUT:invoice_data}}, \"status\": \"{{ACTION_OUTPUT:processed_invoice.status}}\"}"
            },
            "output": "accounting_updated"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\n\n# Check if approval is needed\nif {{ACTION_OUTPUT:processed_invoice}}.get('approval_required'):\n    approval_message = f\"Invoice requires approval: Amount ${{{ACTION_OUTPUT:invoice_data.amount}}} from {{{ACTION_OUTPUT:invoice_data.vendor}}}\"\n    approval_needed = True\nelse:\n    approval_message = \"Invoice auto-approved and processed\"\n    approval_needed = False\n\nresult = {\n    'approval_needed': approval_needed,\n    'message': approval_message\n}\n\nprint(json.dumps(result))"
            },
            "output": "approval_check"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "finance_manager",
                "message": "{{ACTION_OUTPUT:approval_check.message}} - Invoice: {{ACTION_OUTPUT:invoice_data.invoice_number}}",
                "method": "email"
            },
            "output": "approval_notification"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/invoices/processed/invoice_log.json",
                "task": "append {\"invoice\": {{ACTION_OUTPUT:invoice_data}}, \"processed\": {{ACTION_OUTPUT:processed_invoice}}, \"timestamp\": \"{{ACTION_OUTPUT:processed_invoice.processed_date}}\"}"
            },
            "output": "log_updated"
        },
        {
            "type": "actions",
            "name": "display_message",
            "details": {
                "message": "Invoice processing completed. {{ACTION_OUTPUT:approval_check.message}}"
            },
            "output": ""
        }
    ]
},

"Calendar Event Sync & Notification": {
    "description": "Syncs events across calendars, sends smart reminders, and creates preparation tasks",
    "category": "productivity",
    "steps_count": 8,
    "steps": [
        {
            "type": "triggers",
            "name": "schedule_trigger",
            "details": {
                "frequency": "every_hour",
                "time": "00:00"
            },
            "output": "calendar_sync_trigger"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://www.googleapis.com/calendar/v3/calendars/primary/events",
                "method": "GET",
                "headers": {"Authorization": "Bearer google_calendar_token"},
                "body": ""
            },
            "output": "google_events"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Analyze upcoming calendar events: {{ACTION_OUTPUT:google_events}}. Identify meetings that need preparation, travel time, or special arrangements. Create smart reminders and preparation tasks.",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "event_analysis"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\nfrom datetime import datetime, timedelta\n\n# Process events and create smart notifications\nsmart_reminders = []\nfor event in {{ACTION_OUTPUT:event_analysis}}:\n    event_time = datetime.fromisoformat(event.get('start_time', ''))\n    \n    # Create different reminder types based on event\n    if 'meeting' in event.get('title', '').lower():\n        smart_reminders.append({\n            'type': 'preparation',\n            'message': f\"Prepare for meeting: {event.get('title')}\",\n            'remind_at': (event_time - timedelta(hours=2)).isoformat(),\n            'event_id': event.get('id')\n        })\n    \n    if event.get('location'):\n        smart_reminders.append({\n            'type': 'travel',\n            'message': f\"Leave for {event.get('title')} at {event.get('location')}\",\n            'remind_at': (event_time - timedelta(minutes=30)).isoformat(),\n            'event_id': event.get('id')\n        })\n\nprint(json.dumps(smart_reminders))"
            },
            "output": "smart_reminders"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://outlook.office.com/api/v2.0/me/events",
                "method": "POST",
                "headers": {"Authorization": "Bearer outlook_token", "Content-Type": "application/json"},
                "body": "{\"events\": {{ACTION_OUTPUT:google_events}}}"
            },
            "output": "outlook_sync"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/calendar/reminders_queue.json",
                "task": "replace entire content with {{ACTION_OUTPUT:smart_reminders}}"
            },
            "output": "reminders_saved"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "calendar_owner",
                "message": "Calendar sync completed. {{ACTION_OUTPUT:smart_reminders.length}} smart reminders scheduled.",
                "method": "push_notification"
            },
            "output": "sync_notification"
        }
    ]
},

"E-commerce Order Processing": {
    "description": "Processes new orders, updates inventory, sends confirmations, and creates shipping labels",
    "category": "ecommerce",
    "steps_count": 11,
    "steps": [
        {
            "type": "triggers",
            "name": "file_created_trigger",
            "details": {
                "file_path": "/orders/new/"
            },
            "output": "new_order"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Process this e-commerce order and extract customer info, items, quantities, shipping details, and payment status.",
                "read_file_flag": "true",
                "file_path": "{{ACTION_OUTPUT:new_order}}"
            },
            "output": "order_details"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\nfrom datetime import datetime\n\n# Process order and check inventory\norder_processing = {\n    'order_id': {{ACTION_OUTPUT:order_details}}.get('order_id'),\n    'processed_at': datetime.now().isoformat(),\n    'status': 'processing',\n    'estimated_ship_date': (datetime.now() + timedelta(days=2)).isoformat(),\n    'tracking_number': f\"TRK{datetime.now().strftime('%Y%m%d%H%M%S')}\"\n}\n\n# Check inventory for each item\ninventory_updates = []\nfor item in {{ACTION_OUTPUT:order_details}}.get('items', []):\n    inventory_updates.append({\n        'sku': item.get('sku'),\n        'quantity_ordered': item.get('quantity'),\n        'action': 'reduce_stock'\n    })\n\nprint(json.dumps({'processing': order_processing, 'inventory': inventory_updates}))"
            },
            "output": "order_processing"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.shopify.com/admin/api/inventory_levels.json",
                "method": "PUT",
                "headers": {"X-Shopify-Access-Token": "shopify_token", "Content-Type": "application/json"},
                "body": "{\"inventory_updates\": {{ACTION_OUTPUT:order_processing.inventory}}}"
            },
            "output": "inventory_updated"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Create a professional order confirmation email for this customer: {{ACTION_OUTPUT:order_details}}. Include order summary, tracking info, and estimated delivery.",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "confirmation_email"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.sendgrid.com/v3/mail/send",
                "method": "POST",
                "headers": {"Authorization": "Bearer sendgrid_key", "Content-Type": "application/json"},
                "body": "{\"personalizations\": [{\"to\": [{{ACTION_OUTPUT:order_details.customer_email}}]}], \"from\": {\"email\": \"orders@store.com\"}, \"subject\": \"Order Confirmation #{{ACTION_OUTPUT:order_details.order_id}}\", \"content\": [{\"type\": \"text/html\", \"value\": \"{{ACTION_OUTPUT:confirmation_email}}\"}]}"
            },
            "output": "email_sent"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.shipstation.com/orders",
                "method": "POST",
                "headers": {"Authorization": "Basic shipstation_auth", "Content-Type": "application/json"},
                "body": "{\"orderNumber\": \"{{ACTION_OUTPUT:order_details.order_id}}\", \"orderDate\": \"{{ACTION_OUTPUT:order_processing.processing.processed_at}}\", \"shipTo\": {{ACTION_OUTPUT:order_details.shipping_address}}, \"items\": {{ACTION_OUTPUT:order_details.items}}}"
            },
            "output": "shipping_created"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/orders/processed/order_log.json",
                "task": "append {\"order\": {{ACTION_OUTPUT:order_details}}, \"processing\": {{ACTION_OUTPUT:order_processing}}, \"shipped\": {{ACTION_OUTPUT:shipping_created}}}"
            },
            "output": "order_logged"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "fulfillment_team",
                "message": "New order processed: #{{ACTION_OUTPUT:order_details.order_id}} - ${{ACTION_OUTPUT:order_details.total}}. Shipping label created.",
                "method": "slack"
            },
            "output": "team_notified"
        },
        {
            "type": "actions",
            "name": "display_message",
            "details": {
                "message": "Order #{{ACTION_OUTPUT:order_details.order_id}} successfully processed and queued for shipping."
            },
            "output": ""
        }
    ]
},

"Survey Response Analyzer": {
    "description": "Processes survey responses, analyzes feedback, generates insights, and creates action items",
    "category": "analytics",
    "steps_count": 9,
    "steps": [
        {
            "type": "triggers",
            "name": "file_created_trigger",
            "details": {
                "file_path": "/surveys/responses/"
            },
            "output": "survey_responses"
        },
        {
            "type": "actions",
            "name": "run_py_code", 
            "details": {
                "code": "import pandas as pd\nimport json\nfrom collections import Counter\n\n# Load and analyze survey data\ndf = pd.read_csv('{{ACTION_OUTPUT:survey_responses}}')\n\n# Basic analysis\nanalysis = {\n    'total_responses': len(df),\n    'response_rate': 85.5,  # Would calculate from actual data\n    'avg_satisfaction': df.get('satisfaction', pd.Series([0])).mean() if 'satisfaction' in df.columns else 0,\n    'completion_rate': (len(df) / len(df)) * 100,  # Simplified\n    'top_issues': [],\n    'demographics': {}\n}\n\n# Analyze text responses for common themes\nif 'feedback' in df.columns:\n    feedback_words = ' '.join(df['feedback'].fillna('').astype(str)).lower().split()\n    common_words = Counter(feedback_words).most_common(10)\n    analysis['common_themes'] = [word for word, count in common_words if len(word) > 3]\n\nprint(json.dumps(analysis))"
            },
            "output": "survey_analysis"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Analyze survey results: {{ACTION_OUTPUT:survey_analysis}} and the raw data. Identify key insights, trends, areas for improvement, and actionable recommendations.",
                "read_file_flag": "true",
                "file_path": "{{ACTION_OUTPUT:survey_responses}}"
            },
            "output": "insights_report"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import matplotlib.pyplot as plt\nimport seaborn as sns\nimport json\n\n# Create visualizations\nplt.figure(figsize=(12, 8))\n\n# Satisfaction distribution\nplt.subplot(2, 2, 1)\nsatisfaction_data = [4.2, 3.8, 4.5, 3.9, 4.1]  # Sample data\nplt.bar(range(len(satisfaction_data)), satisfaction_data)\nplt.title('Satisfaction by Category')\nplt.ylabel('Average Rating')\n\n# Response trends\nplt.subplot(2, 2, 2)\ntrend_data = [45, 52, 48, 61, 58]  # Sample monthly responses\nplt.plot(range(len(trend_data)), trend_data, marker='o')\nplt.title('Response Trends')\nplt.ylabel('Number of Responses')\n\nplt.tight_layout()\nplt.savefig('/surveys/analysis/survey_charts.png', dpi=300, bbox_inches='tight')\n\nvisualization_info = {\n    'charts_created': True,\n    'chart_path': '/surveys/analysis/survey_charts.png',\n    'chart_types': ['satisfaction_distribution', 'response_trends']\n}\n\nprint(json.dumps(visualization_info))"
            },
            "output": "survey_charts"
        },
        {
            "type": "actions",
            "name": "think",
            "details": {
                "text_input": "Create a comprehensive survey analysis report in HTML format including: executive summary, key findings, visualizations, recommendations, and action items. Use the analysis: {{ACTION_OUTPUT:insights_report}} and charts: {{ACTION_OUTPUT:survey_charts}}",
                "read_file_flag": "false",
                "file_path": ""
            },
            "output": "html_report"
        },
        {
            "type": "actions",
            "name": "modify_file",
            "details": {
                "file_path": "/surveys/reports/survey_analysis_report.html",
                "task": "replace entire content with {{ACTION_OUTPUT:html_report}}"
            },
            "output": "report_saved"
        },
        {
            "type": "actions",
            "name": "run_py_code",
            "details": {
                "code": "import json\nfrom datetime import datetime, timedelta\n\n# Generate action items based on survey insights\naction_items = [\n    {\n        'title': 'Address customer service response time',\n        'priority': 'high',\n        'assigned_to': 'customer_service_manager',\n        'due_date': (datetime.now() + timedelta(days=14)).isoformat(),\n        'description': 'Improve response time based on survey feedback'\n    },\n    {\n        'title': 'Update product documentation',\n        'priority': 'medium',\n        'assigned_to': 'product_team',\n        'due_date': (datetime.now() + timedelta(days=30)).isoformat(),\n        'description': 'Address confusion mentioned in survey responses'\n    }\n]\n\nprint(json.dumps(action_items))"
            },
            "output": "action_items"
        },
        {
            "type": "actions",
            "name": "make_api_request",
            "details": {
                "url": "https://api.trello.com/1/cards",
                "method": "POST",
                "headers": {"Authorization": "OAuth trello_token", "Content-Type": "application/json"},
                "body": "{\"name\": \"Survey Action Items\", \"desc\": \"{{ACTION_OUTPUT:action_items}}\", \"idList\": \"trello_board_id\"}"
            },
            "output": "trello_cards_created"
        },
        {
            "type": "actions",
            "name": "notify_user",
            "details": {
                "user": "product_manager",
                "message": "Survey analysis completed. {{ACTION_OUTPUT:survey_analysis.total_responses}} responses analyzed. Report available at /surveys/reports/. {{ACTION_OUTPUT:action_items.length}} action items created.",
                "method": "email"
            },
            "output": "analysis_notification"
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
