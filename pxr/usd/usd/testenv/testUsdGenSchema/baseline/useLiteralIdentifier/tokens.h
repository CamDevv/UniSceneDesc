//
// Copyright 2016 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
#ifndef USDCONTRIVED_TOKENS_H
#define USDCONTRIVED_TOKENS_H

/// \file usdContrived/tokens.h

// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
// 
// This is an automatically generated file (by usdGenSchema.py).
// Do not hand-edit!
// 
// XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#include "pxr/pxr.h"
#include "pxr/usd/usdContrived/api.h"
#include "pxr/base/tf/staticData.h"
#include "pxr/base/tf/token.h"
#include <vector>

PXR_NAMESPACE_OPEN_SCOPE


/// \class UsdContrivedTokensType
///
/// \link UsdContrivedTokens \endlink provides static, efficient
/// \link TfToken TfTokens\endlink for use in all public USD API.
///
/// These tokens are auto-generated from the module's schema, representing
/// property names, for when you need to fetch an attribute or relationship
/// directly by name, e.g. UsdPrim::GetAttribute(), in the most efficient
/// manner, and allow the compiler to verify that you spelled the name
/// correctly.
///
/// UsdContrivedTokens also contains all of the \em allowedTokens values
/// declared for schema builtin attributes of 'token' scene description type.
/// Use UsdContrivedTokens like so:
///
/// \code
///     gprim.GetMyTokenValuedAttr().Set(UsdContrivedTokens->libraryToken1);
/// \endcode
struct UsdContrivedTokensType {
    USDCONTRIVED_API UsdContrivedTokensType();
    /// \brief "libraryToken1"
    /// 
    /// Special token for the usdContrived library.
    const TfToken libraryToken1;
    /// \brief "/non-identifier-tokenValue!"
    /// 
    /// libraryToken2 doc
    const TfToken libraryToken2;
    /// \brief "myColorFloat"
    /// 
    /// UsdContrivedBase
    const TfToken myColorFloat;
    /// \brief "myDouble"
    /// 
    /// UsdContrivedBase
    const TfToken myDouble;
    /// \brief "myFloat"
    /// 
    /// UsdContrivedBase
    const TfToken myFloat;
    /// \brief "myNormals"
    /// 
    /// UsdContrivedBase
    const TfToken myNormals;
    /// \brief "myPoints"
    /// 
    /// UsdContrivedBase
    const TfToken myPoints;
    /// \brief "myVaryingToken"
    /// 
    /// UsdContrivedBase
    const TfToken myVaryingToken;
    /// \brief "myVaryingTokenArray"
    /// 
    /// UsdContrivedBase
    const TfToken myVaryingTokenArray;
    /// \brief "myVelocities"
    /// 
    /// UsdContrivedBase
    const TfToken myVelocities;
    /// \brief "unsignedChar"
    /// 
    /// UsdContrivedBase
    const TfToken unsignedChar;
    /// \brief "unsignedInt"
    /// 
    /// UsdContrivedBase
    const TfToken unsignedInt;
    /// \brief "unsignedInt64Array"
    /// 
    /// UsdContrivedBase
    const TfToken unsignedInt64Array;
    /// \brief "VariableTokenAllowed1"
    /// 
    /// Possible value for UsdContrivedBase::GetMyVaryingTokenAttr()
    const TfToken variableTokenAllowed1;
    /// \brief "VariableTokenAllowed2"
    /// 
    /// Possible value for UsdContrivedBase::GetMyVaryingTokenAttr()
    const TfToken variableTokenAllowed2;
    /// \brief "VariableTokenAllowed<3>"
    /// 
    /// Possible value for UsdContrivedBase::GetMyVaryingTokenAttr()
    const TfToken variableTokenAllowed3;
    /// \brief "VariableTokenArrayAllowed1"
    /// 
    /// Possible value for UsdContrivedBase::GetMyVaryingTokenArrayAttr()
    const TfToken variableTokenArrayAllowed1;
    /// \brief "VariableTokenArrayAllowed2"
    /// 
    /// Possible value for UsdContrivedBase::GetMyVaryingTokenArrayAttr()
    const TfToken variableTokenArrayAllowed2;
    /// \brief "VariableTokenArrayAllowed<3>"
    /// 
    /// Possible value for UsdContrivedBase::GetMyVaryingTokenArrayAttr()
    const TfToken variableTokenArrayAllowed3;
    /// \brief "VariableTokenDefault"
    /// 
    /// Fallback value for UsdContrivedBase::GetMyVaryingTokenAttr()
    const TfToken variableTokenDefault;
    /// \brief "Base"
    /// 
    /// Schema identifer and family for UsdContrivedBase
    const TfToken Base;
    /// A vector of all of the tokens listed above.
    const std::vector<TfToken> allTokens;
};

/// \var UsdContrivedTokens
///
/// A global variable with static, efficient \link TfToken TfTokens\endlink
/// for use in all public USD API.  \sa UsdContrivedTokensType
extern USDCONTRIVED_API TfStaticData<UsdContrivedTokensType> UsdContrivedTokens;

PXR_NAMESPACE_CLOSE_SCOPE

#endif
