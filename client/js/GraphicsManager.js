/**
 * GraphicsManager creates, initializes, and manages an HTML5 canvas for Collaborative Chess project.
 * @param  {div} canvas_container Div container for the HTML5 canvas
 * @param  {int} width            The width of the canvas. Defaults to 1000.
 * @param  {int} height           The height of the canvas. Defaults to 1000.
 */
var GraphicsManager = function (canvas_container, width, height) {
    var canvas = null;
    var context = null;
    var square_width = null;
    var square_height = null;

    /**
     * Initialize HTML5 canvas
     * @param  {div} canvas_container Div container for the HTML5 canvas
     * @param  {int} width            The width of the canvas. Defaults to 1000.
     * @param  {int} height           The height of the canvas. Defaults to 1000.
     */
    function init(canvas_container, width, height) {
        // set default values
        width = typeof width !== 'undefined' ? width : 1000;
        height = typeof height !== 'undefined' ? height : 1000;

        // create the canvas
        canvas = document.createElement('canvas');

        // attach the canvas to its container
        canvas_container.appendChild(canvas);

        // get the 2d context
        context = canvas.getContext('2d');

        // resize the canvas
        context.canvas.width = width;
        context.canvas.height = height;

        // determine the size of a square on the board
        square_width = width / 8;
        square_height = height / 8;
    }

    /**
     * Draw objects to the screen
     * @param  {Array} objects The object to draw on the screen
     */
    this.draw = function () {
        // clear the canvas
        context.clearRect(0, 0, canvas.width, canvas.height);

        drawBoard();
    };

    /**
     * Draw a rectangle to the canvas
     * @param  {float} x      The x coordinate of the top left corner of the rectangle
     * @param  {float} y      The y coordinate of the top left corner of the rectangle
     * @param  {float} width  The width of the rectangle
     * @param  {float} height The height of the rectangle
     * @param  {color} color  The color of the rectangle.
     */
    function drawRectangle(x, y, width, height, color) {
        // set the rectangle's color
        context.fillStyle = color;

        // create the rectangle
        context.fillRect(x, y, width, height);
    }

    /**
     * Draw the chess board to the canvas
     */
    function drawBoard() {
        var square_color = ['#F6E497', '#4C1B1B']; //https://color.adobe.com/Cherry-Cheesecake-color-theme-2354/edit/?copy=true&base=0&rule=Custom&selected=2&name=Copy%20of%20Cherry%20Cheesecake&mode=rgb&rgbvalues=0.72549,0.0705882,0.105882,0.298039,0.105882,0.105882,0.964706,0.894118,0.592157,0.988235,0.980392,0.882353,0.741176,0.552941,0.27451&swatchOrder=0,1,2,3,4

        for (var r = 0; r<8; r++) {
            for (var c = 0;  c<8; c++) {
                // alternate black and white squares
                drawRectangle(c*square_width, r*square_height, square_width, square_height, square_color[(r+c)%2]);
            }
        }

        // draw example
        drawUnit("P", 1, 0, 1);
        drawUnit("P", 1, 1, 1);
        drawUnit("P", 1, 2, 1);
        drawUnit("P", 1, 3, 1);
        drawUnit("P", 1, 4, 1);
        drawUnit("P", 1, 5, 1);
        drawUnit("P", 1, 6, 1);
        drawUnit("P", 1, 7, 1);
        drawUnit("R", 1, 0, 0);
        drawUnit("H", 1, 1, 0);
        drawUnit("B", 1, 2, 0);
        drawUnit("Q", 1, 3, 0);
        drawUnit("K", 1, 4, 0);
        drawUnit("B", 1, 5, 0);
        drawUnit("H", 1, 6, 0);
        drawUnit("R", 1, 7, 0);
    }

    /**
     * Draws a unit to the canvas in the desired tile
     * @param  {string} unit Name of the unit
     * @param  {int} team The unit's team. 0 for white. 1 for black.
     * @param  {int} r The row the unit is on
     * @param  {int} c The column the unit is on
     */
    function drawUnit(unit, team, r, c) {
        var team_colors = ['#FCFAE1', '#B9121B'];

        context.fillStyle = team_colors[team];
        context.font = "bold " + Math.min(square_height, square_width)*0.9 + "px Arial";
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(unit, r*square_height + square_height/2, c*square_width + square_width/2);

    }

    /**
     * Resize the canvas
     * @param  {int} width  The new width of the canvas
     * @param  {int} height The new height of the canvas
     */
    this.resize = function(width, height) {
        // resize the canvas
        context.canvas.width = window.innerWidth;
        context.canvas.height = window.innerHeight;
    };

    // initialize object
    init(canvas_container, width, height);
};