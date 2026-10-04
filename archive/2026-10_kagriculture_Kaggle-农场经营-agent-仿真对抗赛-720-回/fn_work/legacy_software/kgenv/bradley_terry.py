"""Order-independent Bradley-Terry and Davidson batch ratings.

This module is descriptive evidence only.  It is intentionally independent of
Elo and must not be read as holdout generalization evidence.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any, Iterable, Sequence


class RatingError(ValueError):
    """The observations cannot support a trustworthy global rating."""


def _logistic(value: float) -> float:
    if value >= 0:
        z = math.exp(-min(value, 700.0))
        return 1.0 / (1.0 + z)
    z = math.exp(max(value, -700.0))
    return z / (1.0 + z)


def _logsum(values: Iterable[float]) -> float:
    values = list(values)
    pivot = max(values)
    return pivot + math.log(sum(math.exp(value - pivot) for value in values))


def _softmax_logs(values: Sequence[float]) -> list[float]:
    normalizer = _logsum(values)
    return [math.exp(value - normalizer) for value in values]


def _validate_game(game: dict[str, Any]) -> tuple[str, str, str, int]:
    if not isinstance(game, dict):
        raise RatingError("games must be objects")
    players = game.get("players")
    if not isinstance(players, list) or len(players) != 2 or players[0] == players[1]:
        raise RatingError("each game needs two distinct players")
    if game.get("statuses") != ["DONE", "DONE"] or game.get("contract_ok") is not True:
        raise RatingError("rating input contains abnormal game")
    rewards = game.get("rewards")
    if (not isinstance(rewards, list) or len(rewards) != 2 or
            any(isinstance(value, bool) or not isinstance(value, (int, float)) or
                not math.isfinite(float(value)) for value in rewards)):
        raise RatingError("each rating game needs two finite rewards")
    expected_winner = (players[0] if rewards[0] > rewards[1] else
                       players[1] if rewards[1] > rewards[0] else None)
    winner = game.get("winner_label", game.get("winner"))
    if winner != expected_winner:
        raise RatingError("winner is inconsistent with rewards")
    if "winner" in game and game["winner"] != expected_winner:
        raise RatingError("winner is inconsistent with rewards")
    if "winner_label" in game and game["winner_label"] != expected_winner:
        raise RatingError("winner_label is inconsistent with rewards")
    if "seed" not in game or isinstance(game["seed"], bool) or not isinstance(game["seed"], int):
        raise RatingError("each rating game needs an integer seed")
    outcome = "A" if winner == players[0] else "B" if winner == players[1] else "T"
    return players[0], players[1], outcome, game["seed"]


def _counts(games: Sequence[dict[str, Any]]) -> tuple[dict[tuple[str, str], list[int]], set[str], set[int], dict[str, int]]:
    counts: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0, 0])
    agents: set[str] = set()
    seeds: set[int] = set()
    seats = {"AB": 0, "BA": 0}
    for game in games:
        a, b, outcome, seed = _validate_game(game)
        agents.update((a, b))
        seeds.add(seed)
        if game.get("seat") in seats:
            seats[game["seat"]] += 1
        key = (a, b) if a < b else (b, a)
        # counts are always from canonical key[0]'s perspective.
        canonical_outcome = outcome if key == (a, b) else ("B" if outcome == "A" else "A" if outcome == "B" else "T")
        counts[key][0 if canonical_outcome == "A" else 1 if canonical_outcome == "B" else 2] += 1
    return dict(counts), agents, seeds, seats


def _graph_connected(agents: set[str], counts: dict[tuple[str, str], list[int]]) -> bool:
    if not agents:
        return False
    seen = {next(iter(agents))}
    while True:
        expanded = set(seen)
        for a, b in counts:
            if a in seen or b in seen:
                expanded.update((a, b))
        if expanded == seen:
            return len(seen) == len(agents)
        seen = expanded


def _solve_linear(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            raise RatingError("singular rating information matrix")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        augmented[col] = [value / divisor for value in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor:
                augmented[row] = [left - factor * right for left, right in zip(augmented[row], augmented[col])]
    return [augmented[i][-1] for i in range(n)]


def _project_zero_sum(values: list[float]) -> list[float]:
    mean = sum(values) / len(values)
    return [value - mean for value in values]


def _bt_fit(counts: dict[tuple[str, str], list[int]], agents: list[str], regularization: float,
            max_iterations: int, tolerance: float) -> tuple[list[float], bool, int, float, bool]:
    index = {name: i for i, name in enumerate(agents)}
    abilities = [0.0] * len(agents)
    separation = any(row[0] == 0 or row[1] == 0 for row in counts.values())
    for iteration in range(1, max_iterations + 1):
        gradient = [-regularization * value for value in abilities]
        hessian = [[0.0 for _ in agents] for _ in agents]
        for i in range(len(agents)):
            hessian[i][i] = regularization
        for (a, b), (wins_a, wins_b, _ties) in sorted(counts.items()):
            ia, ib = index[a], index[b]
            n = wins_a + wins_b
            p = _logistic(abilities[ia] - abilities[ib])
            gradient[ia] += wins_a - n * p
            gradient[ib] -= wins_a - n * p
            weight = n * p * (1.0 - p)
            hessian[ia][ia] += weight
            hessian[ib][ib] += weight
            hessian[ia][ib] -= weight
            hessian[ib][ia] -= weight
        try:
            step = _solve_linear(hessian, gradient)
        except RatingError:
            raise RatingError("rating information matrix is singular")
        step = [max(-2.0, min(2.0, value)) for value in step]
        updated = _project_zero_sum([a + s for a, s in zip(abilities, step)])
        if max(abs(a - b) for a, b in zip(updated, abilities)) < tolerance:
            abilities = updated
            return abilities, True, iteration, _bt_log_likelihood(counts, index, abilities, regularization), separation
        abilities = updated
    return abilities, False, max_iterations, _bt_log_likelihood(counts, index, abilities, regularization), separation


def _bt_log_likelihood(counts, index, abilities, regularization=0.0) -> float:
    result = 0.0
    for (a, b), (wins_a, wins_b, _ties) in sorted(counts.items()):
        log_p = math.log(max(_logistic(abilities[index[a]] - abilities[index[b]]), 1e-300))
        result += wins_a * log_p + wins_b * math.log(max(1.0 - math.exp(log_p), 1e-300))
    return result - 0.5 * regularization * sum(value * value for value in abilities)


def _davidson_objective(counts, agents, abilities, log_tie, regularization):
    index = {name: i for i, name in enumerate(agents)}
    result = 0.0
    for (a, b), (wins_a, wins_b, ties) in counts.items():
        xa, xb = abilities[index[a]], abilities[index[b]]
        log_denom = _logsum((xa, xb, log_tie + 0.5 * (xa + xb)))
        result += wins_a * (xa - log_denom) + wins_b * (xb - log_denom)
        result += ties * (log_tie + 0.5 * (xa + xb) - log_denom)
    return result - 0.5 * regularization * sum(value * value for value in abilities) - 0.5 * regularization * log_tie * log_tie


def _davidson_fit(counts, agents, regularization, max_iterations, tolerance):
    index = {name: i for i, name in enumerate(agents)}
    params = [0.0] * len(agents) + [0.0]
    previous = _davidson_objective(counts, agents, params[:-1], params[-1], regularization)
    for iteration in range(1, max_iterations + 1):
        gradient = [-regularization * value for value in params]
        hessian = [[0.0 for _ in params] for _ in params]
        for i in range(len(params)):
            hessian[i][i] = regularization
        for (a, b), (wins_a, wins_b, ties) in sorted(counts.items()):
            ia, ib = index[a], index[b]
            xa, xb, log_nu = params[ia], params[ib], params[-1]
            log_terms = (xa, xb, log_nu + 0.5 * (xa + xb))
            log_denom = _logsum(log_terms)
            probabilities = [math.exp(value - log_denom) for value in log_terms]
            observations = [wins_a, wins_b, ties]
            features = []
            for outcome in range(3):
                feature = [0.0] * len(params)
                if outcome == 0:
                    feature[ia] = 1.0
                elif outcome == 1:
                    feature[ib] = 1.0
                else:
                    feature[ia] = feature[ib] = 0.5
                    feature[-1] = 1.0
                features.append(feature)
            total = sum(observations)
            expected_features = [sum(p * feature[position] for p, feature in zip(probabilities, features))
                                 for position in range(len(params))]
            observed_features = [sum(n * feature[position] for n, feature in zip(observations, features))
                                 for position in range(len(params))]
            for position in range(len(params)):
                gradient[position] += observed_features[position] - total * expected_features[position]
            for left in range(len(params)):
                for right in range(len(params)):
                    covariance = sum(p * feature[left] * feature[right] for p, feature in zip(probabilities, features))
                    hessian[left][right] += total * (covariance - expected_features[left] * expected_features[right])
        try:
            step = _solve_linear(hessian, gradient)
        except RatingError:
            raise RatingError("singular Davidson information matrix")
        step = [max(-2.0, min(2.0, value)) for value in step]
        # The zero-sum projection removes the ability translation null direction.
        candidate = params[:]
        candidate[:-1] = _project_zero_sum([a + s for a, s in zip(params[:-1], step[:-1])])
        candidate[-1] += step[-1]
        objective = _davidson_objective(counts, agents, candidate[:-1], candidate[-1], regularization)
        scale = 0.5
        while objective < previous and scale > 1e-8:
            candidate = params[:]
            candidate[:-1] = _project_zero_sum([a + scale * s for a, s in zip(params[:-1], step[:-1])])
            candidate[-1] += scale * step[-1]
            objective = _davidson_objective(counts, agents, candidate[:-1], candidate[-1], regularization)
            scale *= 0.5
        if objective < previous:
            break
        params, previous = candidate, objective
        if max(abs(value) for value in step) * scale < tolerance:
            return params[:-1], params[-1], True, iteration, previous
    return params[:-1], params[-1], False, iteration, previous


def _strict_count(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RatingError(f"pair counts {field} must be a non-negative integer")
    if value < 0:
        raise RatingError(f"pair counts {field} cannot be negative")
    return value


def _parse_pair_count_rows(pair_counts: Sequence[dict[str, Any]]) -> tuple[dict[tuple[str, str], list[int]], set[str]]:
    parsed: dict[tuple[str, str], list[int]] = {}
    agents: set[str] = set()
    for row in pair_counts:
        if not isinstance(row, dict) or not all(key in row for key in ("a", "b", "wins_a", "wins_b", "ties")):
            raise RatingError("pair counts require a, b, wins_a, wins_b, ties")
        a, b = row["a"], row["b"]
        if not isinstance(a, str) or not isinstance(b, str) or not a or not b or a == b:
            raise RatingError("pair counts require two distinct agent names")
        key = (a, b) if a < b else (b, a)
        if key in parsed:
            raise RatingError("duplicate canonical pair in pair counts")
        values = [_strict_count(row["wins_a"], "wins_a"),
                  _strict_count(row["wins_b"], "wins_b"),
                  _strict_count(row["ties"], "ties")]
        if key != (a, b):
            values[0], values[1] = values[1], values[0]
        if sum(values) == 0:
            raise RatingError("pair counts total must be positive")
        parsed[key] = values
        agents.update((a, b))
    if not parsed:
        raise RatingError("pair counts are required")
    return parsed, agents


def _parse_pair_counts(pair_counts: Sequence[dict[str, Any]], games_counts):
    parsed, _ = _parse_pair_count_rows(pair_counts)
    if set(parsed) != set(games_counts):
        raise RatingError("pair counts aggregate does not cover every games pair")
    for key, values in parsed.items():
        if games_counts.get(key) != values:
            raise RatingError("pair counts aggregate does not match games")


def _percentile(values: list[float], quantile: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    position = (len(values) - 1) * quantile
    lower, upper = int(position), min(int(position) + 1, len(values) - 1)
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def tier_from_interval(interval: Sequence[float], margin: float = 0.3) -> str:
    """Classify a difference only when its complete CI clears a fixed margin."""
    low, high = float(interval[0]), float(interval[1])
    if low > margin:
        return "higher"
    if high < -margin:
        return "lower"
    if low >= -margin and high <= margin:
        return "same"
    return "uncertain"


def _validate_parameter(value: Any, name: str, *, integer: bool = False,
                        minimum: float | None = None) -> None:
    if integer:
        if isinstance(value, bool) or not isinstance(value, int):
            raise RatingError(f"{name} must be an integer")
    elif isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise RatingError(f"{name} must be finite")
    if minimum is not None and value < minimum:
        requirement = "non-negative" if minimum == 0 else "positive"
        raise RatingError(f"{name} must be {requirement}")


def fit_ratings(games: Sequence[dict[str, Any]] | None = None, *, pair_counts: Sequence[dict[str, Any]] | None = None,
                bootstrap_samples: int = 200, bootstrap_seed: int = 20260831,
                regularization: float = 1e-4, max_iterations: int = 400,
                tolerance: float = 1e-8, tier_margin: float = 0.3,
                _bootstrap: bool = True, min_seed_clusters: int = 4,
                require_ab_ba: bool = False, allow_nonconverged: bool = False) -> dict[str, Any]:
    """Fit one batch from games or validated pair counts, independent of row order."""
    _validate_parameter(bootstrap_samples, "bootstrap_samples", integer=True, minimum=0)
    _validate_parameter(bootstrap_seed, "bootstrap_seed", integer=True)
    _validate_parameter(max_iterations, "max_iterations", integer=True, minimum=1)
    _validate_parameter(regularization, "regularization", minimum=0.0)
    _validate_parameter(tolerance, "tolerance", minimum=0.0)
    _validate_parameter(tier_margin, "tier_margin", minimum=0.0)
    _validate_parameter(min_seed_clusters, "min_seed_clusters", integer=True, minimum=1)
    games = list(games or [])
    if games:
        counts, agent_set, seeds, seats = _counts(games)
        if pair_counts is not None:
            _parse_pair_counts(pair_counts, counts)
    elif pair_counts:
        counts, agent_set = _parse_pair_count_rows(pair_counts)
        seeds, seats = set(), {"AB": 0, "BA": 0}
    else:
        raise RatingError("rating games or pair counts are required")
    if not counts or not agent_set:
        raise RatingError("rating comparisons are required")
    incomplete_pairs = False
    if games:
        grouped_rows: dict[tuple[tuple[str, str], int], list[dict[str, Any]]] = {}
        canonical_order: dict[tuple[str, str], tuple[str, str]] = {}
        for game in games:
            unordered_pair = tuple(sorted(game["players"]))
            if game.get("seat") == "AB":
                canonical_order.setdefault(unordered_pair, tuple(game["players"]))
            grouped_rows.setdefault((unordered_pair, game["seed"]), []).append(game)
        incomplete_pairs = any(len(rows) != 2 or {row.get("seat") for row in rows} != {"AB", "BA"}
                               for rows in grouped_rows.values())
        if require_ab_ba:
            for (unordered_pair, _seed), rows in grouped_rows.items():
                if len(rows) != 2 or {row.get("seat") for row in rows} != {"AB", "BA"}:
                    raise RatingError("each pair and seed requires exactly one AB and one BA")
                a, b = canonical_order[unordered_pair]
                for row in rows:
                    expected_players = [a, b] if row["seat"] == "AB" else [b, a]
                    if row["players"] != expected_players:
                        raise RatingError("seat and player order are inconsistent with first game pair ordering")
    if not _graph_connected(agent_set, counts):
        raise RatingError("comparison graph is disconnected; no unique global ranking")
    agents = sorted(agent_set)
    separation = any((row[0] == 0 or row[1] == 0) and row[2] == 0 for row in counts.values())
    ties = any(row[2] for row in counts.values())
    if ties:
        abilities, log_tie_parameter, converged, iterations, ll = _davidson_fit(counts, agents, regularization, max_iterations, tolerance)
        tie_parameter = math.exp(log_tie_parameter)
        model = "davidson"
    else:
        abilities, converged, iterations, ll, separation = _bt_fit(counts, agents, regularization, max_iterations, tolerance)
        log_tie_parameter = None
        tie_parameter = None
        model = "bradley-terry"
    if not converged and not allow_nonconverged:
        raise RatingError(f"{model} optimizer did not converge within {max_iterations} iterations")
    inference_reasons = []
    if not converged:
        inference_reasons.append("optimizer_nonconverged_diagnostic_only")
    if not games:
        inference_reasons.append("pair_counts_have_no_seed_clusters")
    if len(seeds) < min_seed_clusters:
        inference_reasons.append(f"requires_{min_seed_clusters}_independent_seed_clusters")
    if incomplete_pairs:
        inference_reasons.append("each_pair_and_seed_requires_complete_AB_BA")
    if require_ab_ba and games:
        for key in counts:
            rows = [game for game in games if tuple(sorted(game["players"])) == key]
            if not {game.get("seat") for game in rows} >= {"AB", "BA"}:
                inference_reasons.append("each_pair_requires_complete_AB_BA")
                break
    if separation:
        inference_reasons.append("complete_separation_is_regularized_diagnostic")
    inference_status = "inferential" if not inference_reasons else "insufficient_data"
    separation = any((row[0] == 0 or row[1] == 0) and row[2] == 0 for row in counts.values())
    by_agent = {name: abilities[i] for i, name in enumerate(agents)}
    pairwise = []
    for i, a in enumerate(agents):
        for b in agents[i + 1:]:
            xa, xb = by_agent[a], by_agent[b]
            if model == "davidson":
                probs = _softmax_logs((xa, xb, log_tie_parameter + 0.5 * (xa + xb)))
                probs = (probs[0], probs[2], probs[1])
            else:
                p = _logistic(xa - xb)
                probs = (p, 0.0, 1.0 - p)
            pairwise.append({"a": a, "b": b, "p_a_win": probs[0], "p_tie": probs[1], "p_b_win": probs[2],
                             "ability_difference": xa - xb,
                             "probability_status": "inferential" if inference_status == "inferential" else "regularized_descriptive"})
    bootstrap = {"samples_requested": int(bootstrap_samples), "samples_used": 0,
                 "seed": int(bootstrap_seed), "cluster_unit": "seed", "failed_disconnected": 0}
    ci_values = {name: [] for name in agents}
    pair_ci = {(row["a"], row["b"]): [] for row in pairwise}
    if _bootstrap and bootstrap_samples and games:
        grouped = {seed: [game for game in games if game["seed"] == seed] for seed in sorted(seeds)}
        rng = random.Random(bootstrap_seed)
        seed_values = sorted(grouped)
        for _ in range(bootstrap_samples):
            selected_seeds = [seed_values[rng.randrange(len(seed_values))] for _ in seed_values]
            sample = []
            for cluster_index, seed in enumerate(selected_seeds):
                for game in grouped[seed]:
                    row = dict(game)
                    row["seed"] = cluster_index
                    sample.append(row)
            try:
                child = fit_ratings(sample, bootstrap_samples=0, regularization=regularization,
                                    max_iterations=max_iterations, tolerance=tolerance,
                                    _bootstrap=False, min_seed_clusters=min_seed_clusters,
                                    require_ab_ba=require_ab_ba)
            except RatingError:
                bootstrap["failed_disconnected"] += 1
                continue
            bootstrap["samples_used"] += 1
            values = {row["agent"]: row["ability"] for row in child["agents"]}
            for name in agents:
                ci_values[name].append(values.get(name, 0.0))
            for row in child["pairwise_probabilities"]:
                pair_ci[(row["a"], row["b"])].append(row["ability_difference"])
    if (inference_status == "inferential" and bootstrap_samples and
            bootstrap["samples_used"] < max(10, bootstrap_samples // 2)):
        inference_reasons.append("insufficient_successful_bootstrap_samples")
        inference_status = "insufficient_data"
        for row in pairwise:
            row["probability_status"] = "regularized_descriptive"
    agent_rows = []
    for name in agents:
        interval = ([None, None] if inference_status != "inferential" else
                    ([_percentile(ci_values[name], 0.025), _percentile(ci_values[name], 0.975)] if ci_values[name] else [None, None]))
        agent_rows.append({"agent": name, "ability": by_agent[name],
                           "rank": 1 + sum(value > by_agent[name] for value in abilities),
                           "ci95": interval, "tier": "reference" if inference_status == "inferential" else "insufficient_data"})
    for row in pairwise:
        values = pair_ci[(row["a"], row["b"])]
        row["difference_ci95"] = ([None, None] if inference_status != "inferential" else
                                   ([_percentile(values, 0.025), _percentile(values, 0.975)] if values else [None, None]))
        row["tier"] = (tier_from_interval(row["difference_ci95"], tier_margin)
                        if inference_status == "inferential" and values else "insufficient_data")
    return {
        "model": model, "identifiability": "zero_sum", "converged": bool(converged),
        "inference_status": inference_status, "inference_reasons": inference_reasons,
        "iterations": int(iterations), "log_likelihood": float(ll),
        "abilities_are_descriptive_only": True, "tie_parameter": tie_parameter,
        "tie_parameter_parameterization": "nu = exp(log_nu)" if model == "davidson" else None,
        "separation_detected": separation,
        "regularization": {"type": "zero-mean Gaussian MAP", "lambda": regularization,
                            "disclosed_for_separation": bool(separation)},
        "agents": agent_rows, "pairwise_probabilities": pairwise,
        "seat_counts": {"AB": seats["AB"], "BA": seats["BA"]},
        "game_count": len(games), "seed_count": len(seeds), "bootstrap": bootstrap,
        "tier_margin": tier_margin,
    }
