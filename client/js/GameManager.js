var GameManager = function (canvas_container, width, height, json) {
    this.gfx = new GraphicsManager(canvas_container, width, height);
    var square_dim = this.gfx.getSquareDimension();
    var board = new Board(json);
    var selected_tile = null;
    var moves = [];
    var my_json = json;

    /**
     * Updates the board
     * @param  {JSON} json Only pass in JSON if the board state has changed outside the client, IE after a move vote
     */
    this.update = function (json) {
        json = typeof json !== 'undefined' ? json : my_json;
        my_json = json;

        this.gfx.draw(json, moves);
    };

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
            if (selected_tile[0] != r || selected_tile[1] != c) {
                board.movePiece(selected_tile[0], selected_tile[1], r, c);
                updateJSON(selected_tile[0], selected_tile[1], r, c, board.getPiece(r, c).team);
                selected_tile = null;
                moves = [];
            } else {
                selected_tile = null;
                moves = [];
            }
        } else if (board.isOccupied(r, c)) {
            selected_tile = tile;
            moves = board.getPiece(r, c).getMoves();
        }
        // console.log(r, c, selected_tile);
        // console.log(moves);
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

    document.addEventListener("click", boardClick );
};