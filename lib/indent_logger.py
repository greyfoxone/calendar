import functools
import logging
import sys
import time
import traceback
from pprint import pformat
from pprint import pprint
from typing import Tuple
from lib.loggers import logger
from termcolor import colored

__all__ = [
    "pvars",
    "debug_log",
    "class_debug_log",
]
DECORATED_FUNCTIONS = set()


def truncate(value, max_len=200):
    s = str(value)
    if len(s) <= max_len:
        return s
    half = max_len // 2
    return s[:half] + f" ...({len(s)-max_len})... " + s[-half:]


def params(args, kwargs):
    params = ""

    def brackets(text, color="light_red"):
        return f"{colored('(',color)}{text}{colored(')',color)}"

    args_repr = ""
    for arg in args:
        arg_repr = pformat(arg, indent=2)
        args_repr += f"  {colored(truncate(arg_repr), 'yellow', attrs=['dark'])}, "
    params += truncate(args_repr)

    for key, value in kwargs.items():

        value_repr = pformat(value)
        params += (
            f"\n  {colored(f'  {key} = ', 'magenta')}"
            f"{colored(truncate(value_repr), 'yellow', attrs=['dark'])}, "
        )
    params += "\n"
    return brackets(params.rstrip(", "))


class PrettyStack:
    def __init__(self, e):
        self.e = e

    def get(self) -> str:
        stack_lines = []
        last_filname = ""

        for frame, line_no in traceback.walk_tb(self.e.__traceback__):
            filename = frame.f_code.co_filename
            func_name = frame.f_code.co_name
            class_name = ""
            if "self" in frame.f_locals:
                class_name = frame.f_locals["self"].__class__.__name__
            if "cls" in frame.f_locals:
                class_name = frame.f_locals["cls"].__name__
            if class_name:
                func_name = f"{class_name}.{func_name}"

            redacted_parts, unique_parts = self.redact_path(filename, last_filname)
            colored_path = colored(redacted_parts, "grey") + colored(
                unique_parts, "yellow", attrs=["bold"]
            )
            locals = frame.f_locals

            local_vars_str = "\nLocal Vars:\n"
            local_vars_str += params(locals.get("args", []), frame.f_locals)
            stack_line = f"{'-'*15}\n:"
            stack_line += f"{colored(func_name, 'green')}()"
            stack_line += f"({colored(line_no, 'red', attrs=['bold'])})\n"
            stack_line += local_vars_str
            stack_line += f"\n\n"
            stack_lines.append(stack_line)
            last_filname = filename

        trace = "\n".join(stack_lines)

        msg = f"\n{'-'*5}\nStacktrace:\n{trace}\n\n"
        msg += f"{'-'*5}\nError:\n"
        msg += f"{colored(str(self.e), 'red')}\n"
        #        msg += f"\nFile: {traceback.extract_tb(self.e.__traceback__)[-1].filename}, Line: {traceback.extract_tb(self.e.__traceback__)[-1].lineno}"
        msg += f"{'-'*5}\n"
        return msg

    def redact_path(self, filename: str, last_filename: str) -> Tuple[str, str]:
        common_prefix_len = len(set(filename).intersection(last_filename))
        return filename[:common_prefix_len], filename[common_prefix_len:]

    def __repr__(self):
        return self.get()

    def __str__(self):
        return self.get()


class IndentLogger:
    def __init__(self):
        self.indent = 1
        self.start_times = {}
        self.start_time = time.perf_counter()

    def log(self, message):
        time_diff = (time.perf_counter() - self.start_time) * 1000
        # timediff from ms to "h m s ms"
        hours, rem = divmod(time_diff // 1000, 3600)
        minutes, seconds = divmod(rem, 60)
        milliseconds = int(round(time_diff % 1000))
        formatted_time = f"{int(hours)}:{int(minutes)}:{int(seconds)} {milliseconds:03.2F}ms"
        if message:
            logger.info(f"{formatted_time}" + " " * self.indent + message)
            print(f"{formatted_time}" + " " * self.indent + message)
        else:
            logger.info("")

    def enter(self, class_name, method_name, args, kwargs):
        self.start_times[self.indent] = time.perf_counter()

        msg = f"+  {colored(class_name, 'light_blue')}.{colored(method_name, 'cyan')}"
        params_str = params(args, kwargs)

        self.log(f"{msg}{params_str}")
        self.indent += 1

    def exit(self, class_name, method_name, result):
        self.indent -= 1
        start_time = self.start_times[self.indent]
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        class_name = colored(class_name, "light_blue")
        method_name = colored(method_name, "cyan")
        msg = f"-  {class_name}.{method_name}{colored('()', 'light_red')} ({execution_time:03.2f})"
        if result:
            msg += f" = {colored(truncate(result), 'yellow', attrs=['dark'])}"
        self.log(msg)
        self.log("")


indent_logger = IndentLogger()


def pvars(text="", frame=None):
    frame = sys._getframe(1) if frame is None else frame
    local_vars = frame.f_locals
    info = frame.f_code
    print(f"{info.co_filename}: {info.co_name} ({frame.f_lineno})")
    print(f"+++ local vars {text}+++")

    pprint(local_vars, depth=2)
    print("--- local vars ---\n")


def debug_log(method):
    @functools.wraps(method)
    def wrapped(*args, **kwargs):
        try:
            class_name = args[0].__class__.__name__ if len(args) else ""
            method_name = method.__name__
            indent_logger.enter(class_name, method_name, args[1:], kwargs)
            result = method(*args, **kwargs)
            indent_logger.exit(class_name, method_name, result)
        except Exception as e:
            msg = PrettyStack(e)
            logging.error(msg)
            sys.exit(-1)
        return result

    DECORATED_FUNCTIONS.add(method.__name__)
    return wrapped


def class_debug_log(cls, skip=False):
    if skip:
        return cls
    if logger.level == logging.DEBUG:
        indent_logger.log(f"@class_debug_lo {cls}")
        for key, value in vars(cls).items():
            if not callable(value):
                continue
            if isinstance(value, staticmethod):
                continue
            setattr(cls, key, debug_log(value))
    return cls