// Contains the mancala board logic.
package main

import (
	"fmt"
	"slices"
)

type MancalaGameBoard struct {
	p1Name     string
	p1Row      [7]int
	p2Name     string
	p2Row      [7]int
	playerTurn int
}

func UncompressedStringToBoard(boardString string) MancalaGameBoard {
	board := MancalaGameBoard{}
	board.ResetBoard()
	for i:=0; i<=6; i++ {
		fmt.Sscanf(boardString, "%2d", &board.p1Row[i])
		boardString = boardString[2:]
	}
	for i:=0; i<=6; i++ {
		fmt.Sscanf(boardString, "%2d", &board.p2Row[i])
		boardString = boardString[2:]
	}
	fmt.Sscanf(boardString, "%d", &board.playerTurn)
	return board
}

func CompressedStringToBoard(boardString string) MancalaGameBoard {
	board := MancalaGameBoard{}
	board.ResetBoard()
	for i:=0; i<=6; i++ {
		fmt.Sscanf(boardString, "%c", &board.p1Row[i])
		board.p1Row[i] -= 48
		boardString = boardString[1:]
	}
	for i:=0; i<=6; i++ {
		fmt.Sscanf(boardString, "%c", &board.p2Row[i])
		board.p2Row[i] -= 48
		boardString = boardString[1:]
	}
	return board
}

func (mgb *MancalaGameBoard) BoardToUncompressedString() string {
	boardString := ""
	for i := 0; i <= 6; i++ {
		boardString += fmt.Sprintf("%02d", mgb.p1Row[i])
	}
	for i := 0; i <= 6; i++ {
		boardString += fmt.Sprintf("%02d", mgb.p2Row[i])
	}
	boardString += fmt.Sprintf("%d", mgb.playerTurn)
	return boardString
}

func (mgb *MancalaGameBoard) BoardToCompressedString() string {
	boardString := ""
	for i := 0; i <= 6; i++ {
		boardString += fmt.Sprintf("%c", mgb.p1Row[i] + 48)
	}
	for i := 0; i <= 6; i++ {
		boardString += fmt.Sprintf("%c", mgb.p2Row[i] + 48)
	}
	return boardString
}

func (mgb *MancalaGameBoard) PrettyString() string {
	prettyString := ""
	p2String := make([]int, len(mgb.p2Row))

	copy(p2String, mgb.p2Row[:])

	slices.Reverse(p2String)

	for i := 0; i < 7; i++ {
		prettyString += fmt.Sprintf("| %2d |", p2String[i])
	}

	prettyString += "|    |\n|    |"

	p1String := make([]int, len(mgb.p1Row))

	copy(p1String, mgb.p1Row[:])

	for i := 0; i < 7; i++ {
		prettyString += fmt.Sprintf("| %2d |", p1String[i])
	}

	prettyString += "\n"

	return prettyString
}

func (mgb *MancalaGameBoard) ResetBoard() {
	for i := 0; i < 6; i++ {
		mgb.p1Row[i] = 4
		mgb.p2Row[i] = 4
	}
	mgb.p1Row[6] = 0
	mgb.p2Row[6] = 0
	mgb.p1Name = "player_0"
	mgb.p2Name = "player_1"
	mgb.playerTurn = 1
}

func (mgb *MancalaGameBoard) MakeCopy() MancalaGameBoard {
	board := MancalaGameBoard{}
	board.p1Name = mgb.p1Name
	board.p2Name = mgb.p2Name
	board.playerTurn = mgb.playerTurn
	for i := 0; i < 7; i++ {
		board.p1Row[i] = mgb.p1Row[i]
		board.p2Row[i] = mgb.p2Row[i]
	}
	return board
}

// MakeMove takes in a board, a player, and a move and returns the new board
// after the move has been made.

func (board *MancalaGameBoard) MakeMove(move int) error {
	if board.playerTurn == -1 {
		return fmt.Errorf("game over, invalid move")
	}
	// Check if the move is valid
	if board.playerTurn == 1 && board.p1Row[move] == 0 {
		return fmt.Errorf("invalid move")
	}
	if board.playerTurn == 2 && board.p2Row[move] == 0 {
		return fmt.Errorf("invalid move")
	}

	// Try to correctly get the pits pointers
	var curPlayerPits, otherPlayerPits *[7]int
	if board.playerTurn == 1 {
		curPlayerPits = &board.p1Row
		otherPlayerPits = &board.p2Row
	} else if board.playerTurn == 2 {
		curPlayerPits = &board.p2Row
		otherPlayerPits = &board.p1Row
	} else {
		return fmt.Errorf("invalid player")
	}
	// Move the stones
	stones := curPlayerPits[move]
	curPlayerPits[move] = 0
	// Simple way to check if the last pit was 0 after adding a stone
	finalPitStones := -1
	finalInd := -1
	for i := 1; i <= stones; i++ {
		pitIndex := (move + i) % 13

		if pitIndex < 7 {
			curPlayerPits[pitIndex] += 1
			finalPitStones = curPlayerPits[pitIndex]
			finalInd = pitIndex
		} else {
			pitIndex = pitIndex - 7
			otherPlayerPits[pitIndex] += 1
			finalPitStones = -1
			finalInd = -1
		}
	}

	crossPit := crossPitConversion(finalInd)
	if finalPitStones == 1  && finalInd != -1 && finalInd != 6 && otherPlayerPits[crossPit] > 0 {
		curPlayerPits[6] += otherPlayerPits[crossPit] + 1
		otherPlayerPits[crossPit] = 0
		curPlayerPits[finalInd] = 0
	}

	if finalInd != 6 {
		board.playerTurn = (board.playerTurn % 2) + 1
	}

	if board.IsGameOver() {
		for i := 0; i < 6; i++ {
			curPlayerPits[6] += curPlayerPits[i]
			curPlayerPits[i] = 0
			otherPlayerPits[6] += otherPlayerPits[i]
			otherPlayerPits[i] = 0
		}
		board.playerTurn = -1
	}

	return nil
}

func crossPitConversion(index int) int {
	return 5 - index
}

func (board *MancalaGameBoard) IsGameOver() bool {
	// Check if the game is over
	p1Empty := true
	p2Empty := true
	for i := 0; i < 6; i++ {
		if board.p1Row[i] > 0 {
			p1Empty = false
		}
		if board.p2Row[i] > 0 {
			p2Empty = false
		}
	}
	if p1Empty || p2Empty {
		return true
	}
	return false
}

func (board *MancalaGameBoard) GetWinner() (int, error) {
	if !board.IsGameOver() {
		return -1, fmt.Errorf("game not over")
	}
	if board.p1Row[6] > board.p2Row[6] {
		return 1, nil
	}
	if board.p1Row[6] < board.p2Row[6] {
		return 2, nil
	}
	return 0, nil
}

func (board *MancalaGameBoard) GetValidMoves() []int {
	var validMoves []int
	if board.playerTurn == 1 {
		for i := 0; i < 6; i++ {
			if board.p1Row[i] > 0 {
				validMoves = append(validMoves, i)
			}
		}
	} else {
		for i := 0; i < 6; i++ {
			if board.p2Row[i] > 0 {
				validMoves = append(validMoves, i)
			}
		}
	}
	return validMoves
}
