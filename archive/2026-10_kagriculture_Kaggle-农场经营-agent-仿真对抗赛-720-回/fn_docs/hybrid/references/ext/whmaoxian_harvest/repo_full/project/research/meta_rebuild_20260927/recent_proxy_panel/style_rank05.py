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
_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['DROP'], ['EAST'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['FEED'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['PASS'], ['CARE'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'COW', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_PASTURE'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['PLACE', 'COW', 1], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'MELON'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['BUILD_COOP'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['PLACE', 'GOOSE', 1], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['FEED'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['FEED'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['FEED'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['DROP'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['FEED'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_LAND'], ['BUY_LAND']]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['DROP'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 2], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['BUILD_COOP'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['DROP'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'GOOSE', 1], ['WEST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['BUILD_COOP'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['PLACE', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['NORTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PICKUP', 'COW', 1], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['CARE'], ['BUILD_PASTURE'], ['SOUTH'], ['DROP'], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['PLACE', 'COW', 1], ['EAST'], ['PICKUP', 'COW', 1], ['SOUTH'], ['EAST'], ['PICKUP', 'COW', 1], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['DROP'], ['NORTH'], ['WEST'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['CARE'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['DROP'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['NORTH'], ['FEED'], ['NORTH'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'COW', 1], ['CARE'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['CARE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['CARE'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WEST'], ['FEED'], ['FEED'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['EAST'], ['PASS'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['NORTH'], ['WATER'], ['WEST'], ['PASS'], ['EAST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['EAST'], ['CARE'], ['CARE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['EAST'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['SOUTH'], ['WEST'], ['DROP'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['CARE'], ['EAST']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['FEED'], ['WEST'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED'], ['NORTH'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['DROP'], ['CARE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 9], ['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WEST'], ['DROP'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['CARE'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['FEED'], ['EAST']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['CARE'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 5], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['DROP'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['DROP'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'STRAWBERRY', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PLACE', 'SHEEP', 1], ['PLACE', 'SHEEP', 1], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['PASS'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['DROP'], ['PASS'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['CARE'], ['HARVEST'], ['FEED'], ['DROP'], ['WATER'], ['DROP'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['DROP'], ['WEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 9], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['PASS']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PASS'], ['EAST'], ['WEST'], ['PASS'], ['CARE'], ['CARE'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FEED'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['CARE'], ['FEED'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['HARVEST'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['CARE'], ['HARVEST'], ['WATER'], ['CARE'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['DIG'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PASS'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['DROP'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['SOUTH'], ['FEED'], ['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['DROP'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['DROP'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 10]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['DIG'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['DROP'], ['WATER'], ['NORTH'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['DIG']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 5]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['FEED'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['CARE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['DIG'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['DIG'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['DIG'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['DROP'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FERTILIZE'], ['WEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['DIG'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['NORTH'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['DROP'], ['SOUTH'], ['PASS'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': [['SELL', 'MILK', 3], ['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['FEED'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['DIG'], ['DROP'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 10]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['EAST'], ['NORTH'], ['PASS'], ['CARE'], ['CARE'], ['NORTH'], ['DROP'], ['EAST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['WEST'], ['CARE'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['DIG'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['PASS'], ['WATER'], ['FERTILIZE'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DIG'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['DIG'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['HARVEST'], ['NORTH'], ['DIG'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['DIG']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['DIG'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['DIG'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['DIG'], ['PLANT', 'CARROT'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['FEED'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['DIG'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['HARVEST'], ['DIG'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['DIG'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['DIG'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'CARROT'], ['CARE'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['DIG'], ['HARVEST'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['DIG'], ['DROP'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST'], ['PASS']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['SOUTH'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['FEED'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['FEED'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['PICKUP', 'WHEAT', 2], ['CARE'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST'], ['CARE'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['DIG']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['NORTH'], ['WEST'], ['EAST'], ['DROP'], ['DROP'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['DROP'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['DROP'], ['SOUTH'], ['WATER'], ['EAST'], ['PASS'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['FEED'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['DIG'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'CARROT'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['DROP'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 3]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['DROP'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['DIG'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['HARVEST'], ['DIG'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['FEED'], ['HARVEST'], ['CARE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['DIG'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['FEED'], ['NORTH'], ['CARE'], ['PLANT', 'CARROT'], ['DIG'], ['WEST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['DROP'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['PASS'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['DROP'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['FEED']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['DROP'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['WEST'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['DROP'], ['FERTILIZE'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'CARROT', 12], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['DROP'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['CARE'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['DROP'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WEST'], ['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['DROP'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'CARROT', 3]]}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['DROP'], ['WATER'], ['PASS'], ['HARVEST'], ['PASS'], ['FERTILIZE'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['DROP'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['EAST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FERTILIZE'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['DROP'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['PASS'], ['COLLECT_FERTILIZER'], ['DROP'], ['DROP'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['DROP'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['DROP'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DROP'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['DROP'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['PASS'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['PASS'], ['EAST'], ['DROP'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['EAST'], ['DROP'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1000], ['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4], ['SELL', 'EGG', 4]]}]
_PROXY=make_agent({0:_DEMO})
def recent_demo_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_demo_agent.telemetry=_PROXY.chassis.diagnostics
agent=recent_demo_agent
