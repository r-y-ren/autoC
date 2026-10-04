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

# Modified 2026-09-22: public Vadim Vasilenko episode 111903848 action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode('c%1EB(T*HPa{QNlo(GC6>P~)Jk$Vzxlvd!97S4ho2=EyOjPrx+H^cw#)$UABcV%QmWL6JFOM231xYJ#gm6eql8JYF{|6KjsPe1?T?>}Gt)Av{3-rV0`{cyPY_n-drU;pdji-(W@`03~W`1^l9eE$CGi}!!~@#dS?U*EjBI$XWH`|j%S$q$F8ufKhJ_v-!2cMsox_tovq!+&4=@WcNeHjjS&@~`i|UHve5$^Gq{H|NJZzTm6ZZ*Q-}2Qs$h>-(>6Zy!c*Jr3=Q_pjf)`tf1z@7_N?Z5i2W)W_dGK9qlXetG;mKGjiTZ*E@RB7uE>_08SecV9iu8-4oj_Ws?KcvrS=aTKRX9RJ{YGmxiO9abOC!x+T6(|G=Jd;4m;M&t6q!JLF?E`>du<Ez#xGrlQ`;;`(r@2_6oMB)7M>ib{jdAR!e_RZZlSBK{_0(yD{62c*@;Cdi(s`q#AH!25binI|;P)=ji#82=FpZDMK-^i4Xl7Tzx;d$S@TLw71>v8qSgGWQU%;!NKH}7uW@;8))6_*Cuh2_oaJx2*IS|?sVP6Qc<IN9(|PjB^h=60arv^h<6yD!H9kd-+8o03p8mto<9)H^HTyeF7qPr$~@ppjcYF}?$S(-!LRBq&|@iQArZzEOJ?S)OfPG!<R>o}R?^%||8IX#cu$J&W`F>GozTYhq_lKN3$IpUsYhyEkucU%vbCFSl>sy?*ohU$z6@PT6rx<%i+@uioB$t4(?MR64g8<yt(0^YhUBp+#Q(0dbhZS;6HS-Pq0Gv_c$pXYKu<7baHn(Sg`bj2-gu2Ur&uNuQmu!JT>Th*>V}`8{~rqszAI(gtq|?CJAjK6ylCUnib?$vVK7#{J)YX;{8gg}_LBv6nqRux+@^C*IBuu6!fcrJwtki(73t?#xEUlW9DKHV0tG5CLsulJR8_>?0I{j9GvT#)wBa0s3%0M?uk_Y6Mm2gkMJ5c;50`DAI}N<pV7}kGlf<3~*6X=_(cFr}xa|eJ>9}VLli{A;7#D94F6BW<-I{<{v5r4U1b93`Wi^zF`?ZcrKV*7Q$(F1f0;?Eo7q$k<cty#$J}5m3ra;0Zb;VT;m~-#xqApc+fQE_5=Gv01eZT2&0IHGV<7-Z->DVhNe7p>=2R7;Gv}(vS1TNjPL&4+nevcxPANfZ&tiPJp}aW1C8q()p6AL{OPNkxBq<l(egQ6S2~=y0XYabxGco#Id5l9`C`<8zZCr3nrjE9170GfEYFYi6TrE9mgUg{Udbx^x+iDi{;+ZRwqyG3K>nlO{Xt%iSK=&)8BY`Jo#DBb>sflk;379?kmzUrHilwU_GgZ?7X5XW8<ts|d8pLFK2{JM_I4^zYV_12uD8*9@7yl=k>JorISGpnK!XD|Sp_ck;vgFujy_^^rRD2vsMuJ?UXT#|gq89Pd+Sp!*4$}vmf98t@E<_5V4+zybWSI22PQ@TF^vn5WkII39g~BxoK6A&cCNjlpoIH6*-=}OES9aAoNwp9oOH4sInf|)KTnW_AK?^7N9~*^hy*PTe(L_u!Q~Y5tXRirlz=x4&V<T=&HymxM$e@rqpX}mz2qfC1*DSdIFy+ej3*(%X%M#3A!q)1Z4xv?*+cC=Hm4X22v0Hxxv%k;B~KZky!?#ss6BcPNWvEs-vZ~+M0`gy9<1P?&)uv8O6wL~YlQ?e&r2~zD#$p6$@)wUa9-tU6n7OpcMg~}enNKKX*55vq6B8|Y&^7v4uoEtRO*$l-QYO0LJWF-5GVf;mnQS)X8mvF=K-U^xo~^x6|#W9)yEE#F9YIBQ6}N&1(n>j3cm<}`XbIKxV?0;BLKPw46x`FRjz_`feXes2w5C81uf(uPtUC+T<n~t!QaqL-;-^Q)u#+xZ$~-ruWDx9r<vNd6p$<y7akmz=0AAlQ_il!w$pc4f!l5IEqu-?jn{mC7y!>EbiesDK*A*lJchLVfSctuIsO>>R9dIrIW|JRB{}9)$Msiyd3S-cqwWLmwBj0(voe_uLr1hXTp^5bH&vxGx(SQyu~mbec*>LH$UXfepUgzhmddGBSbaB$o}t@v=wooZ_i$`Pl%7#(n$zReUc0=)K~HB0y%uyc9hzv80<g3d5SSsR&ufmS?~`&605gDHnwd-W9H(j!Jea>=se^QsA~7209~pkR{)L0CeRp^F@So2VyZ2ARn^N2b1Y7Nfa4wHjJ_52gN1=1VR1nwU2~>I5;ID#y$76hXN9Yw0j`Q>%(7Cg+ni8|krjWGtfN;?v;Yf#`A2G%N4LmYF2x;|k{)&S`!{5szGE9IdSxzF!O_f-@@RJDNjmso;F1CsQ1HX)jwK9Ze5+xE4I~Jj}*Lt2RvhYQVl3WZ_UU#0-IIG2lLStw`7|bE+(-{HCiRjCp?X@6`8?h$G4En`9Lt1xe$ue4tC@p3`Hv3@E3*fg>>t>5~{QBM9*EjF()Dd9AAWU=E7U2vcc}^FmUn<bd+TVB@)i+GlS_GD!3*<4NWxSMna=fH(%*qftwg)sq3VM^yE=`VQszLeQ#OlOvXwsIp^y&>WuIpm89c_sClRoaPMHb`^-v+3BXQe4jwh*HrQVR`EzYc*dmAbMqIa*Z6p?s$Bf#7Xi0wl2VAS)-MRDx+j{>ji74i9%%HPV~QOxXDyGeNN3nFQ!)gUyWZGCg)c$srA_<WlP_kAc)nkVMZ)Vtu0d-uxtx3AZp5NYM$H!l%_x>^ydqN~ZkNg5cXq&WI-pw=!0)KCO6UYFsByf*FK#MXu2{1b#;&wIMS((GiNTj};CnHO}xvv{;!RU)i+=Ms<zdIs-SPco|`iMPbH&atgS8TjF+64zqBW3h{(z$(bBdsRCw$(;54R#QGe-GVn`kLD9q6oMc_r#&eEPS7u`}=7r(Slez7{4rhN|C4^*)hO`{`Cjen<O3PZ!w64T(xR%k+2C=N_0B9BqEd>PP#<Py-(1LP$aDflbvXQjHhL4J!wmPPdrzRZ$Sb~BC*a7Lie^LM-XZ`EN#wXqV`t_T?ZsT>Rk+7Gd44v&5`8e}sFtQ(5ICg=<&a)D#X!}y3HBdvl5M<L>1^UA~gx1C>Ih8D*3Z`vff*nZUNZcb>u2arZ9b1z9E~$#JGgh0bm(q)^iDFPDGx9vY*XH>-JPG1|GhOVUWXi))jt{R{;&~MZK#)a-xy;xRxgiV{>c@anq9g>|Uy}AadvxROtBtA-z(z^NZ#v!T)KxS?FiW>_7eYikcwRRFC0ytNRzRv4odQ4~rT`;jNydC<Cl=k%13&<kkWVC@pUpY#UQ*od;A{aEG?0DBLNr)e>Z5;$?gbkmtOeITq*f9BIiulDUsHir&-2Q-P@B1L#^0ueqA5~Y(>zlyrZv$+C<fqE1f+VTHUf_L1CQBB9aq*t?#~yGJA97-_+a_JCb1k)_0|EUh%$lhaY7c4<-x*kB1OVGqWRgBPoFd!!KZ)Xs60`KKg9<rkaKijGIsoCGNZo;6>b>|VPx|%(Ix6Q?}oFR6~j$<#%1A&8Zy+02F#%N_tX^nPGw38D}(hKqS29de##v%G`p2nEdvu-GRQ%UVfOj;i=IX2LG=R!yz6Bg&aPMt=a+YP_qV?1q+-r>!ep>hG-Qgd6^ZYcDKCR3q{MN8`X6j81sFC->4^Fu(Khv$BI9iILGgDfPhq6#sfv!Lao5YcU$#rx)Ua!kh?6gurDBEfZIq8c@96Lac-v}Y)6kcB-*K}Zu!G7H6^W20Lclz<Mw^*rZZS3X@vn~yG5QD^RPCV!qFS8OW>M`%G|DV;ucIA%s4dytF!r%ATl5^TjccYUn{l<sh#;as`M`m@9yb0Fps)r9jM%Oj0=-%Jbik3(+RmWpzITdFtR|SN8K9Hn2_Y>A04U#;y2GYKC*!qH;DEcWRI!kSN-t|oPN%)snpP2bgQNK)&R=kDb{-a`i$wB)aG))oD>&!WMJO4wHWI*AipKMr)JQre87xa-<Xp~nZn*{aci1kUKQ8Q!V4p)A*$`o_akM6}J<@tC`&XMBa}oLvrOU9Mf(FIJ{Y2;r*ZB&DJ`)J)3U_`)#+Y?`o*)i2ia%=10N_5F_upmtoDyP1X_J!vg-tZaJ`L7|Tf<R?B-i5r{ZKbQVYsr^&xj4f7sDC?L2Nk0z^ta90tIF;Da#%D+Oh*&qo8gZQUgRR(Cj5_6KvUz7Y#mp_RPvUfg}boXV^Y*Oa<!Ne51rTTpzb1NgV(O4m|@uNT@=pN@d~%=nk;(z}uw)tZEyWfg1Q3q(@o54OEp}^MsfCNg#3p2g?oshB@0qq*9}BVz_w0Zt>#s(B#-t+DKu$(}w}<iJXfj;7Ehr0y{D~aXCt!oZ!-Tqv{0qsDw_**2sy{zmiQu(^5W>3zK0_p$t0}_XUIInOg<4E-Ks6Sba8%iLnfKF>v(MU^o)kIk1&x2H%(0hqOZjkqk}u@NN}zTO5gFty;Y_D~&Z;)GeNNAoQ$){0ue^!4Vv#N9ni~sb%s*As=5xcwP+qgaSZi=p#d3&6&oCD7rr$q{FI^F`8Ango?zU?214V5V25VKD23~H_$=$gQ5sk75klXG(L>XZ=K>595-MxWm*dnB`}IcZav1vCFCqF*)p^x2xJH(@H$4orC?vzRhv6dw&EU5<HP5PN}!o~sEk8;X_FyQMin6^^5-6ly2V^ad(LKTDsNulV6H<eoj<ZcM07X!qvxS{JglxSe%K+*itZ-Z8o=5|!<@4@)g8!X#~p%`{{9)Dg!~5YJX0FY3@tiv3+CuuZRh|Iw~wz4gaC-ho%HrHWeTa4ZX3^(dmiALFl`cLG)7Pe3YgM_J0XscMcN^}HIrvN(Qfg1`l*uyG}$Uh0pWqQczmwgcZ~~JUk3{#0p2g8+JGlyBHB-XaQald_mCu5K_;IDrJkP9&N(p$$QWBRfLKonDtko<8oU=$VB~dSFA;cHGcb<U8To&#qOCf;UlYrzT>w*rb#{3U6xnI_KNEAF^)y9EVDvxEI)qPmhz%pp6a1V>;?LvA;{`U6&;g*KVCSqVDji=AwNS-CnZ79hS}|7$y(xviD$^n<ZU!4QyPw1*^KTn0IAK$~AmG7)Y+l{2BF(ipYsw`vuZy36LhZUyiV=omiY6JGqP6KjTj#2vAM03k{Rl1QN_5TG3}`Hn-_xV>7P%D-{{5Q0e|k)!442>@)M;-%4rf%SEJ~A3tBNcc7`M)F4$%e+oMqbEor{Py1|hD@x(bYR5XId3Svp1w>_9_PEqR6tC$4z~=)jy9G-wz+vO0HJ1df~raakNKWst$t9}0=VQd^A?cUC^s6EUwTD~F?dU{zoN5E<FNJW^<4D{uyJ7Xz=&A|pQJN&_C2fdE)EHaaFwnUhfn`ysSjV+pVhu|GQ1z;;wb>XnX}iE__C=s}fvIUfeK0X<w0n8NzpzOcXiG+9y-4?pSP<I^?~GHt``a{(4OfHB`tzF*vO%Gxq{bxL-|pLKmY6k>Twd0-sac4{9CP5AuE=GFNMayzWjX*tfodK-fW6r>q-x5>kyw-msPs9ZD{A$8T5G~I%p8}?s2MRqd^3l^81yTmIUI0g)%eYA#?muW<0_CYwj3*!@=yb$9>mh>BJF4|9{35{xXn$h@7?JyLOMb9kdy9Y*N?+!|UXWrfjjdfu#qUGfd4WojUKyN=RqCTkTx=^X(?D6iEswyM|ZBE`}cWe5V-gmo&*=C;Ex{(GOMnN^7yypid;)6*r!x+15{4VuBPSp>K#{mO}@dDb?r~DNP3|0`(+*p=J3@{I1fM_TT<OlvLo-|z(18r}<sz9Haevqo%HSp~~9l&l0-iNpK#y^9Dz5VjbZ8^%4=P%^mGPi;B^R`eMsQ|6(mM(^TY}?FiZ)RX{htp1)mF;N%{*%vED;)YFHv7qh-d)?vrUV}i##o55M{jB6g-8l_)KJyq&fpC^r2pkKc}$TKGM&&QhxK-``_6)Ogi94YYhFzw2k$nVh!BZ?WfqtmaK{I{pfU>-+qmH{D3VEcL2Sv;)4dXKrQ!?o__EwCLH;*=_-W`X!n%HrHVs-QLVb{5iV-ORju^}ogAStkpCgySTLo*67`k1^41sB9UDg{hNp+tn`Uxe~L%t7WX&TyA-Vbq%fOEuIs5@5b#vKM08gEm-pJ;_wvj-N&*q2JPOt_$ClPIT3lN4>bm?RwKWY+?V0CM;6rlbFe?7W5+3GBjZWD5kSJUK+Id8scBOK)c*%upq~!aGS)ax9rwf}ni_uI$EiQM)%&UCn;$@koM*iNEF)G6Cyjr49|0<)A}7h#Yz}7n2GZCQQ1q<X}vQDInR7CL5B)r??U6FjL^5tT6%8d)&YgPvs@QPG6W1Q~BJB47y6pL%g-O&qQ%uBoM%m5}PI^z>?VWYU(`Wr99t`G=}f0Rv|_7E&FIY{v?f=orDs&$%>&$-abofqLye`3K;tY`u40{8}Z2Q$}Dx<TZft+vt8z~eR$;oi1J%xQH4{fe+Lav%{+LAh)JkZE4GHJVocJM3brNwNdX}2iP>o!&0LxI``ud%%-Ck>)5;#NdKQQIssIqRCAc7Uc_ZzwnW$w<WyY-XNFpYLU9~sZXV&d!)E@|1S&&T0@R<2ntNukF_rqH35pH6L3~MjY_sTK4pEffoQn|ABWYNRvmxgu2e2C!q9muRtyII7zE(|n5?lp&Cs-^Dxac=ln(WqfkxDrFF!;@#zB*c<JhQsnmlx4#bIR>gD9B^}gznz6HKXr-&QoBS=cwj-SXYh!%gw7Ok0tuGFfh(Kh<a2bK8cex_DGh`+o-KW#oS5s>5c*gPl5HJzLCRd16}?(1%o+L|f(oNN<*5$6L>OCk&@|)$t)o2Q*wGBQHzm*mQ+&iUuuqwN_6ue-Xw#>~(DwE$%NX;w#@WzG@+YLDEoVn^i9I3~RsT+z3%@R90YPvDatNrr1i>tK%CB^Rh)MK{MTF(Gl#MX>(>ou(nk1CSq8!?+kvkulb&;Pubi?d!TEV{9`Z8(r^(JE^Yz)@Y2pA&2naPC+RA7_CqZ#sBDqsR<eJDnS`~%WId4SMV!BB$*=3X8P;;~W%kYe94N|a$2N~z~v%ZE^F7Xa-uu!G<Ik){3iATN0>5J*)KIZPPOW^a5Kg!d{Dr|>Z8^jdr!PJ1Y-mte~wjsf?|bh&8_8fJaNO#GF@IJ{DDvXD*&H(2aC)&LXMCnN8siXSi9=KyUmQ|VnA4@<?QmHJqf;oJnpioi4BIs}rcL;$XU5rN8<aik0hdYnKIb(z{@0ZkVxz5;BuUHCoM;G|st*?M-Xz_o$4C=AZL>^ue%q&E!@CL;JU!~3C^M8&|uZATMx%YJEmkNDH%t*~AngVQ$_DS-o6y~HZf4||3&f-0P(ZJY@`yuq)l;2nO+MUN`vHy?8t*u8L?k%Sob1p;dd|J1_NsKaJMXGfTcx12|#S}k&(gW~k^BrDaR{Y{4%t!}5qoQO=js{Ug<NO-c8MiT3!W=~^T@1HD;Oh$@=iX18Lf<5fwFv!0#;2Wu>4z*RV<qN$yWwA#ivs<Y50qaNzbAtVZGwI#ysd!-(15eq0(nW(#Fb>8huzrvlcWQwc<z^Oxvso)Rq0u`1neW4?82eIMKv$8(5n~ltcq14)l6aQ>c}wGD(q*fRg1`|m>p+1fq3FE4ns$$2hK_O%qm<DZ1b#_5wTfQjfFdS7mnbpNhEyOOOyn?5GTfu$(r`rK(?>_Zd5*rk&eo~Rz?p|TDqU%=H|MEM#X(#NL0{)JPl|uw7YXpzG&1%Q(=DLOlrkZNWeiSb``}^LsEAVW7qh6cs4D}PyBr%8OacS|IFtO~Wrtv;xlA}L(mQyiCm|aR1nx(?KA07B`%#m^saV&%8Z;#mF`&59Ojp+66vameF@XFHJYy<-V4QX}Mz5?|9y41LXi>p6Vu_QvTdd>T28t7z<tT=}RqpwUdp?VtvRD&(x12<>>>+*FfqgAl>^#j^Xj9>K`hm*x=g09CTjKGP!bc`WeH>Vn9&lcx>H+}n)$1=)ExTBWq2Ot(bsNyTjw9B)fnLEb(%lo&0~>~;D0G}ar`&oNazxBBxl|dC+4IChghg>(wdj(j2n6j~8{U>dMMKIqG2_B%VoO+sCeoaVl-Uz-Jf<yjsqQ*3m%y*_wgYN={`=F^5V0Mi%*(h>+h~0x9ZRwfW2~_LY7Lr%Sp$Igsh&$0T~cU|-Uq3b<|0g*N1^;W_c!g@C?~i}o<w%MsEKApWd$yk0i9emHSD&Jw6A6Ac>b~_w~t+ct^#hG2<+q8L1Pog!hJ2<aXiU<#elKH2~LW1ZPW{yJv)<I(5Y&YUu+Z@VnqZ@_f!nOt!!sTo{7K!Wi^8yBj_s6>Gsa7MM6cN%Vm+kfxL{O<Gl>+hQ|#k)UP%P=5|4oV?{(}lKp_K%i2%tLAstg1A_=Bt}@zmO@OX_veva)vuhO<0&m}URi!QS(#)IboonG|83-UaUqT_0Jt+~2wDZl1l%l@@0w8of;Z{@0u1Uk7>5e4~O@QT#c3Udx;w3tbVKoFV`KWS+>x|(Vh5qG10dyo9l|rLc3Y0Q$X=fdop{rmk<Xwc+Is-IqOeO5k-$p=mnr!7DDpC7U0q6QB{Hj2<W${7$sNY5%)suiwAs9b#w65@GCVRp{As^1Vg<<2w=tCT)9gbc&8QiyLH#BHLq90S~AEu^iuKp+c5*$Z)eHC*=*OwM`(JqhDP9a>M`eO2gvcP98oZ59zu?(VlORnI*T&$79E)_r0QDV_UiE0Fo58Yj&8eU2RY;ui^=$fD4V_@Qzg@7n_dZEi_{lwK*MJ^kqS;v(uWyB3da!?)O`_XEi!HzQEz`cIlETzG26KyR_ZnkJEnjdKoJsdn?Fs248%3$<x8audU{00t((I*uZ#*<m+o-1WU>d0Xmz;6_!eA0wuwoky4g|2yzC>Y?JnU%*t3tJ3&b)S2xKrDciL_yY6jWTlqkQRzDB1bkHXu#7u#N@)O;K(cQB#^TqcGC1wMZJPk&5;mtmeyTG;)?7QMF}WF!kgfpg(dWHV0_1#cS2xYKdm59w>^L}pU;~@RZenZm>1NZ5cJMglTtSbe3j-ztDMM4vE%k%<x3L8RrNwly&0@@6q^cVVvw@b>M>>&^QopxD)}JrsP(<&A3YvbrY7ZOZ9p@|_=Z?|+Sh284n5PbjEUVr2~FTqVJnbUKe~rV<ixsh1VSJ#217;eNQ(u7Px3ul|3IHfk1=oI>=nI5*VpHJbiwHi1S2x9kw8Y=tHiod$Ppx`P_tjE0By7=A~YtB?J<-OV28}+t|+D503qerIVQx-lJQP45+f3o3A*E8vqOxy)LT{XPy_2>Myyc)Otc^*-?<{F1c4$b(^#0}sa|1R8jiNH{UMVNWB{CakGP49BAJX5Sp{}gqprUF+}tIEeby|BfiPbZs5obH93l7pN65|t$5J??Nv1Llq1gd!s`UU;vkK&#*ZDFWi<@|xngI_hAY}&`a*wI$Hps|JNM#6C2YNZQ^hmOXi;g@H2Bp?<J{L8@wGF0-T0FD5sc;^vwG<3kRow)<$+9#OcS2M1x-#XHsWFTWFr+QrQ<#B;W@?-#HW*&z(U1OL!98;j2KaJc`cb$o@4_S`yTEIALQ)anVE~SgkQCZEe<ZXc8*xzFX~d)yPy^%VbjS^OJP8{L8ak7Ew8O1)b`^Ve-pB}fx-l)-5@yRD{1vBtY5I`u9!cGR*W6{!Aikg`#xuQeNytfgrS%@rbGhI+lZ>Si4a>>76MZzniJ%Zbv&LXM)a;}t-W!rTc66N}ntIZrr3Fv>(_D5ln=aDPjCsUR6KMUa?*H00f4WlQSppkaq1Y-zB_dR)526iPlc85`JGqB}yuEt|*w<i1-8Ln1v1obAGz~}+#{$%+yq}T4aTMBi3O0N^M^1^B6RQiR;jBjPW3L^akc;_K;|z?1P#F?A%&!XA@S+u$;z}wib*)r1fiL)NdV)|A*=HDyshwnuq?y9P>;EG=63Njk`>Vo5KzAi11jNnfKrm4@2hh^m;{Oz3B98qy7%D|8Qx%|--XAjB1syurJ)u7gPbe?^QkH&4p3o)gw`7Eupkqv_vOTf`JBXC?d$i*Z4HjL398{_rD}omcNdkv<cE9ZU19OEN{g;cSYh+{10(p+fmg{3^UcO6UXB(Py2|kJ_#h=&_Q6<>DOhH{%N4(3}uZQ9QgdyYxd{wv|8@S|SRYj&<t45C<Uf%(>K2WonvKrv|`fY(cKi06DbTQ?bw`;HNOxG3bof1Im^*09(0>QL9yULIH^^`^;v3_rh%~qtEv37oB<T(}iSM|_VbQX>|I<~3cI!!Z6D8Run(s*cd@(~s_^yypY2pTOEn(W|733WjDO7&})lg9!BN2H|6=-%y`LPHgXmIQ@XdaK0&UlBlg0BHB%FtfWv;IW%`ip+N>oQxJZ7#rt-3hZ^&V0yTe0gRq1bcdkCuQFxFEY+^3sZdVR25v$S)DxvAtF)=vPM{c~iq0xiBT4?#G+&G}vL_TQPm8g1vDVqV5V=KO3jCwgZOeZ}c1WdF64>R!SqNc&gRnHJpAFXzGEj_sRfhw72$7uL{OvR*6Y33%K}4)9+^2)mg}_FcUkC!={uZMyu`QL9uQk?<*Z7o!!tKq5&xt6NH|aoD5;Ld<B*2Fh+)UPHwU;OCHabm|!!O`8OL``h?PL($TlQd%F~oc>GpYnjOU>!-AcP*Nes7Yh&d>?@pkma*9Ahqa^N#ys9ss&G{6<L?@QG6ud|S#>*x)Q9SYf_Ybed&2GSO8V;rE=yh$4_c8>(E&=dQjdRJ_V2<kxTeLWn^udkDsWSY+Zdvh>HyguA`*JTe7q9)v=}Xo5!e;|_Qd%P%^#Z4(vFITNLvqRri9r@Z32%DQZIV6}2d9eYIO%O=ixRq<$PH}t-7?VQ#;T4EdG+6sEbd<157vvPm~Mu@}zRm$qtJLM7ESu=(ywj)y%z8P3-6rgHHPtK)9J)7o5ot}h1sr`6T-7317;<~JZlESfQfbY-Iyt6K=qRJ<416I3orZ)Q|s2%CZ(&(Rrj!ZA`go{{ZNCi*B=S1<`*A65bcBIcWNW#9m(4`jAWL)qZoeH2Yc@IWRlt+MuV30S-6FC#AusN;HD#|yQr$^BQlH3L;u0v1U^1Z6eb4a^V{;G(f!KP1L#}5In3Rr^PlxK8<k(`uLOAvn75+DfMO_1pHF3ILHHy>Sx0*P_&LN5(Mqiu=%%m`AG?u%qJ&hvW0ZpvE7<+&dDXUB3)67gjFjsuf>kd$QoScAcazs+iSc3><O5<nEKX0RFOaP5dP@qJ3`X!x9H?Cr2sHtFkbg(jt7Q7DtosnoiRbp@xX2(07|`nMtr9XCSgt6kHCJRfQ>zOd<6J~H3BElv|LinJKO<G%6Oi*4Ey-m%7oLKWTVu-(*htj=YKCmod6=XGhy^ejC}3ciPenvN}-<V=2J$WxI5<#(r<xkc`IVWv(4Cvd>n=n~tyX2+%tBfz0Z)w(z#-7hpbZPAD(0_~Hz?lzJtwQ*A2`WhW>kV#&A^N{A1ye9Uzan)PNGS9C8Fm9e@<(?$6=VqRn=|<V7j=PB5)2_fZl*bhwROSXu>>V3EVBWB5y%bF!>3lXH-LOoZdlfWcLNuY<?mqGgb_FJf(z1#^)sLWkFP1?Rc}YIe(wqBx!_e(ns+5pQ-3CrpS>_(_oClCIH(5}o0481GE$oZhahIMEoY1ieJR|%5stHO%jB)%^k+Ta+HGuVVvV7=(oI$CH7P)+{NrnRisugdF^yg#6WjUJDNQ6vO_)#p$0}W_)t5>sIOcq-8U%K3y9+F_=M_p_udy=CgvRZH`5*zGUdA44OWx^t|0AG2``8uMug!U5yHvu?N*e4X;JCYEb!|5D@4XFa>Dyye+vBOw64K{3sZf2^QKB1Bo@`ba(J3g9XKiG20sqvGPDleRv@2%xl0kRBXlWf)Ly<KGV9gC`-7--kYrfBxeR<+Kw__0_X7<M|pz9$w3`W&$C9aHkbqQ?rJXM~WTcCwN`d~z0RSR2uOm`lWtfa_JDP_Td*f#;hF!_SJ@d(}wG>vHc<uPf@K$4xV(*%0i`9@rYh)&Nqg6*+?T4VIn=psn)kf@;7v>bilG5_(7Vnlv8RG9Z2`7WeaC)YG+^bl5Z^`x1uk90ggY!g2BMmuKm`Y9SQ?PnoGA{fEHh%XgZ`4K-UyDE)Jf70b9i8EUh~)WR|uMPX)anaRkyPcq+MEKYIT0CC)sW>hTe!9QK7^LMzI%=1~8H%GedoUV(k>=oDG0#H)mt2r(d;`|t|K!Ucw9C!sDL$=6RYw)NjU8bZ0aWcy6rifpGDvkM#k<YQ1@>3#-J5?2KS48s@bOnZt`BjCiu>l+A6F+H9A+f1e5;sCqNM=hKQIT!rlB<C7+MKF2CUdbiQ=#=syS7ip;KGbqeoB=jMygbO>J)`ltnRH5`m&oF&r7=rg|QTo5&C+32%DE*7!5dlfx%D$&WORBH}5B5TWtU;yixwI*hQ`0L}y?0#?csL84Asr_4W(Sj>~#yVHZtj?^UiMy7VCDM>MM0wJ(yOzuTR7(r=rIPZoHK&0-m$Lf*;sUlEfYEidIxG}2(1o=|4LPva_)aLSG7UGHB_k@irbPKmSH2%i?`9bEC8$Wht~G<KwWLaw$k9I}XhF%QilkB9v9`U$`>;ZeXE$J7%cA_KK1JikN<Ke-V*P^g0;PDZeaa=3h-;$t8MYJ~rN9&?AqkVWu9{z&TQJ~GY(5`Zbn7rjc-D$tM8k=g>@-sYawWo-+tiewUQDd_x26OHl=L*rPFWTK*ddf$8LLp!%B>utE|jIpyk{@2od()kxa-s`_Q*`q&=N`|Cobc{U$A)yX1{RfqmcI1NotOg`>Q%o#dpZcV5Xw;s<^Hj5JozD!PX#@yH%RIH>3?8aEO_$#z&N|uib!N%xaU6aHQ*=qz=AJ%<McVXQK?f2ilA(@GR!YIy5(7`|3vp%Ewc54Yo;<n_Ryl<@_7pG=Ikc(5<7gMDinue{{|X3W0_3$!8Mv4w8W!5vr0U6S;D%?<HmRrEH+SE}Z=XP~?U%>Ear@=j<=uR}#7x_-kEyTiV^2`!v#hH6@t=&Yqj8_ckb?;y-IMc&P{~0;cQ;Et{O-jHKmmxFP{9()`0quu9vncU;nG)s$aS^rff54|8h`bNRH30Yus<s4Kg4PS!BnmuQ1KfSEV<xI1aylks`$wQT7H9~W#MV>X!^a1^@slh6F_5J')))
_DEMO_IMPL = make_agent({0: _DEMO_TAPE})
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
