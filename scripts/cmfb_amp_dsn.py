import bag
from bag.data import load_sim_results
from scripts_char.mos_query import get_db
import pprint
import matplotlib.pyplot as plt


def generate(prj, temp_lib, impl_lib, cell_name, sch_params):

    print("Generating schematic ...")
    dsn = prj.create_design_module(temp_lib, cell_name)
    dsn.design(**sch_params)
    dsn.implement_design(impl_lib, top_cell_name=cell_name)


def simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params, show_plot=True):

    # generate tb schematic
    print("Generating testbench ...")

    dsn = prj.create_design_module(temp_lib, tb_name)
    dsn.design(impl_lib=impl_lib, cell_name=cell_name)
    dsn.implement_design(impl_lib, top_cell_name=tb_name)

    # configure tb
    tb = prj.configure_testbench(tb_lib=impl_lib, tb_cell=tb_name)
    tb.set_parameter('vdd', sim_params[0])
    tb.update_testbench()

    # rum simulation
    tb.run_simulation()
    print(tb.save_dir)
    results = load_sim_results(tb.save_dir)

    gain = results['gain']
    freq = results['freq']
    return gain, freq


def design(prj, temp_lib, impl_lib, tb_name, cell_name, sch_params):

    print("Simulating ...")

    generate(prj, temp_lib, impl_lib, cell_name, sch_params)

    gain, freq = simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params=[1.2], show_plot=False)

    plt.figure()
    plt.semilogx(freq,gain)
    plt.show(block=True)


if __name__ is '__main__':

    if 'bprj' not in locals():
        bprj = bag.BagProject()

    impl_lib = 'bag240_generated'
    temp_lib = 'bag240'
    cell_name = 'opamp_cmfb_cs'
    tb_name = 'tb_opamp_cmfb_cs'

    sch_params = dict(
        mos_l=300e-9,
        mos_w=360e-9,
        mos_nf_pin=18,
        mos_nf_nload=10,
        mos_nf_pcm=54,
        mos_intent='svt'
    )

    design(bprj, temp_lib, impl_lib, tb_name, cell_name, sch_params)

