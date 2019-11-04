#include "oscillating.h"

#include <petibm/io.h>

OscillatingSolver::OscillatingSolver(const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // OscillatingSolver::OscillatingSolver

OscillatingSolver::~OscillatingSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // OscillatingSolver::~OscillatingSolver

PetscErrorCode OscillatingSolver::init(const MPI_Comm &world,
                                       const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = RigidKinematicsSolver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    const YAML::Node &config_kin = node["bodies"][0]["kinematics"];
    f = config_kin["f"].as<PetscReal>(0.0);
    PetscReal Dc = config_kin["D"].as<PetscReal>(1.0);
    PetscReal KC = config_kin["KC"].as<PetscReal>(0.0);
    Am = Dc * KC / (2.0 * PETSC_PI);
    Um = 2.0 * PETSC_PI * f * Am;
    Xc0 = config_kin["center"][0].as<PetscReal>(0.0);
    Yc0 = config_kin["center"][1].as<PetscReal>(0.0);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // OscillatingSolver::init

PetscErrorCode OscillatingSolver::setCoordinatesBodies(const PetscReal &ti)
{
    PetscReal Xd,  // displacement in the x-direction
              Yd;  // displacement in the y-direction
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;
    petibm::type::RealVec2D &coords0 = body->coords0;

    PetscFunctionBeginUser;

    // compute the displacement
    Xd = -Am * PetscSinReal(2*PETSC_PI * f * ti);
    Yd = 0.0;

    for (PetscInt k = 0; k < body->nPts; k++)
    {
        coords[k][0] = coords0[k][0] + Xd;
        coords[k][1] = coords0[k][1] + Yd;
    }

    PetscFunctionReturn(0);
} // OscillatingSolver::setCoordinatesBodies

PetscErrorCode OscillatingSolver::setVelocityBodies(
    const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscReal Ux;  // translation velocity in x-direction
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];

    PetscFunctionBeginUser;

    // compute the translational velocity at current time
    Ux = - Um * PetscCosReal(2 * PETSC_PI * f * ti);
    // update the boundary velocity array
    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    for (PetscInt k = body->bgPt; k < body->edPt; k++)
    {
        UB_arr[k][0] = Ux;
        UB_arr[k][1] = 0.0;
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // OscillatingSolver::setVelocityBodies
