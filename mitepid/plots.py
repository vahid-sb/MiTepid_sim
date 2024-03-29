#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:49:51 2020.

@author: vbokharaie
"""
# %% bplot_strat
def bplot_strat(t,
          sol,
          ylim=None,
          if_show=False,
          if_save=True,
          filesave='test.png',
          labels=[''],
          suptitle='',
          list_vl=[],
          list_all_policies=None,
          ylabel='',
          if_plot_in_pc=True,
          cmap='Dark2',
          Ng=None,
          policy_name_pos=0.8,
          policy_legend=True,
          v_line=True,
          N_population=None):
    """
    Line plots of the solutions to the epidemilogical model.

    Parameters
    ----------
    t : numpy array, (N_time,)
        time array
    sol : ND numpy array, (N_time x N_groups)
        solution of an SIS or SIR model, or solution of any ODE.
    plot_type : int, optional
        1: concurrent plots of all age groups, 2: each in a separate subplot. The default is 1.
    ylim : list of floats, optional
        y-axis limits. The default is (0,1).
    if_show : bool, optional
        Should plots be closed or not. The default is False.
    if_save : bool, optional
        save the plots to disk or not. The default is True.
    filesave : pathlib Path, optional
        filename for plots. The default is 'test.png'.
    labels : list of str, optional
        labels for plot legends. The default is [''].
    suptitle : str, optional
        main plot title. The default is ''.
    list_vl : list float, optional
        list of swithing times between policies, marked by red vertical lines. The default is [].
    list_all_policies : list of str, optional
        list of policies to implement at each switching time. The default is [].
    ylabel : str, optional
        y-axis label. The default is ''.
    if_plot_in_pc : bool
        y axis in percents or just the ratio.
    cmap : matplotlib colormap
        cmap used in plot
    Ng : int
        number of groups in the oringal model
    policy_name_pos : float
        in [0,1] range. Where in y axis should the text for each policy be insterted.
    policy_legend: bool
        if show policy legends in the plot
    v_line= bool
        if show vertical lines which indictae beginning of each policy.
    N_population: int
        to use for verticl axes instead of percentages

    Returns
    -------
    None.

    """
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pl
    import matplotlib as mpl
    import numpy as np

    plt.style.use('seaborn-whitegrid')
    # plt.style.use('seaborn-darkgrid')
    # plt.style.use('bmh')
    # plt.style.use('ggplot')
    # mpl.rcParams['lines.linewidth'] = 3.0
    # mpl.rcParams['font.weight'] = 'bold'
    font_size = 40
    font = {'family' : 'DejaVu Sans',
                'sans-serif' : 'Tahoma',
                'weight' : 'bold',
                'size'   : font_size}
    mpl.rc('grid', color='#316931', linewidth=1, linestyle='dotted')
    mpl.rc('font', **font)
    mpl.rc('lines', lw=3,)
    # mpl.rc('xtick', labelsize=font_size)
    # mpl.rc('ytick', labelsize=font_size)

    if cmap == 'viridis_r':
        colors = pl.cm.viridis_r(np.linspace(0,1,Ng))
    elif cmap == 'viridis':
        colors = pl.cm.viridis_r(np.linspace(0,1,Ng))
    elif cmap == 'Dark2':
        colors = pl.cm.Dark2.colors
    elif cmap == 'Set1':
        colors = pl.cm.Set1.colors
    else:
        colors = pl.cm.Dark2.colors

    if if_plot_in_pc:
        if ylabel:
            ylabel = ylabel + ' (values in %)'

        y_ax_scale = 100
    else:
        y_ax_scale = 1

    if not N_population is None:
        sol = sol*N_population

    fig, ax = plt.subplots(1, 1, figsize=(24,18))
    # ax.set_facecolor('0.95')
    fig.subplots_adjust(bottom=0.15, top=0.92, left=0.1, right = 0.85)
    for cc in np.arange(Ng):
        # my_label = 'x'+str(cc+1).zfill(2)

        if not labels==['']:
            ax.plot(t, sol[:, cc] * y_ax_scale, label=labels[cc], color = colors[cc], alpha=0.98)
            ax.legend(bbox_to_anchor=(1.2, 1.0), prop={'size': 24, 'weight': 'bold'})
        else:
            ax.plot(t, sol[:, cc] * y_ax_scale, color = colors[cc], alpha=0.98)

        if ylim:
            ax.set_ylim(ylim)
        ax.set_xlabel('\nTime (days)', fontweight='bold')
        ax.set_xticks(np.arange(0, t[-1], step=30))
        plt.xticks(rotation=90)
        ax.set_ylabel(ylabel, fontweight='bold')
        ylim_max = ax.get_ylim()[1]
    for idx1, xc in enumerate(list_vl):
        if v_line:
            ax.axvline(x=xc, color='r', linestyle='--', linewidth=1)
        bbox = {'fc': '0.92', 'pad': 4, 'alpha': 0.3}
        props = {'ha': 'center', 'va': 'center', 'bbox': bbox,}
        if policy_legend and not list_all_policies is None:
            my_text = list_all_policies[idx1]
            if isinstance(my_text, (int, float)):
                my_text = 'R0 = ' + str(my_text)

            # make sure policy label does not cover main plot
            idx_xc_in_t = [idx for idx, x in enumerate(t) if x>xc][0]
            if sol[idx_xc_in_t, 0] < 0.9*ylim_max and sol[idx_xc_in_t, 0] < 0.7*ylim_max:
                policy_label_loc = policy_name_pos*ylim_max
            else:
                policy_label_loc = 0.3*ylim_max
            xc_plot = xc+10*t[-1]/500
            ax.text(xc_plot, policy_label_loc, my_text, props,
                    rotation=90, color='k', alpha=0.7, fontweight='bold', fontsize=40)
    fig.suptitle(suptitle, fontsize=24, fontweight='bold')

    if not if_show:
        plt.close('all')
    if if_save:
        dir_save = filesave.parent
        dir_save.mkdir(exist_ok=True, parents=True)
        fig.savefig(filesave, dpi=150)
        filesave_pdf = filesave.with_suffix(".pdf")
        fig.savefig(filesave_pdf, dpi=150)

# %% bplot_strat_multiax
def bplot_strat_multiax(t,
                        list_sol,
                        Ng,
                        ylim=None,
                        if_show=False,
                        if_save=True,
                        filesave='test.png',
                        labels=[''],
                        ylabels=[''],
                        suptitle='',
                        list_vl=[],
                        list_all_policies=None,
                        ylabel='',
                        if_plot_in_pc=True,
                        cmap='Dark2',
                        policy_name_pos=0.75,
                        policy_legend=True,
                        v_line=True,
                        N_population=None):
    """
    Line plots of the solutions to the epidemilogical model.

    Parameters
    ----------
    t : numpy array, (N_time,)
        time array
    sol : ND numpy array, (N_time x N_groups)
        solution of an SIS or SIR model, or solution of any ODE.
    plot_type : int, optional
        1: concurrent plots of all age groups, 2: each in a separate subplot. The default is 1.
    ylim : list of floats, optional
        y-axis limits. The default is (0,1).
    if_show : bool, optional
        Should plots be closed or not. The default is False.
    if_save : bool, optional
        save the plots to disk or not. The default is True.
    filesave : pathlib Path, optional
        filename for plots. The default is 'test.png'.
    labels : list of str, optional
        labels for plot legends. The default is [''].
    suptitle : str, optional
        main plot title. The default is ''.
    list_vl : list float, optional
        list of swithing times between policies, marked by red vertical lines. The default is [].
    list_all_policies : list of str, optional
        list of policies to implement at each switching time. The default is [].
    ylabel : str, optional
        y-axis label. The default is ''.
    if_plot_in_pc : bool
        y axis in percents or just the ratio.
    cmap : matplotlib colormap
        cmap used in plot
    Ng : int
        number of groups in the oringal model
    policy_name_pos : float
        in [0,1] range. Where in y axis should the text for each policy be insterted.
   policy_legend: bool
        if show policy legends in the plot
    v_line= bool
        if show vertical lines which indictae beginning of each policy.
    N_population: int
        to use for verticl axes instead of percentages

    Returns
    -------
    None.

    """
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pl
    import matplotlib as mpl
    import numpy as np

    plt.style.use('seaborn-whitegrid')
    # plt.style.use('seaborn-darkgrid')
    # plt.style.use('bmh')
    # plt.style.use('ggplot')
    # mpl.rcParams['lines.linewidth'] = 3.0
    # mpl.rcParams['font.weight'] = 'bold'
    font_size = 40
    font = {'family' : 'DejaVu Sans',
                'sans-serif' : 'Tahoma',
                'weight' : 'bold',
                'size'   : font_size}
    mpl.rc('grid', color='#316931', linewidth=1, linestyle='dotted')
    mpl.rc('font', **font)
    mpl.rc('lines', lw=3,)
    # mpl.rc('xtick', labelsize=font_size)
    # mpl.rc('ytick', labelsize=font_size)

    if cmap == 'viridis_r':
        colors = pl.cm.viridis_r(np.linspace(0,1,Ng))
    elif cmap == 'viridis':
        colors = pl.cm.viridis_r(np.linspace(0,1,Ng))
    elif cmap == 'Dark2':
        colors = pl.cm.Dark2.colors
    elif cmap == 'Set1':
        colors = pl.cm.Set1.colors
    else:
        colors = pl.cm.Dark2.colors
    if if_plot_in_pc:
        if ylabel:
            ylabel = ylabel + ' (values in %)'
        y_ax_scale = 100
    else:
        y_ax_scale = 1

    if not N_population is None:
        for idx, sol in enumerate(list_sol):
            list_sol[idx] = sol*N_population

    fig, ax_all = plt.subplots(Ng, 1, figsize=(20,18))
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.1, top=0.95, left = 0.1)
    # colors = pl.cm.viridis_r(np.linspace(0,1,2))
    # fig.subplots_adjust(bottom=0.15, top=0.92, left=0.1, right = 0.88)
    for cc in np.arange(Ng):
        # my_label = 'x'+str(cc+1).zfill(2)
        ax = ax_all[cc]
        for cc2, sol in enumerate(list_sol):
            if cc==0:
                ax.plot(t, sol[:, cc] * y_ax_scale, label=labels[cc2], color = colors[cc2], alpha=0.98)
                ax.legend(prop={'size': 24, 'weight': 'bold'})
            else:
                ax.plot(t, sol[:, cc] * y_ax_scale, color = colors[cc2], alpha=0.98)  # policy
        if ylim:
            ax.set_ylim(ylim)
        if cc == Ng-1:
            ax.set_xlabel('\nTime (days)', fontweight='bold')
            plt.xticks(rotation=90)
        else:
            ax.xaxis.set_ticklabels([])
        ax.set_xticks(np.arange(0, t[-1], step=30))
        if not ylabels==['']:
            ax.set_ylabel(ylabels[cc], rotation=90, fontweight='bold')
        # ylim_max = ax.get_ylim()[1]
        for idx1, xc in enumerate(list_vl):
            if v_line:
                ax.axvline(x=xc, color='r', linestyle='--', linewidth=1)
    fig.suptitle(suptitle, fontsize=24, fontweight='bold')

    if not if_show:
        plt.close('all')
    if if_save:
        dir_save = filesave.parent
        dir_save.mkdir(exist_ok=True, parents=True)
        fig.savefig(filesave, dpi=150)
        filesave_pdf = filesave.with_suffix(".pdf")
        fig.savefig(filesave_pdf, dpi=150)

# %% bplot_agg
def bplot_agg(t,
          sol,
          Ng,
          ylim=None,
          if_show=False,
          if_save=True,
          filesave='test.png',
          labels=[''],
          suptitle='',
          list_vl=[],
          list_all_policies=None,
          ylabel='',
          if_plot_in_pc=True,
          cmap='tab20',
          policy_name_pos=0.8,
          v_line=True,
          policy_legend=True,
          N_population=None):
    """
    Line plots of the solutions to the epidemilogical model.

    Parameters
    ----------
    t : numpy array, (N_time,)
        time array
    sol : ND numpy array, (N_time x N_groups)
        solution of an SIS or SIR model, or solution of any ODE.
    plot_type : int, optional
        1: concurrent plots of all age groups, 2: each in a separate subplot. The default is 1.
    ylim : list of floats, optional
        y-axis limits. The default is (0,1).
    if_show : bool, optional
        Should plots be closed or not. The default is False.
    if_save : bool, optional
        save the plots to disk or not. The default is True.
    filesave : pathlib Path, optional
        filename for plots. The default is 'test.png'.
    labels : list of str, optional
        labels for plot legends. The default is [''].
    suptitle : str, optional
        main plot title. The default is ''.
    list_vl : list float, optional
        list of swithing times between policies, marked by red vertical lines. The default is [].
    list_all_policies : list of str, optional
        list of policies to implement at each switching time. The default is [].
    ylabel : str, optional
        y-axis label. The default is ''.
    if_plot_in_pc : bool
        y axis in percents or just the ratio.
    cmap : matplotlib colormap
        cmap used in plot
    Ng : int
        number of groups in the oringal model
    policy_name_pos : float
        in [0,1] range. Where in y axis should the text for each policy be insterted.
    policy_legend: bool
        if show policy legends in the plot
    v_line: bool
        if show vertical lines which indictae beginning of each policy.
    N_population: int
        to use for verticl axes instead of percentages

    Returns
    -------
    None.

    """
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pl
    import matplotlib as mpl
    import numpy as np

    plt.style.use('seaborn-whitegrid')
    # plt.style.use('seaborn-darkgrid')
    # plt.style.use('bmh')
    # plt.style.use('ggplot')
    # mpl.rcParams['lines.linewidth'] = 3.0
    # mpl.rcParams['font.weight'] = 'bold'
    font_size = 40
    font = {'family' : 'DejaVu Sans',
                'sans-serif' : 'Tahoma',
                'weight' : 'bold',
                'size'   : font_size}
    mpl.rc('grid', color='#316931', linewidth=1, linestyle='dotted')
    mpl.rc('font', **font)
    mpl.rc('lines', lw=3,)
    mpl.rc('xtick', labelsize=font_size, )
    mpl.rc('ytick', labelsize=font_size)

    if cmap == 'viridis_r':
        colors = pl.cm.viridis_r(np.linspace(0,1,Ng))
    elif cmap == 'viridis':
        colors = pl.cm.viridis_r(np.linspace(0,1,Ng))
    elif cmap == 'Dark2':
        colors = pl.cm.Dark2.colors
        colors = colors + colors
    elif cmap == 'Set1':
        colors = pl.cm.Set1.colors
        colors = colors + colors
    elif cmap == 'tab10':
        colors = pl.cm.tab10.colors
        colors = colors + colors
    elif cmap == 'tab20':
        colors = pl.cm.tab20.colors
        colors = colors + colors
    if if_plot_in_pc and N_population is None:
        if ylabel:
            ylabel = ylabel + ' (in %)'

        y_ax_scale = 100
    else:
        y_ax_scale = 1

    if not N_population is None:
        sol = sol*N_population
    fig, ax = plt.subplots(1, 1, figsize=(25,18))
    # ax.set_facecolor('0.95')
    fig.subplots_adjust(bottom=0.15, top=0.92, left=0.1, right = 0.85)
    # fig.tight_layout()
    for cc in np.arange(sol.shape[1]):
        # my_label = 'x'+str(cc+1).zfill(2)
        if not labels==['']:
            try:
                ax.plot(t, sol[:, cc] * y_ax_scale, label=labels[cc], alpha=0.98)
                # ax.plot(t, sol[:, cc] * y_ax_scale, label=labels[cc], color = colors[cc], alpha=0.98)
            except:
                a=1
            ax.legend(bbox_to_anchor=(1.21, 1.0), prop={'size': 30, 'weight': 'bold'})
        else:
            ax.plot(t, sol[:, cc] * y_ax_scale, color = colors[cc], alpha=0.98)

        if ylim:
            ax.set_ylim(ylim)
        ax.set_xlabel('\nTime (days)', fontweight='bold')
        ax.set_xticks(np.arange(0, t[-1], step=30))
        plt.xticks(rotation=90)
        ax.set_ylabel(ylabel, fontweight='bold')
        ylim_max = ax.get_ylim()[1]
    for idx1, xc in enumerate(list_vl):
        if v_line:
            ax.axvline(x=xc, color='r', linestyle='--', linewidth=1)
        bbox = {'fc': '0.92', 'pad': 4, 'alpha': 0.3}
        props = {'ha': 'center', 'va': 'center', 'bbox': bbox,}
        if policy_legend and not list_all_policies is None:
            my_text = list_all_policies[idx1]
            if isinstance(my_text, (int, float)):
                my_text = 'R0 = ' + str(my_text)
            # make sure policy label does not cover main plot
            idx_xc_in_t = [idx for idx, x in enumerate(t) if x>xc][0]
            if sol[idx_xc_in_t, 0] < 0.9*ylim_max and sol[idx_xc_in_t, 0] < 0.7*ylim_max:
                policy_label_loc = policy_name_pos*ylim_max
            else:
                policy_label_loc = 0.3*ylim_max
            xc_plot = xc+10*t[-1]/500
            ax.text(xc_plot, policy_label_loc, my_text, props,
                    rotation=90, color='k', alpha=0.6, fontweight='bold', fontsize=40)
    fig.suptitle(suptitle, fontsize=24, fontweight='bold')
    # ax.axvline(x=xc, color='r', linestyle='--', linewidth=1)

    if not if_show:
        plt.close('all')
    if if_save:
        dir_save = filesave.parent
        dir_save.mkdir(exist_ok=True, parents=True)
        fig.savefig(filesave, dpi=150)
        filesave_pdf = filesave.with_suffix(".pdf")
        fig.savefig(filesave_pdf, dpi=150)
