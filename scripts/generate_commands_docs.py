#!/usr/bin/env python3

# Copyright 2022, DragonflyDB authors.  All rights reserved.
# See LICENSE for licensing terms.


import pathlib
import requests
import sys
import json
import argparse
import logging
from functools import partial
from io import StringIO, TextIOWrapper
from random import choice
import re
import os
from textwrap import fill
from typing import Optional, Sequence
from xmlrpc.client import Boolean
from enum import Enum
from railroad import *
from typing import List
import pytoml
import yaml

USER = "dragonflydb"
REPO_NAME = "redis-doc"

# Non-breaking space
NBSP = '\xa0'

# HTML Word Break Opportunity
WBR = '<wbr>'


class ArgumentType(Enum):
    INTEGER = 'integer'
    DOUBLE = 'double'
    STRING = 'string'
    UNIX_TIME = 'unix-time'
    PATTERN = 'pattern'
    KEY = 'key'
    ONEOF = 'oneof'
    BLOCK = 'block'
    PURE_TOKEN = 'pure-token'
    COMMAND = 'command'


FM_TYPES = {
    '{\n': {
        'eof': '}\n',
        'ext': '.json'
    },
    '---\n': {
        'eof': '---\n',
        'ext': '.yaml'
    },
    '+++\n': {
        'eof': '+++\n',
        'ext': '.toml'
    }
}

PARSERS = {
    '.json': {
        'dump': lambda x, y: json.dump(x, y, indent=4),
        'dumps': lambda x: json.dumps(x, indent=4),
        'load': lambda x: json.load(x),
        'loads': lambda x: json.loads(x),
    },
    '.yaml': {
        'dump': lambda x, y: yaml.dump(x, y),
        'dumps': lambda x: yaml.dump(x),
        'load': lambda x: yaml.load(x, Loader=yaml.FullLoader),
        'loads': lambda x: yaml.load(io.StringIO(x), Loader=yaml.FullLoader),
    },
    '.toml': {
        'dump': lambda x, y: pytoml.dump(x, y),
        'dumps': lambda x: pytoml.dumps(x),
        'load': lambda x: pytoml.load(x),
        'loads': lambda x: pytoml.loads(x),
    },
}


def do_dumps(payload: str, file_type: str):
    return PARSERS[file_type]['dumps'](payload)


def do_dump_file(payload: str, file_type: str, file_handler: TextIOWrapper):
    return PARSERS[file_type]['dump'](payload, file_handler)


def do_load(payload: str, file_type: str):
    return PARSERS[file_type]["loads"](payload)


def do_load_file(payload: str, file_type: str, file_handler: TextIOWrapper):
    PARSERS[file_type]["load"](payload, file_handler)


def command_filename(name: str) -> str:
    return name.lower().replace(' ', '-')


def base_url(user, repo_name):
    return f'https://raw.githubusercontent.com/{user}/{repo_name}/master/'


def read_from_github(path_to_file):
    base_name = base_url(USER, REPO_NAME)
    url = f'{base_name}/{path_to_file}'
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        return req.text
    else:
        logging.debug('Content was not found.')
        return None


def read_from_local(base_path, path_to_file):
    full_path = os.path.join(base_path, path_to_file)
    txt = pathlib.Path(full_path).read_text()
    return txt


def read_md_file(command_name: str, read_f) -> str:
    command_name = command_filename(command_name)
    content = read_f(f"commands/{command_name}.md")
    return content


def read_commands_json(read_f) -> dict:
    content = read_f('commands.json')
    if content is not None:
        commands = json.loads(content)
        return commands
    else:
        return None


