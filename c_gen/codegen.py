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
Code generation

These functions extract data from the IR and render templates with it.
"""

from collections import namedtuple
from itertools import groupby
import template_utils
import loxi_globals
import loxi_ir.ir as ir
import util
import c_code_gen
import c_gen.of_g_legacy as of_g

PushWireTypesFn = namedtuple('PushWireTypesFn',
    ['class_name', 'versioned_type_members'])
PushWireTypesMember = namedtuple('PushWireTypesMember',
    ['name', 'offset', 'length', 'value'])

def gen_push_wire_types(install_dir):
    fns = []
    for uclass in loxi_globals.unified.classes:
        if uclass.virtual or not uclass.has_type_members:
            continue

        # Generate a dict of version -> list of PushWireTypesMember
        type_members_by_version = {}
        for version, ofclass in sorted(uclass.version_classes.items()):
            pwtms = []
            for m in ofclass.members:
                if isinstance(m, ir.OFTypeMember):
                    if m.name == "version" and m.value == version.wire_version:
                        # Special case for version
                        pwtms.append(PushWireTypesMember(m.name, m.offset, m.length, "obj->version"))
                    else:
                        pwtms.append(PushWireTypesMember(m.name, m.offset, m.length, m.value))
            type_members_by_version[version] = pwtms

        # Merge versions with identical type members
        all_versions = sorted(type_members_by_version.keys())
        versioned_type_members = []
        for pwtms, versions in groupby(all_versions, type_members_by_version.get):
            versioned_type_members.append((pwtms, list(versions)))

        fns.append(PushWireTypesFn(
            class_name=uclass.name,
            versioned_type_members=versioned_type_members))

    with template_utils.open_output(install_dir, "loci/src/loci_push_wire_types.c") as out:
        util.render_template(out, "loci_push_wire_types.c", fns=fns)

    with template_utils.open_output(install_dir, "loci/src/loci_push_wire_types.h") as out:
        util.render_template(out, "loci_push_wire_types.h", fns=fns)

def generate_classes(install_dir):
    for uclass in loxi_globals.unified.classes:
        with template_utils.open_output(install_dir, "loci/src/%s.c" % uclass.name) as out:
            util.render_template(out, "class.c")
            # Append legacy generated code
            c_code_gen.gen_new_function_definitions(out, uclass.name)
            c_code_gen.gen_accessor_definitions(out, uclass.name)

# TODO remove header classes and use the corresponding class instead
def generate_header_classes(install_dir):
    for cls in of_g.standard_class_order:
        if cls.find("_header") < 0:
            continue
        with template_utils.open_output(install_dir, "loci/src/%s.c" % cls) as out:
            util.render_template(out, "class.c")
            # Append legacy generated code
            c_code_gen.gen_new_function_definitions(out, cls)
            c_code_gen.gen_accessor_definitions(out, cls)

def generate_lists(install_dir):
    for cls in of_g.ordered_list_objects:
        with template_utils.open_output(install_dir, "loci/src/%s.c" % cls) as out:
            util.render_template(out, "class.c")
            # Append legacy generated code
            c_code_gen.gen_new_function_definitions(out, cls)
            c_code_gen.gen_list_accessors(out, cls)
