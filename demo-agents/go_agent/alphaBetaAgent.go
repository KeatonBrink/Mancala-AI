package main

import (
	"fmt"
	"math"
	"time"
)

type SharedData struct {
	my_side         int
	max_depth       int
	evaluated_nodes int
}

func AlphaBetaAgent(env *MancalaGameBoard, depth int) (int, float64) {
	sharedData := SharedData{my_side: env.playerTurn, max_depth: depth, evaluated_nodes: 0}

	bestMove := -1
	bestScore := math.Inf(-1)
	alpha := math.Inf(-1)
	beta := math.Inf(1)
	for _, move := range env.GetValidMoves() {
		newEnv := env.MakeCopy()
		newEnv.MakeMove(move)
		val := 0.0
		if newEnv.playerTurn == sharedData.my_side {
			val = AlphaBetaMax(&newEnv, 1, alpha, beta, &sharedData)
		} else {
			val = AlphaBetaMin(&newEnv, 2, alpha, beta, &sharedData)
		}
		if val > bestScore {
			bestScore = val
			bestMove = move
		}
	}
	if bestMove == -1 {
		bestMove = env.GetValidMoves()[0]
	}
	// print("Evaluated ", sharedData.evaluated_nodes, " nodes\n")
	return bestMove, bestScore
}

func AlphaBetaMax(env *MancalaGameBoard, depth int, alpha float64, beta float64, sharedData *SharedData) float64 {
	if depth == sharedData.max_depth || env.IsGameOver() {
		return AlphaBetaEval(env, sharedData)
	}
	bestScore := math.Inf(-1)
	for _, move := range env.GetValidMoves() {
		newEnv := env.MakeCopy()
		newEnv.MakeMove(move)
		val := 0.0
		if newEnv.playerTurn == sharedData.my_side {
			val = AlphaBetaMax(&newEnv, depth, alpha, beta, sharedData)
		} else {
			val = AlphaBetaMin(&newEnv, depth+1, alpha, beta, sharedData)
		}
		if val > bestScore {
			bestScore = val
			if bestScore >= beta {
				return bestScore
			}
			if bestScore > alpha {
				alpha = bestScore
			}
		}
	}
	return bestScore
}

func AlphaBetaMin(env *MancalaGameBoard, depth int, alpha float64, beta float64, sharedData *SharedData) float64 {
	if depth == sharedData.max_depth || env.IsGameOver() {
		return AlphaBetaEval(env, sharedData)
	}
	bestScore := math.Inf(1)
	for _, move := range env.GetValidMoves() {
		newEnv := env.MakeCopy()
		newEnv.MakeMove(move)
		val := 0.0
		if newEnv.playerTurn == sharedData.my_side {
			val = AlphaBetaMax(&newEnv, depth+1, alpha, beta, sharedData)
		} else {
			val = AlphaBetaMin(&newEnv, depth, alpha, beta, sharedData)
		}
		if val < bestScore {
			bestScore = val
			if bestScore <= alpha {
				return bestScore
			}
			if bestScore < beta {
				beta = bestScore
			}
		}
	}
	return bestScore
}

func AlphaBetaEval(env *MancalaGameBoard, sharedData *SharedData) float64 {
	sharedData.evaluated_nodes++
	if env.IsGameOver() {
		winner, err := env.GetWinner()
		if err != nil {
			panic("AlphaBetaEval game not over")
		}
		if winner == sharedData.my_side {
			return math.Inf(1)
		} else if winner == 0 {
			return 0
		} else {
			return math.Inf(-1)
		}
	}
	// Try to correctly get the pits pointers
	var curPlayerPits, otherPlayerPits *[7]int
	if sharedData.my_side == 1 {
		curPlayerPits = &env.p1Row
		otherPlayerPits = &env.p2Row
	} else if sharedData.my_side == 2 {
		curPlayerPits = &env.p2Row
		otherPlayerPits = &env.p1Row
	} else {
		panic("AlphaBetaEval invalid player")
	}

	score := 0.0
	for i := 0; i < 6; i++ {
		score += float64(curPlayerPits[i]) - float64(otherPlayerPits[i])
	}
	score += float64(curPlayerPits[6])*3 - float64(otherPlayerPits[6])*3

	return score
}

type BestMove struct {
	move  int
	depth int
	score float64
}

func IterativeParentAB(mgb *MancalaGameBoard, timeLimit int) int {
	MAX_GOROUTINES := 4
	start := time.Now()
	bestMove := BestMove{move: -1, depth: -1}
	// Initial go routines

	c := make(chan BestMove, MAX_GOROUTINES)
	depth := 11
	for i := 0; i < MAX_GOROUTINES; i, depth = i+1, depth+1 {
		tempBoard := mgb.MakeCopy()
		go AlphaBetaGoRoutine(&tempBoard, c, depth)
	}

	for time.Since(start).Seconds() < float64(timeLimit) {
		if len(c) > 0 {
			newMove := <-c
			fmt.Printf("Depth: %d, Move: %d\n", newMove.depth, newMove.move)
			if newMove.depth > bestMove.depth {
				bestMove = newMove
				if bestMove.move == -1 || bestMove.score == math.Inf(1) || bestMove.score == math.Inf(-1) {
					break
				}
			}
			depth = depth + 1
			tempBoard := mgb.MakeCopy()
			go AlphaBetaGoRoutine(&tempBoard, c, depth)
		}
	}
	return bestMove.move
}

func IterativeParentAB13Test(mgb *MancalaGameBoard, timeLimit int) int {
	MAX_GOROUTINES := 4
	start := time.Now()
	bestMove := BestMove{move: -1, depth: -1}
	// Initial go routines

	c := make(chan BestMove, MAX_GOROUTINES)
	depth := 13
	var startTime time.Time
	for i := 0; i < MAX_GOROUTINES; i, depth = i+1, depth+1 {
		tempBoard := mgb.MakeCopy()
		if depth == 13 {
			startTime = time.Now()
		}
		go AlphaBetaGoRoutine(&tempBoard, c, depth)
	}

	for time.Since(start).Seconds() < float64(timeLimit) {
		if len(c) > 0 {
			newMove := <-c
			if newMove.depth == 13 {
				fmt.Printf("IterativeParentAB13Test: Depth: %d, Time: %f\n", newMove.depth, time.Since(startTime).Seconds())
				return bestMove.move
			}
			if newMove.depth > bestMove.depth {
				bestMove = newMove
				if bestMove.move == -1 || bestMove.score == math.Inf(1) || bestMove.score == math.Inf(-1) {
					break
				}
			}
			depth = depth + 1
			tempBoard := mgb.MakeCopy()
			go AlphaBetaGoRoutine(&tempBoard, c, depth)
		}
	}
	return bestMove.move
}

func AlphaBetaGoRoutine(board *MancalaGameBoard, ch chan BestMove, depth int) {
	bestMove, best_score := AlphaBetaAgent(board, depth)
	ch <- BestMove{move: bestMove, depth: depth, score: best_score}
}
