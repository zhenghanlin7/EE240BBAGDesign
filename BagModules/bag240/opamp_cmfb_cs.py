# -*- coding: utf-8 -*-

import os
import pkg_resources
from typing import Dict

from bag.design import Module


yaml_file = pkg_resources.resource_filename(__name__, os.path.join('netlist_info', 'opamp_cmfb_cs.yaml'))


# noinspection PyPep8Naming
class bag240__opamp_cmfb_cs(Module):
    """Module for library bag240 cell opamp_cmfb_cs.

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
            mos_w = 'transistor width',
            mos_nf_pin = 'number of fingers -pmos input pair',
            mos_nf_nload = 'number of fingers -nmos load',
            mos_nf_pcm= 'number of fingers -pmos current mirror',
            mos_intent = 'threshold option'
        )

    def design(self, mos_l, mos_w, mos_nf_pin, mos_nf_nload, mos_nf_pcm, mos_intent, **kwargs):
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
        self.instances['PM3'].design(l=mos_l, w=mos_w, nf=mos_nf_pin, intent=mos_intent)
        self.instances['PM5'].design(l=mos_l, w=mos_w, nf=mos_nf_pin, intent=mos_intent)
        self.instances['PM9'].design(l=mos_l, w=mos_w, nf=mos_nf_pcm, intent=mos_intent)
        self.instances['NM11'].design(l=mos_l, w=mos_w, nf=mos_nf_nload, intent=mos_intent)
        self.instances['NM10'].design(l=mos_l, w=mos_w, nf=mos_nf_nload, intent=mos_intent)

