/**
 * \file main.cpp
 * \brief Implementation of the PetIBM application for the 2D array of decaying vortices.
 */

#include <petscsys.h>
#include <yaml-cpp/yaml.h>

#include <petibm/parser.h>

#include "config.h"
#include "taylorgreen.h"
#include "taylorgreenib.h"

int main(int argc, char **argv)
{
    PetscErrorCode ierr;
    YAML::Node config;

    ierr = PetscInitialize(&argc, &argv, nullptr, nullptr); CHKERRQ(ierr);
    ierr = PetscLogDefaultBegin(); CHKERRQ(ierr);
    MPI_Comm comm = PETSC_COMM_WORLD;

    // Parse the YAML configuration file
    ierr = petibm::parser::getSettings(config); CHKERRQ(ierr);

    // Check command-line option to choose whether to consider an immersed body
    PetscBool with_ib = PETSC_FALSE;
    ierr = PetscOptionsHasName(nullptr, nullptr, "-with-ib",
                               &with_ib); CHKERRQ(ierr);

    if (with_ib)
    {
        // Create and initialize solver based on the decoupled IBPM
        TaylorGreenIBSolver solver;
        ierr = solver.init(comm, config); CHKERRQ(ierr);
        ierr = solver.ioInitialData(); CHKERRQ(ierr);
        // Advance solution in time
        while (!solver.finished())
        {
            ierr = solver.advance(); CHKERRQ(ierr);
            ierr = solver.write(); CHKERRQ(ierr);
        }
        // Finalize
        ierr = solver.destroy(); CHKERRQ(ierr);
    }
    else
    {
        // Create and initialize solver based on pure Navier-Stokes solver
        TaylorGreenSolver solver;
        ierr = solver.init(comm, config); CHKERRQ(ierr);
        ierr = solver.ioInitialData(); CHKERRQ(ierr);
        // Advance solution in time
        while (!solver.finished())
        {
            ierr = solver.advance(); CHKERRQ(ierr);
            ierr = solver.write(); CHKERRQ(ierr);
        }
        // Finalize
        ierr = solver.destroy(); CHKERRQ(ierr);
    }

    ierr = PetscFinalize(); CHKERRQ(ierr);

    return 0;
}  // main
