# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/

import typing as ty

from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.ports.ports import InPort, OutPort


class EventsToFrame(AbstractProcess):
    """Process that transforms a collection of (sparse) events into a (dense)
    frame.

    Output shape can be either (W, H, 1) or (W, H, 2).
        (1) If output shape is (W, H, 1), input is assumed to be unary.
        (2) If output shape is (W, H, 2), input is assumed to be binary.
        Negative events are represented by 1s in first channel.
        Positive events are represented by 1s in second channel.

    Parameters
    ----------
    shape_in : tuple(int)
        Shape of InPort.
    shape_out : tuple(int, int, int)
        Shape of OutPort.
    """
    def __init__(self,
                 *,
                 shape_in: ty.Tuple[int],
                 shape_out: ty.Tuple[int, int, int],
                 **kwargs) -> None:
        super().__init__(shape_in=shape_in,
                         shape_out=shape_out,
                         **kwargs)

        self._validate_shape_in(shape_in)
        self._validate_shape_out(shape_out)

        self.in_port = InPort(shape=shape_in)
        self.out_port = OutPort(shape=shape_out)

    @staticmethod
    def _validate_shape_in(shape_in: ty.Tuple[int]) -> None:
        """Validate that a given shape is of the form (max_num_events, ) where
        max_num_events is strictly positive.

        Parameters
        ----------
        shape_in : tuple(int)
            Shape to validate.
        """
        if len(shape_in) != 1:
            raise ValueError(f"Expected shape_in to be of the form "
                             f"(max_num_events, ). "
                             f"Found {shape_in=}.")

        if shape_in[0] <= 0:
            raise ValueError(f"Expected max number of events "
                             f"(first element of shape_in) to be strictly "
                             f"positive. "
                             f"Found {shape_in=}.")

    @staticmethod
    def _validate_shape_out(shape_out: ty.Tuple[int, int, int]) -> None:
        """Validate that a given shape is of the form (W, H, C) where W and H
        are strictly positive and C either 1 or 2.

        Parameters
        ----------
        shape_out : tuple(int, int, int)
            Shape to validate.
        """
        if not len(shape_out) == 3:
            raise ValueError(f"Expected shape_out to be 3D. "
                             f"Found {shape_out=}.")

        if not (shape_out[2] == 1 or shape_out[2] == 2):
            raise ValueError(f"Expected number of channels "
                             f"(third element of shape_out) to be either "
                             f"1 or 2. "
                             f"Found {shape_out=}.")

        if shape_out[0] <= 0 or shape_out[1] <= 0:
            raise ValueError(f"Expected width and height "
                             f"(first and second elements of shape_out) to be "
                             f"strictly positive. "
                             f"Found {shape_out=}.")