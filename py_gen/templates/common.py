:: # Copyright 2013, Big Switch Networks, Inc.
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
:: # http://www.eclipse.org/legal/epl-v10.html
:: #
:: # Unless required by applicable law or agreed to in writing, software
:: # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
:: # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
:: # EPL for the specific language governing permissions and limitations
:: # under the EPL.
::
:: include('_copyright.py')

:: include('_autogen.py')

import sys
import struct
import action
import const
import util

# HACK make this module visible as 'common' to simplify code generation
common = sys.modules[__name__]

def unpack_list_flow_stats_entry(buf):
    entries = []
    offset = 0
    while offset < len(buf):
        length, = struct.unpack_from("!H", buf, offset)
        if length == 0: raise loxi.ProtocolError("entry length is 0")
        if offset + length > len(buf): raise loxi.ProtocolError("entry length overruns list length")
        entries.append(flow_stats_entry.unpack(buffer(buf, offset, length)))
        offset += length
    return entries

def unpack_list_queue_prop(buf):
    entries = []
    offset = 0
    while offset < len(buf):
        type, length, = struct.unpack_from("!HH", buf, offset)
        if length == 0: raise loxi.ProtocolError("entry length is 0")
        if offset + length > len(buf): raise loxi.ProtocolError("entry length overruns list length")
        if type == const.OFPQT_MIN_RATE:
            entry = queue_prop_min_rate.unpack(buffer(buf, offset, length))
        else:
            raise loxi.ProtocolError("unknown queue prop %d" % type)
        entries.append(entry)
        offset += length
    return entries

def unpack_list_packet_queue(buf):
    entries = []
    offset = 0
    while offset < len(buf):
        _, length, = struct.unpack_from("!LH", buf, offset)
        if length == 0: raise loxi.ProtocolError("entry length is 0")
        if offset + length > len(buf): raise loxi.ProtocolError("entry length overruns list length")
        entries.append(packet_queue.unpack(buffer(buf, offset, length)))
        offset += length
    return entries

:: for ofclass in ofclasses:
class ${ofclass.pyname}(object):
:: for m in ofclass.type_members:
    ${m.name} = ${m.value}
:: #endfor

    def __init__(self, ${', '.join(["%s=None" % m.name for m in ofclass.members])}):
:: for m in ofclass.members:
        if ${m.name} != None:
            self.${m.name} = ${m.name}
        else:
            self.${m.name} = ${m.oftype.gen_init_expr()}
:: #endfor

    def pack(self):
        packed = []
:: include("_pack.py", ofclass=ofclass)
        return ''.join(packed)

    @staticmethod
    def unpack(buf):
        assert(len(buf) >= ${ofclass.min_length}) # Should be verified by caller
        obj = ${ofclass.pyname}()
:: include("_unpack.py", ofclass=ofclass)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
:: for m in ofclass.members:
        if self.${m.name} != other.${m.name}: return False
:: #endfor
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def show(self):
        import loxi.pp
        return loxi.pp.pp(self)

    def pretty_print(self, q):
:: include('_pretty_print.py', ofclass=ofclass)

:: if ofclass.name.startswith("of_match_v"):
match = ${ofclass.pyname}

:: #endif
:: #endfor
