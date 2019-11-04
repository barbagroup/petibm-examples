#include "flapping.h"

#include <petibm/io.h>

FlappingSolver::FlappingSolver(const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // FlappingSolver::FlappingSolver

FlappingSolver::~FlappingSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // FlappingSolver::~FlappingSolver

PetscErrorCode FlappingSolver::init(const MPI_Comm &world,
                                    const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = RigidKinematicsSolver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    f = 0.0; A0 = 0.0; alpha0 = 0.0; beta = 0.0; phi = 0.0;
    c = 1.0; Xc0 = 0.0; Yc0 = 0.0;
    if (node["bodies"][0]["kinematics"])
    {
        const YAML::Node &config_kin = node["bodies"][0]["kinematics"];
        f = config_kin["f"].as<PetscReal>(0.0);
        A0 = config_kin["A0"].as<PetscReal>(0.0);
        alpha0 = config_kin["alpha0"].as<PetscReal>(0.0);
        beta = config_kin["beta"].as<PetscReal>(0.0);
        phi = config_kin["phi"].as<PetscReal>(0.0);
        c = node["c"].as<PetscReal>(1.0);
        Xc0 = config_kin["center"][0].as<PetscReal>(0.0);
        Yc0 = config_kin["center"][1].as<PetscReal>(0.0);
    }

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // FlappingSolver::init

PetscErrorCode FlappingSolver::setCoordinatesBodies(const PetscReal &ti)
{
    PetscReal Xd,  // displacement in the x-direction
              Yd;  // displacement in the y-direction
    PetscReal alpha;  // body orientation
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;
    petibm::type::RealVec2D &coords0 = body->coords0;

    PetscFunctionBeginUser;

    // compute the displacement
    Xd = A0/2 * PetscCosReal(2 * PETSC_PI * f * ti);
    Yd = 0.0;
    // compute the body orientation
    alpha = alpha0 + beta * PetscSinReal(2 * PETSC_PI * f * ti + phi);

    // apply rotation and translation
    PetscReal cos_alpha = PetscCosReal(alpha),
              sin_alpha = PetscSinReal(alpha);
    for (PetscInt k = 0; k < body->nPts; k++)
    {
        coords[k][0] = Xd + Xc0 \
                       + (coords0[k][0] - Xc0) * cos_alpha \
                       - (coords0[k][1] - Yc0) * sin_alpha;
        coords[k][1] = Yd + Yc0 \
                       + (coords0[k][0] - Xc0) * sin_alpha \
                       + (coords0[k][1] - Yc0) * cos_alpha;
    }

    PetscFunctionReturn(0);
} // FlappingSolver::setCoordinatesBodies

PetscErrorCode FlappingSolver::setVelocityBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscReal Xc,  // x-position of the center
              Yc;  // y-position of the center
    PetscReal Umax,  // maximum translational velocity in x-direction
              Ux,    // translation velocity in x-direction
              Uy;    // translation velocity in y-direction
    PetscReal Omega;  // angular velocity
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;

    PetscFunctionBeginUser;

    // compute the current position of the center
    Xc = Xc0 + A0/2 * PetscCosReal(2 * PETSC_PI * f * ti);
    Yc = Yc0;
    // compute the translational velocity at current time
    Umax = PETSC_PI * f * A0;
    Ux = - Umax * PetscSinReal(2 * PETSC_PI * f * ti);
    Uy = 0.0;
    // compute the angular velocity at current time
    Omega = 2 * PETSC_PI * f * beta * PetscCosReal(2 * PETSC_PI * f * ti + phi);
    // update the boundary velocity array
    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    for (PetscInt k = body->bgPt; k < body->edPt; k++)
    {
        UB_arr[k][0] = Ux - Omega * (coords[k][1] - Yc);
        UB_arr[k][1] = Uy + Omega * (coords[k][0] - Xc);
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // FlappingSolver::setVelocityBodies
