import bag
import numpy as np
from bag.data import load_sim_results
from scripts_char.mos_query import get_db
import pprint
import matplotlib.pyplot as plt


def generate(prj, temp_lib, impl_lib, cell_name, sch_params):

    print("Generating schematic ...")
    dsn = prj.create_design_module(temp_lib, cell_name)
    dsn.design(impl_lib=impl_lib,**sch_params)
    dsn.implement_design(impl_lib, top_cell_name=cell_name)


def simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params, show_plot=True):

    # generate tb schematic
    print("Generating testbench ...")
    dsn = prj.create_design_module(temp_lib, tb_name)
    dsn.design(impl_lib=impl_lib, cell_name=cell_name)
    dsn.implement_design(impl_lib, top_cell_name=tb_name)

    # configure tb
    tb = prj.configure_testbench(tb_lib=impl_lib, tb_cell=tb_name)

    scale_ratio = sim_params['scale_ratio']
    print("Running simulation... scale ratio is",scale_ratio)
    tb.set_parameter('R1A', sim_params['rc']['R']['1A']/scale_ratio)
    tb.set_parameter('R2A', sim_params['rc']['R']['2A']/scale_ratio)
    tb.set_parameter('R3A', sim_params['rc']['R']['3A']/scale_ratio)
    tb.set_parameter('R1B', sim_params['rc']['R']['1B']/scale_ratio)
    tb.set_parameter('R2B', sim_params['rc']['R']['2B']/scale_ratio)
    tb.set_parameter('R3B', sim_params['rc']['R']['3B']/scale_ratio)
    tb.set_parameter('C1A', sim_params['rc']['C']['1A']*scale_ratio)
    tb.set_parameter('C1B', sim_params['rc']['C']['1B']*scale_ratio)
    tb.set_parameter('C2A', sim_params['rc']['C']['2A']*scale_ratio)
    tb.set_parameter('C2B', sim_params['rc']['C']['2B']*scale_ratio)
    # not completed yet...

    tb.update_testbench()

    # rum simulation
    tb.run_simulation()
    print(tb.save_dir)
    results = load_sim_results(tb.save_dir)

    # Get results
    gain = results['vodm_dB']
    freq = results['freq']
    int_noise = results['int_noise']
    R2_noise = results['R2_noise']
    NM0_noise = results['NM0_noise']
    print("NM0_noise is ",NM0_noise, "R2_noise is",R2_noise)
    flag = 1
    if(R2_noise > NM0_noise):
        flag = 0
    return gain, freq, int_noise, flag


def design(prj, temp_lib, impl_lib, tb_name, cell_name, sch_params):

    print("Simulating ...")

    rc = get_rc_param(sch_params['fc'],sch_params['C']['1A'])
    print(rc)
    input("hey, is the RC right?")

    sch_params['R']=rc['R']
    sch_params['C']=rc['C']

    print(sch_params['R'])
    input("hey, is the R right?")

    generate(prj, temp_lib, impl_lib, cell_name, sch_params)

    int_noise = 5.1e-8 # just an initial value
    scale_ratio = 1    # R_final = R/scale ratio, C_final = C*scale ratio
    sim_params = {'scale_ratio': scale_ratio,'rc':rc}
    scale_ratio_list = []
    int_noise_list = []
    i = 0
    while int_noise > 5e-10:
        gain, freq,  int_noise, flag = \
            simulate(prj, temp_lib, impl_lib, tb_name, cell_name, sim_params, show_plot=False)

        # add to lists
        scale_ratio_list.append(scale_ratio)
        int_noise_list.append(int_noise)
        i = i+1
        print("Output integrated noise is ", int_noise," @ scale ratio is", scale_ratio)

        # change scaling ratio
        scale_ratio = scale_ratio * 1.189 # 2^(1/4)
        sim_params = {'scale_ratio': scale_ratio, 'rc': rc}
        #if(i>1 and ((int_noise_list[i-1]-int_noise)/(int_noise_list[i-1]) < 0.05)):
        if(flag == 1): #transistor noise surpasses resistor noise
            print("Output integrated noise is ", int_noise," @ scale ratio is", scale_ratio, \
            "stop scaling RC, resizing transistors...")

            break;


    plt.figure()
    plt.semilogx(scale_ratio_list,int_noise_list)
    plt.title('Scaling ratio vs noise power (V^2)')
    plt.show(block=True)

def get_rc_param(fc, C_1):

    print("Calculating RC values for Bessel LPF, fc=",fc/1000000,"MHz.")

    # params for bessel filter
    Q_A    = 0.5219
    Q_B    = 0.8055
    FSF_A  = 1.4192
    FSF_B  = 1.5912
    M      = 0.75

    N_A    = 2.26
    N_B    = 5.36

    # C_1 is same for both stages, may change depending on noise spec

    R_1A = 1 / (FSF_A * fc * 2*3.1415926*C_1 * np.sqrt(N_A * M))
    R_2A = R_1A
    R_3A = M * R_1A
    C_2A = N_A * C_1 * 2

    R_1B = 1 / (FSF_B * fc * 2*3.1415926*C_1 * np.sqrt(N_B * M))
    R_2B = R_1B
    R_3B = M * R_1B
    C_2B = N_B * C_1
    # print(R_1A,R_3A)

    return dict(
        R = {'1A': R_1A, '2A': R_2A, '3A': R_3A, '1B': R_1B, '2B': R_2B, '3B': R_3B},
        C = {'1A': C_1, '2A': C_2A, '1B': C_1, '2B':C_2B}
    )



if __name__ is '__main__':

    if 'bprj' not in locals():
        bprj = bag.BagProject()

    impl_lib = 'bag240_generated'
    temp_lib = 'bag240'
    cell_name = 'filter'
    tb_name = 'tb_filter'

    sch_params = dict(
        mos_l={'L_in':400e-9, 'L_N':300e-9, 'L_P':300e-9},
        mos_w={'W_in':480e-9, 'W_N':360e-9, 'W_P':360e-9},
        mos_nf={'N_in':58, 'N_P':6, 'N_PCAS': 6, 'N_NCAS':6, 'N_N':36, 'N_OS':60, 'N_OSL':20},
        mos_intent='svt',
        #impl_lib='bag240_generated',
        R={'1A':8.66e3,'2A':8.66e3,'3A':6.49e3,'1B':5.11e3,'2B':5.11e3,'3B':3.65e3},
        baseC=1,
        C={'1A':1e-12,'2A':2.26e-12,'1B':1e-12,'2B':5.36e-12},
        fc = 20e6
    )


    design(bprj, temp_lib, impl_lib, tb_name, cell_name, sch_params)

