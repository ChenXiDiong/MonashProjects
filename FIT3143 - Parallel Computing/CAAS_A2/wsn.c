/*
S2 2023 FIT3143 Parallel Computing Assignment 2
Name: Chen Xi Diong
Student ID: 32722656
Email: cdio0004@student.monash.edu

Simulation program for a wireless sensor network (WSN) of EV charging nodes.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>

// Constants used for determining neighbours
#define SHIFT_ROW 0
#define SHIFT_COL 1
#define DISP 1
// Constants used for messaging with the base station
#define MSG_COORDS 0
#define MSG_EXIT 1
#define MSG_REPORT 2
#define MSG_FREE 3
#define REPLY_NEAREST 4
#define MSG_FIND_AVAI_NEIGHBOURS 5
#define REPLY_FIND_AVAI_NEIGHBOURS 6
#define REPLY_DONE 7
#define MSG_END 8
#define MSG_DONE 9
#define STATIONS 10
// Constants used for messaging between the charging stations
#define MSG_REQ_AVAI 11
#define REPLY_AVAI 12
// Constants used for logging a charging station
#define LOG_NORMAL 0
#define LOG_FULL 1
#define LOG_FREE 2
// Constants used for the report struct
#define REPORT_SIZE 6
#define NUM_NEIGHBOURS 4
// Constants used for logging the base station
#define INIT 0
#define REPORT_HEAVY 1
#define REPORT_FREE 2
#define EXIT 3
#define NUM_OF_REPORTS 50
// Default Values for User-defined Variables
#define NUM_CHARGING_PORTS 3 // k
#define CYCLES 24 // number of cycles
#define FULL_THRESHOLD 1 // if <30% of charging ports are available, station is heavily in use
#define FREE_THRESHOLD 2 // if >60% of charging ports are available, station is free

// C structures
struct report_t { 
    int hour;
    int minute;
    int second;
    int availability_count;
    int station_rank;
    int my_neighbours[NUM_NEIGHBOURS];
};

struct charging_port_t{
    int port_rank;
    int station_rank;
};

//Function Prototypes
int run_base_station(MPI_Comm world_comm);
int run_charging_station(MPI_Comm world_comm, MPI_Comm comm, int *dims);
void* runBaseMessenger(void *pArg);
void* runCSMessenger(void *pArg);
void* runChargingPort(void *pArg);
int baseLogFile(char *pFileName, struct report_t report, int *stations_available, int *station_coord_x, int *station_coord_y, double comm_time, int message_count, int report_type, int full_reports_received, int free_reports_received);
int stationLogFile(char *pFileName, struct report_t report, int* neighbours_available, int *other_neighbours, int log_type);
int find_neighbours_available(int* availability_list, int left, int right, int top, int bottom, MPI_Comm comm);

//Global Variables
int end = 0; // flag to indicate the end of the simulation
int* availability_arr; // array to store the availability of the charging ports
MPI_Datatype REPORT;
int left_neighbour, right_neighbour, top_neighbour, bottom_neighbour;
int wait = 1, finish = 0;
int reply_from_base = 0; 
int *otherstations, *neighbours_available;
int full_reports_received = 0, free_reports_received = 0;
int k, num_iters, full_thres, free_thres;

int main(int argc, char **argv)
{
    int ndims = 2, rank, size, provided; 
    int dims[ndims]; // dimensions of the cartesian grid
    MPI_Comm commEVCS;

    MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE, &provided);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Create MPI struct for the report
    struct report_t values;
	MPI_Datatype type[6] = { MPI_INT, MPI_INT, MPI_INT, MPI_INT, MPI_INT, MPI_INT };
	int blocklen[6] = { 1, 1, 1, 1, 1, 4};
	MPI_Aint disp[6];

	MPI_Get_address(&values.hour, &disp[0]);
	MPI_Get_address(&values.minute, &disp[1]);
    MPI_Get_address(&values.second, &disp[2]);
	MPI_Get_address(&values.availability_count, &disp[3]);
    MPI_Get_address(&values.station_rank, &disp[4]);
    MPI_Get_address(&values.my_neighbours, &disp[5]);

	//Make relative
    for(int i = 1; i < REPORT_SIZE; i++){
        disp[i] = disp[i] - disp[0];
    }
	disp[0]=0;

	MPI_Type_create_struct(REPORT_SIZE, blocklen, disp, type, &REPORT);
	MPI_Type_commit(&REPORT);

    // Split the communicator into 2 groups: base station and EV charging nodes
    MPI_Comm_split( MPI_COMM_WORLD, rank == 0, 0, &commEVCS);

    // Packing the user-defined variables
    char *pack;
    int pack_size;
    MPI_Pack_size(3, MPI_INT, MPI_COMM_WORLD, &pack_size); // k, full_thres, free_thres

    // Base station
    if (rank == 0){
        if(argc == 7){
            dims[0] = atoi(argv[1]);
            dims[1] = atoi(argv[2]);
            k = atoi(argv[3]);
            num_iters = atoi(argv[4]);
            full_thres = atoi(argv[5]);
            free_thres = atoi(argv[6]);
        }
        else{
            //Prompt the user to input for the (m x n) cartesian grid dimensions
            printf("Enter the dimensions of the cartesian grid (m x n): \n");
            scanf("%d %d", &dims[0], &dims[1]);

            /* Check if the input dimensions are valid 
            Base station: 1 process
            m x n grid of EV charging nodes: m*n processes
            */
            if(size != (dims[0]*dims[1] + 1)){
                printf("ERROR in dimensions. %d(m) * %d(n) + 1 != %d(size)\n", dims[0], dims[1], size);
                MPI_Finalize();
                return 0;        
            }

            // Prompt user for other parameters (k, cycles, full_thres, free_thres)
            printf("Enter the number of charging ports per station: \n");
            scanf("%d", &k);
            if(k <= 0){
                printf("ERROR: Invalid number of charging ports\n");
                printf("Setting number of charging ports to 3\n");
                k = NUM_CHARGING_PORTS;
            }

            printf("Enter the number of cycles: \n");
            scanf("%d", &num_iters);
            if(num_iters <= 0){
                printf("ERROR: Invalid number of cycles\n");
                printf("Setting number of cycles to 24\n");
                num_iters = CYCLES;
            }

            printf("Enter the threshold for heavily in use stations: \n");
            scanf("%d", &full_thres);
            if(full_thres <= 0){
                printf("ERROR: Invalid threshold\n");
                printf("Setting full threshold to 1\n");
                full_thres = FULL_THRESHOLD;
            }

            printf("Enter the threshold for free stations: \n");
            scanf("%d", &free_thres);
            if(free_thres <= 0){
                printf("ERROR: Invalid threshold\n");
                printf("Setting free threshold to 2\n");
                free_thres = FREE_THRESHOLD;
            }
        }

        // Broadcast the user-specified values to setup Charging Nodes 
        pack = (char*) malloc(pack_size * sizeof(char));
        int pos = 0;
        MPI_Bcast(dims, ndims, MPI_INT, 0, MPI_COMM_WORLD); // dimensions of the cartesian grid
        MPI_Pack(&k, 1, MPI_INT, pack, pack_size, &pos, MPI_COMM_WORLD); // number of charging ports per station
        MPI_Pack(&full_thres, 1, MPI_INT, pack, pack_size, &pos, MPI_COMM_WORLD); // threshold for heavily in use stations
        MPI_Pack(&free_thres, 1, MPI_INT, pack, pack_size, &pos, MPI_COMM_WORLD); // threshold for free stations
        MPI_Bcast(pack, pack_size, MPI_PACKED, 0, MPI_COMM_WORLD); // broadcast the packed values

        // Start Simulation
        run_base_station( MPI_COMM_WORLD);
    }
    //Charging Node
    else{
        // Receive the broadcasted dimensions to setup 
        MPI_Bcast(dims, ndims, MPI_INT, 0, MPI_COMM_WORLD); // dimensions of the cartesian grid
        pack = (char*) malloc((unsigned)pack_size);
        MPI_Bcast(pack, pack_size, MPI_PACKED, 0, MPI_COMM_WORLD); // broadcast the packed values
        int pos = 0;
        MPI_Unpack(pack, pack_size, &pos, &k, 1, MPI_INT, MPI_COMM_WORLD); // number of charging ports per station
        MPI_Unpack(pack, pack_size, &pos, &full_thres, 1, MPI_INT, MPI_COMM_WORLD); // threshold for heavily in use stations
        MPI_Unpack(pack, pack_size, &pos, &free_thres, 1, MPI_INT, MPI_COMM_WORLD); // threshold for free stations

        printf("k: %d, full_thres: %d, free_thres: %d\n", k, full_thres, free_thres);

        availability_arr = (int*) malloc(k * sizeof(int));
        // Initialize the availability array
        for(int i = 0; i < k; i++){
                availability_arr[i] = 1; // 1 = available, 0 = occupied
        }
        
        // Start Simulation
        run_charging_station( MPI_COMM_WORLD, commEVCS, dims );

    }

    free(pack);
    free(availability_arr);
    MPI_Type_free(&REPORT);
    MPI_Comm_free(&commEVCS);
    MPI_Finalize();
    return 0;

}

