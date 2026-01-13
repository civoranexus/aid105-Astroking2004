import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Any

load_dotenv()

# Configure Gemini API
# The user should set GOOGLE_API_KEY in their environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)  # type: ignore

async def generate_chat_response(query: str, context_schemes: List[Dict[str, Any]]) -> str:
    """
    Generates a response to a user query using Gemini, providing scheme context.
    """
    if not GOOGLE_API_KEY:
        return "AI features are currently unavailable. Please set the GOOGLE_API_KEY environment variable."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
        
        # Format context for the prompt to help the AI understand available schemes
        context_text = "\n".join([
            f"- {s.get('title')}: {s.get('description')}" 
            for s in context_schemes
        ])

        prompt = (
            f"You are 'SchemeAssist AI', a helpful assistant designed to help citizens find "
            f"government schemes. Use the following list of schemes to answer the user's question. "
            f"If the information is not in the list, use your general knowledge but mention it's general info.\n\n"
            f"Available Schemes:\n{context_text}\n\n"
            f"User Question: {query}\n\n"
            f"Response:"
        )

        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Error generating AI response: {str(e)}"