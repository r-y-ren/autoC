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

# Modified 2026-09-22: executed public episode 111915821 production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode('c%0o`U2h#na{VuSo(GGPyt{d$C9Wl`Y#REAurUn7KsE>vY#yAv1^Mrx$b09b>(n`?YUa}300MMzNzQavS65e^I#vDS|6KjsFTei%Z@*ss(~nm_+<f?O_0x3q@4x)#zy8<#7xy3k{>!ib@wflJ|NP_CH=q9c^AGRuUVnP^@oKvI{O0!N{{NRhO^-jh`Tp&9H}CF$@apdK)%5JApZ<5+Jo@dczkK>(`EmA=54Z2$El+>;<>_zUzQ4T^AJ7QKuRpxGy}cj7^Koe3e0uxt_0RWn|M=<QY4gZdqdxuZ!$bL(%gf{M@u`jydw28d776UftMBjLe|+;WZ}jQ&?T3$7;$2g+ocX$)e&P9MAdjz_Rv(sO3}QWKJb%8ueZ5_yarxk2&cZa8!XD1)Rcn<Q-xNhL%{%SKt5-KsIA31<;mbUytM6{#-F<&GUGEXl<13I5rm%wRfyk+TxcjtGIXF|Kjc9^$8lxsY!z;Y(zthjilunX?JL~>=-+!D3IK1m&^-8ij&1bdp=?luT8lME`^ZDlE?fc=Adf`dZ;f3cXAWJaXq18+uALnho?Fe3mDGw(V5~uUcX(mbn(JY4dBl(sk?Yt+LTu;u%%b+n^KXKe}!_SZ~GhIFZ6_jB5Xlzd^>KT?q$ZdS~`LEEk7khZPY~lk~#&?lhuuGO~=D%N_89otXcm7>?GV~t#>h9gU+gBfd{`2kok8j_-{g>^Kw~C#6g`0oF8(zP^`yn%x;S(7t(}(%sB_7#ohJ&{YkNaSXxun7vN+&*8*hMtigUR!v%;Q6d%!Frpy?rv0OZxTg&FS@zAH0?F76>TFvJ>X_7KW?b1H&T(1DHP;_7zO&?0p3xHGZItn05}YHv!oC%jL9;??FrbeDFvzCk$+s+2^yQ442YYGw^!gAe?<qpyt~1n5Sb}%J@jSV+Yx6o(@h7WYmEJBfagOJ3l`c3|1c+QGZ$75x<Gcr`_XO5c9~1+t7JjzONcj15()WSmK-aR{e<_C3yx`{G=wb7QL#LCzbCLYn~xc&m4yJH{3emb6qMGm=cS9wHp)OFpnQh1bmepCHl;0c~DHu`*zo&_sUE2jP4G^OuRo6%@CxTVIPx3<~aZ%R6Qo(e_i)HHq*R1$2G$E;t}J-GH`#t7@WBeAK%}6{^s`m`@dRn$mlYFm6k&AUmqj&2qGeD`sU{SKQrC1N3cAI+dm+dSzUJx;Oqsgeo0|rgHtmBprntF%&%FCII6<@(<W{J<T-!Xycvk6IyoSw+#B1hgC|d@Ls3nbdkUTZqNad3g%68~?db`5B9O8Xf&qUqzJsk>%O$m5aRIk?7FN%>W{Jv6IKt(#?D=+UOK->XUQ=9<q_$?yZPCx{XfOEa?6?FFc`<WMy>u2HVBxN$?|9UHjy3ve%8%X|<fSh#))eIsG<tEGBJ@j;&TrBpi3dsj6$ZdMZbTgLGNgIv5hN3S+}=?o!r=LJ7JW9|j&xA~-iQ1w<%H}ORNQSbDjNOG!Be`-0_M5d=mD%vE%K#y`N<AG36!ZAtr3q0oZUcaBy7p>+XQEfKicoMA^#h%nw$~ZZ(%0UO=RhAANFLsV_7K2Y&eiDI!uO{?R*2?+c6d^y(S7@ZPh(UH^mG=9$s13gHrKm`3k=Fi{G2C{UY_XXD%G_RN|K<Od7egi!yQgns&RGe~qS^9^X50b{V+%_TENb(fp2xS(IyyY#QCUk29)AFmZ7SaRVH!iYTCuL5XQoFA(u2`rb=)%3+RSg@XZ2s7)WZM@7ipT4&S$zD|zO5u)1dI7UIBtrjIQni(mH08p@?44#A*Fj#Q+=tLQQT{&}s0;iy0Ddgt1KlPnT?;!91d`D*<6bX#JzMh5-tC7GEYdH@q3MVsqg(bP}xj}vX#H016>iEydR_}wP>ptv}cyWs*VW!}BxU!2DUDTD0$fn1ykQ0rkDzg9$*ENpZu*)THwT|IW!Li%noi4Cz<_dGTJs#byV<$RHtI0|Nt7GN7aTFcY^0^_`7|g%#qf*{5V?wZM0LwG;-b}pXM*hU$mVg)fC>f=)=hQo3DH_?SUjBwaGw4%o@{yWsxWl`44-hSP_zf5;#|)9-LjpaJ7)WqkGSSlXs0_{N6<)$)jFPiO-olrPZNCDK4h1l|G=F>VG}z!HT+*(S3OPK>$p$%l7TSp&u@2pVl|PuTZJc9~`V6>t6VIe>(v$|B@$=o?{eNF8F7Hbmq(wMa;(i{Zp|mgON6vzgXW$~alh76VIEd?{?Dz5S>yS@~?#TR(P&?mY#UcgN{$MtRq|F6{`!4u1&<R9FWS~h#MqVN9G?uTB!@an_!|%&8J~Rd)in|KKZSx04yV8g77ZK5&SN_|(yAQW%v3#p%2AI(LE%-}H3&o2u|9vTxkIfy@ZAWziN*;tsd!()0eP6!OOtM4(7cr;1q;nNreL$!f6P{~3^+oMo-2vk|RJU`MjNILO){o{y0%LOha4SwTR;tyiVUR6?AgGSTV?N92wFMioP9Q|kD~FCd>JHc&aw=H8sVYR9M0Y1vXwC=s<O+OW%Ew~ETt2P!iH)k7Uj%zS8j2`obnbv9kMscNz=`-GIx>bG<}dR8HZXC3;Fv?AVrxBrl`plGy&l$r`4*eOW^0(+*y`XmD>H1?m=r_ZX5@+<U;Y3Y7kP`8LW=8;DV`vkk?i^4Q(a)Xq}0fR<OL9dA|2&c(S%KNSHsjPE>)xJONk*OE=p>oH+}Y)9J{Qr@Y4f@goIvxx~C!KKqB3uQC)YW1-6|9wgd_j1PWeMBc_x?`C>CoRi>cWf^992r*k4$1$WUL3?M)?v#a*PFuG0_FC<#Smk#n@oc4G!?L_jGmFl;AC&w`dxdvbfxGFQ^IP1v#O{)ISmG}!FqqlX#ObEue9wet-Q^;oFf~LCk+`;yyEO^yN0g68X5@A9&k=X0t0WGD9qriQ#f&)xFGNO;=4NPjg<}m;bpo&7W)*gTtbebZ!lyTpwE{#@qh&<y=L4gB5C89wriwVRvC<29kbBfp?+dKwm4X#HV1dE5)q@6+^(iYd1W78DAX^g-kLnPnjhhb9)=B{EicpWoQG82W#xP&VF8<0PL!tgsg%Y(Of-o4+wefO7#d?OFhMSp|60s2WM^I+6;o`nOERjILwyvW9Rskk2Ks8?Dw4b_imB1gpam1BE8oaPTKX4oIP+n`8nt7d|4r9fSTvOand0|H`vl2d%xLv6JKO%kY=zgLQmS6Br#G@RtMZPyi(w&MkwhUk*7`ewD^mG~iUW)M#oq=jf&N?gG20E*UQkb?274JwGA+E5xww#jN6TpDP@fY-%?7>To?f0GqI(0mQqBfxF6978zR-~@qDL5%<*9#8sL9LDH1vx^v_maa!kb4|?%*~^!*F;fn>-$2oa6?lY9Duqn`Zj%AQS@BLBy2uo)`u?;ek6FFUZdY7p(FSq4`N6PXPBnd*@c3I}uo(IEPn9S|8rMHPXyt)1tf1?dJas@RT?b4e90c)H{0o$8o|2@q@IlghtulQl?IKvnZnz<jMC5H4&FFr9tr$G<X&u0MD1_F{udbWpD}dhu#2M1`<H;+D`(p><``Ny~yC2*i`q3HS^hdM?xSuK;*@@FMMB<134BZy*DFtkRCWBZ^^!kfgn?Nqb3_KmBxfCZk#5XH~K1su*b++rj%hC%r=Xi1p4$zjdyB2{ucU6<p*g!nrTJ~zunRZgZlVP#ujvBVb$3#u&(i!6(gkeBAv%UHA-o7jCGHl9AP3G0kWNgY=KrBa&3F`6WYGc7LSdG;hqc)MGGhXjB0vZE4Y)DrgPb<QO0!1;aLj91cue}Sdw|cK-N-2#Attkfn!;qC`i$yWHY#N0w&skrasCKhdgWMU@eDwerPxdnC-rk=DEQ(5)-A~{d+IOt8M3^8>3T1d|mH!?yadi?OO%xORwfYK|2^oKAg4f;hCHlr3=}kUSaIrjG9J5CsKv_)-HEWq6%bJp_Tl-p+m&Lj2RA_7f^v11c<Db$3n#&L;4hNkaroo0e@f`aN5@P}-{3PR=vJ^<U!)j{dzY=$134AhooBFCp193QyF-nQ(6YVd0NN2EG5*qmL?B3qEy*qhogdn3E=kSnmqYKb;KY7Fs4h7G5A;UxKFi5?t*0#7440%P(Oir?{1j+p*essdZF^~pz+Q>&G6#Y^Z76U+B&>n;umdBfR133ozC4j#age1^*(Pv?0qUJcIG;SN|gPSKMDQpA_3=xUEvyn2}t<-fM3(y%}B@t&^8g%fsP&BIc7#?9X{VcnRL)s&v1#lD+8ju7@J#CSR@;HR3EHrG$s<-vg31nm|s!G``)jn^(J+E(G#NG0kcQE3>Q9icpSce^B;1z?KR6oywRcXViQ`09~a*}|duTe$VsmWY9mQ#@)O58WD<-nVUh0r}J12;GbPNmljM`2aye^FeyZ;kbd2KNzbn~xRKVPbk^aUZ!xqxGyEht*3L*8)Jvg@>s25?u!nGU@fr&b}0mUa_&^?YG~aGS7`-5EG^#EwYP&yy5M>P%^5-`7xkTxz`5YffkbcKw7iiZ*&Qaq>$e%A$o4I`#0D!5*9%D_63kxpEh8DQf6i;)J37Jzu+p3XDo{Pl~RB#s7SF&1V%cPX3A0~z+TTRnX2BCvKzOY1gvdZ4D00e`<$z2RbV`Ca7fmhf}t<kouM0+f_$b^VWKc47lMR()RWJy00f*Y)BBejU=^=?y!-Cv<DF`iY6Oz*VW8$f(?GE5-|2S@+>>rj&kx43E|J&*u7H8{PBLgdJ5znxRr556q2WCZCV&{6+W7q_5XJ{nRA>7M_>encp!FhCr3ZXXY$q~fO!q~r+C!z&6IaQP+@Zzn5(#oDJxfvRie4uQ1vdXc=F=iOG`m5zET6>bD>;%@3;Eq9gnXYR`z5MQLXje4X7ylzBM)^S=kPd;G0um^32@P^yqCqp;I&6q6=ix!SX2p4v~Z~zmiks4&KBnL)x+{%0Q0HcTTz66_;VOukYheeF~~G3g#!VJ@+eVg)Ww28M$?0UuIVoLBA4u+3wXu*IY?zYOvX!!zgyPA^x$0N(W_r-QcV<qgOWcU$W)o5&72{r_f~R8{Eft&7@r29Zs}^^n1yGvI0{Dw9m+-M&S32+#9^M+3X#FlB3G4X1#$BEF9wcx9#{E38W?Ib{|iUS5~*@Gf(7Xcy<`ZPY9Ka1Hpgmm8~9jIs6dy{E=%A96-1@^>#=@^?l^#qY8Tl_6O1dtY{XE!Q)$&gl>j1lY(vrzRtBq?;GoL`EZliyC!{a4#YV8?cCt-*4y05H$<IANX&RjwZYTO)0Mbe@!=q?U<J43NWA~bqV4W2y`UO%>%M`Zu7K0Fa1G8Wp8$@oXDSD8qP<aEyVapz%!-Qs!Sldi|#x;6i;4PD6I`LS5p~=jPN4Q+)AjVqMLNg{0>!oFl^bZnSxrrB?DlKs6AY20tG#Cn_f{Vqh&mJkh+hE?iPSfjcrWkL)fv}LL^H}4tR3-Rqke%z5IM!PE@cq-=EwU5kY2ZPmKkq<u*<{rp^!?fDn+p(t7>y=+UF_CUyOSqr_|7mfpSeUDtozq36z*d%N^N=sAQjny07fDo;^$OAO`2&8ZT--Zl^?LSK#lISX}h7xi>R=lR#@5|3n=ZuvHr@s5|28C?2sFs<bq2f+450k*lCCmF-}(LDGljSrPM=ZwIbQCrx&0+!tZxWvso}+R&@Su#{;DoIDS#}hYE0D0dskZOzlCEk)>&2<4ne~uw1;gkGf9OSPh8WB&wp1n7cXdqb>`;4($Oxp$P$IPY0!_kpOfK3QLEvt@-#DdHhCy^H}B)9WmpeU`T~NIO6YzAzq3OS5DxY{XFuHFcLOMJCd1GW@u(YT_UF~igXz|fzpsYU37^QoLrIOQQLF1o2Ib}HSlPx8SDskl-a=FV)h$s<3bVsk}H+l-b4fI-BG}XB#|&Yuph!>z{U?C)9JQA(ai<mMYPBtHDnSA$1tBi9g8tttYVC(lzd<)!Q26im&<N#n|;)X!fbXc*A-R;g3i$TCNXiSKhqAtjiPGhj<4Ht6JC{~n`t_zGOd)rHE?!k2L<+oX0PizmMY2Q6oV*vs{qXkOf*=)AdZ0yOekRhN|t`(MsX%c0yTvk7+&KBcZ|`b@D5gI$hl0ahHeke>h`>Gsub`f*?!*N&l`{^n0N_DsE6lZrVxfv?xe9p+Wp7(s4O8>5Fb6WG5cL*&O?>d8%kG^yB56a5a3HyKLQt%w|TI@zbb_+DZ7b#jXVF9V8&p((Q3}s+L9_+AVFC;WN@t{Lgpq<`s4x0CUsFUn%h))_xKPV0tIFUO?q;kfC&O|EO2Elu=biXh(2~~CZv+_tI0nRQ0et4XFrQ{jf7YTb-#O?QoV{0+iXG>TPDl5#$yZ;V2py+WTdI=drAn(=E0Ggb!Z-ndzQ<A{2o7sHe|_(tg!&40M>vTul#F`NIb~n$x6L0LGxi9ZNQPB*gt~Pqi}Y(r_+>hf$suR-X6c_8h=^f`oy9w&~1;j-INth!YLWOQ^u926<WGk&dw4om|9g2ZS;_12?ju)X_ApFrVn(b0#rt(kY0RZoh3@jRQR?04rzFqh2N-+bb+7JfXDj5Jt21kx`cp~6&;1&z!SNJc5kbK#H0U|M4PVGJKX5JmS#O47ROB3*&3tHRP^c5MZ?=t4>S>KLtcFkfUM=jCtn9ywCV#s6<AKxmw*>Mi696JX$Gi6lMJ_}wh<v7Fx_Z-z!u|O8Z<eH(+_q)mb8B!jlyx|CEC4X&yyCwS7<#V=xThX4d05EDJR!it+sr&`idwy_(Nuqf<+P1u1%=@g`l;IVGTkexCtY+?4modIf8uvmVseI>0Zy*u-Ne^aY?wcJ1yR^tdHYe(b`aUNyUVm@?6h1JHlChlSRXjde-o0be4;-)MLw?EiM&qQw7U%A{7N&ef}D6RM<WOMpa>9Ylgl=op};iid_uVV-p$193GQ_U9wVug+z3~Rag`f0c;_9tul=JV&1-t)D_?;a_KH-4<*ef{7V<&A9q+oc68eVqg*!=ue1b4?5sIy3xw18?e@+i#Xwq}Qi+IPEXP^VF^t&JmOAbMz_V~X>Ka`tZ1^KsL3S5-#ychzb`X%Wcz^3_|5|*lsQSDY4|S~$Xm0MoRv;!)rYOuawtB|ccy^^(-FJ5DM{(<ACrz5oMjrxhg(f6&gcb_^0S$C4%R(9~6JITi3S2aHR%S=NcH&*JD!aW!HRM)5VD2+66JynY)o-F<<+3|vwpG6z6E{-{9Ja_7mCQ!})kx4nEj=HBrJt9(M3~HTNlD|G7@k6lm6JnCQ5yEiS+^RmOObcSK*~V8B>RbUx}@E%U@N2+n~&AsCL+_o5y1M$wFDg{@eVzvJMOuR<_C8{?wNP-FiwwUfdF%?S<Z2Fq{$<i=U7xJI1{hsL7#{EhutM+4r=u5w{Bz9Ly)X~)qEpH3~3`5G3EWuia_BK<8=u3?m?Z4?CLXK)dV8zG>ps#pM%XiLg(We7l8$gxR?3dQVfA;Vm9=`(j1_8trHzr65@6@9f>|lmwHE$7P-+ZJBB6}iNM1d?{#*n6~Pw2xP`Uk;WrtfBlEy^MzC%Pd{8QalD2UQys?p|`@C4krl`7YH9D=v{IJ!xk~GDNHJ#7Aw>{+<Q%M%fa8kR)g#t>ky+rVoMt#m13Y>RdIjFe)Y10T>j?LSiXuBMMsH96wYyw`a`rv5{YjO$VViP<hW3XHtCyVPOXbx#3*zF0=h@uR*N$PeI8dgTlA^DUDhd7+j=<auRZq9ezJUY{Sx^IN_Ebjq|YY<?<_eE$(UlXk2K*!Z*UI%3XIR#u5C1(DD$KsMSm|Dx`&>rZSb6YP^mrS9#XW}+vLVupqFxITA^GpLn=`yI!#jYcJqJ}~t)kRf)8m<oe@aFdRhvIc(r@sNko4lvcc8cpa<1futL#Rrr0P)0km;7hZG)UABR)|70T)Y(616>Q&DZCW03|?^w+95Z(;m#gFehgXIU!X%0xPEjf?5zZC4h$9Jfd$DgqHu!|-VP=FC~M#)j*|<bx~<gxtHeO_V3ict2Qk@j3fSfd6K`iT=O<sk{WjUE(h@%WX-Qur*ado`!Fp!iFV<(W4Yz?w6XL>?{O&x1$wk9I5<P^JjB{wRYFD*MJ4{+a5|uTt2+wI;V<3znBJ#Lh$+d73Hf|P-&x1K{&R)QsFjCrGxWyq(gKhA`a+7rtmlqJ5<wfJ|fZ60IeG6#3D2>K3Kp7#-D^s_o08SKS1;J^XonV#wSip{mr#Tw5+>9t5K5v@y|1g$5WJ5sGUuant2^Sf5iN87mpFO>sLQ{z36vi&d%MR15+h`~OfE8+-w`=V4NmG=^so`QJ0)i3l{TdT~itX&bcx;nNOz+Wp!fw$Qr0iTLDkUj9Dd;7pd^BZe#if~GluK=WZjepRP9ak8YJkL6&r7+i;q{OjR(GZ5SIM;$_&5+ymy2o>bV@jgDU3SGLo#$W0>R1w<wN>p9kPEx&9Z1cREZh{Yo}Y&$UE#zGNw?~Ek&%yZdlDcJG-5+KwujLo%O+eE*dWNECrMuBk#QVWLy}|_+EBtR1PnLs4UCs@)A@xyr3Hvdab~h?r<8dYm(3beFT9+bm3L}^5y3^5EB(nJ?)Qij@|1n!DSdqVK%`vc7=OI0E^=y`lVY?vEo#h(6lgU<X~MBJ^@^sqVGvgKzequ)uo%DdKK>UatsPY`Mk*OQRCPBY`4_SX^1prKzF@ens74k0|ETndC45oUJ?XJ4T6UN=1QQbg|1_oSaJ&cfaPIDV}@@QqcaByC=HS4vLX6R`o5NnrO#K)OVy<#$96j!_$W`G@JZtOM=S_IDx32vxh0I*NJS9?bqL&>E<i+~N%lW{0oRdKpCX3%sMRkE!?%b#QI7>dhjPYbHxAmvXLn0i@}4PmF$r;j=kRyLh=u$o`s9ZJh6~ZT?90WfaKcoC=wKb(7Cn>l?O6|;SmDEv9M(q0YGz^MRJ(5gQ`@H06v_?pVa{*ImZ>;9>gOngK>LhzV(aj>;cgItmf!YYr^~V?psjslxA(znBv1*gakft=TD2UndL1^2e~Ep<FmHCT5coY*PP_cy=fLQ$an8MPNxX%cb6O|<VJ8i+2r9S$IdGIh$ciGQ(5pF}EIgLx^*q$Efk|rRd_(&fPf|0>D;;1KmRB+5@M?MQjSo+?gRz+boJ9c_6od18!HQGFwVV=KvWhAcLNExDP+Z1E>K@UQh0k`QT`*h6|8s61@LA`rMoDJ*uuJ|wJ;PF3^7<Rz4c~*kjn3xQ1>4O$25=Ki*b_}Y<ynU7yOv2r)W}bS;gDV@P)TtgHS#%16pGpy#;g?K5Ey8(sWKPk3y}`VYxP}Y8(Z-_Ar<I)GvE@%!(~M5xl?{94ZH+%h(ZL&YJ`*KiOEByKn9x#uX#%8Xi+hIbo@2Bn5AF+8UoV8$74h=EWNfGM>zM$(dk{-L>;AK6`0Xy2#A&nnNdD2xAVN{cNmpqoxm*GaaUki`A5=+8917us$QcVawl?nQtmb<S-z}dUM?*+rllk*Q&Nkl4NubXXC)E?Zg`^)bQ(b!9a~A3x5O_uU}B=1nfJR<kU;wxSFg@HWm#&r;doyd8=ce!kq)p^tc(XzD}e3ND<~C(1$c3<i5~C`dYWydVWnbf1i{A3peF`3I>)(3-lEm2a&8(IE%|hrt|btB@j62E7bSN{<r*1%1`A7YL8VPzYi#vmQvsP_jR4zHNo72BSkh=yqjfIid$Ia1M`ALDN-Qpj0F&UgPVjy%7eyPrxEzcDU=o^pm{A$CIZO8Uf!dgm1H2a9x#i11aJ-Gyrv4D(8jqt~c;+aM4~13=*>Dz$UX0h%?5&I`cO0H&^&ln01uVJ`e-%@No=0Byn(Oog-jGl<5^Z_BrCmS*{q;c3nLU!TED+3iPH^r)HyuK%D0Mbjqt0o{+wpnZJ0F!2;S)Qu$9R;+*a*E+#wmo&lL{)56eMyrz_}3*7u{AfSuM5%BrR8La~vUn6f*%|HFKp@4HAD{25UZZB3WYm;@s4*YR?Hzw*gT4bb|!<1Dnr|omd!Z6ND<gom~5r$k#Zzy1XDDaKY7OwZ@dXl;VdT8>>rvoAsK-P1PPIeqP_U(1ba}p(jk(Blrq$2*~1;+HDM!J46&@9u_I@1G5<xx=h`o_k#o2o}d#<=q9hc&*dXUO-O-r5RCBbOuQ)R;v?aaZr;>nduPrI_m4@FAAqW)*DeKi!U^}`z2Zyxc^L3BO=K*rels8&BRa5|^Yo8L?U6NM`+%WC2tC?uIfC4Ceew1`oW#Q*rQd|Zb3W2`*Mse0>>wi)Aq#d7cZDTJ_&VL7!Um6kjilYw{1UN7$X~r@TxcKf2Luku+%L#O!0Zh5dsH(O6C{30!SivU;~LNG&z7TjJq9m3!tc>lbJ~fLo4rV(i%3Y4_`Bcgm#Db_fWb@##H3AMviOw{0V*M$#%q-Fr#)K&od)d#RFpzlO)!pSjiib#v3e0J<+t$?$n7$+ULu5BP&Q2<4euX!g~C+{4}zs}lnbl@^gz^{sIGziE!aFY%5Bbm8{Xu5&?vU;HH8xZ6x!85gdCKTAvT^n^qLOC2N}9dR}A4mXZz-4LWIvvnKRgm;QSbIl(^aPkKZhj#6$&?ov<MmyE3DdEQ>CVgGPx8Q&Mh__7+Gi62sF{B9b8SoMDyquW<-U)-s!|f;IveDOxxla!dXnfi^HpeE@Ro=@I3*KzAVw)1pJbry&7YUjR(o$(utLw^MA9q!$~T!m`J}NVo`QiP>(~7@>Wx%Z+xkLxwP{R3N#k1Xk0mRQq&TR_u6woLOiPW`eGavP5qXQBIUb3f-kkc@}y9A&^7uRu@6KaWv3+^N@lpwRuFI*iUJDSueXS^Ukh`NVLMC(&0kXdt^>Tp`J%wr?oDwM{R@)QPcT~N7|I<A<0y`bL{Gi*R(OUY3uM;dwY;|0uj)f7|;Bqqqkh{I6|e?;nO(JIycAWgGa82+wO{2hxl>2F?JGx+XUYj#wH<n_A;V1z<Cs^YCxC_5KLRKO64&ygCyRimrwHiJ3ngJ_6#O@YC~$Y7q&Jout{jfs;eO%0Gh*F&P@kVh|e<6i4G{|f>v8F2adK6Cu)&$9T312mvZUm#YU+)LR7RN_8A?GI$J0sYG)(W*~~1=Hdrh*vd{*Wv6hWv_L&t|es>}VqH7EMGR|)|E$AFOPXE6+K?e6k(dwRv1Vqufjhj&{6+4*V1A3d=Jf+`5*_hW(C0&LR6L1&t$72;uIF>C9bBq@$r`lJ0uX;z30``JOzQS9@b}AAnpsY`>`SBPFOtO{tqgv2mRHWaVDl$iGuawgnipX%kuq&&YskC<i2bNdtbtH#})M~7P*w}~Gqac;kgA<qh%nmU7@Q;a4z##(??m;{zR%O6Y8q)q?^jIqFscJmH7f@4bam$GURcZWKIh7dcKw4-T2{MaGvn1<zKHxtzntTXrdi67f4qH|3EqcZ{={orcg2#Zekbq>xW7`10RapSnz0gcs5+Eryg)<c?PoTV27z4?!VM@Z`(NoR&KDBcT*l<!lkQ|lk4`8C&4Fh{GJF4NS?snbarGs8Aq){LyL06qM0LBAYPLo_^Fh~ezXU*i#XgmXHqfkhRH}VpKpSuc44J5Xe&i{|@yndGjV;5~56z(24v@VRcRx0ok!1mw5L|+q&!0M>v0m$*8aRUXO3<#hFXMr>^8dj=<Bo(?W?(Uw#N_SYgLAqp(xH;qyW9?3x=#mFq74oy(4U8rm9a4?WrJ-@NC2mx8aMS^vh|Y0VqNcLh)xx!-E@#qgI~OHJ2b>)ziE@TQH3s8!#L`cmY27YiD7iU;=cCpK>%YaKv0AE5I7$Qy7ed)?&4!ANcxjU}S`Qhqa{FOMNo-2l2@Ll!XIY+7*C6=FyjoFBoMWUI6`G@|nv2S;hKhef(-a=vAHajK6DSnT5~;?5Zw107LEuyyo*`|V^{7V+trFw2V3C=qSqwxZ&h*ltq{SD+24lXj=ar1A2(g$bq0j+??1esghSI<KJ7c@ZYz?RCP}(pNc-k>IjyyvktX^UKZdGc6<jDlCMS{BGl=(u}nba;sL@g~Zqw<eLqjgDG02g+4i_GQ>dRX(KSn^Xo-LJ>#ZoXL`xDFCktQq?Xyy{|*6t5$LKt=_#qWNB{s0=}$#}t~yLnLAx5~$HN<J*UmvznEf)uT|99iaC7iR#LHwh}()a9^KJK^CP4N=yd~Sb=E}27=*Khm%tWs%(UlF`X0@+JHTyYgQw5gR@Y&gFKCfJhI@-=wby@ULh-mcsS)SaCOLK=OdUq+PRlrL`;MkoDw{0{l&dXO5n9qPnNXdguie0R@&8}7Q~r_J}1$EG#pa*AX#~r(lUWP?pH_%ZDeskZFl<wLWz5+KhmIn3tF|=*T|QM!9@g`B@F@?c-H=pdpxR-5b3U~%bUf1n_V6}2-x=J{3o;*F)<s7Z$=MIde{NYkVGY?-Fe~q?OMi%(isx)VuNr-wr2?drjBl%ZV7cvWd)Ivp*GiK`@6N=&*Mrtke-|0ggyl_J&7u+tc|2L5#Z!=SaK&3K#*(TP^!3uYP-Dsj&&W9Hq_;1K@169jh1yE%5W9~YGS2{^QvV)W^Faon*g9t)Rk{?X232`p6$gN5rvwsEHT32AsMEvbhUPmy{!AwWqP%aM5?ck!Op56V<~^BS3INK>-|0RBkM-HTBMw&TXkYaF12ymjgo=0<d7O1YBcrS>nIT`-Gi~eB0W${xT6Y9O(w9fhFpr(cq%{W<GLD9p`m3hvz;klqxgUpC^N&&BL(ZoPu36-8}!PHQvbRV&@vT)ix&{V+RCE{(7!0aFCOhQ@!&?>4j%F}t8!_14^Ss0h4>I2ISPwJhZLJLRpYQ#Zdy>(8}!MBeT|+#G0Jj|P6Z)(GKLY)+)A|?;Ct;|R@}~rA%V#dQ|rhVxV_L9pk+%5rcBg;6u@LrV(@36z-6HiBaNlJC+k!YS!$yJ%e>;T#|}ikTO>DVa+u`@zc!B#o}rZTSc6`{y9?RmG*scd4OFRxOh71Us$CWb!A6_8P+`ZhLTl6p`UK##*e@HL0+DJS_V*<K4B%kYWT#@A-19X~kMh{hV8xb^G#NiYU3;8afFG7vh%CVLYerG*7IwDNaf==vY^-W)HF@Nol)FJPJRl@F!R~8NaWkYRggr@??`5a<Zn6pF2^cOiV@~^wrP_gLjH?JNP+h6H7J7|=@eu)Cy(x};M-|clzu^Ih@khn&FLQ;ARbeAI3tRAGIX6)_Z}pXZbh5tsDzNscpGCEg2jCzMaGD(=;%{@v>{f(|OYB9ty)lw##q4&$quKKSUm9X%^#nkK#P8-Kc6%40G^mm9jME^oA%G0xywZA7Vnc&MFzHer3i`EqL~%xs-|QCdkaX+JMOiz~S8=uFg{3X<nq^=WBM%*oo9p@h`7Hrv#kzp^QrZY2TvbL_C<}4SWVD3w1FN}>NQ)n7qKXrz;^)f({q%qCG77)')))
_EXECUTOR = make_agent({0:_EFFECTIVE},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
