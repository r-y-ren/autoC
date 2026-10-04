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

# Modified 2026-09-22: executed public episode 111910148 production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode('c%1EBU5^|`a{Mp*JP-VoWWQ15o<!VAEAZopvp@&}e1-wz{2=?y@PGGmcW1i0GBP4EyJjhw2N2+(cc#0mDl;oHGBWGu|GD_LUw`}i-+sIJ=btZrdhzz{#mB?NzyJE5|N37y7j8cO{ny|A<8S|c^ZDnCZ{Pp*m!IBTzk2`j-NoVJ!}pgjZvKD%@o@K-7eBuK;l<U>A6{O6xHvri`0;-an_Itr`RDgPEq~4)^7iuTYPtL4Pj~<R^_$BJ@d3TTc=_%3mzOth@N|5&Z{NSZdiBfA*x$Xsz1!){R&Ra(+uNJ+i_62~_xMo98M}J%@)Awh&lf*lzj^ol?YPmW50`J>U5IBLlI6_T?fwf-H!pJcsKe^R@*2amPI{j|U0%N0uF<%B@MVsZX)cBRI`@xSi_G|>I2DJJru}^J@<p7SPmg~4X`F|PA1<%1f4n$6*)u_Rk3f@f2rIaL5joVi*Y7tX2S<ve5e-ldW0b_lc!d}JyZ;**(*4Xp&APeYkMB+|I6Uii^~jA!LwXv|&3wFgclm}tp*&e}X`o%mo}51Kex^T3AFxiFmxo5-^uSRgE$!RB#Pcxd`@3&-FJH6px8s$&2gq57rZFt?YQXuY@^j+q0s}|%xH*_%dg6pRS2pkQNsMwyI^JW~d>TT+_ADfx<1LThMz^$PC>W2*l*Id?sWF~`X6E$!#j=M_#OfWt3%7{Vj<;O8d?B`+m)BQUmoMM_@~6u;?_OWM{+I0wZ)H4p4mbaXC%k%d{gbwwdM9B*aoT^0W40RM;Pk>>KkNW}rouavHh!?I%hY5yCijbTzIZ5Gx5&BM=oUQL-WknH^)k?=bltq=0^%~N#rgw!f#?<(uHZ@?@7<*^0QOL080me%I<apTr@TB9CrLXwW~VFWv!CE+=dOB?0<h<zNm_OnIEB4s3d5ge?M`<dt}qoge91v9o!f#PE?aEtb}`gTZnAUC?6$e%Zg|J)cG#!VyFtA1;z?*>BJ=8@8(OP&tP|6n{5@;)cam+e2WYRW;v_ZEwdhi{+^F2)cGfip>zRkOzQTQbyr)QkO2aNUB$H1#y+0TTxReEb#vashpV&0h_^bdasYjd9TOT#U&p#<9LphwtRC(-rCctwU%rd^f{YZrG_GB|?vdreN6OT{fe5s>Yodw5}d;9Lqix1ykzIpT48X5!k12jz!^jgtl3a{|VqQ7|am*e}NKBtieeTAq)$j)bu9I;}~!@)icTwC^VX|0H30gOR>0-WB0ceUJmy=b{tx0)}Zlg<VgpR<Dh9mUUQZv@uiq+wrZ?_<DJ<(GF3lex*uCkcv?Cq(fEuBG-Utuf#!LcpOM5ycIc4HsB1DuRVf<~h7%X&r$Fv)c462UczZHJ}TiwYwbjeAm7VV%drbSmF!VDbsUyf&!L0RIY0$M6dx~;Hxd+QNcHl?qP<GW{XTi!0EmQk|ZF{F$tP(la?IBX_AgR5K$UA*pp)T*4bL2*=wOW6fcpO^YR+&eIHKBUWXaI=&(aP!&|A^0~66U;On+~4Qw6D``ex&*qI}Q8bjimXXr#!fNBzkT0=u=W)fvWwaK(#ab*0XV_%%GxF~eO%5qR08F1AcNnqG01%<~5ue7hlk;Dw#xT}_YlJqWc3upuYz+0xa!3Y7ODSSw08RP___l|e^)xgnD;>D6j3!EzM!gk~Z-G@4{nn;mj=X?%*2Q_X_0Dl1{Z~5ch_xJd~UB5f=)tbmPv3}!j4BVmGE|!Oh?lO9AE_3V9wjbtKE-o6JSWn<KF0)%)P|C;{(V4_Uh-z5CZy}oz!|`zf*52~6V^-yh5`EBsy$AtH*wc#Z%iPc$aT43M|M=)K2v;YyawWe62SeP8EBeLkq13M{pnEzhHRG7dGYte2WChrcx<6OUp1jBVi$epcpB?vSE_j3OL(yKe?o%-A?NaXdP&Ie!Sth-?ij|fHY`cyZ{LJ#^%(5Q}wS_<S98}<FTR5)9#xqB{=>f+vNB|H#*=N2+;~n=s;F66tw&c^Z2|E34bo@)JV!+8j{CGlRM#_Xm5p>J-HV(j0)szRY%%f2EkPuWs=cRp{gOwZ?h`v%msX6=EPD~x4`p8W;e^_T=T=(f%3JE1PaN=+|-az)UnoA)C%D~LJP7Jm0`yL_)^LSi@(%&KXrtUI)Lf3C5v<dWFfoK=T35JKHvXKth?So3MbO{t8z73gmysVb)x-HE#SisByb3CI+M_xzJBjSjkwn;!5@Y#p!>zn_+QvBM-kHogKFn{eWaUO^nT{y`US*GrO);XCe%-7)#hq=+;R|aS1^o&r{9xbBYSCIs2)GQl<*?)p3eGh4$4b8SeeJL{1hSRQsIs@P)2I%KYAlS#CsS>Lhei9+TxIj`2W1EBJbwRU-{>;LD6*li`)1XA@$s!4aMo4YHC+`^rUuAdtZCBusILGsVG8XMr3Gl>_C<DnM)!t(&lB`6{Af<f>m@^Ml4oTmp^@x#GNdf!pC1X$<XEk1l`(9kK=te=ahbJCS@uwt6AwonG3bfYfMvw}9gFb=WWMTuC7e+Zzj--?(lE7oM#AH3oAky%1OCPg_1F-65Sf!H?0{=AYC$WAZ(s@afl9vQ(C_#%d7pY~)QVqY`PL$lt$jnF5tC^NH5{z*`G}j)#4&I5i#4=cM!1Tw*GTtBh7FnEfB9F56b9UeX7?DD5;+r(Ymd!OLhTc|wK?2r=i~)4O%+douV-mCh_6Hi#YmC6oo6tBnc{~FYT(I8gx8>KZ%6E?d^r%B6gKjkX(4=sQMd(pUxJ)!-+dl|ufXsw{-rXa_wkn=Uy^*KefuX;;gePq<9C2qpp8|@EHAD`i&*O5JgJipa?k!;=ntrgUv4#y6_g}RE&3E1Cs6{Xldy)ygOb20lx>*!#$OI@Zh~Nm;hys8|u_<fUjQp1vK|+tr%afeU4TvZ^N{XT|vfUu5VZpC~QRZ$kdp@Nm8~!~|{`e5Da&BqlNuKX0HX&EA99~R^fQgHUP$SGDjdj6P#d#6s{O_)Rc=7JK4WQ-thqsRV$dP1Sz;ZNbepW<EO$;T_amUAyUX<9QNIZ1T*~==*u8#mx^u(D|rkFZjrBg*3gs4}j&>=x$7^k%Mc7{rNvj>MECQ9!W`iIw7f4)tssp22p4G&$EQMVml-_O$N9n~lw2d{z^R<Uk;p4+rD5(kzy`joKffUr#Qrah4;2lk+f<FHl2X(Z3+l>?IA+yL6{D5b!NQ<mK|--H*j(iJP&3S=-9_vmv}a^T$brj_`ObTNJ_$zX^$H`ovAr8hHrSx}~N+SO*)OS*81^MRMix0+xsi-l(_h8e&}nTas{HYCN#Ito(L*j9)HX=o4@o>=N!(D%VJcd`!4JHi5dr0S4VhAb-RdXddM(3xl26<&-^OrosblZcO(RT8nE@4H8Bk@*SCF(8W0guDF0XqS(`GhXP_P}R+4d@+U8DnG``aE_N|M{jDQv^kToVzwCzlLMseNH_{ZobOKM#i0Z;L)%89^hK&jF1~`g5Lk>509Z{pSzhS~88yZ5Z-m=YiN6e!f0!Gni(}kOf;nL0@g^Kt8FC)y(?Rx4)FH5Ff$OvhYqLY8q#8Rzu=L^h3U_4VXIL{lTtA_+Lv?0;`sr0-_e)wfdI~G!w8qFCG)01M?3}K0d|?Cbu<6pQLpMuh@GUCtJti@}lK=L1N#M)~?5Sj3xf4pku(d3WJgo+lGKHZW;fR=j1*u~&@57yh7Miw>p?lHcSMH$lxg>dH1i>1~&?14^1ZJXjDiC4T398Ip<^oz5OX9Tv?FY(jl**t|DIXB<)<@|VtGb9*gH=;t(`Idc9rqfNei7gylT%UsVm}yZ3906_hlEU=56N&+=wyu{XQY~~NSG*=1Gkor8!Uesse2L#7pRBr6w(tkJBkZ4<F=~!O=<wAopldi0g2NPV2m>!!J-H*p0@Y{3@iEeSugWhV{eJ9-OrAaqLPi<uQoKHNu`WN@-d|9mMekDj?o#V)q^cChm|J4ag{@0S3+TVNE%VbQ*BJDNx0zOBiq#k?#0Hlcywzi&dI<4+=LAU<0<x(H@&f)i_f=KnRm&u${V~<f5fK^d;E*E!<4$z{zQ`JPxCblG#X~{VhR#?&Baj~K-aSx+*?ae0I!psbsOCThmBSOH4vR0<y`T2aE1{2Jmv0UJGdhN?^hl@g~PbJk3Pu;vOw}la$-HBQ7>@AO(aGr)=}hJ5`HMU1rRBg@xT%UkB=($4rw&IBem5hG;bLL=q3USMI1ue@mSzTj~*ROX&0k_36O}xL!uAJWux726-lDo;nXowDAd8gB5c@)%}8L3Wa<_Km%}rNVYJ0p-8F9n3kute60G(qTu`J-(~u^dTi8c`9Ep5HLikWo5e?<cK%)!{27{67!XTpH0G$vgO9~NcbrWMFUWnF(!bsV&B#eMaI?Ay{B|?_HNyZ>DtHx1s&H#IlvDoe<@T=_v)VN+#q!>*#y5`|B%!>wJ)2DuI`{8KtjWIDHq8O(<S!`1NByuSn)tD*K97=@Z8VA7}pRm|zKYtDgXr<@TFpR8^3V8LD@zA$Cz<=n-9UDI|Ro2({FBBLYH3OW}%p<9|iByVM%yKKn?BYovG)OXBhf};jWd(?ETYogMl?f`rK%ky~F$agX=wKNY%T5;A4~E77cP2O}V9>n~8bSO3BZ>8?NwX0<z@#R^x8BZdzy!b#1L#?Ul)%jR(XcMr2A6tV+1eb_LSmeHHC*J~kP`5*W56BPRiJmYZZ>nahx%C80k@G9pqDV>13zGVgRJU^fI{D0U%$QdF@g?i5+nchL*>uWCJuOMNmtDJc#yU#u#?qBNIOBnBq^;j!p~Y*MBA85J3wDpQ<h>do5p$|Sg;y&fG<VFc3m(Y*~ppJbkJhiA#6*^e0j~0MdYHgn&YNkI9Q+)+uVklYjx*aP9e?Yb&A@7`+;2ugqTT@m-;Xhxns(J(+7lyM8DJx`(33V`2&u3AOWG7lLm?K{!K3u2eHpgU;TJRp+U&GZvQz$1JuO2Od9@+0yrqeiTgy$!tpAuEr5o9mC552D%eVo*H3p@N(>vaOO2~yPZ<C_&@fn$2%Fpb=8@JEkIpMIzj&md|8xQ^3<n|`Bxqh0V1W_F+P^qR5W>#MFC-qOa34HCN(bB4-hH*%P&Kup4gl@BNRhHSz_$%HSq{Fy*JpVXS?Lt0Zsf#q1tpyVn9~QCE8!#|QlzEHGI^^`zps_;V32yW;R>1mZ_3z)SOoQVWMKWyNd{IW@imJ7u|6t1$qIdO6Gfbg2HHy@y=gJiQKNQh3#Lh)zDJ!KXo&nW;vEPWA>i7{KnT(UP@h?X8NMl)b%raM-qoJkkAsOK<#?DPh_LhGsAsF>VdYfMSQ|eh;dSk>6o-L*iRM(`v26t8cYJ}3Ub1kiQKj$0WK>_{#Ih<r9F!6>IZt~)lp1$|xDV<8HZkdrG?YW{wy6L~q(Zkb)&I$gOQ(%aM)DH!V7#$)?U%<AYuC^j=np{tE079aE@)a>fj^!Q2~>$vSYk@Hx88xg5p$4Du+>VAew|@mN4cw3ir{z6lz}HBd7sHkTT){6WkpQDt_@@e*V=%w&g3zz&pf?_RRErI+YIJmPHNi8Zt^c8o_`*1M4nSPE7lw`fl7c+%iLVQosiY}ixQhiAeg254{ivQ|DD9{56^k>AvNHISwScnQ&bejeu|KiHdd*}NTP^vJQ2Y??8uH2R||=0$tfczZ$zO+>^1C^Fqcd&G%cN!q3gKpj0=w)sl7A{A^}mt6m`(|1SzFrkl91C%?p_49<vXV;u_iNDKrb47iZ}N?Kh$7B_~!+DS{5dd$7S|RTrZvc({PDgTu#tiQcba|7qgfNCPy;uN8cvG89HWw7NQVum-P$@?My}$t>AE8AI;{({LtNhOVhw-(wC*5N2=>O&X6g@@SfEW^2bcA#<E4YfNZ1t?iW-LW6ali(F73PT?;|pK=Zzf+?EY4o=B&V@By^$gWT^+dJK~V;;#Rp;ykf8=@Fr8<LK}dl<`b;Q@UuAo#?LuyN3X0SZOi!t74^w-UhPCxRs3=kb%(eb>*sz5dW_s1exs`c|%oi(jP|Y3bD<+$L7EnXAeu37E%mBf$-bI$Ew3WJ>WkR6ejiJG3DXwLUuJu0dKoU?_GSSRJ&*^GJl=L_{mluT%)<Rmwq>5GGa>Sw_X+jz42Z+rbp@P@322w>oIIob){kq7H4~xy$3|$I_t+ZE>3N00@D47ime}s#>U`IxNgX6*~=DN{p;&VI0>Kl0NX`e;<Oa#O(XqmPJ#Nq=<daiI)SXgqf9m&4AO?8-w+9ONZc}JEheGvn5xI5}1uW?^VAsl9f;MlC(s|h$~7uZ&XKkT>ZwBo+;>&r<j1sL|&~UHF9Y8=<1;jBY70#l*qzF&4@YYLPdEkl_78htV|XR;I=H&3Fh7}Jmt?%>?01(cNdWnbO>dA{7JSxmERXM>&b{VnV5@R$qP?wvf%=SHC&5w8nZd(B^olL(_+K<3^|6qafnE#MySJmz%a<XuId)24{1Itn;W2@oJPi+chs(gwu;g!iH^iu9X|!i<V3Lx4Dey0TUr*CRJ<jMz)sOi;i$a)jv?d>l;)9sX+ZR(Jy^IFKh)P1-gpd@YZfXmT8fN~Jb}jB>e^nejE$W`1e;BmcDA}0R!2I;yQ|AiP>zPI*V2O0WApVR2Kv0hm1qfd>SlKpQz!{6aU;z=C$|-|O<H{6<por)Y<lk=wJxq|Q%TWTJgEb{6BD$1qR?DSMlHahNJo0>9iw?ZQYEzO0H&a50G!FU#VD-GSgsQw9BC>fj#+W_(Li<rIII;V_#5Ui?W&I|0581xBuJApU<nVvjgi*r?xUC=<}ww7f3*Uz4VOdkV)CL(!Ie`z7Y}WKP1Eav!ZW&=MbbMj_9n{9T&6oE7h(%Nzhghv7~Yf_at~yW7VTo@bd!BO%^B6V3tW4i$SGT_%U)@6SHX#3gbCXsszQ?}<P?~Fp0-IAC&=lag!I8{ZF?urYp&3W#_*X~LTC*B@q*SxT5HDKT22-cmWLs}x~vQ^H1_g^5;rP`iwdtBBQTEz1nXoYg~1Cn*!zh*xm`F0_&>`SU{k3g7DVbHD#cqKi)Z1a<{OV+_~|z-UcmaPB|{C$2$-2C$<}4qwhF1qkNXMcBy5nH8r_G6gKgBaX6FpBz^@7{u@qi80J0mYx%^QM$JWx16@C;D(&gYi=fs>iz^O^;DAdu&qd*19Ij@Wxx(Oy$=ddHnV#hiti7P<22NY_RverU+L|+l9qi$GTmL$p=Loo^s1Zknp0C~?qmE6#q6A2R-fsjx<XsO@wTJZrI@gcose>|pgM}vi$)s|v&5D#S3mV_rnv9YJ-3PQ7`0b!2Uzk2;$`u)_AoS{&<2aW`T7*%(#5Eft+YKnOEfZ)L;Ka{V(h6gUc`|fx)@mB0C@ygO7vgVb7kvW^rwR#bV+;tq=*~-o$25^qnM1&el%Fb5K)bv6$rx^yL9^m$Db+V5Ed-S_m#0ZG>%J&#y?Fdu02}a}tP=BTpxLx=rY663o^l2NB9^_7d4)kNaTrSQ<LJ&=4h|b7O%%&^wh~+wh7hO7(%zw9314t>Cf66olchhhMYi#d!F{-o&B;zY#y?)za(6x+3Z)&iPZzHqFU8q<Qx!G6?!mP!{3y!5)fd&QGrlc4X6>Skg0`|%(m_QJ%>m7r_N{3PJNec*07|*4c>IEQ~-`>4f8tk<mMT9P@(GkfyU!(Up1fIOk3?%|<tO}-a0lRRWdv3PKuBU`W;>9=}s_2#?a-uFtDnUrfAcC|%z-0mufnCvw=7zTb+N$gGzWuSiTcDJ{^Z+5GKx50EfcOTy0F3Z*42>AYj9+&r{Dwu*>@KqVBf~<NWK3Ic5t<D{(6;Ne6LiL#Qq&Cw*i>8?4ZEC;#51R)>)B@QTNPbv;O)5C(NXU%=wg)}vWyEBLhdTwx_=$m6wzri{WLWitZ2(^4_z4vuiA=7niDb(TQ*Dra2pmkDxOGJ+yg=bP>kms^bwy!37Z;7-C$Qw$a_qHXfz&$ypX*mFsf}&L`Z2QuHtz{JZ-Zw+!oZCZR)0}OC3#snPv5dc`0KN(Gk6+tk%>`j3g=);V5wdGkxbd&8G<xo7V&89eh%ciS8AX>20jwj^@^m+1m+qU<Ecwsp$vE-Vn6JC=c_*o5s4VSEeF7qzQL6J2MjI+++fH$}2L+D`fXFt}}xsjR&hTHc1tGTU}c*c>$QUYj0^&7jr8(M!-9#AP=D2>`kgpn9+XXqBs~=+U^d5L}?<$Lp(un%o<ul73y<*_<>cdo@+I!Kx()1T|+o^W=ic+;(!rJ@+q-k5=1m2Dw(I2U8gKRW{U-JOO9^M+sF{4(s*4r4&i(V(cVhpen!ta-Zl}J4cJ8KE2R%*jt}Igz_Y;(3<Q9x8i%3;r^(zM20L3b11I6hxk)^Nc!-qZGc$QgF)(i{Bsu9*=sPeCY0&}>`5G#zZv~a-Ly~w3K`yC2qpZw*06Z7Mf#$^<yr*|BZX;YCl=M<gIl&8dQ`(xPNj}>RJI?B{Qc(<zkQ~#@4~Q8`WI)eV3>rlg+xaB(=Qm%rT9pRZ9`)jmGR-PFkIpp;xu^j2GwvO(m`RAw(Fkb!2LJw_ZeOa^W+g^An$<;3BE{`8=YJaf#me@w&@GmNfHhEHsa-%kZ#+O5d2CszNdz-B1Iu%mZFn1oFHBcX@`U<pkgz6QKIG;aXbb591iY%Jnidfqc#x;2M9aei!kx=<b|(c;MX;_O#fH;^xCz(nA<`lU%_bqyXfmJ0&17Ke7C)-OV7enS@tv3xRV@H>z#+%=&go+7F#yU*HUXqrh)~}-=+HN-c{n29pYgDIAN~kuE1@#M<8Riu*P1h+V6(HFNDp`#qL5n#!GuDjNoPTnNHK)jgQWm>FxJw9L~{>OLa_s42FloaK-Eg25W|xscV4}isDjwjR@ZKvsyUc8pF{=!%$C|cdkm%p1CzY{Tk3kZ<a{qD12u=ndzwy#jR;#kgmCFrM0Gguh`qZJN~lyD0B_0G8QCs2O%sypq4KN?@@;lH8&P$E2y@QbZsLdpM3r$RuyBN-JU&}*84v;$(M3t{_p`F+BK36lGdEdF5u7GRf#3kbL8Ux%5C9=icB)2r0HoQx8jrz<Zrnm4h)vKG2<weRxm8k52HWoqKp0e*k%I9xX3JB=MQ3R7^g7gbzO}-{|IuE`-60{oDeQ+KIjWzirxnFRu8Pf$7-}R0H>2vH3SPQ!CUeEXiBe=l1|<g^iiuWK@TKpOAT!CMGheFY)?^P=>g0hgaoFeg0`jmrvkK`a$9SZbeqI<Afp|di5?~ONx)X|QtBIO1+$4v1pmmNq7(4sO<mW>oJPd#fWoLKd@T{~3!vm_@D9B0M;En<Nm*Ul=!i*&6WmjS!;=$SAY5bE=tw%9Fxhq9D!I0p+WGYuKfFT0@ZU++WOSe)Z5T)YY)xa@HE94Y36C9LC1Lnmgo)b)kJ%oToS&y$wKzhmzpn1&o7qzIz;^vyP(Res(*hUeHL3x-f?gnijElAi^(nMRma;Wx9AbfI`A)HXN1d{fJn1Uj?D1da}X|-ee_kw!(lxGw(0Og<&T+W~?PqEc2#AS0q>qiTulz{U_Cnnvf19W)@k@R;@U3?>&$u3u&TCxsNg=@boGjkiBrJ?-Z?&X;iq0&~^Jp^CXRD(4+h2to|Bi{l#9LzT>mAFpGg45eEeVvSn5^*>!fxzq()}@F)82<RnbD%Ge>G4#h4|0|m(vsI)wW&2{hFw6ABRMu<K!9W>JS~%9Q|@50Jr|y{Y9uuvj;6yVC;~8cHdWM<JrJt~9FJQk)o`YJ-&yb0)5MNS{7fH~w8*yXDy^npYX(BTN)+z#Y|vJ1oG)pQ%B{!oaS^{gW9FwcDHJR?1fHmm{`$$vQs<u}4)FVYEBmvf)B>fo&KCr$;F8AhU_Q9x)bC_UA(c4ADpZrq2>?a2O@t68Xt@eLw1N4f*(qj4$@gs3PT+)xZf8^SeYx@i-onDsc*vyiX^LfF?nr59s{xtR-yAS^9+|U(&n~qGSOm(9ayw#T<+P5%;K6!d4JkgAd1JIqPzDy+bZRyYowL?h=nf3QaX@A{tOH>fL#Zr_WxCP6DJnfq%5-O78gEU*|AIwer<npocOuG_@Nam&7DkV8D`TD1^bo#DhCo5BBjn=)T__uwl+PLdO;Ur${1L+QTEBS^zCSD($s!=-hiX+=NleOCr%s)v@+|7~?~i^&iU=rk6B*mzQz4lFTtHtENA>3^CIeqmDFv^m%s$Yod9)Zi0D^|E>)-BfSsn34LlR_vqzA-zZOE}&>6Q=-2)NsBV!-r)bxDS@fs?+7y{4O&_>?;UGyuaG8($E-yC~bhAzsbhh9hD(zhRQnEd}aUw^blC=rCs<7%fCeT(uTZOK=a6`UM^!TaIKzA#(9r_Vh|{84?%YghnnLrcF3cXKLnyctMF~<%Pz)n+!E&6NZ3{LyvDowZ(25t#kKK-JxS#8VKdPF}%tHTX>4YF#xO#(e1Cqh!>I{vI-jJA)LzIk|BySBAZo~sCf)eRsa*7#r-HK$ZC;ips^B?0j?<}8^L<lJg3>v4Wrewz~aCFu#^dkCRc~eAz0ZF^&BrsRtHs70$B&K#EjKR4vh+GLH+wRuy%gx6mE5f95qI%l82-v*pP`k)-j?TN2ZBGKt!%()C)C2`1W(pO9PvqU#o&D$n;tkFjCHLqv>z(LvRULIlC^g#<FtH^?}454(kh;jO}_ZRU~3iPIqB3W*a<{Ici@%wF}^%As)Gmv5{HTKgar~+&YRc?0~wUDJRDkO7yMN_9m!xN#htkq)NSV7Keg=L#R1{(-4(UN`9r&n43Z-tfz7?Kw5|S+mBEWRf_^;aStw><EE5W=H<yF8NeWCx-lhm^ehEZVWt4d2<S9}43wkC)3z++&*n|A2sPt8<R_@{{$AvM;;Hnqd9eK_>b@dmH-sVHZcEHU5^PEn%_@}`2Z)w9*04;&@nfykgl>}~(GY(r4JV5xVnd<man;eFmHe$Ss?q#=7T)P^K2CF4v%t{uZb%sNXCxvE9yt&YsJmG~FqRe#N1Natj1H|@dc;@}m2=u!Wpu{G3hRPxY<tR^^SXnVSHXzVSGf$vwNoi`;CP8<F{ZgJ9ZV-_UmJMucSQRto<KLZEb;+pUosqhs4B=N+lyk14^4pasb7`WUk1)}_MYNw=4G4ZGdC)!v%{ifS%mS;U%O3u96Ffb3g)bYN}=XC6@i=|SM>1&UtSZ!+<YdfM<5odeIie~QkAO4?H2563k=qLl_><w#C4S7S&x`W=np~@nyB`1oPL3$9pTgd-L!Q*vS2bk?oD;=m@B|V%#E5`r9KlkWA)9-CRwL5!QRFLU(~b$``I%<PuN6*nXs&SghkwL_uG-({OZm1Ek&^1OpD{otf3j@IiAUm@fts6ni<bCK{zyv!;S<ogCYpd{hDS1hc`>J-&~`jvBq>Hh($fM1o?&@t>R4NI_?q!966FjJp3<KIF?F)sSsp{QKZL<4r?apWmC@5QU?L&<mj-5`Y3F?L9Y;^Rc+G6B+C7yTuAyGfs+3bJ9zB`ug=lRYqc?ajzjW3Ujwg6N8uTT$Y3}BoG2Djzdyi9c&Y?K;wCdH7$bmRVXS2PnoTGxv>NL95qpouQw0=rBU+o;qLhQBHCH|^h$3*3a8`FN3DO1-l0%|&0A9V<&L&Vz>m`~(WlpyO;cHGSFZLklqSE`7h~*tqCib+0=}VZ9ltz{ECuqRPag!bt7ZH(68Yo7<cgT7*aDv_%=_E=O$Hp|bNTq!vscU91$5D2xEh|?-k<f&<W^RIsg7`*rQ?}5}!uM=abW=-&#9Qlx_8XQhQA^f3bdL&SX2(DUs>uf2I1IhTptXb={{V0kx)i*FTg7CKI*9d2FoXA9uaG$dK*-w(EHaxS&c&lGXqdM_h#${QyB|fcAb9Z-sNv1c<O6iIitv>Ju3^KL?RQV$q-Ru~ouORuw!Y?fUapuU4u=#UBGdRl)ro?)h)Y~Jk;^DljOl>Y3qBPZs{(Xj@nBOXCx2gY(0Em1rFRvKy}ar~Nje6eYh{oTr4aS4_0qjgi>6xst=ZgKNub*k+FgB`u9ChcJkA&fI12WqeIcO_umfWi#w7$gK37n%Yn;LjS~BQ%(l=sHzj{q~4lC-!VG8`G+C4C;YED(ps#r9&d~cb9Utw6Fd!fGP1ef)5L79iHdLq)kJ0o#YWFSb^M~Fl%z5qX~XB&KRW)!7pP;1HO3S>IJyb-uffbGi(KJgaFjoR7GtB^1gB|csk!WvRtfz#a{F$}&M7Hgje#Lx)h$Wgkt%1iM@6sEn9_T<kNg^5s*z*5#^h1EUMaB_LW$i`u)Nwt>BN9^*BHAK4{IAM(kBov_p>jCsCUBH&`&9lKqxuArX=c~co!a<;q<N6XugMdU)K}vg@Bo;nOr(Cil9-?6u4Fa75?+KKcHoGHd{P=a}vpbv@PK+SPh*vaLY2OsqH;A%wz+3<zv)Pqa2Hnm$4HAJS&NN<;X?pGTi{gSDE9s&+Ee9s_Np&48>=G6@WV|IROWvjO3LNupd752A<K??p(KPSqp*%Ucr*n!Eh2qpS+I2B?XPVL1UH*M49;0$L`GFL?gpDv|gKO!DLam`;1yWhNODb92V-aM*I=Z4*I;g+|xuyuCQ$EIG70CgsWEf<x4v{sMxOZCKLoL*ft|$mbEI2ecfHpX3L5RUS`;;ay?Z9S?a8gNXot-{gRV)lO|0xR(BXUVhS<KM`SBWqPK-h{FDT=JbhjD`hoXFA9J@b@md%eL3vm7Y?mSH!c8EPq-5#MIZj8VUM0w&0Ps+b#AAq8+@mEP&X4Jt-U>8pX02)#IFURXGcSTxBdSYo0)OKCZ`3wj1{!Ve&s)yN$lwQC&N7h!7GWqQY2;vj9PmP-%t2*`v9w)*c;D%m(U^PptALvQs>rBN4tGJ~d*Pr|d3ZxrWA@6gh5q-LR*8bboTzP1Q-yCZkAaj{5|)Y1!_$>xE;`aPIV74jXTe2LEx{*B|B$<U(PWlB_=Tb5{%%>wC!)NqP0>5Q}3ktev)K6nWt8w<R|Z-rbC@Xgx$=*a+hihv_!B_C=y@#xW`mHGSO^6L7>c=gVK+Fra5*tZuKj_&62(W(xY@BGr?w#THv=IYiLeH6S=D21yo1#vD_L{0OB_NMdyaH^Sdf$fAR1e^@Q7d){*^nBWBDNXaGOmf6yz|^vqKe0KB7nOav6C8JSHot5+hDG?tl%g#z3Mg5CaoYberIp}4&Tw3X0oD6bCO954CL;Pcg)XPyi<(!9mq7#l!a)RI&?JBSKcwXb2>')))
_EXECUTOR = make_agent({0:_EFFECTIVE},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
