# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

"""
Python backend for LOXI

This language specific file defines a dictionary 'targets' that
defines the generated files and the functions used to generate them.

For each generated file there is a generate_* function in py_gen.codegen
and a Tenjin template under py_gen/templates.

Target directory structure:
    pyloxi:
        loxi:
            __init__.py
            of10:
                __init__.py
                action.py       # Action classes
                common.py       # Structs shared by multiple messages
                const.py        # OpenFlow constants
                message.py      # Message classes
                util.py         # Utility functions
            of11: ...           # (code generation incomplete)
                instruction.py  # Instruction classes
            of12: ...           # (code generation incomplete)
                oxm.py          # OXM classes
            of13: ...           # (code generation incomplete)
                meter_band.py   # Meter band classes

The user will add the pyloxi directory to PYTHONPATH. Then they can
"import loxi" or "import loxi.of10". The idiomatic import is
"import loxi.of10 as ofp". The protocol modules (e.g. of10) import
all of their submodules, so the user can access "ofp.message" without
further imports. The protocol modules also import the constants from
the const module directly into their namespace so the user can access
"ofp.OFPP_NONE".
"""

import os
from loxi_globals import OFVersions
import loxi_globals
import loxi_utils.loxi_utils as loxi_utils
import py_gen
import py_gen.util
import py_gen.codegen
import template_utils

versions = {
    1: "of10",
    2: "of11",
    3: "of12",
    4: "of13",
}

prefix = 'pyloxi/loxi'

modules = {
    1: ["action", "common", "const", "message", "util"],
    2: ["action", "common", "const", "instruction", "message", "util"],
    3: ["action", "common", "const", "instruction", "message", "oxm", "util"],
    4: ["action", "common", "const", "instruction", "message", "meter_band", "oxm", "tlv", "util"],
}

def make_gen(name, version):
    fn = getattr(py_gen.codegen, "generate_" + name)
    return lambda out, name: fn(out, name, version)

def static(template_name):
    return lambda out, name: py_gen.util.render_template(out, template_name)

targets = {
    prefix+'/__init__.py': static('toplevel_init.py'),
    prefix+'/pp.py': static('pp.py'),
    prefix+'/generic_util.py': static('generic_util.py'),
}

for version, subdir in versions.items():
    targets['%s/%s/__init__.py' % (prefix, subdir)] = make_gen('init', version)
    for module in modules[version]:
        filename = '%s/%s/%s.py' % (prefix, subdir, module)
        targets[filename] = make_gen(module, OFVersions.from_wire(version))

def generate(install_dir):
    py_gen.codegen.init()
    for (name, fn) in targets.items():
        with template_utils.open_output(install_dir, name) as outfile:
            fn(outfile, os.path.basename(name))
