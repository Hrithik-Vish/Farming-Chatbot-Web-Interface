# 🌱 Farming Chatbot Web Interface

A modern, responsive web-based chatbot interface for providing crop-specific farming advice with comprehensive agricultural information.

## 🚀 Complete Setup Guide

### 📋 Prerequisites
- Python 3.7 or higher installed on your system
- Basic command line knowledge

### 🔧 Step 1: Create Project Directory
```bash
# Create your project folder
mkdir farming-chatbot
cd farming-chatbot
```

### 🐍 Step 2: Set Up Virtual Environment

#### On Windows (Command Prompt):
```bash
# Create virtual environment
python -m venv chatbot-env

# Activate virtual environment
chatbot-env\Scripts\activate.bat

# You should see (chatbot-env) in your prompt
```

#### On Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv chatbot-env

# Activate virtual environment (if execution policy allows)
chatbot-env\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### On Mac/Linux:
```bash
# Create virtual environment
python3 -m venv chatbot-env

# Activate virtual environment
source chatbot-env/bin/activate

# You should see (chatbot-env) in your prompt
```

### 📦 Step 3: Install Required Libraries
```bash
# Make sure your virtual environment is activated
# You should see (chatbot-env) in your prompt

# Install from requirements.txt
pip install -r requirements.txt

# OR install individually:
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.0 python-multipart==0.0.6
```

### 📁 Step 4: Create Project Structure
```bash
# Create the static folder for frontend files
mkdir static

# Your structure should look like:
# farming-chatbot/
# ├── chatbot-env/          (virtual environment)
# ├── main.py              (backend server)
# ├── requirements.txt     (dependencies)
# ├── crop_data.json       (your crop data - optional)
# ├── static/
# │   └── index.html       (frontend interface)
# └── README.md           (this file)
```

### 📝 Step 5: Add Your Files
1. Save the FastAPI backend code as `main.py`
2. Save the HTML interface code as `static/index.html`
3. (Optional) Add your crop data as `crop_data.json`

### 🚀 Step 6: Run the Application
```bash
# Make sure virtual environment is activated
# Run the server
python main.py
```

**You should see output like:**
```
🌱 Starting Farming Chatbot Server...
📱 Open http://localhost:8000 in your browser
📋 API docs available at http://localhost:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 🌐 Step 7: Access Your Chatbot
- **Main Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### ⏹️ Step 8: Stop the Server
- Press `Ctrl+C` in the terminal to stop the server
- Type `deactivate` to exit the virtual environment

## 🔄 Daily Usage

### Starting the Chatbot:
```bash
# Navigate to project folder
cd farming-chatbot

# Activate virtual environment
# Windows Command Prompt:
chatbot-env\Scripts\activate.bat
# Mac/Linux:
source chatbot-env/bin/activate

# Run the server
python main.py
```

### Stopping the Chatbot:
```bash
# Stop server: Ctrl+C
# Deactivate environment: 
deactivate
```

## 🔧 Integrating Your Existing Chatbot Logic

The current backend includes sample crop data and logic. To integrate your existing Python chatbot:

### Option 1: Replace the FarmingChatbot Class
Replace the `FarmingChatbot` class in `main.py` with your existing chatbot logic:

```python
# Import your existing chatbot
from your_chatbot_module import YourChatbotClass

# Replace the FarmingChatbot initialization
chatbot = YourChatbotClass()

