# PEOPLEWORKS - AI-Powered Performance Review System

An intelligent system that automates the feedback pipeline -- end-to-end.

We offer:
- A system to manage and view the growth of your group.
- An agent-driven system to automatically conduct feedback interviews.
- An agent-driven flow to convert unstructured interview transcripts to intuitive graphs and visualizations.

## Screenshots

[Add screenshots of the application interface here]

## Project Structure

```
hackfleisch/
├── src/
│   ├── interview_agent/     # Interview agent implementation
│   ├── external_agents/     # External agent integrations
│   └── ...
├── data/                    # Data storage
├── memory/                  # Memory management
├── booscript/              # Scripts and utilities
└── Transcript/             # Interview transcripts
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- ElevenLabs API key

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd hackfleisch
```

2. Install Python dependencies:
```bash
conda create -n cdtmhack python=3.8
conda activate cdtmhack
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install @fastify/formbody @fastify/websocket dotenv fastify ws twilio
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
ELEVENLABS_API_KEY=your_api_key_here
```

## Running the Application

### 1. Start the ElevenLabs Node.js Server

```bash
node booscript/elevenlabs_server.js
```

### 2. Start the Main Application

```bash
uvicorn main:app --reload
```

## Usage

1. The system can be used to conduct automated interviews and feedback sessions
2. Interviews are processed and stored in the database
3. Feedback analysis tools are available for competency assessment

## Features

- AI-powered interview conduction
- Voice synthesis using ElevenLabs
- Real-time interview processing
- Competency assessment and feedback analysis
- Database integration for storing interview data

## Contributing

[Add contribution guidelines here]

## License

[Add license information here]
