/**
 * Piece class which all chess peices inherit from
 * @param {int} r    the current row of the piece
 * @param {in} c    the current column of the piece
 * @param {int} team the piece's team
 */
var Piece = function(r, c, team) {
    this.init(r, c, team);
};

/**
 * Initialize a piece
 * @param {int} r    the current row of the piece
 * @param {in} c    the current column of the piece
 * @param {int} team the piece's team
 */
Piece.method('init', function (r, c, team) {
    this.r = r;
    this.c = c;
    this.team = team;
});

/**
 * Get all legal moves for a piece
 */
Piece.method('getMoves', function () {
    return [];
});

Piece.method('getGenericMoves', function (moves, cap, rmod, cmod, rend, cend) {
    var i = this.r + rmod;
    var j = this.c + cmod;
    while (i != rend && j != cend) {
        moves.append([i , j]);

        if (cap) {
            return moves;
        }

        i += rmod;
        j += cmod;
    }

    return moves;
});

/**
 * Get all horizontal moves possible from the piece's current position
 * @param  {array} moves any already found moves
 * @param  {bool} cap if true, will only return the first moves found in any direction
 */
Piece.method('getHMoves', function (moves, cap) {
    moves = this.getGenericMoves(moves, cap, 0, 1, 0, 8);
    moves = this.getGenericMoves(moves, cap, 0, -1, 0, -1);

    return moves;
});

/**
 * Get all vertical moves possible from the piece's current position
 * @param  {array} moves any already found moves
 * @param  {bool} cap if true, will only return the first moves found in any direction
 */
Piece.method('getVMoves', function(moves, cap) {
    moves = this.getGenericMoves(moves, cap, 1, 0, 8, 0);
    moves = this.getGenericMoves(moves, cap, -1, 0, -1, 0);

    return moves;
});

/**
 * Get all diagonal moves possible from the piece's current position
 * @param  {array} moves any already found moves
 * @param  {bool} cap if true, will only return the first moves found in any direction
 */
Piece.method('getDiagMoves', function(moves, cap) {
    moves = this.getGenericMoves(moves, cap, 1, 1, 8, 8);
    moves = this.getGenericMoves(moves, cap, 1, -1, 8, -1);
    moves = this.getGenericMoves(moves, cap, -1, 1, -1, 8);
    moves = this.getGenericMoves(moves, cap, -1, -1, -1, -1);

    return moves;
});

var King = function(r, c, team) {
    this.init(r, c, team);
};
King.inherits(Piece);

King.method('getMoves', function () {
    var moves = [];
    moves = this.getHMoves(moves, true);
    moves = this.getVMoves(moves, true);
    moves = this.getDiagMoves(moves, true);
    return moves;
});

var Queen = function(r, c, team) {
    this.init(r, c, team);
};
Queen.inherits(Piece);

Queen.method('getMoves', function () {
    var moves = [];
    moves = this.getHMoves(moves, false);
    moves = this.getVMoves(moves, false);
    moves = this.getDiagMoves(moves, false);
    return moves;
});

var Rook = function(r, c, team) {
    this.init(r, c, team);
};
Rook.inherits(Piece);

Rook.method('getMoves', function () {
    var moves = [];
    moves = this.getHMoves(moves, false);
    moves = this.getVMoves(moves, false);
    return moves;
});

var Bishop = function(r, c, team) {
    this.init(r, c, team);
};
Bishop.inherits(Piece);

Bishop.method('getMoves', function () {
    var moves = [];
    moves = this.getDiagMoves(moves, false);
    return moves;
});

var Knight = function(r, c, team) {
    this.init(r, c, team);
};
Knight.inherits(Piece);

Knight.method('getMoves', function () {
    var moves = [];
    moves.append([this.r + 2, this.c + 1]);
    moves.append([this.r + 2, this.c - 1]);
    moves.append([this.r - 2, this.c + 1]);
    moves.append([this.r - 2, this.c - 1]);
    moves.append([this.r + 1, this.c + 2]);
    moves.append([this.r + 1, this.c - 2]);
    moves.append([this.r - 1, this.c + 2]);
    moves.append([this.r - 1, this.c - 2]);
    return moves;
});

var Pawn = function(r, c, team, d) {
    this.init(r, c, team);
    this.d = d;
    this.moved = false;
};
Pawn.inherits(Piece);

Pawn.method('getMoves', function () {
    var moves = [];
    moves.append([this.r + this.d, this.c]);

    if (!this.moved) {
        moves.append([this.r + 2 * this.d, this.c]);
    }

    return moves;
});