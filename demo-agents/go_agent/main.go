package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"sync"
	"time"
)

type pair struct {
	p1Winner int
	p1Move   int

	p2Winner int
	p2Move   int
}

type MancalaBestMoves struct {
	// Mutex
	mu sync.RWMutex
	// BestMoves map[string]
	BestMoves map[string]pair
}

func main() {
	TEST := false
	if !TEST {
		scanner := bufio.NewScanner(bufio.NewReader(os.Stdin))
		ok := scanner.Scan()
		if !ok {
			fmt.Println("Scan failed:", scanner.Err())
			os.Exit(1)
		}
		board := UncompressedStringToBoard(scanner.Text())
		// fmt.Println(board.PrettyString())
		os.Exit(IterativeParentAB(&board, 30))
	}

	depth13Test()

	// userInputTest()
	// return
	// moves := findBestMoves()
	// fmt.Print(moves)
	// alphaBetaTest()
	// iterativeAlphaBetaTest()
	// iterativeVsAlphaBetaTest()
	// iterativeVsRandomAlphaBetaTest()
}

func depth13Test() {
	i := 13
	board := MancalaGameBoard{}
	board.ResetBoard()
	// Test
	startTime := time.Now()
	AlphaBetaAgent(&board, i)
	endTime := time.Now()
	fmt.Printf("AlphaBeta: Depth: %d Found in %ds \n", i, int(endTime.Sub(startTime).Seconds()))
	startTime = time.Now()
	board.ResetBoard()
	IterativeParentAB13Test(&board, 60)
}

func iterativeVsRandomAlphaBetaTest() {
	startGameTime := time.Now()
	maxTurnTime := 30
	board := MancalaGameBoard{}
	board.ResetBoard()
	// Test
	for i := 1; !board.IsGameOver(); i++ {
		fmt.Println(board.PrettyString())
		startTime := time.Now()
		var move int
		if board.playerTurn == 2 {
			move = IterativeParentAB(&board, maxTurnTime)
		} else {
			move = randMove(board)
		}
		endTime := time.Now()
		fmt.Printf("Turn Number: %d, Turn: %d, Move: %d, Found in %ds \n", i, board.playerTurn, move, int(endTime.Sub(startTime).Seconds()))
		board.MakeMove(move)
	}
	val, err := board.GetWinner()
	if err != nil {
		fmt.Print(err)
	}
	fmt.Printf("Player %d wins! Found in %ds\n", val, int(time.Since(startGameTime).Seconds()))
}

func iterativeAlphaBetaTest() {
	startGameTime := time.Now()
	maxTurnTime := 30
	board := MancalaGameBoard{}
	board.ResetBoard()
	// Test
	for i := 1; !board.IsGameOver(); i++ {
		fmt.Println(board.PrettyString())
		startTime := time.Now()
		move := IterativeParentAB(&board, maxTurnTime)
		endTime := time.Now()
		fmt.Printf("Turn Number: %d, Turn: %d, Move: %d, Found in %ds \n", i, board.playerTurn, move, int(endTime.Sub(startTime).Seconds()))
		board.MakeMove(move)
	}
	val, err := board.GetWinner()
	if err != nil {
		fmt.Print(err)
	}
	fmt.Printf("Player %d wins! Found in %ds\n", val, int(time.Since(startGameTime).Seconds()))
}

func iterativeVsAlphaBetaTest() {
	alphaBetaDepth := 13
	startGameTime := time.Now()
	maxTurnTime := 30
	board := MancalaGameBoard{}
	board.ResetBoard()
	// Test
	for i := 1; !board.IsGameOver(); i++ {
		fmt.Println(board.PrettyString())
		var move int
		startTime := time.Now()
		if board.playerTurn == 1 {
			move = IterativeParentAB(&board, maxTurnTime)
		} else {
			move, _ = AlphaBetaAgent(&board, alphaBetaDepth)
		}
		endTime := time.Now()
		fmt.Printf("Turn Number: %d, Turn: %d, Move: %d, Found in %ds \n", i, board.playerTurn, move, int(endTime.Sub(startTime).Seconds()))
		board.MakeMove(move)
	}
	val, err := board.GetWinner()
	if err != nil {
		fmt.Print(err)
	}
	fmt.Printf("Player %d wins! Found in %ds\n", val, int(time.Since(startGameTime).Seconds()))
}

func alphaBetaTest() {
	board := MancalaGameBoard{}
	board.ResetBoard()
	// Test
	for i := 2; i <= 20; i++ {
		startTime := time.Now()
		move, _ := AlphaBetaAgent(&board, i)
		endTime := time.Now()
		fmt.Printf("Depth: %d, Turn: %d, Move: %d, Found in %ds \n", i, board.playerTurn, move, int(endTime.Sub(startTime).Seconds()))
	}
}

