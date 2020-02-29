/**
 * \file taylorgreenib.cpp
 * \brief Implementation of the methods of the class TaylorGreenIBSolver.
 */

#include "taylorgreenib.h"

TaylorGreenIBSolver::TaylorGreenIBSolver(
    const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // TaylorGreenIBSolver::TaylorGreenIBSolver

TaylorGreenIBSolver::~TaylorGreenIBSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // TaylorGreenIBSolver::~TaylorGreenIBSolver

PetscErrorCode TaylorGreenIBSolver::init(
    const MPI_Comm &world, const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = RigidKinematicsSolver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(
        RigidKinematicsSolver::stageInitialize); CHKERRQ(ierr);

    ierr = setInitialSolution(RigidKinematicsSolver::t); CHKERRQ(ierr);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // TaylorGreenIBSolver::init

PetscErrorCode TaylorGreenIBSolver::setInitialSolution(const PetscReal &ti)
{
    PetscErrorCode ierr;
    DMDALocalInfo info;
    DM packer, u_da, v_da, p_da;
    Vec u, v;
    PetscReal nu = config["flow"]["nu"].as<PetscReal>();
    PetscReal a = 2 * PETSC_PI;

    PetscFunctionBeginUser;

    ierr = VecGetDM(solution->UGlobal, &packer); CHKERRQ(ierr);
    ierr = DMCompositeGetEntries(packer, &u_da, &v_da); CHKERRQ(ierr);
    ierr = DMCompositeGetAccess(packer, solution->UGlobal,
                                &u, &v); CHKERRQ(ierr);

    petibm::type::GhostedVec2D &coords_u = mesh->coord[0];
    PetscReal *xu = coords_u[0], *yu = coords_u[1];
    ierr = DMDAGetLocalInfo(u_da, &info); CHKERRQ(ierr);
    PetscReal **u_arr;
    ierr = DMDAVecGetArray(u_da, u, &u_arr); CHKERRQ(ierr);
    for (PetscInt j = info.ys; j < info.ys + info.ym; ++j)
    {
        for (PetscInt i = info.xs; i < info.xs + info.xm; ++i)
        {
            u_arr[j][i] = -PetscCosReal(a * xu[i]) *
                          PetscSinReal(a * yu[j]) *
                          PetscExpReal(-2 * a * a * ti * nu);
        }
    }
    ierr = DMDAVecRestoreArray(u_da, u, &u_arr); CHKERRQ(ierr);

    petibm::type::GhostedVec2D &coords_v = mesh->coord[1];
    PetscReal *xv = coords_v[0], *yv = coords_v[1];
    ierr = DMDAGetLocalInfo(v_da, &info); CHKERRQ(ierr);
    PetscReal **v_arr;
    ierr = DMDAVecGetArray(v_da, v, &v_arr); CHKERRQ(ierr);
    for (PetscInt j = info.ys; j < info.ys + info.ym; ++j)
    {
        for (PetscInt i = info.xs; i < info.xs + info.xm; ++i)
        {
            v_arr[j][i] = PetscSinReal(a * xv[i]) *
                          PetscCosReal(a * yv[j]) *
                          PetscExpReal(-2 * a * a * ti * nu);
        }
    }
    ierr = DMDAVecRestoreArray(v_da, v, &v_arr); CHKERRQ(ierr);

    ierr = DMCompositeRestoreAccess(packer, solution->UGlobal,
                                    &u, &v); CHKERRQ(ierr);

    ierr = VecGetDM(solution->pGlobal, &p_da); CHKERRQ(ierr);
    petibm::type::GhostedVec2D &coords_p = mesh->coord[3];
    PetscReal *xp = coords_p[0], *yp = coords_p[1];
    ierr = DMDAGetLocalInfo(p_da, &info); CHKERRQ(ierr);
    PetscReal **p_arr;
    ierr = DMDAVecGetArray(p_da, solution->pGlobal, &p_arr); CHKERRQ(ierr);
    for (PetscInt j = info.ys; j < info.ys + info.ym; ++j)
    {
        for (PetscInt i = info.xs; i < info.xs + info.xm; ++i)
        {
            p_arr[j][i] = -0.25 * (PetscCosReal(2 * a * xp[i]) +
                                   PetscCosReal(2 * a * yp[j])) *
                          PetscExpReal(-4 * a * a * ti * nu);
        }
    }
    ierr = DMDAVecRestoreArray(p_da, solution->pGlobal, &p_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // TaylorGreenIBSolver::setInitialSolution

PetscErrorCode TaylorGreenIBSolver::setVelocityBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;

    PetscFunctionBeginUser;

    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    PetscReal a = 2 * PETSC_PI;
    for (PetscInt k = body->bgPt; k < body->edPt; ++k)
    {
        UB_arr[k][0] = -PetscCosReal(a * coords[k][0]) *
                       PetscSinReal(a * coords[k][1]) *
                       PetscExpReal(-2 * a * a * ti * nu);
        UB_arr[k][1] = PetscSinReal(a * coords[k][0]) *
                       PetscCosReal(a * coords[k][1]) *
                       PetscExpReal(-2 * a * a * ti * nu);
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // TaylorGreenIBSolver::setVelocityBodies
