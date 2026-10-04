# Strategy: Use the inspected Pipe-16 HybridOpening controller. Reassign idle workers during the first three days to plant, water and harvest one temporary wheat crop, then restore the planned pasture and deliver the wheat. Preserve the public Metav4 production and market controller. This is attributed reuse, and its stronger public source still needs live confirmation. Disable optional environment-dependent external library loading so the archive is self-contained.
# Local packaging modifications, 2026-09-20. Original attribution retained.
# Kaggriculture submission v9/3: public V39 (Apache-2.0, notices below) plus the v9 layers
# RACEPX gate, RACE (reservation from step 192, horizon 40 / margin 12), COURIER, CARROT and HERD
# appended at the end of this file.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent

# Modified 2026-09-22: public DSM episode 111918050 action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode('c%0o`O>ZPua{Mnm_d!dJ)|PM73|AT~B?=_RgS8+C0=$L+V||c)GyLB@BH7iiUPeYlW>s_KJ*m~rsd^vz@*^@b-;e)u@o&HU`nSLSdht&`Ui@(V@Nn_d;o{$a`Okm-uTNim`uMkBe*KTX{`aTPKVE$O;V(a5fB*iw>)VUN#oN1&7l%Lmba?*yhx@yCAKpHG`u^j$H`ky3`{hqR{qJG*==X2`{Nab;A0{t(xVgPOJ?7~J-@d=Uxey=7*p{y!zP-8mG=i&nXkUMLfBWv|Pji3#@bt80WW%Um{_WF4`Io1c$G_uKomcGk`t1!`upckJzq^0@_G#Ye)5n{K#|!bUY~SK2j+1!#gR9j*o?mqsKAeUzE$dF>`P0qKyY(K;+Xn}8TugH-?BTq;Y809IO>rp>%Srq3;_Y=@oZnvk@Y_5O7vJ67-hF>@xZJWp&#yp>a0oj%4n$7%;qJpq<lsz^G@=R0Y0Q%N2fV|l^Y`)_nbOP3z?1dqdEY-S1DxLVw0otsdYR9#^XUu9Yc)R!&gbLx<IVl_Nxkr8rNax4Pe7Vr)<eTgpC9KPz4Zv9IhiaKT2AMimzk&)h-xvsAFXeBrJeT#mFumu@iM5)#wX4PZu+ggnA4Nss-~~gIwqYj5#z9RJFM^VN$7niUHU5P8ecLf^V6CKJ=b2><(a4Vgil1F9{(0vpWY+i-re5bynX!nPdE3E?{DA#%X-M`Njom6{4l-$-TmDUnX(R_$UK--EvBFNgv0zNe;Ya+!5Hv$3}Yzy9AMi|OOrjAJTI<!d<a=H;TvDBpN!Te{rcwm<@L`Wyq)qk2nfjOoGkAx40i`-4h&%V(DWF=G><-ESh&UyTov}+*vnO@IDUDu>)_o$B(5gkDH{_wREu}o-wj(F!Rvu5bM%tYad2GX;5RK(G_|bv8ma-NHC(+B*r$!_3cNQNYV=~6<+)&9+Fr#Y!Gf;%O_T^78!QX4jGXv5oyX-zwed8t3L73v0+ZgZzmf+h&2PnlYr={cXw)E#=iBAS$C`csFESTq{6^?J=xIn<15;vnfOf3H8<z2diGZ&%qouWI%co<@yzS7Pj)U?WJzeZB13(eQ`?IB)f^@tN$n+WTg!UrA!j#_&d^q4GUiSP-Q#&^o2x6wuYB`Y^)D3SYm-FHA{`%wBH~05{v4%H$AwWt>3&UR@QHco3B2E15_5DA)GDJskdJxy0U|ANi-ZX%tV=?@Z!WJh#=>UMD-L?bhigE3uj4Z!4;SsRV%ZJsQ!Mg1>Yp}4nOSsy(jXMCvF-jbBo>dgHNgBZ_gbycmzq2foSAh)^Q7U~oaE#;2nQXLtZ|fCj@b8yZ>_rhQ9eoauUz)Hyw9kDa&j(NO*5LO?=XjM(z>Y^D(qM)gB`~Hv`lI&Eov?!?Yn5M~gFhvpVp-qW9D@m3uaMX|o>#i5gXk?GAjy(Vqj{MXJi%z9YSk-AheTTj>1SgEvbbz~B@9cJ*8-NKBMHXW^jm<t68R4#!q9FE*quwVJ5GiZoQoKvjm{Rd<VCSDVz@Y(<-;i~z+TrjAKb|319MrCUz#-o1~@v_4U82y@5pIM{Mfn)0wQyO^F00N96R6&A|)92Y;q5G^97OOjUqcQbxpA(yTY|Ud*v2T0EC=OX61arnrc_R^ach@B}*H3aMOekc>`J?7P$#m`_1QewZVW&Za0V>(3d619iY%9-&?zg%=w0gk<%pGs6R<JpaGp6FW(y`4mX-<k1o@6xzV}m_}GLQnwgT7xzRZUX25`H_EK+K6uJr%5DHvaP&!{gJ3~Nb!x>L=07yWA0o&w6f=Q!{6LD=_FWU&fmS=LIO2j}LqVf)>#(X!Y47>qsc7aSJ7nv)4By%QfC`^|{*le~1N(q}D3xXn1BnxHB5j}kyi~t(hTr>4g0a0%g<GWeRKnBrttm*t%GHWYq#9YNTto#~|?N#dA)%ix2%X&)UFQr0=kSI|B0*^CLU=!&jP9pb(FRRWXBd&6LHrm?Ri{0Rzj<p_UY*CytvF{t4@UH1`Gbs6f&>EbwnJ_4whamOa9m{p89(37hF^m=93DE=2xq&_lwtzD*mc3-S4W%$!L^ml8j)$)n!DlWr9XdPVd$<fPsx+@cH>&~W*IPp`1{VHZ<LFv$2+$N=ET7`u6{T;wSqy=0prm|}0Hv?taswt)eDHjD_jE{!vaSf%IS^O)!Q+QQ?$F6OfwV&ln8XLPCBX*08h^E=o(zx$5733exlbc?{_*ba_BT>R0j@`W%ZW6i{3h^kMNya^jGlaC<xQVf?q$*A5b1Kgi1zLE_wPbT7Tx^i9ie$bhuVt-5dSl03TB@Zo*&OndZ@II5f|)#qH->*Eef_;LmqH?i1ckjix(n+$b&?hO6+F%ClPCm8zjXrw$nHb7c>>=uPp3~q9p+|6p`oTBncx>N|U4_v~;9D=`TTnUl|d#8vy~YCSQirA3O_);o27_3EWuV+@TW@1rW?>Mw>S5TqOqrP9_r4>AR^V0+`Mw!gGW-;u4ZY1zfghnoEkPW<W-CatpJXC=H++Kvq;86V-UDzh5X~A$oXF0cy;eOTLTQmowx?9_<}XJnoe5jN^=_bvYiu*;cZ%50f8|43`y&9Bm*sN=O?0gevAP*mn{s#}i9;pEQGOY&9zaEvO0J6K>;bT1}0@V1e;rjgRICvx|uVY!{GQU{*g^brF}!){l8VnjM?(0G3KxA$_R!a<OwFaA>SQ0+jM<Sju1#BSRH4aH=TUUnPdhxLKuggCd#I^JfAm?pw+)^d35uAPV2nv)Z9zLY^fp(N<O<G2yJRAz&bHn%G+Wzz4diJdBDw(;=#2-$?2K1J7p_Eo)fxfZ2e+REs@`77)1t6f3YCK$js)h@4DTQfi@yLrZPK!g{mDv5+|}r2_=4@JWg>U6+3^%@{Mqv2lvkF^KDzG(yvghn?dX@<VtD;Y{cskjM3+ApjSKWHoVeW7b<VNeeo9w@`E4s~N8;aF<iOX4g0ab|*=jwwmNW+k@>30|<f`+70r!V0{rlx^aC8L=s#U42u9fB5TmJm&nE;j(Mysnnt*yE4tkQ0@0*E0{BW{vKfGkQpQeXPI*{48rDo+11Wb_1N>Qubi|{67`xGbA@K>oDEPdbhkwlIVBfvJ{qs{g)^U{_>cdtT;bmo(amjXd!S~|<jwrnIv)kk0>7ft6vD1#imrqMF_VYo1um|>FSZ81ts8QYoDcE4mBEO)RM*|3H*E=>efy$^bb$RJR)c|W|Hl<U?spiE83I!8dHO&gy0$4A)BW+rOCdII76C}umx@23X;nI1BZd4X@hswG5%o$O~0pT}37>qIo^{7O9Ew)(a%$YB>S78EtweAWmU}hxJm``Hhg>~Q({0Dkxz??u!C#WY8F5@>P6^-6Fq!{Iqlqef&1#-0V1c=`>`Ti)<6HS_IGFF8fSm>gWv#9W5;>Idvz_EPSOkT?ZB?AFrc@ni7Ba*&B<2sEUgYr#B_O4J18RZk1uIR~G7o=4zu(x+}jyPEzx+tBor06*$T7z;u#0W2}4#l1cngBp(8d19^(z(40?Vr)$zyu;1VV#`SQw+Li{6EvHdIb-F^vSx-yh-FOcaN^74d*lm;PFg-ZSkFX$){K$!3JvW{Ba1+9QP!#3YM2NlOw&k<};2FrsGgZ#Q<*;zl5Z5fg?*TvAjersM?T_Mgl6y=j*f9`@poRijFi6H7hfmN>e-hCuK1L!7ABlp1Gno(|}@^4qs!J7&Ibn(b=GF09&#=>*sIo?jCLs0k(Q2F*+4_B%)v_3FPD%&dNzKI&}KJEG8;X8mj;Vvb-o)y^eGe_ZOUf;F0vnQWY3&md`U5ps<7~%cw^tz&L0UMok)Ew`dTR_y<8`L|ED=4uu%Alf7%s7)=MQGz^vm2N4PV=s0i*-gTM=P6av^5O%^8?!Ub|xls{^QTLbbJJpC%@@Z0<!g1lSEFh`ynSk514zP>Kexy|ttSJuyEfnKT?PaMZ3Cxdg2%t;|4l5J)ylKO$>~7>@P?AkvewAOu+;c`Z%^}wiqS6O@EdUid2b2hoyj6ur5YLpOw(ABkU(D*bL2bG6!6co<XZ*YF0&jp5{%!}J%Xsd;dNT6oB)b4g$cpW9g`JrZ#`3=;oXrD;peXd!`%tp;ti;fuk5neNA|YHE8yFgbu<#aWiO4tWO^ArTeW_sbHSna^<>JgL?bh}i_&k!>g?q%{yc_j2_Mq38C<IWziNyq~y@fl<$TLxlVNwqM%JsdZD-u$S?;J8WnWk+^x3YVUUxERs7y6M~#1|OzG(muD&gUAd#FyJIV|~Spyu>*M3=pPuh?f#~?3DUNM3x~CfB-<2Q2Bk}OGx3WYhZ&yKJ7Em%)Fp|z2m{cks@B&H%gfozEv<wLprl$qxX|C@qh`^6kP@lqwN|hfNZmKzI@T6kq5`s$}t>N7o8g;fKN3yOIXkrXui%+Nu=)M1V(C^vgbiel#~%q3h;~S<8Tf@6Ugd%hJ`jRD@=AyDniAQ0utxOrYQv{U=7pU^{E7lbC!$M@`f9f(L)Ptibw$?Dn;2skAz|aoDH|R$zpw?q>;fwYOiq+Y^0PHPBOv?ONwTe))aY~x|VlcGP1BHjYUKgx&5S<EPgQ*TH<O7G-RxK(z(AUG-uwL!+CHUgz2MeXrbdIF06$=drfNL!d!_7_CeV6#sNIwXnFEUzfnI^_-eo4*(Vwyu60KL+yJE5KD&{mWg8N4If+qFCaU7I0F+{F0=y!4*&iy(0w87iI}EhBvGD3oO5k8bi6accP*$L-J=X82WY^WQOBLHj23Q1;(~$Hk5eP5ImKE|x6r>$hBYrvx{N+E#sA6`xPVKx73t~iCyeyk>CXxqI$VAHE)@Uq5+ExctRml?ZDF0?U4M{~WKO$o6@RI@o&LSP2zDUYh@r_9$*UZT!v}Xa=@L_yZgUM4wGSKM|Ra}T5r|B=Wlml_-&H-SAf^HfP%N3y(D-k{)xTTeiz#f9RtfguFf2}y(a2jYvl0}&LkEQh^j1cMafmNM~L^NTqds3Oea`pvSLCQ?Z!JP(^=Oj`*`2hX+Q6AMT_B$>$KtXhSgh6S8V<e;lL<j{Ej|rH8*CB9(7QZsU)#ysdu_V5$j(|EU!K<JH5yA?xd9IT@13m*Ci&6MxdlufaC6<bfe@5t)$J6qKnALE=9`C-pe!Nqb`Ct=uz`+a!WWyCO0NcqH(jdN6s9SgepGFp%CB>VOte0G^?0t+23D+R4r>YE_T?7jgc?z0Xb~4^51i306oS2M0Vk!RpO6o6hd|%>kMbLm9Ogu%Kl>*#H+TuF~QXO(y&*=pp`~W|C$Kcp6vQ{*0u?ki3KLocTwrv7EV{-COA{E3T_61*Kqu$8~%?2ECFE&&mrOhb_3mgirj`l~zN$(=slfs9s&w$?gY*g-_O2yK^2czZyC<Me{)-f`{2pnE7jEDR(YztxX@(l$FCkQZL-!HRsnP8d5#C|QnM<H;soiqZo;^yiFk1SN1B1a{Qe4-?@D+k1oS&WCm2bF;Iv^=?0C{l<f8NP%{gYmpOK{_W^qhA?@PyS`;{NRI#nfM}=K)HJ~Y4DT{clz;g{4FE@pjml^x0&Fkxr8~rxD_R-S6`uoj+6`5=a%}LhgZf+KwB#Z6oD~y4xeyLg=Z?#1v*N(KUo&G#*mHGUim#>U^uI*YGU-6#Iy(W)8_kySP#s7Japyk0tkdOUQ$of_9dJH<WJiRErIQvs@<coGyxI=+EdQ6N?P@TB8#Eqv}=g6QsLmt259LLRCoEJ@PG)A#Tl6>v9sDN7?;7Xiz88rQBI96$qbB#%-U|b)C9iRpc89iuH!so=F`cjCs1=#5kOoZbY@9Y_M2d7tj}k^MU_w9^5KRWdAhtMek<?H_JGhxG^xmP${rtsDSV&|Vj$#2aH%+*N9rN6>4qT$h1`SW(1pZm904lfO(LQlGP?~f!OwkE#G`;j7d;a2Ub4K*u5Z@e3^qeMjRn~?ne(Uecw><Y)t>-2T|#v%ML?m@x?qf_usoL2e|eCm<IQiTe?n8XOQV&8m-LCN&CuKg^9eT`0#rMMm$l=k(^>oVYA*Ds;fxSbK%Gb2%bF83B%{|<FcIE}CT(b(stcIeNU6mYaETmEqwog=+$wmkbnDD1*A1-4aOd$Q9P`Ct(1!xPIb*W4TV65OSzMNjgbZvTYliT$1O=7tgE|IJx3Y!ZG%d;2^M*C73cx8`vLYd7oD8-NXyih0pUy>9AksEyLWf;KGfqcCFc5KPfh$aoNFjsevxE{(eDOr|4?>F<&`ny$Q&u<#J$D_tUs<K*AweE^c+?F#qx(qOw-@40LJ<ja)~Qgn@f=`yGP%ZaQ;CsbBU2`i$!gD?XZGu$RM6z$OnJ2{7D$q~0lL2F(-`jW%$zciXopF}(uL4Z=9045qLBa|TweqN#p8#9P^aH+M&Qt8qdO=Tw`qQ&0KL|++hMrG93^n+A&aEY6c(>2#@UD*MDz^6SW;v<`!2|DLQrDq9hU*&m>tOC%a+=j2T)nkM;zOcATZ|Un{T{=-VAq_gfJ@AdG%7oeo8QAzgEH)FpJb`qfu}~EXa0`YFIU#sh95r#SY4MQ1CwpA?wb<?|||eCew4AKxp*-tq3<k)98C_UI<W{2fe{uwSM$?DtI@|7yu?W>IFSQ0$BeEe8fmfotoT2k7RpwV@-%p=-Rf>HZvfFyNGbb^|X6X7|gp$kwA})L@WL|WC9$gS~$otdAs>imo7zfBc9{$M~)FM0<DlxtQ+&0<FC)cRyqyjFx!=0a>)}Kvurb}uEd0!a%jdj8MG0pR!L$!4UAVm>a*cpA0m$iV}YY$(9Bh#InFQ4<tCs+;zHB(YqCScx7wZClMP1mO<^KPs<#r_X2q722gn(YWY!X2i(~W8Q;F>xn~RjQCC^E$uj)QTQe4ELNn!&CnzDzTqVX!uJb@+GyW=|uL}6s-%3*v|F62l{VtVvrpPNPqC)jF+LnCFvqS7$j4%rf{P*j~Au`=U`M_lR&z<IVk0p{_bK(`8sqBeXD_M_MYm;=Fcs;$Xcs5cu+l{_qvVI6CkE=-Do2(d1J^C1X&1s5X?)Ds7{(OlQ1*ht&Ta<qOs#cpqp3i(Etdx}0Rn|mR!iX|#Hyb4rB_05(atoaVkRQs0R%;eV6uz5>b2_KK&blSe0QI@^jAav1#1aEJ04a}Sk!=>krb;;~72a+g-ry(2t5_jk!9f?<mZhcI)cBzV^wE^;qjs#t81^X1Xrh@}mN?PMoB3b$96<M+u3WN2SXp+y>m68$Nk>i^k;N7l2p)dwsVRmk53)#NddNKk_jjR)gkLD~&dyv&oiIlR~fbNO4O8G+eEQ;w>e<`LoQZ*U0tCXeH7a@con)!6<D_JM5WTCZY!O?iWPykGc60++LVn6V4PkOCMrRAKOG3`4Sg&CYedbny!xtv3M`WQpT2gaNVmnV<~P-%)cYbyFHn-JY8rfZ%7qG9YKR1z=1uJ(#q5lFJve9o3JZ-UacnK&_Cvb5k(@sefbw)cnu<u#xyqITMmWiY$PB)x3wfGcS*0~776e2VmCAzAeeQKEunHh0==MqY6YC2PSVRuOBJT3<|0*E*)(FvRW7sbU`+J>fgP2Qm?T7M@$JWLalev4s1Ob}|+1)NTZ%&$aDO1N;~TK6(G2F)}8A5Gf!W0TXy84!Z=)lH9^F)0Jeu#wemQ=<_I5!vGczz+8V1Oo@^Y1cLHoXs3z25ffMVp)%pDliZ1=OoNlKKQp$P;XZ&L{Kz2*AC*ERZ49cRYEF^IHmOdZN9)1rZz6Nm6xl5-0*?vC!9C31R>8U9=@&p>oD~4n->?;f)?k$sO^z2OJ%Ax3w6kj4XwH4;L4HoR5@8y^p$mahjm?nL$beN<EU>(K3;Ye?z=lYSTqj<jTSmb_i6-_NP$P`ul~y*bh%vN;iz9i0qb5?syv{{}H$lH_0%=m#%##=SO4n3xK^Ov{qsb>8SUou#{sirC4Mb^yQUvEyEh2);W*;3IZ_{!G)LKj+ID23rITf$Qs^}4KL~l$$Wffbe$v4Eoh;$o7XZPtVdaG10w-rIFkS^G==bm>Fo`L2aQiFM6qud1*MK#$@a!ZjR7QEqi@4vBx+z6>b(ma|{e){aDJancEkx3#_f}=(}K=&!;p-WnKP!ngm;5OkdJ%~eI{U{@ZPhY}X;u+_yq40~@?bG3>4V;R&%vnf~yT7YXEJ!B=u)QE7&1?r@ZT6=+LWbBu0oy2;G&fa#6lkEQ(?#Ayc)%y0TuPww;Az8GHyl5BljBNV<i#n@WY&_D;v!qSGX@8v-7;>J74g!1Dp+iv2BRq+$Y#Q0UBt~3{%Wp^K_5M$uya`<Fv%Dl8JhB0AwVIg$f(+$6Xg1$aSB9)7~7_>&!P>S#xKO>metIF`kI2nBNQ@bz_M$Yq@4xJ8dH087l2czK|yxQu1T%g1)VwAO<r~&*Ic156LQV+XKRL%Bjc}1wz*0~pv1OOagw!=2HD1DeicYKm-xsqx>O<ja?M`3OnpD54#sgmHyg)qAq~6^hli86MW2CzBMfJsc#~h~!>Be!a+hC3$hbD$vKgz)ElN>lD|wl48||sz_XN%Y#D_c*3OtWW;-#h$f_(Ji3Oyu2P@PS24>S{%4tNQ>N^i8BOH#%t?9xNc`eEryUEn9nZ)W$keVS?Bi{ciDxs!&ZrrR~7%{KJA6~YLx#5DDTe@vIEhAJho5WDhEfE>B$*jywR{Rtm?5sWSd?siZB(mi5$$9k<8&ywtn6+#~aX77+npwtGS{r%zUY!8$g?L^+q>wtWwa9VlkN>3jqUKphW@<K$c_h&$0k2Nl&VUKG`xOz-s&f8R>2Z64yr0;+y))_FQ?rW#_kO|D_jnUql8b%=Wm5x7^ZpR?_{`-K9OoZc*Ia;6_X8?{^zZ?TOYBPcemQ>{c5eDMHh#*YJXk58}C_qEH;qEjY=v$~b;%rq~Eox76E=m<oo8X@!yN9Khc<#Lp`T%f2ErnC+Q!4w}xz37+IqZ@>yP=G_4L$r`u~k#JF-wUWxoDIpx1x_TM9BvDTACz1aQAHwCXX%OSZUC81yN#^#1qEL8lXj&7$<;ZZ}RCG6xoBp&>72MQA~w`!rB|$d<5tZ;6k+^AYh1v*_g&swUk!RA)QJE2_GC|Pq1QdM_q!ojp~H3rB>f%4t<XD)L<p_c1euD;vgFQ$r3geU>i%r&S6m0!;jD?DQ-XwrGbVhn+Oc0BOl4<^fsAE4tN^aC$tiZ@RM}Q$ZCN_h`7Vn%O==nNvV=K;wJ9_<YaQhZf>lQzk#M<hgu;zq)-(ulxb?2LYGuAQo?l<{Z(<W&jZTwcF7Q;Ul}#M1cC@vYmuL|1p`WwG@rN9i*bf7(U(_PQ?)olgSptL!i!=#`51rS)S=5A_8IPN4D}k+A)5G$(6)pxP$vdAkF5zeHEz&pR=eN;Mvq{FWzINAcI#JFblE<41=dLEei3A5eSX+3No6H7o|nhyM$U=h41WLE!ql4}7e%<DT@FHfE+{YoWwLmQpLN@4Y<ObSCU*lJnH&x6YGD43IDhLmm|gchBI{P4JUisX&sHFwVY*48l@eOLdXq>D<Cy?tFLO>^9pIx{NNR;b`_yC)oyHfnHX?B#IzeHSoq$g?slCsMM@~t8;`4}!QJvz4Zh%d28r8+p!~@(<j4e^T0WLW>g*LW8BthH`0h{2)bP%<J2S`y}%!@1&BVulELIvuIAv{*>HkgVJY36MmpVDgIW41@i1qMrEnk3wpf@YZj$;=noI18e+5j8I88tA8a5)k09l+N*}##TvyCY82x{=y)JRpxrip<h2d7>6PaefH#09T#E5&yMxYpSz#61({vWHlW6x>axFIiy~!oo)BJV%2~RsffuW@u~SuAnOG$;s8*9=tWFC2uzd(tY9~JryNVXnEj2z~Uuy#lb54x#0!1jJJp65<07}hBz*;BBn+=qEREAy1D!eb0nYQc~H`-uoJO`rhq4waD6qyJ6@N<y_y*#xd4hl9X=py9_rL3Wm0De2wxXfTZkPq1IDCNza6JwL+humGI=_LI-5OxjuM86Zq3M*B&ts-8Y6-K*2L!*4`C}CJT7zy#MoqicBf}Y=KInPoUnCX^<N)&rIfeMspHrffB406l{%^-3RcRRd?tn{K#Ra(MnFbuoiuoJb*a7GP^T9fre+h~guR;+bxqnJRxaD67QM`BOVr;_Z0gX#H@R!b=+?}tzcTLF(`N(Gq*p8vIud|E<S<Yld*m~J1$A~OrwR%b~}M%IFuosX0?HW~Xopi%%-&cn$vGY<bR8#d)7cL|y_u1>f}@EqNksFTE+4E!$oEMb<$c05Qp`WyN!Wt2FpT-$_=P?@S<$z(TVqJ1uzG!-EVcGdUE(+c8~*@(m$uf>*UJPClAhy9%xuFyPq37`YAPQMZ`gedSOAl*Ksr@FYy=sgoJR=#rjD+UDj?tSLBZAGC$_=;jd+MTcaS3jq;fy4{04;iT@PBlswuRrNZtzRZ-nqx#&1n(f!%SM2dZ)^c%YYkei8RXrGusXOVm=i5-0ZZ+LnT?B+wnDhu&K^27tiL{@Dw%}28l;t;9b$td(Mnv@$cqs<xP>s<ws7(b6*T3g*wd@FGpyqlJ0;lBr(2@I8j5&@4mP4flmbUAUBhYawX*=kfz>q&mKhWY3lc{GyhU#Aa|7u`8Iq8W^h6GGjkKr}`=`kdq_EV&eR5$upE<9G%gJJ|N`VU4O|!}jen}~euLWE&<Pg=4<m0OJr?#%BFtMxT;!{>t2O`NrMU{`k?Z{%XaDozuC7hwK9r`9Xfj~fRa?%VUvBEntU-pPQNKp*$Y?OUgeq$HQVnj39=^X3>^O-E*qC&wb5~hGNQj-tCb{5Vdp>vnOM$+tErHS1PtciaaR1T%DP@r~lHjr`D0fQUM?&6a`?PVxgyK#m5T+1*gwFW>MxQu&^<Wlf)Z>m!kB+vgBsc~LnU-HaX%|7s10K0*7MxJP)Hi4GHXgvc4=TK4V9MM9+&;9*XR%s|Z=)s$WKtYrERFVv9t`EY&!^Eg`l@!V$p}tU@G&TGx9O;)Lp2ia)CVIy}s`{*hUx5f%)gSMf>%ljU5rCT0bWE^4NVsL}Zk8t9jKOpK6V#aGc0NnhCxob~2qbQr*DE7Zt`*jsQF@9Dsnb_ugdZ0p@^~U<MDDZ$A-L=Y!BowD)Tk8&Y66;`@0k00rbQXYf=|zE%w8i*y>{EGGJ$G|QTJhG2)uAhuc{u+DyM(}2uH$D@=i6eJ+qoDAs<l}@d`kGtpYTXuTp2H>blHk?3J3k%{SPA$^uQAlSK?(p4$SMzC5b1dQ~3uk^s|_v7qg8yYBT%N*|HKL0TRs!_EDgJ&s1J)XoPxJ+eiEW|)My%~DX%GplmbffMjssfUWn+qa90hPnuo1=7(XMCle2bx2r^1ivcW^R=rL4;2rlTUaDYSJWg0c;WN0Hlap*qgW}emnSgC?7-E$w>H&$g61iMe}+&?Q}5n@2Hg7^1t)XC1T2-~Nz%rH$OPKV0*+Xrsfpl7oj}sO(~=5Aj~3K7zdEbdTMpWeJsd^JVQhSg8T^XSltC_(Ap-CwN?7LGQ{!`OtMa2Ap^{;_^tdXlJWZ)fhdO(m-m5d8wqBw4EYB36+em#vqb@Xl0&2CyaQdo$*L{fP1VaEQ7U@ZLKqOhU79orzqd_T5g$leTUME~x%oK@qn$hEu^+Dxp@;FUkhQQ(-t#0d5h=^^iy(1X}FfMQ_4yV4g`b!B}@#1EQL(p3b6gkKOUWO`x*6sFItl^`OAb)hOp8nuSNbp)ktC>j<%FL!iY?4BQSTg2eiq`~XvbPl+>O{McJ{pmojB%M|<98!+P)8fQz5wunEHXpGj(YQKpe)#(XkAR0;`k2*{@}qT^%gkb($PGxpCq&`T1~0X)^1!Vl$t;p<z+6w(7JcciH$oRoUhCYnzTC#b8xN>W5%4_7@3zWn9ZqC_}XAVIVHkC=knNk3lo-E2FhL!%7=@BLHMF!duUpXxJ4PFHtxJ$HiKbS!G|c8f^{Zq0~3ctK}QoD8i9jaOLvg3rTx!*ua;pK&knd&2xX@1^QxQ!AHs&7p4)=~?O-*V{If1gsa-I#SUW&bqQvaPnW%TsrqI_kub0tMmBJf1p)&P24X=d{qlQu-u6d)pr%<pTFn?77wLr0!8TpNG)=oYM<5YAnig?b5XQ;w9WTwqtIZbzfyH+yImH75T;~T~_NDtr(2j2=<Ce3VQSEC>&yjO$~p}Z{kE(8wh@FRRo(ADMX2nSs^!qM4*0h(9j6+;(^15EE&W84_OYt>SsL1Xh~>nsw`FmD$TA!po|5$|>wyGYQcra>NJ-gV{a*F7mc;4&v9RJ>X?V%D@rh@+>{=?q@Y=KC7KR50;DDW6nWYo<bL7g7i#D<%c&Mn&QY?*Rl;8HfM`M)a1elfRrAe@`X=#_9ERON6A^cE?TZf?n?;7c+<IWLz*d<k>@UQhLQ5lP|>(nGihDZO5zZezK7oDZa7es&NGzQq#I<QvXFpzhZb8X=`){PH3TAEo8||Y*m!xDMgjHO@gyOPIjEd3oR(lKD_{M7YY$v!^7{JT2#o?=3Tl-$c*|K%gM1$EAGu$j8ivTmm18x+XZl?+_?HzRLxiIOt<*V-U{f1G~0BDVr$)iiuoUOwTp6Jzc(SIrZgc+2h`gjA6nQE+vp^uGjae+t@w(SZ;Ar94>Gv$5NmovIOdeju%9~=h7C?!=B2RQ6a^=vqO0XlwSSQ_cq+&-=Z_RgM_jU%qs$QZbVtalMjzK=q_O66wT2M_esGHdj6O1}jgGk1qQr=`svjdtRpJ>?9tq`ad*QM63I14(GS6&TQyS8=Lvvua1G%PB#<w5x!EO(?3E2#UXwe_T=`!-39HWGSz-as7Q#~&~d^N^gjs>&1<_z~vw}l?OWYm?unAnzLo6ITO)r?No4ccgJBMK(boamZQ#ZMd@7>O-;9n`8xV`6q*;0bsz&?nK+fG>cAeZsl*=q|^}{V@^7v-N@oN3qEer(74dZWNb*2eUJ)BR&(JlwTrMBEtY*&(o->{b!&Hb?zK1<&foy+E8K?(pO+{zwbE5k*Qm_6jwqAbI~&``6@@Mob+A<IAqfG440wXlbI5hvvo8}1kyZHNf_{pMVP0Svr6f;_fapIojyEQxe??0h&(z-bE$-#T3Ij}<OP8EN2S840j$9zu<4_Kk+D1M0lZa7<XaTKf*c$%AMFxkH~bh-E|mfmfg;%mdNJjWHo_)7c-qDn9j%C&!~yFBa^5b|3G-s84OVvfis!YK(MLp^OrsQGd&mHQ@))x?-4V)p4ukzNS@YmDvPsZ&jUT|y%=l4b(eXSCn8t%uqug8NPaOc%J_iiCS(58uOV}<&h15lDF5N8wuHA`of1C!bL?gmh0T0H*(C7-lmYl3_W&(07U<GLm%KoSS1J(D<wE')))
# The generic dead-stock heuristic considers future SALES only. It does not
# preserve wheat/fertilizer required by PICKUP/FEED/FERTILIZE, so it must be
# disabled for a new production route whose input contracts are not modeled.
_DEMO_IMPL = make_agent({0: _DEMO_TAPE}, dead_stock=False)
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