def generate_payload_from_md(file_name: str, read_f):
    payload = read_md_file(file_name, read_f)
    i = 0
    while i < len(payload):
        if payload[i].startswith('\ufeff'):  # BOM workaround
            payload[i] = payload[i][1:]
        if payload[i].strip() == '':         # Munch newlines and whitespaces
            i += 1
        else:
            fm_type = FM_TYPES.get(payload[i])
        break

    if not fm_type:
        payload = ''.join(payload)
        fm_type = FM_TYPES.get('---\n')
        fm_ext = fm_type.get('ext')
        return payload, fm_type, None
    eof, fm_ext = fm_type.get('eof'), fm_type.get('ext')

    fm_data = {}
    if fm_ext == '.json':
        fm_data.update(do_load(
            fm_ext, ''.join(payload[i:j+1])))
        payload = ''.join(payload[j+1:])
    else:
        fm_data.update(do_load(
            fm_ext, ''.join(payload[i+1:j])))
        payload = ''.join(payload[j+1:])
    logging.info(
        f"we have payload of size {len(payload)} and fm type {fm_type}")
    return payload, fm_type, fm_data


class RuntimeException(Exception):
    def __init__(self, err: str):
        self.error = err

    def __str__(self):
        return self.error


# def syntax(name: str, **kwargs) -> str:
#     opts = {
#         'width': kwargs.get('width', 68),
#         'subsequent_indent': ' ' * 2,
#         'break_long_words': False,
#         'break_on_hyphens': False
#     }
#     args = [name] + [arg.syntax() for arg in self._arguments]
#     return fill(' '.join(args), **opts)


class Argument:
    def __init__(self, data: dict = {}, level: int = 0) -> None:
        self._level: int = level
        self._name: str = data['name']
        self._type = ArgumentType(data['type'])
        self._optional: bool = data.get('optional', False)
        self._multiple: bool = data.get('multiple', False)
        self._multiple_token: bool = data.get('multiple_token', False)
        self._token: str | None = data.get('token')
        self._display: str = data.get('display', self._name)
        if self._token == '':
            self._token = '""'
        self._arguments: List[Argument] = [
            Argument(arg, self._level+1) for arg in data.get('arguments', [])]

    def syntax(self, **kwargs) -> str:
        show_types = kwargs.get('show_types')
        args = ''
        if self._type == ArgumentType.BLOCK:
            args += ' '.join([arg.syntax() for arg in self._arguments])
        elif self._type == ArgumentType.ONEOF:
            args += f' | '.join([arg.syntax() for arg in self._arguments])
        elif self._type != ArgumentType.PURE_TOKEN:
            args += self._display
            if show_types:
                args += f':{self._type.value}'

        syntax = ''
        if self._optional:
            syntax += '['

        if self._token:
            syntax += f'{self._token}'
            if self._type != ArgumentType.PURE_TOKEN:
                syntax += NBSP

        if self._type == ArgumentType.ONEOF and (not self._optional or self._token):
            syntax += '<'

        if self._multiple:
            if self._multiple_token:
                syntax += f'{args} [{self._token} {args} ...]'
            else:
                syntax += f'{args} [{args} ...]'
        else:
            syntax += args

        if self._type == ArgumentType.ONEOF and (not self._optional or self._token):
            syntax = f'{syntax.rstrip()}>'
        if self._optional:
            syntax = f'{syntax.rstrip()}]'

        return f'{syntax}'


def make_args_list(name: str, args: dict) -> Argument:
    carg = {
        'name': name,
        'type': ArgumentType.COMMAND.value,
        'arguments': args.get('arguments', [])
    }
    arguments = Argument(carg, 0)
    return arguments


def args_syntax(name: str, args: dict) -> str:
    arguments = make_args_list(name, args)
    s = ' '.join([arg.syntax() for arg in arguments._arguments[1:]])
    return s


def help_command(name: str) -> bool:
    return name.endswith(" HELP")


def container_cmd(cmd_info: dict) -> bool:
    return cmd_info.get('arguments') is None and cmd_info.get('arity', 0) == -2 and len(cmd_info.split(' ')) == 1


def command_args(name: str, args: dict, **kwargs) -> str:
    opts = {
        'width': kwargs.get('width', 68),
        'subsequent_indent': ' ' * 2,
        'break_long_words': False,
        'break_on_hyphens': False
    }
    arguments = make_args_list(name, args)
    args = [name] + [arg.syntax() for arg in arguments._arguments]
    return fill(' '.join(args), **opts)


