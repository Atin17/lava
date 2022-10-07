from lava.magma.core.process.ports.ports import OutPort
from lava.magma.core.process.process import AbstractProcess

class NeuronProcess(AbstractProcess):
    def __init__(self,
                 shape: tuple = (1, ),
                 enable_learning: bool = False,
                 update_traces = None,
                 *args,
                 **kwargs):

        kwargs['enable_learning'] = enable_learning
        kwargs['shape'] = shape
        kwargs['update_traces'] = update_traces

        self.enable_learning = enable_learning

        # Learning Ports
        self.s_out_bap = OutPort(shape=(shape[0],)) # Port for backprop action potentials
        self.s_out_y2 = OutPort(shape=(shape[0],)) # Port for arbitrary trace using graded spikes {shape=shape?}
        self.s_out_y3 = OutPort(shape=(shape[0],)) # Port for arbitrary trace using graded spikes

        super().__init__(*args, **kwargs)

