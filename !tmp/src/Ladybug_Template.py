# Ladybug: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
#
# This file is part of Ladybug.
#
# Copyright (c) 2013-2015, ....(YOUR NAME).... <....(YOUR EMAIL)....>
# Ladybug is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License,
# or (at your option) any later version.
#
# Ladybug is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Use this component to ....(COMPONENT DESCRIPTION)....
_
....(REFERENCES + PAPERS)....
-
Provided by Ladybug 0.0.67

    Args:
        _input1: A ....(DATE TYPE).... that represents ....(INPUT DESCRIPTION).... .
        _input2_: A ....(DATE TYPE).... that represents ....(INPUT DESCRIPTION).... .  If nothing is connected here, a default of ....(DEFAULT VALUE).... will be used.
        input3_: The output from the ....(OTHER LB COMPONENT).... component.  Use this to ....(INPUT DESCRIPTION).... .
    Returns:
        readMe!: ...
        output1: A ....(DATE TYPE).... that represents ....(OUTPUT DESCRIPTION).... .
		output2: A ....(DATE TYPE).... that represents ....(OUTPUT DESCRIPTION).... .
		output3: A ....(DATE TYPE).... that represents ....(OUTPUT DESCRIPTION).... .
"""

ghenv.Component.Name = "Ladybug_Template"
ghenv.Component.NickName = 'WIP.'
ghenv.Component.Message = 'VER 0.0.67\nSEP_25_2019'
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "6 | WIP"
#compatibleLBVersion = VER 0.0.59\nJAN_24_2016
#try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
#except: pass

import Grasshopper.Kernel as gh
import scriptcontext as sc

w = gh.GH_RuntimeMessageLevel.Warning




def checkTheInputs():
    #....(INSERT INPUT CHECKING FUNCTIONS HERE)....
    if _test:
        return True
    else:
        return False


def main():
    #....(INSERT MAIN COMPONENTS FUNCTIONS HERE)....

    return "test" #-1


#If Honeybee or Ladybug is not flying or is an older version, give a warning.
initCheck = True

#Ladybug check.
if not sc.sticky.has_key('ladybug_release') == True:
    initCheck = False
    print "You should first let Ladybug fly..."
    ghenv.Component.AddRuntimeMessage(w, "You should first let Ladybug fly...")
else:
    try:
        if not sc.sticky['ladybug_release'].isCompatible(ghenv.Component): initCheck = False
        if sc.sticky['ladybug_release'].isInputMissing(ghenv.Component): initCheck = False
    except:
        initCheck = False
        warning = "You need a newer version of Ladybug to use this compoent." + \
        "Use updateLadybug component to update userObjects.\n" + \
        "If you have already updated userObjects drag Ladybug_Ladybug component " + \
        "into canvas and try again."
        ghenv.Component.AddRuntimeMessage(w, warning)


#If the intital check is good, run the component.
if initCheck:
    checkData = checkTheInputs()
    if checkData:
        result = main()
        if result != -1:
            output = result
            test = output
