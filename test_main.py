import asyncio
import time

from client_impl.openai_impl import OpenAI_Client
from client_impl.google_impl import Gemini_Client
from client_impl.anthropic_impl import Anthropic_Client
from client_impl.reka_impl import Reka_Client
from client_impl.mistral_impl import Mistral_Client

from client_impl.zhipu_impl import Zhipu_Client
from client_impl.yi_impl import Yi_Client
from client_impl.moonshot_impl import Moonshot_Client
from client_impl.baidu_impl import Baidu_Client
from client_impl.stepfun_impl import StepFun_Client
from client_impl.sensenova_impl import SenseNova_Client
from client_impl.baichuan_impl import Baichuan_Client
from client_impl.alibaba_impl import Alibaba_Client
from client_impl.minimax_impl import Minimax_Client
from client_impl.deepseek_impl import DeepSeek_Client
from client_impl.tencent_impl import Tencent_Client
from client_impl.bytedance_impl import ByteDance_Client

from client_impl.together_impl import Together_Client
from client_impl.siliconflow_impl import SiliconFlow_Client
from client_impl.duckagi_impl import DuckAgi_Client


async def run_test(client_factory, model_name, prompt):
    client = client_factory()
    history = [{"role": "user", "content": prompt}]
    temperature = 0.8

    model_param = {
        'temperature': temperature,
    }
    client_param = {
        'force_calc_token_num': True,
    }

    result = ''
    usage = None
    async for chunk in client.chat_stream_async(model_name, history, model_param, client_param):
        result = chunk['accumulated_content']
        if 'usage' in chunk:
            usage = chunk['usage']

        if 'delta_content' in chunk:
            print(chunk['delta_content'], end='', flush=True)
        else:
            print()

    if result == '':
        print(f'finish_reason: {chunk["finish_reason"]}')

    await client.close()

    ret = {
        'result': result,
        'usage': usage,
        'finish_reason': chunk['finish_reason'],
        'first_token_time': chunk['first_token_time'],
        'total_time': chunk['completion_time'],
    }
    if usage and 'completion_tokens' in usage and chunk['completion_time'] > chunk['first_token_time']:
        ret['token_speed'] = usage['completion_tokens'] / (chunk['completion_time'] - chunk['first_token_time'])
    return ret


