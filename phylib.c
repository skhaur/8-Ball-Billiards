#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "phylib.h"


//function to allocate memory for a new object
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){

    //mallocing space for new object of size phylib_object
    phylib_object *newObject = malloc(sizeof(phylib_object));
    
    //if space is correctly allocated
    if (newObject != NULL) {
        //the new objects type is set to a still ball
        newObject->type = PHYLIB_STILL_BALL;
        //the number of the new ball is set to parameter sent
        newObject->obj.still_ball.number = number;
        //the position is set to parameter sent in
        newObject->obj.still_ball.pos = *pos;

        //returning the newly malloced object
        return newObject;
    } else {
        //we return null if space is incorrectly malloced
        return NULL;
    }

}

/* the below functions wil do the same thing as phylib_new_still_ball for thier own 
respective structures */
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){

    //mallocing space for a new object
    phylib_object *newObject = malloc(sizeof(phylib_object));

    if (newObject != NULL){
        //setting the new object type to rolling ball
        newObject->type = PHYLIB_ROLLING_BALL;
        //using the parameters to fill in the information for the new object
        newObject->obj.rolling_ball.number = number;
        newObject->obj.rolling_ball.pos = *pos;
        newObject->obj.rolling_ball.vel = *vel;
        newObject->obj.rolling_ball.acc = *acc;

        return newObject;
    } else {
        return NULL;
    }

}

phylib_object *phylib_new_hole(phylib_coord *pos){

    //new hole object created and malloced
    phylib_object *newHole = malloc(sizeof(phylib_object));
    
    //if new hole is properly allocated space
    if (newHole != NULL) {
        //we change the type of the object to a new PHYLIB_HOLE
        newHole->type = PHYLIB_HOLE;
        //new hole object's hole's position is set to the position parameter sent to the function
        newHole->obj.hole.pos = *pos;
        //we return the new hole
        return newHole;

    } else {
        //other wise we return null
        return NULL;
    }

}

phylib_object *phylib_new_hcushion(double y){

    //creating a new horizontal cushion
    phylib_object *newHCushion = malloc(sizeof(phylib_object));
    //if the memory is correctly allocated
    if (newHCushion != NULL) {
        //we set the type to a phylib horizontal cushion
        newHCushion->type = PHYLIB_HCUSHION;
        //and we update its cushion vector y, to the sent parameter. 
        newHCushion->obj.hcushion.y = y;
        //we then return the newly created cushion object
        return newHCushion;

    } else {

        return NULL;
    }

}

phylib_object *phylib_new_vcushion(double x){

    //creating a new vertical cushion
    phylib_object *newVCushion = malloc(sizeof(phylib_object));
    //if the memory is correctly allocated
    if (newVCushion != NULL) {
        //we set the type to a phylib vertical cushion
        newVCushion->type = PHYLIB_VCUSHION;
        //and we update its cushion vector x, to the sent parameter. 
        newVCushion->obj.vcushion.x = x;
        //we then return the newly created cushion object
        return newVCushion;

    } else {

        return NULL;
    }

}

//function to allocate memory for a table structure, we return null for failure to allocate
phylib_table *phylib_new_table( void ){

    phylib_table *newTable = malloc(sizeof(phylib_table));

    if (newTable != NULL) {

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            newTable->object[i] = NULL;
        }

        newTable->time = 0.0;

        //adding the cushions
        newTable->object[0] = phylib_new_hcushion(0.0);
        newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
        newTable->object[2] = phylib_new_vcushion(0.0);
        newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

        //creating array of holes of type phylib_coord
        phylib_coord holePositions[6];
        //depending on array, we access the correspinding index and insert values for the members
        holePositions[0].x = 0.0;
        holePositions[0].y = 0.0;

        holePositions[1].x = 0.0;
        holePositions[1].y = PHYLIB_TABLE_WIDTH;

        holePositions[2].x = 0.0;
        holePositions[2].y = PHYLIB_TABLE_LENGTH;

        holePositions[3].x = PHYLIB_TABLE_WIDTH;
        holePositions[3].y = 0.0;

        holePositions[4].x = PHYLIB_TABLE_WIDTH;
        holePositions[4].y = PHYLIB_TABLE_WIDTH;

        holePositions[5].x = PHYLIB_TABLE_WIDTH;
        holePositions[5].y = PHYLIB_TABLE_LENGTH;

        //for loop to add in the holes, and free if adding in the values fails. 
        for (int i = 4, j = 0; i < 10; i++, j++) {
            newTable->object[i] = phylib_new_hole(&holePositions[j]);
            if (newTable->object[i] == NULL) {
                phylib_free_table(newTable);
                return NULL;
            }
        }

        return newTable;
    }
    return NULL;
}

