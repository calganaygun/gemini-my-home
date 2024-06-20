# Gemini My Home

Gemini My Home is a project that leverages the Google Gemini API to ask questions about your home. This project connects a large language model (LLM) to your home CCTV cameras (via RTSP) and enables querying and monitoring your home using a multi-modal interface.

## Features

- **Interactive Queries**: Ask questions about different areas in your home by connecting Gemini to CCTV cameras.
- **Multi-Modal Interface**: Utilize text and visual data for comprehensive home monitoring.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/calganaygun/gemini-my-home.git
    cd gemini-my-home
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before using the project, configure the `devices.yaml` file with your device and API information. This file should include details about your cameras, rooms, and other relevant information.

## Notes
This project requires a Google Gemini API key to access the language model. You can obtain an API key by following the instructions in the [official documentation](https://ai.google.dev/gemini-api/docs/api-key).

This project highly inspired by the [joshblake87's project](https://www.reddit.com/r/homeassistant/comments/1dgzuh7/extended_openai_image_query_is_next_level/).