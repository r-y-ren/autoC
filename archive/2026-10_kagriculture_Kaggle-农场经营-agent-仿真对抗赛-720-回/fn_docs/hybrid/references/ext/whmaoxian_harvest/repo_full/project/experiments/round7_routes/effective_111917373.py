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

# Modified 2026-09-22: executed public episode 111917373 production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode('c%0>3U2h#%a{MoRz7G;bIo`a{64w@1HVui2u@MBrKsE>vY#yAv1^MrxN#40Lr>m=~dk$%N1sL$fi1*I<=+ht7)qOtx@7cfq^6TIK_UqX{e?0r~^8Nd>PlvPr_~pO;?Z0my+<yG~FTeih-~Q+J^T)GqKK%9PAKzWS{_yJN>~QwecUPCU|9|=EaQ`otKfL+=^6l+Eyt@AB?C|{4r~f-_e)`R;zkK-d^v~H#-e0|ad;0a~zy11mZ{A&<i4SN5<Ky?=U0vOd;Kew!Z$7+v`}*hGx!-)a`?Y0ct5H9E_wGme!_&*--|?xAEB5yC)fHN>k7qwzzq|SFZr<qAPgn16&cwS8$#&-Z_V5QUHUqhT)nWDFG>l<cCynRNS68pMdo*qz9L#Ys&8@J9^YE&*$c%4_OL16E+Q+k3mvM1^d-eO@=6N{#{_5@Z4`+w-JqvXI3bY7^u!HM?$f>@+{;&}_I8!8zXo7MYqa;4ZJA68S5C2A{^sqAUWZnMW4>!vIhj-oW9{J%>kuLMOU60F~t9Sej<;99y1NB1o=Jb6JD;?f9jvQ))<!$3}w2t0(1TVvkAAWs%@bV1{|8{(G{{p!LQ7?uaUQIavRDMs~TA<y?A#P4)Sf03G&XdhJG8sC4d)G=D;=xQ663p=@kAIDR(psCKGb&3Ge-AB<@eZ^y%lA(TJ$xd{?)bORGAxGf^yunRSejSYZ{J?My7~FfSMP4#ynXYp+W~K-JNF4U{|#?={qFiltuVC#VM4K(UE+_eW;pn|(AWn>%vUOmp=9sDww{(I`(g5Xam`PT$<`Zker@yy&bPme)}{IwoThZ&yzK(wG9HWd2Q+}_4HzEa>Nq}lNnrx)rN%VU-v#@`{<^s2<&{_@ZSlvJC+54)@w;;mJ$g^k+M-1|Sr@p3y=@B9pQY`VUml*YBW!q)gIGF03oKl=+1Ag+2rv1OopWYCoBQjAU#xx(`&8N*#2-F+5?Yv?b!C`_K2+i7Mz5qM>R?or!vhv@5$>MfRdJJ=uv&DgT8>oiaywfaqx8(jT0i05J+>-RrqYnh4aejgmhpp$fJa%tXIP<*1I3n^MrZ{rNxj;P-}-PFe*bb<8N%Vjrpjm6D*@iiAeM0e4>J+o+xceFWSh-tCqAD7_)=G~x(bdj_x|SH<xk&Sy?gi98WMvH7Feby8dmg~!VrGb=$G&Q<v9N3a~f;VA;dGp6BNL4*ztB?s)2Vqf+QPTs}&Y_2{muaOXM;a9JmPJt`-J*c*DN~pCX*o(}1B)3X6v2OnWbuagCx(9i*sqa<6a`6Qjk-y|bNeC>2HRNII`rK15K#m;+i5`ntGHqv5DYJcSPdVq(mRq%j}EQ<fSM=nQH2E8#|TnxkiFz(NH#oh6}`*#<$E-mK%O*CyKvLfGtVXW0)7z>I`j$}@i2!uf8gAuM3$clsF7X_bdW7%iaX>XJvX*60;RluYFXi;I$a@^ml-*v4?<4fC+}ir@;&_lidga3O}6cm;_V8z6OYyi|FD7*xu0#cMzPYz%v;+iZAXCniMti@>KYIYj6Op*A2g=+8s2v6c}y?mzR2fvN|O%5va^Hek^z@e@NosR<kBT3Wj(yuhg+UCie000kSBN(&~Y7A1|43eNDw(>lXiH^0aX`D(e*SK`Bxiv^HY?lpF@9O!peo`1wuHC-ad$N3ui?r5|X2x5sw>GY5Hf4{^3R8BU7=FxYX=ro!eq~bt7sTKz3xs1%#G~*|h?V{et@q^r5G&`}O%=0L2DCJ!sUk7YxJcb4D4zd-oqs~m#+HEciSPT}B1asHPMX+C#d|#5Vr?5`}WTIvjooTW*U6^>iduU!ev&mlI87#u?mz06jri{`g%dU55__8K!I!5-~#>y)r9hoGj99E5IIjD#r(Vl{;Z^yacBh`$oi_Dt>2cl6O08E_Y^j>(c^GbNo>;PW1gROzyfHKT=Z!~qAnTJ^N05j@nfOePn`drqyWGpt02U{PYxMJ*wlevyA{|;xq1R<w?oQ!jynPJJ?x+8>2XM}Ay$qjHzB2&5(gDTgXT6q_*H84(46orhG5SEhMQyeSh_{<5ZG?fL6u7oy3Pnzo7Jm8r!VfyY_6J*mu@MweiiA-^gx8I>9Onw6s_tZ1&y}<-U1yJp~?R<ZB(R>&jdS3H6eRmX6aME%BSZ1N~vGmx*scOI9Ao=1)drFAbG4%*G;<s&5kNKNVD{y^%`@gRgefFhDJe&v#iqr|dyBEG(esWnD?mBH&?qSgt7B(!`;U53FJ>#zpHq7#lP^%tGgtQg)ok(X2Nm~hsZ2cqrn+#4stBb6Hjx@zMJ)$Jz@$U`j(LWBr6jIKt(3u-)`S$wy{S|6Mg8QR5eJxgQ`Tm79>PzCzhaL;^n1TVWS4KgG0Q*?JP8J^?)vN?S2CLR$v-Ow6-5v5C1x!g^;qX(Z{&Z%@)WI5nJ%y9)?<fcp;%P$1`u?w8T|Zc(SapxKlnZ8MxfwK_9=-TvEdb1~0A@T};8^)(tuarZ(@;P;9AHQ}9gZH;IBb7ltg8VUqE{*bx7Jyq^@p`At6>oY5|ARmTa_LUqPZQBQEZwY#g0I6(JEthr=Meb1}Klz6-g7#E53`Nt%?4q?47V#td~w=vaGW^?0C#HqIM|k--07l%YO1SIZvloU@lghxjXk2KWMy|5m9PQHEd_vtfK(xNdw1u49PGIBkkd`_EoB-3Zb;q5qk=8<=6q0XW;jipnIctN%j|onp!<8T}r{*%I%*7Wlj@t2GZ$6jr2t|K#GCDIzJ8UG#YlN=E;+BmhDr3n6Yv7X+_%}_8_1baS}`)q&xBgokHM;)bl^uNy;+g>(>M1HfPE)EW=$_PL9C*dU1eRjJVzgRZ&%kx`>d(7C3Ru83>m3qQVV<nZ8Lvdc9T5z3pNV;Lmfq&DS-171v(5)PVLF88|IBB$PvfwP5j`&-5iSXt7#=mLR6Bu?Z|fqrE*CY~t?#iO9gZGd`1C4FV@wJ5UT$b^IjKvta-<bav|hX+)gY$XiSTeGbX`L)0g0dvyTrCtiR;)fJ^M<~8=hSJ0VkmS*nvrAixA9Z%W!Z{GgpE~&@ETG(q(#=4%9x(p#}U>~~`Nq6NUIbVXmYPd5yLt$|8?1GO?nFDlSi(~UVSVEFqj0dpLOoJ9Er#5!LS{neHS%YV0_6blx!IJbRyC~K$oGmSd(IIGXG|VPgeMm#|Ae3|f+d1Kk<T+t?fEwq>S&5rZ{u~Zg(vVS_9M8buSJtr$lnF5cIJZhsI&ntogBPS7kn4+CTh_AaQUF0-H^kEDv@Wm*qkTmthBc>MYATv{Rn15IF;)(9jAY6OU5_Vs?oq&-#CUr&r8A}|Yxrc84Ue^pPIqjYR%1m=qZ?2j9k4W6?Sot)prczY|7Zy!IA6R2QLCI3=m5}6CwU|Oj!}P?Ure!yB;+L+902e%RHXtDdXcqS=iWw1eQ^hqPRZULEPkQMDF;Lu-eBVp9rVp3PVqA1;Bfs9*mP7Ik3e0TT1`pza`uJ~b<Zolz{eTv0EtxMhn)P50hi-g2u+)(MwaO9bYf0ERt!TS?H(9sMZ~{2Ny~o3K?QssbtkW4n_-eAKBFCQjpsvWXlFMaP$7Z9ciKh^)E@XjdQ4SJp#z7|d_{x5947_x2$G8c^b)!y5T9ht0zOgjw7-KW+j9Id-pk4Za!wy|Km`GON6f{_MA4^04G)mp=)I=->vT8E&a-4T^F9D=VvSs?l%`r+fbC;m(P9>-V;Xf_IZIaIH@R2BIkS_YE^*X>9Opq5c1Qe^+?#>yLnCFC=f=YBRSxnFaZUIy`PpW&iozhR8dNgDVB+jp0L%stN7N5^%{mEShjV4M!}>%H=Gvv>l3c`RI4&#{&dzNFZ68Z4ZeUZT<npNhkxr{|t!ad7*7E5Aq!{+ud#^3+upq^e?dY&sr!T>&i+&?J^Eriryu5@3&euyH*pla@-?C#*-BBkmwB6c9;|wzmVdsBa$pM#xvR2(+-^t}fbS_dmQagX2%6@^pvrXeK`(YZ=r?e1Kl0hf?DZ6o(6IUX?qEz=#|3pXxFY-Ne_yvq=nFD$rh6?vop8z{as&c1R>Ws0=E9aI~Q2@q^%!%UE8pkCoj3>KFVp&dX!5z}$=9zbwt7Tt+JV$`gSl`G<z|Bu161$I2qs9pA8jENBg!?AE;MX?$wp})9fu56MTb;fR&{eigSZ6+5z5MLiv!mV=^MsiwfEO^@1JsCMPrI(A1WVOnkEe!_be3bV>_{0vnzdO6Kh&YdPe8+f`**5Pp_EVRt}>n#n7rI(yLF<(mf(g0d&=nWQA`;5XzpgKOW{22sgxA;CU`YfH%tTpF9lVooeuVovD*fXP#<{^PUTRbP%3JwG*DN&H*FqPP&*7W)(z!ZCks0i&0hDSVNC2$3_vkUzo9EbH;tO?ho8@kH`pdxO2Uw%B_6)lV_#+VZl?~cpcn~QWX_*<yR~Q5Q)$fU$RM!bn*-Yfrp`POPo5}H3aq}g$!2gR+0dkw9L*o_Y_drlG>Askd!079!xgh;=Z6BZpoeD_p^;35N7yIJ;+QjyAzZYs6zTCV`4mjNSjX0jqgm7vQ7mm-uvV)waC+#~+B;&k&M0@C6LBgX^O#C)c3VM^9AQBDC2xMV9C?)x_c5@OVyjzn;4r4KL{5NHi9oiL;_kQ`qKC3gG}CQ8&JzK^a85kb8C9-B8dJwG#`$ZXR@!pb77Q@Y0CBEG2wUlBLgeDPDtV+%ZIETx7$9*4V^rg6u@i#0n&Q0o9QK>*?=NqzCsVzE9)<}4zOSNa9R70`t|+jaqcTp3LTEqZfhB>WHFkv|@gx`ufLVCJ&Z*8V@c4XXVNVeZG(M!BBtIc3&^rNJ;mRu7ob3!zXqIlmgwc|ezuNyKl>vT6d!!s{^O<M$%0J>Ycd-CwLGdUG?Nk|J3PtIWgv8_FP#=~{{!~<k!826I%VdWt0^@P&wo4W9aISRpFiBCg&=8CRMNv^bs9=f<F~QRyFSUzg@)|duk+X0c_&XQa3B3CDTTQ_#yM_n5$&RQlWR3;apU4S-s|LOfSLoD`ZaeaLK@MqQ;}nCD+@l?%94nLxO^(HD^2f~(C$5Qk-FRifHVumbMpzKtkeefoC7>mO5^C*fg;6|Iep(9UY;uvtNz%Ah`vAG-aQ%u@@D((}Jf<qaf<8_Oql(gD^aV;THNrrkr;@~Rg9}KYw1(JX>kQl(N)uTJ?CZgrkz6V0X$7+=VW1=f{N-x&r7`2EJ?KNISJ8ZP)UUeL_?WIzFYE0B<!64AG6G*cPC%)d2}sOC#H08uZX|X{+(n~eB!>&+GZsYQnb~{NpAaSxCxI^ABr?104=!^p%UTTkXgmkyCVH^E8fMl=@eYG`AD8c87v*weoz-9D7&E8~VYb_gB#JKaPT8*zcK9a{|I@K;zCyDYcZ`BNod4lT@rp%G7-6InAWaB-8IUJNDv9^}(nV!NP!ocCY^KYEHpA}CIeV~?(nE`Wg#^@`S_}yowS|>&q3RF8nFe{alG9J<ELO`F8H|mx{`BM);6Ot2U`&gKT_xX}MXM^fvmM?fMjIfk9tnoX3-qboeAGOeOI%NI3XzGfvd?OOhFu6kCgR)T;&R$R9L|eX3gLw3A5bc-K1fxhPmKlI0@9ySa#=M**~QX`1O#MXWXKr}5Q*PPdM;uuj6g{VXSr`RL!gl>2qZxI>d35g3^Q;ROQn`>h>funoX##sAX<D?xD+$(3Mt@0Bg?GT0ENOSX3!glN7yb}%#A||4~`kLi(y7pL<ItQC`O}(mRqwCi<YDb5M!=m&wFRz?3|X)+$2O9L<&ZmF@?B7x;7m(G#Y5D$M05QUpgNAMxrQ$0!WX=-pWWW%)Tih#<(Tq9pVUsEG)~xC7Dg<j_UB$Y96Ovs}@m*)!4=l;9ft3*%8j!gx)%j2fwfmI$1Dmcf>((mI7E_R0dBQ<b-Ri3M0>^4x;mNwH29sXqE$-8zUgh?H!^+n<@=qRs_B&Rv5R9t9lsxqUsF3)Hd&3h3BiO;Js3=ZF)&n5l`rmF@i=Ym|uwrXsKakBygwsfdFkn@<REc(uqn>Fh9@Ta_Q1lqcHj`K))b?PYR)?2w0P51~-=m-xRUwftR4UQvQTu_rR9)bfwhZ1Baz~Svzb+H4b7AM(>oziV6V#{x&_{f;<zr*hL{K_-7YWsfo2@GO&hw(aq>VSbnw$WthZ`87c6yLyD28vgk-2yNrq^1fm->C$IvVRyHz*JW22VPo|9or*k_BG&$|G)0&Y2cw8>JVr$0I`VebT2hJ;CD~Lj^7cRBDFe0yQEnOyF+(YDZ3zGC;9S-nRj#l`k90_?2>gGdm6EPjDyhyEfnl2xX*Q3!=?&khGHDD>${y?07G3`8AT}L9i2xxapM&R?xpila5UOba5ZGJLBsSiuK6WRhb@GMg4M7!NK!@`qFh|>Zh7y^NAjy(^dP~Lw9&->jKh7ejFn*bI!IYv=zxMGC}mcKc*fQB%(RJn!#^VhuPF>Fr*7n%xXWH}L+iRvVtY#G6}9!V~)8)~wxSZ4BI>SNfGVz6pmsMsrhZcDj}baGWA<E!j+j<QlagS3O8+5938(Phnmc4R>nmI_)aIhi}WoxTxLXhoMYYNJIVM{O-Je#N07*d<Pj>fXjOtWLyh;cIiT92P(<(?0CI`kjwitSUvGAVnz64}|pl4n_%!;}jdi>JV&Rrta|!TKkvf$AqhhBu}wnqq?6qFQ6Pq9TPujUJu!kkug;xa2w7~Jtb~+$XWNj0s=^5flE{^WlNcSD$rFf*2A|k8rJJ3Daz)K1c^-uz*M1K{Em<fZ#d<b1qr@~Pi4uBK!xIx-)_Ci&x6Di_$%loA=g<reI-UqInIWtPlRFw>qgC?8{O<<y|^t$BuG#}dt}T=xcP1i9~m+5puom#4uf<VD1w5J0B%zte?3KeUJx#_E;TM4zS3owdFszY7gZJov+gy@T?6aC6Kl=k8`t|nh?0xlNIX9ga{JaRA}=0w9<2Bt(H5%T=6Rso6(|zH+J;oYCi`+XBtn)e7Pi4cc04T}%QP3#n@;AD*uTl>^D8QGHYmUG7_0L-VIFwyDK>HNf_SeU5rbM>k1GvoQ;Xc0xF=d+6K1|Ssf<u(!|obIhk>DpQg;&KD2H&C<#W955Juk`ls19YFBL*WW<wC}9hMOj*GbT&m#xyjM|T47QQEp?fg!!`cKR1{yJQU|q(BZb&%*3^<F#zjpao!PhwhRJe59v~-G%}F+<^`5MjqA}SUwK7Z1Sx0Du)hsGg#fzWd?V~?6A8ApI(R!=o4%F#UY7q){jC^qpN*k)^!~cv-_uAB@BdO<Kr>y#uZQ3I|dXk0o5J3HM{tnG2tyeX(RAw1REwaltk(DjPaM9dk*S2XbbIBuMrV1wD|NHTUCd`Zg#8!Zt7gpYaMEynxqo?QqG}))D@i})&e!5jaZPzs}%V3B$|*PalEGeq#<POAs2lO#_&*>ha|p!Ig{G8IkcUVO%+dOs7VWdT6sK_s|S@0)WeKJ3zr=1NS%C8yZ?k>5GK)y^t`B#wb1vt1A1m^WdZ`=u^FKI>Rmk}!gm_D9(Hpe+$Kt8U}<n==Am<>N2*8DMAuzlp<%6iY4+%axihrUbb%IOOB2*kWmAxlQpydE&;h1U=^Vt7QYYOKA_$(uZ6aXKhW&HD(k}x{5}WP@kBjtqVGV6kd+<~!&Kir@kZEW;+R_It3$p0~eE2AAntKKqg|?oEN7Lh(R4Fz|mD5HPo``5OHUuGi`<bw5WO7YlASE&lD=~{$4W>T01IzL(CY{EJWcL+4krbIkKPIwfSpSARz>>%q5)UU)UuDPGB^Zfub)nTJbB5=ZRKlrpAWZ^I$ntb+q7tBX7%X$7(WeT3CQ^nE%??8V?=rg>=O+ZWXaTxscJENXM$H(o8Lc%>Hn^fKMi(wUh<1bAnYA^Lw)N-NZ@x{3uCYM?_>}NL3>d|es2Uv8$~<27I-5xYwuD#qpi^6Jv|op2)0{p5@Cuw@igQ&&Jc+wgDfN`SIu0UdGqr1QROAbjkAdIEp*kg0Wway83u!@RUUowVI(nPZJ8<g?8<a8UYGg~>v<pjOk(2|YA&@U`{UuO)bP_aK2jDxQd56+PAoWxseo@w(0;uFgz5g(roiYfNw7Gd=dXCS*S(K<vPJpp{lh5qoKH-vXfCtqZoGd&Ra)s3Tbj3|I`^hnnbv=b()OQp<$o)Y6lpT~FP;^>g@vzz|!Hi|`Cuxc^xet+jSj<FUJVsWhNtccuEuAVtA|l?s`^({D*f0<_bvaqB)rW(^mbi?CdD9XE)Mv^LWDTeQa4s}=>x3;PSnT7pw~<R{UZPdy|CJ+xaU8HS4ltS#E@21?4J8?(_VVZ<)!R9s@d)k(2$E@*LPI-lKUKe}4q?OaBswoQ)ATe>Dx%c`C<c=R%wwcdfJ5%TA}UM3a$(DzgOjAJt<OXVada9<$q-4=K4?XR26NJDmwK347G_g|0@Ri?S>5YuY>_JQAAs#3;7;Kr5}nPwO}KVl-b$wZ=H0=>Txc8uq$OeTY;)t&sQBYcMMasPi7DKhpcn`E{CI~F5SHcNp!j5;-Iac{iYmmwpnY9RAAWB#j^+x}-Zq~bONXkSNnD%^huwwAOycOIaQXVfXVdXUE8iJiZ<<6Mw5s~@iY&l+QjU(yXki9_DV}~*+74Jo`^Ix-qcbbgZkBFeQ={5!2xz%=*&xrr0V)#k=7H<EkF>M4sY%zHPPv%SFO=~yqvH)Jd1Q@{u#9q^4pS`^;1Na`a-msVfMW6__AUGRc2a}dz$NFSLUs~Icp}~l61hzBi`}y57q<QJpeM?<1JRe_{;|s?Ry+VSyIe~d2}HA0gJmUjA3@S+F-=O>X*mh^6LSq3=}f{vqUdC+D=zf0cz!06a<nc~UqcZ{Nl!@oy1Zed-l`-5P&e?G2pEr=p*CSJd27&Su;VUMBRXh}M94^bu<GJu0tikG`q~}*rF%bB#9An}uPdQ;U@qqs%;gSk_~Q{`&e21N&YW)qrA3aJfwnj-7#yAWv`^-xNJ>cTL^GS!;$Lg^cs*<EY#rsf#GZlqhw=NRn8xF=bo-!CtvmCMq`i%R7zLU#oM&JT5yJ)e3C-WijhI1YAQw@^fn)uWxq2cc&_)v!1*g$~q~N48#n`!*BJpquO}o<r13q=Og*q|}u1e_qCzG0AellVNWe`G;c8UmUSa;%ChQu#vCE+J|#rD-yHHbS{zSWK1r`*GmIO7Kh(+LV&bnd4iLbUaTs@c<<NhwG=+Kc{x3egF@C4)p5`OEE^B2iF7E|X8_?|f=qf=wW**VLPqIFmpSJ1C9;4IGi7I5zAs;YLef8kEo!M=rG`a2J5%m%K+|$w-c%ms1;{aQAY{NZMIJMdxe0N>4~6iS)k26;y12IO^ENKElV6J<t<A-hvVJ3+3jB?4ZKXCw8Wh$josWzFsZEh6ppSerX>O2I4R0<8pS1FuyCkg$-IEFez{3d`~F)h+LJZwAy49AVK@sD$eH_d==;R8V0}EObHSxHRvmzZ&EMp0vZ&nNS~@OiP9pD356WPX-RKDz}xaD^3Q70lK4A$+%5C5L0;rPrH7JtxOH=Tb)N?VW7*PVu|Fb`*vV+CzNf-V2tb5?mz~7fCtye*sR;Dp(nldwh6H$p`I>FsdXAPBP+AtmA|w)R(-TLgiZT*J-bg3cmnrxgBq(^cn(?~Mz1>)Xx%RA&nzDWnBA+0cny+g|zs_ZDb;^bp7NQ<591BV4CA<nD<A(1pcUsc499FPgI`qY@-kTsdK!lOaRtW|y_GXtR*lD1>1rP>;-VYvh6g$E%D&>sv`{V^z%v_k2Xv9|Jt!uhGLYa#=xg<F27I(l3|L-gTxMeELB!Zj3qXxb;k^>MA<Q0U<dKU@U`*5N!hrKhVj3^<EOt!(+$rH%AA^ro=bqKe?pHN<r`eck8nbPRo*YjCYcChqy(k+Uo!-#4;i2>lVxsXpJ=|sdwfiTpWQ~N<t>{@GClhq?hGo0fCf*)~_&CDJc5r&gTLc~DpfNYz=s<4#{(Bf_`8&Bn8wI+`>6dv9qD1b74MU)_w>_lWjP;LVa#I08NrD9#X-7SH0U7_?aw4#!<EJn?`z3%Pyyt}>uwLLU{ugdL^mmb3htjX^F^)cB@83~d|S-@xm7vNzXmAM)IZNFU7ZOSwehX7P#HwGV;6^2Esvp5(?`cOqo&NWtH$0L#IK=G{yWojBvcUNG}E9VCRKr(|nT#VD>@KCNI%8R4d!@5o+FVRsc5wsY9o}E-Q35?Dlm)S{0<ZVfM6;m$tjXLEScaizy&)1DqjzG%#+y?k*!@x0V-+H6+1f)*FEahfWwK_Z2hMzXsn)NEpt15e1no_R)9}Q}n(uN0Xq)As~owLcu#ygSxJNG&)#?tV~OL7`JTaxssO`pSsSw5|&+APD<MpN#}QYPBvpd^nOWYufD(+LuV2AF}X^%}F|)z3`gfG<{24j|J)USgQFiprd9KjZc!LVoD_)4EvJZyC)Cxkg=Ejs|w4XfX>RNUJ)qQSLVf&bqc#kf04DM~#~)cbNAN@gdOj4x$E5d5M{^cEYCOY1t74#~x($CdSAI4>)7A0-zkDeU^A_L#zrgm_<M(+*&vfPW$mfFC$vcR%ZP{M{phjiTZX*QE=**YvCh@y+%Vw1L$Yw*|jU8v)Psqeh2s}<)M?|am*UW>w+_2aF7Uq<#;UF6nO53*4H-#-{=zLK+)jTo;tNfkB)J(8KR4dv5q9wuB3BHo_TSoMWV`fVp65ril6*>@{fEd2!5SyokWCYU#QNgFO^UYNneGWRI6%>l}9<&@F-VbRT)xyQ~MS4#z1}MT!0mk9#NUlp!Jj6u(~eM4it!c%7umketA++(g@p5A55>P94H7LuNB!!_15HZuCh0U{gb=y+=5!MeucLOKTQc2cE`lDNC7}g9=_WOa0RYY(wA(q)u5N^NYSw-6tyutXfJ{fWsqwL;3P*xng&m^Ne(sJ>s@sSW=UP`k!aC@wRY92sgg6*qs7f4Nt)O!J`M#U(VyjwlrpfRO+bt?Xt%&Y38mwarx+dy96IL+s0Vg3lDd|(es^_l=w(Syf&<eoJQkEqOMdCR4iM^V-j{_%nzE5-;~vucje~m4MRyoFp134uq-=H^1`;J=C;b4I$H%ixn%R+)4aqY1IMUkJOMO7Q>6pARRgkZAV+TpQlc(Oh(_NxZ$3;Ocq~_Jcm1?ym4M{PMTCJ(qe4vR8B#<C0Fpzv=PL*@CVd5Em!F*)Ur6DQb3Z1t8{a-FkgM7eVO(Co*agI1cgMBcFCLz9pi=9JI_EiN<;v5=I2nA7sqV&3Ms|i-Bhzjf-vJAy$eO?c}HYwD-xn&1Ct1Tx;x!b=QttibDjwiPcyRN9KGcJSb9T*^F7Pb@n3J|=b#J%@>KY^lN)){33wP2j81Ut0a(t==5WRbapo~7Q6DGXzMa5#8}ri8!-EnG%+OEJch8{6pPATSVu+-V{TTneXzY)<=}4r_65M;dnYAD^kEsu>w6MPQneimEGIUYh%6r42blL;&Hm?{@<;a&v_-iyTM7CkEUYKq>58;mhf(Kn&2KLBk7)UMu0}9&+UZD4qd=PubE^#!}TcOAsC)?zB?^&4+mux;qK>Yw1kQ!^wR)k`CAw7W@|BtE2MFF6cJ;lQWrylrOxMK&a66cVMeH-F0&(+dL{l6{=T!3_uGWm6OJ7b#+R=Zr#I1!*+jS;93vG9ub$AiLi_>+Db>vfVqxH+`TTjNYw)&T*wL;;7@ZZhPH&Rb8OQ`;9M!kVI;*g?Y2Kwm6GkDrjmJ~Y&CFCRqmJ=Jd|r>gy$mR!L6_4=}l(M=M?^NTOHA%Kv@Q<%B<RgmfA6I&*dku(4cwimW+TRs*}=PA17+a)>vXe@jS7>2LhPQ2I#?C=-&&Fhc~05GLp9IMG1jcuL^@Pc2p@83P`eJM@C1x{b>!4Q4P9?bYe43foJC!B}5H7&?w->)gi-5K+0oo<RH*ETwk;Hm`7J|#{h&~1kQ|2ZC!^!U!4Or5GthL?_f#hSPNL;!#iY25SljaCQD*sXU<J^Q6T|CAo0#xPN3RF3d`WBqpc+}9=A|(auY#F*?z=ppwvQ2RLUz)m!PmK5W=Qr1*mA?tkk?)cqb1knNflQCXiU|@$f+&&9BC}IhWa#xls2D_88bvpaW%bPp7ozfW7Y>3@Ox*O4k)e%2QNtnl*<sdODK|Ft(}3c6yb~P2<-dyL71h4{8<Dz^I5$90J-)`=nUINz8^FP}UY(#@Z&0twf`WtlLCs8vDx|LFVSWB^PoLD`j51)O#?fED|;g6bg#Stp+Q_=YEFU#0_X0Bb6Yq?mvkbgL*k$LE0;JoGsPh4uzfbjLP5vJaBN3ORg)75}YMk$Y2MlwhWY#zgWT0CDcWourSGp%npP2TE!#r1PPladjyp+C1d13EbOHh%(Qgg^;no^KSk|0?<A-LjgpGx1dya;niry#i)=QDZo4cQRH4H(TI5m=giq9ZS%&HYD1$hBbUbJh*rGG7OY4D~9@HvGUn|;%^8`Bxy14}L>y~{<BtDLY;sk`poHP*f0Ie{JW!%dL>Ampqgs^15MP@Hok5C8dqs4uhNKCUjQeha{7Mr*|=z`--`~eBUvksf@5o-`WvRO>po2T@l9cpw#Y4m9fKpJHMu?Gd}nU3gR7vpBWY%S9fdD#m6f&2rDhbYa@awHyP=<7^`D(Um2gu|{Y<3!4Q4s^iER95b0az2y%P02M<6((iV-q3dbSt^~JP$fHak94p=La`dUq9Hch*RE76R{g>zP$qKvOy+j;i$pzlk&)nhCMZEo+CxV|Puitl!kj+vN2PYNgqtFwRyb4v+|4LS#OJAU%CLBk3rNNVVwwD6C2XN(Vt_fYI<S5AY@I*({_5@Z5Ao?e(6N2^5C(4_o-%Kn#|wtGef*Hsd<Jg4AD(V0!OsFIc<MS+oX!S{zJP@#xI}u;q{THe$X~+xuF8Hw#2!s6i0Zfh^rfsR;XokhiWT0p@5B2dmUR)dLcOcE#$yMTFL#X#jsRF>wL>n%^5w2S#Y}*LMjD2E^-Eb;(BU8{gNO_1HGoUwn=fUFSvndBs)rP|8Ge7<Mg8>uB_hIr')))
_EXECUTOR = make_agent({0:_EFFECTIVE},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
