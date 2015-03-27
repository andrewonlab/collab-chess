var GameManager = function (canvas_container, width, height, json) {
    this.gfx = new GraphicsManager(canvas_container, width, height);
    var square_dim = this.gfx.getSquareDimension();
    var board = new Board(json);
    var selected_tile = null;
    var moves = [];
    var my_json = json;
    var last_move = null;
    var last_occupant = null;

    /**
     * Updates the board
     * @param  {JSON} json Only pass in JSON if the board state has changed outside the client, IE after a move vote
     */
    this.update = function (json) {
        json = typeof json !== 'undefined' ? json : my_json;
        my_json = json;

        this.gfx.draw(json, moves, board);
    };

    this.undoMove = function () {
        undoMove();
    };

    function undoMove() {
        if (last_move !== null) {
            // move the last moved piece back to its original location
            board.movePiece(last_move[2], last_move[3], last_move[0], last_move[1]);

            // subtract 2 from the number of moves. one for the move and one for the undo move
            board.getPiece(last_move[0], last_move[1]).num_moves -= 2;

            // update the piece's location in the json
            updateJSON(last_move[2], last_move[3], last_move[0], last_move[1], board.getPiece(last_move[0], last_move[1]).team);

            // return any deleted piece to the board
            if (last_occupant !== null) {
                board.addUnit(last_occupant.type, last_occupant.team, last_occupant.r, last_occupant.c);
                updateJSON(-1, -1, last_occupant.r, last_occupant.c, last_occupant.team);
            }

            // reset the undo variables
            last_move = null;
            last_occupant = null;
        }
    }

    function getClickedTile (event) {
        r = Math.floor((event.clientY - canvas_container.offsetLeft)/square_dim[1]);
        c = Math.floor((event.clientX - canvas_container.offsetLeft)/square_dim[0]);
        return [r, c];
    }

    function boardClick (event) {
        var tile = getClickedTile(event);
        var r = tile[0];
        var c = tile[1];

        if (selected_tile !== null) {
            if ((selected_tile[0] != r || selected_tile[1] != c) && validMove(tile)) {
                if (board.isOccupied(r, c)) {
                    last_occupant = board.getPiece(r, c);
                    updateJSON(r, c, -1, -1, board.getPiece(r, c).team);
                } else {
                    last_occupant = null;
                }

                board.movePiece(selected_tile[0], selected_tile[1], r, c);
                updateJSON(selected_tile[0], selected_tile[1], r, c, board.getPiece(r, c).team);
                last_move = [selected_tile[0], selected_tile[1], tile[0], tile[1]];
                selected_tile = null;
                moves = [];
            } else {
                selected_tile = null;
                moves = [];
            }
        } else if (board.isOccupied(r, c)) {
            selected_tile = tile;
            moves = board.getPiece(r, c).getMoves(board);
        }
    }

    function updateJSON(from_r, from_c, to_r, to_c, team) {
        var team_pieces = [];
        if (team === 0) {
            team_pieces = my_json["white"];
        } else {
            team_pieces = my_json["black"];
        }

        for (var i=0; i<team_pieces.length; i++) {
            if (team_pieces[i][0] == from_r && team_pieces[i][1] == from_c) {
                team_pieces[i][0] = to_r;
                team_pieces[i][1] = to_c;
                return;
            }
        }
    }

    function validMove(target_tile) {
        for (var i=0; i<moves.length; i++) {
            if (target_tile[0] == moves[i][0] && target_tile[1] == moves[i][1]) {
                return true;
            }
        }

        return false;
    }

    document.addEventListener("click", boardClick );
};