//part 2

//utility function which alocates new memory for an object. 
void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    //if the source doesnt point to NULL and its pointer, this means we are pointing to nothing
    if (src != NULL && *src != NULL) {

        //we malloc for the destination, the size of the object we are making room for
        *dest = malloc(sizeof(phylib_object));
        //if the destination memory allocation does not fail
        if (*dest != NULL) {
            //we then use memcpy to copy over the source to the destintation, the size being the object
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    //otherwise, if our source is pointing to NULL, our destination will also point to NULL
    } else {
        *dest = NULL;
    }    

}

//function to allocate memory for a new phylib table
phylib_table *phylib_copy_table( phylib_table *table ){

    //if the original table points to NULL memory location, we return null
    if (table == NULL) {
        return NULL;
    }
    //mallocing new table, size of the phylib_table
    phylib_table *copyTable = malloc(sizeof(phylib_table));

    //if the memory does not properly allocate, we simply return NULL
    if (copyTable == NULL) {
        return NULL;
    }
    //the objects for the new table are now going to be null
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        //the objects of the table are pointing to null
        copyTable->object[i] = NULL;
    }
    //theres only one time, so we copy that over
    double tableTime = table->time;
    copyTable->time = tableTime;

    //loop to iterate through all of the objects on the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            phylib_copy_object(&(copyTable->object[i]), &(table->object[i]));
            if (copyTable->object[i] == NULL) {
                //cleaning up for failure
                for (int j = 0; j < i; j++) {
                    //freeing previous copied objects
                    free(copyTable->object[j]);
                }
                //freeing the table
                free(copyTable); 
                return NULL;
            }
        }
    }
    //we return the new table
    return copyTable;
}

//function to iterate over the object array in the table until iteration finds a null
void phylib_add_object( phylib_table *table, phylib_object *object ){

    //if the object is null and so is the table we simply return doing nothing
    if (object == NULL) {

        return;

    } else if (table == NULL) {

        return;

    } else {
        //when we find an empty object space pointing to null we add the object to the table
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            //if object is null, means theres space
            if (table->object[i] == NULL) {
                //set the space to the object
                table->object[i] = object;
                break;

            }
        }
        return;
    }
    
}

//function to free non null pointers in the table
void phylib_free_table( phylib_table *table ){

    //if the table is null we simply return while doing nothing
    if (table == NULL) {

        return;

    } 
    //for loop to iterate through the objects of the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        //when we find an object not pointint to null we free it
        if (table->object[i] != NULL) {
            free(table->object[i]);
            //we free it and set it equal to null
            table->object[i] = NULL;

        }

    }
    //freeing the whole table here
    free(table);
    //setting the table to null
    table = NULL;

}

//function to return the difference between the given parameters
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

    phylib_coord result;

    result.x = c1.x - c2.x;

    result.y = c1.y - c2.y;

    return result;

}

//function to reutrn length of vector c
double phylib_length( phylib_coord c ){

    double lengthResult;

    //pythagoriean theorem for result of length of vector c
    lengthResult = sqrt((c.x * c.x) + (c.y * c.y));

    return lengthResult;

}