func userInputTest() {
	board := MancalaGameBoard{}
	board.ResetBoard()
	// board.MakeMove(5)
	// board.MakeMove(2)
	// board.MakeMove(1)
	for !board.IsGameOver() {
		fmt.Printf("Player %d's turn\n", board.playerTurn)
		fmt.Print(board.PrettyString())
		// Get user input
		// fmt.Print("Enter move: ")
		// var move int
		// fmt.Scanln(&move)
		move := randMove(board)
		fmt.Printf("Move: %d\n", move)
		// Make move
		if err := board.MakeMove(move); err != nil {
			fmt.Print(err)
		}
		fmt.Print(board.PrettyString())
		fmt.Print("\n\n\n")
	}

	val, err := board.GetWinner()
	if err != nil {
		fmt.Print(err)
	}
	fmt.Printf("Player %d wins!\n", val)
}

func randMove(board MancalaGameBoard) int {
	validMoves := board.GetValidMoves()
	randMove := rand.Intn(len(validMoves))
	return validMoves[randMove]
}

// func test() {
// 	board := MancalaGameBoard{}
// 	board.ResetBoard()
// 	// Test
// 	s := board.BoardToCompressedString()
// 	fmt.Print(s + "\n")
// 	board2 := CompressedStringToBoard(s)
// 	print(board2.BoardToCompressedString() + "\n")
// 	print(board2.BoardToUncompressedString() + "\n")
// 	// fmt.Print(board.BoardToUncompressedString() + "\n")
// 	// fmt.Print(board.BoardToCompressedString())
// }

func findBestMoves() map[string]pair {
	// Initialize
	moves := MancalaBestMoves{}
	moves.BestMoves = make(map[string]pair)
	// Start with empty board
	board := MancalaGameBoard{}
	board.ResetBoard()
	// Find best moves
	findBestMove(board, &moves)
	// Return
	return moves.BestMoves
}

func findBestMove(board MancalaGameBoard, moves *MancalaBestMoves) int {
	// print(board.PrettyString() + "\n")
	compressedStringBoard := board.BoardToCompressedString()
	// Check if the board has been seen before
	moves.mu.RLock()
	val, ok := moves.BestMoves[compressedStringBoard]
	moveLength := len(moves.BestMoves)
	moves.mu.RUnlock()

	if moveLength%1000000 == 0 {
		fmt.Printf("Moves: %d\n", moveLength)
	}

	if ok {
		if board.playerTurn == 1 && val.p1Winner != -1 && val.p1Move != -1 {
			return val.p1Winner
		} else if board.playerTurn == 2 && val.p2Winner != -1 && val.p2Move != -1 {
			return val.p2Winner
		}
	}

	winner := -1
	if board.IsGameOver() {
		var err error
		// If so, return the score
		winner, err = board.GetWinner()
		if err != nil {
			fmt.Print(err)
		}

	}

	var bestMove int
	if winner == -1 {
		bestMove, winner = decideBestOption(board, moves)
	}

	currentPlayer := board.playerTurn

	moves.mu.Lock()
	val, ok = moves.BestMoves[compressedStringBoard]

	var curPair pair
	if ok {
		curPair = val
	} else {
		curPair = pair{p1Winner: -1, p1Move: -1, p2Winner: -1, p2Move: -1}
	}

	if currentPlayer == 1 {
		curPair.p1Move = bestMove
		curPair.p1Winner = winner
	} else {
		curPair.p2Move = bestMove
		curPair.p2Winner = winner
	}

	moves.BestMoves[compressedStringBoard] = curPair

	moves.mu.Unlock()

	return winner
}

func decideBestOption(board MancalaGameBoard, moves *MancalaBestMoves) (int, int) {
	bestOption := -1
	bestWinner := -1
	validMoves := board.GetValidMoves()
	currentPlayer := board.playerTurn
	for _, move := range validMoves {
		newBoard := board.MakeCopy()
		if err := newBoard.MakeMove(move); err != nil {
			fmt.Print(err)
		}
		var winner int
		if newBoard.IsGameOver() {
			var err error
			// If so, return the score
			winner, err = newBoard.GetWinner()
			if err != nil {
				fmt.Print(err)
			}
		} else {
			winner = findBestMove(newBoard, moves)
		}
		if winner == currentPlayer {
			bestOption = move
			bestWinner = winner
			break
		} else if winner == 0 {
			if bestOption == -1 {
				bestOption = move
				bestWinner = winner
			}
		}
	}
	if bestOption == -1 {
		bestOption = validMoves[0]
		bestWinner = (currentPlayer % 2) + 1
	}

	return bestOption, bestWinner
}
