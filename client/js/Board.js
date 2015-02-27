var Board = function () {
    var MAX_ROW = 8;
    var MAX_COL = 8;

    this.board = null;

    /**
     * Create the board
     */
    this.init = function () {
        this.board = [];
        for (var r = 0; r<MAX_ROW; r++) {
            var row = [];
            for (var c = 0; c<MAX_COL; c++) {
                row.append(null);
            }
            this.board.append(row);
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
        if (!isOccupied(from_r, from_c)) {
            throw "Tile unnocpuied! Cannot move a unit from an empty tile!";
        }

        // move the piece
        this.board[to_r][to_c] = this.board[from_r][from_c];
        this.board[to_r][to_c].r = to_r;
        this.board[to_r][to_c].c = to_c;

        // empty the old tile
        this.board[from_r][from_c] = null;
    };

    // initialize the board
    this.init();
};