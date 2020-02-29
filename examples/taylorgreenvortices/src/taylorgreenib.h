/**
 * \file taylorgreenib.h
 * \brief Definition of the class TaylorGreenIBSolver.
 */

#pragma once

#include <petibm/rigidkinematics/rigidkinematics.h>

#include "taylorgreen.h"

class TaylorGreenIBSolver : protected RigidKinematicsSolver
{
public:
    TaylorGreenIBSolver() = default;

    TaylorGreenIBSolver(const MPI_Comm &world, const YAML::Node &node);

    ~TaylorGreenIBSolver();

    using RigidKinematicsSolver::destroy;

    using RigidKinematicsSolver::advance;

    using RigidKinematicsSolver::write;

    using RigidKinematicsSolver::ioInitialData;

    using RigidKinematicsSolver::finished;

    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:

    PetscErrorCode setInitialSolution(const PetscReal &ti);

    PetscErrorCode setCoordinatesBodies(
        const PetscReal &ti){PetscFunctionReturn(0);};

    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // TaylorGreenIBSolver
