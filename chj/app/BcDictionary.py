# ------------------------------------------------------------------------------
# CodeHawk Java Analyzer
# Author: Henny Sipma
# ------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 Kestrel Technology LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

import chj.util.IndexedTable as IT

import chj.app.Bytecode as BC

opcode_constructors = {
    'ld': lambda x: BC.BcLoad(*x),
    'st': lambda x: BC.BcStore(*x),
    'inc': lambda x: BC.BcIInc(*x),
    'icst': lambda x: BC.BcIntConst(*x),
    'lcst': lambda x: BC.BcLongConst(*x),
    'fcst': lambda x: BC.BcFloatConst(*x),
    'dcst': lambda x: BC.BcDoubleConst(*x),
    'bcst': lambda x: BC.BcByteConst(*x),
    'shcst': lambda x: BC.BcShortConst(*x),
    'scst': lambda x: BC.BcStringConst(*x),
    'ccst': lambda x: BC.BcClassConst(*x),
    'add': lambda x: BC.BcAdd(*x),
    'sub': lambda x: BC.BcSub(*x),
    'mult': lambda x: BC.BcMult(*x),
    'div': lambda x: BC.BcDiv(*x),
    'rem': lambda x: BC.BcRem(*x),
    'neg': lambda x: BC.BcNeg(*x),
    'ifeq': lambda x: BC.BcIfEq(*x),
    'ifne': lambda x: BC.BcIfNe(*x),
    'iflt': lambda x: BC.BcIfLt(*x),
    'ifge': lambda x: BC.BcIfGe(*x),
    'ifgt': lambda x: BC.BcIfGt(*x),
    'ifle': lambda x: BC.BcIfLe(*x),
    'ifnull': lambda x: BC.BcIfNull(*x),
    'ifnonnull': lambda x: BC.BcIfNonNull(*x),
    'ifcmpeq': lambda x: BC.BcIfCmpEq(*x),
    'ifcmpne': lambda x: BC.BcIfCmpNe(*x),
    'ifcmplt': lambda x: BC.BcIfCmpLt(*x),
    'ifcmpge': lambda x: BC.BcIfCmpGe(*x),
    'ifcmpgt': lambda x: BC.BcIfCmpGt(*x),
    'ifcmple': lambda x: BC.BcIfCmpLe(*x),
    'ifcmpaeq': lambda x: BC.BcIfCmpAEq(*x),
    'ifcmpane': lambda x: BC.BcIfCmpANe(*x),
    'goto': lambda x: BC.BcGoto(*x),
    'jsr': lambda x: BC.BcJsr(*x),
    'jret': lambda x: BC.BcRet(*x),
    'table': lambda x: BC.BcTableSwitch(*x),
    'lookup': lambda x: BC.BcLookupSwitch(*x),
    'new': lambda x: BC.BcNew(*x),
    'newa': lambda x: BC.BcNewArray(*x),
    'mnewa': lambda x: BC.BcAMultiNewArray(*x),
    'ccast': lambda x: BC.BcCheckCast(*x),
    'iof': lambda x: BC.BcInstanceOf(*x),
    'gets': lambda x: BC.BcGetStatic(*x),
    'puts': lambda x: BC.BcPutStatic(*x),
    'getf': lambda x: BC.BcGetField(*x),
    'putf': lambda x: BC.BcPutField(*x),
    'ald': lambda x: BC.BcArrayLoad(*x),
    'ast': lambda x: BC.BcArrayStore(*x),
    'invv': lambda x: BC.BcInvokeVirtual(*x),
    'invsp': lambda x: BC.BcInvokeSpecial(*x),
    'invst': lambda x: BC.BcInvokeStatic(*x),
    'invi': lambda x: BC.BcInvokeInterface(*x),
    'invd': lambda x: BC.BcInvokeDynamic(*x),
    'ret': lambda x: BC.BcReturn(*x)
    }

class BcDictionary(object):

    def __init__(self,jclass,xnode):
        self.jclass = jclass                          # JavaClass
        self.jd = jclass.jd                           # DataDictionary
        self.pc_list_table = IT.IndexedTable('pc-list-table')
        self.slot_table = IT.IndexedTable('slot-table')
        self.slot_list_table = IT.IndexedTable('slot-list-table')
        self.opcode_table = IT.IndexedTable('opcode-table')
        self.tables = [
            (self.pc_list_table, self._read_xml_pc_list_table),
            (self.slot_table, self._read_xml_slot_table),
            (self.slot_list_table, self._read_xml_slot_list_table),
            (self.opcode_table, self._read_xml_opcode_table) ]
        self.initialize(xnode)

    def get_opcode(self,ix): return self.opcode_table.retrieve(ix)

    def get_pc_list(self,ix): return self.pc_list_table.retrieve(ix)

    def get_slot(self,ix): return self.slot_table.retrieve(ix)

    def get_slots(self,ix): return self.slot_list_table.retrieve(ix)

    def write_xml(self,node):
        def f(n,r):r.write_xml(n)
        for (t,_) in self.tables:
            tnode = ET.Element(t.name)
            t.write_xml(tnode,f)
            node.append(tnode)

    def __str__(self):
        lines = []
        for (t,_) in self.tables:
            if t.size() > 0:
                lines.append(str(t))
        return '\n'.join(lines)

    # ----------------------- Initialize dictionary from file ------------------
 
    def initialize(self,xnode,force=False):
        if xnode is None: return
        for (t,f) in self.tables:
            t.reset()
            f(xnode.find(t.name))

    def _read_xml_pc_list_table(self,txnode):
        def get_value(node):
            rep = IT.get_rep(node)
            args = (self,) + rep
            return BC.BcPcList(*args)
        self.pc_list_table.read_xml(txnode,'n',get_value)

    def _read_xml_slot_table(self,txnode):
        def get_value(node):
            rep = IT.get_rep(node)
            args = (self,) + rep
            return BC.BcSlot(*args)
        self.slot_table.read_xml(txnode,'n',get_value)

    def _read_xml_slot_list_table(self,txnode):
        def get_value(node):
            rep = IT.get_rep(node)
            args = (self,) + rep
            return BC.BcSlotList(*args)
        self.slot_list_table.read_xml(txnode,'n',get_value)

    def _read_xml_opcode_table(self,txnode):
        def get_value(node):
            rep = IT.get_rep(node)
            tag = rep[1][0]
            args = (self,) + rep
            if tag in opcode_constructors:
                return opcode_constructors[tag](args)
            else:
                return BC.BcInstruction(*args)
        self.opcode_table.read_xml(txnode,'n',get_value)
