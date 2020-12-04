#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:51:35 2020.

@author: vbokharaie

Studying the effects of various containment Strategies on the spread of SARS-CoV-2 in the population of Iran.
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
    dir_save_plots = Path(Path(__file__).resolve().parent, 'OUTPUTS', 'Iran')

    age_groups = ['[0-10]',  '[10-20]', '[20-30]', '[30-40]',
                  '[40-50]', '[50-60]', '[60-70]', '[70-80]', '80+',]

    module_path = Path(mitepid.__file__).parent
    dir_B_opt = Path(module_path, 'Optimised_B')

    country = 'Iran'
    t_end = 271
    x00 = 1e-6
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
                        country='Iran',
                        policy_list=['Uncontained'],
                        policy_switch_times=[0],
                        x0=x0_vec,
                        t_end=t_end,
                        str_policy='Uncontained',
                        group_labels=age_groups,)

    # %% current estimate
    t_s = 60
    list_t_switch = [0] + list(np.arange(t_s, t_s + 30 * 7, 30))
    str_ts = '_start_' + str(t_s) + 'D'
    all_containment_list = ['Uncontained',
                            1.5,
                            1.2,
                            1.5,
                            1.2,
                            1.5,
                            1.2,
                            1.5,
                           ]
    policy_name = 'Iran_Current_estimate_' + str_ts

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
    epid_obj.plot_agg()
    epid_obj.plot_strat()
    epid_obj.plot_strat_multiax()

    # %%
    t_end = 541
    t_s = 60
    list_t_switch = [0] + list(np.arange(t_s, t_s + 30 * 8, 30))
    str_ts = '_start_' + str(t_s) + 'D'
    all_containment_list = ['Uncontained',
                            1.5,
                            1.2,
                            1.5,
                            1.2,
                            1.5,
                            1.2,
                            1.5,
                            'Uncontained',
                           ]
    policy_name = 'Iran_future_estimate_uncontained_' + str_ts


    ref_obj = epid_sim(model_type=model_type,
                    B=B_opt_country,
                    Gamma=Gamma,
                    Sigma=Sigma,
                    dir_save_plots_main=dir_save_plots,
                    country='Iran',
                    policy_list=['Uncontained'],
                    policy_switch_times=[0],
                    x0=x0_vec,
                    t_end=t_end,
                    str_policy='Uncontained',
                    group_labels=age_groups,)
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
    epid_obj.plot_agg()
    epid_obj.plot_strat()
    epid_obj.plot_strat_multiax()
