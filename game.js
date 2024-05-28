$(document).ready(function() {

    //variable drawing set to false
    var drawing = false;

    //constnats declared to intiate them with the local sotrage retrived
    //but json
    const player1Name = localStorage.getItem("player1Name");
    const player2Name = localStorage.getItem("player2Name");

    //hard coding the current player
    var currentPlayer = 1;
    //if the player naemes arent inptuted
    if (!player1Name || !player2Name) {
        //taking back to names.html if neither are inputted
        window.location.href = "names.html";
        return;
    }
    //display for html, if this key is found we replace with variable
    $("#player1NameDisplay").text(player1Name);
    $("#player2NameDisplay").text(player2Name);

    //method to change turns
    updateTurnUI();

    //curball is set to the circle object that is white for unique id
    var cueBall = $('circle[fill="WHITE"]');
    //original svg
    var svgElement = $('svg')[0]; 

    //var for real time
    let shotStartTime = null;



    function startShot(){
        shotStartTime = Date.now();
    }

    function getElapsedTime(){
        if(shotStartTime === null){
            return 0;
        }
        return Date.now() - shotStartTime;
    }

    //function RETRIVED FROM KREMER to get the mouse position via trakcing
    function getMousePosition(svg, event) {
        //turning the current pt into an svg point for conversiojn
        var pt = svg.createSVGPoint();

        //getting values from clinet
        pt.x = event.clientX;
        pt.y = event.clientY;
        //turnign the point into an svg coordinate
        var transformedPoint = pt.matrixTransform(svg.getScreenCTM().inverse());

        //returning the found points
        return { x: transformedPoint.x, y: transformedPoint.y };
    }
   
    //clauclating velocity function
    function calculateVelocity(x1, y1, x2, y2) {
        //distance is set to vector calculation
        const distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));

        //velocity multiplied so the max will be at 10
        let velocity = distance * 10; 
        //max velcoty is 10000
        return Math.min(velocity, 10000); 
    }

    //function to draw the line
    function drawLine(event) {
        //here we will only draw when the mouse is pressed
        if (!drawing) return; 
    
        //variable for the mouse position retrives mouse position via helper method
        //helpermethod gets the svgElement and event
        var mousePos = getMousePosition(svgElement, event);

        //variable set to the cueball's x position and y posotion
        var x1 = parseFloat(cueBall.attr('cx'));
        var y1 = parseFloat(cueBall.attr('cy'));

        //velocity caluclated from the line
        var velocity = calculateVelocity(x1, y1, mousePos.x, mousePos.y); // Calculate velocity
    
        //the line attribtue holds the following variables
        $('#line').attr({
            'x1': x1,
            'y1': y1,
            'x2': mousePos.x,
            'y2': mousePos.y,
            'style': 'display: inline'
        });

        //velocity gets changed to displayt he most current velcotuy
        $('#velocity-display').text('Velocity: ' + Math.round(velocity));
    }

    //changint ot listen to the document on a broader scope
    $(document).on('mousedown', function(event) {
        //checking again for cueline
        cueBall = $('circle[fill="WHITE"]'); 
        //ensuring the mouse is down
        if(event.target.closest('svg')) {
            //drawing set to true if mouse down
            drawing = true;
            //real time
            shotStartTime = Date.now()
        }
    });

    //when the mouse moves while down we track line
    $(document).on('mousemove', function(event) {
        drawLine(event);
    });

    //on mouse up is the real action
    $(document).on('mouseup', function(event) {
        //if not drawing return
        if (!drawing) return;
        //set drawoing to false
        drawing = false;
        //attribtues changed
        $('#line').attr('style', 'display: none');

        //velcoty displau on html
        $('#velocity-display').text('Velocity: 0');
        
        //calculate direction
        var mousePos = getMousePosition(svgElement, event);

        //calcualtihng the x and ys of cueball
        var x1 = parseFloat(cueBall.attr('cx'));
        var y1 = parseFloat(cueBall.attr('cy'));

        //variable for direction is set to the mouse and cueball positon
        var dx = x1 - mousePos.x;
        var dy = y1 - mousePos.y;

        //velcotu calcualted 
        var velocity = calculateVelocity(x1, y1, mousePos.x, mousePos.y);
        
        //send data to server
        $.ajax({
            //process shot url catches this
            url: '/process-shot',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                playerName: currentPlayer === 1 ? player1Name : player2Name,
                dx: dx,
                dy: dy,
                velocity: velocity
            }),
            //on success 
            success: function(response) {
                //assuming we get an array of svgs
                let svgArray = response.svgArray;
                //aniamting the svgs as long as theres an svg to animate
                if(svgArray && svgArray.length > 0) {
                    animateSVGs(svgArray);
                }
                //at the same time we assign the player who sunk a ball (if they did)
                if (response.ballAssignmentMsg) {

                    $("#ballAssignmentMsg").text(response.ballAssignmentMsg);
                }
            },
            error: function(error) {
                console.error('Error processing the current shot', error);
            }
        });
    });

    //here is the function to ANIMATE ALL FOT HE SVGS using the svgArray as a parameter
    function animateSVGs(svgArray) {

        //the current frame is going to be  0
        let currentFrame = 0;
        //displaying the next frame using function
        const displayNextFrame = () => {
            //displayihng as long as theres a frame to diaply
            if (currentFrame < svgArray.length) {

                //pasting it in the svg_box in html
                $('#svg_box').html(svgArray[currentFrame]);

                //incremementing the current frame
                currentFrame++;
                //asking for the next frame
                requestAnimationFrame(displayNextFrame); 
            //if nothing else to idisplay then update the cueball positiona dn swirtch player truns
            } else {
                updateCueBallPosition(svgArray[svgArray.length - 1]);
                switchTurns();
            }
        };
        requestAnimationFrame(displayNextFrame); //mthod used instad of inerva;
    }

    //updating the cueball position
    function updateCueBallPosition(finalSvg) {

        //crating constant to go through the svg
        const parser = new DOMParser();
        //parsing throught he string
        const svgDoc = parser.parseFromString(finalSvg, "text/html");
        //finding cueball from svg string
        const finalCueBall = svgDoc.querySelector('circle[fill="WHITE"]');

        //if we find it we update teh position of it
        if (finalCueBall) {
            cueBall.attr('cx', finalCueBall.getAttribute('cx'));
            cueBall.attr('cy', finalCueBall.getAttribute('cy'));
        }
    }

    //switching turns here
    function switchTurns() {
        currentPlayer = currentPlayer === 1 ? 2 : 1;
        updateTurnUI();
    }

    //updating the turns here
    function updateTurnUI() {
        var currentTurnName = currentPlayer === 1 ? player1Name : player2Name;
        $("#currentTurn").text("Current Turn: " + currentTurnName);
    }
    

});
