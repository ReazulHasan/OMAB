package edu.unh.cs.ai.omab.algorithms

import edu.unh.cs.ai.omab.domain.Action
import edu.unh.cs.ai.omab.domain.BeliefState
import edu.unh.cs.ai.omab.domain.MDP
import edu.unh.cs.ai.omab.domain.Simulator
import org.apache.commons.math3.distribution.BetaDistribution
import java.lang.Math.log
import java.lang.Math.sqrt
import java.util.*
import java.util.stream.IntStream

/**
 * @author Bence Cserna (bence@cserna.net)
 */
fun upperConfidenceBounds(mdp: MDP, horizon: Int, simulator: Simulator): Long {
    val random = Random()
    var currentState: BeliefState = mdp.startState

    fun ucb(μ: Double, t: Int, depth: Int, α: Double): Double {
        return μ + sqrt(α * log(t.toDouble()) / (2 * depth * (t - 1)))
    }

    return IntStream.iterate(0, { i -> i + 1 }).limit(horizon.toLong()).mapToLong {
        val leftBetaDistribution = BetaDistribution(currentState.alphaLeft.toDouble(), currentState.betaLeft.toDouble())
        val rightBetaDistribution = BetaDistribution(currentState.alphaRight.toDouble(), currentState.betaRight.toDouble())

        val leftQ = ucb(currentState.leftMean(), currentState.leftSum(), currentState.totalSum(), 2.0)
        val rightQ = ucb(currentState.rightMean(), currentState.leftSum(), currentState.totalSum(), 2.0)

        val (nextState, reward) = if (leftQ > rightQ) {
            simulator.transition(currentState, Action.LEFT)
        } else {
            simulator.transition(currentState, Action.RIGHT)
        }

        currentState = nextState

        return@mapToLong reward.toLong()
    }.sum()
}