//function to compute the dot product between two vectors
double phylib_dot_product( phylib_coord a, phylib_coord b ){

    double dotProduct = a.x * b.x + a.y * b.y;

    return dotProduct;

}

//function to calcualte the distance between the two sent parameters. 
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

    //checking for null pointers and ensuring objext 1 is still
    if (obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL) {

        return -1.0;

    }
    //new variable ball one is going to hold the same pos properties as obj1
    phylib_coord ballOne = obj1->obj.rolling_ball.pos;
    //new variable for ball distance is set to -1 error value
    double ballDist = -1.0;
    //variable to store posiitons of obj 2
    phylib_coord ballTwo;
    //variales to store the vector difference between positons
    phylib_coord ballDiff;

    //case 1 - if other object is either rolling or still, we calcualte 
    //the vector differneces between the two objects' positons
    if (obj2->type == PHYLIB_ROLLING_BALL) {

        ballTwo = obj2->obj.rolling_ball.pos;
        ballDiff = phylib_sub(ballOne, ballTwo);
        ballDist = phylib_length(ballDiff);
        ballDist = ballDist - PHYLIB_BALL_DIAMETER;

    } else if (obj2->type == PHYLIB_STILL_BALL) {

        ballTwo = obj2->obj.still_ball.pos;
        ballDiff = phylib_sub(ballOne, ballTwo);
        ballDist = phylib_length(ballDiff);
        ballDist = ballDist - PHYLIB_BALL_DIAMETER;

    } else if (obj2->type == PHYLIB_HOLE) {     //case 2 - the other object is a hole

        //calculating the distance from the ball's center and subtracting the hole's
        //radius from the distance
        ballTwo = obj2->obj.hole.pos;
        ballDiff = phylib_sub(ballOne, ballTwo);
        ballDist = phylib_length(ballDiff);
        ballDist = ballDist - PHYLIB_HOLE_RADIUS;

    } else if (obj2->type == PHYLIB_HCUSHION) { //case 3 - the other object is a cushion
        //if the second calculating the difference in the x or y dimensions and subtracitng bal radius
        ballDist = fabs(ballOne.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;

    } else if (obj2->type == PHYLIB_VCUSHION) {

        ballDist = fabs(ballOne.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;

    }
    //returning the distance found
    return ballDist;
    
}

//part 3

void phylib_roll( phylib_object *new, phylib_object *old, double time ){

    //ensuring our pointers do not point to null
    if (new == NULL || old == NULL) {
        
        return;

    }
    //if the new object and the old object are both not rolling balls, we return
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {

        return;

    }
    //copying over all the properties of the old member to the new memebr
    *new = *old;

    //declaring variables for the member access
    double newXVelocity = new->obj.rolling_ball.vel.x;
    double newYVelocity = new->obj.rolling_ball.vel.y;
    //variables for the old pointer
    double oldXVelocity = old->obj.rolling_ball.vel.x;
    double oldYVelocity = old->obj.rolling_ball.vel.y;

    //new position is set equal to the old position being manipulated by the second integral of acc
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * (time * time);
    //we do the same here but for the y member
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * (time * time);

    //new velocity froom adding the old accesslaration * time to the old velocity
    newXVelocity = oldXVelocity + old->obj.rolling_ball.acc.x * time;
    //repeated for the y coordinate
    newYVelocity = oldYVelocity  + old->obj.rolling_ball.acc.y * time;

    //checking if there has been any sort of sign change frot he veolcities in x and y coordinates
    if ((newXVelocity * oldXVelocity) < 0) {
        //if there has been a sign change, the ball has stopped and the velocity is 0
        newXVelocity = 0;
        new->obj.rolling_ball.acc.x = 0;

    }
    if ((newYVelocity * oldYVelocity) < 0) {

        newYVelocity = 0;
        new->obj.rolling_ball.acc.y = 0;

    }
    //setting the new velocities to the struct members
    new->obj.rolling_ball.vel.x = newXVelocity;
    //same for the y coordinate
    new->obj.rolling_ball.vel.y = newYVelocity;

}
//function to check if a ball has stopped moving
unsigned char phylib_stopped( phylib_object *object ){
    //if the object is null we return 0, error check
    if (object == NULL) {

        return 0;
    }
    //as long as the object is a rolling ball
    if (object->type == PHYLIB_ROLLING_BALL) {

        //magnitude of the veclocity vector is calculated here
        double velocityLength = sqrt((object->obj.rolling_ball.vel.x * object->obj.rolling_ball.vel.x) + (object->obj.rolling_ball.vel.y * object->obj.rolling_ball.vel.y)); 

        //if the velocity is below the definition, we consider the ball stopped
        if (velocityLength < PHYLIB_VEL_EPSILON) {

            //then we can change the ball type to a still ball
            object->type = PHYLIB_STILL_BALL;
            //we can also update the acceleration and velocity
            object->obj.rolling_ball.acc.x = 0;
            object->obj.rolling_ball.acc.y = 0;

            object->obj.rolling_ball.vel.x = 0;
            object->obj.rolling_ball.vel.y = 0;
            //then we return 1 to indicate we did make a change
            return 1;

        }
    }
    //else we simply return 0 if the ball has not stopped
    return 0;

}
//function to deal with movement collision between various objects
void phylib_bounce( phylib_object **a, phylib_object **b ){

    //checking for null pointers, returning nothing if any pointer sent in is null
    //since parameters are double pointers we simply return. 
    if (a == NULL || b == NULL || *a == NULL || *b == NULL) {
        return;
    }
    //if the first object is a type of rolling_ball, we simply return
    if ((*a)->type != PHYLIB_ROLLING_BALL){
        return;
    }
    //declaring varibales ourside of switch to ensure full function scope. 
    phylib_coord r_ab;
    phylib_coord v_rel;
    double v_rel_n;

    switch ((*b)->type) {
        //if object b is a horizontal cushion
        case PHYLIB_HCUSHION:
            //here we refract the velocity and accelleration of the y cooridinate
            //to show case a type of incidence refraction
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * (-1.0);
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * (-1.0);
            break;
        //if object b is a vertical cushion
        case PHYLIB_VCUSHION:
            //refract the velocity and acceleration of x coordinate
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * (-1.0);
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * (-1.0);
            break;
        //if the object b is a type of hole
        case PHYLIB_HOLE:
            //we make object a "disappear" by freeing its memory and making it null
            //making it seem as if the ball fell into the hole
            free(*a);
            *a = NULL;

            break;
        //if the other obejct is a still ball
        case PHYLIB_STILL_BALL:
            //we turn it into a rolling ball as the motion would end up pushing it
            (*b)->type = PHYLIB_ROLLING_BALL;
            //we update its number and position
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            //and we set the velocity and accelerations to 0.0 and let the case
            //fall throguh to rolling ball so the updates can be made accordingly
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

        //case if we hit another moving ball
        case PHYLIB_ROLLING_BALL: 
            //our defined variables hold the subtracted values of positions and velocity respectively
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            //we create a length varaible to hold the length of the positoin vector
            double r_abVal = phylib_length(r_ab);

            //divide by zero not allowed
            if (r_abVal == 0) {
                break;
            }

            phylib_coord n = {r_ab.x / phylib_length(r_ab), r_ab.y / phylib_length(r_ab)};

            v_rel_n = phylib_dot_product(v_rel, n);
            //here we adjust the velocities based on the dot product's output
            //this way we can have bounce
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

            (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * n.x);
            (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * n.y);

            //here we are appling a drag effect to both of the objects in the case they are moving
            if (phylib_length((*a)->obj.rolling_ball.vel) > PHYLIB_VEL_EPSILON) {

                phylib_coord velocityObjectA;
                //formula retrived from asssingemnt specifications
                velocityObjectA.x = (*a)->obj.rolling_ball.vel.x / phylib_length((*a)->obj.rolling_ball.vel);
                velocityObjectA.y = (*a)->obj.rolling_ball.vel.y / phylib_length((*a)->obj.rolling_ball.vel);
                //multupling the negated velocity fro each x and y with the drag componenet
                (*a)->obj.rolling_ball.acc.x = -velocityObjectA.x * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -velocityObjectA.y * PHYLIB_DRAG;

            }
            //doing the same thing here for the second ball
            if (phylib_length((*b)->obj.rolling_ball.vel) > PHYLIB_VEL_EPSILON) {

                phylib_coord velocityObjectB;

                velocityObjectB.x = (*b)->obj.rolling_ball.vel.x / phylib_length((*b)->obj.rolling_ball.vel);
                velocityObjectB.y = (*b)->obj.rolling_ball.vel.y / phylib_length((*b)->obj.rolling_ball.vel);

                (*b)->obj.rolling_ball.acc.x = -velocityObjectB.x * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -velocityObjectB.y * PHYLIB_DRAG;

            }

            break;

        default: 

            break;
        
    }

}

unsigned char phylib_rolling( phylib_table *t ){
    
    //ensuring we are not working with a null, returning 0 if that is the case
    if (t == NULL){
        return 0;
    }
    //declaraing a count variable, initializing to 0
    int count = 0;

    //for loop to iterate through the max number of objects
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

        //if the object at the index is not null and the object type is a rolling ball
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            //we iterate the count variable
            count++;
        }

    }
    //we return the count variable
    return count;

}

