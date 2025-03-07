set(PXR_PREFIX pxr/base)
set(PXR_PACKAGE vt)

pxr_library(vt
    LIBRARIES
        arch
        tf
        gf
        trace
        ${TBB_tbb_LIBRARY}

    INCLUDE_DIRS
        ${TBB_INCLUDE_DIRS}

    PUBLIC_CLASSES
        array
        dictionary
        hash
        streamOut
        types
        value

    PYTHON_PUBLIC_CLASSES
        arrayPyBuffer
        valueFromPython
        wrapArray

    PUBLIC_HEADERS
        api.h
        traits.h
        typeHeaders.h
        visitValue.h
    
    PYTHON_PUBLIC_HEADERS
        pyOperators.h

    PYTHON_CPPFILES
        moduleDeps.cpp

    PYMODULE_CPPFILES
        module.cpp
        wrapArrayBase.cpp
        wrapArrayDualQuaternion.cpp
        wrapArrayFloat.cpp
        wrapArrayIntegral.cpp
        wrapArrayMatrix.cpp
        wrapArrayQuaternion.cpp
        wrapArrayRange.cpp
        wrapArrayString.cpp
        wrapArrayToken.cpp
        wrapArrayVec.cpp
        wrapDictionary.cpp
        wrapValue.cpp

    PYMODULE_FILES
        __init__.py

    DOXYGEN_FILES
        overview.dox
)

pxr_build_test(testVtCpp
    LIBRARIES
        tf
        gf
        vt
    CPPFILES
        testenv/testVtCpp.cpp
)
pxr_test_scripts(
    testenv/testVtArray.py
    testenv/testVtValue.py
)
pxr_register_test(testVtValue
    PYTHON
    COMMAND "${CMAKE_INSTALL_PREFIX}/tests/testVtValue"
)
pxr_register_test(testVtArray
    PYTHON
    COMMAND "${CMAKE_INSTALL_PREFIX}/tests/testVtArray"
)
pxr_register_test(testVtCpp
    COMMAND "${CMAKE_INSTALL_PREFIX}/tests/testVtCpp"
)
