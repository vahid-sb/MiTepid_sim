#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:48:58 2020.

@author: vbokharaie
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

    #%% folders
    dir_source_mat = Path(Path(__file__).resolve().parent)
    dir_save_plots_main = Path(Path(__file__).resolve().parent, 'outputs_test')

    #%% age groups, used as legends in plots
    age_groups = ['[0-10]',  '[10-20]', '[20-30]', '[30-40]',
                  '[40-50]', '[50-60]', '[60-70]', '[70-80]', '80+',]

    model_type = 'SEIR'
    country = 'Germany'
    t_end = 541
    x00 = 1e-5
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    #
    if model_type == 'SIS':
        file_Bopt = Path('B_opt_SIS_I9p6.mat')
    elif model_type == 'SIR':
        file_Bopt = Path('B_opt_SIR_I9p6.mat')
    elif model_type == 'SEIR':
        file_Bopt = Path('B_opt_SEIR_I5_E4p6.mat')

    module_path = Path(mitepid.__file__).parent
    dir_B_opt = Path(module_path, 'Optimised_B')
    file_B_opt = Path(dir_B_opt, file_Bopt)

    B_opt_selected = get_B_policy(file_B_opt, country, 'Uncontained', )
    Ng = B_opt_selected.shape[0]
    Gamma = load_mat(file_B_opt, 'Gamma')

    if model_type == 'SEIR':
        Sigma = load_mat(file_B_opt, 'Sigma')

    assert len(age_groups)==9, 'Check the defined age-groups. Something is wrong there.'
    #%% reference policy: uncontained
    policy_name = 'Uncontained'
    list_t_switch = [0,]
    all_containment_list = ['Uncontained',]
    ref_obj = epid_sim(model_type=model_type,
                        B=B_opt_selected,
                        Gamma=Gamma,
                        Sigma=Sigma,
                        dir_save_plots_main=dir_save_plots_main,
                        country='Germany',
                        policy_list=all_containment_list,
                        policy_switch_times=list_t_switch,
                        x0=x0_vec,
                        t_end=t_end,
                        str_policy=policy_name,
                        group_labels=age_groups,)
    ref_obj.plot_agg()
    ref_obj.plot_strat()
    ref_obj.plot_strat_multiax()
    print('*************************************************************')
    #%% Uncontained_then_switching_R0
    list_t_switch = [0, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, ]
    all_containment_list = ['Uncontained',
                            'R0_is_1',
                            'Uncontained',
                            'R0_is_1',
                            'Uncontained',
                            'R0_is_1',
                            'Uncontained',
                            'R0_is_1',
                            'Uncontained',
                            'R0_is_1',
                            'Uncontained',
                           ]
    policy_name = 'Uncontained_then_switching_R0'

    epid_obj = epid_sim(model_type=model_type,
                        B=B_opt_selected,
                        Gamma=Gamma,
                        Sigma=Sigma,
                        dir_save_plots_main=dir_save_plots_main,
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
    #%% Uncontained_then_switching_Lockdown
    list_t_switch = [0, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, ]
    all_containment_list  = ['Uncontained',
                            'Lockdown',
                            'Uncontained',
                            'Lockdown',
                            'Uncontained',
                            'Lockdown',
                            'Uncontained',
                            'Lockdown',
                            'Uncontained',
                            'Lockdown',
                            'Uncontained',
                           ]

    policy_name = 'Uncontained_then_switching_Lockdown'
    epid_obj = epid_sim(model_type=model_type,
                        B=B_opt_selected,
                        Gamma=Gamma,
                        Sigma=Sigma,
                        dir_save_plots_main=dir_save_plots_main,
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
    #%% Uncontained_then_switching_Lockdown_R0
    list_t_switch = [0, 90, 120, 150, 180, 210, 240, 270, 300, 330,]
    all_containment_list = ['Uncontained',
                            'Lockdown',
                            'R0_is_1',
                            'Uncontained',
                            'Lockdown',
                            'R0_is_1',
                            'Uncontained',
                            'Lockdown',
                            'R0_is_1',
                            'Uncontained',
                             ]
    policy_name = 'Uncontained_then_switching_Lockdown_R0'
    epid_obj = epid_sim(model_type=model_type,
                        B=B_opt_selected,
                        Gamma=Gamma,
                        Sigma=Sigma,
                        dir_save_plots_main=dir_save_plots_main,
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

    #######################################################################################
    #%% Compare different policies for one country.
    #######################################################################################
    country = 'Germany'
    t_end = 541
    list_t_switch = [0, 90]
    x00 = 1e-5
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_list = ['Uncontained',
                   'Schools_closed',
                   'Elderly_self_isolate',
                   'Kids_Elderly_self_isolate',
                   'Schools_Offices_closed',
                   'Adults_Elderly_Self_isolate',
                   'Social_Distancing',
                   'Lockdown',
                   ]
    policy_labels = ['UN',
                   'KI',
                   'EL',
                   'KIEL',
                   'KIOF',
                   'ADEL',
                   'SD',
                   'LD',
                   ]
    list_sol_I = []
    list_sol_R = []
    for policy in policy_list:
        all_policies = ['Uncontained',]
        all_policies.append(policy)
        policy_name = 'Uncontained_then_' + policy
        print('*********************************************')
        print(policy_name)
        epid_obj = epid_sim(model_type=model_type,
                            B=B_opt_selected,
                            Gamma=Gamma,
                            Sigma=Sigma,
                            dir_save_plots_main=dir_save_plots_main,
                            country=country,
                            policy_list=all_policies,
                            policy_switch_times=list_t_switch,
                            x0=x0_vec,
                            t_end=t_end,
                            str_policy='00_OVERALL',
                            group_labels=age_groups,
                            ref_class=ref_obj)
        sol_agg_I = epid_obj.sol_agg_dict['I']
        sol_agg_R = epid_obj.sol_agg_dict['R']
        list_sol_I.append(sol_agg_I)
        list_sol_R.append(sol_agg_R)


    dir_save_plots_country = Path(dir_save_plots_main, country)
    dir_save_plots = Path(dir_save_plots_country, '00_OVERALL')
    dir_save_plots.mkdir(exist_ok=True, parents=True)
    filesave_I = Path(dir_save_plots, 'SIR_I_AGG_ALL_policies' + country +'.png')
    filesave_R = Path(dir_save_plots, 'SIR_R_AGG_ALL_policies' + country +'.png')

    # plot aggregate plots to compare all policies.
    t = np.arange(0, t_end+.01, step=0.1)
    list_all_policies = ['Uncontained']
    list_all_policies.extend(['Policy']*(len(policy_list)-1))

    arr_sol = np.squeeze(np.array(list_sol_R)).T
    bplot_agg(t, arr_sol, Ng=Ng, filesave=filesave_R,
      suptitle='', labels=policy_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Recovered Ratio')

    arr_sol = np.squeeze(np.array(list_sol_I)).T
    bplot_agg(t, arr_sol, Ng=Ng, filesave=filesave_I,
      suptitle='', labels=policy_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Infectious Ratio')

    #######################################################################################
    #%% Compare one policies for different countries.
    #######################################################################################
    t_end = 541
    list_t_switch = [0, ]
    x00 = 1e-5
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    list_countries = ['Germany',
                       'Iran',
                       'Italy',
                       'Spain',
                       'China',
                       'USA',
                       'UK',
                       'France',
                       ]
    all_policies = ['Uncontained',]
    list_sol_I = []
    list_sol_R = []
    for country in list_countries:
        print('*********************************************')
        print(country)
        epid_obj = epid_sim(model_type=model_type,
                            B=B_opt_selected,
                            Gamma=Gamma,
                            Sigma=Sigma,
                            dir_save_plots_main=dir_save_plots_main,
                            country=country,
                            policy_list=all_policies,
                            policy_switch_times=list_t_switch,
                            x0=x0_vec,
                            t_end=t_end,
                            str_policy='00_OVERALL',
                            group_labels=age_groups,
                            ref_class=ref_obj)
        sol_agg_I = epid_obj.sol_agg_dict['I']
        sol_agg_R = epid_obj.sol_agg_dict['R']
        list_sol_I.append(sol_agg_I)
        list_sol_R.append(sol_agg_R)


    dir_save_plots_country = Path(dir_save_plots_main)
    dir_save_plots = Path(dir_save_plots_country, '00_OVERALL_Uncontained')
    dir_save_plots.mkdir(exist_ok=True, parents=True)
    filesave_I = Path(dir_save_plots, 'SIR_I_AGG_ALL_countries.png')
    filesave_R = Path(dir_save_plots, 'SIR_R_AGG_ALL_countries.png')

    # plot aggregate plots to compare all policies.
    t = np.arange(0, t_end+.01, step=0.1)
    list_all_policies = ['Uncontained']

    arr_sol = np.squeeze(np.array(list_sol_R)).T
    bplot_agg(t, arr_sol, Ng=Ng, filesave=filesave_R,
      suptitle='', labels=list_countries, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Recovered Ratio')

    arr_sol = np.squeeze(np.array(list_sol_I)).T
    bplot_agg(t, arr_sol, Ng=Ng, filesave=filesave_I,
      suptitle='', labels=list_countries, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Infectious Ratio')
