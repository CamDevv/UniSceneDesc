/*
 * Copyright (c) 2016, Alliance for Open Media. All rights reserved
 *
 * This source code is subject to the terms of the BSD 2 Clause License and
 * the Alliance for Open Media Patent License 1.0. If the BSD 2 Clause License
 * was not distributed with this source code in the LICENSE file, you can
 * obtain it at www.aomedia.org/license/software. If the Alliance for Open
 * Media Patent License 1.0 was not distributed with this source code in the
 * PATENTS file, you can obtain it at www.aomedia.org/license/patent.
 */
#include "pxr/imaging/plugin/hioAvif/aom/config/aom_config.h"

#define RTCD_C
#include "pxr/imaging/plugin/hioAvif/aom/config/aom_scale_rtcd.h"

#include "pxr/imaging/plugin/hioAvif/aom/aom_ports/aom_once.h"

void aom_scale_rtcd() { aom_once(setup_rtcd_internal); }