def test_128k():

    gap_time = 0

    client_factory, model_name = Gemini_Client, "gemini-1.5-flash"
    # client_factory, model_name = Gemini_Client, "gemini-1.5-pro"

    # client_factory, model_name = OpenAI_Client, "gpt-4o"
    # client_factory, model_name = OpenAI_Client, "gpt-4-0125-preview"

    # client_factory, model_name, gap_time = Anthropic_Client, "claude-3-sonnet-20240229", max(60/1000, 60 / (80 / 120))  # tier2 # TPD 太低
    # client_factory, model_name, gap_time = Anthropic_Client, "claude-3-haiku-20240307", max(60/1000, 60 / (100 / 120))  # tier2 # TPD 太低
    # client_factory, model_name = DuckAgi_Client, "claude-3-haiku-20240307"
    # client_factory, model_name = DuckAgi_Client, "claude-3-sonnet-20240229"

    # client_factory, model_name, gap_time = Reka_Client, "reka-core", 60
    # client_factory, model_name, gap_time = Reka_Client, "reka-flash", 0

    # cohere
    # client_factory, model_name = DuckAgi_Client, "command-r"
    # client_factory, model_name = DuckAgi_Client, "command-r-plus"


    # client_factory, model_name, gap_time = Zhipu_Client, "glm-3-turbo", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-air", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-airx", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-flash", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-0520", 0

    # client_factory, model_name, gap_time = Yi_Client, "yi-medium-200k", max(60/10, 60 / (300 / 120))  # tier1

    # client_factory, model_name, gap_time = Moonshot_Client, "moonshot-v1-128k", max(60/200, 60 / (128 / 120) * 2)

    # client_factory, model_name, gap_time = Baichuan_Client, "Baichuan3-Turbo-128k", 60 / 120
    # client_factory, model_name, gap_time = Baichuan_Client, "Baichuan4", 60 / 120

    # client_factory, model_name, gap_time = StepFun_Client, "step-1-128k", max(60/5000, 60 / (720 / 120))  # V3
    # client_factory, model_name, gap_time = StepFun_Client, "step-1-256k", max(60/5000, 60 / (720 / 120))  # V3

    # client_factory, model_name, gap_time = Minimax_Client, "abab6.5s-chat", max(60/5000, 60 / (720 / 120))

    # client_factory, model_name = SenseNova_Client, "SenseChat-128K"  # content blocked

    # client_factory, model_name, gap_time = Baidu_Client, "ERNIE-Speed-128K", max(60/60, 60 / (300 / 120) * 2)

    # client_factory, model_name, gap_time = Tencent_Client, "hunyuan-lite", 0
    # client_factory, model_name, gap_time = Tencent_Client, "hunyuan-standard-256K", 0

    # client_factory, model_name, gap_time = SiliconFlow_Client, "deepseek-ai/deepseek-v2-chat", 10

    # client_factory, model_name, gap_time = ByteDance_Client, "ep-xxxxx", max(60/1000, 60 / (400 / 120)), # doubao-lite-128k

    # client_factory, model_name, gap_time = ByteDance_Client, "ep-xxxxx", max(60/1000, 60 / (400 / 120)), # doubao-pro-128k

    test_file_list = [
        'test_case3v2_128k_sample1.txt',
        'test_case3v2_128k_sample2.txt',
        'test_case3v2_128k_sample3.txt',

        'test_case4v2_128k_sample1.txt',
        'test_case4v2_128k_sample2.txt',
        'test_case4v2_128k_sample3.txt',
    ]

    print(f'model_name: {model_name}')
    for test_file in test_file_list:
        print(f'=================== {test_file} ===============')
        prompt = open(test_file, 'r', encoding='utf8').read()

        output_sample_num = 5
        success_num = 0
        first_token_time_list = []
        token_speed_list = []
        prompt_token = None
        for i in range(output_sample_num):
            print(f'-------------- {test_file} {i}--------------')
            start_time = time.time()
            result = asyncio.run(run_test(client_factory, model_name, prompt))
            print('-------------------------------')

            if 'prompt_tokens' in result['usage']:
                prompt_token = result['usage']['prompt_tokens']

            success = '1350' in result['result']
            if success:
                success_num += 1

            print(f'usage: {result["usage"]}')
            if 'rate_limit_info' in result:
                print(f'rate_limit_info: {result["rate_limit_info"]}')
            print(f'first token time: {result["first_token_time"]}')
            first_token_time_list.append(result["first_token_time"])
            if 'token_speed' in result:
                print(f'token speed: {result["token_speed"]}')
                token_speed_list.append(result["token_speed"])

            if gap_time > 0:
                sleep_time = max(3, gap_time - (time.time() - start_time))
                time.sleep(sleep_time)

        print(f'===================STAT {test_file} ===============')
        print(f'prompt token: {prompt_token}')
        print(f'success rate: {success_num}/{output_sample_num}')

        stat_first_token_time_list = sorted(first_token_time_list)[:-1]
        avg_first_token_time = sum(stat_first_token_time_list) / len(stat_first_token_time_list)
        print(f'avg_first_token_time: {avg_first_token_time}, {first_token_time_list}')

        if token_speed_list:
            stat_token_speed_list = sorted(token_speed_list)[1:]
            avg_token_speed = sum(stat_token_speed_list) / len(stat_token_speed_list)
            print(f'avg_token_speed: {avg_token_speed}, {token_speed_list}')


