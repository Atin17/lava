# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/

import numpy as np
import typing as ty
import warnings


def sub_sample(data: np.ndarray,
               indices: np.ndarray,
               max_events: int,
               random_rng: ty.Optional[np.random.Generator] = None) \
        -> ty.Tuple[np.ndarray, np.ndarray]:

    data_idx_array = np.arange(0, data.shape[0])
    sampled_idx = random_rng.choice(data_idx_array,
                                    max_events,
                                    replace=False)

    percentage_data_lost = (1 - max_events/data.shape[0])*100
    warnings.warn(f"Read {data.shape[0]} events. Maximum number of events is {max_events}. "
                  f"Removed {data.shape[0] - max_events} ({percentage_data_lost:.1f}%) events by subsampling.")

    return data[sampled_idx], indices[sampled_idx]