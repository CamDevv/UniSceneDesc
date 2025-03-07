#!/pxrpythonsubst                                                                   
#                                                                                   
# Copyright 2017 Pixar                                                              
#                                                                                   
# Licensed under the terms set forth in the LICENSE.txt file available at
# https://openusd.org/license.

from __future__ import print_function

from pxr import Tf, Sdf, Usd, UsdGeom, UsdShade
import unittest

palePath = Sdf.Path("/Model/Materials/MaterialSharp/Pale")
whiterPalePath = Sdf.Path("/Model/Materials/MaterialSharp/WhiterPale")
classPalePath = Sdf.Path("/classPale")

Input = UsdShade.AttributeType.Input
Output = UsdShade.AttributeType.Output

class TestUsdShadeShaders(unittest.TestCase):
    def _ConnectionsEqual(self, a, b):
        return a[0].GetPrim() == b[0].GetPrim() and a[1] == b[1] and a[2] == b[2]

    def _SetupStage(self):
        stage = Usd.Stage.CreateInMemory()

        UsdGeom.Scope.Define(stage, "/Model")
        UsdGeom.Scope.Define(stage, "/Model/Materials")
        UsdShade.Material.Define(stage, "/Model/Materials/MaterialSharp")

        pale = UsdShade.Shader.Define(stage, palePath)
        self.assertTrue(pale)
        whiterPale = UsdShade.Shader.Define(stage, whiterPalePath)
        self.assertTrue(whiterPale)

        # Make a class for pale so we can test that disconnecting/blocking works
        classPale = stage.CreateClassPrim(classPalePath)
        self.assertTrue(classPale)
        pale.GetPrim().GetInherits().AddInherit(classPalePath)
        shaderClass = UsdShade.Shader(classPale)
        # it's not valid because it's not defined, but we can still author using it
        self.assertTrue(not shaderClass)

        return stage

    def test_InputOutputConnections(self):
        stage = self._SetupStage()

        ################################
        print ('Test Input/Output connections')
        ################################

        pale = UsdShade.Shader.Get(stage, palePath)
        self.assertTrue(pale)

        whiterPale = UsdShade.Shader.Get(stage, whiterPalePath)
        self.assertTrue(whiterPale)
        
        shaderClass = UsdShade.Shader.Get(stage, classPalePath)

        print ('Test RenderType')
        chords = pale.CreateInput("chords", Sdf.ValueTypeNames.String)
        self.assertTrue(chords)
        self.assertTrue(not chords.HasRenderType())
        self.assertEqual(chords.GetRenderType(), "")
        chords.SetRenderType("notes")
        self.assertTrue(chords.HasRenderType())
        self.assertEqual(chords.GetRenderType(), "notes")

        ################################
        print ('Test scalar connections')
        ################################

        usdShadeInput = pale.CreateInput('myFloatInput', Sdf.ValueTypeNames.Float)

        # test set/get documentation.
        doc = "My shade input"
        usdShadeInput.SetDocumentation(doc)
        self.assertEqual(usdShadeInput.GetDocumentation(), doc)
        
        # test set/get dislayGroup
        displayGroup = "floats"
        usdShadeInput.SetDisplayGroup(displayGroup)
        self.assertEqual(usdShadeInput.GetDisplayGroup(), displayGroup)

        self.assertEqual(usdShadeInput.GetBaseName(), 'myFloatInput')
        self.assertEqual(usdShadeInput.GetTypeName(), Sdf.ValueTypeNames.Float)
        usdShadeInput.Set(1.0)
        self.assertTrue(not usdShadeInput.HasConnectedSource())
        
        usdShadeInput.ConnectToSource(
            UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(),
            'Fout', Output))
        self.assertTrue(usdShadeInput.HasConnectedSource())

        self.assertEqual(usdShadeInput.GetAttr().GetConnections(),
                [whiterPale.GetPath().AppendProperty("outputs:Fout")])

        self.assertEqual(usdShadeInput.GetConnectedSources()[0],
                [UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(),
                'Fout', Output)])
        usdShadeInput.ClearSources()
        self.assertTrue(not usdShadeInput.HasConnectedSource())
        self.assertEqual(usdShadeInput.GetConnectedSources()[0], [])

        # Now make the connection in the class
        inheritedInput = shaderClass.CreateInput('myFloatInput', 
                                                 Sdf.ValueTypeNames.Float)
        inheritedInput.ConnectToSource(
            UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), 'Fout', Output))
        # note we're now testing the inheritING prim's parameter
        self.assertTrue(usdShadeInput.HasConnectedSource())
        self.assertTrue(usdShadeInput.GetConnectedSources()[0],
            [UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), 'Fout', Output)])
        # clearing no longer changes anything
        usdShadeInput.ClearSources()
        self.assertTrue(usdShadeInput.HasConnectedSource())
        self.assertTrue(usdShadeInput.GetConnectedSources()[0],
            [UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), 'Fout', Output)])
        # but disconnecting should
        usdShadeInput.DisconnectSource()
        self.assertTrue(not usdShadeInput.HasConnectedSource())
        self.assertEqual(usdShadeInput.GetConnectedSources()[0], [])


        ################################
        print('Test asset id')
        ################################
        self.assertEqual(pale.GetImplementationSource(), UsdShade.Tokens.id)
        self.assertEqual(whiterPale.GetImplementationSource(), 
                         UsdShade.Tokens.id)

        self.assertTrue(pale.SetShaderId('SharedFloat_1'))
        self.assertEqual(pale.GetShaderId(), 'SharedFloat_1')

        self.assertTrue(whiterPale.CreateIdAttr('SharedColor_1'))
        self.assertEqual(whiterPale.GetIdAttr().Get(), 'SharedColor_1')

        self.assertTrue(pale.GetSourceAsset() is None)
        self.assertTrue(whiterPale.GetSourceCode() is None)

        # Test boundaries of parameter type-testing when connecting
        print("Test Typed Input Connections")

        colInput = pale.CreateInput("col1", Sdf.ValueTypeNames.Color3f)
        self.assertTrue(colInput)
        self.assertTrue(colInput.ConnectToSource(
            UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), 'colorOut', Output)))
        outputAttr = whiterPale.GetPrim().GetAttribute("outputs:colorOut")
        self.assertTrue(outputAttr)
        self.assertEqual(outputAttr.GetTypeName(), Sdf.ValueTypeNames.Color3f)

        v3fInput = pale.CreateInput("v3f1", Sdf.ValueTypeNames.Float3)
        self.assertTrue(v3fInput)
        self.assertTrue(v3fInput.ConnectToSource(
            UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), "colorOut", Output)))

        pointInput = pale.CreateInput("point1", Sdf.ValueTypeNames.Point3f)
        self.assertTrue(pointInput)
        self.assertTrue(pointInput.ConnectToSource(
            UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), "colorOut", Output)))

        floatInput = pale.CreateInput("float1", Sdf.ValueTypeNames.Float)
        self.assertTrue(floatInput)
        # XXX The following test must be disabled until we re-enable strict
        # type-checking for input / output connections.  See bug/113600
        # can't connect float to color!
        #with RequiredException(Tf.ErrorException):
        #    floatInput.ConnectToSource(
        #        UsdShade.ConnectionSourceInfo(whiterPale, "colorOut", Output))

        self.assertTrue(floatInput.ConnectToSource(
            UsdShade.ConnectionSourceInfo(whiterPale.ConnectableAPI(), "floatInput", Input)))
        outputAttr = whiterPale.GetPrim().GetAttribute("outputs:floatInput")
        self.assertFalse(outputAttr)
        outputAttr = whiterPale.GetPrim().GetAttribute("inputs:floatInput")
        self.assertTrue(outputAttr)

        print("Test Input Fetching")
        # test against single input fetches
        vecInput = pale.CreateInput('vec', Sdf.ValueTypeNames.Color3f)
        self.assertTrue(vecInput)
        self.assertTrue(pale.GetInput('vec'))
        self.assertEqual(pale.GetInput('vec').GetBaseName(), 'vec')
        self.assertEqual(pale.GetInput('vec').GetTypeName(), Sdf.ValueTypeNames.Color3f)
        self.assertTrue(pale.GetInput('vec').SetRenderType('foo'))
        self.assertEqual(pale.GetInput('vec').GetRenderType(), 'foo')

        # test against multiple input parameters.
        inputs = pale.GetInputs()

        # assure new item in collection
        self.assertEqual(len([pr for pr in inputs if pr.GetRenderType() == 'foo']),  1)

        # ensure the input count increments properly
        oldlen = len(pale.GetInputs())
        newparam = pale.CreateInput('struct', Sdf.ValueTypeNames.Color3f)

        # assure new item in collection
        self.assertEqual(len(pale.GetInputs()), (oldlen+1))

        # ensure by-value capture in 'inputs'
        self.assertNotEqual(len(pale.GetInputs()), len(inputs))

    def test_SdrMetadata(self):
        stage = self._SetupStage()

        ################################
        print ('Testing Shader Metadata API')
        ################################

        pale = UsdShade.Shader.Get(stage, palePath)
        self.assertTrue(pale)

        self.assertEqual(pale.GetSdrMetadata(), {})

        # Pale inherits from ClassPale.
        classPale = UsdShade.Shader.Get(stage, classPalePath)

        from pxr import Sdr
        baseSdrMetadata = {Sdr.NodeMetadata.Primvars : 
                                "primvarA|primvarB|primvarC"}
        classPale.SetSdrMetadata(baseSdrMetadata)

        self.assertEqual(pale.GetSdrMetadata(), baseSdrMetadata)
        paleSdrMetadata = {Sdr.NodeMetadata.Departments : "anim|layout",
                              Sdr.NodeMetadata.Category : "preview"}
        for i,j in paleSdrMetadata.items():
            pale.SetSdrMetadataByKey(i, j)

        self.assertEqual(pale.GetSdrMetadata(), 
            {'category': 'preview', 
             'primvars': 'primvarA|primvarB|primvarC', 
             'departments': 'anim|layout'})

        pale.ClearSdrMetadataByKey(Sdr.NodeMetadata.Primvars)
        self.assertEqual(pale.GetSdrMetadata(), 
            {'category': 'preview', 
             'primvars': 'primvarA|primvarB|primvarC', 
             'departments': 'anim|layout'})

        classPale.ClearSdrMetadataByKey(Sdr.NodeMetadata.Primvars)
        self.assertEqual(pale.GetSdrMetadata(), paleSdrMetadata)

        pale.ClearSdrMetadata()
        self.assertEqual(pale.GetSdrMetadata(), {})

    def test_ImplementationSource(self):
        stage = self._SetupStage()

        ################################
        print ('Testing Implementation Source API')
        ################################

        pale = UsdShade.Shader.Get(stage, palePath)
        self.assertTrue(pale)

        whiterPale = UsdShade.Shader.Get(stage, whiterPalePath)
        self.assertTrue(whiterPale)
        
        self.assertEqual(pale.GetImplementationSource(), UsdShade.Tokens.id)
        self.assertEqual(whiterPale.GetImplementationSource(), 
                         UsdShade.Tokens.id)

        self.assertTrue(pale.SetShaderId('SharedFloat_1'))
        self.assertEqual(pale.GetShaderId(), 'SharedFloat_1')

        self.assertTrue(whiterPale.SetShaderId('SharedColor_1'))
        self.assertEqual(whiterPale.GetShaderId(), 'SharedColor_1')

        pale.GetImplementationSourceAttr().Set(UsdShade.Tokens.sourceAsset)
        self.assertTrue(pale.GetShaderId() is None)

        whiterPale.GetImplementationSourceAttr().Set(UsdShade.Tokens.sourceCode)
        self.assertTrue(whiterPale.GetShaderId() is None)
    
        glslfxSource = "This is the shader source"
        self.assertTrue(pale.SetSourceCode(sourceCode=glslfxSource, 
                                           sourceType="glslfx"))

        # Calling SetSourceCode() updates the implementationSource to 'code'.
        self.assertEqual(pale.GetImplementationSource(), 
                         UsdShade.Tokens.sourceCode)

        self.assertTrue(pale.GetShaderId() is None)

        self.assertTrue(pale.GetSourceAsset() is None)
        self.assertTrue(pale.GetSourceAsset(sourceType="glslfx") is None)

        self.assertTrue(pale.GetSourceCode(sourceType="osl") is None)
        self.assertTrue(pale.GetSourceCode() is None)

        self.assertEqual(pale.GetSourceCode(sourceType="glslfx"), glslfxSource)

        oslAssetPath = Sdf.AssetPath("/source/asset.osl")
        self.assertTrue(whiterPale.SetSourceAsset(
                sourceAsset=oslAssetPath, 
                sourceType=UsdShade.Tokens.universalSourceType))

        # Calling SetSourceAsset() updates the implementationSource to 'asset'.
        self.assertEqual(whiterPale.GetImplementationSource(), 
                         UsdShade.Tokens.sourceAsset)

        self.assertTrue(whiterPale.GetShaderId() is None)

        # Since the sourceAsset was set with universal sourceType, we can fetch 
        # it successfully irrespective of the sourceType that's passed in.
        self.assertEqual(whiterPale.GetSourceAsset(sourceType="osl"), 
                         oslAssetPath)
        self.assertTrue(whiterPale.GetSourceAsset(sourceType="glslfx"), 
                        oslAssetPath)
        self.assertEqual(whiterPale.GetSourceAsset(), oslAssetPath)

        self.assertTrue(whiterPale.GetSourceCode() is None)
        self.assertTrue(whiterPale.GetSourceCode(sourceType="osl") is None)

        # Set another sourceAsset corresponding to a specific sourceType.
        glslfxAssetPath = Sdf.AssetPath("/source/asset.glslfx")
        self.assertTrue(whiterPale.SetSourceAsset(
                sourceAsset=glslfxAssetPath, 
                sourceType="glslfx"))
        self.assertEqual(whiterPale.GetSourceAsset(sourceType="osl"), 
                         oslAssetPath)
        self.assertTrue(whiterPale.GetSourceAsset(sourceType="glslfx"), 
                        glslfxAssetPath)
        self.assertEqual(whiterPale.GetSourceAsset(), oslAssetPath)

        # Test getting a sub identifier before it has been set
        self.assertTrue(whiterPale.GetSourceAssetSubIdentifier() is None)
        self.assertTrue(
            whiterPale.GetSourceAssetSubIdentifier(sourceType="glslfx") is None)

        # Reset implementation source to not be 'sourceAsset'
        whiterPale.GetImplementationSourceAttr().Set(UsdShade.Tokens.id)
        self.assertEqual(whiterPale.GetImplementationSource(),
                         UsdShade.Tokens.id)

        # Check that calling SetSourceAssetSubIdentifier updates
        # implementationSource to 'asset;
        subId = "mySubIdentifier"
        self.assertTrue(whiterPale.SetSourceAssetSubIdentifier(
            subIdentifier=subId,
            sourceType=UsdShade.Tokens.universalSourceType))
        self.assertEqual(whiterPale.GetSourceAssetSubIdentifier(
            sourceType=UsdShade.Tokens.universalSourceType), subId)
        self.assertEqual(whiterPale.GetImplementationSource(),
                         UsdShade.Tokens.sourceAsset)

        # Test that setting a source asset and sub identifier will update the
        # correct attributes for a variety source types.
        sourceAsset = Sdf.AssetPath("someSourceAsset")

        sourceTypes = [UsdShade.Tokens.universalSourceType, "osl"]
        subIds = ["myUniversalSubIdentifier", "myOSLSubIdentifier"]

        for sourceType, subId in zip(sourceTypes, subIds):
            self.assertTrue(whiterPale.SetSourceAsset(
                sourceAsset=sourceAsset,
                sourceType=sourceType))
            self.assertTrue(whiterPale.SetSourceAssetSubIdentifier(
                subIdentifier=subId,
                sourceType=sourceType))
            self.assertEqual(whiterPale.GetSourceAssetSubIdentifier(sourceType),
                             subId)

    def testGetSourceTypes(self):
        stage = self._SetupStage()

        ################################
        print ('Testing Get Source Types API')
        ################################

        pale = UsdShade.Shader.Get(stage, palePath)
        self.assertTrue(pale)

        self.assertEqual(pale.GetImplementationSource(), UsdShade.Tokens.id)

        self.assertTrue(pale.SetShaderId('SharedFloat_1'))
        self.assertEqual(pale.GetShaderId(), 'SharedFloat_1')

        pale.GetImplementationSourceAttr().Set(UsdShade.Tokens.sourceCode)
        self.assertTrue(pale.GetShaderId() is None)

        self.assertEqual(pale.GetSourceTypes(), [])

        # Set sourceType for a sourceCode implementation.
        oslSource = "This is the shader source"
        self.assertTrue(pale.SetSourceCode(sourceCode=oslSource, 
                                           sourceType="osl"))
        self.assertEqual(pale.GetSourceTypes(), ["osl"])

        # Check if we can detect multiple sourceTypes per implementation
        glslfxSource = "This is the shader source"
        self.assertTrue(pale.SetSourceCode(sourceCode=glslfxSource,
                                           sourceType="glslfx"))
        self.assertEqual(sorted(pale.GetSourceTypes()),
                         ["glslfx", "osl"])

        # Set sourceType for sourceAsset implmentation.
        pale.GetImplementationSourceAttr().Set(UsdShade.Tokens.sourceAsset)
        glslfxAssetPath = Sdf.AssetPath("/source/asset.glslfx")
        self.assertTrue(pale.SetSourceAsset(
                sourceAsset=glslfxAssetPath, 
                sourceType="glslfx"))
        
        self.assertEqual(pale.GetSourceTypes(), ["glslfx"])


if __name__ == '__main__':
    unittest.main()
