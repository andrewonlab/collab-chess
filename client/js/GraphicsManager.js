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
    var tint_canvas = document.createElement('canvas');
    tint_canvas.width = 600;
    tint_canvas.height = 600;
    var tint_context = tint_canvas.getContext('2d');

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
     * @param  {json} json JSON object with board state
     */
    this.draw = function (json, green_h, red_h) {
        // clear the canvas
        context.clearRect(0, 0, canvas.width, canvas.height);

        drawBoard(green_h, red_h);
        drawUnits(json["white"], 0);
        drawUnits(json["black"], 1);
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
    function drawBoard(green_h, red_h) {
        green_h = typeof green_h !== 'undefined' ? green_h : [];
        red_h = typeof red_h !== 'undefined' ? red_h : [];

        // var square_color = ['#F6E497', '#4C1B1B']; //https://color.adobe.com/Cherry-Cheesecake-color-theme-2354/edit/?copy=true&base=0&rule=Custom&selected=2&name=Copy%20of%20Cherry%20Cheesecake&mode=rgb&rgbvalues=0.72549,0.0705882,0.105882,0.298039,0.105882,0.105882,0.964706,0.894118,0.592157,0.988235,0.980392,0.882353,0.741176,0.552941,0.27451&swatchOrder=0,1,2,3,4
        // Color scheme: https://color.adobe.com/Honey-Pot-color-theme-1490158/edit/?copy=true
        var square_color = ['#FFFAD5', '#FFD34E']; // cream, yellow
        // var square_color = ['#105B63', '#BD4932']; // blue, red

        for (var r = 0; r<8; r++) {
            for (var c = 0;  c<8; c++) {
                    drawRectangle(c*square_width, r*square_height, square_width, square_height, square_color[(r+c)%2]);
            }
        }

        // draw green tiles
        for (var i = 0; i<green_h.length; i++) {
            drawRectangle(green_h[i][1]*square_width, green_h[i][0]*square_height, square_width, square_height, 'green');
        }


        // draw red tiles
        for (i = 0; i<red_h.length; i++) {
            drawRectangle(red_h[i][1]*square_width, red_h[i][0]*square_height, square_width, square_height, 'green');
        }
    }

    /**
     * Draws a unit to the canvas in the desired tile
     * @param  {string} unit Name of the unit
     * @param  {int} team The unit's team. 0 for white. 1 for black.
     * @param  {int} r The row the unit is on
     * @param  {int} c The column the unit is on
     */
    function drawUnit(unit, team, r, c) {
        // var team_colors = [{r:16, g:91, b:99}, {r:189, g:73, b:50}]; // blue, red
        // var team_colors = [{r:255, g:250, b:213}, {r:219, g:158, b:54}]; // cream, yellow
        var team_colors = ['#BD4932', '#105B63']; // red, blue

        // aquire correct image for the unit, the scale for that image, and its position on the board
        var img = null;
        var w = square_width;
        var h = square_width;
        var x = c*square_width;
        var y = r*square_height;
        var big_mod = 0.9;
        var med_mod = 0.8;
        var small_mod = 0.6;
        switch (unit) {
            case 'k':
                img = document.getElementById("king_img");
                w *= big_mod;
                h *= big_mod;
                x = c*square_width + (square_width - square_width*big_mod)/2;
                y = r*square_height + (square_height - square_height*big_mod)/2;
                break;
            case 'q':
                img = document.getElementById("queen_img");
                w *= big_mod;
                h *= big_mod;
                x = c*square_width + (square_width - square_width*big_mod)/2;
                y = r*square_height + (square_height - square_height*big_mod)/2;
                break;
            case 'r':
                img = document.getElementById("rook_img");
                w *= med_mod;
                h *= med_mod;
                x = c*square_width + (square_width - square_width*med_mod)/2;
                y = r*square_height + 3*(square_height - square_height*big_mod)/2;
                break;
            case 'b':
                img = document.getElementById("bishop_img");
                w *= med_mod;
                h *= med_mod;
                x = c*square_width + (square_width - square_width*med_mod)/2;
                y = r*square_height + 3*(square_height - square_height*big_mod)/2;
                break;
            case 'h':
                img = document.getElementById("knight_img");
                w *= med_mod;
                h *= med_mod;
                x = c*square_width + (square_width - square_width*med_mod)/2;
                y = r*square_height + 3*(square_height - square_height*big_mod)/2;
                break;
            case 'p':
                img = document.getElementById("pawn_img");
                w *= small_mod;
                h *= small_mod;
                x = c*square_width + (square_width - square_width*small_mod)/2;
                y = r*square_height + (square_height - square_height*small_mod)/2;
                break;
            default:
                console.error("Could not find a unit of type " + unit);
                return;
        }

        // tint image
        tint_context.clearRect(0, 0, tint_canvas.width, tint_canvas.height);    // clear any old tinting from the tint canvas
        tint_context.fillStyle = team_colors[team];                             // select the correct team color
        tint_context.fillRect(0, 0, tint_canvas.width, tint_canvas.height);     // fill the tint canvas with the color
        tint_context.globalCompositeOperation = "destination-atop";             // set the layer blend mode
        tint_context.drawImage(img, 0, 0);                                      // tint the image the desired color

        // draw tinted image to the canvas
        context.drawImage(tint_canvas, x, y, w, h);
    }

    /**
     * Draw all the units for a given team to the canvas
     * @param  {json} json JSON representation of the current team state
     * @param  {int} team The team id
     */
    function drawUnits(json, team) {
        for (var i in json) {
            if (json[i][0].between()-1, 8) {
                drawUnit(json[i][2], team, json[i][0], json[i][1]);
            }
        }
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

    // from: http://stackoverflow.com/questions/12806304/shortest-code-to-check-if-a-number-is-in-a-range-in-javascript
    Number.prototype.between = function (min, max) {
        return this > min && this < max;
    };

    this.getSquareDimension = function () {
        return [square_width, square_height];
    };

    // initialize object
    init(canvas_container, width, height);
};