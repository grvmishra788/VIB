import numpy as np
from sklearn import datasets
from ctypes import *
from sys import platform
import math


def generateDynamicProjPath(projS, projE, mode='FIX_STEPNUM'):
    # S-start  E-end
    # Fa, Fz, starting and ending frame
    # Ga, Gz, principal vector: starting and ending frame without in plane rotation
    Fa = np.matrix(projS)
    Fz = np.matrix(projE)

    # check if basis are orthonormal
    print("FaDot:", np.dot(np.transpose(Fa[:, 0]), Fa[:, 1]))
    print("FzDot:", np.dot(np.transpose(Fz[:, 0]), Fz[:, 1]))

    # svd
    U, s, V = np.linalg.svd(Fa.T * Fz)
    print("shapes:", U.shape, s.shape, V.shape)
    Va = np.matrix(U)
    Vz = np.matrix(V)
    Ga = Fa * Va
    Gz = Fz * Vz.T

    # print ('s:',s)
    tau = np.arccos(s)
    # euclidean norm of principal angles
    dist_az = np.sqrt(np.sum(np.multiply(tau, tau)))

    if (dist_az < 0.001):
        return [Fz]  # the span(Fa) is equal to span(Fz)

    Gz[:, 0] = gram_schmidt(Ga[:, 0], Gz[:, 0])
    Gz[:, 1] = gram_schmidt(Ga[:, 1], Gz[:, 1])

    Gz = normalizeBasis(orthnogoalize(Gz))

    # generate path
    projPath = []
    if mode == 'FIX_STEPSIZE':
        projPath.append(Fz)
    elif mode == 'FIX_STEPNUM':
        stepsize = 50
        for i in range(0, stepsize + 1):
            t = i / float(stepsize)
            F = projPath_t(tau * t, Ga, Gz, Va, Vz)
            projPath.append(F)
        # target subspace
        projPath.append(Fz * Vz.T * Va.T)

    return projPath


def projPath_t(tau_t, Ga, Gz, Va, Vz):
    G = np.matrix(np.zeros(Ga.shape))
    for i in range(Ga.shape[1]):  # num of column
        ct = np.cos(tau_t[i])
        st = np.sin(tau_t[i])
        G[:, i] = ct * Ga[:, i] + st * Gz[:, i]

    F = G * Va.T
    return F


def generateFullDynamicProjPath(Fa, Fz, stepsize=50):
    Fa = np.matrix(Fa)
    Fz = np.matrix(Fz)

    if np.all(np.fabs(Fa.T * Fz - np.identity(2)) < 0.001):
        return [Fz]

    U = np.hstack([Fa, Fz])
    B = np.matrix(gs(U))
    Wa = B.T * (Fa)
    Wz = B.T * (Fz)

    givensList = []
    tWz = Wz.copy()
    for k in range(0, tWz.shape[1]):
        for i in range(k + 1, tWz.shape[0]):
            if tWz[k, k] != 0.0 or tWz[i, k] != 0.0:
                R, theta = GivensRotation(k, i, tWz[k, k], tWz[i, k], tWz.shape[0])
                givensList.insert(0, [-theta, k, i])
                tWz = R * tWz

    # projPath = [Fa]
    projPath = [Fa]

    for i in range(0, stepsize + 1):
        t = i / float(stepsize)
        tWa = Wa.copy()
        listOfR = generateRotation(givensList, t, Wz.shape[0])
        # print "Wa:\n", Wa
        for R in listOfR:
            tWa = R * tWa

        # print "B*rot*Wa:\n", B*tWa
        basis = B * tWa
        # basis = normalizeBasis(orthnogoalize(basis))
        projPath.append(basis)

    projPath.append(Fz)
    return [np.array(x) for x in projPath]


def generateRotation(Glist, t, dim):
    # tolR = np.identity(dim)
    listOfR = []
    for l in Glist:
        # [-r, k, i]
        R = np.identity(dim)
        theta = l[0]
        i = l[1]
        j = l[2]
        R = np.identity(dim)
        cr = np.cos(theta * t)
        sr = np.sin(theta * t)
        R[i, i] = cr
        R[j, j] = cr
        R[i, j] = -sr
        R[j, i] = sr
        # tolR = R*tolR
        listOfR.append(R)
        # print tolR
    return listOfR


def GivensRotation(i, j, x1, x2, dim):
    R = np.identity(dim)
    r = np.sqrt(x1 * x1 + x2 * x2)
    cr = x1 / r
    sr = -x2 / r
    R[i, i] = cr
    R[j, j] = cr
    R[i, j] = -sr
    R[j, i] = sr
    # theta1 = math.acos(cr)
    # theta2 = math.asin(sr)
    theta = math.atan2(sr, cr)
    # print "Angle:", theta, theta2, theta3
    return R, theta


############################# utility ############################
# def gs(X):
#     Q, R = np.linalg.qr(X)
#     return Q

# this need to be fixed, if the rank is less than 4 the rest column should be zero
def gs(X, row_vecs=False, norm=True):
    if not row_vecs:
        X = X.T
    Y = X[0:1, :].copy()
    for i in range(1, X.shape[0]):
        proj = np.diag(np.nan_to_num((X[i, :].dot(Y.T) / np.linalg.norm(Y, axis=1) ** 2)).flat).dot(Y)
        Y = np.vstack((Y, X[i, :] - proj.sum(0)))
        # if X.shape[]
        # print Y
    if norm:
        Y = np.diag(1 / np.linalg.norm(Y, axis=1)).dot(Y)
        Y = np.nan_to_num(Y)
    if row_vecs:
        return Y
    else:
        return Y.T


def normalizeBasis(F):
    projDim = F.shape[1]
    # print "projDim:", projDim
    for i in range(0, projDim):
        F[:, i] = normalize(F[:, i])
    return F


def orthnogoalize(F):
    F[:, 1] = gram_schmidt(F[:, 0], F[:, 1])
    return F


def pricipalAngle(Fa, Fz):
    U, s, V = np.linalg.svd(np.transpose(Fa) * Fz)
    Va = np.matrix(U)
    Vz = np.matrix(V)
    Ga = Fa * Va
    Gz = Fz * Vz
    tau = np.arccos(s)
    # print ('principal angle', tau)


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def gram_schmidt(col1, col2):
    tol = 0.999999999
    n = col1.shape[0]
    ip = np.dot(np.transpose(col1), col2);
    # print "gram-schimidt-ip", ip

    if abs(ip) < tol:
        for j in range(n):
            col2[j] = col2[j] - ip * col1[j];
        normalize(col2);
    return col2