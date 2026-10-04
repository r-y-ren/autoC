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

# Archived public-development proxy; not the author private program.
import json
_DEMO=json.loads('[{"farmer":["PASS"],"hands":[],"market":[["BUY_ANIMAL","COW",1],["BUY_PRODUCT","WHEAT",5],["BUY_ANIMAL","SHEEP",1],["BUY_ANIMAL","SHEEP",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["PICKUP","COW",1],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1],["HIRE"]]},{"farmer":["BUILD_PASTURE"],"hands":[["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","COW",1],["PICKUP","SHEEP",1],["PICKUP","COW",1]],"market":[["SELL","WHEAT",1]]},{"farmer":["PLACE","COW",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["WEST"],["WEST"],["NORTH"],["BUILD_PASTURE"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",1]]},{"farmer":["CARE"],"hands":[["BUILD_PASTURE"],["PLACE","SHEEP",1],["NORTH"],["PLACE","SHEEP",1],["NORTH"]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["WEST"],"hands":[["PLACE","SHEEP",1],["CARE"],["WEST"],["NORTH"],["WEST"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["FEED"],"hands":[["CARE"],["WEST"],["BUILD_PASTURE"],["BUILD_PASTURE"],["NORTH"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["EAST"],"hands":[["NORTH"],["PLANT","MELON"],["PLACE","COW",1],["PLACE","SHEEP",1],["PLANT","MELON"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["NORTH"],["CARE"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["FEED"],"hands":[["PLANT","WHEAT"],["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["PLANT","MELON"],["PLANT","WHEAT"],["PLANT","MELON"],["PLANT","WHEAT"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["FEED"],"hands":[["WEST"],["WATER"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WEST"],["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["PLANT","WHEAT"],["PLANT","MELON"],["WEST"],["PLANT","MELON"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["NORTH"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["NORTH"],["WEST"],["PASS"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PLANT","WHEAT"],["PASS"],["PASS"],["PASS"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["PASS"],"hands":[["WATER"],["PLANT","WHEAT"],["NORTH"],["PLANT","WHEAT"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PLANT","WHEAT"],["WATER"],["PASS"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["SOUTH"],["WATER"],["EAST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["SOUTH"],["PLANT","WHEAT"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["CARE"],"hands":[["DROP"],["EAST"],["CARE"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",2],["DROP"],["PASS"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PASS"],["PASS"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",2],["PASS"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["CARE"],["FEED"],["CARE"]],"market":[]},{"farmer":["PASS"],"hands":[["FEED"],["NORTH"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["FEED"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["PLANT","MELON"],["WEST"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["PLANT","MELON"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["NORTH"],["WEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["DROP"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["SOUTH"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["PLACE","FERTILIZER",1],["DROP"],["WEST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["NORTH"],["WATER"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["CARE"],["SOUTH"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["PICKUP","COW",1],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["NORTH"],["HARVEST"],["HARVEST"],["WATER"]],"market":[["BUY_PRODUCT","WHEAT",1]]},{"farmer":["WATER"],"hands":[["PICKUP","WHEAT",2],["NORTH"],["PLANT","MELON"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["NORTH"],["WATER"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["HARVEST"],["SOUTH"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["BUILD_PASTURE"],["WATER"],["CARE"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["PASS"],["PLACE","COW",1],["EAST"],["FEED"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["SOUTH"],["WATER"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["PASS"],["SOUTH"],["EAST"],["FEED"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["NORTH"],["NORTH"],["NORTH"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["PASS"],["PASS"],["NORTH"],["NORTH"],["WATER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["PASS"],["PASS"],["NORTH"],["PASS"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["SOUTH"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","WHEAT",7]]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["NORTH"],["WEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[["SOUTH"],["SOUTH"],["CARE"],["NORTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["DROP"],["DROP"],["WEST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["NORTH"],["WATER"],["WEST"],["SOUTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["PASS"],["NORTH"],["HARVEST"],["WEST"],["DROP"]],"market":[]},{"farmer":["NORTH"],"hands":[["PASS"],["NORTH"],["EAST"],["WATER"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["BUILD_PASTURE"],"hands":[["PICKUP","COW",1],["WEST"],["FEED"],["WEST"],["CARE"]],"market":[]},{"farmer":["PLACE","COW",1],"hands":[["WEST"],["WEST"],["SOUTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["HARVEST"],["CARE"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["SOUTH"],["FEED"],["WEST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["EAST"],["SOUTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["HARVEST"],["FEED"],["FEED"],["WATER"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["BUILD_PASTURE"],["SOUTH"],["PASS"],["EAST"],["NORTH"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["PLACE","COW",1],["FEED"],["PASS"],["EAST"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["CARE"],["PASS"],["EAST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["EAST"],["PASS"],["EAST"],["PLANT","WHEAT"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["NORTH"],["PASS"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["FEED"],["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[["SELL","WHEAT",2]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["NORTH"],["WEST"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["DROP"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["SOUTH"],["SOUTH"],["WEST"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["CARE"],["SOUTH"],["SOUTH"],["WATER"],["WEST"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["CARE"],"hands":[["PICKUP","COW",1],["EAST"],["SOUTH"],["NORTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["SOUTH"],["DROP"],["NORTH"],["WEST"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["DROP"],["NORTH"],["NORTH"],["WATER"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",2],["NORTH"],["WATER"],["WEST"],["DROP"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["WEST"],["WEST"],["NORTH"],["HARVEST"],["WATER"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"],["CARE"]],"market":[["BUY_SEED","STRAWBERRY",2]]},{"farmer":["FEED"],"hands":[["BUILD_PASTURE"],["FEED"],["WATER"],["SOUTH"],["NORTH"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["PLACE","COW",1],["WEST"],["WEST"],["FEED"],["WATER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["WEST"],["CARE"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["EAST"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["WEST"],["WATER"],["EAST"],["WATER"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["WEST"],["SOUTH"],["EAST"],["PLANT","STRAWBERRY"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["HARVEST"],["WATER"],["WATER"],["FEED"],["EAST"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["PASS"],["SOUTH"],["EAST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["FEED"],["CARE"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["NORTH"],["NORTH"],["SOUTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["SOUTH"],["SOUTH"],["CARE"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["DROP"],["WEST"],["NORTH"],["SOUTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["CARE"],["CARE"],["NORTH"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["CARE"],"hands":[["PICKUP","COW",1],["PICKUP","COW",1],["WATER"],["WEST"],["DROP"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["HARVEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["SOUTH"],["EAST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["WEST"],["WEST"],["EAST"],["FEED"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["FEED"],["SOUTH"],["CARE"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["NORTH"],["WEST"],["CARE"],["SOUTH"],["NORTH"],["DROP"]],"market":[]},{"farmer":["FEED"],"hands":[["BUILD_PASTURE"],["NORTH"],["WEST"],["DROP"],["NORTH"],["PASS"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["PLACE","COW",1],["WEST"],["WATER"],["PASS"],["FEED"],["PASS"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["HARVEST"],["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["PLANT","STRAWBERRY"],["PASS"],["FEED"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["WEST"],["NORTH"],["WATER"],["PASS"],["CARE"],["PASS"]],"market":[]},{"farmer":["CARE"],"hands":[["PLANT","STRAWBERRY"],["WATER"],["NORTH"],["PASS"],["NORTH"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["WATER"],["PASS"],["CARE"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["EAST"],["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WATER"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["WEST"],["PICKUP","WHEAT",3],["NORTH"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["DROP"],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","WOOL",6],["BUY_LAND"]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["DROP"],["CARE"],["FEED"],["EAST"],["EAST"],["NORTH"],["WATER"],["EAST"],["WATER"]],"market":[["SELL","WOOL",6],["BUY_ANIMAL","COW",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["PICKUP","COW",1],["NORTH"],["CARE"],["EAST"],["SOUTH"],["NORTH"],["WEST"],["EAST"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",3]]},{"farmer":["NORTH"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["DROP"],["WATER"],["WATER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",6],["BUY_ANIMAL","COW",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["BUILD_PASTURE"],["SOUTH"],["NORTH"],["WATER"],["PICKUP","COW",1],["EAST"],["WEST"],["PLANT","STRAWBERRY"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLACE","COW",1],["PLACE","FERTILIZER",1],["FEED"],["NORTH"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["FEED"],"hands":[["PICKUP","COW",1],["PICKUP","COW",1],["CARE"],["PLANT","STRAWBERRY"],["EAST"],["WATER"],["EAST"],["EAST"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["WATER"],["BUILD_PASTURE"],["EAST"],["NORTH"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["PLACE","COW",1],["NORTH"],["EAST"],["EAST"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["NORTH"],["SOUTH"],["PLANT","STRAWBERRY"],["BUILD_PASTURE"],["WATER"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","STRAWBERRY",2]]},{"farmer":["DROP"],"hands":[["EAST"],["NORTH"],["DROP"],["WATER"],["PLACE","COW",1],["EAST"],["WATER"],["PLANT","STRAWBERRY"],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["PLANT","STRAWBERRY"],["NORTH"],["EAST"],["EAST"],["EAST"],["PLANT","STRAWBERRY"],["NORTH"],["WATER"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","MELON",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["EAST"],["PLANT","STRAWBERRY"],["PASS"],["WATER"],["WATER"],["SOUTH"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["PLANT","MELON"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["EAST"],["PLANT","STRAWBERRY"],["DROP"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["PLANT","STRAWBERRY"],["CARE"],["WATER"],["NORTH"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["EAST"],["PLANT","STRAWBERRY"],["NORTH"],["WATER"],["EAST"],["WEST"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["WEST"],["SOUTH"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["PASS"],["EAST"],["PLANT","STRAWBERRY"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["EAST"],["WATER"],["PASS"],["WATER"],["PASS"],["PLANT","STRAWBERRY"],["WATER"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["PASS"],["FEED"],["PASS"],["PASS"],["PASS"],["PASS"],["WEST"],["PASS"],["PASS"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PASS"],["CARE"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["CARE"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["CARE"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["DROP"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",3]]},{"farmer":["EAST"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["DROP"],"hands":[["WEST"],["EAST"],["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["DROP"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["NORTH"],["SOUTH"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["DROP"],["CARE"],["DROP"],["SOUTH"],["WEST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["NORTH"],["CARE"],["FEED"],["CARE"],["DROP"],["WATER"],["NORTH"]],"market":[["SELL","FERTILIZER",4]]},{"farmer":["CARE"],"hands":[["FEED"],["PICKUP","WHEAT",3],["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["CARE"],["FEED"],["WATER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["WATER"],["WEST"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","COW",1],["NORTH"],["NORTH"],["PICKUP","COW",1],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["EAST"],["WEST"],["FEED"],["PASS"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["NORTH"],["WATER"],["CARE"],["PASS"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["EAST"],["WEST"],["NORTH"],["PASS"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["BUILD_PASTURE"],["COLLECT_FERTILIZER"],["FEED"],["PASS"],["NORTH"],["DROP"]],"market":[]},{"farmer":["FEED"],"hands":[["SOUTH"],["PLACE","COW",1],["SOUTH"],["CARE"],["PASS"],["WATER"],["PASS"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["SOUTH"],["NORTH"],["EAST"],["NORTH"],["PASS"],["EAST"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["CARE"],["NORTH"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["WEST"],["SOUTH"],["WEST"],["PASS"],["EAST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["SOUTH"],["CARE"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["FEED"],["SOUTH"],["EAST"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PASS"],["DROP"],["EAST"],["PASS"],["EAST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["WATER"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["CARE"],["NORTH"],["NORTH"],["WEST"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",6],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["PICKUP","WHEAT",3],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["PLACE","FERTILIZER",1],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["EAST"],["WEST"],["WEST"],["WATER"],["SOUTH"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["DROP"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["DROP"],["WATER"],["SOUTH"],["SOUTH"]],"market":[["BUY_LAND"]]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["PLACE","FERTILIZER",1],["WEST"],["WATER"],["NORTH"],["EAST"],["DROP"],["SOUTH"]],"market":[["SELL","MILK",5],["BUY_LAND"],["BUY_LAND"]]},{"farmer":["FEED"],"hands":[["CARE"],["PASS"],["PASS"],["WATER"],["EAST"],["NORTH"],["WATER"],["WEST"],["DROP"]],"market":[["SELL","FERTILIZER",5],["BUY_PRODUCT","WHEAT",3],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["PICKUP","WHEAT",2]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["FEED"],["PASS"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["SOUTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["PICKUP","WHEAT",2],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["FEED"],["NORTH"],["SOUTH"],["NORTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["NORTH"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WATER"],["NORTH"],["FEED"],["WATER"],["WEST"],["SOUTH"],["WATER"],["WEST"],["WEST"]],"market":[["BUY_ANIMAL","GOOSE",1]]},{"farmer":["CARE"],"hands":[["WEST"],["CARE"],["NORTH"],["SOUTH"],["WATER"],["DROP"],["NORTH"],["WATER"],["PLANT","STRAWBERRY"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["CARE"],["PLANT","WHEAT"],["SOUTH"],["PICKUP","GOOSE",1],["WATER"],["SOUTH"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["FEED"],["WATER"],["WATER"],["SOUTH"],["WEST"],["SOUTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["SOUTH"],["FEED"],["WEST"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["EAST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["SOUTH"],["CARE"],["WEST"],["PLANT","WHEAT"],["NORTH"],["BUILD_COOP"],["WEST"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["PLACE","GOOSE",1],["WEST"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["WEST"],["CARE"],["SOUTH"],["PASS"],["SOUTH"],["WEST"],["SOUTH"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["DROP"],["WATER"],["WEST"],["PLANT","WHEAT"],["PASS"],["PLANT","MELON"],["PASS"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_PRODUCT","WHEAT",6]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",2],["WEST"],["WATER"],["WATER"],["SOUTH"],["PLANT","STRAWBERRY"],["SOUTH"],["WATER"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["PASS"],["PASS"],["PASS"],["WATER"],["WATER"],["PASS"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",5],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",5]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["FEED"],["WEST"],["PICKUP","WHEAT",3],["WEST"],["PLACE","FERTILIZER",1],["SOUTH"],["PICKUP","WHEAT",4],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["CARE"],["FEED"],["NORTH"],["HARVEST"],["EAST"],["SOUTH"],["NORTH"],["WEST"]],"market":[["SELL","WOOL",4],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["DROP"],["NORTH"],["CARE"],["NORTH"],["EAST"],["NORTH"],["WATER"],["FEED"],["WATER"]],"market":[["SELL","WOOL",4],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["PICKUP","GOOSE",1],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"],["DROP"],["WEST"],["PLANT","STRAWBERRY"],["WEST"],["WATER"]],"market":[["SELL","WOOL",4],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["WEST"],["NORTH"],["CARE"],["PICKUP","GOOSE",1],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["EAST"],"hands":[["BUILD_COOP"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["DROP"],["WEST"],["NORTH"],["WATER"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["PLACE","GOOSE",1],["FEED"],["EAST"],["WEST"],["WEST"],["PICKUP","WHEAT",2],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["PICKUP","GOOSE",1],"hands":[["NORTH"],["CARE"],["SOUTH"],["FEED"],["WEST"],["PICKUP","GOOSE",1],["WATER"],["FEED"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WEST"],["PLACE","FERTILIZER",2],["CARE"],["BUILD_COOP"],["WEST"],["SOUTH"],["CARE"],["EAST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["BUILD_COOP"],"hands":[["SOUTH"],["NORTH"],["CARE"],["WEST"],["PLACE","GOOSE",1],["WEST"],["PLANT","STRAWBERRY"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["PLACE","GOOSE",1],"hands":[["WEST"],["WATER"],["FEED"],["NORTH"],["NORTH"],["FEED"],["WATER"],["WATER"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PICKUP","GOOSE",1],"hands":[["PLANT","STRAWBERRY"],["WEST"],["PICKUP","GOOSE",1],["COLLECT_FERTILIZER"],["WATER"],["CARE"],["WEST"],["EAST"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["FEED"],["PICKUP","WHEAT",2],["CARE"],["SOUTH"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WEST"],["CARE"],["NORTH"],["FEED"],["SOUTH"],["NORTH"],["WATER"],["EAST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["BUILD_COOP"],"hands":[["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["PLANT","STRAWBERRY"],["WEST"],["NORTH"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLACE","GOOSE",1],"hands":[["PLANT","STRAWBERRY"],["EAST"],["NORTH"],["CARE"],["PLANT","STRAWBERRY"],["NORTH"],["PLANT","WHEAT"],["EAST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["PLANT","STRAWBERRY"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["FEED"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["PLANT","STRAWBERRY"],["SOUTH"],["NORTH"],["WEST"],["PLANT","STRAWBERRY"],["CARE"],["NORTH"],["EAST"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[["PLANT","STRAWBERRY"],["SOUTH"],["FEED"],["WATER"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WATER"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["PLANT","STRAWBERRY"],["DROP"],["SOUTH"],["SOUTH"],["PLANT","STRAWBERRY"],["WEST"],["WATER"],["EAST"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["WATER"],["PASS"],["WATER"],["PASS"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["WEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["WEST"],["EAST"],["WEST"],["NORTH"],["WEST"]],"market":[["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",9]]},{"farmer":["WATER"],"hands":[["WEST"],["FEED"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["WEST"],["WATER"],["NORTH"],["PICKUP","WHEAT",4],["NORTH"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WEST"],["CARE"],["FEED"],["WEST"],["WEST"],["EAST"],["WEST"],["NORTH"],["WEST"],["DROP"],["NORTH"]],"market":[["SELL","MILK",3]]},{"farmer":["EAST"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["CARE"],["SOUTH"],["WEST"],["WATER"],["WEST"],["FEED"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",9]]},{"farmer":["EAST"],"hands":[["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["EAST"],["NORTH"],["CARE"],["HARVEST"],["PICKUP","WHEAT",4],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["EAST"],["WEST"],["WATER"]],"market":[["SELL","MELON",6],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["EAST"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["HARVEST"]],"market":[["BUY_PRODUCT","WHEAT",14]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["WEST"],["SOUTH"],["EAST"],["WATER"],["EAST"],["NORTH"],["EAST"],["NORTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["DROP"],["CARE"],["FEED"],["FEED"],["EAST"],["NORTH"],["EAST"],["WATER"],["DROP"],["FEED"],["SOUTH"]],"market":[["SELL","MELON",6],["SELL","MELON",6]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["CARE"],["CARE"],["EAST"],["WATER"],["SOUTH"],["WEST"],["WEST"],["CARE"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["DROP"],["NORTH"],["EAST"],["HARVEST"],["CARE"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","MELON",6]]},{"farmer":["CARE"],"hands":[["NORTH"],["WATER"],["WEST"],["SOUTH"],["PICKUP","WHEAT",3],["WATER"],["DROP"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"]],"market":[["SELL","MELON",6],["SELL","MELON",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["EAST"],["FERTILIZE"],["SOUTH"],["WEST"],["NORTH"],["WEST"],["FEED"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WATER"],["WATER"],["WATER"],["WEST"],["WATER"],["SOUTH"],["CARE"],["PLANT","WHEAT"],["NORTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["NORTH"],["WEST"],["WEST"],["WATER"],["WEST"],["SOUTH"],["SOUTH"],["WEST"],["FEED"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["CARE"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["FEED"],["WEST"],["WATER"],["WEST"],["PLANT","WHEAT"],["WEST"],["WEST"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["CARE"],["WATER"],["SOUTH"],["WEST"],["WATER"],["WATER"],["WATER"],["DROP"],["WEST"],["NORTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FERTILIZE"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["NORTH"],["FEED"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["WATER"],["FERTILIZE"],["NORTH"],["WATER"],["WATER"],["WEST"],["WATER"],["CARE"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","MILK",3]]},{"farmer":["NORTH"],"hands":[["CARE"],["NORTH"],["WATER"],["NORTH"],["SOUTH"],["EAST"],["SOUTH"],["WEST"],["WATER"],["EAST"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["PASS"],["WATER"],["PASS"],["WATER"],["SOUTH"],["PASS"],["PASS"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["NORTH"],["PICKUP","WHEAT",4],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",6],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["FEED"],["FEED"],["FEED"],["WEST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["CARE"],["CARE"],["WEST"],["WEST"],["FEED"],["SOUTH"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WEST"],["NORTH"],["SOUTH"],["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["CARE"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["FEED"],["NORTH"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["CARE"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["CARE"],["FEED"],["NORTH"],["NORTH"],["WEST"],["WEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["DROP"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["CARE"],["CARE"],["NORTH"],["WATER"],["FEED"],["FEED"],["WEST"]],"market":[["SELL","MELON",6]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["NORTH"],["SOUTH"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["CARE"],["CARE"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["CARE"],["HARVEST"],["NORTH"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["CARE"],["WEST"],["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WEST"],["WATER"],["WATER"],["FEED"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["PLANT","WHEAT"],["NORTH"],["WEST"],["SOUTH"],["FERTILIZE"],["EAST"],["WEST"],["WEST"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["EAST"],["WEST"],["WATER"],["WATER"],["EAST"],["WATER"],["HARVEST"],["FEED"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["EAST"],["FERTILIZE"],["HARVEST"],["WEST"],["EAST"],["WEST"],["FEED"],["CARE"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["EAST"],["WATER"],["SOUTH"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["FEED"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["PLANT","WHEAT"],["EAST"],["WATER"],["NORTH"],["WATER"],["EAST"],["PLANT","WHEAT"],["EAST"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WATER"],["WATER"],["WEST"],["WEST"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["WATER"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["NORTH"],["EAST"],["WEST"],["NORTH"],["DROP"],["SOUTH"],["WATER"]],"market":[["SELL","MILK",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLANT","WHEAT"],["WATER"],["HARVEST"],["PASS"],["WATER"],["WEST"],["PASS"],["EAST"],["WEST"],["PASS"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["SOUTH"],["PLANT","WHEAT"],["PASS"],["SOUTH"],["WATER"],["PASS"],["EAST"],["WATER"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["SOUTH"],["PASS"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",14],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["NORTH"],["EAST"],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",6],["SELL","MELON",6],["HIRE"],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["DROP"],["FEED"],["FEED"],["WEST"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4]],"market":[["SELL","MILK",3]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",4],["CARE"],["CARE"],["WEST"],["HARVEST"],["EAST"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","WOOL",4]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["NORTH"],["SOUTH"],["CARE"],["HARVEST"],["EAST"],["SOUTH"],["CARE"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["EAST"],["CARE"],["HARVEST"],["SOUTH"],["EAST"],["WATER"],["FEED"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["WEST"],["SOUTH"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["FERTILIZE"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["CARE"],["FEED"],["FEED"],["DROP"],["NORTH"],["WATER"],["CARE"],["WATER"]],"market":[["SELL","MILK",6],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["CARE"],["CARE"],["PICKUP","WHEAT",2],["WEST"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["WATER"],["WATER"],["FEED"]],"market":[]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["SOUTH"],["HARVEST"],["NORTH"],["WEST"],["WEST"],["CARE"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["WATER"],["WATER"],["NORTH"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["FEED"],["WATER"],["SOUTH"],["SOUTH"],["HARVEST"],["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["NORTH"],["WEST"],["FERTILIZE"],["CARE"],["WATER"],["FERTILIZE"],["FEED"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WEST"],["FEED"],["SOUTH"],["WATER"],["CARE"],["HARVEST"]],"market":[]},{"farmer":["EAST"],"hands":[["WEST"],["EAST"],["WEST"],["WATER"],["EAST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["HARVEST"],["SOUTH"],["HARVEST"],["HARVEST"],["CARE"],["NORTH"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["FEED"],["WATER"],["PLANT","STRAWBERRY"],["PASS"],["FEED"],["EAST"],["WATER"],["WEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["CARE"],["NORTH"],["WATER"],["NORTH"],["SOUTH"],["NORTH"],["HARVEST"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["PASS"],["PASS"],["WATER"],["PLANT","WHEAT"],["WEST"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["EAST"],["EAST"],["PASS"],["PASS"],["EAST"],["WATER"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["WATER"],["WATER"],["PASS"],["DROP"],["WATER"],["PASS"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","MILK",5],["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",6],["EAST"],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","MELON",6],["SELL","FERTILIZER",2],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["HARVEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["PICKUP","WHEAT",4],["WEST"],["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["FEED"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["CARE"],["HARVEST"],["CARE"],["EAST"],["HARVEST"],["WEST"],["NORTH"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["SOUTH"],["WEST"],["NORTH"],["EAST"],["SOUTH"],["FERTILIZE"],["HARVEST"],["NORTH"],["FEED"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["HARVEST"],["CARE"],["WATER"],["WATER"],["WATER"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["WEST"],["SOUTH"],["WEST"],["CARE"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["SOUTH"],["CARE"],["FEED"],["WATER"],["WATER"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["FEED"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["WATER"],["EAST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["CARE"],["HARVEST"],["FERTILIZE"],["WATER"],["WEST"],["SOUTH"],["SOUTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["PLANT","WHEAT"],["WATER"],["NORTH"],["WATER"],["WATER"],["DROP"],["WATER"],["WEST"]],"market":[["SELL","MILK",6],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["WEST"],["WATER"],["WATER"],["WEST"],["WATER"],["HARVEST"],["HARVEST"],["WEST"],["NORTH"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WEST"],["WEST"],["HARVEST"],["WEST"],["PLANT","STRAWBERRY"],["PLANT","STRAWBERRY"],["WEST"],["FERTILIZE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WATER"],["FEED"],["WATER"],["WATER"],["WATER"],["NORTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["HARVEST"],["HARVEST"],["CARE"],["WEST"],["WEST"],["EAST"],["HARVEST"],["NORTH"],["FEED"]],"market":[["SELL","MILK",3]]},{"farmer":["WEST"],"hands":[["FEED"],["PLANT","WHEAT"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WATER"],["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["WATER"],["CARE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["NORTH"],["WATER"],["SOUTH"],["WATER"],["NORTH"],["EAST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["WATER"],["FERTILIZE"],["EAST"],["FERTILIZE"],["NORTH"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WATER"],["SOUTH"],["PASS"],["WATER"],["WATER"],["WATER"],["EAST"],["WATER"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PASS"],["PASS"],["SOUTH"],["EAST"],["WATER"],["PASS"],["SOUTH"],["SOUTH"]],"market":[["SELL","WHEAT",7]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","MILK",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["NORTH"],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",5],["HIRE"]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["DROP"],["FEED"],["WEST"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"],["PICKUP","WHEAT",4]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["CARE"],["WEST"],["HARVEST"],["SOUTH"],["SOUTH"],["EAST"],["WEST"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["DROP"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["CARE"]],"market":[["SELL","MILK",6]]},{"farmer":["FEED"],"hands":[["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["PICKUP","WHEAT",3],["SOUTH"],["EAST"],["HARVEST"],["SOUTH"],["FEED"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["CARE"],["DROP"],["NORTH"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["HARVEST"],["FEED"],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["WATER"],["NORTH"],["NORTH"],["FEED"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["WATER"],["EAST"],["FEED"],["NORTH"],["CARE"]],"market":[["SELL","MILK",3]]},{"farmer":["CARE"],"hands":[["EAST"],["FEED"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["CARE"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["WEST"],["WEST"],["CARE"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["WATER"],["WATER"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WEST"],["HARVEST"],["NORTH"],["EAST"],["WEST"],["WEST"],["FEED"],["WATER"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["WATER"],["WATER"],["WATER"],["CARE"],["HARVEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["WATER"],["FEED"],["NORTH"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WEST"],["WEST"],["CARE"],["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["NORTH"],["WEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["NORTH"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"],["NORTH"],["WATER"],["HARVEST"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["DROP"],"hands":[["WATER"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["EAST"],["WATER"],["EAST"],["WEST"],["HARVEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["WEST"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["SOUTH"],["HARVEST"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["SOUTH"],"hands":[["WEST"],["SOUTH"],["NORTH"],["FERTILIZE"],["EAST"],["FERTILIZE"],["NORTH"],["WATER"],["FEED"],["EAST"]],"market":[["SELL","MILK",3]]},{"farmer":["HARVEST"],"hands":[["PASS"],["EAST"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["PASS"],["SOUTH"],["CARE"],["SOUTH"]],"market":[["SELL","WHEAT",12]]},{"farmer":["PASS"],"hands":[["WATER"],["WATER"],["WATER"],["EAST"],["PASS"],["PASS"],["PASS"],["PASS"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","EGG",8]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","WOOL",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","FERTILIZER",4],["PICKUP","WHEAT",4],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",4],["WEST"],["PICKUP","FERTILIZER",4]],"market":[["SELL","WOOL",1],["SELL","EGG",8],["SELL","EGG",6],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["DROP"],["EAST"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["PICKUP","FERTILIZER",4],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["PICKUP","WHEAT",4],["NORTH"],["CARE"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["PICKUP","FERTILIZER",4],["WEST"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["EAST"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["PICKUP","FERTILIZER",4],["NORTH"],["FEED"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["FERTILIZE"],["NORTH"],["EAST"],["SOUTH"],["EAST"],["WATER"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["CARE"],["WATER"],["WEST"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"],["CARE"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["SOUTH"],["NORTH"],["NORTH"],["WATER"],["WEST"],["EAST"],["WEST"],["NORTH"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["FERTILIZE"],["HARVEST"],["EAST"],["WATER"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["CARE"],["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WEST"],["FERTILIZE"],["HARVEST"],["FEED"],["WEST"],["FEED"]],"market":[["SELL","MILK",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["CARE"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["FEED"],["FEED"],["FERTILIZE"],["FEED"],["NORTH"],["WATER"],["NORTH"],["WATER"],["EAST"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["CARE"],["WATER"],["CARE"],["FERTILIZE"],["WEST"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["WEST"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WEST"],["WATER"],["WATER"],["FERTILIZE"],["WEST"],["FERTILIZE"],["SOUTH"],["NORTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["FERTILIZE"],["WEST"],["WEST"],["WATER"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["HARVEST"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["WEST"],["FERTILIZE"],["NORTH"],["HARVEST"],["EAST"],["HARVEST"],["WEST"],["PLANT","WHEAT"],["PLANT","WHEAT"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["WEST"],["WATER"],["WATER"],["PLANT","WHEAT"],["FERTILIZE"],["PLANT","WHEAT"],["WEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["WATER"],["WEST"],["WEST"],["NORTH"],["WATER"],["NORTH"],["WATER"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["WATER"],["NORTH"],["WEST"],["HARVEST"],["WATER"],["SOUTH"],["FERTILIZE"],["NORTH"],["SOUTH"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["EAST"],["SOUTH"],["SOUTH"],["WEST"],["EAST"],["WEST"],["NORTH"],["FEED"],["NORTH"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["EAST"],["HARVEST"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["EAST"],["CARE"],["EAST"],["WATER"]],"market":[["SELL","WHEAT",7]]},{"farmer":["EAST"],"hands":[["PASS"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["WEST"],["SOUTH"],["PASS"],["PASS"],["HARVEST"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","MILK",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",3],"hands":[["EAST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["EAST"],["NORTH"],["EAST"]],"market":[["SELL","MILK",6],["SELL","FERTILIZER",6],["SELL","FERTILIZER",2],["HIRE"],["HIRE"]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["WATER"],["FEED"],["WEST"],["WEST"],["EAST"],["HARVEST"],["EAST"],["NORTH"],["EAST"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["CARE"],["WEST"],["FEED"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["NORTH"],["PLACE","MILK",3],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["HARVEST"],["PICKUP","WHEAT",3],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["DROP"],["SOUTH"],["FEED"],["CARE"],["HARVEST"],["HARVEST"],["NORTH"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","MELON",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","WHEAT",3],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["CARE"],["FEED"],["HARVEST"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["HARVEST"],["FERTILIZE"],["HARVEST"],["CARE"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["FEED"],["CARE"],["WEST"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["FEED"],["HARVEST"]],"market":[["SELL","MILK",3]]},{"farmer":["FERTILIZE"],"hands":[["PLANT","WHEAT"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["WEST"],["HARVEST"],["WEST"],["SOUTH"],["NORTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["CARE"],["WATER"],["WEST"],["WATER"],["WEST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["WEST"],["NORTH"],["DROP"],["WEST"],["HARVEST"],["HARVEST"],["DROP"],["NORTH"],["SOUTH"]],"market":[["SELL","STRAWBERRY",8]]},{"farmer":["FEED"],"hands":[["FEED"],["WATER"],["FERTILIZE"],["FEED"],["PICKUP","WHEAT",2],["WEST"],["WEST"],["WEST"],["WEST"],["NORTH"],["SOUTH"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["CARE"],["NORTH"],["WEST"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["DROP"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["FERTILIZE"],["SOUTH"],["WEST"],["WEST"],["HARVEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["FERTILIZE"],["WEST"],["FEED"],["WATER"],["SOUTH"],["WATER"],["WEST"],["EAST"],["EAST"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["SOUTH"],["WATER"],["WATER"],["CARE"],["EAST"],["SOUTH"],["SOUTH"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","MILK",6]]},{"farmer":["CARE"],"hands":[["EAST"],["WATER"],["EAST"],["NORTH"],["WEST"],["WATER"],["WEST"],["HARVEST"],["HARVEST"],["EAST"],["EAST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["EAST"],["NORTH"],["WATER"],["CARE"],["NORTH"],["DROP"],["SOUTH"],["PLANT","WHEAT"],["HARVEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",8],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WATER"],["WATER"],["EAST"],["FEED"],["WATER"],["WEST"],["HARVEST"],["WATER"],["EAST"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["NORTH"],["HARVEST"],["HARVEST"],["NORTH"],["NORTH"],["PICKUP","WHEAT",2],["EAST"],["SOUTH"],["HARVEST"],["NORTH"]],"market":[["SELL","MILK",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["WATER"],["PLANT","WHEAT"],["CARE"],["EAST"],["WATER"],["FEED"],["SOUTH"],["HARVEST"],["SOUTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2],["SELL","WHEAT",7]]},{"farmer":["FEED"],"hands":[["PASS"],["NORTH"],["WATER"],["PASS"],["PASS"],["PASS"],["CARE"],["PASS"],["PASS"],["PASS"],["NORTH"]],"market":[["SELL","WHEAT",7],["SELL","WHEAT",4]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["PICKUP","FERTILIZER",4],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","WOOL",3],["SELL","FERTILIZER",6],["HIRE"],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["CARE"],"hands":[["FEED"],["DROP"],["WEST"],["CARE"],["EAST"],["SOUTH"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["PICKUP","WHEAT",4],["WEST"],["FEED"],["EAST"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["FEED"],["NORTH"],["WATER"],["FERTILIZE"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["WATER"],["WEST"],["WATER"],["NORTH"],["WEST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["FEED"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["WATER"],["WEST"],["FERTILIZE"],["HARVEST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["SOUTH"],["HARVEST"],["FEED"],["EAST"],["WATER"],["WATER"],["PLANT","WHEAT"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["SOUTH"],["WATER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["NORTH"],["FERTILIZE"],["FERTILIZE"],["WEST"],["EAST"],["PLANT","WHEAT"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["EAST"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["SOUTH"],["HARVEST"],["WATER"],["NORTH"],["WEST"],["WEST"],["HARVEST"],["EAST"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["EAST"],["FEED"],["CARE"],["WEST"],["WATER"],["WATER"],["FERTILIZE"],["NORTH"],["WATER"],["FERTILIZE"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["NORTH"],["NORTH"],["WATER"],["FEED"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["NORTH"],"hands":[["NORTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WEST"],["CARE"],["WATER"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["CARE"],["HARVEST"],["WEST"],["NORTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["PLANT","WHEAT"],["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["WEST"],["WEST"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["WATER"],["WATER"],["WEST"],["WATER"],["WEST"],["HARVEST"],["WEST"],["FERTILIZE"]],"market":[["SELL","MILK",6]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["SOUTH"],["WEST"],["WATER"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["HARVEST"],"hands":[["WEST"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["FERTILIZE"],["HARVEST"],["FERTILIZE"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["WEST"],["WEST"],["WEST"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["FERTILIZE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["FERTILIZE"],["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"],["WATER"],["EAST"],["NORTH"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["FEED"],["WATER"],["FERTILIZE"],["SOUTH"],["SOUTH"],["SOUTH"],["EAST"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","WHEAT",7]]},{"farmer":["PASS"],"hands":[["CARE"],["EAST"],["WATER"],["PASS"],["PASS"],["EAST"],["WATER"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","SHEEP",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",4],["HARVEST"],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","FERTILIZER",6],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["WEST"],["PLACE","MILK",3],["NORTH"],["WEST"],["WEST"],["NORTH"],["NORTH"],["EAST"],["PICKUP","SHEEP",1],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["SOUTH"],["PICKUP","WHEAT",3],["NORTH"],["HARVEST"],["SOUTH"],["NORTH"],["NORTH"],["EAST"],["WEST"],["EAST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["HARVEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["WEST"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["SOUTH"],["WEST"],["FEED"],["NORTH"],["SOUTH"],["SOUTH"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["FEED"],"hands":[["HARVEST"],["FEED"],["FERTILIZE"],["CARE"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"],["EAST"],["EAST"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["WEST"],["HARVEST"],["HARVEST"],["HARVEST"],["BUILD_PASTURE"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["HARVEST"],["WEST"],["WEST"],["HARVEST"],["EAST"],["FERTILIZE"],["WEST"],["EAST"],["WEST"],["PLACE","SHEEP",1],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["CARE"],["FERTILIZE"],["FEED"],["SOUTH"],["HARVEST"],["WATER"],["FEED"],["HARVEST"],["WEST"],["CARE"],["WEST"]],"market":[["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["FEED"],["WEST"],["FERTILIZE"],["SOUTH"],["NORTH"],["FERTILIZE"],["CARE"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["DROP"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["DROP"],["FEED"],["WEST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["WEST"],["NORTH"],["WEST"],["NORTH"],["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"],["CARE"],["SOUTH"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WEST"],"hands":[["NORTH"],["HARVEST"],["WATER"],["WATER"],["DROP"],["DROP"],["FERTILIZE"],["WEST"],["WEST"],["NORTH"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",8],["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["HARVEST"],["EAST"],["PICKUP","WHEAT",2],["WATER"],["HARVEST"],["WEST"],["EAST"],["NORTH"],["DROP"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["NORTH"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"],["WEST"],["WEST"],["DIG"],["WEST"],["EAST"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["DROP"],["WATER"],["WATER"],["NORTH"],["FEED"],["FERTILIZE"],["PLANT","WHEAT"],["DROP"],["EAST"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",8]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["HARVEST"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["WATER"],["PICKUP","WHEAT",2],["EAST"],["WATER"],["NORTH"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["WATER"],"hands":[["EAST"],["NORTH"],["WATER"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["EAST"],["HARVEST"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["FEED"],["NORTH"],["HARVEST"],["WATER"],["FERTILIZE"],["NORTH"],["NORTH"],["PLANT","WHEAT"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["NORTH"],["PLANT","WHEAT"],["CARE"],["EAST"],["WEST"],["NORTH"],["WATER"],["FEED"],["HARVEST"],["WATER"],["NORTH"]],"market":[["SELL","MILK",6]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["NORTH"],["SOUTH"],["CARE"],["NORTH"],["NORTH"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",9]]},{"farmer":["HARVEST"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["PASS"],["NORTH"],["FERTILIZE"],["WATER"],["PASS"],["PASS"],["HARVEST"],["WATER"],["WATER"]],"market":[["SELL","EGG",13],["SELL","WHEAT",9]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",4],["WEST"],["PICKUP","FERTILIZER",4]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["EAST"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["NORTH"]],"market":[["SELL","STRAWBERRY",5]]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["WATER"],["WEST"],["EAST"],["WEST"],["EAST"],["PICKUP","WHEAT",3],["SOUTH"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["HARVEST"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["FEED"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["HARVEST"],["CARE"],["FEED"],["PLANT","WHEAT"],["SOUTH"],["FERTILIZE"],["NORTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","MILK",2]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["HARVEST"],["NORTH"],["FERTILIZE"],["FERTILIZE"],["FEED"],["CARE"],["FERTILIZE"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["WEST"],["HARVEST"],["NORTH"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["NORTH"],["EAST"],["CARE"],["FEED"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["FEED"],["HARVEST"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["FERTILIZE"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["WEST"],["CARE"],["NORTH"],["HARVEST"],["FERTILIZE"],["NORTH"],["WATER"],["FEED"],["CARE"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["FERTILIZE"],["WEST"],["FERTILIZE"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["CARE"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["NORTH"],["FERTILIZE"],["CARE"],["WATER"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["WATER"],["SOUTH"],["HARVEST"],["EAST"],["NORTH"],["WATER"],["WATER"],["WATER"],["EAST"],["SOUTH"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["NORTH"],["EAST"],["WATER"],["PLANT","WHEAT"],["FERTILIZE"],["EAST"],["FERTILIZE"],["WEST"],["NORTH"],["FERTILIZE"],["WATER"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["WATER"],["EAST"],["WATER"],["WATER"],["NORTH"],["NORTH"],["WEST"],["WATER"],["WATER"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["WATER"],["WEST"],["EAST"],["EAST"],["WATER"],["HARVEST"],["FERTILIZE"],["EAST"],["WATER"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["HARVEST"],["HARVEST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"],["EAST"],["WEST"],["FERTILIZE"]],"market":[]},{"farmer":["SOUTH"],"hands":[["FERTILIZE"],["EAST"],["PLANT","WHEAT"],["WATER"],["FERTILIZE"],["EAST"],["WATER"],["WATER"],["WATER"],["NORTH"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["DROP"],["WATER"],["HARVEST"],["EAST"],["NORTH"],["HARVEST"],["SOUTH"],["NORTH"],["FERTILIZE"],["WEST"],["WEST"]],"market":[["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["NORTH"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["FERTILIZE"],["DROP"],["WEST"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["WEST"]],"market":[["SELL","STRAWBERRY",10]]},{"farmer":["HARVEST"],"hands":[["EAST"],["HARVEST"],["EAST"],["WATER"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["WEST"],["EAST"],["WATER"],["WEST"]],"market":[["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["EAST"],["FERTILIZE"],["EAST"],["SOUTH"],["NORTH"],["SOUTH"],["EAST"],["NORTH"],["HARVEST"]],"market":[["SELL","EGG",10],["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["PASS"],["HARVEST"],["WEST"],["PASS"],["PASS"],["HARVEST"],["PASS"],["WATER"],["SOUTH"],["SOUTH"],["FERTILIZE"],["CARE"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["WEST"],["WEST"],["WEST"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["EAST"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["HARVEST"],["FEED"],["FEED"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["CARE"],["CARE"],["HARVEST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["FEED"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["HARVEST"],["CARE"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["EAST"],["SOUTH"],["NORTH"],["HARVEST"],["HARVEST"],["WEST"],["FERTILIZE"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["EAST"],["FEED"],["FEED"],["WEST"],["NORTH"],["HARVEST"],["WATER"],["SOUTH"],["HARVEST"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["WEST"],["NORTH"],["WEST"],["WEST"],["SOUTH"],["SOUTH"],["FEED"],["FERTILIZE"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["DROP"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["CARE"],"hands":[["SOUTH"],["PICKUP","WHEAT",2],["SOUTH"],["NORTH"],["WEST"],["NORTH"],["WEST"],["WEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["DROP"],["DROP"],["WATER"],["HARVEST"],["DROP"],["WEST"],["CARE"],["NORTH"]],"market":[["SELL","STRAWBERRY",12]]},{"farmer":["NORTH"],"hands":[["DROP"],["HARVEST"],["WEST"],["HARVEST"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"],["DIG"],["NORTH"],["DROP"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",10]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",3],["SOUTH"],["WATER"],["PLANT","WHEAT"],["NORTH"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["EAST"],["EAST"],["WATER"],["DIG"]],"market":[["SELL","MILK",3]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["WEST"],["WATER"],["EAST"],["EAST"],["HARVEST"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["EAST"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["FEED"],["NORTH"],["WEST"],["SOUTH"],["FERTILIZE"],["NORTH"],["EAST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WEST"],["WATER"],["CARE"],["EAST"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["WEST"],["HARVEST"]],"market":[["SELL","WOOL",2]]},{"farmer":["HARVEST"],"hands":[["FEED"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["FEED"],["HARVEST"],["WEST"],["NORTH"],["HARVEST"],["WATER"],["DIG"]],"market":[["SELL","EGG",5]]},{"farmer":["WEST"],"hands":[["CARE"],["WATER"],["NORTH"],["SOUTH"],["NORTH"],["CARE"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["NORTH"],["SOUTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WATER"],["HARVEST"],["EAST"],["WATER"],["EAST"],["EAST"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PLANT","WHEAT"],["WEST"],["WEST"],["EAST"],["EAST"],["EAST"],["SOUTH"],["HARVEST"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["FERTILIZE"],["WATER"],["FERTILIZE"],["FERTILIZE"],["EAST"],["DROP"],["EAST"],["SOUTH"],["EAST"],["HARVEST"],["WATER"],["SOUTH"]],"market":[["SELL","WHEAT",13],["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["PASS"],["WATER"],["SOUTH"],["HARVEST"],["EAST"],["WATER"],["HARVEST"],["WEST"],["PASS"],["FERTILIZE"]],"market":[["SELL","EGG",4]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",11],["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["PICKUP","FERTILIZER",3],["NORTH"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",2],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["WATER"],["HARVEST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["PICKUP","WHEAT",2]],"market":[["SELL","MILK",2]]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["CARE"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["FERTILIZE"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["FEED"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["HARVEST"],["NORTH"],["EAST"],["FERTILIZE"],["SOUTH"],["WATER"],["FERTILIZE"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["SOUTH"],["WEST"],["FEED"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["WATER"],["NORTH"],["CARE"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FEED"],["FEED"],["NORTH"],["CARE"],["NORTH"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["SOUTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"],["EAST"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["HARVEST"],["CARE"],["NORTH"],["NORTH"],["WATER"],["WEST"],["FEED"],["HARVEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"],["HARVEST"],["CARE"],["PLANT","WHEAT"],["EAST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","MILK",4]]},{"farmer":["HARVEST"],"hands":[["WATER"],["SOUTH"],["WEST"],["HARVEST"],["WATER"],["WEST"],["EAST"],["WEST"],["WEST"],["EAST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["SOUTH"],["FERTILIZE"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["EAST"],["DIG"],["NORTH"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["WEST"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["WATER"],["HARVEST"]],"market":[["SELL","WOOL",2],["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["WEST"],["WATER"],["WEST"],["HARVEST"],["NORTH"],["DROP"],["WATER"],["NORTH"],["SOUTH"],["PLANT","WHEAT"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["WATER"],"hands":[["WEST"],["NORTH"],["EAST"],["WEST"],["WEST"],["WEST"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"],["WATER"]],"market":[["SELL","EGG",8]]},{"farmer":["SOUTH"],"hands":[["WEST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["NORTH"],["FERTILIZE"],["DIG"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["HARVEST"],["SOUTH"],["HARVEST"],["WEST"],["WATER"],["EAST"],["WATER"],["PLANT","WHEAT"],["WEST"],["WATER"]],"market":[["SELL","WOOL",2],["SELL","MILK",1]]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["EAST"],["DROP"],["WEST"],["WATER"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",7]]},{"farmer":["SOUTH"],"hands":[["PASS"],["WATER"],["FERTILIZE"],["WATER"],["PASS"],["WATER"],["PASS"],["FERTILIZE"],["SOUTH"],["PASS"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",5],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["EAST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["PICKUP","FERTILIZER",4],["EAST"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["WEST"],["WEST"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","WOOL",1]]},{"farmer":["CARE"],"hands":[["HARVEST"],["CARE"],["WEST"],["FEED"],["EAST"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["DIG"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["HARVEST"],["WEST"],["NORTH"],["NORTH"],["HARVEST"],["WATER"],["WEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["PLANT","WHEAT"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["DIG"],["FERTILIZE"],["EAST"],["COLLECT_FERTILIZER"],["DIG"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["HARVEST"],["HARVEST"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["FEED"],["HARVEST"],["SOUTH"],["DIG"],["NORTH"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["HARVEST"],["CARE"],["FEED"],["CARE"],["DIG"],["FERTILIZE"],["PLANT","WHEAT"],["EAST"],["NORTH"],["NORTH"],["PLANT","WHEAT"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["DIG"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["EAST"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["PLANT","WHEAT"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"],["NORTH"],["WEST"],["DIG"],["DIG"],["NORTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["CARE"],["WEST"],["FERTILIZE"],["NORTH"],["FERTILIZE"],["HARVEST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WEST"],["DIG"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FERTILIZE"],["NORTH"],["HARVEST"],["WATER"],["DIG"],["WEST"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["WEST"],["WATER"],["FEED"],["DIG"],["WEST"],["PLANT","WHEAT"],["FERTILIZE"],["EAST"],["NORTH"],["HARVEST"],["WATER"]],"market":[["SELL","WOOL",2]]},{"farmer":["CARE"],"hands":[["WEST"],["WEST"],["SOUTH"],["CARE"],["PLANT","WHEAT"],["WATER"],["WATER"],["WATER"],["HARVEST"],["EAST"],["PLANT","WHEAT"],["EAST"]],"market":[["SELL","WHEAT",9],["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["DROP"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["FERTILIZE"],["NORTH"],["WEST"],["DIG"],["HARVEST"],["WATER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","WHEAT",2],["WATER"],["WEST"],["WEST"],["WEST"],["WEST"],["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"],["DIG"],["NORTH"],["DIG"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WEST"],"hands":[["EAST"],["SOUTH"],["FERTILIZE"],["HARVEST"],["HARVEST"],["NORTH"],["DIG"],["WEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","MILK",4]]},{"farmer":["HARVEST"],"hands":[["EAST"],["SOUTH"],["WATER"],["SOUTH"],["DIG"],["WATER"],["PLANT","WHEAT"],["FERTILIZE"],["EAST"],["WATER"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["SOUTH"],["EAST"],["EAST"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"],["NORTH"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["HARVEST"],["EAST"],["FERTILIZE"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WEST"],["WATER"],["EAST"],["WEST"],["SOUTH"],["DIG"],["HARVEST"],["DIG"],["HARVEST"],["SOUTH"],["DIG"]],"market":[["SELL","WOOL",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["HARVEST"],["DIG"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["PLANT","WHEAT"],["DIG"],["SOUTH"],["PASS"]],"market":[["SELL","WHEAT",13],["SELL","WHEAT",5]]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["EAST"],["WATER"],["WATER"],["WATER"],["PASS"],["PASS"],["WEST"]],"market":[["SELL","EGG",8]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","FERTILIZER",4],["SELL","EGG",2],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["HARVEST"],["WEST"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",3],["SOUTH"],["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["PLANT","WHEAT"],["WEST"],["WEST"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["CARE"],["CARE"],["FEED"],["WATER"],["WATER"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WEST"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["CARE"],["NORTH"],["WEST"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["CARE"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["DIG"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["FEED"],["FEED"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["FERTILIZE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["HARVEST"],["CARE"],["FEED"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",2]]},{"farmer":["WEST"],"hands":[["CARE"],["CARE"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["HARVEST"],["WEST"],["WEST"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["FERTILIZE"],["FEED"],["FERTILIZE"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WEST"],["WATER"],["HARVEST"],["WATER"],["WATER"],["WATER"],["CARE"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["HARVEST"],["SOUTH"],["WEST"],["WEST"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["FEED"],["WATER"],["SOUTH"],["WEST"],["WATER"],["SOUTH"],["WEST"],["DIG"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["EAST"],["CARE"],["WEST"],["FEED"],["NORTH"],["HARVEST"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["WATER"],["CARE"],["FEED"],["NORTH"],["FERTILIZE"],["NORTH"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["EAST"],["HARVEST"],["HARVEST"],["CARE"],["WATER"],["WATER"],["WATER"],["WEST"],["FERTILIZE"]],"market":[["SELL","MILK",5],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["PLANT","CARROT"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["SOUTH"],["WEST"],["WATER"],["NORTH"]],"market":[["SELL","EGG",4]]},{"farmer":["NORTH"],"hands":[["WATER"],["DROP"],["NORTH"],["EAST"],["WEST"],["PLANT","WHEAT"],["FERTILIZE"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["EAST"],"hands":[["SOUTH"],["NORTH"],["WEST"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"]],"market":[["SELL","EGG",8]]},{"farmer":["HARVEST"],"hands":[["WATER"],["EAST"],["WEST"],["DROP"],["FEED"],["EAST"],["HARVEST"],["PLANT","CARROT"],["WATER"],["PASS"]],"market":[["SELL","WOOL",3],["SELL","FERTILIZER",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["HARVEST"],["NORTH"],["EAST"],["CARE"],["FERTILIZE"],["PLANT","CARROT"],["WATER"],["EAST"],["SOUTH"]],"market":[["SELL","WOOL",1],["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["PASS"],["DROP"],["FERTILIZE"],["PASS"],["PASS"],["PASS"],["WATER"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","WHEAT",5]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","WOOL",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",3],["WEST"],["NORTH"]],"market":[["SELL","MILK",8],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["WEST"],["NORTH"],["EAST"],["SOUTH"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[["SELL","WOOL",1]]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["SOUTH"],["WEST"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["EAST"],["HARVEST"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["FERTILIZE"],["DIG"],["HARVEST"],["WEST"],["NORTH"],["WATER"],["WEST"]],"market":[["SELL","WOOL",2]]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["PLANT","WHEAT"],["DIG"],["WATER"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",1]]},{"farmer":["CARE"],"hands":[["WATER"],["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["NORTH"],["PLANT","WHEAT"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WEST"],["FEED"],["NORTH"],["FERTILIZE"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["PLANT","WHEAT"],["FEED"],["CARE"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["EAST"],["NORTH"],["WEST"]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["WATER"],["CARE"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["DIG"],["WATER"],["NORTH"],["FERTILIZE"],["FEED"],["WATER"]],"market":[["SELL","WOOL",1]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["NORTH"],["HARVEST"],["PLANT","WHEAT"],["FERTILIZE"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["WATER"],["CARE"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["WATER"],["WATER"],["WATER"],["EAST"],["EAST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["HARVEST"],["WEST"],["EAST"],["NORTH"],["WEST"],["WEST"],["WATER"],["FERTILIZE"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",4]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["EAST"],["FERTILIZE"],["EAST"],["FERTILIZE"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","WHEAT",13]]},{"farmer":["WEST"],"hands":[["WATER"],["EAST"],["WEST"],["SOUTH"],["WATER"],["DIG"],["WEST"],["PLANT","WHEAT"],["EAST"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["DROP"],["WEST"],["FERTILIZE"],["NORTH"],["PLANT","CARROT"],["WATER"],["WATER"],["WATER"],["EAST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["FEED"],["EAST"]],"market":[["SELL","WOOL",3],["SELL","STRAWBERRY",2]]},{"farmer":["PLANT","WHEAT"],"hands":[["HARVEST"],["DROP"],["SOUTH"],["EAST"],["SOUTH"],["WEST"],["SOUTH"],["EAST"],["PLANT","WHEAT"],["CARE"],["FERTILIZE"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["SOUTH"],["NORTH"],["WATER"],["FERTILIZE"],["WEST"],["WATER"],["WATER"],["EAST"],["WATER"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["SELL","EGG",8]]},{"farmer":["WEST"],"hands":[["SOUTH"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["FEED"],["SOUTH"],["WEST"],["FERTILIZE"]],"market":[]},{"farmer":["WATER"],"hands":[["DROP"],["HARVEST"],["PLANT","CARROT"],["EAST"],["SOUTH"],["NORTH"],["NORTH"],["CARE"],["WATER"],["NORTH"],["EAST"]],"market":[["SELL","MILK",6],["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["NORTH"],["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"]],"market":[["SELL","WHEAT",8]]},{"farmer":["FERTILIZE"],"hands":[["PASS"],["HARVEST"],["SOUTH"],["EAST"],["PASS"],["WATER"],["HARVEST"],["DROP"],["SOUTH"],["EAST"],["CARE"]],"market":[["SELL","WHEAT",9]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","WHEAT",16],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["PICKUP","FERTILIZER",3],["WEST"],["NORTH"]],"market":[["SELL","WOOL",2],["SELL","FERTILIZER",2],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["EAST"],["DROP"],["WEST"],["FEED"],["EAST"],["HARVEST"],["EAST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["FEED"],"hands":[["FERTILIZE"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["PICKUP","WHEAT",3],["FEED"],["NORTH"],["HARVEST"],["HARVEST"],["NORTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["CARE"],["FEED"],["PLANT","WHEAT"],["WEST"],["FERTILIZE"],["HARVEST"],["WATER"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["FEED"],"hands":[["WATER"],["CARE"],["COLLECT_FERTILIZER"],["CARE"],["EAST"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["EAST"],["SOUTH"],["WEST"],["HARVEST"],["WATER"],["DIG"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["FEED"],["WEST"],["HARVEST"],["PLANT","WHEAT"],["FERTILIZE"],["NORTH"],["WATER"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["CARE"],["CARE"],["CARE"],["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"],["WEST"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["SOUTH"],["EAST"],["WATER"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","WOOL",1]]},{"farmer":["NORTH"],"hands":[["PLANT","CARROT"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["EAST"],["HARVEST"],["CARE"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WEST"],["WATER"],["WEST"],["WEST"],["DIG"],["FERTILIZE"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["FERTILIZE"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["NORTH"],["HARVEST"],["WEST"],["FERTILIZE"],["WEST"],["PLANT","CARROT"],["WATER"],["WATER"],["SOUTH"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["WATER"],["NORTH"],["FEED"],["WATER"],["NORTH"],["EAST"],["FEED"],["WEST"],["WATER"]],"market":[["SELL","EGG",8]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["CARE"],["WEST"],["WATER"],["EAST"],["CARE"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["PLANT","CARROT"],["WEST"],["FERTILIZE"],["NORTH"],["DROP"],["HARVEST"],["EAST"],["EAST"],["EAST"],["WATER"],["WATER"]],"market":[["SELL","EGG",2]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["DIG"],["WATER"],["EAST"],["FEED"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["NORTH"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["NORTH"],["SOUTH"],["CARE"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",9]]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["SOUTH"],["FERTILIZE"],["EAST"],["WATER"],["WATER"],["DROP"],["SOUTH"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["PLANT","CARROT"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["NORTH"],["EAST"],["SOUTH"],["WEST"],["SOUTH"],["FEED"],["PLANT","CARROT"],["EAST"]],"market":[["SELL","WHEAT",5]]},{"farmer":["WATER"],"hands":[["PLANT","CARROT"],["WEST"],["WATER"],["WATER"],["EAST"],["HARVEST"],["WEST"],["SOUTH"],["CARE"],["WEST"],["EAST"]],"market":[["SELL","MILK",6]]},{"farmer":["EAST"],"hands":[["WATER"],["FERTILIZE"],["EAST"],["WEST"],["FERTILIZE"],["WEST"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"]],"market":[["SELL","WHEAT",5]]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["HARVEST"],["PASS"],["WATER"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["DROP"],["SOUTH"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","WHEAT",16],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["WEST"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","WOOL",2],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["WEST"],["NORTH"],["WATER"],["HARVEST"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["SOUTH"],["FEED"],["HARVEST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["WEST"],["FEED"],["CARE"],["PLANT","WHEAT"],["HARVEST"],["SOUTH"],["WEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WEST"],"hands":[["WATER"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["WEST"],["FERTILIZE"],["HARVEST"],["WATER"],["WEST"],["EAST"]],"market":[["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["HARVEST"],["WATER"],["WATER"],["PLANT","WHEAT"],["EAST"],["WEST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WEST"],["FEED"],["CARE"],["DROP"],["HARVEST"],["SOUTH"],["WATER"],["WATER"],["FERTILIZE"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"],["FERTILIZE"],["NORTH"],["HARVEST"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["WATER"],["WATER"],["FEED"],["PLANT","CARROT"],["SOUTH"],["HARVEST"]],"market":[["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["WEST"],["NORTH"],["NORTH"],["SOUTH"],["WEST"],["CARE"],["WATER"],["WATER"],["PLANT","CARROT"]],"market":[["SELL","WOOL",1]]},{"farmer":["FERTILIZE"],"hands":[["PLANT","CARROT"],["HARVEST"],["WEST"],["FEED"],["HARVEST"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["WATER"],["DIG"],["WATER"],["CARE"],["EAST"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["FERTILIZE"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PLANT","WHEAT"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["PLANT","CARROT"],["WEST"],["WATER"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["WATER"],["WEST"],["NORTH"],["PLANT","WHEAT"],["WATER"],["DIG"],["HARVEST"],["EAST"],["SOUTH"],["HARVEST"]],"market":[["SELL","WOOL",1]]},{"farmer":["WATER"],"hands":[["PLANT","CARROT"],["EAST"],["FERTILIZE"],["DIG"],["WATER"],["EAST"],["PLANT","CARROT"],["PLANT","CARROT"],["WATER"],["WATER"],["PLANT","CARROT"]],"market":[["SELL","WHEAT",5]]},{"farmer":["WEST"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["PLANT","CARROT"],["SOUTH"],["EAST"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["WATER"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["WEST"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["EAST"],["PLANT","CARROT"],["PLANT","CARROT"],["SOUTH"]],"market":[["SELL","WOOL",1],["BUY_SEED","CARROT",6],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["NORTH"],["FERTILIZE"],["NORTH"],["WEST"],["EAST"],["DIG"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"]],"market":[["SELL","EGG",6]]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["WATER"],["WATER"],["DROP"],["DROP"],["PLANT","CARROT"],["WATER"],["NORTH"],["EAST"],["SOUTH"]],"market":[["SELL","WHEAT",5]]},{"farmer":["PLANT","CARROT"],"hands":[["EAST"],["NORTH"],["SOUTH"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"]],"market":[["SELL","MILK",6],["SELL","WHEAT",13]]},{"farmer":["WATER"],"hands":[["HARVEST"],["NORTH"],["WATER"],["PLANT","CARROT"],["NORTH"],["DROP"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["WEST"]],"market":[["SELL","EGG",10]]},{"farmer":["EAST"],"hands":[["PASS"],["EAST"],["HARVEST"],["WATER"],["PASS"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["PASS"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","WHEAT",24],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["WEST"],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",3],["WEST"]],"market":[["SELL","WOOL",3],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["PLACE","MILK",3],["NORTH"],["FEED"],["WEST"],["HARVEST"],["EAST"],["HARVEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","WOOL",1]]},{"farmer":["DROP"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["SOUTH"],["NORTH"],["EAST"],["SOUTH"],["NORTH"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",4]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["WEST"],["EAST"],["COLLECT_FERTILIZER"],["FEED"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["SOUTH"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["CARE"],"hands":[["WEST"],["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["WATER"],["NORTH"],["FERTILIZE"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["PLANT","CARROT"],["CARE"],["SOUTH"],["NORTH"],["FERTILIZE"],["HARVEST"],["FERTILIZE"],["WATER"],["PLANT","CARROT"],["HARVEST"]],"market":[["SELL","WHEAT",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WATER"],["WEST"],["FEED"],["HARVEST"],["WATER"],["PLANT","CARROT"],["WATER"],["WEST"],["WATER"],["PLANT","CARROT"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["EAST"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["NORTH"],["WATER"],["NORTH"],["WATER"]],"market":[["SELL","MILK",4]]},{"farmer":["FEED"],"hands":[["FERTILIZE"],["WATER"],["CARE"],["WEST"],["EAST"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["PLANT","CARROT"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["PLANT","CARROT"],["WEST"],["WATER"],["NORTH"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["WEST"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["WATER"],["WATER"],["FERTILIZE"],["SOUTH"],["WATER"],["FERTILIZE"],["PLANT","CARROT"],["EAST"],["EAST"],["WATER"],["HARVEST"]],"market":[["SELL","WOOL",2],["SELL","STRAWBERRY",2]]},{"farmer":["FEED"],"hands":[["HARVEST"],["WEST"],["WEST"],["WATER"],["HARVEST"],["WATER"],["WATER"],["WATER"],["NORTH"],["HARVEST"],["PLANT","CARROT"]],"market":[["SELL","CARROT",10]]},{"farmer":["CARE"],"hands":[["PLANT","CARROT"],["WEST"],["WATER"],["SOUTH"],["PLANT","CARROT"],["NORTH"],["NORTH"],["HARVEST"],["WATER"],["EAST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["FEED"],["SOUTH"],["WATER"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["HARVEST"],["EAST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["HARVEST"],["HARVEST"],["SOUTH"],["WEST"],["NORTH"],["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",1]]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["FEED"],["SOUTH"],["PLANT","WHEAT"],["FEED"],["WEST"],["NORTH"],["WEST"],["WATER"],["EAST"],["SOUTH"]],"market":[["SELL","WHEAT",5]]},{"farmer":["WATER"],"hands":[["WATER"],["DROP"],["SOUTH"],["WATER"],["CARE"],["WATER"],["DROP"],["WATER"],["EAST"],["SOUTH"],["HARVEST"]],"market":[["SELL","EGG",4]]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["WATER"],["NORTH"],["WEST"],["HARVEST"],["HARVEST"],["HARVEST"],["EAST"],["DROP"],["EAST"]],"market":[["SELL","WHEAT",10],["SELL","FERTILIZER",2]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["NORTH"],["HARVEST"],["WEST"],["WEST"],["PLANT","WHEAT"],["DROP"],["PASS"],["EAST"],["NORTH"],["FERTILIZE"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2],["SELL","WHEAT",10]]},{"farmer":["WATER"],"hands":[["NORTH"],["CARE"],["NORTH"],["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["EAST"],"hands":[["WATER"],["PASS"],["FERTILIZE"],["PASS"],["NORTH"],["PASS"],["PASS"],["PASS"],["DROP"],["HARVEST"],["WATER"]],"market":[["SELL","WHEAT",10],["SELL","WHEAT",4]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","WHEAT",20],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",3],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","MILK",5],["SELL","STRAWBERRY",2],["SELL","WHEAT",5],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["SOUTH"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["HARVEST"],["NORTH"],["EAST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["NORTH"],"hands":[["EAST"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["WEST"],["FERTILIZE"],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","WOOL",1]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["WEST"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["WEST"],["NORTH"],["WEST"],["SOUTH"],["EAST"],["HARVEST"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["SOUTH"],["FERTILIZE"],["WEST"],["WEST"],["FERTILIZE"],["EAST"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","WOOL",4],["SELL","STRAWBERRY",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["WATER"],["FEED"],["WATER"],["FERTILIZE"],["WEST"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["FERTILIZE"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["NORTH"],["WATER"],["EAST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["WEST"],["HARVEST"],["FERTILIZE"],["WATER"],["NORTH"],["FERTILIZE"],["WEST"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","WOOL",4]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["WEST"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["FERTILIZE"],["WATER"],["WEST"]],"market":[["SELL","MILK",2]]},{"farmer":["HARVEST"],"hands":[["WEST"],["HARVEST"],["WATER"],["WATER"],["FEED"],["HARVEST"],["EAST"],["WATER"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["DROP"],["SOUTH"],["HARVEST"],["HARVEST"],["SOUTH"],["EAST"],["WATER"],["WEST"],["SOUTH"],["WEST"]],"market":[["SELL","CARROT",10]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["SOUTH"],["FERTILIZE"],["EAST"],["HARVEST"],["WEST"],["WATER"],["WEST"]],"market":[["SELL","MILK",4]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["EAST"],["SOUTH"],["WEST"],["EAST"],["SOUTH"],["FERTILIZE"],["SOUTH"],["SOUTH"]],"market":[["SELL","WHEAT",8]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["HARVEST"],["WATER"],["EAST"],["FERTILIZE"],["FEED"],["WATER"],["WATER"],["SOUTH"],["DROP"]],"market":[["SELL","CARROT",8]]},{"farmer":["EAST"],"hands":[["EAST"],["WEST"],["SOUTH"],["EAST"],["EAST"],["EAST"],["HARVEST"],["HARVEST"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",5]]},{"farmer":["HARVEST"],"hands":[["WATER"],["WATER"],["WATER"],["EAST"],["WATER"],["DROP"],["WEST"],["EAST"],["WEST"],["EAST"]],"market":[["SELL","WOOL",3],["SELL","EGG",4],["SELL","EGG",4]]},{"farmer":["EAST"],"hands":[["EAST"],["HARVEST"],["HARVEST"],["EAST"],["SOUTH"],["WEST"],["NORTH"],["PASS"],["SOUTH"],["EAST"]],"market":[["SELL","WHEAT",5],["SELL","FERTILIZER",1]]},{"farmer":["EAST"],"hands":[["HARVEST"],["EAST"],["EAST"],["SOUTH"],["PASS"],["HARVEST"],["HARVEST"],["PASS"],["DROP"],["PASS"]],"market":[["SELL","WHEAT",10],["SELL","CARROT",3]]},{"farmer":["WEST"],"hands":[],"market":[["SELL","CARROT",20],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["WEST"],["NORTH"],["NORTH"],["WEST"],["WEST"],["NORTH"]],"market":[["SELL","CARROT",20],["SELL","WHEAT",20],["HIRE"]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["WEST"],["HARVEST"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["SOUTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"]],"market":[["SELL","MILK",5]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["NORTH"],["SOUTH"],["WATER"],["NORTH"],["FERTILIZE"],["WATER"],["SOUTH"],["NORTH"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WEST"],["HARVEST"],["SOUTH"],["HARVEST"],["FERTILIZE"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["EAST"],["WATER"],["WEST"],["WATER"],["HARVEST"],["SOUTH"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["EAST"],["WATER"],["SOUTH"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["SOUTH"],"hands":[["WEST"],["HARVEST"],["WEST"],["HARVEST"],["WEST"],["NORTH"],["HARVEST"],["FERTILIZE"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["NORTH"],["SOUTH"],["FERTILIZE"],["EAST"],["WATER"],["WATER"],["EAST"],["WATER"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["WEST"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["EAST"],["HARVEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["WEST"],["HARVEST"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["WEST"],["HARVEST"],["SOUTH"]],"market":[["SELL","MILK",3]]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["NORTH"],["DROP"],["SOUTH"],["WEST"],["EAST"],["WATER"],["SOUTH"],["DROP"]],"market":[["SELL","EGG",8],["SELL","EGG",4]]},{"farmer":["EAST"],"hands":[["SOUTH"],["DROP"],["EAST"],["NORTH"],["SOUTH"],["WEST"],["DROP"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WHEAT",10],["SELL","FERTILIZER",2],["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["NORTH"],["NORTH"],["NORTH"],["EAST"],["WEST"],["NORTH"],["NORTH"],["EAST"],["DROP"]],"market":[["SELL","WHEAT",14]]},{"farmer":["EAST"],"hands":[["EAST"],["NORTH"],["EAST"],["NORTH"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WOOL",1],["SELL","CARROT",8]]},{"farmer":["NORTH"],"hands":[["EAST"],["NORTH"],["DROP"],["WEST"],["DROP"],["DROP"],["PASS"],["NORTH"],["DROP"],["NORTH"]],"market":[["SELL","CARROT",9],["SELL","CARROT",9],["SELL","FERTILIZER",2]]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["PASS"],["WEST"],["NORTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","CARROT",5],["SELL","WHEAT",14]]},{"farmer":["PASS"],"hands":[["DROP"],["SOUTH"],["PASS"],["COLLECT_FERTILIZER"],["PASS"],["NORTH"],["NORTH"],["EAST"],["PASS"],["EAST"]],"market":[["SELL","CARROT",6],["SELL","FERTILIZER",2],["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["PASS"],["NORTH"],["PASS"],["EAST"],["PASS"],["NORTH"],["EAST"],["DROP"],["PASS"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","CARROT",5],["SELL","WHEAT",6],["SELL","EGG",5]]},{"farmer":["PASS"],"hands":[["PASS"],["SOUTH"],["PASS"],["EAST"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]}]')
_PROXY=make_agent({0:_DEMO})
def archived_proxy_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
archived_proxy_agent.telemetry=_PROXY.chassis.diagnostics
agent=archived_proxy_agent
