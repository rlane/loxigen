#!/usr/bin/env python
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
import unittest

try:
    import loxi
    import loxi.generic_util
    from loxi.generic_util import OFReader
except ImportError:
    exit("loxi package not found. Try setting PYTHONPATH.")

class TestUnpackList(unittest.TestCase):
    def test_simple(self):
        def deserializer(reader):
            length, = reader.peek("!B")
            return reader.read('!%ds' % length)[0]
        reader = loxi.generic_util.OFReader("\x04abc\x03de\x02f\x01")
        a = loxi.generic_util.unpack_list(reader, deserializer)
        self.assertEquals(['\x04abc', '\x03de', '\x02f', '\x01'], a)

class TestUnpackListLV16(unittest.TestCase):
    def test_simple(self):
        def deserializer(reader):
            reader.skip(2)
            return str(reader.read_all())
        reader = loxi.generic_util.OFReader("\x00\x05abc\x00\x04de\x00\x03f\x00\x02")
        a = loxi.generic_util.unpack_list_lv16(reader, deserializer)
        self.assertEquals(['abc', 'de', 'f', ''], a)

class TestOFReader(unittest.TestCase):
    def test_empty(self):
        reader = OFReader("")
        self.assertEquals(str(reader.read('')), "")
        with self.assertRaisesRegexp(loxi.ProtocolError, "Buffer too short"):
            reader.read_buf(1)

    def test_simple(self):
        reader = OFReader("abcdefg")
        self.assertEquals(reader.read('2s')[0], "ab")
        self.assertEquals(reader.read('2s')[0], "cd")
        self.assertEquals(reader.read('3s')[0], "efg")
        with self.assertRaisesRegexp(loxi.ProtocolError, "Buffer too short"):
            reader.read('s')

    def test_skip(self):
        reader = OFReader("abcdefg")
        reader.skip(4)
        self.assertEquals(reader.read('s')[0], "e")
        with self.assertRaisesRegexp(loxi.ProtocolError, "Buffer too short"):
            reader.skip(3)

    def test_empty(self):
        reader = OFReader("abcdefg")
        self.assertEquals(reader.is_empty(), False)
        reader.skip(6)
        self.assertEquals(reader.is_empty(), False)
        reader.skip(1)
        self.assertEquals(reader.is_empty(), True)
        with self.assertRaisesRegexp(loxi.ProtocolError, "Buffer too short"):
            reader.skip(1)

    def test_exception_effect(self):
        reader = OFReader("abcdefg")
        with self.assertRaisesRegexp(loxi.ProtocolError, "Buffer too short"):
            reader.skip(8)
        self.assertEquals(reader.is_empty(), False)
        reader.skip(7)
        self.assertEquals(reader.is_empty(), True)

    def test_peek(self):
        reader = OFReader("abcdefg")
        self.assertEquals(reader.peek('2s')[0], "ab")
        self.assertEquals(reader.peek('2s')[0], "ab")
        self.assertEquals(reader.read('2s')[0], "ab")
        self.assertEquals(reader.peek('2s')[0], "cd")
        reader.skip(2)
        self.assertEquals(reader.read('3s')[0], "efg")
        with self.assertRaisesRegexp(loxi.ProtocolError, "Buffer too short"):
            reader.peek('s')

    def test_read_all(self):
        reader = OFReader("abcdefg")
        reader.skip(2)
        self.assertEquals(str(reader.read_all()), "cdefg")
        self.assertEquals(str(reader.read_all()), "")

    def test_slice(self):
        reader = OFReader("abcdefg")
        reader.skip(2)
        self.assertEquals(str(reader.slice(3).read_all()), "cde")
        self.assertEquals(str(reader.slice(2).read_all()), "fg")
        self.assertEquals(reader.is_empty(), True)

if __name__ == '__main__':
    unittest.main()
