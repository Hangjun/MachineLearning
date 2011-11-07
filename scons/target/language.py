############################################################################
# LGPL License                                                             #
#                                                                          #
# This file is part of the Machine Learning Framework.                     #
# Copyright (c) 2010, Philipp Kraus, <philipp.kraus@flashpixx.de>          #
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Lesser General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Lesser General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Lesser General Public License #
# along with this program. If not, see <http://www.gnu.org/licenses/>.     #
############################################################################

# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("..")
import help

Import("*")
 
 
sources = []
for i in env["CPPSUFFIXES"] :
    lst = help.getRekusivFiles(os.path.join("..", ".."), i, ["examples", "scons", "install", "build"], True, False)
    for i in lst :
        sources.append( os.path.sep.join(i.split(os.path.sep)[2:]) )


# get all strings out of the sources
updatetargets  = []
createtargets  = []
compiletargets = []
updatetargets.append( env.Command("xgettext", "", "xgettext --output="+os.path.join("tools", "language", "language.po")+" --keyword=_ --language=c++ " + " ".join(sources)) )
createtargets.extend( updatetargets )


# get all language files in the subdirs and add the new texts
po = help.getRekusivFiles(os.path.join("..", "..", "tools", "language"), ".po") 
for i in po :
    updatetargets.append( env.Command("msmerge", "", "msgmerge --no-wrap --update " + os.path.sep.join(i.split(os.path.sep)[2:]) + " "+os.path.join("tools", "language", "language.po") ) )
    createtargets.append( env.Command("msmerge", "", "msgmerge --no-wrap --update " + os.path.sep.join(i.split(os.path.sep)[2:]) + " "+os.path.join("tools", "language", "language.po") ) )

createtargets.append( env.Command("deletelang", "", [Delete(os.path.join("tools", "language", "language.po"))] ) )
updatetargets.append( env.Command("deletelang", "", [Delete(os.path.join("tools", "language", "language.po"))] ) )

# compiling all files
for i in po :
    updatefile = os.path.join(os.path.dirname(i), "machinelearning.mo")
    updatefile = os.path.sep.join(updatefile.split(os.path.sep)[2:]) 
    
    updatetargets.append( env.Command("msgfmt", "", "msgfmt -v -o " + updatefile +" "+ os.path.sep.join(i.split(os.path.sep)[2:]) ) )
    compiletargets.append( env.Command("msgfmt", "", "msgfmt -v -o " + updatefile +" "+ os.path.sep.join(i.split(os.path.sep)[2:]) ) )
    

env.Alias("updatelanguage", updatetargets)
env.Alias("createlanguage", createtargets)
env.Alias("compilelanguage", compiletargets)