int run_base_station(MPI_Comm world_comm)
/*
This is the main function to simulate the base station.
Input:
    world_comm: the world communicator
*/
{
    int size, nStations, ticks = 0;
    int prev_alerts = 0, prev_free_reports = 0;
    MPI_Comm_size(world_comm, &size );

    nStations = size - 1;
    pthread_t tid;

    printf("Hello from Base Station\n");

    // Thread used for messaging between MPI Processes (Charging Stations).
    pthread_create(&tid, 0, runBaseMessenger, &nStations);

    while(ticks < num_iters){
        printf("Hour %d\n", ticks);
        sleep(6); // scale of 1 second = 10 minutes in real life
        printf("Alerts received: %d\n", full_reports_received - prev_alerts);
        printf("Free reports received: %d\n", free_reports_received - prev_free_reports);
        prev_alerts = full_reports_received;
        prev_free_reports = free_reports_received;
        ticks++;
    }

    printf("Shutting down for maintenance\n");

    end = 1; // set the end flag to 1 to signal the end of the simulation
    int buf;
    MPI_Request request[size-1];
    for(int i = 1; i < size; i++){
        MPI_Isend( &buf, 1, MPI_INT, i, MSG_END, world_comm, &request[i-1]);
    }
    MPI_Waitall(size-1, request, MPI_STATUSES_IGNORE);

    printf("End flag broadcasted\n");

    // Wait for all the charging stations to send confirmation messages
    while(wait){
        //Simply waiting for all the charging stations to send confirmation messages
    }

    printf("All stations have sent confirmation messages\n");

    for(int i = 1; i < size; i++){
        MPI_Isend( &buf, 1, MPI_INT, i, MSG_DONE, world_comm, &request[i-1]);
    }
    MPI_Waitall(size-1, request, MPI_STATUSES_IGNORE);

    pthread_join(tid, NULL);

    printf("All stations have shut down\n");
    printf("Goodbye from Base Station\n");

    return 0;
}

