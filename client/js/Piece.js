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
    this.init = function (r, c, team, board) {
        this.r = r;
        this.c = c;
        this.team = team;
        this.board = board;
        this.num_moves = 0;
    };

    this.moveTo = function (r, c) {
        this.r = r;
        this.c = c;
        this.num_moves++;
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
            if (this.board.isOccupied(i, j)) {
                if (this.board.getPiece(i, j).team != this.team) {
                    moves.push([i, j]);
                    return moves;
                } else {
                    return moves;
                }
            }

            moves.push([i, j]);

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
        moves = this.getGenericMoves(moves, cap, 0, 1, -1, 8);
        moves = this.getGenericMoves(moves, cap, 0, -1, -1, -1);

        return moves;
    };

    /**
     * Get all vertical moves possible from the piece's current position
     * @param  {array} moves any already found moves
     * @param  {bool} cap if true, will only return the first moves found in any direction
     */
    this.getVMoves = function(moves, cap) {
        moves = this.getGenericMoves(moves, cap, 1, 0, 8, 8);
        moves = this.getGenericMoves(moves, cap, -1, 0, -1, -1);

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

var King = function(r, c, team, board) {
    this.init(r, c, team, board);
    this.type = 'k';
};
King.prototype = new Piece();

King.prototype.getMoves = function () {
    var moves = [];
    moves = this.getHMoves(moves, true);
    moves = this.getVMoves(moves, true);
    moves = this.getDiagMoves(moves, true);
    return moves;
};

var Queen = function(r, c, team, board) {
    this.init(r, c, team, board);
    this.type = 'q';
};
Queen.prototype = new Piece();

Queen.prototype.getMoves =  function () {
    var moves = [];
    moves = this.getHMoves(moves, false);
    moves = this.getVMoves(moves, false);
    moves = this.getDiagMoves(moves, false);
    return moves;
};

var Rook = function(r, c, team, board) {
    this.init(r, c, team, board);
    this.type = 'r';
};
Rook.prototype = new Piece();

Rook.prototype.getMoves = function () {
    var moves = [];
    moves = this.getHMoves(moves, false);
    moves = this.getVMoves(moves, false);
    return moves;
};

var Bishop = function(r, c, team, board) {
    this.init(r, c, team, board);
    this.type = 'b';
};
Bishop.prototype = new Piece();

Bishop.prototype.getMoves = function () {
    var moves = [];
    moves = this.getDiagMoves(moves, false);
    return moves;
};

var Knight = function(r, c, team, board) {
    this.init(r, c, team, board);
    this.type = 'h';
};
Knight.prototype = new Piece();

Knight.prototype.getKnightMove = function (moves, target_move) {
    // make sure target move is on the board
    if (target_move[0] > 7 || target_move[0] < 0 || target_move[1] > 7 || target_move[1] < 0) {
        return moves;
    }

    // add tiles occupied by enemy units but not friendly
    if (this.board.isOccupied(target_move[0], target_move[1])) {
        if (this.board.getPiece(target_move[0], target_move[1]).team != this.team) {
            moves.push(target_move);
            return moves;
        } else {
            return moves;
        }
    }

    // add the move if the tile is unoccupied
    moves.push(target_move);
    return moves;
};

Knight.prototype.getMoves = function () {
    var moves = [];

    moves = this.getKnightMove(moves, [this.r + 2, this.c + 1]);
    moves = this.getKnightMove(moves, [this.r + 2, this.c - 1]);
    moves = this.getKnightMove(moves, [this.r - 2, this.c + 1]);
    moves = this.getKnightMove(moves, [this.r - 2, this.c - 1]);
    moves = this.getKnightMove(moves, [this.r + 1, this.c + 2]);
    moves = this.getKnightMove(moves, [this.r + 1, this.c - 2]);
    moves = this.getKnightMove(moves, [this.r - 1, this.c + 2]);
    moves = this.getKnightMove(moves, [this.r - 1, this.c - 2]);
    return moves;
};

var Pawn = function(r, c, team, board) {
    this.init(r, c, team, board);
    this.d = 0;
    if (team == 1) {
        this.d = 1;
    } else {
        this.d = -1;
    }

    this.type = 'p';
};
Pawn.prototype = new Piece();

Pawn.prototype.getPawnAttack = function (moves, target_move) {
    // make sure target move is on the board
    if (target_move[0] > 7 || target_move[0] < 0 || target_move[1] > 7 || target_move[1] < 0) {
        return moves;
    }

    // add tiles occupied by enemy units but not friendly
    if (this.board.isOccupied(target_move[0], target_move[1])) {
        if (this.board.getPiece(target_move[0], target_move[1]).team != this.team) {
            moves.push(target_move);
            return moves;
        } else {
            return moves;
        }
    }

    // do not add tile unless an enemy occupies it
    return moves;
};

Pawn.prototype.getMoves = function () {
    var moves = [];
    var fwd_move = [this.r + this.d, this.c];
    if (!this.board.isOccupied(fwd_move[0], fwd_move[1])) {
        moves.push(fwd_move);
        if (this.num_moves === 0) {
            fwd_move = [this.r + 2 * this.d, this.c];
            if (!this.board.isOccupied(fwd_move[0], fwd_move[1])) {
                moves.push(fwd_move);
            }
        }
    }


    moves = this.getPawnAttack(moves, [this.r + this.d, this.c + 1]);
    moves = this.getPawnAttack(moves, [this.r + this.d, this.c - 1]);
    return moves;
};