'''
Wrappers around several sparse system solvers
'''
from __future__ import unicode_literals, print_function, division, absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import range, object

import numpy as np
import scipy.sparse
import scipy.sparse.linalg

DefaultSolver = None

active = []
solvers = {}

try:
    from pymatsolver import MumpsSolver as _MumpsSolver
except (ImportError, SyntaxError):
    _MumpsSolver = None
else:
    active.append('mumps')

try:
    from pyMKL import pardisoSolver as _MKLPardisoSolver
except ImportError:
    _MKLPardisoSolver = None
else:
    active.append('mklpardiso')

try:
    from scipy.sparse.linalg import splu as _SuperLUSolver
except ImportError:
    _SuperLUSolver = None
else:
    active.append('splu')

if not active:
    raise ImportError('Problemo: could not load backend')


class BaseSolver(object):
    '''
    Wrapper around a direct sparse system solver.
    '''

    Solver = None

    def __init__(self, A=None):
        '''
        Initialize solver

        Args:
            A (sparse matrix): The matrix to solve
        '''

        self.A = A

    @property
    def Ainv(self):
        'Returns a Solver instance'

        if not hasattr(self, '_Ainv'):
            self._Ainv = self.Solver(self.A)
        return self._Ainv

    @property
    def A(self):
        'The system matrix'

        if not hasattr(self, '_A'):
            raise Exception('System matrix has not been set')
        return self._A
    @A.setter
    def A(self, A):
        if A is None:
            return
        if isinstance(A, scipy.sparse.spmatrix):
            self._A = A
        else:
            raise Exception('Class %s can only register SciPy sparse matrices'%(self.__class__.__name__,))

    @property
    def shape(self):
        return self.A.T.shape

    def __mul__(self, rhs):
        '''
        Carries out the action of solving for wavefields.

        Args:
            rhs (sparse matrix): Right-hand side vector(s)

        Returns:
            np.ndarray: Wavefields
        '''

        if isinstance(rhs, scipy.sparse.spmatrix):
            def qIter(qs):
                for j in range(qs.shape[1]):
                    qi = qs.getcol(j).toarray().ravel()
                    yield qi
                return
        else:
            def qIter(qs):
                for j in range(qs.shape[1]):
                    qi = qs[:, j]
                    yield qi
                return

        result = np.empty(rhs.shape, dtype=np.complex128)
        for i, q in enumerate(qIter(rhs)):
            result[:, i] = self._solve(q)

        return result

    def _solve(self, rhs):
        raise NotImplementedError


class MumpsSolver(BaseSolver):
    '''
    Wrapper around MUMPS, via pymatsolver
    '''

    Solver = _MumpsSolver

    def _solve(self, rhs):
        return self.Ainv * rhs

solvers['mumps'] = MumpsSolver


class MKLPardisoSolver(BaseSolver):
    '''
    Wrapper around MKL PARDISO, via pyMKL
    '''

    Solver = _MKLPardisoSolver

    @property
    def Ainv(self):
        'Returns a Solver instance'

        if getattr(self, '_Ainv', None) is None:
            self._Ainv = self.Solver(self.A, 13)
            self._Ainv.run_pardiso(12)
        return self._Ainv

    def _solve(self, rhs):
        return self.Ainv.run_pardiso(33, rhs)

    def __del__(self):
        if hasattr(self, '_Ainv'):
            self._Ainv.run_pardiso(-1)
            del self._Ainv

solvers['mklpardiso'] = MKLPardisoSolver


class SuperLUSolver(BaseSolver):
    '''
    Wrapper around SuperLU, via scipy.sparse.linalg.splu
    '''

    Solver = _SuperLUSolver

    def _solve(self, rhs):
        return self.Ainv.solve(rhs)

solvers['splu'] = SuperLUSolver


BestSolver = solvers[active[0]]