def get_command_tokens(arguments: dict) -> set:
    rep = set()
    if type(arguments) is list:
        for arg in arguments:
            rep = rep.union(get_command_tokens(arg))
    else:
        if 'token' in arguments:
            rep.add(arguments['token'])
        if 'arguments' in arguments:
            for arg in arguments['arguments']:
                rep = rep.union(get_command_tokens(arg))
    return rep


def generate_commands_links(name: str, commands: dict, payload: str) -> str:
    def fix_links(commands: dict, name: str):
        if name:
            exclude = set([name])
            tokens = get_command_tokens(commands.get(name))
            exclude.union(tokens)
        else:
            exclude = set()

        def generate_md_links(m):
            command = m.group(1)
            if command in commands and command not in exclude:
                return f'[`{command}`](/commands/{command_filename(command)})'
            else:
                return m.group(0)
        return generate_md_links
    links = fix_links(commands, name)
    rep = re.sub(r'`([A-Z][A-Z-_ \.]*)`', links, payload)
    rep = re.sub(r'`!([A-Z][A-Z-_ \.]*)`', lambda x: f'`{x[1]}`', rep)
    return rep


def add_command_frontmatter(name: str, commands: dict, fm_data: dict):
    """ Sets a JSON FrontMatter payload for a command page """
    data = commands.get(name)
    data.update({
        'title': name,
        'linkTitle': name,
        'description': data.get('summary'),
        'syntax_str': args_syntax(name, data),
        'syntax_fmt': command_args(name, data),
        'hidden': container_cmd(data) or help_command(name)
    })
    if 'replaced_by' in data:
        data['replaced_by'] = generate_commands_links(
            name, commands, data.get('replaced_by'))
    fm_type = FM_TYPES.get('---\n')
    fm_ext = fm_type.get('ext')
    fm_data.update(data)


def persist(payload: str, data: dict, is_json: Boolean, filepath: str, file_type: dict) -> int:
    '''
    Save to persist storage
    '''
    fm = do_dumps(data, file_type['ext'])
    logging.info(
        f"saving payload of len {len(payload)} and header of {len(data)} to file {filepath}")
    if not is_json:
        fm = f'{file_type.get("eof")}{fm}{file_type.get("eof")}'
    else:
        fm += '\n'

    payload = fm + payload
    dir_p = os.path.dirname(filepath)
    logging.info(
        f"saving payload of len {len(payload)} to file {filepath}, creating at {dir_p}")
    pathlib.Path(dir_p).mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        return f.write(payload) > 0


def convert_command_sections(payload: str):
    """ Converts redis-doc section headers to MD """
    rep = re.sub(r'@examples\n',
                 '## Examples\n', payload)
    rep = re.sub(r'@return\n',
                 '## Return\n', rep)
    return rep


def convert_reply_shortcuts(payload: str) -> str:
    """ Convert RESP2 reply type shortcuts to links """
    def reply(x):
        resp2 = {
            'nil': ('resp-bulk-strings', 'Null reply'),
            'simple-string': ('resp-simple-strings', 'Simple string reply'),
            'integer': ('resp-integers', 'Integer reply'),
            'bulk-string': ('resp-bulk-strings', 'Bulk string reply'),
            'array': ('resp-arrays', 'Array reply'),
            'error': ('resp-errors', 'Error reply'),

        }
        rep = resp2.get(x.group(1), None)
        if rep:
            return f'[{rep[1]}](/docs/reference/protocol-spec#{rep[0]})'
        return f'[]'

    rep = re.sub(r'@([a-z\-]+)-reply', reply, payload)
    return rep


def process_command(name: str, commands: dict, payload: str) -> str:
    """ New command processing logic """
    payload = generate_commands_links(
        name, commands, payload)
    payload = convert_command_sections(payload)
    payload = convert_reply_shortcuts(payload)
    # payload = convert_cli_snippets(payload)
    return payload


