import logging
from typing import Any, List
from ortools.graph import pywrapgraph
import math
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from .compiler import compile, objdump
from .models import Function

logger = logging.getLogger("cpp-needle")

OMEGA = 3 / 2
ALPHA = 2
BETA = 1 / 2


def lcs(a: List[Any], b: List[Any]) -> int:
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return 0
    f = [0] * (nb + 1)
    f[1] = 1 if a[0] == b[0] else 0
    for i in range(1, na+1):
        g = [0] * (nb + 1)
        for j in range(1, nb+1):
            g[j] = max(f[j], g[j-1], f[j-1] + (1 if a[i-1] == b[j-1] else 0))
        f = g
    return f[nb]


def sigma(a: List[Any], b: List[Any]) -> int:
    w = int(round(OMEGA * len(a)))
    if w >= len(b):
        return lcs(a, b)
    return max((lcs(a, b[k:k+w]) for k in range(0, len(b) - w + 1)))


def _normalize(x: float) -> float:
    return 1 / (1 + math.exp(- ALPHA * x + BETA))


def _sigmawrap(arg):
    i, j, a, b = arg
    return i, j, sigma(a, b)


def _sigmainv(arg):
    i, j, a, b = arg
    return i, j, sigma(b, a)


def measure(src1: str, src2: str) -> float:
    proj1, proj2 = [objdump(compile(s)) for s in [src1, src2]]
    n1, n2 = len(proj1), len(proj2)

    logger.debug("Calculate sigmas.")

    opc = {}
    fi = []
    gi = []
    cnt = 0

    for f in proj1:
        t = [i.opcode for i in f]
        for i in range(len(t)):
            if t[i] not in opc:
                opc[t[i]] = cnt
                t[i] = cnt
                cnt += 1
            else:
                t[i] = opc[t[i]]
        fi.append(t)
    for f in proj2:
        t = [i.opcode for i in f]
        for i in range(len(t)):
            if t[i] not in opc:
                opc[t[i]] = cnt
                t[i] = cnt
                cnt += 1
            else:
                t[i] = opc[t[i]]
        gi.append(t)

    logger.debug(str(opc))

    # sigmas = [[sigma(fi[i], gi[j])
    #            for j in range(n2)] for i in range(n1)]
    # sigmainvs = [[sigma(gi[j], fi[i])
    #               for j in range(n2)] for i in range(n1)]

    items = [(i, j, fi[i], gi[j]) for i in range(n1) for j in range(n2)]
    sigmas = [[0 for j in range(n2)] for i in range(n1)]
    sigmainvs = [[0 for i in range(n1)] for j in range(n2)]

    def weight(i, j):
        val = max(sigmas[i][j], sigmainvs[j][i]) / min(len(proj1[i]), len(proj2[j]))
        return _normalize(val)

    with ProcessPoolExecutor() as pool:
        results = pool.map(_sigmawrap, items)
        for i, j, v in results:
            sigmas[i][j] = v
        results = pool.map(_sigmainv, items)
        for i, j, v in results:
            sigmainvs[j][i] = v

    logger.debug("Build weighted flow network graph.")

    def solve():
        mcf = pywrapgraph.SimpleMinCostFlow()

        S = n1 + n2
        T = S + 1

        for i in range(n1):
            c, w = len(proj1[i]), 0
            # logger.debug(f"edge {S} -> {i}, c: {c}, w: {w}")
            mcf.AddArcWithCapacityAndUnitCost(S, i, c, w)
            mcf.SetNodeSupply(i, 0)
        for i in range(n2):
            c, w = len(proj2[i]), 0
            # logger.debug(f"edge {n1+i} -> {T}, c: {c}, w: {w}")
            mcf.AddArcWithCapacityAndUnitCost(n1 + i, T, c, w)
            mcf.SetNodeSupply(n1 + i, 0)

        FACT = 10000

        for i in range(n1):
            for j in range(n2):
                c = sigmas[i][j]
                if c > 0:
                    w = int(round(weight(i, j) * FACT))
                    logger.debug(f"edge {i} -> {n1+j}, c: {c}, w: {w}")
                    mcf.AddArcWithCapacityAndUnitCost(
                        i, n1 + j, c, -w)

        supplies = sum((len(f) for f in proj1))

        logger.debug(f"supplies: {supplies}")

        mcf.SetNodeSupply(S, supplies)
        mcf.SetNodeSupply(T, -supplies)

        logger.debug("Solve weighted flow network graph.")

        status = mcf.SolveMaxFlowWithMinCost()

        if status != mcf.OPTIMAL:
            logger.error("Failed to calculate max cost flow.")

        cost = - mcf.OptimalCost() / FACT

        rawsim = cost / supplies

        sim = rawsim / _normalize(1)

        logger.info(
            f"Optimal cost: {cost}, raw similarity: {rawsim}, similarity: {sim}")

        return sim
    
    sim = solve()

    # return max(0.0, min(1.0, sim))

    proj1, proj2 = proj2, proj1
    sigmas, sigmainvs = sigmainvs, sigmas
    n1, n2 = n2, n1

    sim2 = solve()

    sim = (sim + sim2) / 2

    return max(0.0, min(1.0, sim))
