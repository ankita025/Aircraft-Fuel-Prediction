## Enabling Anthropic Claude Haiku 4.5 (integration notes)

This document explains how to enable access to Claude Haiku 4.5 and a minimal integration example.

- Obtain an API key:
  - Sign in to your Anthropic account and create or copy an API key for your project.
  - Store the key securely. Locally, set an environment variable named `ANTHROPIC_API_KEY`.

- Install dependencies (locally):

  ```powershell
  pip install anthropic requests
  ```

- Set the environment variable on Windows (PowerShell):

  ```powershell
  setx ANTHROPIC_API_KEY "<YOUR_API_KEY>"
  ```

- Model name and endpoint:
  - Anthropic may publish model IDs such as `claude-haiku-4.5`. Always confirm the exact model ID and endpoint in Anthropic's official documentation or your Anthropic Console before calling.
  - This repo includes a small example (`anthropic_example.py`) that uses a safe placeholder model string — replace it with the exact model ID from Anthropic.

- Security & best practices:
  - Do not commit API keys to version control. Use environment variables or a secrets manager.
  - Monitor usage/cost in the Anthropic console and apply rate limits or quotas in your app as needed.

- How GitHub Copilot relates to Anthropic models:
  - GitHub Copilot (the editor-assistant product) uses provider-supplied models controlled by GitHub/Microsoft and is not the same as having direct API access to Anthropic's Claude models.
  - To use Claude Haiku 4.5 in your development or production workflows, call the Anthropic API from your code (examples provided) or use any third-party integrations that explicitly support Anthropic.
  - For enterprise setups, organizations sometimes combine Copilot and third-party LLM calls in backend services: Copilot helps with code/IDE suggestions while your app makes authorized API calls to Anthropic for runtime completions.

- Next steps:
  - Add your API key to the environment, run `anthropic_example.py`, confirm responses, then update the example model string to the exact Anthropic model name.

If you want, I can also add an integration helper that wraps retries, timeouts, and logging for production use.
