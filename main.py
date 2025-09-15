from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import uvicorn

# ------------------------------
# FastAPI App Setup
# ------------------------------
app = FastAPI(title="Farming Chatbot API", version="1.0.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Request/Response Models
# ------------------------------
class ChatMessage(BaseModel):
    message: str
    crop_type: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    crop_type: Optional[str] = None
    suggestions: Optional[List[str]] = None

# ------------------------------
# Farming Chatbot Class
# ------------------------------
class FarmingChatbot:
    def __init__(self):
        self.crop_data = self.load_crop_data_safe('data/crop_data.json')
        self.conversation_context = {}

    def load_crop_data_safe(self, filename):
        if not os.path.exists(filename):
            print(f"❌ File {filename} not found. Using empty data.")
            return {}
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_available_crops(self) -> List[str]:
        return list(self.crop_data.keys())

    def detect_crop(self, message: str) -> Optional[str]:
        message_lower = message.lower()
        for crop in self.crop_data.keys():
            if crop.lower() in message_lower:
                return crop
        return None

    def find_matching_topic(self, message: str, crop_info: dict) -> Optional[str]:
        """Detect which topic the user is asking about"""
        message_lower = message.lower()
        keyword_map = {
            # Existing
            'plant': 'season',
            'sow': 'season',
            'water': 'watering',
            'irrigation': 'irrigation_methods',
            'fertilizer': 'fertilizer',
            'nutrition': 'fertilizer',
            'harvest': 'harvesting',
            'problem': 'pests',
            'disease': 'pests',
            'pest': 'pests',
            'tip': 'organic_tips',
            'advice': 'organic_tips',
            'soil': 'soil',
            'yield': 'yield',
            'spacing': 'spacing',
            'variety': 'varieties',
            'germinate': 'germination',
            'intercrop': 'intercropping',
            'prune': 'pruning',
            'special': 'special_notes',
            'process': 'processing',
            'store': 'storage',
            'climate': 'climate',
            'propagate': 'propagation',
            'economic': 'economic_life'
        }

        for keyword, topic in keyword_map.items():
            if keyword in message_lower:
                return topic

        # fallback: None
        return None


    def get_crop_advice(self, crop: str, topic: str = None) -> str:
        if crop not in self.crop_data:
            return f"Sorry, I don't have information about {crop}. Available crops: {', '.join(self.get_available_crops())}"

        crop_info = self.crop_data[crop]

        # If specific topic requested
        if topic:
            if topic in crop_info:
                value = crop_info[topic]
                # If it's a list, format nicely
                if isinstance(value, list):
                    return "• " + "\n• ".join(value)
                return str(value)
            else:
                return f"No information available for {topic} of {crop}."

        # General info: summarize key points
        main_topics = ['season', 'soil', 'watering', 'fertilizer', 'pests', 'harvesting', 'yield', 'spacing', 'varieties', 'organic_tips']
        response = f"Here's general information about {crop}:\n\n"
        for t in main_topics:
            if t in crop_info:
                value = crop_info[t]
                if isinstance(value, list):
                    value = "\n• ".join(value)
                response += f"**{t.replace('_',' ').title()}:** {value}\n\n"
        return response

    def process_message(self, message: str, crop_type: str = None) -> ChatResponse:
        message_lower = message.lower()

        # Detect crop if not provided
        if not crop_type:
            crop_type = self.detect_crop(message)

        # Greetings
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey']):
            response = "Hello! I'm your farming assistant. I can help you with crop info, irrigation, fertilizers, pests, and more."
            return ChatResponse(
                response=response,
                suggestions=["What crops do you know about?", "Tell me about wheat farming"]
            )

        # Available crops
        if "what crops" in message_lower or "available crops" in message_lower:
            crops = self.get_available_crops()
            response = f"I have information about: {', '.join(crops)}"
            return ChatResponse(
                response=response,
                suggestions=[f"Complete guide for {crop}" for crop in list(crops)[:4]]
            )

        # Crop-specific queries
        if crop_type and crop_type in self.crop_data:
            specific_topic = self.find_matching_topic(message, self.crop_data[crop_type])
            advice = self.get_crop_advice(crop_type, specific_topic)
            return ChatResponse(
                response=advice,
                crop_type=crop_type,
            )

        # Default response
        response = "I'm here to help with comprehensive farming guidance! Ask me about specific crops or topics."
        return ChatResponse(
            response=response,
            suggestions=["Available crops", "Organic farming tips"]
        )

# ------------------------------
# Initialize chatbot
# ------------------------------
chatbot = FarmingChatbot()

# ------------------------------
# Serve static frontend
# ------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# ------------------------------
# API Endpoints
# ------------------------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    try:
        response = chatbot.process_message(message.message, message.crop_type)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/api/crops")
async def get_crops():
    return {"crops": chatbot.get_available_crops()}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    print("🌱 Starting Farming Chatbot Server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("📋 API docs available at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
