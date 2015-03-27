var Board = function (json) {
    var MAX_ROW = 8;
    var MAX_COL = 8;

    this.board = null;

    /**
     * Create the board
     */
    this.init = function (json) {
        this.board = [];
        for (var r = 0; r<MAX_ROW; r++) {
            var row = [];
            for (var c = 0; c<MAX_COL; c++) {
                row.push(null);
            }
            this.board.push(row);
        }

        this.addUnits(json["white"], 0);
        this.addUnits(json["black"], 1);
    };

    this.addUnits = function (json, team) {
        for (var i in json) {
            if (json[i][0].between()-1, 8) {
                this.addUnit(json[i][2], team, json[i][0], json[i][1]);
            }
        }
    };

    this.addUnit = function (type, team, r, c) {
        switch (type) {
            case 'k':
                this.board[r][c] = new King(r, c, team, this);
                return;
            case 'q':
                this.board[r][c] = new Queen(r, c, team, this);
                return;
            case 'r':
                this.board[r][c] = new Rook(r, c, team, this);
                return;
            case 'b':
                this.board[r][c] = new Bishop(r, c, team, this);
                return;
            case 'h':
                this.board[r][c] = new Knight(r, c, team, this);
                return;
            case 'p':
                this.board[r][c] = new Pawn(r, c, team, this);
                return;
        }
    };

    /**
     * Check if a given tile on the board is occupied
     * @param  {int} r the row to check
     * @param  {int} c the column to check
     * @return {bool}   true if the tile is occupied. false if it is not
     */
    this.isOccupied = function (r, c) {
        return this.getPiece(r, c) !== null;
    };

    /**
     * Get the piece that occupies a given tile
     * @param  {int} r the row to check
     * @param  {int} c the column to check
     * @return {Piece}   The piece that occupies that tile, or null if no piece does
     */
    this.getPiece = function (r, c) {
        if (r > 7 || r < 0 || c > 7 || c < 0) {
            return null;
        }

        return this.board[r][c];
    };

    /**
     * Move a piece from one tile to another
     * @param  {int} from_r the row to move from
     * @param  {int} from_c the col to move from
     * @param  {int} to_r   the row to move to
     * @param  {col} to_c   the col to move to
     */
    this.movePiece = function (from_r, from_c, to_r, to_c) {
        if (!this.isOccupied(from_r, from_c)) {
            throw "Tile unnocpuied! Cannot move a unit from an empty tile!";
        }

        // move the piece
        this.board[to_r][to_c] = this.board[from_r][from_c];
        this.board[to_r][to_c].moveTo(to_r, to_c);

        // empty the old tile
        this.board[from_r][from_c] = null;
    };

    // initialize the board
    this.init(json);
};