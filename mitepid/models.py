#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:50:11 2020.

@author: vbokharaie
"""

def SEIR(states, t, B, Gamma, Mu, Sigma):
    """
    Simulate SEIR compartmental Model.

    Parameters
    ----------
    states : numpy array
        array of size 3*Ng for Infective (I) and Recovered (R) trajectories.
    t : numpy array
        time array of interest.
    B : numpy 2D array
        matrix of contact rates. b_{ij} describes the influence of group j on group i.
    Gamma : numpy array
        a diagonal matrix of transmission rates.
    Mu: numpy array
        a diagonal matrix of birth/death rates (it is assumed birth and death rates are equal)
    Sigma: numpy array
        a diagonal matrix of inhibitions rate (related to how long is latent period)

    Returns
    -------
    dsdt : numpy array
        solution of the model.

    """
    import numpy as np
    Ng = B.shape[0];
    I = states[:Ng]  # I
    R = states[Ng:2*Ng]  # R
    E = states[2*Ng:3*Ng]  # E
    dIdt = np.zeros(Ng)
    dRdt = np.zeros(Ng)
    dEdt = np.zeros(Ng)
    for i in np.arange(Ng):
        Sum_j_x = 0
        for j in np.arange(Ng):
            Sum_j_x = Sum_j_x + B[i, j]* I[j]
        # E
        dEdt[i] = (1 - I[i] - R[i] - E[i]) * Sum_j_x - (Mu[i, i] + Sigma[i, i]) * E[i]
        # I
        dIdt[i] = Sigma[i, i] * E[i] - (Mu[i, i] + Gamma[i, i]) * I[i]
        # R
        dRdt[i] = Gamma[i, i] * I[i] - Mu[i,i] * R[i]

    dsdt = np.concatenate((dIdt, dRdt, dEdt))
    return dsdt

def SIR(states, t, B, Gamma, Mu):
    """
    Simulate SIR Model.

    Parameters
    ----------
    states : numpy array
        array of size 2*Ng for Infective (I) and Recovered (R) trajectories.
    t : numpy array
        time array of interest.
    B : numpy 2D array
        matrix of contact rates. b_{ij} describes the influence of group j on group i.
    Gamma : numpy array
        a diagonal matrix of transmission rates.
    Mu: numpy array
        a diagonal matrix of birth/death rates (it is assumed birth and death rates are equal)

    Returns
    -------
    dsdt : numpy array
        solution to the model.

    """
    import numpy as np
    Ng = B.shape[0];
    I = states[:Ng]
    R = states[Ng:]
    dIdt = np.zeros(Ng);
    dRdt = np.zeros(Ng);

    for i in np.arange(Ng):
        #
        Sum_j_x = 0
        for j in np.arange(Ng):
            Sum_j_x = Sum_j_x + B[i, j]* I[j]
        # I
        dIdt[i] = (1-I[i]) * Sum_j_x - R[i] * Sum_j_x - (Mu[i, i] + Gamma[i, i]) * I[i]
        # R
        dRdt[i] = Gamma[i, i] * I[i] - Mu[i, i] * R[i]

    dsdt = np.concatenate((dIdt, dRdt))
    return dsdt


def SIS(I, t, B, Gamma, Mu):
    """
    Simulate SIS model.

    Parameters
    ----------
    I : numpy array
        array of size Ng for Infective (I) trajectories.
    t : numpy array
        time array of interest.
    B : numpy 2D array
        matrix of contact rates. b_{ij} describes the influence of group j on group i.
    Gamma : numpy array
        a diagonal matrix of transmission rates.
    Mu: numpy array
        a diagonal matrix of birth/death rates (it is assumed birth and death rates are equal)

    Returns
    -------
    dIdt : numpy array
        solution to the model.

    """
    import numpy as np
    Ng = I.size;
    dIdt = np.zeros(Ng)
    for i in np.arange(Ng):
        Sum_j = 0
        for j in np.arange(Ng):
            Sum_j = Sum_j + B[i, j]* I[j]

        dIdt[i] = (1-I[i]) * Sum_j - (Mu[i, i] + Gamma[i, i]) * I[i]
    return dIdt


