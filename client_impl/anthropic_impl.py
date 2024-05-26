import time

import llm_client_base

# pip install anthropic
import anthropic

# config from .env
# ANTHROPIC_API_KEY
# HTTP_PROXY
# HTTPS_PROXY


import os

# os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890/"
# os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890/"


class Anthropic_Client(llm_client_base.LlmClientBase):
    def __init__(self):
        super().__init__()

        api_key = os.getenv('ANTHROPIC_API_KEY')
        assert api_key is not None

        self.client = anthropic.AsyncAnthropic(
            api_key=api_key
        )

    async def chat_stream_async(self, model_name, history, temperature, force_calc_token_num):
        current_message = None
        start_time = time.time()
        first_token_time = None
        async with self.client.messages.stream(
                model=model_name,
                messages=history,
                temperature=temperature,
                max_tokens=1024 * 3,  # 必选项
        ) as stream:
            async for delta in stream.__stream_text__():
                current_message = stream.current_message_snapshot
                if delta and first_token_time is None:
                    first_token_time = time.time()
                yield {
                    'role': current_message.role,
                    'delta_content': delta,
                    'accumulated_content': current_message.content[0].text,
                }

        completion_time = time.time()

        usage = {
            'prompt_tokens': current_message.usage.input_tokens,
            'completion_tokens': current_message.usage.output_tokens,
        }
        yield {
            'role': current_message.role,
            'accumulated_content': current_message.content[0].text,
            'finish_reason': current_message.stop_reason,
            'usage': usage,
            'first_token_time': first_token_time - start_time,
            'completion_time': completion_time - start_time,
        }

    async def close(self):
        await self.client.close()

if __name__ == '__main__':
    import asyncio
    import os

    client = Anthropic_Client()
    model_name = "claude-3-haiku-20240307"
    history = [{"role": "user", "content": "Hello, how are you?"}]
    temperature = 0.01

    async def main():
        async for chunk in client.chat_stream_async(model_name, history, temperature, force_calc_token_num=True):
            print(chunk)

    asyncio.run(main())
