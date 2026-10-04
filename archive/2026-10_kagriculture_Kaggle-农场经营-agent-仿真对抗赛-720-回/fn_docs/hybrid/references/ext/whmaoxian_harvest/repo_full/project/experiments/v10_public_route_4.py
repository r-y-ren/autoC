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

import base64,json,zlib
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%0o`U2j}Rj{Prs?uS^iGtRy#wk9z~u>x5hW7aT&05gLH7PAl8eOt_bUysy%zj%1gA?vo2ED#`#miyi+7K=q59<o0E@5SGL{^cKk`{m-_K3@EI{qEhxr^Cg6{QO^k{qN6TeE#^4pMUw!zx~hW&mS+oegBuAuHU}-;rjOCaPjKy!^Pp*r^D0NKi=QHe*fy>^Y<UVzq$VW{}-P={qwMT^qW_IdjI3%hsjIc-Q3>Jk9mB-_iyfRF2n~iw(0A4-{0JP9>LXiXy3knbNl+I&vSox|M;|NWQ$QBfBX1Q{^k7g`0w~sw-UR(eszNc_VMEF-TlM&kMl;KKHR)}xDfBk)-8_WG>PLsxLOV5=~aithj|zqvF<dUKi=HDUa!%1`QTtq!Zeq{9?tPqOO@HaDT?AS?X-^<udbtT{`Km2|C;CF;)k2tySEpI%Mk%Ry#fj05LR$G5INO%ckfp!2WN`35lv7|W2=eJ@CwiS@Ax+|rK4mLS-pLj#<zLZ<KmS>wb-544>$Mx6=h*<pR{=KQI2>7>U~E^hxeVH04EryHEGA`PfySF_TYLb!FX?vtffX1Ngw~FW**I9cpX!evZRgo&CiU+m&&*Iw&c<9oBf3vo_&Y{D8DZ5&iRqENs9`Nq?+x-)4=x>rLhYa78%Iv_*eSS(-Y9Z=ck8H#2A7nk_TCje06twd-Lkyr$64@KfJkp^Y3dhtQ8`68dv{q-thYV?#Il)g->Lpr+<sYIh{4cVOz{_;|xP@AXsWHsW66;LjV?b7EShG^1LYX_z)s9;kaI|pN!;^etmO&+PdN7&sWM@AfO=gPMF?H$EDl_!$kzIoIU{UG$wI!$AVZIe~3b_dyAJVuY0z|-hy6jyphxq3n$s+e|hglt2d%c^UIJtHj7<d<7sXU<3U_j;MbgFr#<g@CQg%_hD)|{!I9q#YH-rgjf@JTj~g)kg%^B!AcG1D?!YX7IQHCS(!O7i>nw@r6&3vD_`E^qW&51pgFDp3*P`>(a+m-zQ&7eju18&ro&t5(lH*%y6_^s3TfrQLH%#LP6R~!(dup^CB_`$&dNe^L<&5RZWQf7R&BXgN(SQKmiROqTGN()&4vw1yoUY5Bn+7BF*2E#w7k9Yhb-?}oeB;f%d$_;;@a@h0{a-A!0PI76Iq|UDe|<dBquYh7>G#+7e`dO2k6?Zfw||CMdILB)6N`VO4uN>)b12S`I(X(%#PG|Ozmhn;$l+Q^#PZ_VNv0jI<@C<+nuTixW>|b9li%sXY)=hC)q4dqPW!wes$ogtfImB+aXWdt%77NKl;`k&HKI(MLFH00H#NoiNG2-+57`l3$sxz2kaI{B0|1V$Ifn-kOtKC|H(R<`^N*G1*b0h{57mBay6W?=CUBJ<mIW|zyDgs!9~Qa^qZ(ifXol)i7dN_j@I0(wywsBlIivJE92Qd{HbDE@bp8k2?rAqhNOgGvO1~Ef>arrJ-XWbFpkt14J`&<Zj{9=fTWrn!;_}_euPdch2i;TW6(DAD-m!K6N?=WV9E$=w=>4xS1**EW*8%reX)JMon{VV#B(8VC;eMVv+zyr;;baX8U9Gi^!-geL86>gij1hDVni(WCdOO4HW8>ayd>SEgPt@Zi4?$t61@>KZ_yAFHA5j3T7iFuXes|@Ofo-GW@Kd6RSLpbSv$PnY!f;H3rLGb*o*UV1l+YN`8gNDqom_-xILW3Kl}w&BJQO5Bn4I1KWNHwOqhnM^4YRWt2~dZ=j#I}FM*ne;mN?>kq_O51u)JMxyH=9g%z&1ijS(oX<9<YzdkMPp(Mm$SX~1;DP+V;kJ0fwN_W_(~TX>N}Z@?01gJGwvncb{nB?bzCG76mBSDZLtONfb+DDTV@C%{4LNJta*PJAr$HSvWJZDUjN5x2cFhMnWOHn+}l6(?bwn5{`{Up45|6w$DKu`nH>49?(8FW7we{XTy$*5uem2;mE~Im0|h*QpE<C8W)ybnIv8mo*wC6GE`LjNEI!w!!?4Oi_@sIpE4gl;m;PUmx!7KL77)MSXm}8dgkHN`Ey195hrYIq8wdo{Rzoi$|fyAyRQ2mHqbm?d!mKh|cHq4(<0EBtoQs8hy>C(C%9hgBDQfZ+oB98p3*D54#E_utZhzRD5o5#1e#`tOtyQEj1@rje~(N8Y{HLX;g=T1rL?wMiicwkK$pc49!GwE$WNFm@Uc9WYbVhjZ>|@BF7FL^*K`97ECZ|TFmiyp#JE{S*21)H_ead6iGadlz==i{D^i$(K0hMzY!do`4XOc38KJ3?~XVJxN>}xAhNEL2Q@lgG{%vbATXjBJg|ZcppD=wyE{T04lX^-3~pRZqP1#+iRxQ2Xi6_<3k<(8IwjCvJgCb?95V<OqSk|w6|nFt8@8NJ`LG7az0q6&sApJoBu~h~arP{!3W2Z8VU=tYTEU8BYyPQ_()n72=y{8Skq>fB^7_C-wLO5@8X_4Q%Tu@n6!r%i()-}|`drOg3xFJtDj=+Kq3Kt<O{7tn=uau~7Fbi87E$+^r!{&~)4=qsBtFiPox4l|(0eSv1CoI?#-}2zdFYe~5Ae@|*xM<W=)wc=O&3Y%SlFG`_F%=U5b%#U4}=Q@4A0H+QxdM1D8wQ%2b@w#65(&CR%!631q*!Zhzsb<F6g^~L?69E1LoT{X|bvrHq9!)AxlJ#01*%Gm<)>xMjDz9yz5x_1!!F$t;Qnliq8_ulc$#f-eeqzQN;=|x@=W>H93d?BKO0M^g7EGLE;?DJmkS`Ck$n!TP&+g0xA%>wAORsmjrdrQ}b|PS?p^BxeOp6OGib*!d|UJuit!^?Plspw6>aq^LYcI5^;jsToR0BK_yY4j|`MDQwOyYT!W<YnbY2xFZ08j+dr*?d(2lvZO3Gs%`NY7j?)NKYW`Vl8cXxO`RJdgdt3(J6lTT10C2xl<T<@%)e``DTRWiw@<bWRTBp)W9#aZEGmIznoCIePOZ1mZgj5s>tVgPEQw|>DC*ZtfOTE}(14s%`<7pl`G<ZQ&hG(j~H01)m5+jE=p-@d2no!T5`YBU8i5=%qf;xQ$j8~JAxvCb{SkG@;-oCYU>Uu@}2M|}M<XZPwDI{>ThNsOM_$QVqkcDI(iK=EFmIouNZR%3MDO%0>Dm&PRZ6gD}<2s}C8Eh?<?&~nK0S5y(`FScC{Be)f1<k$IYna0dKrjt9ehj{_YBLehNt8yz7ziY*i4(yorl9)gCC5gwbq0zPseU^@sOfxWmkx<zk6dPkR{Km26rCzwM4ocV)^PaL9LZ@H=<FWVJam}clW#8kJ(Fw>?xtGCgl<M850I~5Tzg0YT(Gt)8%C@PO%GcG^$w=v5T4k?2|XNf+G2t?FR_fsJtgy>hC;a6{L-!|Mg(Xt$ZkNcy(*xTTzsbj-|jsOfG3u@QT|LB=r4qfarry71gH6KaxHc9O6cv!$-aEjw5{6#sxxS{L5Dq%>HK62zq`A8cN0(kl-ex<#-JbzhJTcJ^ia`xOfPw%lMyB#?U&QLB&#C=7kSgbjbEm4ylxM_!rlVMSr}%4*aA#NTyC49T1aitAV;OcojHo#RoYAS9yT;ll<U<ZnmR4?a%_a%%NJ`v2T>=D5)&63P&|CtBF)v{=i%;$>xVnMZfG`0(#U^SM>6-wxtexT*cwDa9iJRV@RRnwx;vg^r{5d}OJ+mcsM+(13j#fRi~Sv7KD^2x`ZL{%6n4s$(vH;Al>D?bNKX;K#$!Z9rLtDh+iYMJm~x6ZHYz5rr*%Vc7enMl-genZ1VGWuQ#`ADAg`2%77lQz2cu|g9XS}{pteDAIAThMz#JwfiDB^rx7B+ygj>nKM{&tu=K{3M$Y|0r6dHoLY>(yc{llYfp0m@zOHK*7!j8p~LE(Ry_De{a7=&JdruZql0F*;05icoKDY%~u(yns}V8lrxq`)qfp>=)ra)nwF55xstQZlQtD3L^vzYd)FWbF7LhJc#y8h2|D%)p%*E7#6-Twb8K^N@q$E`=CL7c9#wB|u4tq#3MIV4y*)a1z-C+_Bw_*Ifz}8))(qfGGnIaQabp8qd_DBj+P8#<>cuI>bd)QA=38`I3GF<UzeZ2W9C(lM$I>wIkCSzyLq@V%VB2`Cv1{@-V{Wp=XvrFlRLj=775t#S*dQ>_?N&;zF}#eIe#~##57}m$w+cB?_2>0wu`N>i`)jHA^s51mLRjvJzZTYsw(&&nW^7Vw$i@dqk4y?aQ3j6&x4fpGD~GDLz=J&8CK7haH!%R#Zgf)kQyvZXE>TFfC}3SkhU6K$XSC@f$x`#Nblkc#rDj1Y{w=6Jq7ndsz7{tCxNC6_I9uEaaM_6LG>P>6Vu#8a+itLaEYpJkYjm7p^>LjJ|GP45+s3u;g};?Ssl5wuu5=!qfC<#(%M|c|qB={a8>&)1NV*N!0w9Wjt*rn2gk-|L*}#Mu;Qkf0bFnUM+?4>ltq+i#<aXVB9;Y2^~OIl$$<{dub>mcEyg@=oN2`>K*{R#Ibx|VIAQ+nQid+U75b5Bu&nS^7SFuWB`GlmsLV37jX1a{L=`h7&+=wn)FRh5k~LH0Rj^r7;0w;6e~pnE)z{eGmb#Z7SXG-YN|ageV`5kJ@V(2KNT^+MStH+XS=p&A>^ehSGq(2qa%0v+`G8WYEyBlbfkf!40yvZ^NiqD+h1%1-z^FU2z<ba!ZJ|EX^$~3>}CuAi=|>Uy97h5S+~$S%{pbUpihZ)CsA#FOYoUUIttN*X*7OK^@^j!aygzA-+@OrqVK$>XzL2*os}KfV!5SczGXP_PxckCX*_e7Wr;?$+wK^e3LWfUT6jqDvH>PdrkNG(!x?Gi{(1}@5P#7Yx;w00coBk=T+Zz>>{3z8Fr2o01$PDbX2CaMP#1`@!V5?D^tyE}9!4P60ZvnMK@8Y!dE_8DH=WpEca@aJKcQvtLqC(A2CPh8AzIiWT3@_UNf0QmV5GCP0fufH>y<;OX_1@iK!-$YuNLAsnT@Y95sBG1Q%Hfzhsb023}N6S48JXw`Dq}Vp~pLf;430c59GlFYsWtuE7@mW3kf0_hy@RK!vIXW7<R-Xrs}JFe$D;e1Gs>R+*%&JW5q%83%vq>aU5W6?bf{i@L$r5tc+_#=$G@|5~5)>U0N~nP^D;tb+RGRVPuwxF3fHZeQItk%28zz{RXtD(P&8~DDG<s2Eil+_;U%ER`Tj_QaAXGYtV;t$t3!42-dD!xD8u=EySX>17ItG<vJ;{0Ny6k6Ih5s*jVWKs0ndA2GDqxa{#tAU8&ZRBmts0pWQ;>^vnRF7$7ql&_vinJRj;tm#3sK*=+0#d6AtV*=939ej}g3V}10UY{mo8z}>(m+;}E>T$J+2Awn|{^~TFcW*UohaJ)n2fdLD+#|BDD9XyT__7E)_up=c)`li@RS$<}wz)B4^0KBb31|Syfs~AW#T|YA$kD;*Wq$Q)}ZVIIfw2iLT6`0b%<6%Bn?r-6tiU9pZi5K?;Z@Gf?EaEmA=O>%G7*Y;sfLvFFDN^!Fh{8a5rsSPPb++p*_9e&x(p4z_DTVk1@ZFyVH-tj5txIFdQk-DbqnP2OvMx_^ECu*Xv1vmY5vK%8Z|Fdb?1`FE3V63bCa&*}xKCGyBP~~Th=uxJYh_OujijgGNO1?qA{8o8hb(x5CM<*<HsVkKWU~@WCE~1R7@fL4b{nmr;{1YW0GaLrzMOiryE@@&C$?+$A?n@@hsbVVZ5JXV17cU!)w0P}?ip8mKX{xHN{w`AQDus%x$pf$gr?<zI0$>Kt8)i08wbz@>{LKlRn6X|f9aMNRu7>i69|l9-UpbuLe;Yj(N}7tsiMzU`l(ReWX?Ev9@oftl?KNP^5Wa3^DfXV+9Za4A|>!k=sxTt%F>~lO7T)~@TdJlXvTU;D!KXYyQ6V;!c_tHI^tYu0JvN*yTGlcv^o+$TX7<5hb5^-$TZSwbxnr5N*0%*F6rdx&1vCsINqkDmbjvFOVO+6i3)9mlwWe?w<BKGIsv~J1NAyqcX+II;E9!(ijXU`6J3Zf8e7<?iF9wGi_|U&<Ean0gzF=A?xbUNQlRa7Q_WkRDpq4RL9d`xPwHs+eSUfLP~1x(ur%qaYQW3oj^&WsAgZK<<(&kML>A|O3zebCX;iN5wXNi4g7_Gu97W~j<-wdN+SoLtYpTG|mLa$}*VG{PfEEZ&=vS(x7}IK!WV7~&W31l+g~{TMve0O>@w<%{AtTs=%TZ@Z(1@gTrceu9*&eX=&;Zd~#M?T5HrA0vj8=>dtc^HGG`R!fgN+Cm>^Nd2DZUC2#2h!=o0TG06>()_CXk}~E}B`5+dX<RxJ0zV215Uqdn8S+U6TKc2#x^0ku9dc`wnDVBw7wkF?@w16<}}dSF*_XSUk6b^qxVoK=_s3c(fB4Nja*-i-lbftg1pN^V6{aWCcrA==-`HbmSpc8*44D!212P+FHnzf;Jr@Q5H9+1fwbh*6q*>oYLWnt=jL*%N^?hJ8~C;W6Oew^aPA%j8c@^<f@V!D~;MoJ1@IWn4~Zf?q;cftm!Lm)>b-H+b&N-?VK1Xq~L=Wq7R*Du=L;G_B2&Vw*(?XjTW4A8pDCTu9DVS=8_7l=E6k4OyYz|cuQ;lLr`XJlkEjdt<^dzIMPIL0QqiEQV=K%BxS3?I;QSP$lcAfg$HnxB~yy|#?aOP!6%e|b<M8jSt@4EkTyjC4(xSEt0J9q6Fac49RuseK{tK)^Ylrj$b;w`*wHriIN}CD;b3znr(meQw`q=vSL2AhY2hv(crK`7u8afZ`VI#e%lMF#u`#*P=4b)`cUq5kB|2e)mpOE35*+^N>^RoM%Wl`k<&D)@@-N+689mrLTXYVsf(Ln7iRuNPdK<>YP<4=mewgDn=&qZ^S1FT{GQa@7Wa5%|?@+9jqEIez>IrfAW-;?GQ_uEWrc$jl35SmxkTUAcS1k$9YY0KRCYV8PQmz)(FmDQ<{nbg<C;C+8BbXHovn|)cA!hnOkjq^#wedVDwhwv00{K|_0JQ-&R!IaCYEiKb%{9B%w>Ef}41g{O^$uAzo1Aa32OChmy~4L*#ASu65_VvzO>Lnu3dIgP)B$53!8nT89S(y)<K;tm1Mv!TKO>^M_VZRJdW1%43lXet!(Ccoi!h^)3vEhGF<u;mk=~=V5EwC%^bsPiQ*{wV4X~3kk8<k?P;OvF!i}6`y?GNu3GfuLo1$+1&}F*4d-H%9v_dV%d10_tdnem00l*n|bAVQOmMNOEB#bc4s_4~t08=X(u+7<BUIFDYF<VFXH(4mBH;sorJG)+0M={)%I~_QAhD>6G{&ooFO}d3(OyUeizi^2-XFt9-H6Ed7T+$i|og*SQWSrJPbr`9Q;gTu3ht<fbn57)8Wz=+p%_^0}JR^Yoa?ZxeJ$X2b6NvZCb{3MfwFF~2Uc;~02P%Zryns$dB1WXZ=V3NWCS7t+HJZmRNcU{O7Xx{0$JS6^rOU~>@7NcEHCig6E&2sIN6~Y#2K_X;dbN2ddFW#39B=7uByNKH>TomQ`IvGTK*eJP1#0$V(P~C|sPS~DA9XY58a=PvME<Lj4J@~dp)76M6G>}T!Wytjx?Fl6WdR6|DD@~efgCxYL#Zuv<ayO&hvG*mKaSN?5sY7zAVYEQQY*M#YUA(GRE$N&9F7PDQS%HzkrmKEGhA73_?PZ}Zyur5%rdR_%t0KzPKTuR(7{7In7w1gC~o5!fsDwc12{pw&?Rqicv$<i+d`yMkh%p%cje{)QJ8&|SUo@zf9lZKl(N|`E4Qa^gvmjc<WO<BP+-lOF9stQSm}yO{)X!e3F7512*?Z95)EA<FNNo5IUe$0vNSgt9R;Q}-Uo#pf&qt-IqV=&X?c+NN;5YNpwLM~xK7K$K?Lzk@J5S3=Oa%<*U@^Co?|Ich1f>J*wvRQFSI>T2w*KvC-i3;8fmTnx-+3VF@#cLShhwTV!RA+4P{9c2%S|J-eEU|E%2%fU{EFFyl0J|SqyLdYKy`Q1lmr8V1-47Ton`)j*ziLJ+B))*~Ueb<Cuh?f`)doL2-L=cU9KfP9IJoMXhNM^Z_h(3_tc$@NMA`TYcr7#&X5(#!r&s*<EW5G+yPHPnOmSsowprM<T7VP<$H=UFU9y9m8BobHFA5G??NEaL&qac9_N^;s{3)_X(aj<27pmdp9~zEF@YxcB5NbOt=YS%xxfu99dLGNsEH<1prCG>uu_gn{Dr8;auXxE@U(ocJsYSF$QX;$u?lcWXifsHU(|voFtoN<r`cC`-A`sp{un{TbD~@VPlW~UiJ;>Q0N3R6MX_3yUm*AO&_+x*oEhaMaT;h$^(vDj^#rtAQ%XceNsDkOk$hHHajF=h0+gfg&0Oe^44&hpA>(&(No~)<>HGu6D?CP)K3G)msw<yb}OV44cKIzrFC<A_x3kH$I>}iT7{Ro-kO_resWgQ0z&jjCc(s+TVH*%_dQP_h>csOTkbc~HEW>Hcnh49u!O>BhA#R;4r-3WiV4>1rGl`@mO-I|&-?T7VhYq%@t;OOZS%){des<dDs#Qjf-t^Ro6t7IohnnlkZP057J2z!t`OMuq1CJmA?G%655PZd0=pa<TYrugZ)H&S^r=>t*It@sxEInvr=2mBZmS%MisK1m#$*q8nl4LAVr3S(9-tg|lEUAeQ5BIC;VA`*BNdwN12IQrFaixg<T^4JV0|eZ)R>4HR)bF-1uQGVSm8na8@_1WCpF?IQxh?2BJPld0o??2mxN^KIdniq6!Z;Oad`)tHh0kobWnOqK}4eAOogI#O_)WL>IWQQ(~^pI6x@TK?B|kGlor1^jG|IQ9_pe_Q(&hYfl(fZJdUCKT6JwE3~;&nGE{L1_E1VR#wq2wQ~OSwp_~_z>_wa2TBi`zkrR8-K<p?W)ZO?+rFfyhKSBgdBU!ZpCu+d?WC+k1Qo654WLopbnT?R0%M}UtBlEYxk*|3ed)75lenDvkoJusQjwG0`UhbXupD&b<nl4$kX2W%vN#$gXx5Hf^S<=LvaGj)7DLsr;ZOcnCq)TFd)SJY9WtPMSn?+fpP9Gtw?>kFMNf;H4o<(R{q*xAy`a+MHqg<%#O0&_6C=Sr-f$cUeFF-k6J@A8vS#4z`Vkj^?5CbN)wbjN{OOLh3hI6*2(?{okqHdnb9qrrX_)>o5zbX2PDO8(sBL3K7kJiOtf7Y41krK@J8eVg9X|fBv#?bVsEC}jDey1T;789TcJ_#cd)Ve{NFHBqxfe#IqpYbSDw5kw)c1SGo_BXezt9nNztDIa_Je-Qs%3h(G=#IUH{$Fuen4UaAEfj8QP*if9$R@1#*>@k5y42Xq%e`4Eq~@d)$C?C{cAE<JMq{8NT~s4Z=v&;}iY<z~JGJ@<B;a}H_Js{0ZIJl4(m?Q&vCRP?O@h!H8&?<hB2_PoFMZdwwB!1p{5cT%Tda?BRo-Px8Y<O7cGstgv~{0$Op#>=3@Y4M-&znN1s*a-h;=U&kFmE(rd=WYVA0DhZ&x)J(~c+r1|CkAmo4}>d)Tndx;uGRbK^2b2!c4Ga*KnNWp2Ag4=|wRMf4JSl8Aj1d`eL!n)%jz5^tGuQPfB{1(6n-0VaTgtZH(4?U-OzdLYp-J=x_Y$`Be2GRa^fO|DsS$#FoOo8`q<7DG#&pPgo06f`z{3$UNc6p}<wvqX=9YjVg6+%cv|RuPm4*IGdWOn@$2sD&>Cn%^`lhSJbEg$NliML5o~0-bh2S`Jx(jnQ+Z!haDUOqcHx%1HNanFHuA3KsRR5w0>|7?WrZZp_I(hRe%%_Y3U!j(6SZ@MDnEXWu=f@Fmi60$?MBK03ujQwzti$TK7iGqNQI&)JNtMhc=tj+y3DSOhT6w3&8`z260P0Dv}?!_&@G#CT|rM_3|hdMI+oXUklQ)iaG|i*3?moY^GtwYNKZVQ~-v^<s>116mGPq_m}4J-kd@&6wx~Tm>*$aZz_3q|{I>GfaSvfv)m^;nije<GIt-iM;J*LoER{qei6C*b!xHh1w-zbzPsI>KDVRpJkVMR=Rp|z6;Rukx1Q!zsy6PRiz{(4&GHt@KI=N>VP69`lyt{<<cgqwXzPCXdc)D#nd2hJkJApXiSlGVBpzcjj=LN6iD({DSe`;HH=7TffE@bC_N~cF~#XFvBQWqgL6Cg(J6(btJa{6m22BGJqW)S=+12MQ^0D8YMlrq&Y2hY<)Z5N1WW<kjYE(r7ELFry8FzOk)6=4r^EEi5Q_{1qg~3?Z<3>+Efd0na7nng%!(2kY$F0|4MgD;CKxK=RB@9`LU+o%AV3$E3zqo@s&;0*v{Pa)m}C_tXE(ix+RGbpYfeZCa34ib+vYB0NkhRs!bhppnf>m611A85MUWen70Xko7UXIU&Fhqa);p!k<v<G2#)#D6NuBdA60ZxAyv%C%7OyDYy<5NeiFI1SWPYq+5IfnL=@PnWxz!Z-Ksb|N)YS6AU_jahEtwAr8`t4GU?ok0OU%7v?q9}JD&-!yPTQ;kQ9D54B$1@(bjl!27HF3!vIekU=>DZ^MyZcCgD`H3$ickq0$9b5jM)4MK|Ee<(Dti6w4QEVRqJTO>+yqyxRKnBX{+a$f+0Q`b`n0-cBY@EW4b{B6F+}J%^O)LG+c_Mc&La<eHFP#F;fIG#gSsN46iP;*_NxN=Gib}()``YKrZF59$BHxu$~S}Nv4_N)nKjxoacASV3I&U4d|(ny1Ml|^Svo4d<9X`s3f!;)2A#wYak*d&ei4L`O5X+k?koo0AfkqvdBALTIP_&5)F0+tw`}S$EqL$=5O#;BDZIO-LaK+$Ksx2Aq*L-=_=Mii9pCpu-oL3LK6mEHo+W8e0{CiQgUCQ3p+g`!(5L~0pOQZNRBa@YSD)<QZRdG)3jW)tfH6)6D=WO4X^qTW`Z42KCKZ(<q5#0x@{;>e2lsns4+YT-aP>$%7>@LN&eZ+D0VsXnz`;(xvD!RkWByHj3Jjw!HuHAPMw~uy-Z7^&IF8_QlA`DB{@}8`*?R6xB^WQg(;Qk0C!QfW4NlAi@FSwWN0DMs?nNfth!Ucv_KFnZ}3GTc|AbZxq*ZGO1Tnv(HCbKphc$K-k{>ZfXSK)SI^6*Y(ehWP+`L9cy&ME1zAW}=q~LxKwADV@eCXLgJXB@zk>>4^PLd9cSOOWWL_-3+aMo1F{A$QIE&v~$0eZaesAl`&UD(BgBe+xTnr6R%;>WetjRfV2Qz3E3X$2h;16UuTK9vQ1b|?RJH>s(W!z9DwjB#)idmjYt6#DpF$c+1x8QtdF`vaP;!wf6p`hcHexO?uNBO8OnOf-h`gVN`a4Ahkl0HK_ZV`^;_?lhX#eD$UFsM!w1ZJnucd~#*DCWH^L+Z8J;m|07eCuQfIF)$bG)PJo?1obx^q7ZX0|Q2Q?Au$Rk?@?6B=|;mvnc@ZiUmH52?s8aarhMSfFxowN)GnG@WqCwhopyM(DS6jI1}UJ2Oj-r8A#J(3o(E!)rjmf#bIFH#Ml*8Xik{P90|xFAi5-q=`zy5ohB}*=aZq^=*UNV+1R#}Ek)T{Y`;!G3s3V*etu_jiUUf5C~<jMWmq>KSg8v`mF&5%%x<G0t*bJf60(Dnj#$`f%REQZoxh@Cyg<YfhYTH#DcpzGcxxU?1q3Ph^_wjJJM7ODTiNH7cPO!uv@V#7<^`K=mnsH|0(;RGi+#;%K*yqlzG{pnW)D@{*Yn-`MvF!&CXEGbF0N-(|Ct;qE&S=zx9{KFzW(X6DSLQtUd&Xh3aqu@QCkQ2I%vmin;qk@6vi)2UPqBP$b2AhtV~}`sjAZ#x|_ExdIBJ&N0^w(%4VO24Ek5<^17a@nc%-Vh234B{zf<qHF)y*8ytir)+;R@X3FQXaYS%zHy`n5n(2T|w$X_^)YDP%DFx$;_g5>`mJN61u_zX>?i9+tlGleO7{#@Mutt+NR=HS#K9Ol$?o<#WO{pwfz!9U`(J0>pgbK+dLDr_VF)6&sq28!CE-$d6-Yp}~^5*PsfUzOsf(mxRqiWG%tk@o@=I3+Q7N0%<T1rbEea@9Q{2FvNQC9`%c;qNg8b*nfsK|6x`A1!9l_FAE4WxW(RSExD9yXIcDgVu*Qo&Nm#aHKHNqx!wQIPPI)W6ZaF?2VbRZ>`taU)|YdQ*j~>1M~qgvN^2KjL@W?x&=5koIQnG-6Se4UG$uy{M4Wps0{rjZ9o>X2JvLAZlgT%W5#RbcADZROUml?5yl-vI7u>0A)(9sm9&oKD&Wa8F;2!n@DCl?w4`C6n8a1O`g>!vk0F7CytZFwTlP9PPPbIK@J1$Wc0vUFoivNdeZfw42S>XGVtQrMd9&1#%h;qYE;`n3EWUy(Nkf_%A1n0zAav7VUl)H8TDjW43YVw9@~@?jZEr5vaoSIC`L8jAt}@XsR(^iNhoS1y%@3J(yGOqqc>M_205Y;;1%eNtfp)X8Y#6WM>RjCI9s?SEfyN{4{Br*AZ~}y3M`6F9q9VFrLZ%eNkNy;&hwHl8)DW0GP=y$EtZ2vTJ?zV0KU*S;CJg?^;iZK2rDA@piVlPrC{P<rYw`k1kA)<TE>!tnbMPVS;Z0nm~)^)YyQmTCnL~D3#E7&J<1T^&#acgmXP)sB@qT&KL7G)O1AJ|qaci2TS}Qp;wk%mslfAq6q?i!nfY|aRf-l10XQXl#{)5OYb<(*gk_8kwD>CPgd-pi)&){v9d3y`5x3u;3@vQZNCG-L1^d@7fb%>@J||UMpa$l(<D~sR{8+=W|I4#@S(xs3Zt}-t0HvZJ-_lx<>T}QsE=`J<JL*ZbfRcYJg@Aa<!0&FwVakUDyg3@hl=Gvl8V&_VQIYd>_D)f-Jd_y^G#TWy0tMZ#MUnI<g*!b44*-p*ZL8xWrEL=I4LTQ)`R>$5wBlC0y=cU$a1awlrA|(P!NeOXi83)~Z=QAZW?L?m2qCLba($V*5FtJf^ze8DSu==gHEeWAnF#=Ll|8K4Eb`XfFXNoDrah&yHQ<4={S5l8gDF1Q&tc#xZDFJjSPHX1fJa?iwj=YVR&zo(d)lC=Y;{J^gcFPu5SjE39-ngS>B33T!3xJ)McL}_-C=pjoaFG~PJ^t}g(C4A#ruL959S@;P~;?JVyLh(49$aKrXS$65|7wT@dBBFm1uZJetNEYjuRh*r3cQjTxN>G4)AN?jw+HAO!4-HDFuf$T*X7ks~QtSGN8KDudbyts__;Z9|-j*vvCv1o=JXEwNsVPyZ|{+(8kAhV8{eOkXj6)%;a$<+~WY21fb|~<DC;vr_HpeOZW_q&UFcMBWy}E=Cd8r_%oodc2rb5IhbXz#;h}#j$s99?HE_H;9GMXRB%vW{cz*y>4+09UuBKCVWbC?h8MJmT9{A&{Pch7ke6)')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent
