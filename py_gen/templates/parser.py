 # Copyright 2013, Big Switch Networks, Inc.
:: #
:: # LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
:: # the following special exception:
:: #
:: # LOXI Exception
:: #
:: # As a special exception to the terms of the EPL, you may distribute libraries
:: # generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
:: # that copyright and licensing notices generated by LoxiGen are not altered or removed
:: # from the LoxiGen Libraries and the notice provided below is (i) included in
:: # the LoxiGen Libraries, if distributed in source code form and (ii) included in any
:: # documentation for the LoxiGen Libraries, if distributed in binary form.
:: #
:: # Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
:: #
:: # You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
:: # a copy of the EPL at:
:: #
:: # http::: #www.eclipse.org/legal/epl-v10.html
:: #
:: # Unless required by applicable law or agreed to in writing, software
:: # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
:: # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
:: # EPL for the specific language governing permissions and limitations
:: # under the EPL.
::
:: import itertools
:: from loxi_globals import OFVersions
:: import loxi_globals
:: import py_gen.util as util
:: import py_gen.oftype
:: include('_copyright.py')

:: include('_autogen.py')

import struct
import loxi
import action, common, const, message
:: if version >= OFVersions.VERSION_1_1:
import instruction
:: #endif
:: if version >= OFVersions.VERSION_1_2:
import oxm
:: #endif
:: if version >= OFVersions.VERSION_1_3:
import meter_band
:: #endif

uint8 = struct.Struct("!B")
uint16 = struct.Struct("!H")
uint32 = struct.Struct("!L")
:: structs = { 1: "uint8", 2: "uint16", 4: "uint32" }

:: for parser in sorted(parsers):

def ${parser.name}(buf):
    try:
        subtype, = ${structs[parser.discriminator_length]}.unpack_from(buf, ${parser.discriminator_offset})
        child_parser = ${parser.name[6:]}_children[subtype]
    except struct.error:
        raise loxi.ProtocolError("Buffer too short (%d bytes)" % len(buf))
    except KeyError:
        raise loxi.ProtocolError("unknown ${parser.name[6:]} type %#x" % subtype)
    return child_parser(buf)
:: #endfor

:: for parser in sorted(parsers):

${parser.name[6:]}_children = {
:: for value, function_name in sorted(parser.children.items()):
    ${hex(value)}: ${function_name},
:: #endfor
}
:: #endfor
