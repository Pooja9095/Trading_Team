# Trading Team Crew - AI Agents for a Simulated Trading Platform
Welcome to the Trading Team Crew project! This project was built using CrewAI, a multi-agent framework where AI agents collaborate to build, test, and deliver real-world software.

This repo includes:
- Agent definitions for Engineering, Frontend, Backend, and Testing.
- Config files for reusable tasks.
- Auto-generated UI to simulate a trading platform with account management, trading actions, and reports.
- Gradio app to demo the final system.

Visit the LIVE app here: https://huggingface.co/spaces/Pooja-Nigam/Trading_Team

## Technologies Used
- Python ≥3.10 and <3.14
- CrewAI for multi-agent orchestration
- Gradio for UI
- UV package manager
- OpenAI GPT-4o-mini as the LLM backend for all agents

### Installation & Setup
Make sure you have Python and uv installed.
```bash
pip install uv
```

**Add your .env file:**
```bash
OPENAI_API_KEY=your-key-here
```

## Run the Crew
```bash
crewai run
```
This will:
- Load agents/tasks from src/trading_team/config/
- Run them sequentially to build the output/ folder
- Generate backend logic, frontend Gradio app, and (optionally) unit tests
  
## Run the final App
```bash
cd output
uv run app.py
```

- Modify `src/trading_team/config/agents.yaml` to define your agents
- Modify `src/trading_team/config/tasks.yaml` to define your tasks
- Modify `src/trading_team/crew.py` to add your own logic, tools and specific args
- Modify `src/trading_team/main.py` to add custom inputs for your agents and tasks
  
## Understanding the Crew
The Trading_Team Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in the crew.

## MIT License

Copyright (c) 2025 Pooja Nigam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.                              

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         
DEALINGS IN THE SOFTWARE.