# Update the chat endpoint to use your chatbot's method
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    try:
        # Use your existing chatbot's method
        bot_response = chatbot.your_existing_method(message.message)
        
        # Format response to match ChatResponse model
        return ChatResponse(
            response=bot_response,
            crop_type=message.crop_type,
            suggestions=[]  # Add suggestions if your chatbot provides them
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

### Option 2: Load Your JSON Data
If you have a JSON file with crop data, replace the `CROP_DATA` dictionary:

```python
import json

# Load your JSON file
def load_crop_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Replace CROP_DATA with your data
CROP_DATA = load_crop_data('your_crop_data.json')
```

### Option 3: Modify the Process Message Method
Update the `process_message` method to match your chatbot's logic:

```python
def process_message(self, message: str, crop_type: str = None) -> ChatResponse:
    # Your existing chatbot logic here
    bot_response = your_existing_logic(message)
    
    return ChatResponse(
        response=bot_response,
        crop_type=crop_type,
        suggestions=get_suggestions_for_message(message)  # Optional
    )
```

## 🎨 Frontend Customization

### Changing Colors and Styling
Edit the CSS in `static/index.html`:

```css
/* Main theme colors */
:root {
    --primary-color: #4CAF50;      /* Green theme */
    --secondary-color: #667eea;     /* Purple accent */
    --background: #f8f9fa;          /* Light background */
    --text-color: #333;             /* Text color */
}
```

### Adding New Features
The frontend JavaScript class `FarmingChatbot` can be extended:

```javascript
// Add new methods to the FarmingChatbot class
addCustomFeature() {
    // Your custom functionality
}

// Modify the sendToBackend method for custom API calls
async sendToBackend(message) {
    // Add custom headers or modify the request
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Custom-Header': 'your-value'  // Add custom headers
        },
        body: JSON.stringify({ 
            message: message,
            additional_data: 'value'  // Add extra data
        })
    });
    return await response.json();
}
```

## 📱 Features

### ✅ Current Features
- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Instant message exchange
- **Typing Indicators**: Shows when bot is thinking
- **Message Suggestions**: Clickable suggestion chips
- **Auto-scroll**: Automatically scrolls to new messages
- **Message Timestamps**: Shows when messages were sent
- **Clean UI**: Modern chat bubble interface
- **Error Handling**: Graceful error management

### 🔧 Backend Features
- **FastAPI Framework**: High-performance async API
- **CORS Support**: Cross-origin resource sharing enabled
- **Data Validation**: Pydantic models for request/response
- **Health Checks**: Monitoring endpoint
- **Static File Serving**: Serves frontend files
- **Comprehensive Logging**: Built-in logging support

## 🌾 Sample Crop Data Structure

Your JSON file should follow this structure:

```json
{
  "crop_name": {
    "planting_season": "Season information",
    "watering": "Watering guidelines",
    "fertilizer": "Fertilizer recommendations",
    "harvest": "Harvest timing",
    "common_issues": ["Issue 1", "Issue 2"],
    "tips": ["Tip 1", "Tip 2", "Tip 3"]
  }
}
```

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve frontend interface |
| `/api/chat` | POST | Process chat messages |
| `/api/crops` | GET | Get available crops list |
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |

## 🛠️ Development

### Adding New API Endpoints
```python
@app.get("/api/custom-endpoint")
async def custom_endpoint():
    return {"message": "Custom response"}
```

### Environment Variables
Create a `.env` file for configuration:
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CROP_DATA_FILE=crop_data.json
```

### Testing
Test the API endpoints:
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me about wheat"}'
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t farming-chatbot .
docker run -p 8000:8000 farming-chatbot
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

**2. Module Not Found**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

**3. CORS Issues**
- Ensure CORS middleware is properly configured in `main.py`
- Check browser console for error messages

**4. Frontend Not Loading**
- Verify `static/index.html` exists
- Check file permissions
- Ensure FastAPI static file mounting is correct

### Debug Mode
Enable debug logging in `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Tips

1. **Caching**: Implement response caching for common queries
2. **Database**: Consider using a database for larger datasets
3. **Async Processing**: Use async/await for I/O operations
4. **Rate Limiting**: Add rate limiting for production use
5. **Compression**: Enable gzip compression for responses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this code for your projects!

---

**Need Help?** Check the FastAPI documentation at https://fastapi.tiangolo.com/ for more advanced features.