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
        _timeStep_: The number of timesteps per hour used by the sunPath component that generated the sun vectors. This number should be smaller than 60 and divisible by 60. The default is set to 1 such that one ssun vector is generated for each hour.
        _geometry: Geometry for which sunlight hours analysis will be conducted.  Geometry must be either a Brep, a Mesh or a list of Breps or Meshes.
        _sunIsVisible: A grafted data stream for each test point with a "1" for each hour of the sunVectors that the sun is visible and a "0" for each hour of the sunVectors when the sun is blocked.
    Returns:
        readMe!: ...
        analysisMesh: An uncolored mesh representing the test _geometry that will be analyzed.  Connect this output to a "Mesh" grasshopper component to preview this output seperately from the others of this component. Note that this mesh is generated before the analysis is run, allowing you to be sure that the right geometry will be run through the analysis before running this component.
        solarInterrupted: Interupted sunlight hours.
        placeholder: midscript list.
"""

ghenv.Component.Name = "Ladybug_Template"
ghenv.Component.NickName = 'WIP.'
ghenv.Component.Message = 'VER 0.0.67\nSEP_26_2019'
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "6 | WIP"
#compatibleLBVersion = VER 0.0.59\nJAN_24_2016
#row in a section, undefined for now
#try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
#except: pass

#gh libs
import Grasshopper.Kernel as gh
import scriptcontext as sc
import ghpythonlib.components as ghc 
import ghpythonlib.treehelpers as th
import Rhino

#python libs
import itertools

w = gh.GH_RuntimeMessageLevel.Warning

def checkTheInputs():
    if len(_geometry)!=0 and _geometry[0] != None:
        return True
    else:
        return False

def main(timestep, geometry, sunisvisible):
    #set output dict
    result = {"analysismesh":[], "solarinterrupted":[], "placeholder":[]}
    
    #===clean the geometry and bring them to rhinoCommon separated as mesh and Brep===
    analysisMesh, analysisBrep = lb_preparation.cleanAndCoerceList(geometry)

    conversionFac = lb_preparation.checkUnits()
    gridSize = 4/conversionFac
    
    #mesh Brep
    analysisMeshedBrep = lb_mesh.parallel_makeSurfaceMesh(analysisBrep, float(gridSize))
    
    #Flatten the list of surfaces
    analysisMeshedBrep = lb_preparation.flattenList(analysisMeshedBrep)
    analysisSrfs = analysisMesh + analysisMeshedBrep
    
    #===prepare sunvisible===
    sun_1 = ghc.CullIndex(sunisvisible, -1, True)
    sun_2 = ghc.CullIndex(sunisvisible, 0, True)
    
    #mass addition
    sun_addition = [sum(i) for i in itertools.izip_longest(sun_1, sun_2, fillvalue=0)]
    #print sun_addition
    
    #member indexes, this approach produces empty lists instead of error if not found, thus better
    sun_indx = [i for i, k in enumerate(sun_addition) if k == 1]
    
    
    #===compute rays===
    if sun_indx:
        
        #===compute placeholder value===
        plc_indx = [i for i, k in enumerate(sun_indx) if k == 0]
        result["placeholder"] = ghc.ReplaceItems(sun_indx, 1, plc_indx, False)
        #print result["placeholder"]
        
        rays_addition = [i+1 for i in sun_indx]
        rays_insert_1 = ghc.DeleteConsecutive(ghc.InsertItems(rays_addition, 0, 0, True), False)[0]
        rays_insert_2 = ghc.DeleteConsecutive(ghc.InsertItems(rays_addition, len(_sunIsVisible), -1, True), False)[0]
        rays_substraction = ghc.Subtraction(rays_insert_2, rays_insert_1)
        
        #mimic pattern creation without refering to split tree 
        pattern = [0]
        val = itertools.cycle([1, 0])
        for i in sun_indx:
            pattern.append(next(val))
        
        rays_dispatched = ghc.Dispatch(rays_substraction, pattern)[0]
    
    #transfer mesh
    result["analysismesh"] = analysisSrfs
    
    
    return result #-1


#If Honeybee or Ladybug is not flying or is an older version, give a warning.
initCheck = True

#Ladybug check.
if not sc.sticky.has_key('ladybug_release') == True:
    initCheck = False
    print "You should first let Ladybug fly..."
    ghenv.Component.AddRuntimeMessage(w, "You should first let Ladybug fly...")
else:
    lb_preparation = sc.sticky["ladybug_Preparation"]()
    lb_mesh = sc.sticky["ladybug_Mesh"]()
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
        result = main(_timeStep_, _geometry, _sunIsVisible)
        #print result
        analysisMesh = result["analysismesh"]
        solarInterrupted = result["solarinterrupted"]
        placeholder = result["placeholder"]
