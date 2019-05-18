# -*- coding: utf-8 -*-

import os
import pkg_resources
from typing import Dict

from bag.design import Module


yaml_file = pkg_resources.resource_filename(__name__, os.path.join('netlist_info', 'tb_opamp_folded_cascode.yaml'))


# noinspection PyPep8Naming
class bag240__tb_opamp_folded_cascode(Module):
    """Module for library bag240 cell tb_opamp_folded_cascode.

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
            impl_lib = 'implementation library',
            cell_name = 'cell name'
        )

    def design(self,impl_lib, cell_name):
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
        self.instances['I6'].design()
        self.replace_instance_master('I4', impl_lib, 'opamp_cmfb_cs', static='TRUE')
        self.replace_instance_master('I0', impl_lib, cell_name, static='TRUE')
