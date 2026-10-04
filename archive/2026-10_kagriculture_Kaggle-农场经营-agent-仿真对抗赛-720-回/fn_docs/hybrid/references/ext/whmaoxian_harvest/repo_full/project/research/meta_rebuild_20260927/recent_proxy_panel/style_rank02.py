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


# Archived development demonstration; responsive guards, fixed production.
_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['WEST'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2]], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['DROP'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PASS'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['DROP'], ['EAST'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['FEED'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['PASS'], ['CARE'], ['CARE'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['FEED'], ['FEED'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_COOP'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['PASS'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['WEST'], ['BUILD_COOP'], ['WATER'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['PLACE', 'GOOSE', 1], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PLACE', 'GOOSE', 1]], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['DROP'], ['WATER'], ['FEED'], ['NORTH'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['CARE'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['PASS'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_LAND']]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['SOUTH'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_LAND'], ['BUY_LAND']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['DROP'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['BUILD_COOP'], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLACE', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PASS'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['DROP'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['PASS'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['NORTH'], ['PASS'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PICKUP', 'COW', 1], ['CARE'], ['EAST'], ['FEED'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['BUILD_PASTURE'], ['WEST'], ['DROP'], ['CARE'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'GOOSE', 1], ['FEED'], ['PLACE', 'COW', 1], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['BUILD_COOP'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_COOP'], ['FEED'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['BUILD_COOP'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'GOOSE', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['WEST'], ['CARE'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PASS'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FEED'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['CARE'], ['SOUTH'], ['WEST'], ['DROP'], ['EAST'], ['EAST'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['DROP'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['DROP']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['DROP'], ['NORTH'], ['CARE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['PASS'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['FEED'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['FEED'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['DROP'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['DROP'], ['SOUTH'], ['WATER'], ['NORTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['FEED'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['CARE'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['CARE']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['PASS'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['DROP'], ['WATER']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 6], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 3], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['CARE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['EAST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['DIG'], ['WATER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['BUILD_PASTURE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WEST'], ['PLACE', 'SHEEP', 1], ['BUILD_PASTURE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLACE', 'SHEEP', 1], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['FEED'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['FEED'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['FEED'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['DROP'], ['WEST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MELON', 12]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['PICKUP', 'WHEAT', 2], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['FEED'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['CARE'], ['WATER'], ['EAST'], ['CARE'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['DROP'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PASS'], ['WATER'], ['HARVEST'], ['PASS'], ['HARVEST'], ['PASS'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['PLACE', 'MILK', 6], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['CARE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['WEST'], ['CARE'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['PASS'], ['PASS'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['BUY_SEED', 'TOMATO', 10]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['WEST'], ['WATER'], ['FEED'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 3], ['FERTILIZE'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['PLANT', 'TOMATO']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['NORTH'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['DIG'], ['NORTH'], ['FEED'], ['EAST'], ['DROP'], ['FEED'], ['SOUTH'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['PLANT', 'TOMATO'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['CARE'], ['WEST'], ['PLANT', 'TOMATO']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['DROP'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 10], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['FEED'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['HARVEST'], ['PASS'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['CARE'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['FEED'], ['PLANT', 'TOMATO'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['DIG'], ['EAST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['PLANT', 'TOMATO'], ['FERTILIZE'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'TOMATO'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'TOMATO'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['DIG'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'TOMATO'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['DIG'], ['FERTILIZE'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['PASS'], ['NORTH'], ['SOUTH'], ['FEED'], ['PASS'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'TOMATO'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['DROP'], ['DROP'], ['WEST'], ['NORTH'], ['DROP'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['DIG'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'TOMATO'], ['HARVEST'], ['FEED'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['DIG'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['DIG'], ['EAST'], ['EAST'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['DROP'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['EAST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 8]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['FEED'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['CARE'], ['FEED'], ['SOUTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['BUILD_PASTURE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['WATER'], ['FERTILIZE'], ['FEED'], ['FEED'], ['SOUTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['DIG'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['CARE'], ['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['BUILD_PASTURE'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['WATER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['CARE'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['EAST'], ['BUILD_PASTURE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['PLACE', 'SHEEP', 1], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['CARE'], ['FEED']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['DROP'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['CARE'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DIG'], ['CARE'], ['WEST'], ['WEST'], ['DIG'], ['NORTH'], ['DIG'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['DIG'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['DROP'], ['HARVEST'], ['PLANT', 'WHEAT'], ['DROP'], ['FEED'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['DROP'], ['PICKUP', 'WHEAT', 2], ['DIG'], ['WATER'], ['EAST'], ['CARE'], ['NORTH'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['FEED'], ['NORTH'], ['DIG'], ['EAST'], ['DIG'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['DIG'], ['WEST'], ['FEED'], ['EAST'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['DIG'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['DIG']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['DIG'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['DIG'], ['WEST'], ['DIG']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PASS'], ['HARVEST'], ['EAST'], ['PASS'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_PRODUCT', 'WHEAT', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['PLACE', 'MILK', 6], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['DIG'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['CARE'], ['WATER'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['DIG'], ['FEED'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['CARE'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['DIG'], ['FEED'], ['SOUTH'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['PASS'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['DROP'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PASS'], ['DROP'], ['PASS']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['DIG'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['CARE'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WEST'], ['WEST'], ['DIG'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['CARE'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['DIG'], ['DIG'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['HARVEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 8], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 6]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['PASS'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'EGG', 6], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DIG'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['HARVEST'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['DIG'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['CARE'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['FEED'], ['HARVEST'], ['EAST'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['HARVEST'], ['DROP'], ['EAST'], ['HARVEST'], ['PASS'], ['CARE'], ['EAST'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'WHEAT', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['WEST'], ['SOUTH'], ['DIG'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['FEED'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['EAST'], ['CARE'], ['DIG'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'CARROT'], ['FEED'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['SOUTH'], ['NORTH'], ['FEED'], ['PLANT', 'CARROT'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PLANT', 'CARROT'], ['DROP'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['DIG'], ['DROP'], ['SOUTH'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['PASS'], ['DROP'], ['PASS'], ['HARVEST'], ['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['SELL', 'TOMATO', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['EAST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FEED'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['DROP'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WATER'], ['DROP'], ['WATER'], ['PASS'], ['DROP'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['SELL', 'TOMATO', 14]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['DIG'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['DROP'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'CARROT', 7]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 4], ['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['HARVEST'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['SELL', 'TOMATO', 16]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['DROP'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['DROP'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['DROP'], ['NORTH'], ['EAST']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['PASS'], ['DROP'], ['DROP']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['DROP'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'TOMATO', 4], ['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['DROP'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['DROP'], ['DROP'], ['DROP'], ['DROP'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'TOMATO', 1000], ['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4]]}]
_PROXY=make_agent({0:_DEMO})
def recent_demo_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_demo_agent.telemetry=_PROXY.chassis.diagnostics
agent=recent_demo_agent
