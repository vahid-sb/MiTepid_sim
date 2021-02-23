#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:14:03 2020

@author: vbokharaie

Studying the effects of variations in R0 in an uncontained population in the spread of a SARS-CoV-2.

This script uses `mitepid` library to simulate the spread of SARS-CoV-2 in poulations of different countries.

The optimised contact rates can be found in `miteipd/Optimised_B` folder.

More details of the methodlogy can be found in:
https://www.medrxiv.org/content/10.1101/2020.10.16.20213835v1

"""


if __name__ == '__main__':
    # %%
    import numpy as np
    from pathlib import Path
    import logging
    logging.getLogger().setLevel(logging.CRITICAL)

    import mitepid
    from mitepid.policies import get_B_policy
    from mitepid.utils import load_mat
    from mitepid.epid_sim import epid_sim
    from mitepid.plots import bplot_agg


    # %% simulation general variables
    dir_save_plots = Path(Path(__file__).resolve().parent, 'OUTPUTS_submitted', 'Compare_R0_Uncontained')

    age_groups = ['[0-10]',  '[10-20]', '[20-30]', '[30-40]',
                  '[40-50]', '[50-60]', '[60-70]', '[70-80]', '80+',]

    module_path = Path(mitepid.__file__).parent
    dir_B_opt = Path(module_path, 'Optimised_B')

    t_end = 211
    x00 = 1e-5
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]

    policy_name = 'Uncontained'
    model_type = 'SEIR'

    list_t_switch = [0,]
    all_containment_list = ['Uncontained',]
    country = 'Germany'
    list_sol_I = []
    list_sol_R = []
    list_labels = ['R0 ' + "{:3.2f}".format(x) for x in np.arange(2.05, 3.95, 0.1)]
    for R0_float in np.arange(2.05, 3.95, 0.1):
        R0 = "{:3.2f}".format(R0_float)
        print('R0 in opt step = ', R0)
        model_type = 'SEIR'
        file_Bopt = Path('B_opt_SEIR_Ti_5_R0_' + str(R0) + '.mat')
        file_B_opt = Path(dir_B_opt, file_Bopt)
        Sigma = load_mat(file_B_opt, 'Sigma')
        Gamma = load_mat(file_B_opt, 'Gamma')
        B_opt_country = get_B_policy(file_B_opt, country, 'Uncontained', )
        Ng = B_opt_country.shape[0]
        assert len(age_groups)==9, 'Check the defined age-groups. Something is wrong there.'
        dir_save = Path(dir_save_plots, 'R0_variable', str(R0))
        epid_obj = epid_sim(model_type=model_type,
                            B=B_opt_country,
                            Gamma=Gamma,
                            Sigma=Sigma,
                            dir_save_plots_main=dir_save,
                            country=country,
                            policy_list=all_containment_list,
                            policy_switch_times=list_t_switch,
                            x0=x0_vec,
                            t_end=t_end,
                            str_policy=policy_name,
                            group_labels=age_groups,)
        sol_agg_I = epid_obj.sol_agg_dict['I']
        sol_agg_R = epid_obj.sol_agg_dict['R']
        list_sol_I.append(sol_agg_I)
        list_sol_R.append(sol_agg_R)

    # dir_save_plots.mkdir(exist_ok=True, parents=True)
    filesave_I = Path(dir_save_plots, model_type + '_' + country +  '_I_AGG_ALL_R0.png')
    filesave_R = Path(dir_save_plots, model_type + '_' + country +  '_R_AGG_ALL_R0.png')

    # plot aggregate plots to compare all policies.
    t = np.arange(0, t_end+.01, step=0.1)
    list_all_policies = ['Uncontained']

    arr_sol_R = np.squeeze(np.array(list_sol_R)).T
    bplot_agg(t, arr_sol_R, Ng=Ng, filesave=filesave_R,
      suptitle='', labels=list_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Recovered Ratio')


    arr_sol_I = np.squeeze(np.array(list_sol_I)).T
    bplot_agg(t, arr_sol_I, Ng=Ng, filesave=filesave_I,
      suptitle='', labels=list_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Infectious Ratio')

    # writing eventual ratios for I and R and all countries to disk
    filesave_txt = Path(dir_save_plots, model_type + country + '_variable_R0_eventual_I_R.txt')

    max_I = np.max(arr_sol_I, axis=0) * 100
    end_R = arr_sol_R[-1, :] * 100


    with open(filesave_txt, 'w') as my_text:
        my_text.write('\n %14s &  %6s   &  %6s '%('R0   ', 'end_R', 'max_I'))
        for idx, R0 in enumerate(list_labels):
            my_text.write('\n %14s &  $%2.2f\%%$ &  $%2.2f\%%$ \\\\ \hline'%(R0, end_R[idx], max_I[idx]))
