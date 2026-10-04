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

# Modified 2026-09-22: executed public episode 111918050 production orders.
# Empty unfilled-order slots are retained; current prices and stocks remain reactive.
import json, base64, zlib
_EFFECTIVE = json.loads(zlib.decompress(base64.b85decode('c%0o`U2h~ua{MoRo(G9soh`rdc6rj`C{ZA}UYrF%5a2Tm80QDsZ-)Q7S0tyWx-v2%GP{Q>A8^2pX1Lw;k(D2jky$_f&&9v}^6TIJ`s>9%{dn=i^~1x(Plt<t|K&gb^}jxS@#*8=e);u3{`%jaKL2>}#}9w``G@<vcOTw9UK}nyetUEM>Hoj_>G1r^_4n_;yT1MO!`r)$7l$u@`ssfUt4F_o`{xfooPN$;@^Eu|dwTkpzdili_xCp!;sYAN{Pn}PH#eU~a5WF@k00LOzWe#p+#f$YJ#87;FzT0o`}9!$<>}?|@Ay>b6}!EDdxIA2$BXap?jOH>nm79N@#f+2LcHscY-hf2FMn{g8p!jj4#S7jFs5bQX*_?rxp}wVqj~$_V2+DvZiPLZmsgD<GruV=#bG&VKVH1Oj*Ii#s~>)w=i%bJo7=nZFAkSm7U=mEXb}!!2giZPsXp9&Scx2*DUwDsK{<_C62HVdd^&$GzmX}utPDI^pPu*q<1)bMT~E7LTC11&3_G8`puAS|li++lUO(R4PoLBaUsgK2@c0Cz31&Ss%=Gzj-qBl+;Hxm@$x@-^biR3+iCTfE7Q_3|`j%JPc~4Ne-Z~pEgUW1t;(Xwy-_T-avU>bia0SyxV|`K)&#)z8-R5T>{}p=nNgwXMHt~Uj@;$9v&`Z|ZEdT!W%<zdQyW`(N%g}q|+q>J_o41cY|LNxb@%`=le_0QCE!eqNxccAphIjXOKV+&hd?F)d@~{|Q;*kwAoV;CV?t?1kD;362viM+QPfL?Mm^?48d3*?2GvS$DuAhw7CH?y5`sMY{AH1FNHV6pF=_D-gEeuz=2Zl!o2C#fE^edRs(fbOE)c8RwG3^{)t^%;}%agT???GFAHF+eN69x{;;`3Rn47bu2Gw^!gARK*9Am-ZhSf*oY%J@inVyCrPJsnsKq||`}BfagOJHI>^3|1SBD8DT3h~LER)9&%I5X;Dk+t7Jjey$o%1FNv%vBWp;?fNS@O40^a{G=wb7QL#LCzYQQYn~xc&m4yF8?K$OU6(=yro>`j?Z$*REaL|g0bgaNMB9v(2gR0o+vz&Vz4FpLrMm$!6YtNKW(rcxu#c@o<~e{xsCrDm|GMmXY^Hj3%r(OJqKR>08F;?mOwQcH<Nfu=Ki=Hm|HXnsW|sl%v|I%L^)XV9AR^MH-(KJUGm{N_1g8ga{Rft15!X!vIC=rYA1N$sa%v6$DCy%P%WK9Zj-s&q+QbdOdM+PUZwAX#og7%E+#6f%gSVbghN74-_Y^w+MM(j33Lj1?wkId#iC~qD5DfT>@f~d6S}v*eiZi&q%VPDMYnG@yha)VFMIOfH9)#zyrdVL`lA|lR!l<!1FZkumL?T#x+M_>cPu6kLSsG7yu{o$wir<&@oedwDp!Eug>*9H(n>vWz5-^dR$~2mnS-}&GCaPAw0*EKhLXdtoMj(sJ##e%tWO*$hG`ehHd`;H@cnmQ!PW*Q1Nub@iB)b#NC>``N{TStp{tk4fi(+F$e{nR+hm!-2J)&*iu952n=CUHcG@}CyaP(~(&?E4lk<*g+m~|5bMCJhJdHT^gcEIC9N-*x(<ONn;KBQlxWX>yE(;vy=b0yDSX~g;<RAUk-rv;Wy``@KEFrX$`!MIVICWMmy(4Mg1NjT1LKDXlx22^sQK_q~_EWynHfh~E`+TmlaG(2;h4%bG!3Dk}TbaJD7-<G(~Xr?`4M$>^t=c?l|69!;r7*@tZ<LAsA0YmHMm$smz%IQbwX<<R>d;x_C0e}tHI>pJ6fC2;Npz~mED5*mHQP(v#qNe4UTy~P(*7l~nk*Uq@2`)9OAbdZ))Mu>7MdrF4iIz!M3Dad^F`I3H9>J!^B9};d$l}j(7*5{?-S$Sp(#&pC6w}+p_-+;fkU=#4XF5NY>)FbHFjujS1;2*>dX>6xb?%JinV$00OXUY*!pTscVA?E_-^A;PlgM4(%c@Vvn2_9_jkb1nRyR1IBX!>lA&OHb_I-n|-8DUK+9Tf&T2fIq69(t-5Tt&)|G2Kaf}T06cktpkA$q_EHy~r4Ot%KcQjQFsq1;)E%O%CZapct^_%vFkLuV&^50}9OkLFeArXs-ndTZ!~y28I}99_!|0h*!<z*DfgqV!ESi{Z%)FqAJ6V6rt_Zb0;j51tS2o(?Hd))nD82e1l1cuY{p(m6RNkd<fQkNAMLB-mgO<FB?9C;=|r0lH8)VQJ*MKi=Kl{>FqTpz_FXIWawy-vs`xs50_{(UXs?yy?@*y)1ehB3-T*(Z0R@{#^*kqMN_GBh<ooSguF_@jr8>V79H`N$u>Uhr;O?alv*LDz(D8Twtp;r2D3aNZ%%O>>v_|JV>Oe#BPRv60yd(K~fB3cZAb$L63<3%EC4mS`t8i2zgFUk}v|LG#4sDOGo;Xb^#Rll@U?9uM6;M@?|*v!LxuEu6<#Wz>NjY9Xb(F0KuGQv}wc6RdOKUWFjG*zMCrM!E|7B<t}xEH{ueKMFj-3XqroksAfP$baF#Y0#h15H-O})Iwq=*Qh&ct#6tA&paRsGInNt*B#6V~=M^nH%^KEnl5sfkL@go=9AdS<B_=!|=`Hh%9A~hFYQGwtTH+2yi%MeCct+@!k#1UzjboLCg@ehPYI%!hHG~Oc0$QCljhREYF4zP>Q$P-Z>GEJMMZhOp<mH`1wtUbmkF>h>Q0=;5CmZ0<SP?xG=4!mh@CGCG6H{BNpw?d{26wpWnsO@{nJe>W0tnw*iV^f4I&~2WIMK7(p?*M~B`whw+>Y%orTGVN;Y|~?iXZquHx)}!k!LzYReKxRGGNE~tfB!8iypub5b<fT2W~iGEdc611J}C@Q$mDfvXWBsM1WUn=oHqQHQ0pAV<{aV5`<4ujN`ied-=PVf{jf#thO>-zoY@HRy^z+$5<NTHVD8$|A0J>hA;qb3&~#M%f_s+=x!BMaW&docc{fH1f1U#*60KWux&-!k<z5Xxo)SyjE?~dgLpym608<N1-;cG2tx20Flqqe_^iK9QJmsP##Breo+4<BiB(}7Kx}9L4!%<8VFq=g<faqqQpQjY{WR08Ks24z0Do4Z$M7&321E2;$bcW@zF#XlpD~oadw=`qrwpOvWH{OQtpWJU5-j6V1cNVw*Th2uQS#*{T*p(=i`#)qq;2ohEeNaDEa(sRh}w-TBT(nmGHwdSZJ1+`Ur=A7L+`ZL7#o_vGgN@LymVm?fHgB)fvMwE^M6BDp9!s+W+nd*%oN>`cBWkOG*|%y668WftS!@U>AXWXDhs+p<@9job*STjkPjb5MOb@10?_V>E!H`i<16hxn9!IrU`Ddc8wTRPa>9P=z$M5Dbi;r-ftF6NAtKPk?_wz$y>Un}1|z9KHq;7OXCdr}ax*#kC_od<er$eFg|1fU-;fh~@M7Wy9c8Gle49mHUI8ToK}dP}u^SAM{xjn`jh$!mO-J^wP@Wg%6Pd2)$yrx0RV=W#cXM_%Ssl74ow202Gvxk)3Nl1eF02kkZ3%1u;9D9xyC>4Q9|-NAQCe>z4vnx*&gv-!-IIndZpbq^_<)DV`kcH;<SloPuBHv=1OedjOf5?Btz5~cNZMxuwRZkEglF1yl9B|=OPZ3A9#8Wb$57I7D8(xhmOwNvYouZ&_Le9ERiqHoE<h3a#BtW<92hiJT98JcW{H4P@@NPBq&`F7Rwe7qQ$X~-4p4Q`;Wz9Oc}9FKx)`*HTuYW`t^Cd1-NOyy&#q~;Eii_}9}0Yu@J*g7teh01zoYNLV#e&Gu?p}X%RF+0>qsYYdcoNTen_8OQ~}Qh`2>bToiUb|WZCAJ3?I)4iHD{`y<1p^%EyCjF)k?WHHKn^*<0?UX3?n8g2LcNu<ekzjwYYWUS~E2d<1ISN#=fv!r$JV{G14nsEZI=Gm01?pAAjnAJ+%(EZSqA!Iqqo_1D!Bp=8-p%0BDTf*=FM)KXh^1-1-KgReW_83>9c6W+X7|5Y|IG8-t*Brm(k?^x~mehw`qKh~m11p5L2VL1mZ2M(}RWJb`#lv~wVXXeOQeG{nFR1S=!dieBm*D&)oCgJaP;DC&$`0FP-d(JiufJLz)h+JWRVnlxYF9~z-Kv5ft7EPD%Rt+yJFf-T`m4UBv@>hCuzOICQ;G9RARc}5-s_l!-lCObh!>$u%=3}?^%fJVbG$-7|181SAORxvo#Ei~?ZcS_+SZ#wD$rvM1T45#%{>nABB;ye#i0`a1@08{$WtP{ny7rYb(E=~1+-bl7sGE-?R%9<%2uFJT40OekhX858+ywC(;trhhmxzrqINC5O&awg?TypNl5lBy}8zh4sJ?%44sJuFPz2l*k5UJs${dkmB;9CWg4y5BnHhMqD5D%DO{?KL65R&7gZ|SVyoG)MWXe_|NrgHEE)kUY_K5&KRlK2I*fab_AJ=yJ2N?>%BDSL*0;#G{WOn^63wSEER+jcYQIKx7Fj1^Eh=g6R9Ns)kE=SXWbSfVePyFQg*an5qfRNila(o$$SNHKP2Y?~-s=#fxtfV1JYuvn~5lr%C}$WJv6f{jGdN;}4yU^%|b(wZVqGqLjGKgM{~%%=z?A~&A&=)^CELQ7mtfnkh=J38<6gs;q7b2v{s4}_VcJ2|1_ByR77KYPtT;lf;r3EJL!2+-0_?s&k_^5m0#qkg8K(|*CQ&znJn;f%w$0spXlb|Z7iHYCDn5_6z*N=45AsKeR>cvaJ~Jy4Vdz%lZ77-(~2;nkm%FujQFMi_*Fqd--A)YVbRu4_A&Qml=HrilBdA?Z~j5MFjGs}+wZNIR-VBx@A-%YTkh!tBzL+Ibxo#E7(b5iw&JBoCyJiIl;u(O8JIt<I9F93$dU{*7N6l8Rn_M8w$PCoFePiX5K4NXl99jY%TcM8GAqX93snVSH4B_fkYM(CHARNQfM!StPU`0rAJq0bqoxWEu|36`>X@5k4QdrR90R9)h{7rD^?NtvKCq8fYSsMVR@IrS&6J4C(TLRh=pwG`+2RQklSVJ_J}n%KXW}od$*GBvL&20R8w;9@UlJJ1#XqL3EA(ptQj;64C)8gaWO`1kAwe5I90BI2qt-G^OKM65mxvKpmCfm4Sf>VFlSd7yF$7pMj3WDEzX=2yZ+R>z&3wBlN}NY579TYB*qzci&w<-YLs`$hc1qJQ?bthO0FIwv#QS!B?q}sqg|mjqD%iNyQsyte0G^?0t+23D+Pk52_5CU9brgc?z0Xb~4`70=Xw1oS2M0Vk!Q;HR>;Md|#qnMbLm9Ogu%Kl>*#H+Tl3{QXNiN&*=pp`~W|C$Kcp6vQ{*0v8Yn<KLocT_8tO_Pjd24A{E3T_61*Kqu$8~74wd`7rTOx`rH(R1r7yQNBg7VqyZ0Ytl-1eXFzX#5-ImjrDAE|gHdw;6ar!}>lm3}1P&b+#zTHpv4t>s`Gx`|69gErd6n6IORz>`V!syPqYyaRP8xw(adY+JJQk`=k)x7DK2Z|dl>=hP6vjj0gGxYpT5a1Z-6%wp3|~TJv3TB{Ae|GX(XR}{C;zf^e(*uW1bUH5pxiy0G<eE}J56Oc{+5w{(5$>N)l6{HT*91Q+=`Oa>!DCWN6H0j)=K@&!z<$@pf{5PiolpUhfg@B!ZQ`=0v)B?pDYVoW5~uTru>#BFr3xJFfsZ}V%h`xY4i0mtdZkB9=dXN0R%$22dSrN`x4Fp@~7>EmcVvS)$UPPngEFb?J4J3C9Qfvk;PDQnj1t}sc>*+1GF@~sk?kpct8Zm;*3m`*ja5>YRll)#gQn*D5pl3WCq4VX0^3kY64$u(1|rM*KwXP^XX*N6R0_=2p}#HI<urH`%SPk*5|X|amgod`EWyxJYC)rzaMpGdq8L;x<h0+Wsi@+6h2S}F%a@1xKy0ZBlQs3bi)vWLheCw=t5#OjsTVLCK1sNncaSk;O9On;!!}NiyjGhFIiq@*Ej2K2AiRs#)9mc%=uG!ys=1y>Q8{1E}=S>BA`%cT`<N|SRTu1B0Nab@v1P>KcOkxrS-|dOZvpsW@v7L`GgDZ0ID6r%i8hN>8$-44i~z{a7KtIpw1)iWz7j1lF@4_m<VqllXm4z)dkFKq}1XHxI~VoQTPJ_ZWTONnos7G>ju_ixbyfXiTU;`=tBYDoH1G2O{kdbEbdB0LIyUFHA8q=f`ZESK^=pqTiL>HnwDhic>@|&1>h7eS&<MkP6pcsG;$%hPv^EJ5NR7Up~Ehr8K<Km7>KyDz!fG(q>#b#SwaaXzIY<~2cg9a=q9b>DJvX=p1Tg+udGt@kRT5{Jn9CW(S0P{$O~~Np@;-I>r|-Pcn&Z;nOx(zsl>>zktvhMWVNQwGy8Q=Drj<Wro7q}3nWS00A1hoX$<#wW=<JMw8JD~=|boyb4gij(MSLft}g<C;_*X4sMF6jBXH=l(H#_v+XFsPfL=4#?J!(ojuN=^kVR5x3X4}1<7`9@B6<d3EGaUbeHY|6At<r*j>~{>%noGnWlL?%1E?(NBaZDz5Eygw%{N{_Z-%=|LKv0myn3l(KP4EmUvpmzm_=%}(YiMx7G%3eHLM!W)XR5*Vh80rDEJ?QkacI_R~mUOjOjT}AT)Z3RD_$LY4kldF9ayfgI>d}T0eR`6}+2f3;>fG^@1KD0j&Q7K4K)LPEBs1wXwaru_nYPbZuK`n;DS8T|~IzdfGiG4CY;>NTA0?q80xfG69ZLEga;Syxn}MOP8X#5zq1WBgcprfmTQ;){Xhh@z-ZzE1d>%nC(h0x#S6rS+*Hf_d3E&IW%LN4BCiPt0Xa=2F9x&_1W<5?T|-<vA|I=Xy&TW9OoD2auZM@aiMAYHQ6EJTkX#6$p)kOrZ5pC)msT|vtmoi1LO=xGHZ#i#j*M4sl@h;%|*)DlIJ8=xF<vV5J_<nhbD;)AZW@Sc8bQUIP(OST<?zWAP|L-ohyg&QMpGWEs5#Tk9}?$A)H{V84it<35!a@a64p6utHIFcErkzBOY<7CjjT!_5_&6g96<uB#PSbHQ0}06JQPm&#AU1XQAF~ELHNbK!$a!Wx6ma3L?b10M3UX=oMUyG*C|*+(vU<mtrGrE6dUP?G(GcJu2iIUG6FRux##yz$%ug-0&(;71cLeez4{{I8*IgdNY$-OT*?ZX(fC-e$#3Daz<J9a)Z!C4-&k+$u%%@HVl`ZJJuz$!yHJW6rP4`^h?~Khjb)f9lG@~+1jNlj@AaqD>@Q%wH54B*qROwU@2*hQ;B5dqgQ0fUMLLKW1>kuS650#bVrVFc7S)g{)EC9c!k-yr7dLpV(ZBWEH$!D96p+}DD6R3LnTtmVgtG-)+*)e%d;q^SN)}!;z-qG(5_OJR$qh=f@tQ`sjp<6xRQm|ngvJW`9c9OB}&MyKZyOn$35w_CY6?RYR0thToh(-3hCjhE#-0!@#$j>86OyPDqNmG7C@yb-mIzUuWUker<ksJ28f2Sk5EaxlDgU}W<?;$Uh_Fy#=Hqi+h*d#c*)X&L&Zy$mD}DU29(!;u87)cN0!0t9+UL4tpl#4!3<2av+^m@mxW~2H$;gFmf75Cvl)5CF_f$Yi&#ahRcd`PJzeXVe!~#AJEw|$Z1jZh_#Vha^jUarwUT9>VZ{>eL)ytyv{SngkUrP8KMn9>6!_%*f5ym|079gIa0E=?nK<kcEK70=%S>02{Tic)&Y;huR1E`IH~@3~JuoFoJ`f1XkD;9=_C`!x;fKnEvrcj+mNE@a!v4(IYKHp&e()oQBz#l~k+d<WhN?M59^0fkeIBg`tG|iNRa0cQun0UR7zg(-e_I9ThNoWueQ{O*P=CW#3|fO#QZzYUl=J|GkkHPmZKFB&p$GXn-AaUM0EaFFN;Nh^P9p<WRk6VG>Mig$gaaEQF>;-Ffo>TE2PK-=Z$OPOidS0Mv?9jP5-yJ9367db5%W413El+#vI(R~Su;;w<SSiMy#-+ifQ}}gcwqJ9Z1@wj!!;141xgW|Pql~$E}MOHXuM6!6;Nw2f#B?ch2&Jc8mpp5yb--I0hLv3ohIK92P4vL5S`tpujs8(!Q55^twOqB%bt7QMR*39cSsH9g^h9-R20=@JIO6YhFI{1-@X6F5^^J?21)a1O8M!toAS_^GDIecNC}P_@c`YYn1?QD-9b&9>4MvYyYwIqdG(`=5I%hgYl&x^w}!$mX17m=pEhtR;xcC;LGJ#pKCvL35Wx0=j5M<ygtgh9>IfNP2L)`SVA9-F`B9*Oo=z8e6X5}$d~zv)%7dp3U)^y0;7yJzb&(gRIFngRQi_Xg?amk+jCRYoQC7rD^QmC5eHx6Wcp#ezk983@Px!03E(U${h{Dcgg}@|ZbYy7CXN3TToFb!Ydrpw+i^eGs5n^nc!aj>Oa2mf5ms?gd1L|uE4v$dCm;uYKVUl(hENe{d(Om#eodyNjExRVQW*2nkU^jW$fn0NizD&q9%b%?oN{)=bD%s{L5rGohM#V|iLK<WnoB35B;auV)!{}0l@XIxO<udjCm^v88{oHIEzlAjLIvgHO;ud`d297YCed0}ip%0_l7|C6J5h3H+bjxO}GPfv2nXTky!fmvte%})~3lJajNGR|;Dv6hxMhNoJi!1by1VME+#XZnWR65`#>?*y{axO_3qp(X4HS33^FLi;REWerE*Y;_qc`u4vAm&aQlA3PUkT%=U?^XySz!KBc5B@P-sv4@4#6s-KKLK*&rekxFT=XY=>_srT7`WR(0Z8|V;T`L>VmwQ-Ggb(F44Az`DuGfPfcE!?tFt{&YP1u1H?ITonZjx1r7Jysn0R57637b?vEH8nfj!o^kcK_3CE@BZg*k6ig&qXDzLLHJo>*tVkh-s(-a{rZqc=u-Z)zBU&{sPCRJt95;QQ|bHZl>8L*{6KZkz!)V*PRq<fzREB3M$D14I~z2P1+oA)|5S{-FR3>4v-0bf9mc;)t_VX|<?5(YYv9JZ*x1itHYiUgEj;I_Lwy1+^4TsZXiwXXiRABIdA5_Uwi->NfQ7d&O2w;l?Z_YUH9(p4^H)&JZOV;A?4;^uXP>J(xVUd}F0S*A+yGRT57aFKd7nU1FR7j=jmJXHaAh2192ogGDhF3JPm)aPtwMKY$C>f`EV_7G`4_OVv_ZJ%@BE6(oFcj6K1My&ZK4);6jW!j@WnmpSw~%2R`t(Ay<30*ixa@Fz>ySb%LT4LgTHQ4c>tqolY2HIxP#qHH2Cl#YBPpVQl9COP0~V4u)RD8f(DEhDQ179rveTQ8enn<b@6=7^iT2auD=5xcpuLjDGth8=2!=#WBHxKO64WeQzV#YhR)QS?{E!9EWt$J-@Ch<;_%^b!anRINpR))ovXNz#1YN-xG4x<p@IVNKQI3=QUDrwT8M<>X`heN%@nci3mRw=vXfP={#ZFGAZAzCfKA+&s1>+|;;1r&;ZS0~kGm4VF3MAla>7RncYp+!a_OrTayYnf3W$yCjvB%y?cNqZ>IVhBNs6V+&Jnf?O2gigq~&?YW@91eD3*C4Sazqp{(MQJdTibYyZgw5x&nJL3GU-(Ys#_lT@pee&#(6F*ylc!udFiB?Kz_3BL`F^p#dkiE<~b#;J`Y9Xl=3hh&qJ#-ph)Y^!|f#?K<QFa18(WLf1CmuN^`H9aXCPsCNAG!fH!D&<%OA`-pKQXpM@dmi$;1t@}0+9r9I|OWk8`DA54jv#ybullpOpJ)Ry$KblD~9k`vD;uOKBSqqb$m*zeUI55DHj+liD{B>UkaLK0wgnEWaBJ|)<)F0plhI?=1D++!%{lOqZ(T!0h(0W&iM<27*?6<DTjXj@L(K@H1ye%M|E6;5kEWDH-GMa))r)TIop65cdE<&el3cW(Ro66ohfJOvIbtP&c;qvX=P%S#GqPDim^H=@Wb{YSgD=-JnSl3P`A|hczvx6Fw8kI!V46kjPmfei2^7!BLQojAa6EM?ok<bA*=AdP-fb)U)*Sesqq|$zK7a_Pf}za?8DDR67=%aia03PprDJCCzP^=MgsWlRO2#(^*}ygyQ7phcTS8=njdm^m8O&Q??Bi!<P-f)94o9;-L{H&c~%(h0u7Dwv7>}x?O-Itw|4qvtO$C3qvbqHVPK|P7AjHf;RGsBqS<ICY%<6(8#IH+LEP=|9<tJlLRD!Ar@=7ndc#iCF2fl$C~8gC6K$g{PFS(lwT)r|`NH*?z#fS`L7z&p4-Tg1Ls~7Rn7kiCC2R#ek|`Br9(exOI`U}=VUd@$iekEb5R1$#WLupjF&SA4Vs<`K*4Sk1^MFbLP&p4L%gi|Zziil)m)s?2(zrU|BEfTXW1>zHYclY==(B`b8r$(8;plJZx0F%hta5D=HbP~pekGILkcsxWWYScGDA-lsCr>MgPi7+$XS^0$p7A6AW*+u;Vz@%{;3a?#$U6N>z!0Lqmw<Hpke=$|E~EEMyjc0l>8}_N+`IRg-?kNn2H`7;1!;G_?qB_!(gqSQxISd0nmE-cUA+FJE46-^q-l;3RS~>{P%j$+QogYTkgYXnxn_`eC&KFBnqW?}xCJb=7iKmtPTC6LZaaJE)Uf{gh^k}~=4y~udUl8nl0++UQ6n!#<lq*<XxqZcFI3Q!mts$^+Rm_!TkMozN1twq25Ttd6*}063Q-Civ2+cmx!2AD5C>M*ELdhxBrHfA1@IQRxz7!x7iCC7I?@w4%r(-YPVAp1Kaj#w3-`%|@qFgI9xf+~y($GNU^mSwGx#N?FuoRW#gIc(JCcv9(x2M8qQb<kl8aASRUL>V3l&v94!0wV$-)UrAeL~3!glDJ-~<8zxyea0h{Ou-$b8u&?jS`myt7gES^14!EQ=A%WT$hm56ow>fQt$Rr%0Fr&PYu@1lw6ShlI{u0vk!Qca<h~Gq5K9Wl%YkzCwZ8$=N{0Q3nieEW3+O0=1W+WbMWk@^dZ2oYWcsY2Y&MHIhrg$GxdeS&%&cSER;yiG9g4Up4!{X94U6(iwT8h1vvK3ZwN57@R{zsdGdN0YCTmS6QW@?4Sp45&{KH;!{a7thqi22M-gY(p6F@hlKh<anjWAt8k=Wig+4NgqY|Z1F7n>4t@n9U{!y-XRZg|I7R?!PSY{L_8{SwvAbECbTbCe@lQ}=lH2(#Ri6-|sv?lMX<o04NV!&6Z${}UGNevljS+rajL74Om=U?t4us&c8w67|`%$A-6sQSkdcI@s@0k{591A`@voU*(F!kDPtI7nbB}Uzcl_BuLExoFGG^?Bf1|S>>L&-bU#P-Z;vV?p@UBoK@`LznrNWMy)ovQ0Ho3U4F?l#|G2Pz9RX-*a~czJFMWcuo;!s=Cd&`SbLPsW0_%k8??FDZRQ4hLy@oD4VjYxX!Atx`K5?DWVM4VqyR;x<b`LC>tpO$ScEZ>1h8DsSH|E*k10OcqE-ix8z-Ow=J^H4^-)aL?DSRy<TZm~LT_C|yyL6ySx=$J&G%@r`1ov|gUT9J2#g^WNH2^9h=#4E`BHEls_90~&DeYZRQ!1rxATjweYQ4<Zw2GYdFkg{CHgBXt5v^G-`D5ItH@-~8&VT5maMJN9rCC5N%`DQ561LQ@90P=*M=n<!zKZ%>WSwXMpJc7#fX<<jG-u<|seE*<LZb$YMPeA;@2-m^SYfNmr835~kY_z9@h62s~1{$2MWmJ<vCpjf0Q*#VJc)mnrwl8gqWFcm8Bns}XXWieAE(rHGIOV$UKugT*yff)jeceJ{#OCch*wf2r=5Wu*=tvH<e*6J@MWW|e{B@RJvEl}hj3wRl-1X{P-Td{_ZLW2C!xqAA8BO$?S6|H6_K`1ku4zWoJ4PwcdhbdkYl*!&!aHtdQLi%V#b~46gmW|(y$Uz-#@cIJ42eQZv4Lj=1vw^Z;ccOJMVT$8F6!?P&o77w2fJ;a7ynd3<wrDk_K3ltSp-^f9Wt5k>07L8EH77RicyPWpCuq{{D9pjRI*b`}c4K5-vS2o+M&WCN0p*kk1D(rb>n%)JW*I1ZJt!Y83I^eehV7wgHR2X!h}yXGdf5zySp^@WSPIsetPM;Y5(OPiaA*V$YAxMCzLxes^SxSzT|7JBS|OB~vd^n>4txk3dU|dT2DF3KZ1T^#ETwkA$YSjPMTru#6KA5{MVmrj)4X0rOH~SQ;DpN5<21Y$K8zYlfw<<4@}5G$e!%=y3Dg3`T4v-ozF9l@AdFMdy(r>2Bc7oO+mM+yd*w9U0q$DKG*{x=3yp6W(;z*7FC2U;V3{<tkzI{~obX-|MuhUR;JXkwsKbx&F+o?Crz0G6-3Ui#2L@<fkyi{|Bn~jWV~ufR{H|3?i3W|$o2|1*K*PLUM1-7iUq-y!VeBG7o0<lBh<VqQr(gG^^nlBpkWlez*@#)w9wCmNN~be;HJk5i1XIDp2c>*cVXc`8tzAeVjI5XxtQ!@HC%gv`Ol2Sf5E#*0u1@}PYWzK!02rs&(=8E_X4@S%u?u>=i(Jecs*`cS*pO!r#YyQEcTBz%Lu5kmM7JHUvir$KYNYtaj;qEMa7az-qDlQ18U2dkVWh3mAvmFha<z~pGqF`slBX0^-Zlx&{y5oj7B94*IQ#Shyj>_na19T?Z)#B?Q=50`A|W&CXDlbjI<2@jV=+$MY+Y(F^KKWwm2%_iUr{w*wKLt~GkYtb6VhzcA&RYa11jc!(A6%=ef{2qkebqjC>>C5gM4UVM{J{$kj}^fEVbe*R=z0;+&;+Q!b7a-4dIwmI>UbMP#88iahaFGa#IwXjEb(7L)HF8&fuva$DBV>Bpq?dR*o`5+|wN)s~UY=i;>2f&(#`62>8J*3NZS}tTsC0T8k1R)~bGtC{>APKzSsTv+ae)+9&v9HOf4*Wld>F(+<sn-45iMN*UjN$OpSU+$Ll*5TZqY45!P;dvc5t3Ie0;hfnpq{P5Knb2%2w=9)9yJKYv~@RCti`eI^RifuBdY*#ZnSvP2-wT&p4M028RJ{3Q4a9||1<aJQ1CXI>Nd4VV3!9brxM+3e967~t_)}y-|C-;X$7|+%V8XUzYL!5G5*t$_%0v^oHtd96hcv60eREZ1&d_7O2ruLtKF4Vbmtdv8RD{4cDQAl5b#r?kH97m>Z;Zj@)9n3|~wB)NCsdCbL5#W$X*E3v(Zck=PSkBhbED=caOeJB!FBV~*TFxq^*WO3HWOn-ST;)cL?<4Z)AkC!`c4}q8Xpk2G;vba?rv|VFkHDsn0!GH}um|u~C6RAY{0ee##C)_%klpZOK)F;3R0N7-Bk0AHJK6}F^x$b5Uv#u0W)cUi6UceHNGHsTp*C3A<tv`oT1FocZ8D8ggzX^%0Lo*`;&ewS=Q#}at7OfC)5s=4*EN0sJ2T@)jYY@vFkl)FR*iCRl|OX=Q2QJ(=w?Z-gDqjZ6cthzwYhY+1h{r5#{F>`v=WU7TLnBA4@09X09$ghzL^Qgv49n%F(~_={txQ8jaC')))
_EXECUTOR = make_agent({0:_EFFECTIVE},dead_stock=False)
def agent(obs,config=None):
    return _EXECUTOR(obs,config)
agent.telemetry = _EXECUTOR.chassis.diagnostics
