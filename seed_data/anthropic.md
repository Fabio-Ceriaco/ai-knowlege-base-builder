# Claude SDK for Python

The Claude SDK for Python provides access to the Claude API from Python applications, enabling developers to integrate Claude's powerful language model capabilities into their software. The SDK supports both synchronous and asynchronous operations, streaming responses, tool use (function calling), structured outputs, vision capabilities, and extended thinking features. It also provides specialized clients for AWS Bedrock, Google Vertex AI, and Azure Foundry deployments.

This SDK is designed for building conversational AI applications, content generation systems, code assistants, and any application requiring advanced language model capabilities. It offers a clean, type-safe interface with comprehensive error handling, automatic retries, and helpers for common patterns like message streaming and tool execution loops.

## Creating Messages

The core API for generating text responses from Claude. Send a list of messages and receive a response with the model's reply.

```python
from anthropic import Anthropic

client = Anthropic()

# Simple message
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
print(message.content[0].text)

# Multi-turn conversation
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "What's the population there?"}
    ]
)
print(response.content[0].text)
# Output: Message with information about Paris's population
```

## Async Messages

Asynchronous version of the messages API for non-blocking operations in async applications.

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def main():
    message = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Explain quantum computing in one paragraph."}
        ]
    )
    print(message.content[0].text)
    print(f"Tokens used: {message.usage.input_tokens} in, {message.usage.output_tokens} out")

asyncio.run(main())
```

## Streaming Responses

Stream responses token-by-token for real-time output display and better user experience.

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def main():
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Write a haiku about programming."}]
    ) as stream:
        # Stream text as it arrives
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

    # Get the complete message after streaming
    final_message = await stream.get_final_message()
    print(f"\nTotal output tokens: {final_message.usage.output_tokens}")

asyncio.run(main())
```

## Streaming with Events

Access detailed streaming events including content blocks, deltas, and metadata.

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def main():
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Count from 1 to 5."}]
    ) as stream:
        async for event in stream:
            if event.type == "text":
                print(f"Text delta: {event.text}")
                print(f"Accumulated: {event.snapshot}")
            elif event.type == "message_stop":
                print(f"Final message: {event.message}")
            elif event.type == "content_block_stop":
                print(f"Content block complete: {event.content_block}")

asyncio.run(main())
```

## Tool Use (Function Calling)

Enable Claude to use tools/functions to perform actions or retrieve information.

```python
from anthropic import Anthropic
from anthropic.types import ToolParam, MessageParam

client = Anthropic()

# Define available tools
tools: list[ToolParam] = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a specific location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g., San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]

# Initial request
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}]
)

# Check if Claude wants to use a tool
if message.stop_reason == "tool_use":
    tool_use = next(block for block in message.content if block.type == "tool_use")
    print(f"Tool called: {tool_use.name}")
    print(f"Arguments: {tool_use.input}")

    # Provide tool result and get final response
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in San Francisco?"},
            {"role": "assistant", "content": message.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": "Sunny, 72°F (22°C), light breeze"
                }]
            }
        ]
    )
    print(response.content[0].text)
```

## Tool Runner Helper

Automatically execute tools in a loop until Claude completes the task.

```python
import json
from anthropic import Anthropic, beta_tool

client = Anthropic()