int run_charging_station(MPI_Comm world_comm, MPI_Comm comm, int *dims)
/*
This is the main function to simulate a charging node.
Input:
    world_comm: the world communicator
    comm: the communicator for the charging node (slave communicator)
    dims: the dimensions of the cartesian grid
*/
{
    int ndims=2, size, my_rank, reorder, my_cart_rank, ierr, worldSize;
    MPI_Comm comm2D;
    int coord[ndims];
    int wrap_around[ndims];

    MPI_Comm_size(world_comm, &worldSize); // size of the world communicator
    MPI_Comm_size(comm, &size); // size of the slave communicator
    MPI_Comm_rank(comm, &my_rank); // rank of the slave communicator

    printf("Hello from Charging Station %d\n", my_rank);
    fflush(stdout);

    MPI_Dims_create(size, ndims, dims);

    /* create cartesian mapping, periodic shift is false. */
    wrap_around[0] = 0;
    wrap_around[1] = 0;
    reorder = 0;
    ierr =0;
    ierr = MPI_Cart_create(comm, ndims, dims, wrap_around, reorder, &comm2D);
    if(ierr != 0) printf("ERROR[%d] creating CART\n",ierr);

    /* find my coordinates in the cartesian communicator group */
    MPI_Cart_coords(comm2D, my_rank, ndims, coord); //coordinates are returned into the coord array
    // Send coordinates to the base station
    MPI_Send( &coord[0], 1, MPI_INT, 0, MSG_COORDS, world_comm);
    MPI_Send( &coord[1], 1, MPI_INT, 0, MSG_COORDS, world_comm);


    /* use my cartesian coordinates to find my rank in group*/
    MPI_Cart_rank(comm2D, coord, &my_cart_rank);

    /* get my neighbours; axis is coordinate dimension of shift */
    MPI_Cart_shift(comm2D, SHIFT_ROW, DISP, &top_neighbour, &bottom_neighbour);
    MPI_Cart_shift(comm2D, SHIFT_COL, DISP, &left_neighbour, &right_neighbour);

    printf("Charging Station %d located at (%d, %d) has neighbours: left %d, right %d, top %d, bottom %d\n", my_cart_rank, coord[0], coord[1], left_neighbour, right_neighbour, top_neighbour, bottom_neighbour);
    fflush(stdout);

    /* Initial creation of the logs file */
    char filename[20];
    sprintf(filename, "station%d_log.txt", my_cart_rank);
    FILE *fp = fopen(filename, "w");
    fprintf(fp, "Station %d's Log File\n", my_cart_rank);
    fprintf(fp, "|  Hour  | Minute | Second | Availability |\n");
    fclose(fp);

    /* Instantiation of the Charging Station */
    pthread_t tid[k];
    pthread_t messenger_id;
    struct charging_port_t args[k];
    struct report_t reports[NUM_OF_REPORTS];
    struct timespec starts, time_elapseds, startb, time_elapsedb;
    int reported = 0; // flag to indicate if the charging station has reported to the base station
    int neighbour_availability_count = 0, availability_count; 
    int report_count = -1, requests_sent = 0;
    double time_with_base = 0.0, time_with_nodes = 0.0;
    int t = 0; //timer

    printf("Starting up Charging Station %d located at (%d, %d)\n", my_cart_rank, coord[0], coord[1]);
    fflush(stdout);

    // Starting up the charging ports
    for(int i = 0; i < k; i++){
        args[i].station_rank = my_cart_rank;
        args[i].port_rank = i;
        pthread_create(&tid[i], 0, runChargingPort, &args[i]);
    }

    // Thread used for messaging between MPI Processes (Charging Stations).
    pthread_create(&messenger_id, 0, runCSMessenger, &comm2D);

    neighbours_available = (int*) malloc(NUM_NEIGHBOURS * sizeof(int));
    // Initialize the neighbours_available array
    for(int i = 0; i < NUM_NEIGHBOURS; i++){
        neighbours_available[i] = -1;
    }

    // Each iter is 10 minutes
    while(!end){
        t += 10;
        availability_count = 0;
        sleep(1); // scale of 0.0001 second = 1 second in real life, 10 minutes = 600 seconds = 0.06 seconds (scaled)
        for(int i = 0; i < k; i++){
            availability_count += availability_arr[i];
        }

        report_count = (report_count + 1) % NUM_OF_REPORTS;
        reports[report_count].hour = t / 60;
        reports[report_count].minute = t % 60;
        reports[report_count].second = 0;
        reports[report_count].availability_count = availability_count;
        reports[report_count].station_rank = my_rank;
        reports[report_count].my_neighbours[0] = left_neighbour;
        reports[report_count].my_neighbours[1] = right_neighbour;
        reports[report_count].my_neighbours[2] = top_neighbour;
        reports[report_count].my_neighbours[3] = bottom_neighbour;

        // Log current report to a file
        stationLogFile(filename, reports[report_count], neighbours_available, otherstations, LOG_NORMAL);

        if(availability_count <= full_thres){
            // Time the communication
            clock_gettime(CLOCK_MONOTONIC, &starts);

            neighbour_availability_count = find_neighbours_available(neighbours_available, left_neighbour, right_neighbour, top_neighbour, bottom_neighbour, comm2D);

            clock_gettime(CLOCK_MONOTONIC, &time_elapseds);
            time_with_nodes += (time_elapseds.tv_nsec - starts.tv_nsec);

            if(!neighbour_availability_count && !reported){
                // Time the communication
                clock_gettime(CLOCK_MONOTONIC, &startb);

                reply_from_base = 0;
                MPI_Send( &reports[report_count], 1, REPORT, 0, MSG_REPORT, world_comm);
                reported = 1;
                
                while(!reply_from_base){
                    // Waiting for the base station to reply
                }

                requests_sent++;

                clock_gettime(CLOCK_MONOTONIC, &time_elapsedb);
                time_with_base += (time_elapsedb.tv_nsec - startb.tv_nsec);
                
            }


            // Log to a file
            stationLogFile(filename, reports[report_count], neighbours_available, otherstations, LOG_FULL);
        }

        else if(availability_count >= free_thres && reported){
            // Time the communication
            clock_gettime(CLOCK_MONOTONIC, &startb);

            // Notify the base station that the charging station is free
            MPI_Send( &reports[report_count], 1, REPORT, 0, MSG_FREE, world_comm); 

            reported = 0;

            clock_gettime(CLOCK_MONOTONIC, &time_elapsedb);
            time_with_base += (time_elapsedb.tv_nsec - startb.tv_nsec);

            // Log to a file
            stationLogFile(filename, reports[report_count], neighbours_available, otherstations, LOG_FREE);
        }
    
    }

    printf("Station %d sending confirmation to base\n", my_rank);
    fflush(stdout);
    int dummy = 0;
    MPI_Send( &dummy, 1, MPI_INT, 0, REPLY_DONE, MPI_COMM_WORLD);

    while(!finish){
        // Waiting for all communications to end
    }

    for(int i = 0; i < k; i++){
        pthread_join(tid[i], NULL);
    }

    pthread_join(messenger_id, NULL);

    MPI_Send( &reports[report_count], 1, REPORT, 0, MSG_EXIT, world_comm); // notifies base station that the charging station has shut down

    printf("Charging Station %d has shut down\n", my_cart_rank);

    fp = fopen(filename, "a");
    fprintf(fp, "-------------------------------------------------------------------------\n");
    fprintf(fp, "Station has shut down\n");
    fprintf(fp, "Total number of requests sent: %d\n", requests_sent);
    fprintf(fp, "Total communication time with base(nanoseconds): %.2f\n", time_with_base);
    fprintf(fp, "Total communication time with other stations(nanoseconds): %.2f\n", time_with_nodes);
    fclose(fp);
    
    free(neighbours_available);
    MPI_Comm_free( &comm2D );
    return 0;
}

