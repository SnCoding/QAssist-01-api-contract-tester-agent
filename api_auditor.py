import os
import sys
import yaml
import requests
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
        response_text = completion.choices.message.content
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        return yaml.safe_load(response_text[json_start:json_end])
    except Exception as e:
        print(f"⚠️ AI Generation skipped or failed: {e}. Defaulting to empty object.")
        return {}

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

    for path_url, path_details in paths.items():
        for method, operation in path_details.items():
            if method not in ['get', 'post', 'put', 'delete']:
                continue
                
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

# 🌟 STEP 4: Read variables dynamically from terminal input parameters
if __name__ == "__main__":
    # Ensure the user provides exactly 2 arguments (file path and base target url)
    if len(sys.argv) < 3:
        print("\n❌ Missing parameters!")
        print("📌 Usage: python3 api_auditor.py <path_to_swagger_file> <target_base_url>")
        print("💡 Example: python3 api_auditor.py my_swagger.yaml http://127.0.0.1:8000\n")
        sys.exit(1)
        
    user_file_path = sys.argv[1]
    user_base_url = sys.argv[2]
    
    execute_dynamic_audit(base_url=user_base_url, swagger_file_path=user_file_path)
