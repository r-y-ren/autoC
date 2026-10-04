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
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%1EBU5^|`a{Mp*JP*e&QRlZ6xhD~~;tI><31@*21o#XC#`!_^n{of$tDT+h>dMH7$m*IUWg9p^bHmy0`pC@6jEv0s>Ax@j^_O4&{<mK*{^_TSA1*(9xcGFq__tsF<6r*s{)_vMfB)szfB)Nm-GBb+;+v0u{rU3!yYDZrFAf)PZhpKtJo|Jwe*MGk&D)P}?(V<;@w=<b`~SZB^ywdm&7<GF`SZsgnm<fl^5N?GdVS2p3%+}Idvzf`kg+XafB5d|>V5<-`k{UE@!j>?pYP{>_wnIr%gCBhKmP5*L;08M%j56(RQnaXzI=1__`uDee!Ti{_b}<@!~2`tyYHH><dVWYiz7Hq;PD49HpA#&x*12ercsde+y8WR^>#b)exuqKuAffpc3kyYYw<Y8RyMZpiIYAo3iZ>)n@hY5AAXzU;o|$N>znr%hv)uy;_4h<5f|VPB&HpPoaTp{kNq~sc_Ohx)030vMeZ5i+oMh_|3W78xGKpyy}w&V*S+Xr<4OzF=)>jR)h&NTd8zs*H7|Z#MLYuazQ=VA?>jvK*_}A6@K49bddjyQNjy2aL&;s~$A42Zk5(_dkIc8c(8lY+GwlT)dtLHq_zhZAe*wdDwx6OA(N=i<^VLvo>_xg-nTDMPdCnzb+J%-TnxpW@)AXU~CZC9nJHsR2++1H@y}A4OPgl2h@2=nd^L7=s(ww_{oBwrhczb*EL$b2WP3oR<`YE(J%Lzift!9Fq7Yon#V1M~Sg)x*4d9bfwa)s53YaWNUe1m32p51!{&$sVE%ane7b@@1$;|Fi!y!`?Kv+Bk2-qw&jI5OL}DX+lr0>MicCp0dlzXD<)VETB9>D=3aqLUzMI`AHsnT8L?AIteZ$Mek{b4L(>2%{ky=O1|Z;{923F1VFsF|~Ib&$rU!&~}3eEIg^;z&kT19<OmCvqeCjof<JP+v^Gtmt3wy^w;7R1vf{BUe0rwi{n48e+u@(3d{Ms^p^&qv*=xodsO%<=|99EJ$;Jnp(LkSA-0Sz%*fQ@8;IwI;H)&R)JM^n>jYL81#42j7?hN}o9(*44h~i({6jM1WGGetojHd{;EbU1@j=1`drn=j2JHhVgfsEv(F)@OwmgrBrJ}#++_(>Sx0gSDb9H<BR}0$h-H6|e<K^vNPUC4m6H8z@)Wwl4-d=aSH%D~yL}T&Xp+p^u;wnebE}X*4=x7*<6$NRHgy;Z^pcW94^{b7D#Q7Ir)jlotb(Kdw!8<#{D~e&k<Tn6$*!{lMgr*C6)^`A>a?-jzg)dxu4NFm;!#mb^G;tOaufsV)QkamWw@?&|PyI^%xJO8ak5<q99rf(V!bs;cjnauA#`AIg<K_HO0zf@2>FtFCaM)+yYBHyG)Q#?y^5y2;NCHf^jyX?3HR1xThGhlKG#1HEZw=7-u}+RVr3ch*7n32#bcocgv{HgNG$DAVavvvo2fmZ&Ajn1gNCt)ia_mv=@S~j-^2KxV`*yldAZCiLO-v0HU|sTtJ{&0_C(bIxAYn2<A3sc=!`$bqz|?=61HJe5A|A1H7`4qpI1Tck!@m}M>6fW5?SRNu0w;R!w&NVqMVuB8{lSPQm$I{^cp@DZbC4|$p^iTlu=m;shCIlKHXDApqcoC0k@(^%`-Tp(<fsEmC73h<VCBom3e%YZ@BC~le44WXluTP+%dOHWNbIyaZmovW_HMKV4p|Ef4aZA^i?EL08-uOPEV{Nl$USLh5|L<RuJopoi}e3*+Vdvg_xnHfBFi}M@|!v03nbw@aPSZ_!pytxaC8%H06T?=V=E5e)W0glU9mcY;L9VgBv39p1@>de?9}nzY}BW?JYVZ{)2s{t8z&&Hac+;G)IitO2rBc_^aJ&_$eZ02;UGg=0G)kke2kHsa8ZFBh6(#IHFDhY`VvI`Q|`(c3Dkpu)WtUd*7aO()N*`x`BByz3UeSV7V?5_AwMUUImI#i{XT!Bo}}jNYrASXlI$h=><A`v2jVxuuYBFxvlZcowiMFp(3cr_$o)>qMF4wLqPUvlknCiTCOp6@*@Uh|8EU6BxVgFi&sU0Z`xQPLyrQU$l?4D@v5+d7VK5#%43rXnTz8(>3hVVK>(`g>-v%;G^b?kMG#Xy6Dk4PI^v|3*B<&_Z+VyLVxr6o*>mhmiw>anYUl7}3J+bkhmE8E1({d8wmSrjEC!-s&S@v&lZa!S0J|7QD*r(w$Za8q0V|xR|a{)a+ny*Y=Zu{5E-0Ds*0EWA!35AWK_6Mmu-663RL@U}Sr6YkKEb9c>Gp3+95~Wu>${c7W5^Aultc|ty6ktcYkP4MdcaQH#KL;nvdtAmhH;)I&GE7i^!KA)@%r^5}#B)yTc3jJD@1pUDQb1(Adv?v8wv6*>x09{S#zt2RmaTMx-t8jL{3v!nO@>ATq=BwgZZox3Iz`S<CR-;iZ&J~1SL~C4f4~JkT5a_HPUzph`!+uXmECY{oI|%rb-mR&kWdC?O6ArpaeOq)&DT|^W%4x$n+<%G<c<In3GMHk)J~gs_l}S$!MYSEkeg8aZ<VL%;xv@VDjeqphdqy}Vth>}Q3s7d(ns;AO=tn^%P_P(P~*CD8Y;&Yt<Fe&tWzH<FawEbn8gEa3_nARwA6zfIG8plCh*1RkZesL*(i5%oeiqFFt!nyYF)7~x*Y^ZKv{>fU83slZcpCqCA1E;v#Dzu7cl_{!ov<%u^~=3IGHV7)^U+?<JgFaaDx|zP6}@qc%M>c_*YRwJMf}&JJVgF8=(V?u*4ug2G;L|UgBp^bVk<LOea6v2>XE4J8S-Y>lDc)CtOJ*nl3K+Hld!bcpVEnJu*s36c@%eb&dC{)C?MC9iHM*E}|lm{CQ>|Vpz4K`YjHmNqIa5t!%J%@tE(ZfXtQ7$8WwG%CD~UoW5Z$Kvu|-6cm*NmkgX^i_impV`L777Dk%T$jjLVfMF0))}*()HTs?e>LGyS_S2-_6PM`wch`UJ6S#<Xh<f{(QSnBs^Ei1Ki6RU<lb+GbPZ$$`(E}<@kug(R=3U`kxUCWnUDYG<GQd*T6A(Tq8{K4JJFH;8bXfS!yinsQ75VWWuz`y3l{9x-a{u7?LqVgT$3N+lmO>EYM>9(ctax}cCTq*eDE0`{>LL88+T1GUPRDY+s!tnjeebqzt3fnzDlSAbly^tFQShk1!JcJAbNc$kRW-bxkSo$S16{ZFgs89qb+I4t$34kp{qV~YDk8}ko3UZT9gjILCV^I0i~=3U=IcB6V5p@wh7$@h=;9%KwV=N~{tL=p(ia{wlB6WOM`?n+>F|5dsxVcMqrv8*Pm-PnwHayn8P8dgQq@5`2SGH}H5ml|9UmW0JcF8y)S_a+)A65GIWycs&Kg48r21R-rnx;1`nE9pFqeof_-!T&9dIHc_zPn-&|5V89;Lw#Nl*{OyR`<f?9yt=n<n3q85+*Ukz@QavGM$JERW8P4=i#$!ZIX6-R7O9SE_iP=`dQ;fg_#{ShvOyAOpdx>EOD*n*sjs&&S72Xrg)%NXq^@iLA&lkW@-<S+_kS3t{4fII#JljDXF%LNrrY?X%q@yeE1s8y1TM+A&b)lk3u+c||9&i#at(2DN0u7f?XOLp!KbMRzyfU*6perO9E``Y_<fhdL^X$c4U+j@cR@H%J?cRW-=>Q7kwv6ytk&@Y8_=j$oE|S&BsvJ9$U4kow5jO`PDx6AcQjV^=xmp=_D~hf}DL`*&~WW*2aOD5Pk1+bW1IupV;8g<C05QZ!Yk4HUr)a%NNdI5K4*B(%MSnezsogiC{WdCM^8R4-tgHbH{KCbLR3_<UI81SKZda`K6BxCh8I#Xjv44x>3iiKS0GASdB8V-BdWo4?utL6Q~EstPreQQqDPOn5ATp(4U<|3n$FcD<OMLH}9<R{>_pkuTue<UgB04rz_jmN0RS1`VOEd&?bpfn8~df^jlN2{@w|ne3U%d9@CP<M6TDe<XyAWlgiZtd&a&hz=M;%=Po+xRhQSc}l)s2Na`0H(5JEDgoLH-kS^>J4q0koJ=Y~z<}bl(27!)KC2}UBT}(EyIq;6QArYePh+wT04@ZNbbH|E`d9@ixjkB;2%u#M=v1=&QD$r&uQ^_#k`xMy%=uSV!o(&9BCb<smtSq?3!y-eho$t&7un3qH<cq)NJ2osjg0^{tLyG|a_QQ#gDlSUnRdtl1_|y_N>!9I1Kd~(e<xluVSP8+le#PMqylCunzw4W%x_nTes!hmJKdr}r=%2u+gim$KqU+Sk5raU17Q#?c?U9RtaOa5V5kkGB12J6<rlqPaqV!7@m8SWF(KTrh@18hFp{RBx(p6ifumDND#%?Bm5v$;Gs2|Olgfi)d{Q<wJrKr#4(?ThVYOF_F_?!ik0t{&2(~0>FXc1Co+Ctl$=%@$f@En3yEI_oR5V8iOG~f=waRNZ0a;#Zo-4Wmrxz+gG`@SbY8zBm3M<*|FH@l86+R&8A+ll);1Wy$7dakE41Ka(_8|%NN!?8qN22k7!KMiV29`uc<Sa>Po@hIegBmPj03V>AKO+uxE>I0yh%TR>d*3=bs4%F^K9KTK7X@0n6n{>xX;0o-LdQ^Gvy3KIF98W4PD7aVxr5u?*JT0xp+%^HEnx6sZ!zYPlSms}#+9g)C$Z<i<k!|*l-)lDOk|-Ag6L`fE{lrB$T|h69taFDofLqfMF>NhHI6ip#9ll#7%TzvKkdpS5T`L67$i5uK`c^TY*0W*pmKq5+m4U6yT-^eF+@XJgih@kqhK*Z&QDsFdv^Q_RIn453*j_?H8$2TYRFg@06h1TJNiY>W+eDM7aoS}g57_PRfmR%FcWJ328~wuf1~V*_9+O5a4PihS0zTy457&^FKbVN2tmvRn+Kh_R4k-uZUsw$LsBHi#%->4&rMH8v^NCTx%&3o`vw2Q!*n-6c_?uaWllEH5jpkYv^!^g+oSvSbu;G;9`&#o=fI<&=VO6SIdw;Rf)uCGxy_eIGWgsb=LiT>R^fEe2m@sTnf)uC<Moh`b3~>{ydBd}qm5j-O~n;cy4{4?>~L~d)(B)(=p#dg_9T}HJf#A|$8=z8qXi);V9zL#F&1@58V7;7pyenEAi9J(U|u$(wPZszleTFB`N$69i19e`S(b$;uo+6V)eK9N8Z5~-5q=nGXuq58Z%2I5sOP-61N3=yN>Os8iSk6s9IXONTwg}o7z{><ri{?CD9>X{YRpI$UajV6Yq2c4Y|-}wBef#EnD2QKMS-C2o_SENz6^FoqjPNW;NptHI~EP^mAwi3Wz{iR`y-Qe*=#$LGz~@tNCh@x90vdcWhlnFYUAf^WGR6`SR>6=ANzLn{-ilNq|KXv8D03))_hZ%SS1&uV3}x~5mih??3DdNRtr)h+buLCX(-}iD@dC$xtYTP-UUGoqi&AAzuwM?@OjDFexYP5(rsmoYXvD*jH*fch;9lGT1lW>E8ia{A8H|WG#n;;1rfreCBVbXjeBEbh)$q6d?*(h!hRtPD~<ZloS8zaB>9R^NU*(+$bdSXvK~}pv1oFR09Z%*&YJw;$w@f~MShE$#>h!`qaYvfLKDgj#=u~7O3cyNzO#yj7!-<D2nvUp*6fVIjunIgxdL?xspquLwR^xIbWS`%;XyzIj^mPD!;g<G#K3?(cf5bXKz6^Eek)NQ^BFp~?zQiN$9ankER~gI#lRcP!4R7M=P>uQh)yX7$sh<$40qY#%195?%{Tz0I=8J=k_=^@K~bHyTb%qyo8+WWlRm3G-PzqGiV?B2EiD|2Xx|Ebzp3*PAdi%If}ywAG(3ggX5+cQIOC-@``&~p4GvpCHw%*(I{MyNQ5S6vq5%as7O}O}Nukn<06UF`7n+WXtQ5M_F#<t?d)S5gEu|@dJ}o2??llrpMsLkDdlHd<B`hstpmLA1RX86owC!8;Dpdo&hY_a`J9toY>(z!TLl>dMl?gX}6|f-#Plz}XTq)8-oUY4okD(A<v5bm!)QtpHRBNK^D<L0w40976ITo=W57~}s<x~{7!lfUUKZ*J_fp|R&SGK!#2$tM9gCId_(?<mK8HvmeoOUnC1e3=?xvL_|A!^RbS;09%PNC}JZZ?7C^44;YDK(8ZL!%)~hC}XV-@#X;cz+B|P%UnhG$TBj(5lP;@)d$@X?tZ=M}c_Czrv9fB<WE26P9<xJ&tI2I{?R=#3!+QW+hq4O8-cLyE5oLeDp$%vD(cfcaUv(Sj__F#(nd_=BtcmAVO+cZ(9HXBEpn0*bpI_9Yox6kCf7wv=M11=yR;TXqoepcxqXBn7}6}#nhny6_y)_XeMT&3j%}eXhJB;dRft!oscvtRmOxo#I(|EhK(>P6$=}~2`3(HhQmYwLh*_`Ssyu%F2qtuc}V!WnLwf1jSGaJx#2NqCRdy9T`Zv2VFy2Z52nmrf<NBJ0(#zV{{!sPezS(5J4@W`#MA;F#J(=G3$1o=i4w%<kxLX5s?>!8*5WCj6T14WOL&E9WQXLeK*Yvj%uB-#C^+{UZ6l`*sT|GkqWU%u>nX>t6_}J(Z{uD~N?ArI4bIhKe&2A_9G8VW%m9YtI!b$?_L1>H5@{+fN;Uhus~1&_<Ut21&3Z=*;Al*ecdNAdM#L<?!Pa^#J$A%ZR?6vCUuWb&ou!Maw1sh%dJXxylc*{cfQ2Il!JeU;G`Q+dqjBCwL8B<h0S=wzD}3mH6IF@ep2)@A(P-<Du1hXqtuYrkY*lRI0&614tqmOY5;#rDjq!)KhIQECU8iWjo&l6|tf<7#;J9#w!Ro3oqDFRrf8v4_u^fqO2?0+d$7BI5?gn034-@pNnR8r7dGHB{tZTV|%qsk20Qb}7#mz5fFqvQnnoY{MCo#c#%0wVQkIzVGvJmH^RR?{;Ul&cf*@_G)q76gO1gzTqL~YaOUBNcmC1U*6wT{M=)s5x?(Jn|P_#1lH$U+eMd(3;otPjZzC}I;|$Bw{fReDm=pM#sQuIb}cF8Pc?8@eZ{kc0lapsYri0$xcrg1Im?ve|Q)UDJC8Ab}FD2m&8nJudC^5O7=y;9)0v*Fk}sk1U9r;2EMR7uvltAAF>^5Yg0z0EvQpp?F87kCT5N<Hj*Jr%6N2NUo#>rYT(uAYi~cK&jVOt8_6`2^v%MKVW%boLSO+#ynwHvS~k3gaI{`_nUEL#}bqsJJOP7sz48+ZL)wAs2Zb6#0nxn-Wo}Ox1ylkZm4gyS2Z~+s8WUD0V%ZNP_ZV%T`cURR0L7ftKmS-Ud1-Oz=PpZM)wEoC-eI9MswADyVt<mn|=G4NEF3cZ8EIeA9_dgb2q&V?#_)sADWmVj6npUB5ta9fOQRDzk*kU=$2A)F2^f*i&Yb`8=1`ct5Z|ZRw>NHEl2E19$@LdB%#tWe#8@A|0doQoNFda)XW6Po*@x<LWE3my8MpjgXFFZ1#91DcYewyPTHYF@>YevGPm#37*>`w#0OUtRvN8fa#y+jq~ODo%<O#ZOzpDYPpT4OqXHx+mLr+ExDz7c@ha0nNvM$`OVvy_pf)>`?Jn{2geuny>V+y<$^F$t6L>G2t#-Q?lhHy<!{`CPGlHQxQea8Mn3M(jUW*z=o(4pPSac3Vl15NfQ$>o&6lnh#za-nDtaLYfCS`6boC@_#cktp+R6wGU4@+G<KR~ppM}ydVP9cM0NNeT{jL6B$Xesn-EK;0t2CJLEnqKQMH;X<RdXscz3M=~@P#ZYdx+^=JD~|M_cuf;VOm0dIQ|5dMzS(FR0S-v`F|wJ7%hmF5a$qqj?yUC(oG)qaYX<hD@>wFYMS=a2VPy0vp>nd`S8(rHXS!0~1M?F-H$76D_J#tJD-i{5K2VGZSJP9DDx9@8Xf6;$B?@0UKsiU3^$a`pN-8u&ssUIV=F$^(EU#cLC1#I#!A=jd96}&)2%F%~w~#aMF)fqag??6TLAADOAAl|()`UjoBig&$|D2VgRlyjcd4q=^Z%<X}*ATpQ)QrJ_mf$8179Q4%JEiYzG$k1osbT{ohsX$WRrRcRjFGhP16eWbXm;*#8ea%vNr$Vw#s4DF3D8O8D(Tusi|W4TvS%K*x`R%A4%sM*ksBa%DElp8@1Ed$yG!TBgo#yWpGq;|Ws(jnsT^KOkwF0>gB4*1*k#V4)|91BXZCC^mBINTqe|j2%w91<*IeCH5)rJe#lt`CmLE-&qP@Xh+nIdQREfCjfMOn^jB$?46;L~hOkzkO?2vHD<59Cu3=vC%&_`&=l}~3Gt3NFhyL@_-ibl|Rk)K@b0GxLmfI!g4Avk!Ha`zaUCJ{tO_gt_(cKPKkb;U6(>fHPe>{tg7!bQt++dn>;_;Sf}JA;#EwC$#RC=5&#OeBxDC?2Xfux!I3<?al4Si6ob9CjpD{cbs3rAkMDgVj;5sgy1MN~JyYt>oIiGAGMr2~-(ceq#=^`4$F#hw<9ol&m3Up5LR3)YXElcG5InWj_G}izg{4WCo0}4~`+sPoyM9DpG5S|3K4$@PZ_icqBM3an+g@;Cg}VYSddKCb(IMU5;ya)AAd(>tw$L8KzCpcu%^>*DFb4%%Ld!ieas^5|AI6eycjvp-IxHB80;M0INxu%@Hy2GfHAeJjelrGUrQW=7rV1Q_E?f!8_P<I)1cn0daHx`=hyIlme|fQ!7ZsieZxi6pTJ{?nKD7^eo9CL8~}D#WNX4MTV{<ScY>7IFan@hE`T5ovef?$(k^tRPuJk;R2S)D<<}`K>ORiX|9Q#>2g|jjjD^=UQzSYJl1oeDt*Q-C~gvW_eBYw-i0={Ou@}ydeu-viieZfa@rLf`e~ehY{q^(N<g#s4gA!GoKBOlOe&C1!YODD#gI56yWpkQ$qF2o=8IxmJ?~}2XIt&58{D)){T!StyNx(?Vy4lrn9b!#5|aJ#c3HFeSV@*<E)C0=?qJib8uOSCvvSrj7BRCk)(lT<8t^C5Vu^Jg>Z&yc{{fz8bc{vxNSkMsh+`_BM?)*pC#$big1)qFWAFCFQa0Fy#kku=PxB#W*N|r5-DhpoHea#pEc#HtB;wNT&ipFT?J5VwX~yB~B7!rqQJEz&QUiq1pjb?{>~~aG@~9cOs^k5p>qzgPtF*QPUX4B^U;{Pd_@S+f9E22{=%CTC(*sIql4#(C+-buQ#}+i)xJExdeux@nl~^b{o182Mh<%0LLLoS2u}N<3I48TYojIU64LAyKEw!+hxSfe!I%QTn8a+|E-x8QXYE%5Z;&G<XN>mdDjw(<QrjMz$&lfl?!0S(Y-gQqEVJ<5j_`&p~<*OVU0D&$+Eqrv+?$$g|egZq=T#6a!63;(9tPGubxZE!6-!3G{>!W0T_{|XgaC`Ii<D0t+f<>5IC5T2?U%p6;Qx#Bp!RG4|mB@z*gGC0iP4rf$B!w1i?9!+4d&mXX<;y6`+u!Ov^8@6QH7pdAhrtivUVHauBUZ#`6M04><9Z7z;1U;j5RyEx7mSI7CE89R<@vKiSl=#bQ#4@zCc=}TL?M3G`vi@VxJ;|$uF_N~$iRJ-y_b|M5;|3|$2=@7?E@3xB)<tlfB#q*3jYz7(nSd&G8Tg;<coS@g6c;a*np^0vPw%ec(a69bsU1gP)tPC0|m;W0&)TpC+r+8oD`+>C60L+0AXU+P`DYqFK7|G_pOC4lsG9o+?6He6|Qs?|HEii6^l7YhLFX_q`ksvxmlK_y+J9v9yFUErBBFuy?*!FWC1Y|6#fM~!!Zhy=wuM<r?|E;jGke7m0I&c(gk=#*3~IH5Z4lY&=w-bi>K7(PT7js5-M=Z+AFt<k+Lbl#<DCba$kWwHRk+;JJF?utAKDaM4s`wo<CRE)9KL^TB&{*#+`~p1NR=lvPRKX?>_%vL0+q!pX^fR0buD~nfx9%KIZpXF7ca>KmkbbO!xDRVM+k%<6R|a_k|~99ob!?inXF-7g!>EHVcX9P!@nFk7Yjx39=i?9ipO#qRS<53|$s`Cd8~D4+9~x+xD4gMZnuIoBeA8YIS>402QUK{^4|@?`<IqP;f@&p>PH7Y_x-G032m1e3*y@jsn3MqoknGo)vTnHO&A%O6B4Amj&UKf<h0=RM38<5&a;Ez36Nxl@v@Z8fp?iBW_?Gy!ZX{cb7aRWCY5;6~#7V`3edjlGS6!^*|}+*+4FhIsoxvU$I@NaU(qG;VesVSRl_R9wo8|oL@DX!2dASBTi>R5%r8y6*V-WA3!kYfkiaJAYC9z)}_TwC{mHrMY&@PXQxJifkLdM_mLO`EB^qL)&8zblTzGpBb#M-?d({s(eZ{6s`E3W0_7&2B@BIfdOlQIU^fh1-RsAjt3~g=+6cf9TWSP!7;4}o<8inN5l#W*j~O^t7s>7bt_F+aBwxpXvseyEM)$aN2H`NE=FTiRky$kp!y1RDB@bq_5jXE);uK@1&@_59)?2?+{v_j?_Y{;9oHE?WqqKcPGf^h1*cIrN>3}h|19LDuf|q+E`&b6PDbXGZS4J+Xl8g>gc8kQa^G`KY<QOhU_`%!`15^Rg*l^+liJLI_oL93|>y2Q>$!d}qA}=wX5$%I6qm@Y%rbH)3rH3YzX@5U?sAM!bY{~dk4qk5}MmMUKFoAvN%|5K2UZplzCIl=nJN&I^^URq<&e$0=m-9~LIRb1zyK5b)_oPQmb-OZoa~SueAzF_cYPLlyn=LI2FvYTF>4PAx;tBKf02nHc67EUI<e6}joaZ(TQVEXXZuEAOR#|4~W6ejMYPF1`&(6hpu)Z#O(UBmRB|T0?gWLt{Q+8FO^pk`EMN6;BEAcM@<;zqf@R$42R7t9B7<u~wx>%JMU@<;eezwJoxL|FJ?s>^zzJo6RCZDPat7Ty5T$Wgwg@Qc3nLSDBd@$7`P!%;j2@OnQQ_NofFQSLR<~+4L$rCfesDDEm7VLtS)qJ<78nVdPw@Km#(w?di*vJMl6gGrO+$=mDr-+R+sD`SZbc(N(ywQEUqr)iK2qI6!D#0q2pNWp>hm?EY_z!6~Ra-q$j6?w<)-r#fuXD9<g5vV|5~lU}AwMM0yK<No5%q|CLI$8JoF%bK1;GIMFhM?Nf%;fDiMc$qIx1ZUyoJPK>3jI58DK)xO%4o>NK)RO;JPWE<x1KctGMH|ps}q2`Ha-Bp`7FK{i5X#oM?ubv(!SdNu>DQBuqMyB)mu9pvW$X#VY42ngN**5`mYkfg?0<L1Nq5PE{w^18rc4ifuY9_KPWPjU@dKC)h}(b)0hiGBC7=Gh(<s;gx!omghb(3oZ84PF2|i33x<ESXjhBj=Wq-cu3JC$;UFfxe+V_wt%tk3M{mR`a&96vD>_`n~>v4_=GJH8ws-)<S%*RaOCDWyfNN^!vNSNhiRZ39EU;6kIcqUXDYWLn48%x=uk-WYEe=OqB4xsTb6hZkwTw9v+rUilA(<ArkpMVc98z~fIr|yM+`@ibSPTYN{at_kFZ8IPr`r0KzTioSd^*+-_4YdG_Ce~mpLGeFf=KLu{<}LU`@L@V1ocY0P|f>wA$LjGU$~8YM^9<qAgL%8Jkj|Y-wOm62U|VBHwlcXF;HYJ})z84?%7OWuTa4o7DnsDv=SoQM_+(l;w@n#Z1P|C%nsnLj(x1GBv?^&*4fxun2C;pN3~K%HyIb0k9dY30QOo9i*L9PnPe~fJ`VC5(;+@dhltLVkZ+`7$#oGAEEHL8F&1V3;DCSiIc*d8_J?&0Oyr@wr0me*Ref<cWo;$#IS6EiC19Do$J}zl@p-L{PNZE!J|LBCWG(gGcd{7bg=Faq8+nJAAUDY!YD5+o6aCXjHYJJ0P#IjF30C4hm9c}Ec!Y-U(6!Q!c^gOw6D%1<B<s}6?j63PrXub!)SXg;We4}E0hpG65iQW3{Z}+8;@P#B*!`Rf<W4#M3X92BEBywO=pri0?_}av76;#BfovS57Lq;&uD)erc5wQFjIw(x#vhj#EO%eyH>Gx9I{}Fz-u=l%fVw7k~45o_fT-~2-8?tw6Pe&XN66;L+@cvE$+q^5(mje+9ZlC7$9fGGraEZkWvKvD=OF|y~1gKGiV7wIn2%o6!J9z{n^F{3m0AeQX|NmwNRk+C4eZTpXl~gt;j`41D`11%o#f0Jaa;6RTaY!4;0&@agf0l;mC-8`<pGslnFae;!I7ns{1_)G+*`ee(6H^Of9I91oA12jgG%ODa+lJbpTO~*4rIbvy5)818U{a`;=1-oZtl`gS?-hSt1{_l^{jzdyuMDy;i2*`dy2RIBOufmS&zcC<I-;Dnvu|h#GiR6#hZ9zj+r3M0aP~l58dcFn8t;!40BR$c%{{k0p271fHeDz#0gWl>3yPL7+aDAWb!lV5YmcgZ%6R26zUKYw{JBbpjL+d0Bl290vf8sh(nzHjumPb(<DJ&y=Tf$SgLm?#K|En&9jT8nQ_MWJc+(l!2&)R0I_M1GDI8!FQM4CM3efsp=~s1}Z`10c>Cb+<9m8I|<s0GN!bj<K`h@orrFp&PC*ZRXCKIlje66r*N0foX@SSsv*YoaxIZGu5rIdpxng3ll;mMJ``1CctbQnEws6oflazHMkcv(D3FMn-4P8=2fYeZD~`+EcG=kk17ka*1Dz~l=3EqdcoxrRm5meQ=l0A)hWx%wIgYPKh%k`UBImMx5{vdQNOK~ww>vzJF;5Z6NI1t(`pu!Zp~YRy#R-OCdYUB6Pk(B+CZQ*;m&8<_C6F4gUK6FwNu}b^Fth-S4>bW+T^??TO6?QQB0VX#1@W><RQOBl<Yx33vvDNH%Hu>qu!=TbbXt*zW8)ln5ft|+!MNZY@or-Y7J~d_tHnRSn#={Fngn1lPDf*kKL`xH4)<>#N1*ppv2k4OP7mjiy3R@pF*@gEPFp&5b(qiUsiQW5b@NGmyDR=oveFxE3df4ypj`7|Dz58ra5SU;0A~c)V2<Qaiu6zv1gkW+AT6vpbd|NHvNt3*C~apIMha<AppPuFNCFpVKtzKS<~!ttEncOc&ml`nM{>Yd<0MAyC^$A{pcexeBpQ3e5t9`Yv&gEZ$!Ko9ae%S=sK9w2fE5M~KgeKQpdyFBMzGr5q>E@A$snp^ypr63k5^l{$V*<g(q94*-9Dlf`B1AQTrCauO$m$+V!#`LS1?dZn@c_7KTrcxh*{&^M;3<7U~Sadh#x6nl#V1wi%azmsV4wrj$hH;H!dlp1aR<HnU%yRo$L(NHcKb1$*R@Tu&Kuhcwp5{=u?kfaBCedR6zDy^@FFtj4+sBR<Q<<5}mL`)7V+g#wi`a^c7zvt2FOU#?h+3$t;V!E|8)(NZQbi1PG>)Gd~faw&Hmp{{SF?YAK=N=Vc|fB~ZhxpGx(Ew>~1Xpd%J8$BteqXdg!N5j0Ck)*~54%57#aj)YwPSR^4U#}1EIota}KU9kc>Cq^@Fwau2kj{^NfR&o&HiB66}{q#%m#xiu1LM6xyR|@{A|Hv?r%5Lj13ZxI~jYy6fqA*~DO3=9iQaw+;syI-X3QM>jU<gT$s7YR<D+;HRh^wU3U??j#LF6B45o@$i7>Jp~km_jleb`(=t`hDb%1=YeWGE1iiy@RjOn=@+J!|@{1k|IYM5C4vTo(-*tllv87KB3y(blgEum;<i<wFcvt@<09J}U=p)shpdD@`1It_B11$ab#0O)=kVO)vfk?BMY1j=U7qYY4a7S-&$W6c8T((?m9vt%jMQ>Bo!El6Lk>JDpGe`1C)7vAXU')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent
