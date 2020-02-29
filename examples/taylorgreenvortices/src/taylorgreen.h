/**
 * \file taylorgreen.h
 * \brief Definition of the class TaylorGreenSolver.
 */

#pragma once

#include <petibm/navierstokes/navierstokes.h>

class TaylorGreenSolver : protected NavierStokesSolver
{
public:
    TaylorGreenSolver() = default;

    TaylorGreenSolver(const MPI_Comm &world, const YAML::Node &node);

    ~TaylorGreenSolver();

    using NavierStokesSolver::destroy;

    using NavierStokesSolver::advance;

    using NavierStokesSolver::write;

    using NavierStokesSolver::ioInitialData;

    using NavierStokesSolver::finished;

    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    PetscErrorCode setInitialSolution(const PetscReal &ti);

}; // TaylorGreenSolver
