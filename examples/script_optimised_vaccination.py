#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 19:05:30 2020.

@author: vbokharaie

How to optimise limited number of vaccine units in a population.
The optimised ratios are calculated for the population of Germany.

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
    from mitepid.policies import get_pop_distr


    #%% simulation general variables
    dir_save_plots_main = Path(Path(__file__).resolve().parent, 'OUTPUTS')

    age_groups = ['[0-10]',  '[10-20]', '[20-30]', '[30-40]',
                  '[40-50]', '[50-60]', '[60-70]', '[70-80]', '80+',]

    module_path = Path(mitepid.__file__).parent
    dir_B_opt = Path(module_path, 'Optimised_B')

    # %% Herd Immunity, optimise among age-groups
    country = 'Germany'
    t_end = 541
    x0I = 1e-5
    x0_vec=[x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I,]

    model_type = 'SEIR'
    file_Bopt = Path('B_opt_SEIR_Ti_5_R0_2.95.mat')
    file_B_opt = Path(dir_B_opt, file_Bopt)
    Sigma = load_mat(file_B_opt, 'Sigma')
    Gamma = load_mat(file_B_opt, 'Gamma')
    B_opt_country = get_B_policy(file_B_opt, country, 'Uncontained', )
    Ng = B_opt_country.shape[0]
    assert len(age_groups)==9, 'Check the defined age-groups. Something is wrong there.'
    ref_obj = epid_sim(model_type=model_type,
                        B=B_opt_country,
                        Gamma=Gamma,
                        Sigma=Sigma,
                        dir_save_plots_main=dir_save_plots_main,
                        country=country,
                        policy_list=['Uncontained'],
                        policy_switch_times=[0],
                        x0=x0_vec,
                        t_end=t_end,
                        str_policy='Uncontained',
                        group_labels=age_groups,)


    list_sol_I = []
    list_sol_R = []

    pop_pc = get_pop_distr(country)
    pop_pc = [x/100 for x in pop_pc]

    list_x0R_worst = [0.1978, 0.9500, 0.0500, 0.0500, 0.0500, 0.0500, 0.0500, 0.0500, 0.0500]
    list_x0R_opt = [0.0500, 0.0500, 0.0928, 0.0500, 0.0500, 0.1547, 0.2871, 0.3207, 0.3960]
    total_pc_opt = np.sum([x*y for (x,y) in zip(pop_pc, list_x0R_opt)])
    total_pc_worst = np.sum([x*y for (x,y) in zip(pop_pc, list_x0R_worst)])

    list_labels = ['uniform', 'optimised', 'worst']
    list_labels = ['uniform', 'optimised',]
    x0I = 1e-5
    x0E = 1e-5
    x0R = 0.15
    x0_vec_uniform=[x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I,
            x0R, x0R, x0R, x0R, x0R, x0R, x0R, x0R, x0R,
            x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E,]

    x0_vec_opt = [x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I] + list_x0R_opt + \
            [x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E,]

    x0_vec_worst = [x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I, x0I] + list_x0R_worst + \
                [x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E, x0E,]


    x0_vec_list = [x0_vec_uniform, x0_vec_opt,  x0_vec_worst, ]
    x0_vec_list = [x0_vec_uniform, x0_vec_opt,]
    for x0_vec in x0_vec_list:
        policy_name = 'R1p5_herd_immunity'
        epid_obj = epid_sim(model_type=model_type,
                            B=B_opt_country,
                            Gamma=Gamma,
                            Sigma=Sigma,
                            dir_save_plots_main=dir_save_plots_main,
                            country=country,
                            policy_list=[1.5],
                            policy_switch_times=[0],
                            x0=x0_vec,
                            t_end=t_end,
                            str_policy=policy_name,
                            group_labels=age_groups,
                            ref_class=ref_obj)
        sol_agg_I = epid_obj.sol_agg_dict['I']
        sol_agg_R = epid_obj.sol_agg_dict['R']
        list_sol_I.append(sol_agg_I)
        list_sol_R.append(sol_agg_R)


    dir_save_plots = Path(dir_save_plots_main, '00_herd_immunity_opt')
    # dir_save_plots.mkdir(exist_ok=True, parents=True)
    filesave_I = Path(dir_save_plots, model_type + '_' + country +  '_I_AGG_HI_opt.png')
    filesave_R = Path(dir_save_plots, model_type + '_' + country +  '_R_AGG_HI_opt.png')

    # plot aggregate plots to compare all policies.
    t = np.arange(0, t_end+.01, step=0.1)
    list_all_policies = ['R0=1.5']
    list_t_switch = [0]

    arr_sol_R = np.squeeze(np.array(list_sol_R)).T
    bplot_agg(t, arr_sol_R, Ng=Ng, filesave=filesave_R,
      suptitle='', labels=list_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Recovered Ratio',
      cmap='tab10',)


    arr_sol_I = np.squeeze(np.array(list_sol_I)).T
    bplot_agg(t, arr_sol_I, Ng=Ng, filesave=filesave_I,
      suptitle='', labels=list_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Infectious Ratio',
      cmap='tab10',)

    # writing eventual ratios for I and R and all countries to disk
    filesave_txt = Path(dir_save_plots, model_type + country + '_HI_opt.txt')
    max_I = np.max(arr_sol_I, axis=0) * 100
    end_R = arr_sol_R[-1, :] * 100
    with open(filesave_txt, 'w') as my_text:
        my_text.write('\n %14s &  %6s   &  %6s   &  %6s '%('T_i  ', 'end_R', 'end_R-R_init', 'max_I'))
        for idx, label in enumerate(list_labels):
            my_text.write('\n %14s &  $%2.2f\%%$ &  $%2.2f\%%$&  $%2.2f\%%$ \\\\ \hline'%(label, end_R[idx], end_R[idx]-x0R*100, max_I[idx]))


