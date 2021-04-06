from commands import Command
from functools import cmp_to_key

# The Makefile volume-mounts docs.merkely.com/ to /docs/
REFERENCE_DIR = '/docs/source/reference'


def create_rst_files():
    """
    Called from docs.merkely.com/source/conf.py
    Builds the Reference .rst files for each command.
    """
    command_names = Command.names()

    def cmp_names(lhs, rhs):
        order = [
            'declare_pipeline',
            'log_artifact',
            'log_evidence',
            'log_test',
            'approve_deployment',
            'request_approval',
            'control_deployment',
            'control_pull_request',
            'log_deployment',
        ]
        return order.index(lhs) - order.index(rhs)

    command_names.sort(key=cmp_to_key(cmp_names))

    rst = reference_index_rst(command_names)
    with open(f'{REFERENCE_DIR}/index.rst', 'wt') as file:
        file.write(rst)

    for command_name in command_names:
        rst = reference_command_rst(command_name)
        with open(f'{REFERENCE_DIR}/{command_name}.rst', 'wt') as file:
            file.write(rst)


def reference_index_rst(command_names):
    index = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "",
    ])
    for command_name in command_names:
        tab = " " * 3
        index += f"\n{tab}{command_name}"
    return index


def reference_command_rst(command_name):
    tab = " " * 3
    title = " ".join(list(s.capitalize() for s in command_name.split('_')))
    rst = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
        f".. _{command_name}-label:",
        "",  # required!
        title,
        "-" * len(title),
        "",
        f".. describe_command:: {command_name} summary unused",
        "",
        ".. raw:: html",
        "",
        f'{tab}<ul class="nav nav-tabs">\n',
    ])

    if command_name == 'control_pull_request':
        ci_names = ['docker', 'bitbucket']  # No support for github yet
    else:
        ci_names = ['docker', 'bitbucket', 'github']

    for ci_name in ci_names:
        if ci_name == 'docker':
            active = ' class="active"'
        else:
            active = ''
        cap = ci_name.capitalize()
        rst += f'{tab}{tab}<li{active}><a data-toggle="tab" href="#{ci_name}">{cap}</a></li>\n'

    rst += "\n".join([
        f"{tab}</ul>",
        "",
        f'{tab}<div class="tab-content">',
        "",
        "",
    ])

    for ci_name in ci_names:
        rst += f".. describe_command:: {command_name} invocation_full {ci_name}\n"

    rst += "\n".join([
        "",
        ".. raw:: html",
        "",
        f"{tab}</div>",
    ])

    return rst
