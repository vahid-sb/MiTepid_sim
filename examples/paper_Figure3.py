#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:51:35 2020.

@author: vbokharaie

Studying the effects of various containment Strategies on the spread of SARS-CoV-2 in the population of Germany.
It is assumed we switched between policies of various degrees of severity.

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


    # %% simulation general variables
    dir_save_plots = Path(Path(__file__).resolve().parent, 'OUTPUTS_submitted', 'Switching_Policies')

    age_groups = ['[0-10]',  '[10-20]', '[20-30]', '[30-40]',
                  '[40-50]', '[50-60]', '[60-70]', '[70-80]', '80+',]

    module_path = Path(mitepid.__file__).parent
    dir_B_opt = Path(module_path, 'Optimised_B')

    country = 'Germany'
    t_end = 451
    x00 = 1e-5
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]

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
                       dir_save_plots_main=dir_save_plots,
                       country='Germany',
                       policy_list=['Uncontained'],
                       policy_switch_times=[0],
                       x0=x0_vec,
                       t_end=t_end,
                       str_policy='Uncontained',
                       group_labels=age_groups,)
    t_s = 30
    list_t_switch1 = [0] + list(np.arange(t_s, t_s + 30 * 10, 30))
    list_t_switch2 = [0] + list(np.arange(t_s, t_s + 30 * 11, 30))
    list_t_switch3 = [0] + list(np.arange(t_s, t_s + 30 * 11, 30))

    str_ts = '_start_' + str(t_s) + 'D'
    all_containment_list1 = ['Uncontained',
                             'SD',
                             'Uncontained',
                             'SD',
                             'Uncontained',
                             'SD',
                             'Uncontained',
                             'SD',
                             'Uncontained',
                             'SD',
                             'Uncontained',
                             ]
    all_containment_list2 = ['Uncontained',
                             1.5,
                             'SD',
                             1.5,
                             'SD',
                             1.5,
                             'SD',
                             1.5,
                             'SD',
                             1.5,
                             'SD',
                             'Uncontained',
                             ]

    all_containment_list3 = ['Uncontained',
                             1.5,
                             0.9,
                             1.5,
                             0.9,
                             1.5,
                             0.9,
                             1.5,
                             0.9,
                             1.5,
                             0.9,
                             'Uncontained',
                             ]
    policy_name3 = 'Uncontained_then_switching_R0p9_R1p5' + str_ts
    policy_name2 = 'Uncontained_then_switching_R1p5_SD' + str_ts
    policy_name1 = 'Uncontained_then_switching_SD_uncon' + str_ts
    all_containments = [all_containment_list1, all_containment_list2,
                        all_containment_list3, ]
    all_policy_name = [policy_name1, policy_name2, policy_name3, ]
    all_t_switch = [list_t_switch1, list_t_switch2, list_t_switch3]

    for (all_containment_list, policy_name, list_t_switch) in zip(all_containments,
                                                                  all_policy_name, all_t_switch):
        epid_obj = epid_sim(model_type=model_type,
                            B=B_opt_country,
                            Gamma=Gamma,
                            Sigma=Sigma,
                            dir_save_plots_main=dir_save_plots,
                            country=country,
                            policy_list=all_containment_list,
                            policy_switch_times=list_t_switch,
                            x0=x0_vec,
                            t_end=t_end,
                            str_policy=policy_name,
                            group_labels=age_groups,
                            ref_class=ref_obj)
        epid_obj.plot_agg(suptitle='')
        epid_obj.plot_strat()
        epid_obj.plot_strat_multiax()
