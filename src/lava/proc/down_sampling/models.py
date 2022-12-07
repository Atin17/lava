# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/

import numpy as np
from numpy.lib.stride_tricks import as_strided

from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.model.py.ports import PyInPort, PyOutPort
from lava.magma.core.model.py.type import LavaPyType
from lava.magma.core.resources import CPU
from lava.magma.core.decorator import implements, requires
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.proc.down_sampling.process import DownSampling
from lava.proc.conv import utils


@implements(proc=DownSampling, protocol=LoihiProtocol)
@requires(CPU)
class DownSamplingPM(PyLoihiProcessModel):
    in_port: PyInPort = LavaPyType(PyInPort.VEC_DENSE, int)
    out_port: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, int)

    stride: np.ndarray = LavaPyType(np.ndarray, np.int8, precision=8)
    padding: np.ndarray = LavaPyType(np.ndarray, np.int8, precision=8)

    def run_spk(self) -> None:
        data = self.in_port.recv()

        down_sampled_data = self._down_sample(data)

        self.out_port.send(down_sampled_data)

    def _down_sample(self, data: np.ndarray) -> np.ndarray:
        output_shape = self.out_port.shape

        padded_data = np.pad(data,
                             (utils.make_tuple(self.padding[0]),
                              utils.make_tuple(self.padding[1])),
                             mode='constant')

        strides_w = (self.stride[0] * data.strides[0],
                     self.stride[1] * data.strides[1])

        down_sampled_data = as_strided(padded_data, output_shape, strides_w)

        return down_sampled_data
