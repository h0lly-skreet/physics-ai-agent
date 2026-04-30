# GenAI Physics Calculator Agent

A smart web application built with **Streamlit** and the **Google Generative AI SDK**. This agent leverages the Gemini model and **Function Calling** to accurately solve physics problems by delegating complex calculations to custom Python functions.

## Features
* **AI Function Calling:** Uses Gemini's `tools` to map natural language queries to specific Python functions (e.g., Ohm's Law, Kinetic Energy).
* **Deterministic Calculations:** Prevents AI hallucinations in math by executing precise Python logic locally.
* **Interactive UI:** A clean, user-friendly interface powered by Streamlit that displays the agent's thought process and execution steps.
* **Secure Configuration:** API keys are managed securely via environment variables.

## Tech Stack
* **Language:** Python 3.x
* **Framework:** Streamlit
* **AI/LLM:** Google Generative AI SDK (`google-genai`), Gemini 2.5 Flash

## Core Tools Implemented
1. `calculate_kinetic_energy(mass, speed)`: Computes kinetic energy (KE = 0.5 * m * v^2).
2. `calculate_ohms_law(voltage, resistance, current_strength)`: Dynamically solves for the missing variable in Ohm's Law (V = I * R).

## How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/h0lly-skreet/physics-ai-agent.git
cd physics-ai-agent
```

2. Install dependencies:
```bash
pip install streamlit google-genai
```

3. Set up your Gemini API Key:
Set the environment variable GEMINI_API_KEY with your key from Google AI Studio.
On Windows (PowerShell): `$env:GEMINI_API_KEY="your_api_key_here"`
On Linux/Mac: `export GEMINI_API_KEY="your_api_key_here"`

4. Run the Streamlit app:
```bash
streamlit run app.py
```
