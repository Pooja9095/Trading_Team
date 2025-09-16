# Trading Team Crew - AI Agents for a Simulated Trading Platform

Welcome to the Trading Team Crew project! This project was built using CrewAI, a multi-agent framework where AI agents collaborate to build, test, and deliver real-world software.

This repo includes:

Agent definitions for Engineering, Frontend, Backend, and Testing.

Config files for reusable tasks.

Auto-generated UI to simulate a trading platform with account management, trading actions, and reports.

Gradio app to demo the final system.

Visit the LIVE app here: https://huggingface.co/spaces/Pooja-Nigam/Trading_Team

## Installation

#  1. Prerequisites
- Python ≥3.10 and <3.14
- UV package manager

#  2. Install UV

```bash
pip install uv
```


(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/trading_team/config/agents.yaml` to define your agents
- Modify `src/trading_team/config/tasks.yaml` to define your tasks
- Modify `src/trading_team/crew.py` to add your own logic, tools and specific args
- Modify `src/trading_team/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the Trading_Team Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The Trading_Team Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the TradingTeam Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
