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

# Extracted from the frozen One More Wheat source on 2026-09-22.
# Upstream Apache-2.0 notices are retained above. Generic library only.

# Modified 2026-09-22: executed public episode 111903848 production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode('c%1EBU5{KxZv8Lw+z+xw@~-nXmS$~XWsjkc7#l+{3}k}<!REoqTaf>r@l5yady9wX9I|dpj%~nzTRq)<t5_@+d3ebB;eW3F?Wdpr@%Nvv{^^IS?{40{z4~yt`uCsy^I!k#{*C*W|M=<W|M>fV-@pFh>dW_k`|-OscQ4<+cz1QU`u^+NoBRJi|8RKx%gwj1zPWjQ|A!ZM-(MX*`|#m^51XHU_2RGZzdQdqd&t|{*RRjN{@E|T{`IRjw^!l?8o~JX+plkL??-Sw4(-eLuU^0W@qX^_-aq`>GP2dEkKcXxQU2!n;qh~Ps-whS-@Ld*0{h|W+q*aKzJ8cDdiDM7+jm#uS%+jf^L0CZ;CeHV$44DjFV4dl#JbaX{&IW!a=S+3^1;EJglR5?J)GmC)+#eTDT?B-?6e=QUfe|C{PO6xzs&P+_08?;yKk=!PiF-5_y{C~Ls-G}K;%^4-o4+b9GofAMl?Y=jZqUn!z+B=f5*R(DIFyPch>#yefw@1;P9-6)gwPV8q#Gx_wu-Tcl(Avp)9PpG|(<APgc)4O86J816FA>Xk-lH#KNB*pWyAn?Vz5A$seb+-Gk!*h}4gNQ__g0F)VVBa7XISbAs9R1Z+GE8npE<#%I8HkWe#SI(-XD626Ky#n6gHMrXSfw>y&C_}iy%G2Q=UvWd3Ik<D2o=U2BkTX_+Cclwg}#qqb9X}){?`u4@UAOCXu=H08;ul{8_;H_F44&wR0;W;ng+<m7_XLwaQCl}>dPU7?Lp?N~9xcUHbP{Pr`<rv+@&EWLHA9ZByZJ-Axmg?ca-cF1is_+X~=N3tyou9#dc<P8*F75d_c-o_jwCmCa?*;7L^I|@FAZ6boo<7Msz=y_t9xYvbKv=3&UBFX)5pQR1tTxypT)q=eXNOF_X{|E__->1PYB<2m_QjKBJViE#RmZ>pEn`yfWf1Hh6oT~qfegmTK^)lna6Ly8(WhwyC+LJ;M%wtj<-1U%6Tg=awDf!Yh~H;`i<(MTrzk(YXLk0T61Yu65zM!O(L9(pgSF&&$P6a%#ry-LpkZ;Vg2BkS#V0J|2fqvEmccOE%>bvdcK6umLew$~I<bePL3ayDOD3ya-XU-`LqO%a16xCY0mngzhb{8Do^Bt>BXuv-6@Gn0`GQB4ZmPn*UQpJfYxefto15>yynXZLZ<cpRPkHp}BaQ1Ead8Co{OaqQH~)P4((*cu9O!W3CgLF3;C2wp<vg7^(TiaQK2PvfYwj7C4tR)^vOELUzW~n8vn-EZ>`GSI+tpAlESIwjrXK>NIeNl-J_C#IJgpfQ4=DWbyOz&adcxqFHfNA1RsJ*v3sg2$4p9~zWtQBOsfmW?+yNL?m=<<3D%fOnkt0yH(R=T(Eje)Dq(*?emCvSLIh(9P>v{o*jkQLHE&8zXaW?j9tYgnRkB9q8d4|39jEgn*G@PZjMF9?d;HFzJl8r^vNz;g6!s$yLcVt<RX>A9?U@WJT0HBO(7bYm-zMgT^RwRpMYbNL0`ID2Lu_GrMWl8sKmzW`(;^?TYWHdMO6z4m2&FA1~iYZo%V6;8J1qP<Sa&9w#i8;k{sk|sF=j<*y15wYYq&j|M=Ir80Nbnbglyu0M8(y0P&FuA1@n4(o3kHNInS;pJ_|1|-3{X^lly}q~{SHW87Zl$DztKc|e>0w+;5^U0sRK%p7CmT%v@!=vF)b>{Glj7F3<q#t<!K6c6+N#Fm^FSvcD!aZKe3_&+U{&Tw1y6pU7J+ue6PLTII}{idHx|za3d~F;<in@*~-rYMuT(3_S7q60f9%49VTA}#FwH>yU`0OxoZ_(4g%aoI8ktW>10QobB}0$(J8821?d78jOF;VaA^ub$U~l<TS<7tISqn8p_?8j+Z?M;8K2&ca^7FnEVXBu+O-srEEX3Y9G2!6cx67$uEMs{cUOViZSfg=t|pDwe190=%O*m<c{L!vB?ml)wETdZ<qkRi7<yG&r`|a>BD*Cy=2XJ<TYPzUL9L_i1Mjrr8j-UynGQoov^QKKb8t6RWi7gSiR@>q20QVTC&`C<`bj>4h@LH#Q>(E0ZV){~XXVhx;CAof*oY`Sqq#Jv$19q4d4z+W&JboT=w>=J(Od*zX)7QwLrkC698cdT<sblN*t!%jmr6NK)!=b3f5B1*=_p0wF-|iw{Br#b2VMLA?(Y77pDXt4pM*E1C<+L++701cep2}e$le@<&UsNmT!%+c<$i;|4Ei09@#Ptzrac_z=^xO!v$C2Jv(2WEw4Z=*(IMd=hu#!1#sG~bGTH}eNpXIQgG0mT<q;VsK$I-!isYtBEME9ZgzrS35~sfe82DvGtd$`&Jt%Q~*s%z$z1H(ok%cc>l;mQd@_Or(tywM96B<Jk!e9<jpUwzCP7+@}w%39%Zp4}cGw2ud3~61TCCg|nqO_R(*zAKrFM!`lt(z^{@$Gka-`u>rQ%8UegD}luTZ9vZ<T+iKeyIR5Yt!OsRAQJak_P*grQ!k~3}_TBLH-b%4v>~5D?8?x4$yBWEPFcOG`E$lEM;XAqY>YsIak^_syEEIREyDd7C6F3`n0wdS#UG_Ev(X&nXJHWNEc!hL~3Bc;nm@vrBYWWA_sd4DUi=qcpsdFOT_qA8e`=nlqwWW#6B4sgVEvcss?Ivi3K}7W8(YUok?(tHdf5&D$`>Jj2hBUNiMZc(ilLy#5nY<BvdDQyv<JnnQ#jNfef1f2|TMtQs=RwOfaR776ji`a>g4`u#>TJ^=ZW;Q^PWG63if^D{_stA@DmInF*PQiH=Zwe5^xAnQewAqQ%Nw^UAI@Af{{V))}xLg}VsxD+)9I$*GO@ZAlWo>2+|32JwVvxs@Cdsp4IO(;3@q#3~v<67UOOLCwP1oMg?##&eD^PiA8>=7r(Slez7{4riaP@;S0aLs|~}69AAkrDd&VS{7nBT+8TZgIHEH05pq*mIBpq<5@>^XhAu<w?OA+$wXQp!$-wVTOHHKQ<Dw=EI~m6?11#1KPdo^a{hF&@kw{TdG-3Q+jt#nBy1}vLuWfiKF)j@jBJ+`j$Poe^Q3|*t-e%f4b;%C<Jj~pf&TCgp|x>JPUX6%f@vF=U<VR7688v}>x{8f$Cg~Z%ZVc7iq)p-W#nSlpBR+MggQ^pwP|_|&4KveOcy&SneuRy<HJjiXsW~l5M+&DE;DvSZumZh@-N_&C<y`gmt^hE9^JV6YNM(Huu+on9lNZ|X>^al1-gy95F*;a^STKb-9i_z0#e23)bIH)1sEAiGUhuwvFL^#0RE<gd?IiBY|d$qk>Yj-XA3BRf#g9JqQSyYAN@OY?{)}bEx4^9wTkfLj78hdNV3)QyfQA-X6~EOuW6lUid5D#&y<U4P4p0o0XP)_DgLO9fFu6EV|G%<m35H&^Wl!PT>{{P<^P(zaKN-%2b3bp1iHuhR6Ldk3%iLF32lhxXHz<S(kld?{)waV$N+wZ4^klK=)Pp+_RVBQe-SF&G8RIp=2f0c)N$SoXE!T`oA8Xw!V@)Qs1psCLDA=_DfFGnlpI?I>or89BklZ@J78#bE3H}vCbDFZgBZi?^Wzsii_U}U+6QRU%Q&1}u^7&;?(W{+`ks@DIoAo3!A{YTDY{l9zF(%i3_j{#Izjyh8%qI(O;S3dK1j4peNtqcjW#C!F6AkVG(A<(@igvwareu1DVrL0I}ma5<+4<)5We*A;p-h8z5wl7ZEPC)GVeQX)&q7>S)w8l(nJWDht_B_lgurq#y))dxDca{ph49hS|EzOIc*k|UPPnJBKJDlv4`4{%?)E88?!~f1GaI^G-Wfc)(8<q6eu4!aM#1eUjh`?;D8a^HAA2`3zrT!GFsai6y5hu(TUXrb2S5Way%iV1pxr%Yf$0kkm#(t7AhH#w3Tud@=EEgp~-nuSiMpSfHw}B{NdyS=SJW`{#_W64}_y+@le1Cqb|J2Xt9yKwbCh`l%y8Uv8P~J3M1!owiClGq`pH{`Ql+=cSPzO*2jj$a*abR3CxkUU)f)6W{Y#JE-;>y&B8kN84M8j6=4%x=W7(YI3Oe{T$~XJUDn-ig4ffi&8Q{rfp=%#-j=0XN`Mk&HA;3CHo_d5G)NI{iA5PPT#o~E8{K?`!M<8QBXkQN3@QGCcW{VtQ%yewNXt-6mfG{RWd}4xA<;JC1$a`Rl}gwq*s>ij6MpjKiIo%rIR;|Ruzli?2h_FsHiU7wKCDJ^E&#0?I`Vy#@SYTX%De{99bn;sKT8Ez)iy8#HSjZrj*@a4Bq_No2`~4fK;#4tmK^{DaJGj?Aw}WDaKriCLigoIlVeY5BSqCtF9s|oQX-moAPr{=<i+U3<sf!)f=l0xsuS3w64@kMBj+)HBAbS$rF<e6#loIK85Jt-3x=FCw+d)oRJNnB`g{}<BLVJW;OMErkRq^iV57<mT`#W>X*LET8JdmZ%_QcwI1<NNwR%}l8f&zeRXi&|*i!}h8DtxRBREQrvSlmI$>fVdy1b0xJRkN6g?P%)M~1DMGmQ~ZbbmZZhZPB9ysC7?6Nx|BJ$ob|Vxh!*XwyV*po8oOMG>khb`#}zdl;GD*~F^{Zop*9v=$;tU=)qicZ`io$XQ&nWoSzf$Ph^2b&P;Z!M?7GDtBO1#XXwFhffogKr{7F8Hbb7<|?9uCqho-*FBPRi&&2KoK2`y-n_!WT!&UVe`JG*=x*>w&qMQQQe9vCutS&?-A%AHfVGc?IVW4Hi-gOLI|L{F{WCxb`8C*iE;O1MS`*;bv(cN-&;cT@@Ln4T0T7Xk-R)({6jCeQHl8WBB)}zG+9b+ojGzz{Fr_JV!U7?Sv_p7nCeL^(-J;v{Qzr>%vQ>}*!UId?_*}Qo8W*s>4i-iNykAD90l$!mXg~eI=~MCCLy}+xnS2_QdU`?|+r%6oqhHYgVm&3O>=h+wFk49dkJsb8MA2crx;R>A<o~gXw#w)}C6-gWUZn`@?D9KMWT)N#M9g{C(-akZ(f>H>5I)@@HjF$^@O37MKaV4i*TY0Y2Y`lxowJIZbbL9KDis4|`k?%6#atourWF3FOpBzr8En*SP7;^Qzss-SgiY~+fCmS%d3C#rG}q#+DVNN=jC}$MwaYpwMi`DMnq+K>)}{k(ovVU=tYg*nPiQe$qHD%xKx2XYo*rSh$gOCQ>DN^J)6XQza0%`~o%ZJAa7OXSqBQBWs>qUoaqA4{5N)u)S*E?+xrkU}5aP<LtH4MHQOvEMrDL?f4m32?F=r@1;+j{04$O%`gNDH)tFe|v;K*qZm&MUi1{qBKp^z9Xwbi$9XXQgJ3-gk%ayYsNRs|LSk&*4I8HFac0%s6+G4R?fBjQ7@^v7Wt2!KUnqhsQfIT?kpA3`@YmH_Jz`=e70Y)3_;UU8V2DEAD69#ol^^Knoc&|(FFDXb0cbNkI_$&!+I_)!NRer*#W(=N$A7hr({81oI~`^6oitZR~2r(|dRSyQG%A(p3<2gZSIr}n|ngwL;RUY)NXx5Fx(mg5Yp^)UE>f;6M<HhDPo5&@VIm5T-=q^=s1o><Ux!~Sch$Zkeq!Q!%Wmw2TE$ABTU57uz<u8XM5J_v_*Vf;lWFT{9}CH)4Qi?+LHLZe!pW;8xiI}8P6(KAc=?t#(RyMq$onYTAWV_g`GXnDB@!>C{-(Ay7-s1GXoDpcw?d%Sz4stO4~o0GS|-I~6oHQjDuwwY(PE{ws3QBch%ui=4-_+S#uFvjlczDxa&Q}x5*alpV~ynwd!DSw3mgB1icH<slQ1Iz;$AQ}n-`GHTxlcsB8pzY0973ee54^ox82EHAr1K2IW`|!5j_%S%x+poUbmZL0r{zC38a~nvzZ40%L3edU@>0-#owvo*C;sgeFINhFE*^c(_Kl^;O!l7-UJ3ZRGINSv#_-HW3LX<svi7GEdQn;grsvdR*Z{Q*QFQ*4%ij<J)geEzxw~O5t7OW#&s_0qsY8p9sx8X#DNc<bEz~q2CKHvqFS)ka)4TnLIOu7qVONO5Am4GW1Uzo?2<#q}3zv;tILthcr^>ego&^i(7gZxsANC|MnV5S&!5Y7JrxeVSaSbN0K?LuY<Ogn3W-iS%6`$W-CD5)OueIQHI(6;h^h+_ntBhEtIu~IkgFtE^goBGW`E4-RLurS8HRGMYN1vQ&QIaQjZXw$_c;V37&7FYz3yN5R&{UfsT8d@Z<3#*YW5TNqp5Vhu|zBnwsosBR<mGBDhBuUA!WL^n^_7S+U8`DMY-b{5h`>n?#2_h!`np4OGtdEsCG*Fg<4)q{%=+RtEDrA^2>Bf?SF(IaaWILK{NEV;sMx?_`frGNf1WfO714lfTmwcMOFd?S$xfdC9m6(TkscxT%;<`v6fFUI|O-g_zv8UD4dB#h5x*cf@-&L(bis)PR(RTbv8Z$cyC2*4!LzTRJmexcq(XtdU_6hXmR=YOhk=>P9>bSQKH9cm#%wzlT$^#JPx5%Ojr&50h4N%QIc!!8ds8cJphN@yr(v%9eCH_ePAnb|RX&lX5nfU$PTMW$DX6e()9<O>9hxw`i5Va+^Aa!{o?XQ`rWlUwptnx@ACWKwJH`r&^?Pt^n1g$Jcret``e5_UfqL2GwE%pdEF+_&77wCKC7~M~snG~s9S$neR;q*(xx?w&<aQqHr)~nqtVq6ynnjrU@Lon4+_x(6Ge5`2HFezM#q1EBZvuP4yNg=~wc_hlRVTl|A)e#POyv`nyTQW266bGbsiJI`hf>_Vs0c#1JDdGeYEQJGCHpR*3=r}c)atTu!2yHxDdO<lc*Qp`&u@)rTI_iRyxiBkwwNjWf^f?3-MtRCp9eRl{w(Ov3$OBqOdBU-y8E|h(pa-V-h-qM-GJEY8%xKW2Pm7`L?OB#F=5LL&p_AlKNJm@Fj^q-1L@cWQoiZ1GUCIK2;0ojrP<aW0S?-iy=>idx=oO0y%WEkcVerRi9<R2aB9zFY9NMgrJ0F;Jk)J$t!|ZNa!M@n~GHLVmCSxRQ4A#;J7$U!!$%P11V3Wh68S+~yU;<}-C`N_+0O_ARKxnF9sKEkruZIQkSg8U?vF{iq%CHNi)bp<8L#VY2fc6>K!SDXa(tdl8m%J7Tq^gJ<CX8pZH@*wPdzFY&c$jp0Exrz?JrvbTu;mcPfO}=S+_VM_v%X;_{>ot-UMV<PNGF3EEOs4hfC=l9k#|$YKQG$n0BtZ+>0KHROU0y>`dF3W+yupnz%$`G1d^&m0Iq-$fy$O~qznmqm_QJ9nc8CkO&2S^0&KNi_&wL)q+EY&J-b!l+CW<r24`Mp9s>!|n}!Dy5qz29{m@IIVqoF6qlvj?zcju_{Au!5Sg()4=^KlbzyYitVwLEJJ;NA56;9GN&V(M`;MY~~4!`80M-}p$k2wtNUO3H2LJa!?fi;DHYGG>BVY8vLBh18G&ZAMS7CFyBae8@@m1@xbro)U@x6@)yM5bL;|1lmUJXuO3iFH!5r?IT}PZmZdBSk?)j+A%79(HjU<lh+Zjnq<y+A7%cg<hPp*rSozE!6vfbtHs2!G6M-^zQXkys(Oar))pzqCqDZ2V)ahKS+%`wLpw=GmF95tQDNlXr2Dd_u*8GeJL%Vt4QLAu?j4_5sV#4JWKz)rExOpvQ<Vw;E0%Ypg@yQbY5OfyT>p?N4bYl%IFLN-=v&cMXzx{5fh(Flo)73Dv%B)au_EW?on}RIHK_BS4Y5kir&1=)~U<DnTI<nU1_d2=c!G_L0kzzU*|PXihtl23Gmi5GWHVFEuhPkG9iRz3{GYH;9=INh*I$vv#7GDD+8Ci92*r(0t5g!ll<UihhU|-OgJpkJ9wohAsY<@?nk^nm=$#UQIo={Sl7H7G$j%-pt#daSJvPZ#YYD*fcy?TV=8@MoOU%vudG@gGg}jAQNcB0iIcfotmE4TiW8aTD2BdO?)i#)K8u{PSQC1;oJ6whA${0^eJxn*Jk3{VQ{i^{fy(pehw&9#;_;KhM<zvm99Wbda9*S80s!vitFKZmyI6^#;AyON8_>IsBi6ftUcoNX-4oLT8-}AObeuq^+<F*tM9ea|R2h%i^Tb1hMR8rV=#r)g1npWI-j+c{L&`QW<HBiTOIU>_(wvEu*%NR)rY&-*?m94+z_0PP18RHz{Ap^4*bY(VW!$H2v_6uKC0U0tR#?Ba22H}O0l@oM&!vklDYQrLgVaiM5hl%pP(IE5O}jSA3GR|7ksU8;qFGT{flFmTCs$1kyX_<GYneKpzii3vV^^T7fZHYl`*?QH*u=4LU(0qJPcmOIVC-;$lOkOk^+IOP&g2$!s+!~%8wG|~5dqUZ6~lKc+nJGPA}~N%&7j8!y2^99y)$c(P|@ddStM{EFQe#qFGIWGaRUnVt4)HrUC`uM5s{f>UtsI9_S1ThuBXnxAi{~Oj5b{pplhG4b*<LyT1ADx+xJ~nY0JDc^JaSITKHK80tn8RP>5ttN`xZqe6u2@=x=}k2whLO)l{-;(lBVcV+lhOVELlmmP)#KiB4l!4Z%x3s+{3EW4K14e|b;<9f?Mz&}fwcrOaE}Sx08*D%c8n7a_II08JZH3H$TA5fGgwTRDhI)P7XJx&8{jDv)hid=NkAw^2v+C?He_#!norE4-P>p0H5JhqG>B*f=rz5Qk}pqZdvF_wCsY4O)=shgAB<si~T)|H<A2$5CEi#T?P~rA1w|%cHbY2-l~+m^`5@@L3C|b{$kKgJ|B8EBG%LYviy?#gBB9SoBb$8o}d3cbBM!m(l>6Tq7g8<|p_Vn7CyjAc~z{=<-=VarIS^%SLI|aV1L`aYK<DREPL}w3=tIqYOB3uOBx{X|UTwTMLt$E!v9aN7_RV2TvG`slkde7(JZE4sIF0fx}_+NkxV6WY)RoN*R$la@Yp&8wDw!G$EPo6R>2VYu+OY1~_MC<uTC07K2{h=bkDM3m_#?kTq4K%v=DZg<_1zkqrkL@bnHbx$r7D^2$32<ZOtYG<{T2ui#X3B!rx$bytzNB6~$q0?Lr^Cb(x|34I(G-?8SM5LnkwD@fFB58%w_^QKUhlbjgl1+^yxy|dM%)C~e}r8&_mCo)p(xcyi8k_2&8y%1Ax1}h!Krb3w*q%5_1j9JBeswtC7J_tN&eQ)`%9*-(hlk&1Qpc!L)Lo7Y*YqU#;o@rRd#O|PkCUB{+6-cWe-9sdDV%<0bArKdXp(1yr#e%^n`5vu*pwFbon745Dir%8@>+?Oj;B*Fp5t-LWAS3QoV%;d@2$EB%*)LUqHd+)B8WYF%7|I8*LuPYVl+td1kaFxC6XIscc&8YN5sAtK-EpwlAx2#4ttxn^f%PyW)+hibS`d=&ToF`)KoOK_EX?s#uP`nRN88x`kjV!!08YF|+(br^Oh$>U0=ueFSKoeN?h?X2YZk>om@f%boU=KOko*24WaoinDIC%yQ<;X)>;N{^dH|_e1#-^od>M|#O}tIbfQJ>3vV#n{$JBHiWaK5JG6bswy&PJ4Bw52nM;-`+QtLRMiyGnD22(^Wo>|>gIFHp@3I?pIZUWw9SsIBup{aRYnexfh7)A#e(w6Qi%)ml3HO><o46pL&NB^(jo;e5uytyy^DBPBJVG@#E;I%s;sR-~e0LMp23hkVKCA1?OaZuc8#H18Z1LNm($PIWr2^$I;I+J^}!>x066?=Bx$Ow75F)i2<X3HM@7N>n_`jG7&N!@_g+-1%nzMv+?Gre$0$Vqvn^&Zf3x!^dHjHM9`%gMPDeKf&|pb$W_#$Y?t?4%~%8<IPAbe$lYdeWk$1yB3aTy`^?F4EDAdBji?X#J}0|JpV`TPg7@feoxsY?YxB5h~ON(FU!_&?~o{-2Fh_+`R+rYp|kjn-aNLw7g}S1|*4N0qRrU&q&}n3T-<D8$O;Rr$oz%)dkaVRwMVZ*A7p}#r&yp21Y`t42c}(R|RZ%(TYoPB^8yrRw|mn7yLFoK`4prGmOU6PBKQ)Okv^mzsQb6a`ejns&Em|T?q*Raq~G4Oq9(5w6wPPKSh{`V?PdtO3}(x1?Z&rhm3YXhYog6=#Rq_$_u}grQeY!bcy;c8Q~@97*ncjkL<t>BIW!Z?f7GZMVBB4m8!;y-~~gHz@eSpFS~xhT;WFl<znd?*;unco@27*`WTv*?-JPAh9+Htk0MI(Cw4?s33e}2P?yya?=tr5p*R3x2)O}Y6>i4{F8Nqhk!jbe(PM|#cYv)A)NH1#26(=HTOiMmHS8u`OnK(*+N(R$b;Ww81dw|D&B22}FzwE+@}qt|rIARi-`ird6{%*dogW!_P6d9d9@>h|!ZAn3HWgf_X=VupI5<Wc4{c69!lH&ged`=SqlH3~9Xu(a4hUbVehqW-SYY6YlvEkryIoUgsKU^apwLQhwK(7{0w@mv?H(Lvc9#e|cJoe=`R;_1(IN+9<2+D-y{;Ne50^54(Nl%)5R~{;rtFxd+VwaU%1PS5O$dT|r1WH!HZ|J`6hl<eS!HS@$$y&W^KnM@go5R1F_tdYI-3_Fx5!I@f0Vjy`M1apskBN0yIeR6A?$AumPYln;o3n4ijlACaDWdXlGB^dPGd5m-mn-%#LB{bIw)NTY?S$hAOP-fG3pZAQc3w*W8HX-PdO;u-fZ}kh*Eiz4rC=UgK9tmd`Q8~WNlV^dBSd^(?mJ^0#37}XF}Od2GPA`59Sy{%;z$rO0cxlobC=n=#lF8CaLNSosd6Nj9Qpu%*AfrabL^>K=+2<D5(NIajJrMOL+<#oMi+n%$JHzvkXTjx@sf*p0gNH1QKXNl}q{D)%S#oSJ{O8`fXnbF^FXk!59#WOk75mewmqYw>O?greMv3P-qxU(8zw=0Z(H2MTfR+qQW_6qLfp#xx4I?S6o+Fm#q%0RxYVykEndv#96N@9xd&L-Z!qD)0#(1Y(rdIL9dvPz^rao4sgH-arjrItZuzi9<ZG?W0+z)GDYE=fyG7vs&@3`Tw2tVX<pRnmk=nmA5W@VMK@DimvvB5I2H}?{W+R<)@4;x`Q&ZDYFEzGW}gJLBOO^9{gcp<=>?u}5vvTT;A!}rD4zS;fn>vu^tlE}*moDY)Iyq!3!bA>0rVyB!H9|S2+$A=@+NsAXF?S=r`1_S`3Cd!D4IZ$+W^IN=ohzquPXB#(yo-hDq?7`=~LJ7V}PpymY_G~8QowcC#BR9gx|FU2*P#~Bs#rIvboI7N7tc1V%)pXOM}p8TjD-5g4Cq@A{mYIyq>U|vKDfAu1Egav0RfxJlVeEz~mkzC0Re#V6fqLvs#`V7)yl&5JjsQY{ofUJEBZ{pVB%SJ|`M`J8YFr`np@8Nhw$q%H(q@wJu{_!D%W2E4hRIt;j;hjS%{3*EAu|hZ>A8Z2Fat%(rff(?pCSEe7zoZ#?#5oA!ivtZ|`GMRz)EH?<tAa~a}E2j%s7U79jIOOKL*@1dZkW6LHvliwKfRHQ)p-DzfSk$YO0snfs-956Pz#I~;4v1!8ya41r>E>1}I3r$X2G@^+>`(&=WjigF#oK&~IMu!_@k{91Rq<JN;iT&KT>aAp%=hpxjH_x(iPZHU4GtbO)qwG`1T}19_SKu1T;|dQda|0&!jtw6$Z&<Znil&crKAVqjSf<Xs3Yst>n$T@`A9)440+T~&Sw)}fN6@|(%OHxpB%f&M&D*zzq1&@mDIt}*4V<j9%st>a4<Ki5vY<=>OuE8b*cY|qE<GbSp<@$xM)v(x6O@J+<M^i{XBU=g0PE*u`OpD5gHjVMa`|493<n5QE8Z08&&P_(ax|xr2$`txqgav$8qn-kuV%NHEVSysbh$M>B*Dgyy4X(kBu7VNwct=BHrTWBY`qf8ghgZlzVev!bwq6m?I#9q0&t?RPbj>1Bq2D5(>VqkQU%UcR!`?*hp})PY}gFl%v3e~g-TY)7tRLn_|+8q!Io1_ji01cdEvx-Z!Nb9kYxy)WUEf^?INS^SXA}MK)X&hMYCtNs&%HtkHzx9u+#bVJ+U~@=YVzZn36v%daU4iMhFRNCoB2GCugySwGrKixkT&;xLySc1q+xFc)qDH{JfaGSB<p1F82=gx}rXM+%!{~4Z-g0fvrJo4Is5zkt1l|VCjhf+A7a3s0M7Kt{XThp?6fTN#lVn1LCJ*aX<e>Jzc9whfO20FJb7;QIK^i92ft7d6v$r7E%%Ll$k2he+W#ze5ZNbP_vbU(m(fDv5ec3p*DL=Ei98!6lTVjnT)LaB=h~n;uN<H5XUWPM#Zuo{MCgze}{|7JfDSmbEMnO>AJ|uUU3aB03`*!n&Uzt&X4g5BxnoFfmh%$WQ&Zo29Ju;WlAa#C!@@6iue_%(wN^E`5cQWKP8g5Q&r)1MKnJ_S76APUscE&8?a$M@{`sS5}RrzaU(Q^WVWOc71>5Exe6$+&8b>rG8bzz6<WWvYx`sjF3gzar&LK|q)OGNPElCJ>fRcmFT1(%ytJE87)ucup|8h>uzC4~(SXAj7z`!gj2O&$^L`Sx)drx#8|8n+E^75AI{TtGj>aI%P-xDqw_k8}T-G}ayJ$LluW}X9r3X1bqEXGReUSwH-R{JbzS~TEvcOwx7Rv|~@=mV*ikS3hc`0|Ikp|23gfjbm8dr&gQ*K1>djD#Qw1*0HN}Sb3__R3h;ELx&j?z}3u_N6Ra<z@&kVW*1d1wxKJmja>PXLYyj{?>>rk)598K^bk`6WvD$&J{7LLCfoGJ;K%!{z%F9|I{+BmD34m^&<nEP@yEM^Zock#Q!F08CN7=uwhZfxeWE)E4meHutP9Yg=$tB$IGULFY%BXq0Cd8pnDh6BX^#``$}0+PPI(Z^Kn*jGg82zn1Q!&OZn8UVrLjkNz|&8IqpSG4=?AggU_V4=O9|$OV0@1|)P-Oe|ZU`lN7Z)SklgRI_ZI*9@O&1PDgUJhkEs9;!J_m)|4KI@$AeX36St9DW5;bV=6co<4;|+VomM2NEZep^i;fO2OF@15fP>ab?!E+O^xBJh~57IfXd(6fh4tw5h`5Xcwu9xHH=S3J7BY<h4v0xR@mx7TVaP>d9^3h9^%psi)i5ci+Z$A3?9}o5#R$`{vo@-MqcTOxw4QsjuzNo}kJnSylDJpNy`fai7MJg9#tqlk<mA$w5MQH%mSI?!^i~0f?GV!4k^&??tp896+Pt(p!JXb+zk(5(5z$pZY_p(9jy#AC>eUVzq%_DpwDv_zen{T<|3Vx<wUL{A2+wzd_Nm@U(X{{a(fT;r{@UW#f$')))
_EXECUTOR = make_agent({0:_EFFECTIVE},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
