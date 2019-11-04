#include <petibm/rigidkinematics/rigidkinematics.h>

#pragma once

class OscillatingSolver : public RigidKinematicsSolver
{
public:
    OscillatingSolver() = default;
    OscillatingSolver(const MPI_Comm &world, const YAML::Node &node);
    ~OscillatingSolver();
    using RigidKinematicsSolver::destroy;
    using RigidKinematicsSolver::advance;
    using RigidKinematicsSolver::write;
    using RigidKinematicsSolver::ioInitialData;
    using RigidKinematicsSolver::finished;
    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    PetscReal f;
    PetscReal Am;
    PetscReal Um;
    PetscReal Xc0;
    PetscReal Yc0;
    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

};  // OscillatingSolver
