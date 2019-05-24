# -*- coding: utf-8 -*-

import os
import pkg_resources
from typing import Dict

from bag.design import Module


yaml_file = pkg_resources.resource_filename(__name__, os.path.join('netlist_info', 'filter.yaml'))


# noinspection PyPep8Naming
class bag240__filter(Module):
    """Module for library bag240 cell filter.

    Fill in high level description here.
    """

    def __init__(self, bag_config, parent=None, prj=None, **kwargs):
        Module.__init__(self, bag_config, yaml_file, parent=parent, prj=prj, **kwargs)

    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            mos_l = 'Channel length',
            mos_w='transistor width',
            mos_nf='number of fingers',
            mos_intent='threshold option',
            impl_lib='implementation library',
            R='resistors',
            baseC='base capacitance, usually 1',
            C='capacitance',
            fc='filter cutoff frequency'
        )

    def design(self,mos_l, mos_w, mos_nf, mos_intent, impl_lib, R, baseC, C, fc,**kwargs):
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        local_dict = locals()
        # print("Generating filter...")
        self.replace_instance_master('OPAMP1', impl_lib, 'opamp_wrap', static='TRUE')
        self.replace_instance_master('OPAMP2', impl_lib, 'opamp_wrap', static='TRUE')
        # self.instances['OPAMP1'].design(impl_lib, mos_l, mos_w, mos_nf, mos_intent)
        # self.instances['OPAMP2'].design(impl_lib, mos_l, mos_w, mos_nf, mos_intent)
        pass
