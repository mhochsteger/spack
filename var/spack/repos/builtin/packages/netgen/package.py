# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *

class Netgen(CMakePackage):
    """NETGEN is an automatic 3d tetrahedral mesh generator. It accepts
       input from constructive solid geometry (CSG) or boundary
       representation (BRep) from STL file format. The connection to
       a geometry kernel allows the handling of IGES and STEP files.
       NETGEN contains modules for mesh optimization and hierarchical
       mesh refinement. """

    homepage = "https://ngsolve.org/"
    git = "https://github.com/NGSolve/netgen.git"

    maintainers = ['mhochsteger']

    # TODO: multiple versions
    version('6.2.1910', tag='v6.2.1910', submodules=True)

    variant('native', default=True, description='Build/optimize for native CPU architecture')
    variant('python', default=True, description='Enable Python support')
    variant('mpi', default=True, description='Enable MPI support')

    extends('python', when='+python')
    depends_on('py-pybind11', when='+python', type=('build','run'))

    depends_on('zlib')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec
        check_spec = lambda s: 'ON' if '+'+s in spec else 'OFF'

        cmake_args = [
            '-DUSE_SUPERBUILD=OFF',
            '-DUSE_NATIVE_ARCH='+check_spec('native'),
            '-DUSE_PYTHON='+check_spec('python'),
            '-DUSE_MPI='+check_spec('mpi'),
            '-DUSE_GUI=OFF'
            ]

        if '+python' in spec:
            cmake_args.append('-DPYBIND_INDLUDE_DIR='+spec['py-pybind11'].prefix.include)
            cmake_args.append('-DNG_INSTALL_PYBIND=OFF')

        return cmake_args
