import os
# Correct line
from fastapi import FastAPI, Form, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')
app = FastAPI()


def get_gemini_response(user_text: str) -> str:
    """Sends user text to Gemini and gets a response."""
    try:
       
        loaded_api_key = os.getenv("GEMINI_API_KEY")
        print("--- DEBUGGING ---")
        if loaded_api_key:
          
            print(f"API Key being used: {loaded_api_key[:5]}...{loaded_api_key[-5:]}")
        else:
            print("API Key NOT FOUND in environment.")
        print("--- END DEBUGGING ---\n")
      
        
        
        prompt = f"""
You are an intelligent voice assistant for a delivery agent. Your primary goal is to accurately capture and confirm delivery details from a customer's speech.

## CONTEXT:
The customer is on a live phone call and has just spoken.
Customer's transcribed speech: "{user_text}"

## INSTRUCTIONS:
1.  **Extract Key Information**: Carefully identify two main entities from the customer's speech:
    * The full delivery address (including landmarks like "opposite rk villa house").
    * The specific drop-off instructions (including any backup plans like "beside of the shoe stand").

2.  **Formulate a Response**:
    * **If both address and drop-off instructions are clear**: Your response should have two parts. First, confirm the details in a single, concise sentence. Then, immediately follow it with the closing statement: "I have all the required information. Thanks for the response, and the order will be delivered to the specified location."
    * **If the address is clear but instructions are missing**: Confirm the address you heard and then ask a clarifying question about where to leave the package.
    * **If any part is unclear or seems contradictory**: Ask for specific clarification. For example: "I understood the address is in Urapakkam, but could you please repeat the drop-off instructions?"

3.  **Example of a Perfect Output**: "Okay, confirming the delivery to Akshaya Phase 1 in Urapakkam, leaving the package opposite the RK Villa house. I have all the required information. Thanks for the response, and the order will be delivered to the specified location."

Based on these instructions, analyze the customer's speech and generate the appropriate response now.
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I'm having trouble connecting. Could you please repeat that?"
@app.post("/voice", response_class=Response)
async def incoming_call():
    twiml_response = VoiceResponse()
    twiml_response.say("Hello, this is your delivery agent. To confirm, please state your full address and where I should leave the package.", voice='alice')   
    gather = Gather(input='speech', action='/gather', speechTimeout='auto')
    twiml_response.append(gather)
    twiml_response.redirect('/voice')
    return Response(content=str(twiml_response), media_type="application/xml")


@app.post("/gather", response_class=Response)
async def gather_speech(SpeechResult: str = Form(...)):
    """Processes the speech transcribed by Twilio."""
    twiml_response = VoiceResponse()

    if SpeechResult:
        llm_response = get_gemini_response(SpeechResult)
        
        twiml_response.say(llm_response, voice='alice')
    else:
       
        twiml_response.say("I didn't catch that. Could you please repeat the address?", voice='alice')
    
    gather = Gather(input='speech', action='/gather', speechTimeout='auto')
    twiml_response.append(gather)
    

    return Response(content=str(twiml_response), media_type="application/xml")
