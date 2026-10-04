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
_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1], ['HIRE']]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['PLANT', 'MELON'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 1], ['WATER'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['DROP'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PASS']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['NORTH'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'MELON'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'COW', 1], ['NORTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['PASS'], ['FEED'], ['PASS'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['PASS'], ['EAST'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PLANT', 'MELON'], ['DROP'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['DROP']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'STRAWBERRY'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['BUILD_PASTURE'], ['WATER'], ['WEST'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['HARVEST'], ['FEED'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['SOUTH'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['HARVEST'], ['PLACE', 'FERTILIZER', 1]], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['EAST'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['FEED'], ['PLANT', 'MELON'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['WATER'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['EAST'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['FEED'], ['HARVEST'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PASS'], ['FEED'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['EAST'], ['WATER'], ['FEED'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['EAST'], ['CARE'], ['PASS'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['NORTH'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['WEST'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['HARVEST'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['BUILD_PASTURE'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'SHEEP', 1], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['PICKUP', 'SHEEP', 1], ['DROP'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['BUILD_PASTURE'], ['CARE'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'SHEEP', 1], ['PLACE', 'SHEEP', 1], ['EAST'], ['NORTH'], ['EAST'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['BUILD_PASTURE'], ['PICKUP', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['BUILD_PASTURE'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PLACE', 'SHEEP', 1], ['EAST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['BUILD_PASTURE'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['PLACE', 'SHEEP', 1], ['EAST'], ['PLANT', 'STRAWBERRY'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['SOUTH'], ['WEST'], ['CARE'], ['DROP'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['WEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'MELON']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['CARE'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 4], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['CARE'], ['NORTH'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['NORTH'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['EAST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['FEED'], ['BUILD_COOP'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['PLACE', 'GOOSE', 1], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], ['BUY_LAND']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'GOOSE', 1], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'SHEEP', 1], ['WATER'], ['FEED'], ['CARE'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['NORTH'], ['WATER'], ['CARE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PLACE', 'SHEEP', 1], ['WATER'], ['EAST'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['FEED'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['DROP'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'GOOSE', 1], ['FEED'], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['BUILD_COOP'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_COOP'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['CARE'], ['BUILD_COOP'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['PLACE', 'GOOSE', 1], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PLACE', 'FERTILIZER', 2], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['PLACE', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['EAST'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_COOP'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['BUILD_COOP'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['CARE'], ['WATER'], ['WATER'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['WEST'], ['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['DROP'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['CARE'], ['NORTH'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['EAST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['FEED'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['CARE'], ['SOUTH'], ['FEED'], ['SOUTH'], ['CARE'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['NORTH'], ['CARE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['DROP'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['BUILD_COOP'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['CARE'], ['PLACE', 'GOOSE', 1], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['EAST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['PASS'], ['CARE'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FEED'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WEST'], ['CARE'], ['WATER'], ['HARVEST'], ['EAST'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['CARE'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['EAST'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['DROP'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 10]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['SOUTH'], ['FEED'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['NORTH'], ['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['CARE'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FEED'], ['SOUTH'], ['FEED'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['CARE'], ['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['NORTH'], ['PLACE', 'MILK', 3], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['FEED']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['FEED'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['CARE'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['DROP'], ['CARE'], ['SOUTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MELON', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['DROP'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 12], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['CARE'], ['CARE'], ['CARE'], ['FEED'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['FEED'], ['FEED'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['NORTH'], ['WEST'], ['NORTH'], ['CARE'], ['CARE'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['DROP'], ['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['PASS'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WEST'], ['DROP'], ['DROP'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['DROP']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 3], ['SELL', 'FERTILIZER', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['FEED'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['CARE'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['DROP'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE']], 'market': [['SELL', 'MELON', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['WATER'], ['DROP'], ['EAST'], ['DROP'], ['WATER'], ['SOUTH'], ['PASS'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['DROP'], ['NORTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['DROP'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['CARE'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WHEAT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['PASS'], ['HARVEST'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'MILK', 5], ['SELL', 'WOOL', 5], ['SELL', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'COW', 1], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['BUILD_PASTURE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DIG'], ['COLLECT_FERTILIZER'], ['PLACE', 'COW', 1], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['FEED'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DIG'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['DIG'], ['EAST'], ['WATER'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['DIG'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['DIG'], ['CARE'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'CARROT', 9], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['DIG'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['CARE'], ['FERTILIZE'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['DIG'], ['HARVEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['CARE'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['DIG'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['HARVEST'], ['FEED'], ['SOUTH'], ['NORTH'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['DIG'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['CARE'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['FEED'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['DIG'], ['SOUTH'], ['WATER'], ['EAST'], ['DIG'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['DROP']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['PASS'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'EGG', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'EGG', 4], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'EGG', 10], ['SELL', 'WHEAT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'EGG', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['CARE'], ['EAST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['DROP'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 3], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['CARE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['DROP'], ['WEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'CARROT', 6], ['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['CARE'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'EGG', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['DIG']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['DIG'], ['DIG'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['CARE'], ['FEED'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['DROP'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['DROP'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['DROP'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['HARVEST'], ['EAST'], ['EAST'], ['PASS'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'WHEAT', 10], ['SELL', 'EGG', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 4], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FEED'], ['FEED'], ['FEED'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['DROP'], ['WATER'], ['FERTILIZE'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['PASS'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['DROP'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['CARE']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['FEED'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['PASS'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH'], ['PASS'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 5], ['SELL', 'EGG', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'EGG', 4], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['PLACE', 'MILK', 3], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['FEED'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['FEED'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['DROP'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['CARE'], ['PASS'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 10]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['DIG'], ['COLLECT_FERTILIZER'], ['EAST'], ['PASS'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 10]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 1], ['SELL', 'EGG', 4], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['CARE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['DROP'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['DROP'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['EAST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['PASS']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['DROP'], ['PASS']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4], ['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 1], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['DIG'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['FEED'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['DROP'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 13]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 13]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['FEED'], ['SOUTH'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['DROP'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PASS'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['HARVEST'], ['NORTH'], ['DROP'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['EAST'], ['PASS'], ['DROP'], ['NORTH'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'WHEAT', 24], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['DROP'], ['EAST'], ['NORTH'], ['PASS'], ['NORTH'], ['DROP'], ['WEST'], ['PASS']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['EAST'], ['EAST'], ['PASS'], ['NORTH'], ['WEST'], ['DROP'], ['NORTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['NORTH'], ['DROP'], ['DROP'], ['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 30], ['SELL', 'WHEAT', 18], ['SELL', 'WHEAT', 12], ['SELL', 'EGG', 29], ['SELL', 'FERTILIZER', 6], ['SELL', 'WOOL', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['NORTH'], ['PASS']], 'market': []}]
_PROXY=make_agent({0:_DEMO})
def recent_demo_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_demo_agent.telemetry=_PROXY.chassis.diagnostics
agent=recent_demo_agent
