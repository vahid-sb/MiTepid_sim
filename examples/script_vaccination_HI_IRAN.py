#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:05:30 2020

@author: vbokharaie

Studying what happens if we vaccinate different percentage of the population
    and under different containment policies.

This script uses `mitepid` library to simulate the spread of SARS-CoV-2 in poulations of different countries.

The optimised contact rates can be found in `miteipd/Optimised_B` folder.

More details of the methodlogy can be found in:
https://www.medrxiv.org/content/10.1101/2020.10.16.20213835v1
"""
if __name__ == '__main__':
    import numpy as np
    from pathlib import Path

    import mitepid
    from mitepid.policies import get_B_policy
    from mitepid.utils import load_mat
    from mitepid.epid_sim import epid_sim
    from mitepid.plots import bplot_agg
    from mitepid.plots import bplot_agg


    #%% simulation general variables
    dir_save_plots_main = Path(Path(__file__).resolve().parent, 'OUTPUTS', 'Iran')

    age_groups = ['[0-10]',  '[10-20]', '[20-30]', '[30-40]',
                  '[40-50]', '[50-60]', '[60-70]', '[70-80]', '80+',]

    module_path = Path(mitepid.__file__).parent
    dir_B_opt = Path(module_path, 'Optimised_B')

    # %% Herd Immunity, uniform
    country = 'Iran'
    t_end = 540
    x0I = 1e-5
    x0_vec=[x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I,]

    model_type = 'SEIR'
    file_Bopt = Path('B_opt_SEIR_Ti_5_R0_2.95.mat')
    file_B_opt = Path(dir_B_opt, file_Bopt)
    Sigma = load_mat(file_B_opt, 'Sigma')
    Gamma = load_mat(file_B_opt, 'Gamma')
    list_my_policy = [['Uncontained'], [1.5]]
    list_str_policy = ['Uncontained', 'R0_is_1.5']
    list_pc1 = [56, 25]
    for idx, my_policy in enumerate(list_my_policy):
        str_policy = list_str_policy[idx]
        pc1 = list_pc1[idx]
        B_opt_country = get_B_policy(file_B_opt, country, 'Uncontained', )
        Ng = B_opt_country.shape[0]
        assert len(age_groups)==9, 'Check the defined age-groups. Something is wrong there.'
        ref_obj = epid_sim(model_type=model_type,
                            B=B_opt_country,
                            Gamma=Gamma,
                            Sigma=Sigma,
                            dir_save_plots_main=dir_save_plots_main,
                            country=country,
                            policy_list=my_policy,
                            policy_switch_times=[0],
                            x0=x0_vec,
                            t_end=t_end,
                            str_policy=str_policy,
                            group_labels=age_groups,)


        list_sol_I = []
        list_sol_R = []
        # pc1 = 45.
        pc2 = pc1 + 10
        x0R_array = list(np.arange(0., pc1, 5.0)/100) +\
                    list(np.arange(pc1, pc2, 1.0)/100)
        for x0R in x0R_array:
            print('x0R --------------> ', x0R)
            x0I = 1e-5
            x0E = 1e-5
            x0_vec=[x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I,
                    x0R, x0R, x0R, x0R, x0R, x0R, x0R, x0R, x0R,
                    x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E,]

            epid_obj = epid_sim(model_type=model_type,
                                B=B_opt_country,
                                Gamma=Gamma,
                                Sigma=Sigma,
                                dir_save_plots_main=dir_save_plots_main,
                                country=country,
                                policy_list=my_policy,
                                policy_switch_times=[0],
                                x0=x0_vec,
                                t_end=t_end,
                                str_policy=str_policy,
                                group_labels=age_groups,
                                ref_class=ref_obj)
            sol_agg_I = epid_obj.sol_agg_dict['I']
            sol_agg_R = epid_obj.sol_agg_dict['R']
            list_sol_I.append(sol_agg_I)
            list_sol_R.append(sol_agg_R)


        dir_save_plots = Path(dir_save_plots_main, '00_herd_immunity')
        # dir_save_plots.mkdir(exist_ok=True, parents=True)
        filesave_I = Path(dir_save_plots, str_policy+ '_' + model_type + '_' + country +  '_I_AGG_all_R_init.png')
        filesave_R = Path(dir_save_plots, str_policy+ '_' + model_type + '_' + country +  '_R_AGG_all_R_init.png')

        # plot aggregate plots to compare all policies.
        t = np.arange(0, t_end+.01, step=0.1)
        list_all_policies = ['Uncontained']
        list_labels = ['R_init='+'{:2.0f}'.format(x*100)+'%' for x in x0R_array]
        list_t_switch = [0]

        arr_sol_R = np.squeeze(np.array(list_sol_R)).T
        bplot_agg(t, arr_sol_R, Ng=Ng, filesave=filesave_R,
          suptitle='', labels=list_labels, list_vl=list_t_switch,
          list_all_policies=list_all_policies, ylabel='Recovered Ratio')


        arr_sol_I = np.squeeze(np.array(list_sol_I)).T
        bplot_agg(t, arr_sol_I, Ng=Ng, filesave=filesave_I,
          suptitle='', labels=list_labels, list_vl=list_t_switch,
          list_all_policies=list_all_policies, ylabel='Infectious Ratio')

        # writing eventual ratios for I and R and all countries to disk
        filesave_txt = Path(dir_save_plots, str_policy+ '_' + model_type+ '_' + country + '_variable_x0R.txt')
        max_I = np.max(arr_sol_I, axis=0) * 100
        end_R = arr_sol_R[-1, :] * 100
        with open(filesave_txt, 'w') as my_text:
            my_text.write('\n %14s &  %6s   &  %6s   &  %6s '%('T_i  ', 'end_R', 'end_R-R_init', 'max_I'))
            for idx, label in enumerate(list_labels):
                my_text.write('\n $%2s\%%$ &  $%2.2f\%%$ &  $%2.2f\%%$&  $%2.2f\%%$ \\\\ \hline'%(label[7:-1], end_R[idx], end_R[idx]-x0R_array[idx]*100, max_I[idx]))