def test_32k():
    gap_time = 0

    client_factory, model_name = Gemini_Client, "gemini-1.5-flash"
    # client_factory, model_name = Gemini_Client, "gemini-1.5-pro"

    # client_factory, model_name = OpenAI_Client, "gpt-4o"

    # client_factory, model_name, gap_time = Anthropic_Client, "claude-3-haiku-20240307", max(60/1000, 60 / (100 / 30))  # tier2
    # client_factory, model_name, gap_time = Anthropic_Client, "claude-3-sonnet-20240229", max(60/1000, 60 / (80 / 30))  # tier2

    # client_factory, model_name, gap_time = Reka_Client, "reka-core", 0
    # client_factory, model_name, gap_time = Reka_Client, "reka-flash", 0

    client_factory, model_name, gap_time = Mistral_Client, "mistral-small-latest", 0
    # client_factory, model_name, gap_time = Mistral_Client, "mistral-medium-latest", 0
    # client_factory, model_name, gap_time = Mistral_Client, "mistral-large-latest", 0
    # client_factory, model_name, gap_time = Mistral_Client, "open-mixtral-8x22b", 0
    # client_factory, model_name, gap_time = Mistral_Client, "open-mixtral-8x7b", 0
    # client_factory, model_name, gap_time = Mistral_Client, "open-mistral-7b", 0

    # cohere
    # client_factory, model_name, gap_time = DuckAgi_Client, "command-r", 60
    # client_factory, model_name, gap_time = DuckAgi_Client, "command-r-plus", 60


    # client_factory, model_name, gap_time = Zhipu_Client, "glm-3-turbo", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-air", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-flash", 0
    # client_factory, model_name, gap_time = Zhipu_Client, "glm-4-0520", 0

    # client_factory, model_name, gap_time = Yi_Client, "yi-medium-200k", max(60/10, 60 / (300 / 30))  # tier1
    # client_factory, model_name, gap_time = Yi_Client, "yi-large", max(60/10, 60 / (80 / 30))  # tier1

    # client_factory, model_name, gap_time = Moonshot_Client, "moonshot-v1-32k", max(60/200, 60 / (128 / 30) * 2)

    # client_factory, model_name, gap_time = Baichuan_Client, "Baichuan3-Turbo-128k", 60 / 120
    # client_factory, model_name, gap_time = Baichuan_Client, "Baichuan3-Turbo", 60 / 120
    # client_factory, model_name, gap_time = Baichuan_Client, "Baichuan4", 60 / 120

    # client_factory, model_name, gap_time = StepFun_Client, "step-1-32k", max(60/5000, 60 / (720 / 30))  # V3

    # client_factory, model_name, gap_time = Minimax_Client, "abab6.5s-chat", max(60/5000, 60 / (720 / 30))
    # client_factory, model_name, gap_time = Minimax_Client, "abab6-chat", max(60/5000, 60 / (720 / 30))

    # client_factory, model_name = DeepSeek_Client, "deepseek-chat"

    # client_factory, model_name = SenseNova_Client, "SenseChat-32K"  # content blocked
    # client_factory, model_name = SenseNova_Client, "SenseChat-128K"  # content blocked

    # client_factory, model_name, gap_time = Baidu_Client, "ERNIE-Speed-128K", 60
    # client_factory, model_name, gap_time = Baidu_Client, "ERNIE-3.5-128K", 60

    # client_factory, model_name = Alibaba_Client, "qwen-plus"
    # client_factory, model_name = Alibaba_Client, "qwen-max-longcontext"

    # client_factory, model_name, gap_time = Tencent_Client, "hunyuan-lite", 0
    # client_factory, model_name, gap_time = Tencent_Client, "hunyuan-standard", 0
    # client_factory, model_name, gap_time = Tencent_Client, "hunyuan-pro", 0

    # client_factory, model_name, gap_time = Together_Client, "Qwen/Qwen1.5-72B-Chat", 60
    # client_factory, model_name, gap_time = Together_Client, "Qwen/Qwen1.5-110B-Chat", 60
    # client_factory, model_name, gap_time = Together_Client, "Qwen/Qwen1.5-32B-Chat", 60
    # client_factory, model_name, gap_time = Together_Client, "Qwen/Qwen1.5-14B-Chat", 60

    # client_factory, model_name, gap_time = SiliconFlow_Client, "deepseek-ai/deepseek-v2-chat", 10

    # client_factory, model_name, gap_time = ByteDance_Client, "ep-xxxxx", max(60/1000, 60 / (800 / 120)), # doubao-pro-32k
    # client_factory, model_name, gap_time = ByteDance_Client, "ep-xxxxx", max(60/1000, 60 / (800 / 120)), # doubao-lite-32k

    # client_factory, model_name, gap_time = SiliconFlow_Client, "zhipuai/chatglm3-6B", 0
    # client_factory, model_name, gap_time = SiliconFlow_Client, "zhipuai/glm4-9B-chat", 0

    # client_factory, model_name, gap_time = SiliconFlow_Client, "alibaba/Qwen1.5-110B-Chat", 0

    # client_factory, model_name, gap_time = SiliconFlow_Client, "alibaba/Qwen2-72B-Instruct", 0
    # client_factory, model_name, gap_time = SiliconFlow_Client, "alibaba/Qwen2-57B-A14B-Instruct", 0
    # client_factory, model_name, gap_time = SiliconFlow_Client, "alibaba/Qwen2-7B-Instruct", 0

    test_file_list = [
        'test_case3v2_32k_sample1.txt',
        'test_case3v2_32k_sample2.txt',
        'test_case3v2_32k_sample3.txt',

        'test_case4v2_32k_sample1.txt',
        'test_case4v2_32k_sample2.txt',
        'test_case4v2_32k_sample3.txt',
    ]

    print(f'model_name: {model_name}')
    for test_file in test_file_list:
        print(f'=================== {test_file} ===============')
        prompt = open(test_file, 'r', encoding='utf8').read()

        output_sample_num = 5
        success_num = 0
        first_token_time_list = []
        token_speed_list = []
        prompt_token = None
        for i in range(output_sample_num):
            print(f'-------------- {test_file} {i}--------------')
            start_time = time.time()
            result = asyncio.run(run_test(client_factory, model_name, prompt))
            print('-------------------------------')

            if 'prompt_tokens' in result['usage']:
                prompt_token = result['usage']['prompt_tokens']

            success = '1350' in result['result']
            if success:
                success_num += 1

            print(f'usage: {result["usage"]}')
            if 'rate_limit_info' in result:
                print(f'rate_limit_info: {result["rate_limit_info"]}')
            print(f'first token time: {result["first_token_time"]}')
            first_token_time_list.append(result["first_token_time"])
            if 'token_speed' in result:
                print(f'token speed: {result["token_speed"]}')
                token_speed_list.append(result["token_speed"])

            if gap_time > 0:
                sleep_time = max(3, gap_time - (time.time() - start_time))
                time.sleep(sleep_time)

        print(f'===================STAT {test_file} ===============')
        print(f'prompt token: {prompt_token}')
        print(f'success rate: {success_num}/{output_sample_num}')

        stat_first_token_time_list = sorted(first_token_time_list)[:-1]
        avg_first_token_time = sum(stat_first_token_time_list) / len(stat_first_token_time_list)
        print(f'avg_first_token_time: {avg_first_token_time}, {first_token_time_list}')

        if token_speed_list:
            stat_token_speed_list = sorted(token_speed_list)[1:]
            avg_token_speed = sum(stat_token_speed_list) / len(stat_token_speed_list)
            print(f'avg_token_speed: {avg_token_speed}, {token_speed_list}')


if __name__ == '__main__':
    import os
    # os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890/"
    # os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890/"

    # test_128k()

    test_32k()