phylib_table *phylib_segment( phylib_table *table ) {

    //if the table is null we return null, error checking
    if (table == NULL) {
        return NULL;
    }
    //if there are no rolling balls on the table we return null as theres no movement to capture
    if (phylib_rolling(table) == 0) {
        return NULL;
    }
    //making a new variable of type table and setting it equal to the copy of the table
    phylib_table *newTableCopy = phylib_copy_table(table);

    if (!newTableCopy) {
        return NULL;
    }
    double time = PHYLIB_SIM_RATE;
    //for loop to iterate until we reach max time. and we increment by the simulation rate
    while(PHYLIB_MAX_TIME > time) {

        //for loop to iterate through the objects on the table
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            //if the current object is not null, we must make updates to the object if it is rolling as well
            if (newTableCopy->object[i] != NULL && newTableCopy->object[i]->type == PHYLIB_ROLLING_BALL) {

                //calling the roll function to stimulate the movement of the new ball
                phylib_roll(newTableCopy->object[i], table->object[i], time);
            }
        }
        //for loop to iterate through the colliding objects
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {

            //and the current colliding object is not null
            if (newTableCopy->object[j] != NULL && newTableCopy->object[j]->type == PHYLIB_ROLLING_BALL) {

                //if a ball has stopped, accoridng to the assigment specs we must return the table
                if (phylib_stopped(newTableCopy->object[j])) {
                    //we just copy the time over and we return. 
                    newTableCopy->time = newTableCopy->time + time;
                    return newTableCopy;

                }
                //loop to iterate through and check for collisions
                for(int k = 0; k < PHYLIB_MAX_OBJECTS; k++)
                {
                    double dist = phylib_distance(newTableCopy->object[j], newTableCopy->object[k]);
                    //if a collusion as occured - verified by checking is distnace is less than 0.0
                    if(newTableCopy->object[k] != NULL && j != k && (0.0 > dist)) 
                    {
                        //we call phylib bounce with our two obejcts
                        phylib_bounce(&newTableCopy->object[j], &newTableCopy->object[k]);
                        //and we copy over the time to the table's struct definitons
                        newTableCopy->time = newTableCopy->time + time;
                        //we return the table here
                        return newTableCopy;
                    }
                }
            }
        }
        //we set the time variable to a final adiditon for the sim rate to acocunt for the final seg
        time = time + PHYLIB_SIM_RATE;

    }
    //we copy over the final time
    newTableCopy->time = newTableCopy->time + time;

    //returning the table copy
    return newTableCopy;

} 

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }

    return string;

}


