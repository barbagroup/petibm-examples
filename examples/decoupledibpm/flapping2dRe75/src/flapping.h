#include <petibm/rigidkinematics/rigidkinematics.h>

class FlappingSolver : protected RigidKinematicsSolver
{
public:
    FlappingSolver() = default;

    FlappingSolver(const MPI_Comm &world, const YAML::Node &node);

    ~FlappingSolver();

    using RigidKinematicsSolver::destroy;

    using RigidKinematicsSolver::advance;

    using RigidKinematicsSolver::write;

    using RigidKinematicsSolver::ioInitialData;

    using RigidKinematicsSolver::finished;

    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    PetscReal f;
    PetscReal A0;
    PetscReal alpha0;
    PetscReal beta;
    PetscReal phi;
    PetscReal c;
    PetscReal Xc0;
    PetscReal Yc0;

    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

}; // FlappingSolver
