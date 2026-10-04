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



import base64 as _b64,zlib as _zl,json as _js
_D=_js.loads(_zl.decompress(_b64.b85decode('c-q}vU2j`glKd-yp7Riq^4Gp8G7}r)M1~|UF$n}Cz+^Ft#q17}ybb2RuWd=ZU)5bzea@vEKba;e-t&FBtE;R3b@InA|NQm$lmGbY=b!&|@?XFF_K#nG`}m)ex98W_C%0dJb@KOL{`YU6KL7ZifBf>>|NQ#Lr*EHp`|hvr&wqUV!}*(&51(9I?mzr<`r%7=pS-=geEII;=Ho~ESG)6%FP<De9RBS3)o%Cp(;wdc`|Gc!EqHzLmv?Wcza6*cdiUnd_+fV~dG-2gcOtyX`yw^>+jp<uynO#**lyn4{p!%xabJdC`1&j5{c&5+xA{0M2lmbR#V#7xpHF_gyt;XHH!S$&es_Iya;r^1uoTkie)!UM*08(h4lR(HRakE0sTe<hF~jgJ(xSz458t1xmxn2uEsNmo`@MSjF*FEp7Q88X81`{XFU}u2KD-*H=R<>k{Pe3o?A~1dh#Pjj+r1pV^7U66b8lT=zMBqsFfpCl0_Onl_31cIMrFPMKYV<Cv%8|J<-3m!j5qAOk8rb)M?B2q_z@3}Jv1|VSf@cg%xTci(NQq82ae$Mk;Bo_V`P`dqw;L9v3BRnjdgh7-QR_SKl*t7Ua>VVuP)!tTQhp{cp6HBFP<!I%R0J{g!>US=18-#h3C!er;j-=4?l$OVbtx#aa??KbT2;AruY+2!~IKg?875>Jefmh?BBk)eDh{^ar6GW-PO(OH?M!1cV<2;v9T^4R;dMBF~^3Xo*OyQp)=|!v9mV$hxS-vLrgM7*{wUb^~ld1%$&tw1O_DRnL2SxvuiVdQt<l^w=eEiIH!^YG1@BeaNwp@7V7wMff;(&TXWqCCL8K~*5%Q<f`^E+CzfDEv>xVW1#DiAO)a%?*q<W<+c{UHrwqS6IEvDF0EhMP6Z2P9f2!dj>;4!#4u`{HypW`}(E}=4vZI?`c@VT;=MaJXYuFB(EhPEZ;3+Xo3-T!2=Y4D;w*T7rj4dxC_;c$RQ*Fp-M*|F^b}n3o7B>P0M<!ctR<xhFjzxxh4k0XQI1q9GEjEBYiFSx#f=LG7xOu_jusgMMMyfLg7t!!cc*f&~5bPna7?z<17ZJgZnPA)KP~)rftN+Z$Ni^>g+`j*~<z^O+t1SI=h%r`I8``7rIinFbMoqe7gP(@Lnmhy&bUa$A0F=)jCgQ5sH&^HTZ+BN$f7OQ{xn<)OF`NLCfm>obB{X4fj?AqJWl~y3ggL5*MnTx04T9Gev|oqOhi2>W@u*dYdFtI5I54m^#IkO0%7dvDv;-rM>of&ARiX9nx{JM91b5n_Gz6W!>$tY^=>qZacJGD0{ByZCnoXM!65>rN#;u;-mYpEM)IOpY#D=D?7Zi0^7>J68qycKuVj6Cg)f^FNMU8$PUb&xvN0iM}_SwX$8=U0SX{wWX2$^gA?s6bClM4>-)*4<EV;pY^qrJn324<P+Y;w2+`41?>(LgboWAhc*3Ypx<9SQ@D(CRFPlaZSS-5`bDHk$=$?4d`T)1#m(Voo`l1c_9L<KG2m7(Hzio<Zz}+4l-oBJ3D680X8c@-W5Z7GQLpn33DXh!NtqrZwOYKCD9=4mzlbJ70Jhw&%&yq$R{yCttjO@!5w@Dje{Ye1(!jwYIa6I|TB?pmhKZ@YL$okx9tq<^-AG8)-PAx=I+sWq`wm297?SLf#sFP1oh{%(?Bs{D*$NT5dfJub@A@u%r5W63nt5y&Q%UdJijw9jRB-Bj`A%PBAEv#3ZrbouMa3Y$s0{8d^^lp!7VnwZq%ecSZ>q5`~2DWE?Ee(ZDug&d^b359HxDdN4R`ghzLjL;`YQz~o6D9vqwbZ^Q{Co;yiGSJ5<}pw)B&%1_TCK*%`Pkc3JQWZoI>57xO<LtmJmvhY|wJMV;LLF!C-(+`2@Dr`(}%tl}C!CrtDcJ!EG>DjJ94%x)K`r5;&u{rcabu#)nL=q-GdK7PKPh(DwW=-d9v>iF)zR^)(&Z_Hj1|<2G0M9UIaL+)mst5Kt+DM3W*B#Qy&jhx}@n;*Oefb6pT7(G}^?U_2%Qjkn*m{#$6+xR^@57Ct0^`5Q0Lg7W#R_j6GT&h%fNtZwHnU}t-GvPIl~O|hC9?CxZMsYx4%_$>R~{Z>SN9E`>~||qJH{<nPe1B0hzKw?cv<GtfQi$~6)_!^h?br>A{!nv=oemqmudtV$xf3%sV|2aU~GXqc6!S~Ztfwrc6s>*Gu>*4JTYuZbMp+@Lt7t?^AGpMOEIuFTxcVA2^oT}b1*u*O#eYmt4PJTA{?FPb|ah!p>&Iwfjm8mtXJ4=D9nPpN<H+6OC6XP0%jOJXxXf)tC*@SL1R|{Dp(|AKK&XSr0hOW>9ZX6fr~XsAoH~I<lc}?2>^ez-v9wgUYI!MF?+D#Gq^(#C?_pL3dom$I0SyV2vn{!qpHwZcnB1j%V;f6on?67kvXpUK%Mt9>KY6=`wJia^rAJ*DjPkv13a-)l_KfDZcjs7<_qCwBMUD-iZkL&_t0ye_5=fsO$I<n8-AQE$Wk1UH5U-L^F(Gq&}h~2nvOC%Ird?wR>{>^K><v;l_9UDY5m14<&NryZ~+O2F<wsD=d0+!Q5H-V?Z~~M3IjsX#fz=EBzch7!WF2*FvU_yx)RaajJ_vaxm7VRhrH=UAK5A92@F4JmkEo|r||u9?w&A0g{UVCk)w<vN4my|1#fH$ACh#gI2<@=AjL4HWh1P3bT+}uKwvpkN1KRZzy)F}tLSOP?c96}{0zp$Kr*xBeH2DUaL#ORO<8qxI3OI>!si!vdQTxqcrZhB8ynZv#w8+$+gp?OfmVyQ=2LImJ4yKZj+8TV2nlC@g@!f=QdJKarU52Evb$7ph4~r1)p>?B0WD&vXDN)iXS-}~8`!7$0>Lgp3qNinDTN7(A}n5zr608Nq?M}<o`3KvM_G<C7-A-xvV>ZSxGl`Cp2Dw?(jc<lpoyACp?Xt;(5aLpE0f6X>H{0h^)5|05Lw~s(xYvtYr9p(0Y1*i6|4(%1t0(f6j+LvMnN&`soqSP;0Ak^#7lm7{pK(CVRFT#ia0fj$hJivA<oOF*|B01EhHsgIWA*F>q^jS=&vwWj|xV@gr}kiXOmBkun$Z^-Q`ej4vrK68f2<Ln~njwd#tayj*rrius-0Yl~K>hQIq{SkfR7yiY0n;KnzwPlVeaZ<79~Fe}8#-z3aIT5W#MEh@WgvA~deS7ISP&VIg9sVbM1xGS;j&rgX-j9y-&Ff`|G%TJ#f9%@OiD(7AXQdcL?kbbA?595pq%ooEQI-B-hrC2%cLTwB|c3jBaA&ZcrKN|DbLCxB`ic+0_vWf-!Ls&v(koSVxZ&TlUD(-%-A1o9N@Y_7?bvKLHcjkaMBs*4~Z1w4LPSvN-6;F=lH-P(IB#=ne@yy>%*tCb}KM%puzk-cwz&m+JYAtSLJT1;rOkGquf1Xj2KdUhT){?L%5(+;OjvOe3oIlZiTRX=B2hgr1CQE8^xEbn1UjRC74CM~tk^%k2%zFzR61gV?I*CE85{zWk5{SQ5DVhvB`tjvjGmpD^DW@&Zh0ujbp`1z*XZChbO7l~AXx2)p%mV8>s^+ULqQ0C1dL~TT>0{TW%x*$SbB6N}@b*a&s`}D4}Y^I)8FkvJnSR@$vvMq9Nt1{`(!zV~A31<h^PE)Ln6sF13Cm}DC12ej|`e8O)+>3&iJb4*L7;yfQawA$KuZFx-qS~#<_|)qxrRi^sBF|V>cIYxCzT!+Zgw!h;zytzUT=MXEA#6rHJ5{f|;EC<lV3<uK5fWW*`s$AEk7C`2CUsHdH4H5Z?sT~1I<UiX#s1OofV~bmSV`hbEJH)N^1foGn`K3|9Tn6hW%f$kw4PfjoS4ai^F&xt9Xn~xG&UefTjDuZBpHVZ{2)52E#}!H!ITD%(c**iq^k$?#9&xj7RB|34kXE_U3i^dHYq`cP_s!TmnO1gT0=54a^-P0VD!yxgPg7b9BFD@jahQ|8ZZQ)TJ&o7H6GlHW5QSaPT1A90cWu!l{{rF1Fy<Q0y))kc_jFzE_=0U#BdQbkQZAb>^<&jXd8rLr>;w_lq5M<^xY$A1%p5DCv)q}=%}AT>Apa*<Y9fCRq9)zz61^sM9{+JFY>d(A8t!i%|${GVhy7-B>Dt#JDd6L1JFVd8+5u6D`W=hAA-Rl5%ONb1?i9_R6>qZb9CB5tp$r439&$wm_QWEAqnW9=$0ZXFVMjw83)lNoRt&k$`OTt^^9nMz(B)zE<+ddNju%JS%XC-1DZ`<!9C-|!i7hP2{ie&8zppnj!q_0z(@(47P@&vyuHn1rrd0Y42BIu2wg+MIw7Ag4w$u=g#!Z?ufptj45<texCJTWX%Y7xolk4ThNQXh^qP;G%yDsoXRC2coqbQBJd<!Nrp;*{ODCpT7lkl}c<$6|99x`pEK(F!E!EW|M5-~VST?23)h(-MHEpYsq@E!8#X;E`Mbpa<Qk2_p*?JM~kHQ}YydFT4^WiDsFZqU*BOSY}fCfDv$V%;0)ytvuGU+*%zO;@o**(AQNQuc!6~@+nKZ)FH)@2ovUGG!Ld?gAzi_v<LzEAiM`p=z-{6tWV`>AHSa(oC4h~a6cd5Wv0`#K~u=#=0dAPi6{9-l)u2&ED1dxmi!5Kw`4)eYiN;mUTp^L`=Eo$mmaG=aMlf!rie(h+m18T)9BN3eud>Y%%|=xKSO?Lf3%Sw2SF1m=|oG0V7K{shmOlecR@DyCyMK8<lg88nL-d7f{~CLgZeU4Pi;TXQl>be=&ei$w-fe|U)au=^b8jJ!P@uSt<%?8|kSW~NRvn<wFVAnsk5OS?YU#{}(*fThm1m1A;8>bqPuok@-{i2=HfTabQNTtAM<<#q)J2Vim-I_HSW&Wq+9On^e%D|tESVgJ<*VM;kP0733+fra6n$UXywvL|zrjrPr6B?qE}K!)lOn}?o@vwgFvbGhkdMaPzDgEBL80e}<)4jh^&i$544gKo*sr)Q6r^DNQK-1qkeam|zdH#;3k6ihTDw}O^8lTH*kN+CVRheKegT+04IJq!Z#0-_>|4*A)qoHSNvo7S>eV|M_WJRNI4NP?Gn#%kno%1C7aoXZKyp`A#hd{eTl0az7axco#QoMaX}<6wqn@j7t;r=%+r4k6oIY&>1`^x~FS)oMjR>YqqkIil8vYlT7zOL48mp8-?!C~BB=$L63dv%AdP!Xp6)tW1djc;tB-sn2~JZXBy6o0X)L{>mU)KZx*ljHLwIh}7o@96p#iP|Y`E^pQZ}E8lX#9|eZsYP*T$YlYxA&6xH=ldUBmTl=i^ba=&OdHuxB&jg8tN1iNB&$62jE2M~41wJ#q^Vl4)J3cSz+$o+nJkSCd1>JtepkKF$tg{zV;5)h)Ad_FK^RV?JQFO5dspUDsmtlDnp-X6Y8~+G!z-tan=1kL;u1VQ#XA<}~OG3hr`)nADXEw<#`+hFxiT;WJNT>Dw`;0;kk$E*D8+e{h#l7A4-{b1Fx#f?>0;#mbo+$H_Y~pbLN+K=Xob>+4*N?5YmQxXNR!J=w?-V5gv)#l}M6cM5?r4=c9)U!<B-BLkigv7MY*l!bbT@ebM@R=#P6z~v*yjU`_@HN4J3@t_NW~?&sN+;CQ?!O*SOKoT2y>_FQG(yIsmC=TS3<D5kS>edCfzD;byDGq&v?rjO`gLNv@mnO!b}Ym#W;mmVql68ekRcG#}XoC9Wi(zlriu#&s<>4<kPasJV8BNzDfhgR#iP&pS_jQeTafxh~egyOUgAYoNklS-ECD&<r~OZ#|v-L<x;Vk<id4v9f)vEv}{St2i~cSeCs7ST6E3?qP#d#9r&dcc?}bT+Dee*6@VGjP7j-wzNx{Qg>L0%9z7=rXIGX3%1R4Y6hDhe)#~!Cir85No<U9G)saZV$+KySf`oDo8c1y0DMUQV+toTsAY)w8dTh|Z;E;4Ja^)fi{FRmuUZCG-&MT)hO6(sYWK8Q$i{K>iLM>7ysF*VyPLm18)>4i_Je=+&0dxp}Sn7O!@IFc{!>9wd{4CNMf|l%U8G1RjT+#v*i^h+rm>8K4d1@fLrJvt++H%Zhr+Q`R_K?u;;>HPxN4ZKDqi_Kyd7Uh8AvYKo)(MtNbkVaN-vFet_GNkI9vow7;V$>cSu3NH^~62Kz_{fh!qs#YGE^@H#o_fVpN;cuf}TFRce;_%RqVVbKzAW{Nvh7#N}BXI*t>zr(Gp15dKiVX!v1+$e|EwgAE}J-rz8fTi`^V0T0qjk1*lOv9~hf4xMmxQTRFiyWT0kStCG=?3HGL$=cMvMd}38MwF6kHY2o<37m47E%NWL^a%EBP=8j^wIkD)OU!Tp+&2e!wEvKr=;Jf!3x5vcDu<UFzEpIC#KNAS&iBzCG_+t}05_x`28GiXI)1epi(B)##+alNR?AFd7OkbHoaaPSpvjUBiKHEP%*h@o<aRMDN$g}Q<W+l&6Fi0&bq895?)b^z1Pcm#rt|rl#jtjRAdNY)Sjs^6?r0F!2(X^BHIj2{Vf2+hN7xT^Vk0%{7T5~SAVL@Weh$V^Ex)&!(<c)hxU#(PjCD36M!Ti3NT0Bz3v0^D#k4!bsbzK7of+?X|2rLjIj2w?#ut++0^ease)8Fe7^My3z#selt9y7rJe8eVIQbifVUPV&*i9`Lms9nNT$Njdl&ezHK&5AcE6?BqfNqkdM25Wbz2#98cII0u@Ro1%>+7Lp`>~8H-e~A-(X*zUnLg6zs9Co}*R>~{hseD$Zg5l-PueZtb`mJ2lFq{_ZvJoz0li~!0h8gxuO~q(iQ;pP+Ynb<l85Rb9FAh$D#z3p;M(as77Yr)ytkSo#sQ&Z>LnWCN2RDw)DD1>CoYMXvO$-tZa|N?#KqQhONsF%Y4Mp9qqE=(RW=#E|iEjf`DuV-oSTnKu1oBS;b_OP;%W}MA32ZZHsSB?P5(6D{noniIJuoYPOLnQMCL%4!cnPDL>dfXwBAP{F)1XM??qZS?A1}hdFbi115HJMa?U{=mDrgFl)TE>!DvAw}KtdiCgrq9VH)ocR9CA<Op!0SWnTD$5RhZDtMEZn7kB|lm5vzz%Tdi(GYNdB7WX6gN7_3i5l*&o5)Uz)jt|S`~*I(^0bz)edu*edu8Wrte3`4l<c>jh6I3QE+*bYk^M3e$My04TcA{wW5O^~E;vrPdcrVV4WdHhcrf1qK&*@7voifGo2YLJ|KPc5c`@A6c}Ov;kchL+>pdoIShI~Gxa=d!c`HOp2A(MX{`)OH@6jBzSF6F8IJNfNikAsUzG&dX;ONIYaL3-gqTmzlNvltj1qRUw<35(I>$7rV$E$};7*;T@^(`E9pC+EdTu^o!@Qno4<pGJ<MDwUbBXs?xOZCeA9?c;6Gb0Gq{s9ByhCHAkYGROY4@G%0y;OpBYkh7O{-6Lpo9*h3W<s%o&ey=Dw@*4?`@=v%d>IdM8XR%)cakjsHD!XjOj9P_01OxuodQ`t)<V;kDU0pRKM*+`6s{e&wuTC_yVNjNtv0dZx+Rm;ez5~YGj&RV1}l7%UBH@e4}(t$=FT8k<~z}F~blNY67wJ%a<w+&k*XfcaFFeq(b_gXs;P~osIAl;-^5DOj_=vh>rh;=3A!|GQ;W947DsIE{xKCht8P$GwxZ*aex>mXs6z5p)fSf405-cbpLZFnnvi<SWCq>?EoFcbPmFI=g~>=3N+_+HeR#?qifTWr`bP#!Kw<0p-4OCIl0JMv+PCH%B)lYB6ZcaYjx+W9Cd0X(<r=UA*!gjhCkCLfhaDo`L}Ua1r@O%fSe`%k&0jKqkduF=Yb2T24yT7`9HTd=8!SCLMdHU^SEEDoYkd}m#jkBfBjlAI6%GM}zm<Q6dx0a8Zs1c|E2J74AlGf^KgNjBm^lCYsexEa22cbxR3;Bo)LtAZ6QO#T?ogLgp|2U6#;b!c`&EGw^eP3!V~Q!2d;5L0gldg4hrnXf8Bi_TfBmKAJ4#yEfntX*fJ&q=y>o~bJYvYf|oK%^)bV~OsI>nU1_-okCW<#pm{07K?6z`+#6N;z3-d>*Nvocm|DF2*S##v?;kmej<5BUfCQbnAH|F_hHAjktnoW(d>WFY_JGd`_p3b{iugn&Pl>brxs0E5TEuM#H!o;mGO<&6eL9--r90R7Z1_k?F?x-xZ}@-}uIr;-TFHJ)z(m0drf>Go_g>8g9h|GUK-BinGy0*e3uZl#pQC$iS_cc0=!#Wr?!xsd!MPRp!agETG}D$r*76Id%Y6jqtHY9;cz%B-@0m2(*<dFYrV+pCL_jYm*VP@6!@g&Dy4(WbDUa)!VDfm+vlaW_9Wxfld18;->&5ZHOs#;+C?7LgIrtx_?xHsZ-LdCU|NC2D0`kt!>LGz_k)Pm87<fxEO2OlnLypED>lkqf5URdZ+F<c7GN$apFQctLu%{7aNQ3P*;dn2kAt*BJi`PO-T)D=x#`s^G41aBGhkF^(EzQ26(&hG>8ay6&?lKRN`#u`oBsB=@E*g^tg6~Bmhd_;0{G>cQlWRGhpQAcIrQfaBz6GGrWr)3SC+3d8>)^tpGkavY#@nQ!0TSckSit?`;xu42qPZ8UdY*pk^2+X9kwHtQ8BZg>xI7$x38Qf_#KUy7=*iJ=j{F-aUd59<E?_kr9KZzZw!z>K!RMyjF3ny;Eyf^w>B4a@OU6;`K_+=fl}$E7nv>B1N__wXhQIAvvxXCBq8Lh;7R2m_{oJO$DR83ps3uCHMlM%?axIM8(}FyARxjWZ?<9YjVCbuO_;x;=mH8+pZ5RH>^`$Y0`~)KJCHQ)vBpOE-qu};?G@nki}rNabRCMs1iqa0}Wf1s=W8snm`;9D-Mdd270AdpI@@zI-p$*QVf2zGgc9DCn_^~8qgLSa0UF|Q@3eXq3B7$PKbP&lp^?iFDA&;lClW8Pf<~hx#gOYx_YD@DYK+S6UpHRTZa`}cf6%deAPB0e!LVl)0{Eb)%o$?7EsFzo>eQn3!ZOBeHIikf+2xGS9mlWiLck@_5~Dq3TuVA=;4<idceFsH&pV}+Dv;x3WG+i!a$!BVu;qH$4RxYVGnc^CKr2*Qr#nwTh@}7YB2Hy+O!RlE}DMmdFb~MwF-8eTU57VaS*!E3MvaB9EiXNsU~}iu!?4U2<ib0U>YBUG}hvAN_#2dFtHJ#W}^(3LAat%Acz;y8SXRz+|qOJ6GAN7Cl0Av*5Dwd`NeQ3RJP_Edn$9T=wn5BxA7_Hg*rxLN0jToQJ~4q7b1r0vRPG@Ym*o%(68^tW-ajHOaiNAVCkIIO|uB9v%6bBF0=}Cg_|y-V*RC2MJK8(GwKSYmbh^&_D=MnlnR-C@$pUPP3nm72zxbGR&1UobyHbEI7(VBP+O`B4ow;zI-ieaOcCXZxfLY4-pgYWm5Rb@GX|0%{znEd)hJ;L|2R+W5@4D<df)P%1$Lt7bzcEmuW$%dAE*fQYV?JM;vsU;2tfsf*0-?nQvx|TBDXG2jhI9GK1iXlNb}j#Mf(byO{hHGQ&88XH5wJf9WhKCmRc<Lj+-&iu;IlF9Kx`6VXrOq3e6@wB~aCYYN7~8-AXqt0m@YN?9Ra@wI~2Jt)6ubYUJht4E3V3d-$S+s8y2E;KEhlaTNk2C$P>$?Ref~l?#<Hl2h;qUBxXM(xwOxW$nXs5!&+LB#wFH#9F;0md=2msR_GSyfH|0c3Tn!9tI}7{4hq(^o)d)j&9ZGjnc6Lsr(GnPR|}+HdbYCb3S2W5_CgyWo_7P7Zz%8`&qS08wjS(wUWq@JX6yuJAln*e(+kgsM@Og^uYEh(i`gFXc19s1|ecdZXO+5gXT1!75#Qa(^XeZaQ*Ti5-Uq0cZ^R&HA5d((vo%s4MPRISL0P(u`mWA@AD!&lyH)xVBU^w1cA9|st5aVvP1JWEm_7;MwV!)vijGd_^fnG_mO6+iu48df>Pfd@MuUvYsu3T78P=y;WlNJ?;sm&9Ve3kb<{Ct9tTb6?V0dT0NFfQjKIroqMuXmru8zQY_oV46uHO9HkdE?TIPi)`bzuAxnW{S$>L7C9}T6_58YMNPR2TBMg^%g<08xMO(cO~>MR4cNC+iYv~MjZ-x>~43xg5lvR;{jS72M`dJ#7?!WKYyhm*KJ{ZX+i5jRs!b`JpoF}x0Ok_^;T#nDO@Dh-B}>hlK4^cc)^=<7hSVks98pt{>06kd`fcla2lHgU6=>J5k_jHh5&&Kk9AHy-S}f~tV2FYp+QUO_jtGspL_HEEgaS_f8B#Q`(rFMmbZ7M|RKP18NTz-*c#-~s=xMgRgu7?sIdSpvjP%uJUmxLI=-D&Qn>Z`<;hVG<wDKj(OSY(d6sYNe>izI%nafJmyu!m8DG7uHmhvIt@gGBHbTsUm8-RtB$65-;IGO81wLEG32w1WDNA_@RofOSE@Xx{y^rx{=zJBG3>5g06_g{>j}F6GUpAP}Ex(+pvlS?Ztp!tI&tF*WqPjiO}-!InRPo$zx*r=<`a7C~KNkur>0%Sv8nCD4MTX&OLoNb8znR5;a=$l+BS&C9Pj!b*Tta4kWr_cu)F(!SLLo8_f^ZJCt(cEE_RYTMsLz@M&1?FV7UmzUFLGlq2?$nC%j?rMzjdV}$@);+^$m#}k}&Cc&Z9T5d_Ziq2(0&W?e+aG7$EXv8@n_$Qe}xn|3>(8s*?n0@#N$AjR?2~`(qES5NNUjXXb$f?cCmV7P<D${BmKIdqvT<BRtzs44;A&8KsXh`7tMud9-FrMopn8YSswzYuDvI^fG1fE(y0+6wYj2ExRJVn{)sawpMLzH<1_qv}M_+K8P7lX7UE6fe-_tGTLWc;|Y0?Om3)C~YWbobPV=s<3sC`YQAQ7OtVbRU3xD>DZ?l)Y_909XW8Iu;&j(iVWDfszyu7(qx&o?J|YT;6Gz_BmIN3n4SX<BIx%mEqlrQV4#a7YZio=9Kl<2A5mNB4><g*EDDJ%u<PuloHO8Dp<}fi)_%)NP=MrN#Sk6obY@TOCl9hrB~ay%+rjJnhG7i7&BU{??SqNs}>Z2=reJTV=|6OaEyt45_Nz?Aha)=mTh8D-dH}QbgM;IhYuGeC8`5iV@F*j%S0)u8s!z$a)aM2FUq8i_x;5g98DB{U*J3NFeB)d2W1B--5DO7sdsLCtQZF>#29nr0u4$J=#`!=bubMO!S^&9hvRa8zxmR+zbr3T1*#`|+UPR~xT}0ZEd_j6%`k7|^=gQ89*|dQzuXb)EXQlHwHk=N0t7C(gW#&JmpNk`UuMJl^-f#L7MaK*0Xzh@9C1&E%#vfubEaS-C-^$jTg4$-nw!-aNSzN%iSeWld8j-l28jB-{SuJXf=|>3VB3CID(hEvIX^t*>hcD23v#u0Co)S#6ybu=&+;Q^!AlxraV(4kB63Hl3E*e^$g<vabQwi(+Wk`N$%R(<hc!j%hsK(PuiE9cD;St1Il|((Oxm;w|6wj@yrxJ|SSSo6MEY8^VB*~lTa#1Cr0_yyr0&ZV$rS8uPb#~Q_ey}O1RPL5LICJZD>3iMp@7#G+dLS;^VM@JxkN@Wy*N06AxcWpUm-V!F_8CKyoNfq+ES0;>fTgjD<6cECT2?zkDJ4-Z_?2<5<-S;MT%<E%T25icIxWnZu|u-IQs*T>M02crkkJlTg6TZ@O}F9Ghp*Z(4JDYu^^BuVxwk{5H*+4c}c`q1561qw}g>qQ~^s=V2EgyMKIEX(j(@|rEzmD0kxi(=skGAYo+FULpdCjoleO|1bb;s?C(_E3^DRNwF_pumMhaqi?pWTi!C!z8%w1mmp54;ND5+1I_-vFFy7wk0sWEHxUV6=LRcWCP5XPS3(BIXmZvh?+-GKV7H12#d4s}jFX0qQTG(EK32KU)aF}ynshJr`(Vzmt#7m+Xg84={m3++}wS)=}epah__g{AL5(v@h$mm3n5mP;?<y|hfiY2^Dstv+H7DY4liY?!?<6t|Q;TqmYOt;*u+|+e@DWW2j?wXrj0yUEZ3=L>CEG$h!R?INA>S1BBUW>x4Q0Hl1Q7RQoFm%rL#Aw+?%FsHJl9Ur;3W`4W`_4|eV^BE?2@^-4MNuKI2X+Q!Q<t~JJ>VEn0wN0{;d_RNrg&-l-TJbiOX#V!b3J|i*QHS@?X_*^uB%*7nr<&(cF?$~s<`HCo8~g`(4-D7@iI2ji_pohZ@~wOrAqRnv5g-`i^P&69$xUxB2UarENrE{TnIKcH$^g`YBS>EXz9)&{Sja)4dr`88D!L14odN=8@Yg<hNTw4CaBP12pT%}k*@VvQbNu!DF<-nt{G>Hi<*uoEkUosB*So4F>!~F$>jw~Ie&C1G6fx0Rf|I-ZrUhxQ5cnu#XaGU(^w;C%?W<O_DD#&Qi{KUfw)B>85qhNq7;s1=};`OpawFfwNRO}2N$ADtg!h;nnaLWFfBl>=e2>>Pl6?=54XyrmBR=kD%80Ou**c>k#8t;RJfXV(zW`mtzr|Er?>i&dte>TgJ|<8d{cVqV&&vd`>a4L&Hz9jHD*-@#+h!1lYr}22Zu?mZurC7&#h!>8oJ|=e=g2#sR9n@p*RjtylPP!af@0<_%YE!MDi<0m<k*uy;`k0Jlih#psrt9z2vOoSgN4FGMV+bDb}(ZEw7cmd8z0{!ZoQ!x4ntiv>Lb3OJVo;bbFbtQ#VLYZDyIEq=;`A!am@LPseGaNis#Vn^KmVv<XC*)(ZSL6m=5x3X}Xq!OC}|Jz9AuZ#QtoLMKWuo(Ieks#o2D$BT(RaOXzLwd$1r=G8w8R@YuFJEJa;5Zh4_H)U#R<Py4q1UOqt4@2?VO<Kn>QA<wbZc1B|NiPV7h%IpqSLB81g+Q0#YNz-%X)8jk!s(?hb;I#V>4(A^KW&MW5PiM`<luWiQ%n)M!>y!ns7Vofh=IU2i9sIvl0x?ggAIZ=u<*A)R>Ql-s@^2@2!)!nOGL29*~Tw%Devv67nwcf05$M#i8^Q1c@7Y*JpodRi}Xn^t;66_pi>Azj}fdg$KdEM2}J~<_N8EwR*8F09w+Cx7h2<J8<0sjWQom|<Kg{hT|_G%u(;Wxb(wl}$*Bo5(Qve4;tr()_e)R=?&D*KG(io#?*+<G0clBAB|q<5i17;<j6&j_1XD&kfQv5o^B?F6VHr!pNVh4!!R2DDRz)bbzF^uwd~pe5!VU%W9k<~Ceif_?k_gJyHauMCuPOm+C$|zOc-YgH)^#oT&7`CtB@YNU5QyNG2!up~ivv}XHX(A9Q}5GCGEahYXm*gRz?voajz-BEW*%efc&l}fx$3lodi@Gf2KI@HLq4=O=niZc?hc$!ezGhEjGN~h6#&32`MQTeq{7i53D-j<z7qJ#tyln|M8Qcdkj9D#zze@a1VF=UJFjyg_hv+JGey&$+nf&POsSnurI}MvnoXlPw=VV|>}z%s=X^TI=$=Zk%SAar(rI2+q~|Mhst*V9^zDexa}Q<_<nFE!zy9&d$0q#i<iG#+;osBKvlrX57vF3@eDwR@|L>o_-)FM^^watK>sObb$VRU(cJD8)cIQ7F-nsta^77`@>)qjv=^sr0_wCiYA1_|Lzkd6vLnm){H}5abzuPT;=R*ts{r|x}4Sf')))
_T={i:t for i,t in enumerate(_D['tapes'])}
_M=_D['meta']
MODE='fixed'
def _router(obs,step,st):
    if MODE=='fixed': return 0
    shops=list((obs.get('town') or {}).get('unlocked_shops') or [])
    if 'route' not in st: st['route']=0
    if MODE=='shop2' and step>=144 and not st.get('done'):
        best=0;bs=-1
        for i,m in enumerate(_M):
            s=sum(1 for a,b in zip(m['shops'],shops) if a==b)
            if s>bs: bs=s;best=i
        st['route']=best;st['done']=True
    return st['route']
_S={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False}
_IMPL=make_agent(_T,router=_router,**_S)
def agent(observation,configuration=None):
    return _IMPL(observation,configuration)