@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get weather for a location.

    Args:
        location: City and state, e.g., San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'

    Returns:
        JSON string with weather data
    """
    # Simulated weather API response
    return json.dumps({
        "location": location,
        "temperature": "72°F" if unit == "fahrenheit" else "22°C",
        "condition": "Sunny"
    })

@beta_tool
def get_time(timezone: str) -> str:
    """Get current time in a timezone.

    Args:
        timezone: Timezone name, e.g., 'America/Los_Angeles'

    Returns:
        Current time string
    """
    return "2:30 PM PST"

# Tool runner automatically handles the tool call loop
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[get_weather, get_time],
    messages=[{"role": "user", "content": "What's the weather and time in San Francisco?"}]
)

for message in runner:
    print(f"Stop reason: {message.stop_reason}")
    for block in message.content:
        if block.type == "text":
            print(f"Response: {block.text}")
```

## Structured Outputs

Parse Claude's responses directly into Pydantic models for type-safe structured data.

```python
import pydantic
from anthropic import Anthropic

class CalendarEvent(pydantic.BaseModel):
    title: str
    date: str
    time: str
    attendees: list[str]
    location: str | None = None

client = Anthropic()

parsed_message = client.messages.parse(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    output_format=CalendarEvent,
    messages=[{
        "role": "user",
        "content": "Extract event details: Team meeting tomorrow at 3pm with Alice, Bob, and Carol in Conference Room A"
    }]
)

event = parsed_message.parsed_output
print(f"Title: {event.title}")
print(f"Date: {event.date}")
print(f"Time: {event.time}")
print(f"Attendees: {', '.join(event.attendees)}")
print(f"Location: {event.location}")
# Output: Structured CalendarEvent object with extracted data
```

## Vision - Image Analysis

Send images to Claude for analysis, description, or visual question answering.

```python
import base64
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()

# From base64 encoded image
image_data = base64.standard_b64encode(Path("image.png").read_bytes()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": "Describe what you see in this image."
            }
        ]
    }]
)
print(message.content[0].text)

# From URL
url_message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://example.com/image.jpg"
                }
            },
            {"type": "text", "text": "What objects are in this image?"}
        ]
    }]
)
print(url_message.content[0].text)
```

## Extended Thinking

Enable Claude's extended thinking mode for complex reasoning tasks.

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Tokens allocated for thinking
    },
    messages=[{
        "role": "user",
        "content": "Solve this step by step: If a train leaves Chicago at 9am traveling 60mph, and another leaves New York at 10am traveling 80mph toward Chicago (800 miles apart), when and where do they meet?"
    }]
)

for block in response.content:
    if block.type == "thinking":
        print("=== Claude's Thinking ===")
        print(block.thinking)
        print()
    elif block.type == "text":
        print("=== Final Answer ===")
        print(block.text)
```

## Web Search Tool

Enable Claude to search the web for current information.

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[{
        "type": "web_search_20250305",
        "name": "web_search"
    }],
    messages=[{"role": "user", "content": "What are today's top tech news headlines?"}]
)

for block in message.content:
    if block.type == "text":
        print(block.text)

# Check web search usage
if message.usage.server_tool_use:
    print(f"Web searches performed: {message.usage.server_tool_use.web_search_requests}")
```

## Count Tokens

Count tokens for a message before sending to estimate costs and manage context.

```python
from anthropic import Anthropic

client = Anthropic()

# Count tokens for a potential request
token_count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
        {"role": "user", "content": "Can you explain quantum entanglement?"}
    ],
    system="You are a helpful physics tutor."
)

print(f"Input tokens: {token_count.input_tokens}")
# Use this to estimate if you're within context limits before making the actual call
```

## Message Batches

Process multiple messages asynchronously in batches for bulk operations.

```python
from anthropic import Anthropic

client = Anthropic()

# Create a batch of requests
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Summarize photosynthesis."}]
            }
        },
        {
            "custom_id": "request-2",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Explain gravity."}]
            }
        }
    ]
)
print(f"Batch ID: {batch.id}")
print(f"Status: {batch.processing_status}")

# Check batch status
batch_status = client.messages.batches.retrieve(batch.id)
print(f"Processing status: {batch_status.processing_status}")
print(f"Requests: {batch_status.request_counts}")

# Get results when complete
if batch_status.processing_status == "ended":
    for result in client.messages.batches.results(batch.id):
        print(f"ID: {result.custom_id}")
        if result.result.type == "succeeded":
            print(f"Response: {result.result.message.content[0].text}")

# List all batches
for batch in client.messages.batches.list():
    print(f"{batch.id}: {batch.processing_status}")

# Cancel a batch
cancelled = client.messages.batches.cancel(batch.id)
print(f"Cancelled: {cancelled.processing_status}")
```

## AWS Bedrock Integration

Use Claude through AWS Bedrock with AWS credentials.

```python
from anthropic import AnthropicBedrock

# Uses AWS credentials from environment or AWS config
client = AnthropicBedrock(
    aws_region="us-east-1",  # Optional, can be inferred
)

# Standard message creation
message = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from Bedrock!"}]
)
print(message.content[0].text)

# Streaming with Bedrock
with client.messages.stream(
    model="anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a short story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()
```

## Google Vertex AI Integration

Use Claude through Google Cloud's Vertex AI.

```python
import asyncio
from anthropic import AnthropicVertex, AsyncAnthropicVertex

# Synchronous client
client = AnthropicVertex(
    project_id="your-gcp-project",
    region="us-east5"
)

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from Vertex AI!"}]
)
print(message.content[0].text)

# Asynchronous client
async def async_vertex():
    async_client = AsyncAnthropicVertex(
        project_id="your-gcp-project",
        region="us-east5"
    )

    message = await async_client.messages.create(
        model="claude-sonnet-4@20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Async hello from Vertex!"}]
    )
    return message.content[0].text

result = asyncio.run(async_vertex())
print(result)
```

## Azure Foundry Integration

Use Claude through Azure AI Foundry.

```python
from anthropic import AnthropicFoundry

client = AnthropicFoundry(
    resource="your-azure-resource-name",
    api_key="your-azure-api-key"
)

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from Azure!"}]
)
print(message.content[0].text)
```

## MCP (Model Context Protocol) Integration

Integrate with MCP servers for extended tool capabilities.

```python
import asyncio
from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool, mcp_message, mcp_resource_to_content
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

client = AsyncAnthropic()

async def main():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_client:
            await mcp_client.initialize()

            # Get and convert MCP tools
            tools_result = await mcp_client.list_tools()
            tools = [async_mcp_tool(t, mcp_client) for t in tools_result.tools]

            # Use tools with tool_runner
            runner = client.beta.messages.tool_runner(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                tools=tools,
                messages=[{"role": "user", "content": "List files in /tmp"}]
            )

            async for message in runner:
                for block in message.content:
                    if block.type == "text":
                        print(block.text)

# Requires: pip install anthropic[mcp]
# asyncio.run(main())
```

## Auto-Compaction for Long Conversations

Automatically manage context length in long-running tool loops.

```python
import json
from anthropic import Anthropic
from anthropic.lib.tools import beta_tool

client = Anthropic()

@beta_tool
def search(query: str) -> str:
    """Search for information."""
    return json.dumps({"results": [f"Result for {query}"] * 10})

@beta_tool
def done(summary: str) -> str:
    """Call when finished."""
    return "Complete"

runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[search, done],
    messages=[{
        "role": "user",
        "content": "Search for: cats, dogs, birds, fish. Then call done."
    }],
    compaction_control={
        "enabled": True,
        "context_token_threshold": 5000  # Compact when context exceeds this
    }
)

for message in runner:
    print(f"Input tokens: {message.usage.input_tokens}")
    if message.stop_reason == "end_turn":
        print("Task complete!")
```

## Error Handling

Handle API errors gracefully with specific exception types.

```python
from anthropic import (
    Anthropic,
    APIError,
    APIConnectionError,
    RateLimitError,
    APIStatusError,
    AuthenticationError,
    BadRequestError,
)

client = Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(message.content[0].text)

except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Check your API key

except RateLimitError as e:
    print(f"Rate limited: {e.message}")
    # Implement backoff/retry logic

except BadRequestError as e:
    print(f"Bad request: {e.message}")
    # Check your request parameters

except APIConnectionError as e:
    print(f"Connection error: {e.message}")
    # Network issues, retry later

except APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
    # Handle other API errors

except APIError as e:
    print(f"Unexpected API error: {e}")
    # Catch-all for API errors
```

## Custom HTTP Client Configuration

Configure timeouts, retries, and HTTP client settings.

```python
import httpx
from anthropic import Anthropic, DefaultHttpxClient

# Custom timeout
client = Anthropic(
    timeout=60.0,  # 60 second timeout
    max_retries=3  # Retry failed requests 3 times
)

# Custom httpx client for advanced configuration
custom_http_client = DefaultHttpxClient(
    proxy="http://proxy.example.com:8080",
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
)

client_with_proxy = Anthropic(
    http_client=custom_http_client
)

# Per-request timeout override
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Quick question!"}],
    timeout=10.0  # Override timeout for this request only
)
```

## List Available Models

Retrieve information about available Claude models.

```python
from anthropic import Anthropic

client = Anthropic()

# List all available models
for model in client.models.list():
    print(f"Model: {model.id}")
    print(f"  Display name: {model.display_name}")
    print(f"  Created: {model.created_at}")
    print()

# Get specific model info
model_info = client.models.retrieve("claude-sonnet-4-5-20250929")
print(f"Model ID: {model_info.id}")
print(f"Type: {model_info.type}")
```

## Beta Files API

Upload and manage files for use with Claude.

```python
from anthropic import Anthropic

client = Anthropic()

# Upload a file
with open("document.pdf", "rb") as f:
    uploaded = client.beta.files.upload(file=f)
print(f"File ID: {uploaded.id}")
print(f"Filename: {uploaded.filename}")

# List files
for file in client.beta.files.list():
    print(f"{file.id}: {file.filename} ({file.size} bytes)")

# Get file metadata
metadata = client.beta.files.retrieve_metadata(uploaded.id)
print(f"File type: {metadata.mime_type}")

# Download file content
content = client.beta.files.download(uploaded.id)
with open("downloaded.pdf", "wb") as f:
    f.write(content.content)

# Delete file
deleted = client.beta.files.delete(uploaded.id)
print(f"Deleted: {deleted.id}")
```

## Summary

The Claude SDK for Python is designed for building sophisticated AI-powered applications. Primary use cases include conversational AI assistants, automated content generation, code analysis and generation, document processing and summarization, visual content understanding, and complex reasoning tasks requiring extended thinking. The SDK's tool use capabilities enable building agents that can interact with external systems, APIs, and databases while maintaining natural conversation flow.

Integration patterns typically involve initializing a client with API credentials (or using environment variables), creating message requests with appropriate parameters, handling responses including streaming for real-time applications, and implementing tool loops for agentic workflows. For production deployments, the SDK offers robust error handling, automatic retries, configurable timeouts, and support for cloud provider integrations through Bedrock, Vertex AI, and Azure Foundry. The structured outputs feature and Pydantic integration make it easy to build type-safe applications that reliably extract structured data from Claude's responses.
