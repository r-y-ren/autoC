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
_D=_js.loads(_zl.decompress(_b64.b85decode('c-q}vU2j}ha{Ma>pZ#FYjA$uuv^2H^Q=&jp890U@7+41z1e+{uzZv`ABZ=hPuj;O<KIf8ho=kJ7x%Yha>8`G>{`2IIU;g>)?<fEE)z3fwdGepX{PvGufBW=5CvVTMuTS28{ng3efBB!keg6E@|NP^Z-~Rj8KR*BU$#?I5`f&c{)$8+%laHS~zdU^W&*{fMy8Yzs)#ZzK&u>0`ba=Tx|MbI?<A=jPyMDRfzy16V-~a3DucmMC>iLiF-cG+eew*w4#l`qxw{P<D)z$t)_$eQY^t#`@dv)>R!^dg6d3XD*!@G{hGJM0=Un##IzYF?nJ`c-@y*PiqkLLB~lQ)-FH!p9e1^;;1U*DX(*A^hy3h8p+|Iv2#Vz<v7-avY-!gd=k#rXM)6^6eeZ?t&s@$V=5<$j4~+amb&-B~?;8JYyR3f>akPy6^ypP%0keE4Zto{um5=JU6{-d|k4!7p~b-@h3C<m<0C=GnTwd^er&U|~AF3tR(y)~EA4nU(ng{P^+t&Hjq+mhV5kV0>WbV}yr=JmP*G$B(#w?C~|Dhjp6d<C+HJ9GQaQec%jEA32zo9y7Z%kIJ*b!P=iM57zO4xBo7j{L#nr-xc5H#nt88`P+=1JYI&<<cpT2ZCghdl5jtwmwBMo*g|_V`|5{Wm-{cm_b?jv!W<VL9o>tMbSVD9%W(H2G5gTuju&$njQ!ouFE1|k&u>0_zrVV9b@A#y=7X6}OYE#m#wzt-EAH4Z)pI8&GCHG?5<hE`e`wDocEluCl-;^>Uypp<(al**M&Llgk*N!}bh|e5Ck5YsfBWKLg=;E#5Tm0KPX~Ur%0?YOE^tF{M{Dj|!DU0E&xSnOSI~$!XJQFfMEhaxR>0Tmaj2zt9M0#+!FKG5^pxSdhd@!X2XI=CUorow8c#JmWZf@==5R0;<BcS}8#PeTmL1*n%7dW)I)@14Z^M4rY$M6v2Cc-fEGVLEU-z+x*#2!}8(ZE+@axubrrMCvjt&?^?OeDFZEge%j$F3ft!THojz@+^4k0XQIuLRIJvM+oiGGOTf=LeF`1OLv;c#jhj8s<)Zld9t(8l8zA=pFUF)ULJE+T>hGr_mfp~jczSO1>Rljz<hxPAY5%iS!TS6RmC5M!+FHgrbeb4D|6%$jt^244+<HF*jo=y<eK0Vtn6OvF{MZ?4V{-|erie$uBOg=OO%F<5}f#4WL%5}Gh~N9JCIvM4Px!UEOfOF`J5O@j9>=)4ZI58c+`<I!6k*Qxi*z=?rxLp<yDSGjk!f;Yj)<2tVbgR0Pbcf-YAZv;=;qr3>Rz3YUwvUP!Yczg6hfBb8OH=0kI5E9};D(0=u-j{<Q!PTxtL33n~ofIA<v6<@|B+0OIHDuBdHVq=Dz_l1w_KcT?hr|20N4O-thlsF8ew+})G!b}E_;q}b<;-Xf7M!n*6<(r@Vh|l6kU9-tRx%+$Knm@~aJ-X+zr6=Xk8Sb=bj}L8jmK}%-^(WC7K|9dsJPA{%A-H*GPnU~K%~h6ykS$Pm`Wk$9$tQ)VGKtpY)Waab02gVa-V<}J&j^jnm0)D1z>O}NLnFx<ir$ah9*v~R7Qmj40|$+dfic?J4X8ARR}Ej$A$+kSCP5$yS}lBka$R)QzKq!vAd}YM8cMp5)bn8`}@t&lJKRHQ(D#6Wt0-b(U+nhzJIel#G)UPTq^8nEr&+uW^F$i8bWlHV8D>s!EW#ALMseU!QZzr7ClcMWeEy+l}PipwX$1jO;q$^@Z92H4>RDLRV9f_yyqrCT111n^#v;qs`Ah%5F4Cj#GJFA&z5Bf5bDEayI}O-eMWus>Tsqh#^Dv_69^*^^@7LSK3u$!ErWrrIor@a0Q&j-H3rLoQd=6CHcw4SnU1DVh`G-zarPeaSzTkiS~${@Ibju)I?LXSLtr=yUnX$Eqd)G!eBfR)0Y>VG*I-?=Sg56L!OE|2qNzR;ZP5@5KYLXNpq+tXFuGkB4b9vd@GUYlw0R?h5h%JLvz=?t1fk+6nYc0AfE=lwd@U9QCz<#%l|Kw;c!a#s(o1<gKsyz}3(n$~v$A0Jo56S(gv-XRYI%!Na9J({8SRne<HEy6mmlzc(Wmui5&Sr^EAtoY|77UBuJte!Thwt68J#EU6Kg$eC4WER*mVn<NKDgsZvaT3m*=ku>418;Z{=)$78IPOzo)u2E$%gp<|1l=UGq}lG@-H^gzJoqI*-W6i&5bEaCv!w8EahKXE=DnE60`0{HMIm_4uauoA%=T&5IK;CBhwOgml@7pAk%zha$ZRO3~v0g9Gvz&^{b~ce~K?!XWV`OPC8%2m;+LSU)}e6JfbvgfP0D4H++5dj?|5(UX!z4z#4O4=k{hc&bj7=2BL^AMF&aOLXB(-viU(;E#^}n@RQyW}-{d5FB`zbw!3R{|U`?Q5*#`)bZ{fmJHc4O0x~m0gl;FPGOA{DbipICSVu~tsq>aj*Nl0yANJbXy3s5hJiC+t?|;>Dj4oKQ=zX>*$gf!N+1+s>2>Rkw#$kO4-tD(iJQc^@oqL`PquxwFXI}gAD}Q)v8@lhRIF5yKw07NGj30dJw@)4vE3qN$EX6^SoDs{flV7vlG>v_&nhBo%I%B2aPG*WK&4I75o@;LGFtF(=3KVyE?4O$E%qE~&Jl7u+a@h3bUaD)Zy&5W5mh90gx;DRM+%cMw&mI)Z9EZNC)Tc;;<j`DNui@V&O%mv<ZHJTMpjGUdO{&^1AC-+Efvlup9b;(Hs5JG?8U1eykva}oaSVl^+b|Ve#$mUXdiOcVR>mpcMILwB0pR>VP%=btt~_o%{pgi!KgbY&bIO(PIX<r_|AtAR`WFTTnBQVvP8}1y|3=1ZJthwSty+k*)a=rjAsOBk#mCm8*J<dqRnypkWY-YMf@vZYhxyeZ!OqXG2-1+*lzHg;Y*g)7}e`5!I>L<Z{Ep+h#hbt85h5X>luJ_@NaSEsVw-35Lkrz;}B4pDQ)kwdIxkT1zrQ*UjBwBbU_GCL)KLg&X$|V(3lua7D7#=S0JKd84RE#CZzfd0`IY<U>XEcp$6o&tSegNAp);oUHo{LVGsCvf&U@+C7we|0>06U#$AfG<Ws>r+tJd69XAs@%SF@C#>GzAh(>X)C_Z~Vsp1ZL_)TFT5h7t^_)-fXv%?YeP@FrYSHT8{yyh;nGDS`}yf}f9)9qBfBgGzpVUy)-+U_aN*Rt_EEj=PlE!29+U@73DS#*|(nP`jSg=+sEl&hSJvVxQ^3=^QMQQ6pSnVY2IHnwVZS&vq!GJ3*bt)Q`Gxv#c;Nac}7mASkG49Bx2>FDkIs*V;Z2Uua>L1I1YPKl6-ngm|C++|oUFpZQFB~4A<C6jM1*83A+M;;%fA<~A_n|)T)W6=cETB=-+lGO-qXl+#?{58a`G}U}jW4AhmBxaD6g`3${Dk3IocE#)IMhQY4%>!lklL+@|m%^G|DgWce!$Ev&j1@)mye=oJWEZ5+^r{)vNxG|W*a-+Liob)w#i6>;vitsxn#y)~kc#eqG}uzx@nKf`74&GK6~w#+pDU5mt*ByZ*NV%MA;1D!K5{cHR%(cRf4IE7-a~R~l0Shl@p0cyzfxsBO#c;JC}DwF>sgU*o{gQx)X<~Rhzb!Z2=}`a{d8D#c#Lmd`sbHfAt7Jm#26$=d!}qF*YPBSPLKU`I0BlsS95kj6EWIV`2o*0FWrHaebX<&&ZHhZ7xTZ?8D?OUUM`X)!!^>;a%{%xCiP~+0TxFy|7V1lL<rT6vCfX~{F9r@*XK8vl^VA2Hd^YDM%NudCYxIhv<+Va5FzSDDc+!Z4>ynJ7QE$dQY^}Gwc-s;C0oI8?`HmCmozFmU#vjBKGDWTUNkKSu<Ug6U^P!aM9}7|$5;#fM@72%<^3%18S{{6WSyhU-0iZ3BiM^JgeFun`PZK2hE6DBD8c<#tq#u0q*AB~Pa;|b_3&G_zF5??&$&d#tjj6OhGqm4bAPr9SZU~la-^+JOOH@Vr}C$S$|9sPA3Ord+Cj>owJc!+SI)rX`*VsY5gEk-6P#D3)$ax1IM0=GbTbFVu;VtMYXH_ItemY|p27e;t1e|2H(`=(amKtS0|R1|!tNoxeHE;Wxb-d6#%H2@L@?ty><)Lu^bm9I1EQZ1@GIWCNYD%m0izuY1ATJEqGL)<-ktErnT1`akuOcK^eT5HYY!(-0{`{N3Q{s^?=(nfBwAaD_NGCHdBH96c7x&NY}5Rh4hxWL1cV4+<R`m}=Im+GZZ$v1*l$LJF`|`_QxMiX$>V>&#z_{SY@XA~HU0+Z3G&-|MdPexW-dkt19SlugZUEPeQPc7DAk0*_&gkLJ})#L&2G^CgPv|Pj$A-Eg2()6<5vhm;-)~2`y6gMdfnwq8&IFf#z}GU@!YPq-C4OKyW5SLF}AxM;L1#ABr--x@lSYUNih#WC5@awCvhX9h=sQ?0lz7Znan~*b*+hk5F$t~l?=D+@$a?f#J%OV#*3ii-*^oPRQhFX<g5@^QMYn*sqBu(tbUPsyr*})K_K3;dmIor0%}7ljtmL!(%)yfa3fn<#fVJ=IqzX4W62yK5Qx1Fhq$Rd(ji5aVFav`Tg={$_0~!=3vNe(PHkjB5H?#K<|P(fPKU>?0_F~hwMr4bdQ_k#pKOrHy5%7jPZ6j{Qjs0U02O2yNR%OD0wm?6E~$ArNEi6onPPVf!NSHka1pDWg_`VB#^W^Y9vnh$dIQz~vmk=X;W9`_D5w&tb~JVLG(mrm?@QUQE#gg@Uuzj<J%r24#k*4L<XcGw31y~WyJ>JBgm6~|NEL(1QZeKp%8vR$`hnNZ8av#(lahsOd<J$vHp%|_rb2tK-U<11(|9}D4$xvXLnZU|{P^-$mp8cgQ`Ht>t|XY7yN63Mr|YAC0mX#M#xUR$4wngvFaA+0R5U!Ci)>L*X@;I;LJ&PK#^~&*a`$m$6N-@(MCI(FjjWSMx|I^TS&1MiB3})^&AYU^vMJ1Cr5jrmm0KC=JNxpGK0+4T>3l6t?vx=tN#-hp_v(G<W<}v=p%ic+26E(6*=@`P>075e+2lp&*2ru7X1l>Dug(fGmtGPTz;n3Abx|)0eDDn+^qL#yafT2|&?K!FpnF9u#ivkblykGtA)*;S|B0zGKGlx9TKOflrDLvRNbC%$SZ&JANS7)QEC%p&<bpZ9NK1^!X3QUOi$Y<&tk8?oQSce04F~6&b<<pEj}FQhU6d>er3=85xd5JNCV;|w3?Gix0J?_3Q8N)&D`Y-Iw%q93HF<64Y|ZI`O=%^)LN|JKOy5EUrD5Y=vR`|~oiVW^7V$|2mdzb>jAX^GJNMM8@Q-w;*jcxQAQR`t>mFF9%J9U^1k{+C$Gli5&g@7F-Zgy?YyI>p^JUB2RB8%&=~_Z9?WvL*q3DkcX}ZNZ6eSS@tDlQP$h5BtZOb}@hOJ?vC%`zfGlE}$H%!-(Zh}w-o(BvF2>UKam`lAV$i62Vj8rGFbO$+A7%z)U)mSO-WG5J}o~EAAPpoIaSZOWcugS8j=vLquIS^JB4pifs(yn4F(kRcq6c*(Z9X5^rF%b@uL>V{rappuWR2CLM3ia-wItg{Blt9x4AK$oSFJ1u*i?{-=MyV%ZzXrNh8eKLxAwYJ-ORIt$v`-e6G9ng{)JPvE!gne2vnMPQh!>z&*mO`6H?%wPc=Dowb^~#0qCHBs*D@6U))49%wF1}u&H6bMG+m<Z<z74~v)Y-_ebNEg$g}>ax|_N<B2HegL_S8#+9G-CnXyDnKY{_*%%&KGLGdh$$_I#-S~B2>g$IF&eTlP0fK)amRj1SRwBVg&t4}-H&_hX9hz0djQ4C)H2x#ih>kI54^kQOs%-aie62hBh4L)@yj6B9r;4e!pD4m8#O=MJ$o>}`*F-Y1$E`SxYhhxeYxQcZU7d$2K#?`EAgh|6FWnbWssyYOXY*Hp!35&v^142_sA*N(r+yWt=)e2MAptL(}JeJn#gNSDI)-PWDAkKOtV&|GDXdefN5lJUe4L8md)0$gMk>pv?v52--5y~m@dHQ8xkr8MnVU+!_$i<%9t_4w&7OmVvM7L3UUAzQI?tl0JbK7#{#6czn^uG*9u3XdY0AO(E5~f0Qv1=h3Y2R1uyX*8u5&l`C1xJ}E<#Q<PCnhX(sPRu#?@v8mv?;Y#7VL<<5)be}kC&nRA00IaR(An%a@`7noX(CEJ+_*s(oD0k5i54MoDyR_Os&Bm4D|7e#|`8+hl4|Ds0R3sn=g9dvZ2miRtN6f+bw($Lx(ayMBpr_zUX9IJ*iM9J+d9+`0yYZ<=4wMHQayPMPkQ?q}yyjy@{-r0jG$Fh<gkoD-r~zMo}@(A?el5cklqVeMEqpp;65FLhh`{V|ELiqZ7jRq)=JR4_{k@701|X`67aL$5_8wTD^)o2-|J4dEvV?w`DzXdP6wXvKukh?7+e8wB@QO7jvpYr^JRUzim=Sl_E4IlOXC*Mk6_1Rl9y5<ix{y`q)i|k`ke2eZw6CB;{M_X$_hz6`Jp6kYrIavd*4thcGwZd`@8Tr`3}598Z-cDv8vDL9o>G2~L^0g_dzBB5*x9_?_2bOJ_fCM#TpzXa+{9I<vmosTg;_XY6VTWcwbiQJM;>DF?Hn{|b+p3$Ih|3*quoaY1WAVC{7$kQvepTx|xXO=Q*Fx=tjwO2O`e9zV@}#}1`}{fCGmk+0>0grf<Fr2?--F~@{7#Uth<@!)j~h;2$w3X72f3a<)Bg*Q@73u8ALf7)G+b@fdPu}m7Fy8M!MML%L+I5vcvUq-8>H<b`qvV(eI6mtjdct{gdLv)pd$K5N5jc&>~0#`IRltM>#YAKc3mRKd7_82x1uN6ba8gf1Y)p8o>DqU5yg#`zevclBkW@-B>Hiaha;)$e+zfBosv=Q|tRu(MJ^GdWOJI^Da+>WMdA%~TS*+_0&QYbz_>vjTnarmv>QHM2n^z?qjZeUi0{0I+?^)pw3N_US9l_EvIDah4>s_6<31+2}pzN}3I3$fnPfhFnC(A+^hCwp^i(Toue5J-t|I%kc}O8Vg0P2M@gWHoI`%c`O=g-(1-Lu=Dju^63B^%dO85({e%u=L?{qNIfhJXijQ^Hb#3%1yZkT{(aWH0@Qn>$zQQK7Jil1O!fnvZfM1pQjga(NZwJKs-RMKZzC<49`<NDv5*&#Zgv9DU@R-C?AB{<rtwMuIbp`q?V=f_=|j=8j1|Of&!SOO2Zm{Fw$t_fg37G7o~u`lgJ<1M(1`aZ1NU~44t+~>ML;!8619<+cOEt&YXdRWn##Nz>p(Vz0egMW<%1}Yo3Z$&_@>oWCU47T&_?Oyf`acV>Z(MNa{(^I<!b;pO(K8-(lSCp+nX|rUAxyEbIK>RXoW&+)@IU=J|=wYcOaIs`aZ&UN{x1W{C)~^AvcW(Gc6RxD+_274lAF@Fa0x<EBX1GA${jhJ!c#%8l#MQa*!m$+lTqT}-?>N+(_q<UF5u9RKNL{I|8(r>in_G19$#|Ai<BNJ;@)AC@L<xd<42UnIY}#Hqv1R7_ZRH36k5QlqqhL%d~mrbc(dFG|{!-}%1SmfHEKta6I545L61=TO8(Mh~lX%C=p-$+z?SCi17!3}qkI+Hy^=2a^(pA#_y?a<IflNhDdGBe-@qZi#)o<wM&Qb-Y7(60Tne7{%pEUs4}h6o;Ht<vBVsX1^ak=)nKBS{4e)W`+j9-5`aqd9xd6fk(L0{o!DX#1m?c*kO~RFK-H*6~;1XR#!-Cps;k*@vt-=QxpL0g`y&&r?kQ77j#^3P4O4>5=CrR<>0bfQfYRBN}^5?53VJo<Vu>H<+<&Q3E1;Uh5Iw$$|8Prv!JRg?9efRiO0cYaERq2ZT*(F$x3>p2QP!y+~&;I_;m7ZRMb}JIog_FGi7^I=?Se|Kxed*?338W<xCWCkc1Y>oLF7Uh{BOu4UPmysa~dix>+B4jI@^64(At`EE)@Ptni}-ky5z#=2jIb1O!zSQB2|zA0j-@<p%>E`u)pdJCgt8@;cz6tL#L7Xn58zM-tWz1ojlHKjIU}%2~P|(~RF8mdn74TG&J;rqJ+(PHk@I-b};@g)Om`sRrTQp$A*t&<Kt+`?$$+nGv_J;moTsENnn41IJp|41p<;Ma%_>im(N#->@sn6nHcaK>F?(>E)Z1Rytul1;S&>YA@TfQjxYsTu%uxKu%tUO|Ysb$01F|F#@-5$w4ycoW;nL95|y#Oi<Gk#~;Wt9riVKMRaCJxiP7wVilf|+GU?3Lo0sFhBrARGIzqnIKn?gK7%$bsg^3joiew|07nuc!OdT3WbXDhDv;|P!!6{9aQ-zoCfJ-V3XUjfun{Yyg=#@c98C3=xR9_^0faR;_qlExPX1GAUvA8#WFC3tP`+K3Gu5mhzKR8gi2|$}YFheXS6Y*#Y?C8~jtFC?-{4=`XuD4WqA7>yujO=oK{K^VV;m9{-y}HVH~-%`jH`8I|3Zk1J=?TPJ&^>}jGi6aHy({q3ba+4)oMbHUFeQNzz=VH(nZN{qu0{UUFMS5O$xGZK#xg-)N8ov5SQIH#P9gdqH4DFI0I4JeR|($zDOkSP741y-qR|ZitL^ORz$Wjgg%9gz-RW7e}>YI7=l!WkgCudD!8aN75j4QU?GK&A8m;KR5ie~65{Ssf}B-I!*e3~n%^YQ+{A3DRhn)bC~0ymb1EEk#xv4_I>|j=M@!Nre7K4arowtc4C>$bNN+`)ke8D|BEG41+qLqmq<+mxaVsRADx#IO)zjdjYL}yUR+y5D_vKc>-mC(n2gehKS6n{IC}}XN)rgH7BPMo}A;F4sx-Z*Knu+Yb%jMbwNlSrJ&<XjnI5M09v6OksY(vH&*BokcRu{U*cC5rD8&&8%PY-K3X|YfY*TQ4vF8fq#;_*!Lz!F<gsOnR2eB%@0xCxw2;T%l<VgTc!7VB0>E_cR@%Wb(KWf8slN;T{oyT{V$`*Ks2=<!BfNGt05h>g2>?vs<N6HK?UM#<1o&6^jnhLOi;B_LpV?6sPhYO&>)RXXN$Gy#FU+G$=qdLEZh;Zwr>+1Al$&C`c)F{k7+<2n{{C_z3-UOB~XAROD%j<PHDyJ)oVvbP4Ra7(ZFG*6kUJO;*)2_G)*jQ((~QL|reDMsnNhURpCd`{5u4FO$B%;(z{-HizYtPnZHL8BrfMp<z}xXh1q+;+PKs+4*TL(?v>fjkOiw;FP#uEFTxM>9=9TD<|8p%j0&-Z=Epq+SG%d7?Dw!!Q6;G(^<l9$|p(`}X5ywPg=v;fK7&KE@y0d@tUCarDQ>_Ze3g-v2JwW03orC0s$hT%UA}T)uN)C0Oq>u!x0TOU&cs!k#=At~H9%FgzIao?l-JC+jKhxP(#?fKP$8onQbkIzLkL$}e6%JO&T>#qqnWhxudG#!IwT0!?l@)Xh&T)w`9&PnynxnrOsqt#p(TP^Dnnde+2qluKZ%uBc=v;wrLqc_LPq+g7U`2XUCK#?3CknFABKI%lsHgFag5uWRRA#9*9ZA%2yR%vTzlv~@HmDmYM@hyZ1?*#|ylOTK_IWIA`V5lVX@W~t48PG5v9^0-`9=+xq3ccO`FB`XqXQHvG?Eke!$WMsXe{$eGVPfC$T_{i~q3CWT=yjKVkXljwf2<T%J5kmA*r9aG5@#5$~uz)3gna+RF=7i;xnjqS)5Al?+uk%xFv{9zrOJvE#<8pu7ZnP||AB&`C_P>nnTz}}Ek)EQ!o=EfN<w=q0b7+ZeW{p?nklmb<htsboK17aN#7*0Cxiv%jIzXoc65cK`DZ|5TR(k^^peGXH=TxJ&(WfB1b|C}Az*03iq18LI6fn>pDp>F~z}6(<{K3<2Vap+qm=ALAW=0fFoGB`wamIxMSbOg((^=`R7Gx_T=^dI#TQ~zdFn&o7aZ{p!_QX<GBYtiw#81+!T*MO}lKJV&S~y+tNUvdfJ8ajae)8A1%DQy$^oyW`l6oyxR<R%tJq8=p&Dy6W%PCW`cZt6$THE5)AV<5RkL43SM>Yqf4Gl0PW+eCQS=6exz*E&l2(pF+3mPsEnMef4g#OVfB3Dr4?$vK4bb*@`DM>RFvahjCS*H$~VM|QY%ae{Flz>V=p{xgsm7)X_wWhqEYRlRvh4@nYUO?#7RoB$4U>C?V?l0tYGFCds?nNq2La2TK^g>|#M#LEwCZmD1)W9~wq{5Y`)266~DnK0FS{Jxt$fYro8}K~i9999+=zCaU1f8!C@7F+eCXgplWe2a;S<1;e5}qwrBNYYm+I#U?*$X@c!hC?fo&~8cb#tbT5?L7`BSr@u$(PJmhxvVGu~iugOEOQ6lB*!L944+)vhEQfd}2trhVX3Ho=^@9pKfuP-8vlS{s`>Zmj}RZ^_-Ojz(OL7gurh4BCxqatCZn(gxp+usRPWiEJ&*yt4Bb^#+N4Z9>2>x3~3wq6iK~)f3;N((3YcZNN%YDuzUe6#Z^95A>FBmH&zN^d3WrZsd`Ovt$yRpcAa_%TBa50AwiAWm^m`shHH^ymLua*?JQ=Eb#K{}Z=`lMcR@8v<&u~C1{syyG>t0tcq~+wJ&fe4+C6r1j)cui`1naHYi1=o!6Zb>F{8^{0SHOidQ8{}+n^KwN+$ur0r0j+u9!S$<p`!eV`i!~2s1FUme|uFed|ZmmP%^m(ia{FJWh$)7l6KjRV7NA9kAE!LvYIzqgQRU#k{jrMCKuQo_i}1=2e3Tjg~QV&~imkLDPIY3W6a*)Drzk4%iKGhBj2evGXd;bXyo+#4^4<L13TQ-jKHwDSRQj6M5i#%-%h*$**z$ryB6eghpzWGFa%Oio6<<0>_!%o<1bnYO;YOz*Q(b$q?7xOjl+_v5r7@2CRd|I_T<1wL_B>aEr((5{r$G0#X_gcU{8}l2SQ#CoLW?q6J!Mb?R#@5zN6K4<#p;<{a&9U>1}h*ytv(Qz44*n%_&IK+8OMx>afHq7-<krA;DqylJK!8l+M^UW@cBRf_OK^i^rlmSZKtiU6s8ez`~sFK?H+g5_1(52LKQr=1#NjxgZ4D|L5H>F*lHQsOePNJLT0u~@50QyCWvu#!1Cz?y2(wXoR>Ovw^4iA#+7cj2K;$5{uDP3=+Mb0n9l?0->2RrI-o>Gcyt5a5KKcMNt!ZB}l9TvsPvM_mEJ=*OrE`R~M|$r}q&%yggkF(NHP5)xly1|jgKVm1TJ4d|;Rcg@PkZ@Dyrhy6x2BdE0&>blaMH_}~kZ#d2whSwHFjCJ{Vr-u+cV(e;wxK2rcg4tD;;v&IvoyE&>)ou2XeVeL@n|ZeAGd?PcyBhsI<8(ol(t5m@zgSAEL%7V?ts>aU>8*qO@Amyl8UsBVbFBS)2b?WeLqkrhkYyyTnMv3vmK}DQNJpPFYlaXh(=5UnN)23YQX;4rv=6CJcCwDihTy*%VmS2HV)rRS>5KLo=yj~<nWmjz4DM<V3N_8eSczhv5mNxL{Tf{o<`4xnvvCXi;;uL-^s^MzWh{rOtIG8e#|v7c18fLVguPaDtcxUP+S=fISV8X<RyZ3}KbU<b7!@G^r)>}q^_T`!uOpTZRsbdiB9{?3W}g=?a+mAoHakWMwbr^%1ES{{7G^M@E*1Jij`gl#W~5w~uq83{XLRq|*IF((CdI%A<zB*hc}9f~<LRUdZM+cq9DWQ0{j(_(n6WFCbmP5;e>7T0a-{ukbk8iZAZgv^`oVDdnDQxW_yzdh1rcQ&n&kYP$n-gq^JG&VPuvE!ynh0Jd)iJ2b^78C5G5%c@nR(onw_o&UIN|AzXX!mLmgE+WT*9kt|E^raeDd!lY$p|+^f&tcSl%|i^;Q4hg|btDTeAVhl<=z#=i<#d(aE-l&*!;P#0?Tc^**7#^Js+bn%817Ofmj(t+sGOP$cdNH9b5aSaWXLg-GgX^tK;M8G6^5w)Ccwe$yr{SzW~M(tn@R~8!mdN_%HqN9I-Hm$7D(WzH_zdl+exnbUkl|>A}{k)Q%VtiExTr1wOc{l^`LKKo@ZFElM#^uzVESuA-#l6Ys6j+#osB4g}gcmlK`UY{|GjTX5-V&JH1h|l8`I0t&(GYJ5I8U2xj8Hm-Z*>N*aLP3Bk*YmdS>1-x<{jA&!lj1pQjNA*q8o<=36vr$7o^y|O!pm>A()7_m%KClQ#a5d9rHLRVIDjxv0Lx<X?FU+$cpDmtCn5O#jwFfmoS(nPG`ifm0dJKa8<Y|IvRRh=WjWcbBcL2b&VPT&b-^F6H<!Ff&B8^T0pN+F+Xn*1rk83<Dqq!DWR`ez4umb6UDClQHBc$maf{cyjCusb%`QjhO3c^ln*)AqEi8*75iE3znw<wk-;{L;hF5XObM{0$}^tRx&^aYBAP?(A*gHQYI9hxlAgwb2KmKZ7P>7{FS-E{P?Xc^XUtX$*Q<Bebmf=<&f!=g1xLfQ1J<M3IiO@)ni(B>$~HmU4004(MYEmlphcw(8Q8}_FF=-$l=|A@=_=H_=7nmD4qp<9UaBY{;Zol`1KEa>A1o5Ea@9<SbLyGGgKWEnMbK(v3wg%ik}>7e%$j(a+a<dOv9*$F#VM6CT%vt<Y(GF1xeSJIT?#u*FWMi&-NG3Otg|GEOLgH$m3x7UwQDfVrfA7<xJMek;CBbxP>D;E>*5L?S>zIs0>gvH_V>_v(yEeCrh~qtDjnGqttIW^T`AO}O!L(BJVJzMQv#Hg4)rM>>aLFx=8We!;C<gbnl9#{Ow$W!0-5ZG7Xqm)(2f`;X6G?IcHx>@oWu&6$2F4b?T-Y<))V6)Osfjm2hCX!IYm`5x*iHzr#4WMb{<xdQn|ZO6ZBAuUEBJ284AaFK+uMI)s?h7k<EHYlmrmqFu2-hM4+LToR1!6$?E1Y4qc3%v|S=qCDNN3bRShbO~C~-oWf?1@=mTT*tDMGWiYO(?JONu>Si&YK2F$^l$)afH&bY8@z{mF0>+Zbeo|VG#QWWZ_%P{s$_wkf_CuqNq_)gE>R3bER`@Y7L4v1>86Z+!Bc6MqHxVm~z)~mrso1H}EgDs35aX>vQA-LAtA$Z0x?pF1%sCRspZusvmp23Uqz(b`y~R8v){w?g_*jPhjihO&0-I+Q^6e&dcM>pUM*U&~79t*m{ZN~r*Egq4xu3Rj!MM$`6bdN_eJCT#rPeP2bodaJy*h;8D$^TvbRIsO?4>RP<p2ZUKe7sk3uMupH38~9nI7M9*HptjAcR>V$=RT_etF`lreqrSn}%;F_r4^*R5S|;`qd7WrZ!$|*>p4oPygUhhntu(1?Mmbq;^ky;%GbVmlcx9=DLbPjx+_~STow4bq*giE-{mwg2to%I?iN8rH;8_%OZR+8f<H-8@zUInZZBOxM)Hwju1_P7!YhB>lz{`b%@b63h#s}{2T#+8FP{Sr^6ql$_2ObK7LHYn8RM|?%3jpZW@L)>cnyU6pj!5<9tlV7;R_0I`UOUWk(1hL$5yXtLeNsVN;yCFHK&x&r2WQ&eObF@y+LZ%WHj-w4c6v0)FM5KY2u{c_ck6%KNm}Z@=-^KYsc2eSe<(*WW(=_w;o4Y<IdlJ^lF6?|=W_fBt@(AUeN#y}!Et@cR7f$NguX*iYwIZ$4b#TwZ-{Bl>oK^WpjV_xt51-<|)s|7<c&zPoz&=K0GH*Ka?+)%<^t-|+FZ{`G%t1t50')))
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