void* runBaseMessenger(void *pArg)
/*
This is the thread function that simulates the base station messenger.
Input:
    pArg[0]: number of charging nodes
*/
{
    int nStations, station, dummy = 0, avai_count;
    MPI_Status status;
    struct report_t report;
    int *reports, *stations_available, *neighbours_available, *station_coord_x, *station_coord_y;
    int* p = (int*)pArg;
    nStations = *p;
    int done_count = 0;
    struct timespec start, end;
    double time_taken = 0.0, total_time = 0.0;
    int messages = 0, total_msgs = 0;

    reports = (int*) malloc((nStations) * sizeof(int));
    stations_available = (int*) malloc((nStations) * sizeof(int));
    neighbours_available = (int*) malloc(NUM_NEIGHBOURS * sizeof(int));
    station_coord_x = (int*) malloc((nStations) * sizeof(int));
    station_coord_y = (int*) malloc((nStations) * sizeof(int));
    
    for(int i = 0; i < nStations; i++){
        reports[i] = 0;
    }

    // Receiving the coordinates of all the charging stations
    MPI_Request requests[nStations*2];
    for(int i = 0; i < nStations; i++){
        MPI_Irecv(&station_coord_x[i], 1, MPI_INT, i+1, MSG_COORDS, MPI_COMM_WORLD, &requests[i]);
        MPI_Irecv(&station_coord_y[i], 1, MPI_INT, i+1, MSG_COORDS, MPI_COMM_WORLD, &requests[i+nStations]);
    }
    MPI_Waitall(nStations*2, requests, MPI_STATUSES_IGNORE);

    baseLogFile("log.txt", report, stations_available, station_coord_x, station_coord_y, time_taken, messages, INIT, full_reports_received, free_reports_received);

    while (nStations > 0) {
        MPI_Recv(&report, 1, REPORT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status );
        switch (status.MPI_TAG) {
            case MSG_EXIT: // charging station has shut down
                nStations--;
                break;
        
            case MSG_REPORT: // charging station has sent a report that it is heavily in use
                full_reports_received++;
                station = status.MPI_SOURCE;
                reports[station-1] = 1;

                // Time the communication between the base station and the charging station
                clock_gettime(CLOCK_MONOTONIC, &start);

                /* Finding availability of neighbours of neighbours */
                // Reset the availability of all stations
                for(int i = 0; i < nStations; i++){
                    stations_available[i] = 0;
                }

                avai_count = 0;
                MPI_Request request_s[NUM_NEIGHBOURS];
                MPI_Request request_r[NUM_NEIGHBOURS];
                for(int i = 0; i < NUM_NEIGHBOURS; i++){
                    if(report.my_neighbours[i] > 0 && reports[report.my_neighbours[i]] == 0){
                        // Send a request for available neighbours to all (quadrant not fully occupied) neighbours
                        MPI_Isend( &dummy, 1, MPI_INT, report.my_neighbours[i], MSG_FIND_AVAI_NEIGHBOURS, MPI_COMM_WORLD, &request_s[avai_count]);
                        // Receive the rank of available neighbours from the charging station
                        MPI_Irecv( neighbours_available, 4, MPI_INT, report.my_neighbours[i], REPLY_FIND_AVAI_NEIGHBOURS, MPI_COMM_WORLD, &request_r[avai_count]);

                        for(int i = 0; i < NUM_NEIGHBOURS; i++){
                            if(neighbours_available[i] >= 0){
                                stations_available[neighbours_available[i]] = 1;
                            }
                        }

                        avai_count++; // Count the number of neighbours whose quadrants are not fully occupied
                    }
                }

                // Wait for all the requests to be completed
                MPI_Waitall(avai_count, request_s, MPI_STATUSES_IGNORE);
                MPI_Waitall(avai_count, request_r, MPI_STATUSES_IGNORE);

                MPI_Send( &avai_count, 1, MPI_INT, station, REPLY_NEAREST, MPI_COMM_WORLD); // send the number of available neighbours to the charging station
                MPI_Send( stations_available, nStations, MPI_INT, station, STATIONS, MPI_COMM_WORLD);

                clock_gettime(CLOCK_MONOTONIC, &end);
                time_taken = (end.tv_nsec - start.tv_nsec);
                total_time += time_taken;

                /*Number of messages exchanged
                received report (1) 
                [sent request to neighbours (1) + received reply from neighbours (1)] * number of available neighbours
                notify reporting station (1)
                send available neighbours (1)
                */ 
                messages = 3 + 2*avai_count;
                total_msgs += messages; 

                // Log the report
                baseLogFile("log.txt", report, stations_available, station_coord_x, station_coord_y, time_taken, messages, REPORT_HEAVY, full_reports_received, free_reports_received);

                break;

            case MSG_FREE: // charging station has sent a report that it is free
                free_reports_received++;
                station = status.MPI_SOURCE;
                reports[station-1] = 0;
                time_taken = 0.0;
                messages = 1; //Received report
                total_msgs += messages; 
                baseLogFile("log.txt", report, stations_available, station_coord_x, station_coord_y, time_taken, messages, REPORT_FREE, full_reports_received, free_reports_received);
                break;

            case REPLY_DONE:
                done_count++;
                if(done_count == nStations){
                    wait = 0;
                }
                break;


            default:
                printf("Error Tag");
                break;
        }
    }

    baseLogFile("log.txt", report, stations_available, station_coord_x, station_coord_y, total_time, total_msgs, EXIT, full_reports_received, free_reports_received);
    free(station_coord_x);
    free(station_coord_y);
    free(neighbours_available);
    free(stations_available);
    free(reports);
    return 0;
}

