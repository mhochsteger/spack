# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *

class Ngsolve(CMakePackage):
    """NGSolve is a Finite Element library based on Netgen."""

    homepage = "https://ngsolve.org/"
    git = "https://github.com/NGSolve/ngsolve.git"

    maintainers = ['mhochsteger']

    patch('ngs_mumps_pord1.patch')

    version('6.2.1910', tag='v6.2.1910', preferred=True)
    version('master', branch='master')

    variant('native', default=True, description='Build/optimize for native CPU architecture')
    variant('python', default=True, description='Enable Python support')
    variant('mpi', default=True, description='Enable MPI support')

    extends('python', when='+python')
    depends_on('netgen+native', when='+native')
    depends_on('netgen~native', when='~native')
    depends_on('netgen+python', when='+python')
    depends_on('netgen~python', when='~python')
    depends_on('netgen+mpi', when='+mpi')
    depends_on('netgen~mpi', when='~mpi')

    depends_on('mumps+parmetis+metis', when='+mpi')

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DUSE_SUPERBUILD=OFF',
            '-DUSE_UMFPACK=OFF',
            '-DNETGEN_DIR='+spec['netgen'].prefix
            ]

        if '+python' in spec['netgen']:
            cmake_args.append('-DNETGEN_PYBIND_INCLUDE_DIR='+spec['py-pybind11'].prefix.include)

        if '+mpi' in spec:
            cmake_args.append('-DUSE_MUMPS=ON)')
            cmake_args.append('-DMUMPS_DIR='+spec['mumps'].prefix)
            cmake_args.append('-DPARMETIS_DIR='+spec['parmetis'].prefix)

        return cmake_args
