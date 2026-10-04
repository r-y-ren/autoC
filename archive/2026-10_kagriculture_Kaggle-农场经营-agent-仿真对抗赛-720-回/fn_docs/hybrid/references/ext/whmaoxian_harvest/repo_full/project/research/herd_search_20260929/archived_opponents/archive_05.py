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
_DEMO=json.loads('[{"farmer":["PASS"],"hands":[],"market":[["BUY_ANIMAL","COW",1],["BUY_PRODUCT","WHEAT",5],["BUY_ANIMAL","SHEEP",1],["BUY_ANIMAL","SHEEP",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["PICKUP","COW",1],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1],["HIRE"]]},{"farmer":["BUILD_PASTURE"],"hands":[["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","COW",1],["PICKUP","SHEEP",1],["PICKUP","COW",1]],"market":[["SELL","WHEAT",1]]},{"farmer":["PLACE","COW",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["WEST"],["WEST"],["NORTH"],["BUILD_PASTURE"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",1]]},{"farmer":["CARE"],"hands":[["BUILD_PASTURE"],["PLACE","SHEEP",1],["NORTH"],["PLACE","SHEEP",1],["NORTH"]],"market":[["BUY_SEED","MELON",2],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["WEST"],"hands":[["PLACE","SHEEP",1],["CARE"],["WEST"],["WEST"],["WEST"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["FEED"],"hands":[["CARE"],["WEST"],["BUILD_PASTURE"],["BUILD_PASTURE"],["PLANT","MELON"]],"market":[]},{"farmer":["EAST"],"hands":[["SOUTH"],["NORTH"],["PLACE","COW",1],["PLACE","SHEEP",1],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PLANT","MELON"],["NORTH"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["WATER"],["WEST"],["PLANT","MELON"],["PLANT","WHEAT"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["SOUTH"],"hands":[["PLANT","MELON"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["WEST"],"hands":[["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"],["WEST"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["WEST"],["PLANT","MELON"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["PLANT","MELON"],["WEST"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["SELL","WHEAT",2]]},{"farmer":["CARE"],"hands":[["WATER"],["PASS"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["PASS"],"hands":[["WEST"],["PLANT","WHEAT"],["WEST"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["WEST"],["WATER"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["NORTH"],["WEST"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PLANT","WHEAT"],["NORTH"],["NORTH"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WATER"],["PLANT","WHEAT"],["PASS"],["PASS"],["PASS"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["SOUTH"],["WATER"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["DROP"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["CARE"],"hands":[["PICKUP","WHEAT",2],["PICKUP","WHEAT",2],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["CARE"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["EAST"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WEST"],["DROP"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["FEED"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["CARE"],["FEED"]],"market":[]},{"farmer":["PLANT","MELON"],"hands":[["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["PLANT","MELON"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["WEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["DROP"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["DROP"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["WEST"],["WATER"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["WATER"],"hands":[["PICKUP","COW",1],["CARE"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["SOUTH"],["NORTH"],["HARVEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["PASS"],["SOUTH"],["WATER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["BUILD_PASTURE"],["PASS"],["SOUTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["PLACE","COW",1],["PASS"],["CARE"],["NORTH"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["PASS"],["FEED"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["SOUTH"],["PASS"],["EAST"],["HARVEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["NORTH"],["FEED"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["NORTH"],["PASS"],["PASS"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PLANT","WHEAT"],["PASS"],["PLANT","WHEAT"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WATER"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",7],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["NORTH"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["DROP"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[["SOUTH"],["EAST"],["WEST"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["DROP"],["DROP"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["SOUTH"],["WEST"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["WEST"],["SOUTH"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WEST"],["EAST"],["WATER"],["FEED"]],"market":[]},{"farmer":["BUILD_PASTURE"],"hands":[["NORTH"],["NORTH"],["SOUTH"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["PLACE","COW",1],"hands":[["WEST"],["NORTH"],["DROP"],["SOUTH"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["PASS"],["FEED"],["CARE"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["WATER"],["WEST"],["PASS"],["CARE"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["PASS"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["PASS"],["SOUTH"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["HARVEST"],["PLANT","STRAWBERRY"],["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PLANT","STRAWBERRY"],["WATER"],["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["PASS"],["CARE"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["NORTH"],["SOUTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["DROP"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[["SOUTH"],["EAST"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["DROP"],["DROP"],["WEST"],["WEST"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["SOUTH"],["WEST"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["SOUTH"],["NORTH"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["BUILD_PASTURE"],"hands":[["NORTH"],["WATER"],["EAST"],["WATER"],["DROP"],["NORTH"]],"market":[]},{"farmer":["PLACE","COW",1],"hands":[["WATER"],["WEST"],["SOUTH"],["WEST"],["PASS"],["FEED"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["DROP"],["WEST"],["PASS"],["CARE"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["PICKUP","WHEAT",2],["WATER"],["PICKUP","WHEAT",2],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["NORTH"],["WEST"],["NORTH"],["PICKUP","COW",1],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["FEED"],["WATER"],["WEST"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["WEST"],["HARVEST"],["WEST"],["CARE"]],"market":[]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["FEED"],["PASS"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["WEST"],["PASS"],["CARE"],["PASS"],["WEST"],["FEED"]],"market":[]},{"farmer":["CARE"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["NORTH"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["BUILD_PASTURE"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PLACE","COW",1],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["CARE"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["NORTH"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["PLACE","FERTILIZER",1],["NORTH"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["CARE"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["SOUTH"],["EAST"],["WEST"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["PLACE","FERTILIZER",1],["PLACE","FERTILIZER",1],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["PASS"],["PASS"],["SOUTH"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["CARE"],"hands":[["PICKUP","COW",1],["PICKUP","COW",1],["EAST"],["FEED"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["PICKUP","WHEAT",3],["SOUTH"],["CARE"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["SOUTH"],["NORTH"],["DROP"],["EAST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["DROP"],["NORTH"],["NORTH"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["WEST"],["FEED"],["PICKUP","WHEAT",2],["WEST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["CARE"],["NORTH"],["FEED"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["WEST"],["NORTH"],["CARE"],["NORTH"],["DROP"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["WEST"],["FEED"],["NORTH"],["WEST"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["BUILD_PASTURE"],["WEST"],["CARE"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["PLACE","COW",1],["WEST"],["NORTH"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["WATER"],["NORTH"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["NORTH"],["FEED"],["WEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["NORTH"],["PASS"],["WATER"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["WEST"],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["PLACE","FERTILIZER",1],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","WOOL",6],["BUY_LAND"]]},{"farmer":["NORTH"],"hands":[["DROP"],["NORTH"],["FEED"],["EAST"],["EAST"],["NORTH"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","WOOL",6],["BUY_ANIMAL","COW",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","COW",1],["NORTH"],["CARE"],["PLANT","STRAWBERRY"],["EAST"],["WATER"],["WATER"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["DROP"],["NORTH"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"]],"market":[["SELL","WOOL",6],["BUY_PRODUCT","WHEAT",3],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["BUILD_PASTURE"],["SOUTH"],["WEST"],["NORTH"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"]],"market":[["BUY_ANIMAL","GOOSE",1]]},{"farmer":["PICKUP","GOOSE",1],"hands":[["PLACE","COW",1],["SOUTH"],["FEED"],["PLANT","STRAWBERRY"],["FEED"],["EAST"],["NORTH"],["EAST"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["EAST"],["DROP"],["CARE"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["EAST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["PLANT","MELON"],["PICKUP","GOOSE",1],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["WATER"],["EAST"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["BUILD_COOP"],"hands":[["WATER"],["EAST"],["EAST"],["PLANT","STRAWBERRY"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["EAST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PLACE","GOOSE",1],"hands":[["EAST"],["NORTH"],["EAST"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["SOUTH"],["PLANT","STRAWBERRY"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["PLANT","MELON"],["NORTH"],["DROP"],["EAST"],["NORTH"],["WATER"],["WATER"],["WATER"],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","MELON"],"hands":[["WATER"],["BUILD_COOP"],["PICKUP","WHEAT",2],["PLANT","STRAWBERRY"],["FEED"],["EAST"],["SOUTH"],["SOUTH"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["EAST"],["PLACE","GOOSE",1],["NORTH"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["EAST"],["PLANT","STRAWBERRY"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["PLANT","STRAWBERRY"],["NORTH"],["NORTH"],["EAST"],["NORTH"],["WATER"],["SOUTH"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["WATER"],["PASS"],["WEST"],["PLANT","STRAWBERRY"],["WEST"],["EAST"],["DROP"],["SOUTH"],["DROP"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["PLANT","STRAWBERRY"],["NORTH"],["WATER"],["WEST"],["PLANT","STRAWBERRY"],["PICKUP","WHEAT",2],["PLANT","STRAWBERRY"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PLANT","STRAWBERRY"],["WATER"],["FEED"],["NORTH"],["WEST"],["WATER"],["NORTH"],["WATER"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["WATER"],["WEST"],["CARE"],["PLANT","STRAWBERRY"],["WATER"],["PASS"],["NORTH"],["PASS"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["NORTH"],["WEST"],["WATER"],["WEST"],["PASS"],["WEST"],["PASS"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["CARE"],["CARE"],["PASS"],["WATER"],["PASS"],["WEST"],["PASS"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["NORTH"],["PASS"],["CARE"],["PASS"],["CARE"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["CARE"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["PLACE","FERTILIZER",1],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["FEED"],["SOUTH"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["EAST"],"hands":[["SOUTH"],["FEED"],["NORTH"],["PLACE","FERTILIZER",1],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["PLACE","FERTILIZER",1],["WEST"],["FEED"],["PICKUP","WHEAT",2],["WEST"],["EAST"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["PICKUP","WHEAT",3],["FEED"],["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["NORTH"],["FEED"],["SOUTH"],["PLACE","FERTILIZER",1],["DROP"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["CARE"],"hands":[["NORTH"],["WEST"],["CARE"],["NORTH"],["SOUTH"],["PICKUP","WHEAT",2],["WEST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["FEED"],["FEED"],["WEST"],["NORTH"],["DROP"],["WEST"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["WEST"],["CARE"],["WEST"],["WATER"],["PICKUP","WHEAT",2],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["WEST"],["WEST"],["WATER"],["NORTH"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["NORTH"],["FEED"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["NORTH"],["EAST"],["WEST"],["WEST"],["FEED"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["NORTH"],["SOUTH"],["WATER"],["NORTH"],["CARE"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["SOUTH"],["NORTH"],["SOUTH"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["WATER"],["DROP"],["WATER"],["EAST"],["EAST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PASS"],"hands":[["PLACE","FERTILIZER",2],["WEST"],["PASS"],["EAST"],["NORTH"],["FEED"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PASS"],["EAST"],["CARE"],["EAST"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["EAST"],["PASS"],["EAST"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["WATER"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["EAST"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["CARE"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["NORTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["EAST"]],"market":[["SELL","MILK",6],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"],["WATER"],["WEST"],["NORTH"],["NORTH"],["EAST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",6]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["PLACE","FERTILIZER",1],["WEST"],["WEST"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[["PICKUP","WHEAT",3],["FEED"],["NORTH"],["SOUTH"],["WATER"],["EAST"],["NORTH"],["WATER"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",2],["BUY_LAND"]]},{"farmer":["FEED"],"hands":[["NORTH"],["CARE"],["FEED"],["SOUTH"],["EAST"],["PLACE","FERTILIZER",1],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"]],"market":[["BUY_LAND"],["BUY_LAND"]]},{"farmer":["CARE"],"hands":[["FEED"],["WEST"],["CARE"],["DROP"],["WATER"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["WATER"]],"market":[["SELL","MILK",6],["BUY_LAND"],["BUY_LAND"]]},{"farmer":["NORTH"],"hands":[["CARE"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["WEST"],["SOUTH"],["WEST"],["WATER"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["SOUTH"],["PICKUP","GOOSE",1],["WATER"],["SOUTH"],["DROP"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["PLACE","FERTILIZER",2],["WEST"],["NORTH"],["WEST"],["PICKUP","GOOSE",1],["SOUTH"],["WATER"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["EAST"],["PICKUP","GOOSE",1],["BUILD_COOP"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["EAST"],["SOUTH"],["PLACE","GOOSE",1],["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["DROP"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["WATER"],["NORTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["EAST"],["WEST"],["WEST"],["WEST"],["PLANT","WHEAT"],["BUILD_COOP"],["EAST"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["EAST"],["BUILD_COOP"],["PLANT","WHEAT"],["WATER"],["WATER"],["PLACE","GOOSE",1],["WATER"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["FEED"],["NORTH"],["PLACE","GOOSE",1],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["EAST"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["CARE"],["EAST"],["NORTH"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["DROP"],["WATER"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WEST"],["WATER"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["WATER"],["PASS"],["SOUTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["NORTH"],["NORTH"],["SOUTH"],["WEST"],["PLANT","WHEAT"],["SOUTH"],["WEST"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WEST"],["WATER"],["EAST"],["PLANT","WHEAT"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["WATER"],"hands":[["WATER"],["PASS"],["FEED"],["WATER"],["WATER"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["SOUTH"],["CARE"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["WEST"],["WEST"],["SOUTH"],["PLANT","WHEAT"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["PASS"],["PASS"],["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["PASS"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["CARE"],["WEST"],["PICKUP","WHEAT",2],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",6],["BUY_PRODUCT","WHEAT",6],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["PLACE","FERTILIZER",1],["WEST"],["PICKUP","WHEAT",4],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["FEED"],["EAST"],["SOUTH"],["HARVEST"],["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[["SELL","WOOL",4],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["DROP"],["NORTH"],["PLACE","FERTILIZER",1],["FEED"],["EAST"],["WEST"],["NORTH"],["FEED"],["WEST"]],"market":[["SELL","WOOL",4],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["PICKUP","GOOSE",1],["CARE"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["FEED"],"hands":[["PLACE","FERTILIZER",1],["COLLECT_FERTILIZER"],["BUILD_COOP"],["COLLECT_FERTILIZER"],["DROP"],["WEST"],["EAST"],["FEED"],["WEST"]],"market":[["SELL","WOOL",4],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["CARE"],"hands":[["PICKUP","GOOSE",1],["WEST"],["PLACE","GOOSE",1],["NORTH"],["PICKUP","GOOSE",1],["FEED"],["EAST"],["CARE"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["FEED"],["PICKUP","WHEAT",3],["DROP"],["SOUTH"],["CARE"],["DROP"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",5]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["CARE"],["WEST"],["PICKUP","WHEAT",3],["SOUTH"],["NORTH"],["PICKUP","WHEAT",3],["WEST"],["WATER"]],"market":[["SELL","FERTILIZER",3],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["NORTH"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["SOUTH"],["NORTH"],["FEED"],["FEED"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["BUILD_COOP"],["SOUTH"],["CARE"],["CARE"],["BUILD_COOP"],["FEED"],["CARE"],["CARE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["PLACE","GOOSE",1],["PLACE","FERTILIZER",2],["WEST"],["WEST"],["PLACE","GOOSE",1],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["SOUTH"],["NORTH"],["FEED"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["CARE"],"hands":[["PLANT","WHEAT"],["NORTH"],["CARE"],["FEED"],["WEST"],["WEST"],["WEST"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["NORTH"],["NORTH"],["CARE"],["PLANT","WHEAT"],["FEED"],["WATER"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["NORTH"],["NORTH"],["SOUTH"],["WATER"],["CARE"],["WEST"],["FEED"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["SOUTH"],["CARE"],["NORTH"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["EAST"],["FEED"],["WEST"],["NORTH"],["SOUTH"],["EAST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["EAST"],["EAST"],["CARE"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WEST"],["WATER"],["EAST"],["PASS"],["WATER"],["EAST"],["SOUTH"],["EAST"],["EAST"]],"market":[]},{"farmer":["EAST"],"hands":[["WEST"],["EAST"],["EAST"],["PASS"],["WEST"],["EAST"],["PASS"],["WATER"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["PASS"],["SOUTH"],["WATER"],["SOUTH"],["PASS"],["EAST"],["SOUTH"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["EAST"],["WATER"],["WATER"],["EAST"],["WATER"],["WATER"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["WEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["NORTH"],["EAST"],["WEST"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["WATER"],"hands":[["WEST"],["FEED"],["FEED"],["WEST"],["NORTH"],["WATER"],["NORTH"],["PICKUP","WHEAT",4],["WEST"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WEST"],["CARE"],["CARE"],["SOUTH"],["NORTH"],["EAST"],["WEST"],["NORTH"],["WEST"],["DROP"],["WEST"]],"market":[["SELL","MILK",3]]},{"farmer":["SOUTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["WATER"],["WEST"],["FEED"],["WATER"],["PICKUP","WHEAT",4],["NORTH"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["NORTH"],["WEST"],["CARE"],["HARVEST"],["EAST"],["WEST"],["CARE"],["HARVEST"],["CARE"],["WATER"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","MELON",6],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["EAST"],["HARVEST"],["CARE"],["SOUTH"],["SOUTH"],["EAST"],["HARVEST"],["FEED"],["SOUTH"],["WEST"],["SOUTH"]],"market":[["BUY_PRODUCT","WHEAT",12]]},{"farmer":["FEED"],"hands":[["EAST"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["EAST"],["CARE"],["EAST"],["FEED"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["DROP"],["WATER"],["WEST"],["SOUTH"],["DROP"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["DROP"],["CARE"],["EAST"]],"market":[["SELL","MELON",12],["SELL","MELON",6]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",3],["EAST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["WATER"],["EAST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["DROP"]],"market":[["SELL","MELON",6]]},{"farmer":["CARE"],"hands":[["NORTH"],["WATER"],["WEST"],["SOUTH"],["WEST"],["NORTH"],["EAST"],["WEST"],["WEST"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["EAST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["DROP"],["HARVEST"],["WEST"],["FEED"],["SOUTH"]],"market":[["SELL","MELON",6]]},{"farmer":["WEST"],"hands":[["FEED"],["WATER"],["SOUTH"],["WEST"],["CARE"],["NORTH"],["PICKUP","WHEAT",3],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["CARE"],["NORTH"],["FERTILIZE"],["WEST"],["WEST"],["WATER"],["WEST"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WEST"],["WEST"],["NORTH"],["NORTH"],["DROP"],["WEST"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"],["WATER"],["WEST"],["WEST"],["WEST"],["WATER"],["FEED"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["WEST"],["FERTILIZE"],["SOUTH"],["SOUTH"],["CARE"],["SOUTH"],["EAST"],["WEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["WATER"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["NORTH"],["WATER"],["NORTH"],["WATER"],["NORTH"],["NORTH"],["FEED"],["NORTH"],["CARE"],["FERTILIZE"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["WATER"],["NORTH"],["FERTILIZE"],["SOUTH"],["WATER"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[["SELL","MILK",3]]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["WEST"],["CARE"],["SOUTH"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WATER"],["PASS"],["EAST"],["PASS"],["WEST"],["COLLECT_FERTILIZER"],["PASS"],["WATER"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WEST"],["PICKUP","WHEAT",4],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",6],["HIRE"]]},{"farmer":["WEST"],"hands":[["FEED"],["FEED"],["FEED"],["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["PICKUP","WHEAT",4]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["CARE"],["WEST"],["NORTH"],["FEED"],["SOUTH"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["FEED"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WEST"],["NORTH"],["SOUTH"],["CARE"],["WEST"],["CARE"],["WEST"],["WATER"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["FERTILIZE"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["CARE"],["FEED"],["CARE"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["SOUTH"],["FEED"],["EAST"],["WATER"],["WEST"],["WEST"],["SOUTH"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["EAST"],["NORTH"],["FERTILIZE"],["WATER"],["SOUTH"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["DROP"],"hands":[["FEED"],["EAST"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["WATER"],["WEST"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","MELON",6],["SELL","MILK",6]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["CARE"],["WATER"],["WEST"],["WEST"],["SOUTH"],["WEST"],["WEST"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["FERTILIZE"],["EAST"],["FEED"],["WATER"],["WEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["WATER"],["DROP"],["CARE"],["HARVEST"],["WATER"],["WEST"],["FEED"]],"market":[["SELL","MELON",6]]},{"farmer":["WEST"],"hands":[["NORTH"],["NORTH"],["WATER"],["WEST"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["HARVEST"],["WEST"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FEED"],["WATER"],["WEST"],["WATER"],["WEST"],["WEST"],["WATER"],["PLANT","WHEAT"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WEST"],["EAST"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["WEST"],["WATER"],["PLANT","WHEAT"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["WEST"],["WATER"],["WEST"],["WATER"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["EAST"],["PLANT","WHEAT"],["WATER"],["FEED"],["WATER"],["HARVEST"],["WATER"],["EAST"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["CARE"],["WEST"],["PLANT","WHEAT"],["HARVEST"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["EAST"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WATER"],["WATER"],["HARVEST"],["WEST"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["FERTILIZE"],["SOUTH"],["WATER"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["SOUTH"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"],["PASS"],["PASS"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["NORTH"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["DROP"],["FEED"],["FEED"],["WEST"],["NORTH"],["WATER"],["HARVEST"],["SOUTH"],["WEST"],["WEST"],["PICKUP","WHEAT",4]],"market":[["SELL","MILK",3]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",4],["CARE"],["CARE"],["WEST"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","WOOL",4]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["FEED"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["CARE"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["DROP"],["WATER"],["WEST"],["WATER"],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","MILK",3]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["HARVEST"],["WEST"],["EAST"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["FEED"],["FEED"],["WEST"],["NORTH"],["PLANT","WHEAT"],["WATER"],["EAST"],["EAST"],["HARVEST"]],"market":[["SELL","WHEAT",8],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["EAST"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["DROP"],["EAST"],["CARE"]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["FEED"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"],["WATER"],["WEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["EAST"],["WATER"],["HARVEST"],["FERTILIZE"],["WATER"],["WATER"],["HARVEST"],["WEST"],["EAST"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WEST"],["WEST"],["WATER"],["WEST"],["HARVEST"],["PLANT","STRAWBERRY"],["HARVEST"],["DROP"],["CARE"]],"market":[["SELL","MILK",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["WATER"],["WATER"],["WEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["NORTH"],["PICKUP","WHEAT",2],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["NORTH"],["HARVEST"],["HARVEST"],["FERTILIZE"],["NORTH"],["WATER"],["WEST"],["WATER"],["WEST"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["WATER"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"],["WATER"],["EAST"],["FERTILIZE"],["NORTH"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WEST"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["EAST"],["WATER"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["WATER"],["SOUTH"],["NORTH"],["SOUTH"],["WATER"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["WEST"],["WEST"],["NORTH"],["SOUTH"],["EAST"],["CARE"],["WATER"],["WEST"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WEST"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["EAST"],["HARVEST"],["FERTILIZE"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["NORTH"],["HARVEST"],["FEED"],["WATER"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["PLANT","WHEAT"],["CARE"],["HARVEST"],["WATER"],["DROP"],["WATER"],["NORTH"],["PASS"],["DROP"]],"market":[["SELL","MILK",3],["SELL","EGG",8]]},{"farmer":["HARVEST"],"hands":[["WATER"],["EAST"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["HARVEST"],["PASS"],["PASS"]],"market":[["SELL","FERTILIZER",5],["SELL","EGG",4]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","FERTILIZER",7],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_SEED","STRAWBERRY",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",6],["EAST"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["EAST"],["WEST"],["WEST"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["FEED"],["NORTH"],["HARVEST"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["SOUTH"],["WEST"],["SOUTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["SOUTH"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["SOUTH"],["WEST"],["WATER"],["FEED"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["WEST"],["NORTH"],["WATER"],["HARVEST"],["WATER"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["CARE"],["FEED"],["FEED"],["NORTH"],["PLANT","WHEAT"],["HARVEST"],["HARVEST"],["PLANT","STRAWBERRY"],["NORTH"]],"market":[["SELL","WHEAT",8],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["HARVEST"],["CARE"],["CARE"],["WATER"],["WATER"],["PLANT","STRAWBERRY"],["SOUTH"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["WATER"],["SOUTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["FEED"],["HARVEST"],["WEST"],["WATER"],["WEST"],["SOUTH"],["EAST"],["WATER"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["CARE"],["WEST"],["NORTH"],["NORTH"],["FERTILIZE"],["WATER"],["SOUTH"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WEST"],["FEED"],["WATER"],["WATER"],["HARVEST"],["EAST"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["WEST"],["FERTILIZE"],["CARE"],["EAST"],["WEST"],["PLANT","STRAWBERRY"],["DROP"],["WATER"],["FEED"]],"market":[["SELL","MILK",9]]},{"farmer":["FEED"],"hands":[["WATER"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["FERTILIZE"],["WATER"],["PICKUP","WHEAT",2],["NORTH"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["HARVEST"],["FERTILIZE"],["SOUTH"],["WEST"],["EAST"],["WATER"],["WEST"],["WEST"],["FERTILIZE"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLANT","WHEAT"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["WEST"],["SOUTH"],["WATER"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["WATER"],["NORTH"],["EAST"],["PLANT","WHEAT"],["FERTILIZE"],["SOUTH"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["SOUTH"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["WATER"],["FEED"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["WEST"],["SOUTH"],["SOUTH"],["WEST"],["CARE"],["NORTH"],["NORTH"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["EAST"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["WATER"],["HARVEST"]],"market":[["SELL","WHEAT",8]]},{"farmer":["NORTH"],"hands":[["PASS"],["EAST"],["PASS"],["EAST"],["SOUTH"],["EAST"],["EAST"],["PASS"],["NORTH"],["PASS"]],"market":[["SELL","EGG",6]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",3],["SELL","WHEAT",13],["SELL","WHEAT",13]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["DROP"],["FEED"],["WEST"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["SOUTH"],["WATER"],["WEST"]],"market":[["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["FERTILIZE"],["FERTILIZE"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["WEST"],["WATER"],["EAST"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["SOUTH"],["FEED"],["HARVEST"],["WATER"],["WEST"],["SOUTH"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["EAST"],"hands":[["WATER"],["FEED"],["CARE"],["PLANT","WHEAT"],["NORTH"],["FERTILIZE"],["WATER"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["EAST"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["WEST"],["FEED"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["HARVEST"],["HARVEST"],["WEST"],["NORTH"],["WEST"],["WEST"],["CARE"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["WEST"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["FERTILIZE"],["WATER"],["WEST"],["HARVEST"],["WEST"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["FEED"]],"market":[]},{"farmer":["DROP"],"hands":[["WATER"],["SOUTH"],["WATER"],["WEST"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["CARE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["NORTH"],["WATER"],["HARVEST"],["WATER"],["WEST"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",3]]},{"farmer":["WEST"],"hands":[["WATER"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["HARVEST"],["WEST"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["EAST"],["PLANT","WHEAT"],["WATER"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["NORTH"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["FERTILIZE"],["WEST"]],"market":[["SELL","EGG",8]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["WEST"],["EAST"],["PLANT","WHEAT"],["WATER"],["EAST"],["PLANT","WHEAT"],["WATER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["EAST"],["WATER"],["NORTH"],["WATER"],["WATER"],["EAST"],["SOUTH"]],"market":[["SELL","EGG",8]]},{"farmer":["CARE"],"hands":[["PASS"],["PASS"],["CARE"],["SOUTH"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","EGG",3]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",4],["WEST"],["PICKUP","FERTILIZER",4]],"market":[["SELL","WOOL",1],["SELL","WHEAT",13],["HIRE"],["HIRE"],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["EAST"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["CARE"],["FEED"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["CARE"],["FEED"],["NORTH"],["SOUTH"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["SOUTH"],["SOUTH"],["CARE"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["FEED"],["FEED"],["NORTH"],["WATER"],["HARVEST"],["EAST"],["WATER"],["FERTILIZE"],["HARVEST"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["PLANT","STRAWBERRY"],["FERTILIZE"],["HARVEST"],["WATER"],["EAST"],["PLANT","STRAWBERRY"]],"market":[["SELL","WHEAT",8],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["FEED"],["SOUTH"],["CARE"],["FEED"],["FERTILIZE"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["FERTILIZE"],["PLANT","STRAWBERRY"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["FEED"],["HARVEST"],["CARE"],["WATER"],["PLANT","STRAWBERRY"],["NORTH"],["PLANT","STRAWBERRY"],["FERTILIZE"],["WATER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","STRAWBERRY"],["FERTILIZE"],["PLANT","STRAWBERRY"],["WATER"],["EAST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["WEST"],["WATER"],["WEST"],["FERTILIZE"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["NORTH"],["FERTILIZE"],["PLANT","STRAWBERRY"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["FERTILIZE"],["WEST"],["FEED"],["WATER"],["PLANT","STRAWBERRY"],["NORTH"],["PLANT","STRAWBERRY"],["FERTILIZE"],["WATER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["WATER"],["WATER"],["CARE"],["NORTH"],["PLANT","STRAWBERRY"],["FERTILIZE"],["PLANT","STRAWBERRY"],["WATER"],["WEST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["FERTILIZE"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["WEST"],["WEST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["WATER"],["HARVEST"],["WATER"],["PLANT","STRAWBERRY"],["NORTH"],["PLANT","STRAWBERRY"],["WEST"],["WEST"],["PLANT","STRAWBERRY"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WEST"],["SOUTH"],["HARVEST"],["WEST"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","WHEAT"],["WEST"],["WEST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["WATER"],["SOUTH"],["WEST"],["WEST"],["WATER"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["EAST"],["SOUTH"],["WEST"],["FEED"]],"market":[["SELL","MILK",2]]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["WEST"],["WEST"],["WATER"],["SOUTH"],["NORTH"],["NORTH"],["FERTILIZE"],["WATER"],["HARVEST"],["CARE"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["PASS"],["WATER"],["WATER"],["PASS"],["SOUTH"],["WATER"],["SOUTH"],["PASS"],["PASS"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["EAST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["EAST"],["NORTH"],["EAST"]],"market":[["SELL","STRAWBERRY",6],["SELL","FERTILIZER",2],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["WATER"],["FEED"],["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["CARE"],["WEST"],["FEED"],["WATER"],["SOUTH"],["EAST"],["NORTH"],["WATER"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["EAST"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["DROP"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["WEST"],["HARVEST"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","MELON",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["SOUTH"],["WEST"],["NORTH"],["EAST"],["HARVEST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["WEST"],["WATER"],["DROP"],["SOUTH"],["DROP"],["HARVEST"],["HARVEST"],["SOUTH"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","MELON",12]]},{"farmer":["FERTILIZE"],"hands":[["PLANT","WHEAT"],["SOUTH"],["FEED"],["NORTH"],["PICKUP","WHEAT",2],["WATER"],["PICKUP","WHEAT",2],["EAST"],["NORTH"],["HARVEST"],["WATER"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["FEED"],["CARE"],["WATER"],["NORTH"],["WEST"],["NORTH"],["HARVEST"],["HARVEST"],["SOUTH"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["SOUTH"],["WEST"],["SOUTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["PLANT","WHEAT"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["FEED"],["SOUTH"],["HARVEST"],["WEST"],["WATER"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["WATER"],["NORTH"],["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["DROP"],["NORTH"],["WEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WEST"],["HARVEST"],["FEED"],["HARVEST"],["PLANT","WHEAT"],["HARVEST"],["SOUTH"],["HARVEST"],["WEST"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","MILK",2]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["PLANT","WHEAT"],["CARE"],["EAST"],["WATER"],["CARE"],["WEST"],["WEST"],["WEST"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WEST"],["WEST"],["DROP"],["SOUTH"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["WATER"],"hands":[["EAST"],["PLANT","WHEAT"],["WEST"],["WEST"],["WATER"],["FERTILIZE"],["WEST"],["WEST"],["WEST"],["WEST"],["HARVEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["WATER"],["FERTILIZE"],["NORTH"],["WATER"],["NORTH"],["SOUTH"],["DROP"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","STRAWBERRY",10]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["SOUTH"],["HARVEST"],["WATER"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["SOUTH"],["WATER"],["DROP"]],"market":[["SELL","STRAWBERRY",10]]},{"farmer":["WATER"],"hands":[["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"],["SOUTH"],["NORTH"],["FERTILIZE"],["HARVEST"],["WEST"],["WEST"],["WATER"],["HARVEST"],["WEST"]],"market":[["SELL","WHEAT",8]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["WEST"],["SOUTH"],["HARVEST"],["HARVEST"],["NORTH"],["HARVEST"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["HARVEST"]],"market":[["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["WEST"],["WATER"],["WEST"],["SOUTH"],["EAST"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["DROP"]],"market":[["SELL","EGG",8],["SELL","EGG",8]]},{"farmer":["PASS"],"hands":[["HARVEST"],["HARVEST"],["WATER"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"],["SOUTH"],["WEST"],["WATER"],["PASS"],["PASS"]],"market":[["SELL","WHEAT",7]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",2],["SELL","FERTILIZER",6],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["NORTH"],["HARVEST"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["CARE"],["FEED"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["COLLECT_FERTILIZER"],["CARE"],["FEED"],["SOUTH"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["WEST"],["WEST"],["CARE"],["WATER"],["WEST"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["SOUTH"],["FEED"],["FEED"],["EAST"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["FEED"],["CARE"],["CARE"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["FEED"],["EAST"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["WATER"],["CARE"],["WEST"],["NORTH"],["EAST"],["WATER"],["WATER"],["CARE"],["WATER"],["PLANT","WHEAT"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["HARVEST"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["WEST"],["WEST"],["WEST"],["SOUTH"],["FEED"],["WEST"],["NORTH"],["FERTILIZE"],["FEED"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["CARE"],["WATER"],["HARVEST"],["WATER"],["CARE"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["WATER"],["NORTH"],["EAST"],["HARVEST"],["HARVEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["FEED"],["WATER"],["EAST"],["PLANT","CARROT"],["HARVEST"],["FERTILIZE"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["WATER"],["WATER"],["CARE"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["WATER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["EAST"],"hands":[["WATER"],["SOUTH"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["DROP"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"]],"market":[["SELL","MILK",2]]},{"farmer":["EAST"],"hands":[["NORTH"],["PLANT","CARROT"],["PLANT","WHEAT"],["WEST"],["WEST"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["DROP"],["HARVEST"],["EAST"],["WEST"],["WATER"],["NORTH"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["SOUTH"],["EAST"],["SOUTH"],["NORTH"],["WATER"],["NORTH"],["PLANT","CARROT"],["SOUTH"],["WEST"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",8]]},{"farmer":["EAST"],"hands":[["NORTH"],["WATER"],["WATER"],["WATER"],["SOUTH"],["HARVEST"],["WATER"],["EAST"],["SOUTH"],["HARVEST"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["SOUTH"],["HARVEST"],["SOUTH"],["SOUTH"],["DROP"],["EAST"],["SOUTH"],["SOUTH"],["EAST"],["EAST"]],"market":[["SELL","WHEAT",8],["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["PASS"],["WATER"],["PASS"],["PASS"],["SOUTH"],["PASS"],["EAST"],["SOUTH"],["PASS"],["EAST"],["PASS"]],"market":[["SELL","EGG",5]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["EAST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["NORTH"]],"market":[["SELL","WOOL",2],["SELL","FERTILIZER",8],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FEED"],["WEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["CARE"],["NORTH"],["NORTH"],["SOUTH"],["EAST"],["WEST"],["EAST"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["FERTILIZE"],["HARVEST"],["SOUTH"],["HARVEST"],["WEST"],["HARVEST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["SOUTH"],["CARE"],["WEST"],["WATER"],["WEST"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["SOUTH"],["FEED"],["NORTH"],["WEST"],["WEST"],["HARVEST"],["WEST"],["SOUTH"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["NORTH"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["FERTILIZE"],["HARVEST"],["DIG"],["WEST"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["WEST"],["SOUTH"],["WEST"],["DROP"],["WATER"],["WEST"],["PLANT","WHEAT"],["DROP"],["HARVEST"],["PLANT","WHEAT"]],"market":[["SELL","STRAWBERRY",12],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["DROP"],["NORTH"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["WATER"],["NORTH"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["SOUTH"],"hands":[["EAST"],["FEED"],["WATER"],["WEST"],["EAST"],["WATER"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["WATER"],["CARE"],["WEST"],["HARVEST"],["EAST"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["FERTILIZE"],["DIG"],["FERTILIZE"],["PLANT","WHEAT"],["WEST"],["EAST"],["NORTH"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["WATER"],["EAST"],["WEST"],["WEST"],["SOUTH"],["HARVEST"],["DROP"],["WATER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FERTILIZE"],["WATER"],["WEST"],["NORTH"],["WEST"],["DROP"],["WATER"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"]],"market":[["SELL","STRAWBERRY",8]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["WATER"],["HARVEST"],["FERTILIZE"],["NORTH"],["PLANT","CARROT"],["PICKUP","WHEAT",2],["HARVEST"],["NORTH"],["NORTH"],["EAST"]],"market":[["SELL","WHEAT",10]]},{"farmer":["SOUTH"],"hands":[["EAST"],["EAST"],["PLANT","CARROT"],["WATER"],["NORTH"],["WATER"],["NORTH"],["PLANT","CARROT"],["HARVEST"],["FEED"],["WATER"]],"market":[["SELL","WHEAT",8]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["SOUTH"],["WATER"],["SOUTH"],["EAST"],["SOUTH"],["CARE"],["WATER"],["SOUTH"],["NORTH"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["EAST"],"hands":[["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["HARVEST"],["FERTILIZE"],["NORTH"],["WEST"],["SOUTH"],["FEED"],["HARVEST"]],"market":[["SELL","WHEAT",10]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["SOUTH"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["CARE"],["FERTILIZE"],["CARE"],["PASS"],["PASS"]],"market":[["SELL","EGG",8]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",4],["NORTH"],["PICKUP","FERTILIZER",4]],"market":[["SELL","WOOL",2],["SELL","STRAWBERRY",2],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["EAST"],["HARVEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["NORTH"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["FEED"],["FEED"],["WEST"],["WATER"],["SOUTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["FEED"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["FERTILIZE"],["HARVEST"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["SOUTH"],["SOUTH"],["CARE"],["WATER"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["NORTH"],["FERTILIZE"],["SOUTH"]],"market":[["SELL","WHEAT",8]]},{"farmer":["HARVEST"],"hands":[["FEED"],["FEED"],["FEED"],["WEST"],["EAST"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["COLLECT_FERTILIZER"],["FEED"],["FERTILIZE"],["WEST"],["EAST"],["WEST"],["WATER"],["NORTH"],["HARVEST"]],"market":[["SELL","MILK",2]]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["FERTILIZE"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["FEED"],["HARVEST"],["CARE"],["EAST"],["WATER"],["WATER"],["CARE"],["FERTILIZE"],["EAST"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["CARE"],["SOUTH"],["WEST"],["FERTILIZE"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["FERTILIZE"],["WEST"],["WATER"],["WATER"],["FERTILIZE"],["WEST"],["EAST"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["WEST"],["WATER"],["NORTH"],["HARVEST"],["WATER"],["FEED"],["FERTILIZE"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"],["WATER"],["PLANT","CARROT"],["NORTH"],["CARE"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["DIG"],"hands":[["WEST"],["HARVEST"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["PLANT","CARROT"],"hands":[["HARVEST"],["PLANT","CARROT"],["WEST"],["NORTH"],["WATER"],["WEST"],["WATER"],["WEST"],["WATER"],["SOUTH"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["DIG"],["WATER"],["WEST"],["HARVEST"],["NORTH"],["FERTILIZE"],["NORTH"],["EAST"],["EAST"],["SOUTH"],["NORTH"]],"market":[["SELL","EGG",8]]},{"farmer":["WEST"],"hands":[["PLANT","CARROT"],["WEST"],["FERTILIZE"],["DIG"],["WATER"],["WATER"],["WATER"],["SOUTH"],["EAST"],["WATER"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["SOUTH"],["WATER"],["PLANT","CARROT"],["SOUTH"],["WEST"],["WEST"],["EAST"],["WATER"],["EAST"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["DIG"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["PLANT","CARROT"],"hands":[["WEST"],["WATER"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["HARVEST"],["EAST"],["EAST"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["SOUTH"],["SOUTH"],["DROP"]],"market":[["SELL","WHEAT",10],["SELL","EGG",4]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","STRAWBERRY",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["EAST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",2],["SELL","FERTILIZER",6],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FEED"],["WEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["NORTH"],["WATER"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["CARE"],["WEST"],["EAST"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"],["EAST"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["SOUTH"],["WEST"],["WATER"],["HARVEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["SOUTH"],["CARE"],["WEST"],["SOUTH"],["WEST"],["WATER"],["SOUTH"],["WEST"],["SOUTH"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["SOUTH"],["FEED"],["WATER"],["WEST"],["WEST"],["WEST"],["WATER"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["SOUTH"],["FEED"],["CARE"],["WEST"],["WEST"],["WEST"],["DROP"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["CARE"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WEST"],["SOUTH"],["HARVEST"]],"market":[["SELL","WHEAT",8]]},{"farmer":["WEST"],"hands":[["DROP"],["WEST"],["SOUTH"],["WATER"],["DROP"],["WATER"],["EAST"],["WATER"],["DROP"],["SOUTH"],["PLANT","WHEAT"]],"market":[["SELL","STRAWBERRY",12]]},{"farmer":["WEST"],"hands":[["EAST"],["WATER"],["SOUTH"],["SOUTH"],["EAST"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["HARVEST"],["SOUTH"],["FERTILIZE"],["EAST"],["PLANT","CARROT"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",2]]},{"farmer":["FERTILIZE"],"hands":[["PLANT","WHEAT"],["PLANT","CARROT"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["EAST"],["NORTH"],["HARVEST"],["DROP"],["NORTH"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["WATER"],["SOUTH"],["HARVEST"],["WEST"],["NORTH"],["FEED"],["EAST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["WEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["CARE"],["WATER"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["NORTH"],["FEED"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["FEED"],["CARE"],["HARVEST"],["PLANT","CARROT"],["EAST"],["PLANT","CARROT"],["HARVEST"],["EAST"],["PLANT","WHEAT"],["HARVEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["WATER"],["EAST"],["WATER"],["DIG"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["SOUTH"],["WATER"],["EAST"],["NORTH"],["NORTH"],["PLANT","CARROT"],["HARVEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["SOUTH"],["EAST"],["WATER"],["HARVEST"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["EAST"],["HARVEST"]],"market":[["SELL","EGG",8]]},{"farmer":["NORTH"],"hands":[["CARE"],["WATER"],["SOUTH"],["EAST"],["NORTH"],["SOUTH"],["NORTH"],["FERTILIZE"],["DROP"],["HARVEST"],["NORTH"]],"market":[["SELL","WHEAT",10],["SELL","EGG",8]]},{"farmer":["FERTILIZE"],"hands":[["PASS"],["EAST"],["FERTILIZE"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["PASS"],["HARVEST"],["NORTH"],["FERTILIZE"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["SOUTH"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["NORTH"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["CARE"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["CARE"],["CARE"],["FEED"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["FEED"],["CARE"],["WEST"],["SOUTH"],["HARVEST"],["NORTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["FEED"],["FEED"],["CARE"],["HARVEST"],["WEST"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["CARE"],["WEST"],["EAST"],["FERTILIZE"],["WATER"],["WATER"],["EAST"],["NORTH"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["WATER"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WEST"],["WEST"],["WATER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"],["WATER"],["FEED"],["EAST"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["CARE"],["WEST"],["WEST"],["WATER"],["FERTILIZE"],["WEST"],["CARE"],["FERTILIZE"],["NORTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["FERTILIZE"],["FEED"],["EAST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["EAST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WATER"],["CARE"],["WATER"],["HARVEST"],["HARVEST"],["NORTH"],["HARVEST"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","CARROT"],["PLANT","CARROT"],["FERTILIZE"],["EAST"],["PLANT","WHEAT"],["FEED"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["WATER"],["FERTILIZE"],["SOUTH"],["WATER"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["WATER"],["CARE"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["WATER"],["WATER"],["SOUTH"],["WEST"],["WEST"],["EAST"],["WATER"],["NORTH"],["EAST"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["HARVEST"],["PLANT","CARROT"],["WEST"],["HARVEST"],["WATER"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"],["EAST"]],"market":[["SELL","WHEAT",8]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["EAST"],["WATER"],["NORTH"],["HARVEST"],["SOUTH"],["DIG"],["DROP"]],"market":[["SELL","EGG",8]]},{"farmer":["HARVEST"],"hands":[["WATER"],["WEST"],["HARVEST"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["WEST"],["WATER"],["PLANT","WHEAT"],["NORTH"]],"market":[["SELL","EGG",8]]},{"farmer":["PLANT","WHEAT"],"hands":[["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["PLANT","CARROT"],["SOUTH"],["WEST"],["SOUTH"],["WATER"],["HARVEST"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["NORTH"],["NORTH"],["WATER"],["EAST"],["SOUTH"],["SOUTH"],["SOUTH"],["DROP"]],"market":[["SELL","WHEAT",13],["SELL","CARROT",10]]},{"farmer":["SOUTH"],"hands":[["PASS"],["WATER"],["PASS"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["EAST"],["PASS"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","FERTILIZER",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","FERTILIZER",2],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["WEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["NORTH"],["WEST"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["CARE"],["WEST"],["DIG"],["SOUTH"],["FERTILIZE"],["WATER"],["DIG"],["WEST"],["HARVEST"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["COLLECT_FERTILIZER"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["WEST"],["DIG"]],"market":[["SELL","WHEAT",8]]},{"farmer":["CARE"],"hands":[["HARVEST"],["CARE"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["EAST"],["PLANT","WHEAT"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["DIG"],["WEST"],["FEED"],["NORTH"],["EAST"],["FERTILIZE"],["EAST"],["WATER"],["NORTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["FEED"],["CARE"],["NORTH"],["HARVEST"],["WATER"],["NORTH"],["WEST"],["HARVEST"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["WATER"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["DIG"],["SOUTH"],["HARVEST"],["COLLECT_FERTILIZER"],["DIG"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["PLANT","WHEAT"],["FERTILIZE"],["DIG"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["DIG"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["HARVEST"],["WEST"],["WEST"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["FEED"],["WATER"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["DIG"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["WEST"],["WATER"],["CARE"],["EAST"],["HARVEST"],["WATER"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["PLANT","CARROT"],["SOUTH"],["HARVEST"],["PLANT","CARROT"],["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["PLANT","CARROT"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["PLANT","CARROT"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["SOUTH"],["DIG"],["WATER"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["HARVEST"],["WATER"],["EAST"],["DIG"],["WEST"],["HARVEST"],["SOUTH"],["PLANT","CARROT"],["EAST"],["DIG"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","CARROT"],"hands":[["WATER"],["PLANT","CARROT"],["NORTH"],["EAST"],["PLANT","CARROT"],["WATER"],["DIG"],["FERTILIZE"],["WATER"],["EAST"],["PLANT","CARROT"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["PLANT","CARROT"],["WATER"],["EAST"],["HARVEST"],["WATER"]],"market":[["SELL","CARROT",13]]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["HARVEST"],["SOUTH"],["WEST"],["EAST"],["WATER"],["EAST"],["HARVEST"],["EAST"],["SOUTH"]],"market":[["SELL","EGG",8]]},{"farmer":["FERTILIZE"],"hands":[["DIG"],["WEST"],["PLANT","WHEAT"],["EAST"],["WEST"],["WATER"],["NORTH"],["FERTILIZE"],["DIG"],["EAST"],["HARVEST"]],"market":[["SELL","WHEAT",8]]},{"farmer":["WEST"],"hands":[["PLANT","CARROT"],["FERTILIZE"],["WATER"],["EAST"],["DIG"],["HARVEST"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["EAST"],["WEST"]],"market":[["SELL","MILK",2]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["EAST"],["SOUTH"],["PLANT","WHEAT"],["PLANT","CARROT"],["DIG"],["EAST"],["WATER"],["SOUTH"],["SOUTH"]],"market":[["SELL","WHEAT",7],["SELL","CARROT",4]]},{"farmer":["WATER"],"hands":[["NORTH"],["EAST"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WEST"],["EAST"],["EAST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","EGG",6]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","CARROT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",3],["SELL","FERTILIZER",2],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["WATER"],["EAST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["FEED"],["EAST"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["WEST"],["SOUTH"],["WATER"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["FERTILIZE"],["WATER"],["NORTH"],["PLANT","WHEAT"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FEED"],["CARE"],["FEED"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WEST"],["WEST"],["WATER"],["FERTILIZE"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["CARE"],["SOUTH"],["HARVEST"],["FERTILIZE"],["WATER"],["HARVEST"],["WEST"],["FEED"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["CARE"],["WATER"],["WEST"],["PLANT","WHEAT"],["FERTILIZE"],["CARE"],["SOUTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WEST"],"hands":[["HARVEST"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["DROP"],["FERTILIZE"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["DROP"],["NORTH"],["WEST"],["WEST"],["NORTH"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["EAST"],["WEST"],["SOUTH"],["HARVEST"],["PICKUP","WHEAT",2],["HARVEST"],["FERTILIZE"],["FEED"],["NORTH"],["SOUTH"]],"market":[["SELL","EGG",8]]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["WEST"],["WEST"],["EAST"],["WATER"],["CARE"],["EAST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["FERTILIZE"],["FERTILIZE"],["SOUTH"],["NORTH"],["NORTH"],["HARVEST"],["NORTH"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["WATER"],["WATER"],["FEED"],["FEED"],["DROP"],["PLANT","CARROT"],["NORTH"],["NORTH"],["PLANT","CARROT"]],"market":[["SELL","MILK",2],["SELL","CARROT",13]]},{"farmer":["WEST"],"hands":[["HARVEST"],["HARVEST"],["HARVEST"],["CARE"],["CARE"],["PICKUP","WHEAT",2],["WATER"],["WATER"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["SOUTH"],"hands":[["PLANT","CARROT"],["PLANT","CARROT"],["PLANT","CARROT"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["WEST"],["WEST"],["EAST"],["SOUTH"]],"market":[["SELL","WHEAT",8]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["WATER"],["WEST"],["HARVEST"],["SOUTH"],["FERTILIZE"],["WATER"],["DIG"],["WATER"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["EAST"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["WATER"],["SOUTH"],["PLANT","CARROT"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["SOUTH"],["FERTILIZE"],["HARVEST"],["SOUTH"],["CARE"],["HARVEST"],["FERTILIZE"],["WATER"],["PLANT","CARROT"]],"market":[["SELL","EGG",4]]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["WATER"],["EAST"],["DROP"],["COLLECT_FERTILIZER"],["PASS"],["WATER"],["SOUTH"],["WATER"]],"market":[["SELL","WHEAT",3],["SELL","EGG",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","CARROT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["PICKUP","FERTILIZER",4],["WEST"],["PICKUP","FERTILIZER",4],["WEST"],["PICKUP","FERTILIZER",4]],"market":[["SELL","STRAWBERRY",4],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["WEST"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["PICKUP","WHEAT",2]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["WEST"],["NORTH"],["EAST"],["WEST"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["FEED"]],"market":[]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["WEST"],["CARE"],["WATER"],["EAST"],["WEST"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["CARE"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["HARVEST"],["WEST"],["FERTILIZE"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["WEST"],["FERTILIZE"],["WATER"],["FEED"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["CARE"],["FEED"],["HARVEST"],["NORTH"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["HARVEST"],["CARE"],["NORTH"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["NORTH"],["PLANT","WHEAT"],["HARVEST"]],"market":[["SELL","MILK",4],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["PLANT","WHEAT"],["SOUTH"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["HARVEST"],["WEST"],["WATER"],["FERTILIZE"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["FERTILIZE"],["WEST"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["WEST"],["WEST"],["WATER"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"],["WATER"],["WATER"],["HARVEST"],["HARVEST"]],"market":[["SELL","MILK",2]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["NORTH"],["WEST"],["WATER"],["PLANT","CARROT"],["HARVEST"],["WEST"],["NORTH"],["HARVEST"],["FEED"],["PLANT","CARROT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["WATER"],["HARVEST"],["WATER"],["EAST"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"],["CARE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["NORTH"],["HARVEST"],["PLANT","WHEAT"],["NORTH"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["WATER"],["FERTILIZE"],["EAST"],["PLANT","CARROT"],["NORTH"],["SOUTH"],["FERTILIZE"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["HARVEST"],["NORTH"],["WATER"],["WEST"],["WATER"],["EAST"],["WATER"],["WATER"],["FEED"],["WATER"],["EAST"]],"market":[["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["PLANT","CARROT"],["FEED"],["SOUTH"],["WATER"],["HARVEST"],["EAST"],["WEST"],["HARVEST"],["CARE"],["EAST"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WATER"],["CARE"],["SOUTH"],["HARVEST"],["PLANT","CARROT"],["FEED"],["NORTH"],["PLANT","CARROT"],["WEST"],["SOUTH"],["DROP"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","CARROT"],["WATER"],["CARE"],["FERTILIZE"],["WATER"],["WEST"],["FEED"],["HARVEST"]],"market":[["SELL","CARROT",13]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["EAST"],["PLANT","CARROT"],["WATER"],["NORTH"],["DROP"],["WATER"],["NORTH"],["WATER"],["CARE"],["DROP"]],"market":[["SELL","WHEAT",6],["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["CARE"],["WATER"],["WEST"],["WEST"],["HARVEST"],["EAST"],["WATER"],["PASS"],["HARVEST"],["PASS"]],"market":[["SELL","EGG",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","CARROT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["FEED"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["CARE"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["FERTILIZE"],"hands":[["FEED"],["FEED"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["SOUTH"],["EAST"],["WATER"],["WATER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["WATER"],["SOUTH"],["FERTILIZE"],["HARVEST"],["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["FEED"],["WEST"],["HARVEST"],["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["FEED"],["FEED"],["CARE"],["WEST"],["PLANT","WHEAT"],["WATER"],["NORTH"],["WATER"],["WATER"],["WEST"],["EAST"]],"market":[["SELL","MILK",4]]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["HARVEST"],["FERTILIZE"],["WEST"],["EAST"],["WEST"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["HARVEST"],["WEST"],["SOUTH"],["CARE"],["NORTH"],["WEST"],["WATER"],["WEST"],["WATER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["NORTH"],["FEED"],["HARVEST"],["WATER"],["PLANT","CARROT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WATER"],["WEST"],["WEST"],["HARVEST"],["WEST"],["FERTILIZE"],["CARE"],["PLANT","WHEAT"],["HARVEST"],["WATER"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["WATER"],["SOUTH"],["WATER"],["NORTH"],["PLANT","WHEAT"],["FERTILIZE"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["PLANT","WHEAT"],["WEST"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WEST"],["HARVEST"],["WATER"],["WATER"],["WATER"],["EAST"],["HARVEST"],["WEST"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"],["WEST"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["PLANT","CARROT"],"hands":[["WATER"],["WEST"],["WATER"],["PLANT","CARROT"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["FEED"],["NORTH"],["WEST"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["SOUTH"],["HARVEST"],["SOUTH"],["WATER"],["WEST"],["WEST"],["PLANT","CARROT"],["FEED"],["CARE"],["WATER"],["DROP"]],"market":[["SELL","WHEAT",10]]},{"farmer":["SOUTH"],"hands":[["EAST"],["PLANT","CARROT"],["FERTILIZE"],["WEST"],["SOUTH"],["WATER"],["WATER"],["CARE"],["HARVEST"],["HARVEST"],["HARVEST"]],"market":[["SELL","EGG",4]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WATER"],["WATER"],["FERTILIZE"],["DROP"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["DROP"]],"market":[["SELL","WHEAT",10]]},{"farmer":["EAST"],"hands":[["HARVEST"],["EAST"],["WEST"],["WATER"],["WEST"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"]],"market":[["SELL","MILK",4]]},{"farmer":["SOUTH"],"hands":[["PLANT","CARROT"],["EAST"],["FERTILIZE"],["SOUTH"],["WEST"],["NORTH"],["WEST"],["FERTILIZE"],["SOUTH"],["EAST"],["HARVEST"]],"market":[["SELL","CARROT",5]]},{"farmer":["FEED"],"hands":[["WATER"],["HARVEST"],["PASS"],["SOUTH"],["SOUTH"],["WATER"],["WATER"],["WEST"],["SOUTH"],["FERTILIZE"],["PASS"]],"market":[["SELL","WHEAT",5]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","CARROT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["HARVEST"],["PICKUP","WHEAT",2],["HARVEST"],["EAST"],["WEST"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLACE","MILK",3],["DROP"],["WEST"],["PLACE","MILK",3],["WATER"],["HARVEST"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["SOUTH"],["PICKUP","WHEAT",3],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["NORTH"],["WEST"],["EAST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FEED"],["FEED"],["FEED"],["PLANT","WHEAT"],["WEST"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["CARE"],["CARE"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["HARVEST"],["WATER"],["WATER"],["FERTILIZE"],["DIG"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["WEST"],["SOUTH"],["WEST"],["FEED"],["WEST"],["WEST"],["NORTH"],["WATER"],["PLANT","WHEAT"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["PLANT","WHEAT"],["FEED"],["FEED"],["WATER"],["CARE"],["WATER"],["FERTILIZE"],["WATER"],["EAST"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["CARE"],["CARE"],["NORTH"],["NORTH"],["WEST"],["WATER"],["HARVEST"],["EAST"],["FERTILIZE"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["FEED"],["FERTILIZE"],["SOUTH"],["PLANT","WHEAT"],["FERTILIZE"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FERTILIZE"],["FEED"],["HARVEST"],["NORTH"],["CARE"],["WATER"],["FERTILIZE"],["WATER"],["WATER"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["WATER"],["NORTH"],["NORTH"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["NORTH"],["HARVEST"],["WATER"],["FEED"],["FEED"],["FERTILIZE"],["WEST"],["FEED"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["CARE"],["WATER"],["FERTILIZE"],["CARE"],["HARVEST"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["WEST"],["FERTILIZE"],["HARVEST"],["HARVEST"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["NORTH"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["PLANT","CARROT"],["WATER"],["WATER"],["WEST"],["WEST"],["WATER"],["WEST"],["HARVEST"],["WATER"],["WATER"],["WEST"]],"market":[]},{"farmer":["PLANT","CARROT"],"hands":[["WATER"],["HARVEST"],["SOUTH"],["FEED"],["FEED"],["HARVEST"],["WATER"],["WEST"],["EAST"],["EAST"],["SOUTH"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["EAST"],["PLANT","CARROT"],["FERTILIZE"],["CARE"],["CARE"],["PLANT","CARROT"],["HARVEST"],["FEED"],["WATER"],["WATER"],["DROP"]],"market":[["SELL","EGG",8]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["WATER"],["PLANT","CARROT"],["CARE"],["HARVEST"],["NORTH"],["NORTH"]],"market":[["SELL","WHEAT",10]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["NORTH"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["FEED"],["PLANT","CARROT"],["WEST"],["SOUTH"],["WATER"],["WEST"],["EAST"],["WATER"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["CARE"],["WATER"],["FERTILIZE"],["DROP"],["HARVEST"],["FERTILIZE"],["EAST"],["SOUTH"],["EAST"],["PLANT","WHEAT"]],"market":[["SELL","CARROT",10],["SELL","EGG",4]]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["PASS"],["WEST"],["PASS"],["PASS"],["EAST"],["WATER"],["FERTILIZE"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","WHEAT",3],["SELL","EGG",3]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","CARROT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["WEST"],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",3],["WEST"]],"market":[["SELL","MILK",4],["SELL","CARROT",12],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["FEED"],["FEED"],["FEED"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["DROP"],"hands":[["CARE"],["CARE"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["EAST"],["WEST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["SOUTH"],["CARE"],["NORTH"],["NORTH"],["SOUTH"],["EAST"],["SOUTH"],["NORTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["NORTH"],"hands":[["FEED"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["HARVEST"],["FERTILIZE"],["HARVEST"],["NORTH"],["PLANT","WHEAT"]],"market":[["SELL","WOOL",1]]},{"farmer":["CARE"],"hands":[["WEST"],["CARE"],["CARE"],["WEST"],["HARVEST"],["HARVEST"],["SOUTH"],["WATER"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"],["EAST"],["WATER"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FEED"],["NORTH"],["SOUTH"],["CARE"],["WATER"],["WATER"],["HARVEST"],["FERTILIZE"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["CARE"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["WEST"],["WATER"],["SOUTH"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["WEST"],["WATER"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["EAST"],["WEST"],["SOUTH"],["HARVEST"],["WATER"],["WEST"],["FERTILIZE"],["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["FERTILIZE"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"],["EAST"],["WATER"],["WATER"],["EAST"],["WATER"],["WATER"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["HARVEST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["EAST"],["EAST"],["WEST"]],"market":[["SELL","EGG",8]]},{"farmer":["FEED"],"hands":[["WEST"],["WEST"],["PLANT","CARROT"],["SOUTH"],["EAST"],["HARVEST"],["WEST"],["WATER"],["EAST"],["FERTILIZE"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["HARVEST"],["WATER"],["DIG"],["EAST"],["PLANT","WHEAT"],["WEST"],["HARVEST"],["FEED"],["WATER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["WEST"],["SOUTH"],["EAST"],["WATER"],["WATER"],["NORTH"],["CARE"],["EAST"],["SOUTH"]],"market":[["SELL","MILK",1],["SELL","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["WATER"],["FERTILIZE"],["SOUTH"],["SOUTH"],["HARVEST"],["WATER"],["EAST"],["FERTILIZE"],["DROP"]],"market":[["SELL","WHEAT",10]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["HARVEST"],["WATER"],["DROP"],["FERTILIZE"],["NORTH"],["HARVEST"],["NORTH"],["EAST"],["WEST"]],"market":[["SELL","WHEAT",10]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["NORTH"],["NORTH"],["HARVEST"],["WEST"],["SOUTH"],["NORTH"],["WEST"],["DROP"],["SOUTH"],["WEST"]],"market":[["SELL","WHEAT",10],["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["FERTILIZE"],["EAST"],["WEST"],["WEST"],["FERTILIZE"],["WATER"],["HARVEST"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["EAST"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["DROP"],["SOUTH"],["WEST"]],"market":[["SELL","CARROT",4],["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WEST"],["PASS"],["WATER"],["PASS"],["PASS"],["WEST"]],"market":[["SELL","WHEAT",7],["SELL","EGG",2]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","CARROT",24],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",3],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",4],["NORTH"],["NORTH"]],"market":[["SELL","MILK",5],["SELL","STRAWBERRY",2],["HIRE"]]},{"farmer":["WEST"],"hands":[["PLACE","MILK",3],["WEST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["NORTH"],["EAST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["EAST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["HARVEST"],["WEST"],["WEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["WEST"],["FEED"],["WEST"],["WATER"],["HARVEST"],["SOUTH"],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["NORTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["FERTILIZE"],["SOUTH"],["NORTH"],["HARVEST"],["WATER"],["SOUTH"],["WEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WATER"],["WATER"],["FERTILIZE"],["NORTH"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["HARVEST"]],"market":[["SELL","MILK",5],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["WEST"],["WATER"],["WATER"],["FERTILIZE"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["SOUTH"],["EAST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["HARVEST"],["HARVEST"],["NORTH"],["WEST"],["HARVEST"],["WEST"],["FERTILIZE"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["EAST"],["WEST"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["EAST"],["SOUTH"],["HARVEST"],["HARVEST"],["NORTH"],["FERTILIZE"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["HARVEST"],["WATER"],["EAST"],["SOUTH"],["EAST"],["WATER"],["FERTILIZE"],["WEST"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["FEED"],["HARVEST"],["EAST"],["SOUTH"],["EAST"],["HARVEST"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["DROP"],["NORTH"],["NORTH"],["EAST"],["FEED"],["SOUTH"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["NORTH"],["SOUTH"],["WEST"],["DROP"]],"market":[["SELL","CARROT",13],["SELL","EGG",8]]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["EAST"],["SOUTH"],["HARVEST"],["HARVEST"],["NORTH"],["DROP"],["WATER"],["NORTH"]],"market":[["SELL","WHEAT",13],["SELL","EGG",4]]},{"farmer":["EAST"],"hands":[["HARVEST"],["NORTH"],["EAST"],["SOUTH"],["NORTH"],["DROP"],["NORTH"],["WEST"],["HARVEST"],["NORTH"]],"market":[["SELL","WHEAT",13]]},{"farmer":["EAST"],"hands":[["SOUTH"],["DROP"],["EAST"],["FERTILIZE"],["NORTH"],["NORTH"],["EAST"],["WEST"],["WEST"],["NORTH"]],"market":[["SELL","MILK",6],["SELL","EGG",4],["SELL","FERTILIZER",2]]},{"farmer":["WATER"],"hands":[["WEST"],["NORTH"],["EAST"],["WATER"],["EAST"],["NORTH"],["EAST"],["NORTH"],["SOUTH"],["EAST"]],"market":[["SELL","WHEAT",7],["SELL","CARROT",3],["SELL","FERTILIZER",2]]},{"farmer":["HARVEST"],"hands":[["WATER"],["PASS"],["DROP"],["EAST"],["EAST"],["PASS"],["EAST"],["PASS"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","EGG",8],["SELL","EGG",8]]},{"farmer":["WEST"],"hands":[],"market":[["SELL","CARROT",24],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["HARVEST"],["WEST"],["NORTH"],["EAST"],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",2],["SELL","WHEAT",13],["SELL","WHEAT",13]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["EAST"],["HARVEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["SOUTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["WATER"],["HARVEST"],["SOUTH"],["HARVEST"],["NORTH"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","MILK",5]]},{"farmer":["EAST"],"hands":[["HARVEST"],["HARVEST"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["SOUTH"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["WEST"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["EAST"],["SOUTH"],["WEST"],["EAST"],["HARVEST"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["EAST"],["EAST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["WEST"],["SOUTH"],["EAST"],["HARVEST"],["SOUTH"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["EAST"],"hands":[["WATER"],["DROP"],["DROP"],["NORTH"],["WEST"],["WEST"],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2],["SELL","FERTILIZER",2]]},{"farmer":["DROP"],"hands":[["HARVEST"],["NORTH"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["DROP"],["HARVEST"]],"market":[["SELL","CARROT",7]]},{"farmer":["NORTH"],"hands":[["EAST"],["NORTH"],["EAST"],["NORTH"],["SOUTH"],["WATER"],["NORTH"],["NORTH"],["SOUTH"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["NORTH"],"hands":[["EAST"],["HARVEST"],["NORTH"],["DROP"],["WEST"],["HARVEST"],["EAST"],["NORTH"],["HARVEST"]],"market":[["SELL","CARROT",7],["SELL","FERTILIZER",2]]},{"farmer":["EAST"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["NORTH"],["NORTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["DROP"],["SOUTH"],["NORTH"],["PASS"],["HARVEST"],["WEST"],["DROP"],["NORTH"],["WEST"]],"market":[["SELL","STRAWBERRY",6],["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["PASS"],["SOUTH"],["EAST"],["PASS"],["EAST"],["WEST"],["PASS"],["EAST"],["WEST"]],"market":[["SELL","MILK",1],["SELL","WHEAT",13]]},{"farmer":["EAST"],"hands":[["PASS"],["DROP"],["EAST"],["PASS"],["EAST"],["SOUTH"],["PASS"],["EAST"],["SOUTH"]],"market":[["SELL","WHEAT",13],["SELL","EGG",4]]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["EAST"],["PASS"],["EAST"],["DROP"],["PASS"],["EAST"],["DROP"]],"market":[["SELL","WHEAT",10],["SELL","FERTILIZER",2],["SELL","FERTILIZER",2]]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["SOUTH"],["PASS"],["SOUTH"],["PASS"],["PASS"],["EAST"],["PASS"]],"market":[["SELL","WHEAT",7]]},{"farmer":["NORTH"],"hands":[["PASS"],["PASS"],["NORTH"],["PASS"],["DROP"],["PASS"],["PASS"],["SOUTH"],["PASS"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",2],["SELL","EGG",4]]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["EAST"],["PASS"],["PASS"],["PASS"],["PASS"],["NORTH"],["PASS"]],"market":[["SELL","WOOL",1000],["SELL","WHEAT",2],["SELL","FERTILIZER",1]]}]')
_PROXY=make_agent({0:_DEMO})
def archived_proxy_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
archived_proxy_agent.telemetry=_PROXY.chassis.diagnostics
agent=archived_proxy_agent
