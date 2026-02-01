# Margarita MCP

An MCP service for Margarita prompts.

Connect your margarita prompt templates to your AI agents with this simple MCP service.

## Installation

```bash
docker compose up -d
```

This will start the MCP service on `http://localhost:8000`.

and attach ./prompts as the template directory.

You can connect your AI agents to this endpoint to fetch rendered prompts based on your Margarita templates.

## Connecting your AI Agents

Configure your AI agent to use the MCP service endpoint:

```json