void* runCSMessenger(void *pArg)
/*
This is the thread function that simulates the charging node messenger.
Input:
    pArg[0]: communicator for the charging node.
*/
{
    int station, incoming_msg, my_rank, size, availability_count;
    MPI_Status status;
    MPI_Comm comm = *(MPI_Comm*)pArg;

    MPI_Comm_rank(comm, &my_rank);
    MPI_Comm_size(comm, &size);

    otherstations = (int*) malloc(size * sizeof(int));

    printf("Hello from Station %d's Messenger\n", my_rank);

    // Wait for all communication to be completed
    int from_base = 0, buf;

    while (!finish) {
        MPI_Iprobe(MPI_ANY_SOURCE, MSG_REQ_AVAI, comm, &incoming_msg, &status);
        if(incoming_msg){
            station = status.MPI_SOURCE;
            MPI_Recv( &buf, 1, MPI_INT, station, MSG_REQ_AVAI, comm, &status);
            availability_count = 0;
            for(int i = 0; i < k; i++){
                availability_count += availability_arr[i];
            }
            MPI_Send( &availability_count, 1, MPI_INT, station, REPLY_AVAI, comm);
        }
        
        // Check for confirmation message from base station to shut down
        MPI_Iprobe(0, MPI_ANY_TAG, MPI_COMM_WORLD, &from_base, MPI_STATUS_IGNORE);
        if(from_base){
            MPI_Recv( &buf, 1, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            switch(status.MPI_TAG){
                case MSG_END:
                    end = 1;
                    break;

                case MSG_FIND_AVAI_NEIGHBOURS:
                    find_neighbours_available(neighbours_available, left_neighbour, right_neighbour, top_neighbour, bottom_neighbour, comm);
                    if(neighbours_available[0]) neighbours_available[0] = left_neighbour;
                    if(neighbours_available[1]) neighbours_available[1] = right_neighbour;
                    if(neighbours_available[2]) neighbours_available[2] = top_neighbour;
                    if(neighbours_available[3]) neighbours_available[3] = bottom_neighbour;
                    MPI_Send(neighbours_available, 4, MPI_INT, status.MPI_SOURCE, REPLY_FIND_AVAI_NEIGHBOURS, MPI_COMM_WORLD);
                    break;

                case MSG_DONE:
                    finish = 1;
                    break;

                case REPLY_NEAREST:
                    MPI_Recv( otherstations, size, MPI_INT, 0, STATIONS, MPI_COMM_WORLD, &status); 
                    reply_from_base = 1;
                    break;

                default:
                    printf("Error Tag");
                    break;
                
            }
            
        }
    }

    printf("Goodbye from Station %d's Messenger\n", my_rank);
    
    free(otherstations);
    return 0;
}

void* runChargingPort(void *pArg){
/* Function that simulates the use of a charging port. Updates its availability to the charging node via the shared availability array.
Input:
    pArg[0]: struct charging_port_t containing the rank of the charging station and the rank of the charging port
*/
    struct charging_port_t* args = (struct charging_port_t*) pArg;
    int port_rank = args -> port_rank;
    int station_rank = args -> station_rank;
    double charging_time, free_time;

    /* Setting up the charging port*/
    srand(port_rank + station_rank); // seed the random number generator

    while(!end){
        // generate a random charging time between 1 to 10 hours(scale of 1 second = 10 minutes in real life)
        charging_time = (rand() % 480 + 1) / 10.0;
        availability_arr[port_rank] = 0; // charging port is occupied
        sleep(charging_time); // simulate the charging time
        availability_arr[port_rank] = 1; // charging port is available again
        free_time = (rand() % 180 + 1) / 10.0; // generate a random charging time within 1 hour
        sleep(free_time); // simulate the unoccupied time
    }
    
    return 0;
}

int baseLogFile(char *pFileName, struct report_t report, int *stations_available, int *station_coord_x, int *station_coord_y, double comm_time, int message_count, int report_type, int full_reports_received, int free_reports_received){
/* 
Function invoked by the base station to log the received report into a file.
Input:
    pFileName: name of the log file
    report: the report received from the charging node
    stations_available: array containing the availability of all the charging nodes
    station_coord_x: array containing the x coordinates of all the charging nodes
    station_coord_y: array containing the y coordinates of all the charging nodes
    comm_time: time taken for the communication between the base station and the charging node
    message_count: number of messages exchanged between the base station and the charging node
    report_type: type of report received (INIT, REPORT_HEAVY, REPORT_FREE, EXIT)
    full_reports_received: number of full reports received
    free_reports_received: number of free reports received
*/
    FILE *fp;
    fp = fopen(pFileName, "a");
    if(fp == NULL){
        printf("Error opening file\n");
        return 0;
    }

    switch(report_type){
        case INIT:
            fprintf(fp, "Base Station's Log File\n");
            fprintf(fp, "------------------------------------------------------------------------------------\n");
            break;

        case REPORT_HEAVY:
            fprintf(fp, "Full Report %d\n", full_reports_received);
            fprintf(fp, "Time is %d:%d:%d\n", report.hour, report.minute, report.second);
            fprintf(fp, "Received report from heavily-in-use station %d at (%d,%d), current availability is %d port(s)\n", report.station_rank, station_coord_x[report.station_rank], station_coord_y[report.station_rank], report.availability_count);
            fprintf(fp, "Sent available neighbouring stations nearby: \n");
            int size, avai_count = 0;
            MPI_Comm_size(MPI_COMM_WORLD, &size);
            for(int i = 0; i < size-1; i++){
                int is_neighbour = i == left_neighbour || i == right_neighbour || i == top_neighbour || i == bottom_neighbour;
                if(i != report.station_rank && !is_neighbour && stations_available[i] > 0){
                    fprintf(fp, "Station %d at (%d,%d)\n", i, station_coord_x[i], station_coord_y[i]);
                    avai_count++;
                } 
            }
            if(avai_count){ 
                fprintf(fp, "\n");
            }
            else{
                fprintf(fp, "None\n");
            }
            fprintf(fp, "Communication Time (nanoseconds): %.2f\n", comm_time);
            fprintf(fp, "Number of messages exchanged: %d\n", message_count);
            fprintf(fp, "------------------------------------------------------------------------------------\n");
            break;

        case REPORT_FREE:
            fprintf(fp, "Free Report %d\n", free_reports_received);
            fprintf(fp, "Time is %d:%d:%d\n", report.hour, report.minute, report.second);
            fprintf(fp, "Received report from free station %d at (%d,%d), current availability is %d port(s)\n", report.station_rank, station_coord_x[report.station_rank], station_coord_y[report.station_rank], report.availability_count);
            fprintf(fp, "Number of messages exchanged: %d\n", message_count);
            fprintf(fp, "------------------------------------------------------------------------------------\n");
            break;

        case EXIT:
            fprintf(fp, "Base Station has shut down\n");
            fprintf(fp, "Total Full Reports (Alerts) Received: %d\n", full_reports_received);
            fprintf(fp, "Total Free Reports Received: %d\n", free_reports_received);
            fprintf(fp, "Total Messages Exchanged: %d\n", message_count);
            fprintf(fp, "Total Communication Time (nanoseconds): %.2f\n", comm_time);
            break;
    }
        
    fclose(fp);
    return 1;
}

int stationLogFile(char *pFileName, struct report_t report, int* neighbours_available, int *other_neighbours, int log_type){
/* 
Function invoked by the charging node to log the new report entry into a file.
Input:
    pFileName: name of the log file
    report: the report received from the charging node
    neighbours_available: array containing the availability of all the neighbouring charging nodes
    other_neighbours: array containing the rank of all the neighbouring charging nodes
    log_type: type of log entry (LOG_NORMAL, LOG_FULL, LOG_FREE)
*/
    FILE *fp;
    fp = fopen(pFileName, "a");
    if(fp == NULL){
        printf("Error opening file\n");
        return 0;
    }

    switch(log_type){
        case LOG_NORMAL:
            fprintf(fp, "|%8d|%8d|%8d|%14d|\n", report.hour, report.minute, report.second, report.availability_count);
            break;

        case LOG_FULL:
            int avai_count = 0;
            fprintf(fp, "-------------------------------------------------------------------------\n");
            fprintf(fp, "Station %d is heavily in use at %d:%d:%d, current availability is %d port(s)\n", report.station_rank, report.hour, report.minute, report.second, report.availability_count);
            fprintf(fp, "Available neighbouring stations: ");
            for(int i = 0; i < NUM_NEIGHBOURS; i++){
                if(neighbours_available[i] > 0){
                    fprintf(fp, "%d ", report.my_neighbours[i]);
                    avai_count++;
                }
            }

            if(avai_count){
                fprintf(fp, "\n");
            }
            else{ 
                fprintf(fp, "None\n");
                fprintf(fp, "Nearest available stations from base: ");
                int size, is_me_or_neighbour;
                avai_count = 0;
                MPI_Comm_size(MPI_COMM_WORLD, &size);
                for(int i = 0; i < size-1; i++){
                    is_me_or_neighbour =  i == report.station_rank || i == left_neighbour || i == right_neighbour || i == top_neighbour || i == bottom_neighbour;
                    if(!is_me_or_neighbour && other_neighbours[i] > 0){
                        fprintf(fp, "%d ", i);
                        avai_count++;
                    }
                }
                if(avai_count){
                fprintf(fp, "\n");
                }
                else{ 
                    fprintf(fp, "None\n");
                }
            }
            fprintf(fp, "-------------------------------------------------------------------------\n");
            break;

        case LOG_FREE:
            fprintf(fp, "-------------------------------------------------------------------------\n");
            fprintf(fp, "Station %d is free at %d:%d:%d, current availability is %d port(s)\n", report.station_rank, report.hour, report.minute, report.second, report.availability_count);
            fprintf(fp, "-------------------------------------------------------------------------\n");
            break;
    }

    fclose(fp);
    return 1;
    
}

int find_neighbours_available(int* availability_list, int left, int right, int top, int bottom, MPI_Comm comm){
/*
Function to find the number of neighbouring charging nodes that are available.
Input:
    availability_list: array to store the availability of the neighbouring charging nodes
    left: rank of the left neighbour
    right: rank of the right neighbour
    top: rank of the top neighbour
    bottom: rank of the bottom neighbour
    comm: communicator of the charging node (cartesian grid communicator)
*/
    int neighbours_available = 0, dummy = 0, num_neighbours = 0;
    int left_nac = -1, right_nac = -1, top_nac = -1, bottom_nac = -1;
    int my_rank;
    MPI_Comm_rank(comm, &my_rank);
    MPI_Request request_s[NUM_NEIGHBOURS];
    MPI_Request request_r[NUM_NEIGHBOURS];

    if(left >= 0){
        MPI_Isend( &dummy, 1, MPI_INT, left, MSG_REQ_AVAI, comm, &request_s[num_neighbours]);
        MPI_Irecv( &left_nac, 1, MPI_INT, left, REPLY_AVAI, comm, &request_r[num_neighbours]);

        num_neighbours++;
        
    }

    if(right >= 0){
        MPI_Isend( &dummy, 1, MPI_INT, right, MSG_REQ_AVAI, comm, &request_s[num_neighbours]);
        MPI_Irecv( &right_nac, 1, MPI_INT, right, REPLY_AVAI, comm, &request_r[num_neighbours]);

        num_neighbours++;
    }

    if(top >= 0){
        MPI_Isend( &dummy, 1, MPI_INT, top, MSG_REQ_AVAI, comm, &request_s[num_neighbours]);
        MPI_Irecv( &top_nac, 1, MPI_INT, top, REPLY_AVAI, comm, &request_r[num_neighbours]);

        num_neighbours++;
    }

    if(bottom >= 0){
        MPI_Isend( &dummy, 1, MPI_INT, bottom, MSG_REQ_AVAI, comm, &request_s[num_neighbours]);
        MPI_Irecv( &bottom_nac, 1, MPI_INT, bottom, REPLY_AVAI, comm, &request_r[num_neighbours]);

        num_neighbours++;
    }

    MPI_Waitall(num_neighbours, request_s, MPI_STATUSES_IGNORE);
    MPI_Waitall(num_neighbours, request_r, MPI_STATUSES_IGNORE);

    if(left_nac > free_thres){
            neighbours_available++;
            availability_list[0] = 1;
    }
    else
        availability_list[0] = -1;

    if(right_nac > free_thres){
        neighbours_available++;
        availability_list[1] = 1;
    }
    else
        availability_list[1] = -1;
    
    if(top_nac > free_thres){
        neighbours_available++;
        availability_list[2] = 1;
    }
    else
        availability_list[2] = -1;

    if(bottom_nac > free_thres){
        neighbours_available++;
        availability_list[3] = 1;
    }
    else
        availability_list[3] = -1;

    return neighbours_available;
}