def persist_command(name: str, commands: dict, payload: str, filepath: str, fm_data: dict, file_type: dict) -> int:
    """
    name: the name of the command: for example "ACL"
    commands: data taken from data/commands.json file and convert to python dict
    filepath: path to the index.md file: content/en/commands/<commmand name>
    fm_data: dict with {'github_branch': <branch name>, 'github_path': <command/file name .md>', github_repo': <pointer to the repo url>}
    is_json: <file extenuation == json
    file_type: dict {'eof': '---\n', 'ext': '.yaml'}
    """
    is_json = file_type['ext'] == "'.json" if file_type['ext'] else False
    logging.info(
        f'Processing command {name} from {filepath}, from json {is_json}')
    add_command_frontmatter(name, commands, fm_data)
    payload = process_command(name, commands, payload)
    return persist(payload, fm_data, is_json, filepath, file_type)


def filepath_from_cmd(cmd_name: str, base_name: str) -> str:
    def command_filename(name: str) -> str:
        return name.lower().replace(' ', '-')
    """
    get the path to the md file from the commands list based on the command name
    """
    file_name = command_filename(cmd_name)
    return os.path.join(base_name, file_name)


def driver(commands: dict, out_dir: str, read_f, support_cmd: List) -> int:
    # try:
    commands = read_commands_json(read_f)
    max = len(support_cmd)
    count = 0
    for cmd_name, cmd_info in commands.items():
        if cmd_name in support_cmd:
            if count == max:
                logging.info(f"finish processing after {count}")
                return 0
            else:
                count += 1
            if read_md_file(command_filename(cmd_name), read_function):
                logging.debug(f"successfully read data for {cmd_name}")
            else:
                logging.error(f"failed to read the md file for {cmd_name}")
                return False
            filepath = os.path.join(filepath_from_cmd(
                cmd_name, out_dir), "index.md")
            default_repos = {'github_branch': "main",
                             "github_path": filepath, "github_repo": f"https://{USER}/{REPO_NAME}"}
            payload, f_type, m_data = generate_payload_from_md(
                cmd_name, read_f)
            fm_data = m_data if m_data else default_repos
            fm_type = f_type if f_type is not None else FM_TYPES['---\n']
            if persist_command(cmd_name, commands, payload, filepath, fm_data, fm_type) == 0:
                raise RuntimeException(
                    f"failed to process command {cmd_name} for file {filepath}")
    return 0
    # except Exception as e:
    #     print(
    #         f"failed to process commands into documentation: {e}")
    #     return -1


def process_docs(read_f, out_dir) -> bool:
    commands = read_commands_json(read_function)
    if commands is None:
        logging.error("failed to read commands list")
        return False
    else:
        logging.debug(
            f"we have {len(commands)} commands from commands.json file")
        cmd = ["HSET", "LLEN", "LMPOP", "LMOVE",
               "SET", "GET", "SUBSCRIBE", "PUBLISH"]
        if driver(commands, out_dir, read_f, cmd) < 0:
            return False
    return True


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format=f'{sys.argv[0]}: %(levelname)s %(asctime)s %(message)s', filename="/tmp/build_commands_documents_messages.log")
    parser = argparse.ArgumentParser(
        description='converting markdown files to website commands documentation.')
    parser.add_argument(
        "-l", "--local", help="Running with local repository <repo path>", type=str)
    #
    parser.add_argument(
        "-o", "--output_dir", help="Output directory to which result will be writing <path>", type=str, required=True)
    args = parser.parse_args()
    if args.local:
        if os.path.exists(args.local) and pathlib.Path(args.local).is_dir():
            read_f = partial(read_from_local, args.local)
            logging.debug(f"running from files at {args.local}")
            read_function = read_f
        else:
            print(
                f"not such directory {args.local} - you must use a valid path to the location of the commands.json and commands directory")
            sys.exit(1)
    else:
        logging.debug(f"running with remote host {base_url(USER, REPO_NAME)}")
        read_function = read_from_github
    #
    p = pathlib.Path(args.output_dir)
    p.mkdir(parents=True, exist_ok=True)
    if not process_docs(read_function, args.output_dir):
        logging.error("failed to process input data to commands documents")
        sys.exit(1)
    sys.exit(0)
