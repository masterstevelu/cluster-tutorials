#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
        MPI_Comm comm;
        int np, myid;
        char processor_name[MPI_MAX_PROCESSOR_NAME];
        int nameLen;

        MPI_Init(&argc, &argv);
        MPI_Comm_dup(MPI_COMM_WORLD, &comm);
        MPI_Comm_rank(comm, &myid);
        MPI_Comm_size(comm, &np);

        MPI_Get_processor_name(processor_name, &nameLen);

        printf("Process %d is running on %d processed!\n", myid, np);
        fprintf(stderr,"Process %d is alive on %s\n", myid, processor_name);

        MPI_Comm_free(&comm);
        MPI_Finalize();

        return 0;

}
