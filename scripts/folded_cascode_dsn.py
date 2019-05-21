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


def simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params):

    # generate tb schematic
    print("Generating testbench ...")
    dsn = prj.create_design_module(temp_lib, tb_name)
    dsn.design(impl_lib=impl_lib, cell_name=cell_name)
    dsn.implement_design(impl_lib, top_cell_name=tb_name)

    # configure tb
    tb = prj.configure_testbench(tb_lib=impl_lib, tb_cell=tb_name)
<<<<<<< HEAD
    tb.set_parameter('vdd', sim_params[0])
    tb.set_parameter('Rsense', sim_params[1])
    tb.add_output('imag', """imag(VF("/voutp") - VF("/voutn"))""")
=======
    tb.set_parameter('Rsense',sim_params['Rsense'])
>>>>>>> zhenghan
    tb.update_testbench()

    # rum simulation
    tb.run_simulation()
    print(tb.save_dir)

    print("Hi")

    print(results)

    print("Hi2")

    # Get results
<<<<<<< HEAD
    gain = results['gain']
    phase = results['phase']
    freq = results['freq']
    real = results['imag']
    return gain, phase, real, freq
=======
    results = load_sim_results(tb.save_dir)

    #print(results)
    print('Gain=',results['dc_gain'])
    print('BW=', results['band_width']/(10**6),'MHz')
    print('GBW=', results['unity_gain']/(10**9), 'GHz')
    print('PM=', results['phase_margin'])
    gain = results['amp_gain']
    phase = results['amp_phase']
    freq = results['freq']
    return gain, phase, freq
>>>>>>> zhenghan


def design(prj, temp_lib, impl_lib, tb_name, cell_name, sch_params):

    print("Simulating ...")

    generate(prj, temp_lib, impl_lib, cell_name, sch_params)
<<<<<<< HEAD

    gain, phase, real, freq = simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params=[1.2, 5e3])

    plt.figure()
    plt.subplot(3,1,1)
    plt.semilogx(freq,gain,'r')

    plt.subplot(3,1,2)
    plt.semilogx(freq,phase,'y')

    plt.subplot(3,1,3)
    plt.semilogx(freq,real,'b')

=======
    sim_params = {'Rsense': 5000}

    gain, phase, freq = simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params, show_plot=False)

    plt.figure()
    plt.subplot(2,1,1)
    plt.semilogx(freq,gain)
    plt.subplot(2,1,2)
    plt.semilogx(freq,gain)
>>>>>>> zhenghan
    plt.show(block=False)


if __name__ is '__main__':

    if 'bprj' not in locals():
        bprj = bag.BagProject()
    #comment

    impl_lib = 'bag240_generated'
    temp_lib = 'bag240'
    cell_name = 'opamp_folded_cascode'
    tb_name = 'tb_opamp_folded_cascode'

    sch_params = dict(
        mos_l={'L_in':400e-9, 'L_N':300e-9, 'L_P':300e-9},
        mos_w={'W_in':480e-9, 'W_N':360e-9, 'W_P':360e-9},
        mos_nf={'N_in':58, 'N_P':6, 'N_PCAS': 6, 'N_NCAS':6, 'N_N':36, 'N_OS':60, 'N_OSL':20},
        mos_intent='svt'
    )

    design(bprj, temp_lib, impl_lib, tb_name, cell_name, sch_params)

