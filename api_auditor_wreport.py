import os
import sys
import yaml
import requests
from datetime import datetime
from groq import Groq
from jsonschema import validate, ValidationError

# Initialize the Groq Client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your_free_groq_api_key_here")
client = Groq(api_key=GROQ_API_KEY)

def generate_ai_payload(endpoint_spec, method, endpoint_path):
    """Uses Groq to generate a valid test payload matching the exact endpoint contract"""
    print(f"🤖 AI is generating a test payload for {method.upper()} {endpoint_path}...")
    
    prompt = f"""
    Analyze this OpenAPI path specification and generate a valid JSON request payload that fits the request body requirements.
    Provide ONLY the raw JSON object inside code blocks. Do not write explanations.
    
    Specification:
    {yaml.dump(endpoint_spec)}
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        response_text = completion.choices[0].message.content
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        return yaml.safe_load(response_text[json_start:json_end])
    except Exception as e:
        print(f"⚠️ AI Generation skipped or failed: {e}. Defaulting to empty object.")
        return {}

def generate_html_report(swagger_file, base_url, total_endpoints, violations):
    """Generates a clean, time-stamped responsive HTML report dashboard file"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    display_time = datetime.now().strftime("%d %B %Y, %I:%M %p")
    report_filename = f"compliance_report_{timestamp}.html"
    
    status_class = "pass" if not violations else "fail"
    status_text = "PASSED (COMPLIANT)" if not violations else "FAILED (NON-COMPLIANT)"
    
    # Constructing individual list items for table view metrics
    violation_rows = ""
    if violations:
        for idx, v in enumerate(violations, start=1):
            violation_rows += f"<tr><td>{idx}</td><td class='err-text'>{v}</td></tr>"
    else:
        violation_rows = "<tr><td colspan='2' style='text-align:center; color: #2e7d32;'>🎉 Perfect Score! No contract rule violations found.</td></tr>"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Swagger Compliance Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f5f7fb; margin: 0; padding: 40px; color: #333; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
        h1 {{ margin-top: 0; color: #1e293b; font-size: 28px; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; }}
        .meta-box {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #edf2f7; }}
        .meta-item {{ font-size: 14px; color: #64748b; }}
        .meta-item strong {{ color: #334155; }}
        .status-badge {{ display: inline-block; padding: 8px 16px; font-weight: bold; border-radius: 6px; font-size: 14px; text-transform: uppercase; margin-top: 5px; }}
        .status-badge.pass {{ background-color: #d1fae5; color: #065f46; }}
        .status-badge.fail {{ background-color: #fee2e2; color: #991b1b; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 15px; }}
        th {{ background-color: #f1f5f9; color: #475569; font-weight: 600; }}
        .err-text {{ color: #b91c1c; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 14px; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>API Contract Compliance Evaluation Report</h1>
        <div class="meta-box">
            <div>
                <div class="meta-item"><strong>Swagger Spec File:</strong> {swagger_file}</div>
                <div class="meta-item"><strong>Target Base URL:</strong> <a href="{base_url}" target="_blank">{base_url}</a></div>
                <div class="meta-item"><strong>Total Endpoints Audited:</strong> {total_endpoints}</div>
            </div>
            <div>
                <div class="meta-item"><strong>Execution Timestamp:</strong> {display_time}</div>
                <div class="meta-item"><strong>Audit Integrity Verdict:</strong><br>
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 60px;">Index</th>
                    <th>Violation Rule Tracking Breakdowns Log</th>
                </tr>
            </thead>
            <tbody>
                {violation_rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    try:
        with open(report_filename, 'w') as file:
            file.write(html_content)
        print(f"\n✨ Automated HTML report generated successfully: {report_filename}")
    except Exception as e:
        print(f"❌ Failed to write report file to disk: {e}")

def execute_dynamic_audit(base_url, swagger_file_path):
    """Parses any Swagger YAML file dynamically and tracks contract discrepancies"""
    print(f"📖 Target URL Base: {base_url}")
    print(f"📖 Loading Swagger specification file: {swagger_file_path}")
    
    try:
        with open(swagger_file_path, 'r') as file:
            spec = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"❌ Error: The file '{swagger_file_path}' does not exist.")
        sys.exit(1)

    violations_report = []
    paths = spec.get('paths', {})
    total_endpoints_counted = 0

    for path_url, path_details in paths.items():
        for method, operation in path_details.items():
            if method not in ['get', 'post', 'put', 'delete']:
                continue
                
            total_endpoints_counted += 1
            print(f"\n🔍 Auditing route: {method.upper()} {path_url}")
            
            payload = None
            if method in ['post', 'put'] and 'requestBody' in operation:
                payload = generate_ai_payload(operation, method, path_url)
                print(f"   📦 Sending Payload: {payload}")

            full_target_url = f"{base_url.rstrip('/')}{path_url}"
            try:
                if method == 'post':
                    response = requests.post(full_target_url, json=payload)
                elif method == 'put':
                    response = requests.put(full_target_url, json=payload)
                else:
                    response = requests.get(full_target_url)
                
                try:
                    response_data = response.json()
                except Exception:
                    response_data = {"text": response.text}

                status_code = str(response.status_code)
                responses_spec = operation.get('responses', {})
                
                if status_code in responses_spec:
                    content_spec = responses_spec[status_code].get('content', {})
                    json_schema_spec = content_spec.get('application/json', {}).get('schema')
                    
                    if json_schema_spec:
                        try:
                            validate(instance=response_data, schema=json_schema_spec)
                            print(f"   ✅ {status_code} Response matched Swagger definition successfully.")
                        except ValidationError as ve:
                            violation_msg = f"In {method.upper()} {path_url} ({status_code}): Field '{'.'.join(map(str, ve.path))}' broke rule: {ve.message}"
                            violations_report.append(violation_msg)
                            print(f"   🚩 Contract Violation Flagged!")
                    else:
                        print(f"   ℹ️ No explicit JSON response schema found for status {status_code}.")
                else:
                    violation_msg = f"Undocumented Status Code: {method.upper()} {path_url} returned HTTP {status_code}, which is missing from the Swagger file rules."
                    violations_report.append(violation_msg)
                    print(f"   🚩 Unexpected status code received!")

            except Exception as e:
                print(f"   ❌ Network error trying to connect to {full_target_url}: {e}")

    # 📊 Compile Console report and write the final automated HTML report file
    print("\n" + "="*50)
    print("📋 FINAL COMPLIANCE CONTRACT REPORT SUMMARY")
    print("="*50)
    if not violations_report:
        print("🎉 EXCELLENT: Zero contract rule violations were found across your API implementation!")
    else:
        print(f"🚩 Found {len(violations_report)} contract rule violations:")
        for idx, violation in enumerate(violations_report, start=1):
            print(f" {idx}. {violation}")
    print("="*50)
    
    # Fire off HTML file creation routine 
    generate_html_report(swagger_file_path, base_url, total_endpoints_counted, violations_report)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\n❌ Missing parameters!")
        print("📌 Usage: python3 api_auditor.py <path_to_swagger_file> <target_base_url>")
        print("💡 Example: python3 api_auditor.py my_swagger.yaml http://127.0.0.1:8000\n")
        sys.exit(1)
        
    user_file_path = sys.argv[1]
    user_base_url = sys.argv[2]
    
    execute_dynamic_audit(base_url=user_base_url, swagger_file_path=user_file_path)
