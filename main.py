import google.generativeai as genai
from rtsp_record import snapshot_rtsp_stream
from PIL import Image
from PIL import PngImagePlugin # strange bug https://github.com/google-gemini/generative-ai-python/issues/178
import yaml
import sys
from bullet import Input, colors

def load_config(filename='devices.yaml'):
    """Loads the configuration from a YAML file."""
    try:
        with open(filename, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file exists and is readable.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error reading {filename}: {e}. Please ensure it is in valid YAML format.")
        sys.exit(1)

def get_camera_address(cam_id: str) -> str:
    """Returns the RTSP address of the camera with the given ID."""
    device = next((device for device in devices if device['id'] == cam_id), None)
    return device['address'] if device else None

def capture_camera_snapshot(cam_id: str) -> Image:
    """Returns a snapshot from the camera with the given ID."""
    rtsp_url = get_camera_address(cam_id)
    if rtsp_url:
        return snapshot_rtsp_stream(rtsp_url).convert("RGB")
    else:
        print(f"No camera found with ID {cam_id}")
        return None

# Global function map
FUNCTION_MAP = {
    "capture_camera_snapshot": capture_camera_snapshot
}

def initialize_model(config):
    """Initializes the generative AI model with the given configuration."""
    genai.configure(api_key=config.get("gemini", {}).get("key"))
    return genai.GenerativeModel(
        model_name=config.get("gemini", {}).get("model"),
        tools=list(FUNCTION_MAP.values()),
        system_instruction=f"""
        {config.get("system_prompt", "")}

        Here are the cameras in your home:
        ```csv
        id,name,location,info
        {generate_csv_body(config.get("devices", []))}
        ```

        Here is some extra info about the home, and the people living in it:
        {config.get("home_info", "")}
        """.strip()
    )

def generate_csv_body(devices):
    """Generates a CSV body from the list of devices."""
    return "\n".join([f"{device['id']},{device['name']},{device['location']},{device['info']}" for device in devices])

def handle_model_response(model, messages):
    """Handles the response cycle with the generative AI model."""
    text_returned = False
    while not text_returned:
        text_returned = True
        response = model.generate_content(messages)
        for part in response.parts:
            if part.function_call:
                handle_function_call(part.function_call, messages)
                text_returned = False
            else:
                messages.append("SYSTEM: " + part.text)

def handle_function_call(function_call, messages):
    """Handles the function call from the AI model."""
    function_name = function_call.name
    if function_name in FUNCTION_MAP:
        args = dict(function_call.args.items())
        result = FUNCTION_MAP[function_name](**args)
        if result:
            messages.append(f"SYSTEM: Requested snapshot from the camera {args['cam_id']}. Here is the snapshot:")
            messages.append(result)

def main():
    """Main function to handle user input and responses."""
    device_config = load_config()
    global devices
    devices = device_config.get("devices", [])

    if not devices:
        print("No devices found in the devices.yaml file. Please ensure the file contains a list of devices.")
        sys.exit(1)

    google_api_key = device_config.get("gemini", {}).get("key")
    model_name = device_config.get("gemini", {}).get("model")

    if not google_api_key or not model_name:
        print("Please provide the Google API key and the model name in the devices.yaml file.")
        sys.exit(1)

    print(f"Gemini My Home started with {len(devices)} cameras.")
    print("You can ask questions about the cameras. For example, you can ask 'What is happening in the living room?'")
    print("Type 'exit' or 'quit' to terminate the application.")

    model = initialize_model(device_config)
    messages = []

    prompt = Input(" >>> ", word_color=colors.foreground["cyan"])

    while True:
        request = prompt.launch()
        if request.lower() in ("exit", "quit"):
            print("Exiting Gemini My Home. Goodbye!")
            break
        messages.append("USER: " + request)
        last_index = len(messages)
        handle_model_response(model, messages)
        for message in messages[last_index:]:
            output = message if isinstance(message, str) else "SYSTEM: IMAGE SENT BY SYSTEM, NOT A TEXT"
            prefix = " >>> " if "USER" in output else " <<< "
            print(prefix + output)

if __name__ == "__main__":
    main()