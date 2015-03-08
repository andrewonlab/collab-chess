/**
 * Piece class which all chess peices inherit from
 * @param {int} r    the current row of the piece
 * @param {in} c    the current column of the piece
 * @param {int} team the piece's team
 */
var Piece = function(r, c, team) {
    /**
     * Initialize a piece
     * @param {int} r    the current row of the piece
     * @param {in} c    the current column of the piece
     * @param {int} team the piece's team
     */
    this.init = function (r, c, team) {
        this.r = r;
        this.c = c;
        this.team = team;
    };

    /**
     * Get all legal moves for a piece
     */
    this.getMoves = function () {
        return [];
    };

    this.getGenericMoves = function (moves, cap, rmod, cmod, rend, cend) {
        var i = this.r + rmod;
        var j = this.c + cmod;
        while (i != rend && j != cend) {
            moves.push([i , j]);

            if (cap) {
                return moves;
            }

            i += rmod;
            j += cmod;
        }

        return moves;
    };

    /**
     * Get all horizontal moves possible from the piece's current position
     * @param  {array} moves any already found moves
     * @param  {bool} cap if true, will only return the first moves found in any direction
     */
    this.getHMoves = function (moves, cap) {
        moves = this.getGenericMoves(moves, cap, 0, 1, 1, 8);
        moves = this.getGenericMoves(moves, cap, 0, -1, 1, -1);

        return moves;
    };

    /**
     * Get all vertical moves possible from the piece's current position
     * @param  {array} moves any already found moves
     * @param  {bool} cap if true, will only return the first moves found in any direction
     */
    this.getVMoves = function(moves, cap) {
        moves = this.getGenericMoves(moves, cap, 1, 0, 8, 1);
        moves = this.getGenericMoves(moves, cap, -1, 0, -1, 1);

        return moves;
    };

    /**
     * Get all diagonal moves possible from the piece's current position
     * @param  {array} moves any already found moves
     * @param  {bool} cap if true, will only return the first moves found in any direction
     */
    this.getDiagMoves = function(moves, cap) {
        moves = this.getGenericMoves(moves, cap, 1, 1, 8, 8);
        moves = this.getGenericMoves(moves, cap, 1, -1, 8, -1);
        moves = this.getGenericMoves(moves, cap, -1, 1, -1, 8);
        moves = this.getGenericMoves(moves, cap, -1, -1, -1, -1);

        return moves;
    };

    this.init(r, c, team);
};

var King = function(r, c, team) {
    this.init(r, c, team);
};
King.prototype = new Piece();

King.prototype.getMoves = function () {
    var moves = [];
    moves = this.getHMoves(moves, true);
    moves = this.getVMoves(moves, true);
    moves = this.getDiagMoves(moves, true);
    return moves;
};

var Queen = function(r, c, team) {
    this.init(r, c, team);
};
Queen.prototype = new Piece();

Queen.prototype.getMoves =  function () {
    var moves = [];
    moves = this.getHMoves(moves, false);
    moves = this.getVMoves(moves, false);
    moves = this.getDiagMoves(moves, false);
    return moves;
};

var Rook = function(r, c, team) {
    this.init(r, c, team);
};
Rook.prototype = new Piece();

Rook.prototype.getMoves = function () {
    var moves = [];
    moves = this.getHMoves(moves, false);
    moves = this.getVMoves(moves, false);
    return moves;
};

var Bishop = function(r, c, team) {
    this.init(r, c, team);
};
Bishop.prototype = new Piece();

Bishop.prototype.getMoves = function () {
    var moves = [];
    moves = this.getDiagMoves(moves, false);
    return moves;
};

var Knight = function(r, c, team) {
    this.init(r, c, team);
};
Knight.prototype = new Piece();

Knight.prototype.getMoves = function () {
    var moves = [];
    moves.push([this.r + 2, this.c + 1]);
    moves.push([this.r + 2, this.c - 1]);
    moves.push([this.r - 2, this.c + 1]);
    moves.push([this.r - 2, this.c - 1]);
    moves.push([this.r + 1, this.c + 2]);
    moves.push([this.r + 1, this.c - 2]);
    moves.push([this.r - 1, this.c + 2]);
    moves.push([this.r - 1, this.c - 2]);
    return moves;
};

var Pawn = function(r, c, team) {
    this.init(r, c, team);
    this.d = 0;
    if (r < 2) {
        this.d = 1;
    } else {
        this.d = -1;
    }
    this.moved = false;
};
Pawn.prototype = new Piece();

Pawn.prototype.getMoves = function () {
    var moves = [];
    moves.push([this.r + this.d, this.c]);

    if (!this.moved) {
        moves.push([this.r + 2 * this.d, this.c]);
    }

    return moves;
};