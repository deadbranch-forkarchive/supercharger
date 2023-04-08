# Use modules from parent folder
import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import logging

from server.client import ask_server
from prompts.ask_templates import ask_python_pytest_prototype, ask_python_function_prototype, ask_python_analyzer, ask_python_test_analyzer
from clean_code import clean_code

def autopy_func(comments, prototype, node="localhost", port=5000, temperature=1.0, max_tokens=1024):
    #logging.info(f"autopy_func: comments = `{comments}`")
    #logging.info(f"autopy_func: prototype = `{prototype}`")

    prompt, stop_strs = ask_python_function_prototype(comments, prototype)

    #logging.info(f"autopy_func: prompt = \n{prompt}")
    #logging.info(f"autopy_func: stop_strs = {stop_strs}")

    result = ask_server(prompt, stop_strs, node, port, temperature, max_tokens)

    #logging.info(f"autopy_func: result = \n{result}")

    code, _ = clean_code(result, strip_leading_comments=True)

    #logging.info(f"autopy_func: code = \n{code}")

    if len(code) > 0:
        # Prepend the comments
        code = '\n'.join(comments.splitlines() + code.splitlines())

    return code

def autopy_func_improve(comments, code, node="localhost", port=5000, temperature=1.0, max_tokens=1024):
    #logging.info(f"autopy_func_analyze: comments_and_code = `{comments_and_code}`")

    prompt, stop_strs = ask_python_analyzer(code)

    #logging.info(f"autopy_func_analyze: prompt = \n{prompt}")
    #logging.info(f"autopy_func_analyze: stop_strs = {stop_strs}")

    result = ask_server(prompt, stop_strs, node, port, temperature, max_tokens)

    #logging.info(f"autopy_func_analyze: result = \n{result}")

    code, _ = clean_code(result, strip_leading_comments=True)

    #logging.info(f"autopy_func_analyze: code = \n{code}")

    if len(code) > 0:
        # Prepend the comments
        code = '\n'.join(comments.splitlines() + code.splitlines())

    return code

def autopy_test(comments, prototype, node="localhost", port=5000, temperature=1.0, max_tokens=1024):
    #logging.debug(f"autopy_test: comments = `{comments}`")
    #logging.debug(f"autopy_test: prototype = `{prototype}`")

    prompt, stop_strs = ask_python_pytest_prototype(comments, prototype)

    #logging.info(f"autopy_test: prompt = \n{prompt}")
    #logging.info(f"autopy_test: stop_strs = {stop_strs}")

    result = ask_server(prompt, stop_strs, node, port, temperature, max_tokens)

    #logging.info(f"autopy_test: result = \n{result}")

    code, _ = clean_code(result, strip_globals=False)

    #logging.debug(f"autopy_test: code = \n{code}")

    return code

def autopy_test_improve(comments, prototype, function_name, test_code, node="localhost", port=5000, temperature=1.0, max_tokens=1024):
    #logging.info(f"autopy_test_analyze: comments_and_code = `{comments_and_code}`")

    prompt, stop_strs = ask_python_test_analyzer(comments, prototype, function_name, test_code)

    #logging.info(f"autopy_test_analyze: prompt = \n{prompt}")
    #logging.info(f"autopy_test_analyze: stop_strs = {stop_strs}")

    result = ask_server(prompt, stop_strs, node, port, temperature, max_tokens)

    #logging.info(f"autopy_test_analyze: result = \n{result}")

    code, _ = clean_code(result, strip_globals=False)

    #logging.info(f"autopy_test_analyze: code = \n{code}")

    return code