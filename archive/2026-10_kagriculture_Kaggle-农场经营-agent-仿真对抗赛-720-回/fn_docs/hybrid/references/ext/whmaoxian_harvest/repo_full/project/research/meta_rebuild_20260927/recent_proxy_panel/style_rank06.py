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
_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_PRODUCT', 'WHEAT', 10]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 1], ['WEST']], 'market': []}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WEST'], ['PLACE', 'SHEEP', 1], ['WEST'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['WEST'], ['PICKUP', 'SHEEP', 1], ['EAST'], ['PICKUP', 'SHEEP', 1], ['WEST']], 'market': []}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WEST'], ['CARE'], ['CARE'], ['CARE'], ['BUILD_PASTURE']], 'market': []}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['WEST'], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['EAST']], 'market': []}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['BUILD_COOP'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['BUILD_PASTURE']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['DIG'], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['BUILD_COOP'], ['WEST'], ['FEED'], ['FEED'], ['WEST']], 'market': [['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLACE', 'SHEEP', 1], ['BUILD_PASTURE'], ['FEED'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['PLACE', 'SHEEP', 1], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['WEST'], ['PLANT', 'MELON']], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PICKUP', 'COW', 1], ['WEST'], ['PLANT', 'MELON']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['DIG'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['BUILD_PASTURE'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['NORTH'], ['PLACE', 'COW', 1], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['DROP'], ['WATER']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['WATER']], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PLANT', 'MELON'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['EAST']], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['WATER']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'MELON'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['DROP'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['PICKUP', 'COW', 1], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['BUILD_PASTURE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['PLACE', 'COW', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['CARE'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE']]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['EAST'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['FEED'], ['PICKUP', 'WHEAT', 1], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['DROP']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['EAST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['PICKUP', 'COW', 1], ['FEED'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'MELON'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'WHEAT', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['HARVEST'], ['DROP']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['DROP'], ['WATER'], ['CARE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['EAST'], ['BUILD_PASTURE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['PLACE', 'COW', 1]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['EAST'], ['FEED'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['CARE'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['HARVEST'], ['CARE'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['PLANT', 'MELON'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['CARE'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PASS'], ['PICKUP', 'WHEAT', 2], ['PASS'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PASS'], ['NORTH'], ['PASS'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['DROP'], ['PASS'], ['WEST'], ['PASS'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['CARE'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['PLACE', 'COW', 1], ['FEED'], ['PASS'], ['DROP'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'GOOSE', 1], ['PICKUP', 'COW', 1], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['DROP']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['PICKUP', 'COW', 1], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['BUILD_PASTURE'], ['FEED'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['BUILD_COOP'], ['PLACE', 'COW', 1], ['CARE'], ['BUILD_PASTURE'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'GOOSE', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['DROP']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['DROP'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['SOUTH'], ['BUILD_PASTURE'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['PICKUP', 'GOOSE', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['PLACE', 'COW', 1], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['EAST'], ['CARE'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLACE', 'GOOSE', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 1], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['WATER'], ['DROP'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['EAST'], ['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['DROP'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['DROP'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'GOOSE', 1], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['PICKUP', 'GOOSE', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['SOUTH'], ['EAST'], ['EAST'], ['FEED'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['DROP'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['BUILD_COOP'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WATER'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['WATER'], ['NORTH'], ['EAST'], ['CARE'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DROP'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['EAST'], ['PASS'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 29]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['DROP'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['FEED'], ['EAST'], ['EAST'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['DROP'], ['EAST'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['CARE'], ['EAST'], ['NORTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['FEED'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PICKUP', 'WHEAT', 4], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['FEED']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['PASS'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['PASS']], 'market': [['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE']]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['CARE'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['DROP'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_LAND']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_LAND']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['CARE'], ['FEED'], ['WATER'], ['EAST']], 'market': [['BUY_LAND']]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['DROP']], 'market': [['BUY_LAND']]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['DROP'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'MILK', 1], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['PICKUP', 'GOOSE', 1], ['DROP'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['BUILD_COOP'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 4], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['WEST'], ['DROP'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP'], ['DROP'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['WEST'], ['WEST'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['DROP'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 3], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WHEAT', 8]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WEST'], ['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 5], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'EGG', 2], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 18]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['EAST'], ['DROP'], ['WEST'], ['WATER'], ['DIG'], ['FEED'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['CARE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['DROP'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 2], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['DROP'], ['HARVEST'], ['WEST'], ['WATER'], ['DROP'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['CARE'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['CARE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['DROP'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['DROP'], ['DROP'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['PASS'], ['PASS'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'EGG', 8], ['SELL', 'WHEAT', 9], ['SELL', 'FERTILIZER', 5]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST'], ['EAST'], ['PASS'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['CARE']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['CARE'], ['CARE']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['CARE'], ['EAST'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'TOMATO'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WATER'], ['PASS'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PASS'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MELON', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST']], 'market': [['SELL', 'FERTILIZER', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 4], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DIG'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['PLANT', 'TOMATO'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['DROP'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['HARVEST'], ['PLANT', 'TOMATO'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 11], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MELON', 15], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MELON', 5], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 6], ['WEST'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['PICKUP', 'FERTILIZER', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['EAST'], ['WATER'], ['FERTILIZE'], ['DROP'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['PLANT', 'TOMATO'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'MILK', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 7], ['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['PASS'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'MELON', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 2], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['DIG'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'MELON', 5]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['PLACE', 'MILK', 3]], 'market': [['SELL', 'MELON', 11]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['CARE'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['CARE'], ['SOUTH'], ['HARVEST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['DROP'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 10], ['SELL', 'MILK', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['EAST'], ['EAST'], ['NORTH'], ['PLACE', 'MILK', 3], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'EGG', 10]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 7]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['FEED'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['DROP'], ['EAST'], ['EAST'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['PASS'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['CARE'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'TOMATO'], ['PLANT', 'TOMATO'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['DROP'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 13], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'TOMATO'], ['EAST'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 6], ['SELL', 'WHEAT', 5], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PASS'], ['EAST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 5], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['PICKUP', 'FERTILIZER', 5]], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'TOMATO'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['DROP'], ['WEST'], ['DROP'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 10], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['NORTH'], ['DROP'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 5], ['SELL', 'WHEAT', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['HARVEST'], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'FERTILIZER', 1], ['DROP'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'EGG', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 1], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 7]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['PASS'], ['CARE'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PASS'], ['NORTH']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 8], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['CARE'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['WEST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 11], ['SELL', 'EGG', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['DROP'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['PASS'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 2], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['DIG'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['DIG'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 11], ['SELL', 'EGG', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['PASS'], ['HARVEST'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PASS'], ['NORTH']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 5], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['FEED'], ['FEED'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 14]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['DIG']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'EGG', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['DROP'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'TOMATO', 5]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['WEST'], ['WATER'], ['WEST'], ['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 5], ['SELL', 'EGG', 4], ['SELL', 'TOMATO', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['CARE'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['DIG'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['DIG'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['FEED'], ['HARVEST'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['DIG'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 8], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['CARE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['DIG'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['DIG'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['DIG'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 7], ['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['HARVEST'], ['WEST'], ['DIG'], ['NORTH'], ['DROP'], ['WEST'], ['DIG'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['DIG']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['PASS']], 'market': [['SELL', 'EGG', 6], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['DROP'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['DIG'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['SOUTH'], ['DIG'], ['WATER'], ['SOUTH'], ['WATER'], ['DIG'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 6], ['WEST']], 'market': [['SELL', 'FERTILIZER', 9], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['HARVEST'], ['EAST'], ['FEED'], ['EAST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['EAST'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['FEED'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 8], ['SELL', 'WOOL', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['DIG'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['DIG'], ['SOUTH'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['DROP'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['DROP'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['DROP'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 12], ['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['PASS'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 9], ['SELL', 'EGG', 8], ['SELL', 'MILK', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WEST'], ['WATER'], ['PASS'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 3], ['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['CARE'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WATER'], ['FEED'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['DIG'], ['FERTILIZE']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['DROP'], ['PLANT', 'CARROT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 1]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'WHEAT', 19], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FERTILIZE'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WEST'], ['DIG'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['DIG'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['DIG'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['DROP'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['DROP'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'WHEAT', 15], ['SELL', 'CARROT', 7], ['SELL', 'EGG', 6], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['PASS']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 5], ['SELL', 'CARROT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 2]], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['PLACE', 'MILK', 4]], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'CARROT', 4]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['DIG'], ['PLANT', 'CARROT'], ['WEST'], ['WEST'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['DIG'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['DROP'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['SOUTH'], ['HARVEST'], ['DROP'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'CARROT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['PICKUP', 'FERTILIZER', 1], ['SOUTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 23], ['BUY_SEED', 'CARROT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['DIG'], ['WEST'], ['PASS'], ['FERTILIZE'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'TOMATO', 17], ['SELL', 'CARROT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['HARVEST'], ['FERTILIZE'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 2]], 'market': [['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'CARROT', 4]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLANT', 'CARROT'], ['CARE'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 9]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'CARROT', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['SOUTH'], ['DIG'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['DROP'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 11], ['SELL', 'CARROT', 5]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['PASS'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'TOMATO', 20], ['SELL', 'STRAWBERRY', 6], ['SELL', 'CARROT', 4], ['SELL', 'WHEAT', 5]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'CARROT', 14], ['SELL', 'WHEAT', 15], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'FERTILIZER', 2], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PICKUP', 'FERTILIZER', 1], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['FEED'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['DROP'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['DROP'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 4], ['SELL', 'WHEAT', 3]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'CARROT', 8], ['SELL', 'WHEAT', 6], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PASS']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'TOMATO', 5]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 19], ['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 14], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['DROP']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 6], ['SELL', 'CARROT', 2], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['SOUTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['WEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['DROP'], ['SOUTH'], ['WEST'], ['NORTH'], ['DROP'], ['NORTH'], ['DROP']], 'market': [['SELL', 'CARROT', 14], ['SELL', 'WHEAT', 20]]}, {'farmer': ['DROP'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['HARVEST'], ['EAST'], ['DROP'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'CARROT', 16], ['SELL', 'WHEAT', 9], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['DROP'], ['DROP'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'CARROT', 14], ['SELL', 'TOMATO', 4], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'WOOL', 28], ['SELL', 'CARROT', 8], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 1]]}]
_PROXY=make_agent({0:_DEMO})
def recent_demo_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_demo_agent.telemetry=_PROXY.chassis.diagnostics
agent=recent_demo_agent
