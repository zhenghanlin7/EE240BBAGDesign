# -*- coding: utf-8 -*-

import os
import pkg_resources
from typing import Dict

from bag.design import Module


yaml_file = pkg_resources.resource_filename(__name__, os.path.join('netlist_info', 'opamp_wrap.yaml'))


# noinspection PyPep8Naming
class bag240__opamp_wrap(Module):
    """Module for library bag240 cell opamp_wrap.

    Fill in high level description here.
    """

    def __init__(self, bag_config, parent=None, prj=None, **kwargs):
<<<<<<< HEAD
=======
        print("Initializing Opamp_wrap...")
>>>>>>> yikuan
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
<<<<<<< HEAD
        )

    def design(self):
=======

        )

    def design(self, impl_lib, mos_l, mos_w, mos_nf, mos_intent, **kwargs):
>>>>>>> yikuan
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
<<<<<<< HEAD
        pass
=======
        local_dict = locals()
        print("Generating Opamp_wrap...")
        self.replace_instance_master('I4', impl_lib, 'opamp_cmfb_cs', static='TRUE')
        self.replace_instance_master('I0', impl_lib, 'opamp_folded_cascode', static='TRUE')
        #self.instances['I0'].design(mos_l, mos_w, mos_nf, mos_intent)

>>>>>>> yikuan
