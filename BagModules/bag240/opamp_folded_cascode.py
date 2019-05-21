# -*- coding: utf-8 -*-

import os
import pkg_resources
from typing import Dict

from bag.design import Module


yaml_file = pkg_resources.resource_filename(__name__, os.path.join('netlist_info', 'opamp_folded_cascode.yaml'))


# noinspection PyPep8Naming
class bag240__opamp_folded_cascode(Module):
    """Module for library bag240 cell opamp_folded_cascode.

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
            mos_intent='threshold option'
        )

    def design(self, mos_l, mos_w, mos_nf, mos_intent, **kwargs):
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
        print("Generating folded cascode main amp...")
        self.instances['PMINN'].design(l=mos_l['L_in'], w=mos_w['W_in'], nf=mos_nf['N_in'], intent=mos_intent)
        self.instances['PMINP'].design(l=mos_l['L_in'], w=mos_w['W_in'], nf=mos_nf['N_in'], intent=mos_intent)
        self.instances['PMCM'].design(l=mos_l['L_in'], w=mos_w['W_P'], nf=2*mos_nf['N_in'], intent=mos_intent)
        self.instances['PM0L'].design(l=mos_l['L_P'], w=mos_w['W_P'], nf=mos_nf['N_P'], intent=mos_intent)
        self.instances['PM0R'].design(l=mos_l['L_P'], w=mos_w['W_P'], nf=mos_nf['N_P'], intent=mos_intent)
        self.instances['PM1L'].design(l=mos_l['L_P'], w=mos_w['W_P'], nf=mos_nf['N_PCAS'], intent=mos_intent)
        self.instances['PM1R'].design(l=mos_l['L_P'], w=mos_w['W_P'], nf=mos_nf['N_PCAS'], intent=mos_intent)
        self.instances['NM0L'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_N'], intent=mos_intent)
        self.instances['NM0R'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_N'], intent=mos_intent)
        self.instances['NM1L'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_NCAS'], intent=mos_intent)
        self.instances['NM1R'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_NCAS'], intent=mos_intent)
        self.instances['NMSF0L'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_OSL'], intent=mos_intent)
        self.instances['NMSF0R'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_OSL'], intent=mos_intent)
        self.instances['NMSF1L'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_OS'], intent=mos_intent)
        self.instances['NMSF1R'].design(l=mos_l['L_N'], w=mos_w['W_N'], nf=mos_nf['N_OS'], intent=mos_intent)