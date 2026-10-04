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
_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PASS']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 1], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['DROP']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PASS'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['PASS'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PASS'], ['DROP'], ['EAST'], ['WEST'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PICKUP', 'WHEAT', 2], ['PASS'], ['SOUTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['NORTH'], ['PASS'], ['DROP'], ['NORTH'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['PASS'], ['PASS'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FEED'], ['PASS'], ['PASS'], ['HARVEST'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['PASS'], ['PASS'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PLACE', 'COW', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_PASTURE'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['PLACE', 'COW', 1], ['SOUTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['DROP'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['EAST'], ['DROP'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['NORTH'], ['FEED'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['BUILD_COOP'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['FEED'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WATER'], ['FEED'], ['CARE'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['PICKUP', 'WHEAT', 2], ['WEST'], ['CARE'], ['PASS'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['EAST'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['DROP'], ['WEST'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['CARE'], ['PASS'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['FEED'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['FEED'], ['WEST'], ['CARE'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_LAND']]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['DROP'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['DROP'], ['EAST'], ['DROP']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH'], ['PASS'], ['NORTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['PASS']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['BUILD_COOP'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['DROP'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 7]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 1], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'COW', 1], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['DROP'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['SOUTH'], ['CARE'], ['EAST'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['BUILD_PASTURE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLACE', 'COW', 1], ['SOUTH'], ['CARE'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['CARE'], ['WATER'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['DIG'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['PASS'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['BUILD_COOP'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MELON', 12], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['EAST'], ['CARE'], ['WEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['FEED'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['EAST'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['SOUTH'], ['WEST'], ['DROP'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['FEED'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['FEED'], ['WEST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['CARE'], ['CARE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['DROP'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['EAST'], ['FERTILIZE'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WEST'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['FEED'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['FERTILIZE'], ['EAST'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'TOMATO'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['CARE'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['WEST'], ['PASS'], ['WATER'], ['PASS']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE'], ['FEED'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['CARE'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WATER'], ['DROP'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['PASS'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['DROP'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['PASS'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 5], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['CARE'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['DROP'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['FEED'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['CARE'], ['WATER'], ['HARVEST'], ['WEST'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['PASS'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'WOOL', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 1]], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['FEED'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['PASS'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['FEED'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['PASS'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WATER'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['FEED'], ['DROP'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['CARE'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'TOMATO'], ['EAST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['SOUTH'], ['FEED'], ['CARE'], ['DROP'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['FEED'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['FEED'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['CARE'], ['CARE'], ['WEST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['HARVEST'], ['DROP'], ['EAST'], ['DROP'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 12]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WEST'], ['CARE'], ['PLANT', 'TOMATO'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'TOMATO'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['PLACE', 'MILK', 6], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['FEED']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['DROP'], ['DROP'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 8], ['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['DROP'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 12]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['DROP'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'TOMATO'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PASS'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['DIG'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['DIG'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WATER'], ['DIG'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['PASS'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLACE', 'MILK', 3], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['FEED'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['FEED'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['DROP'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DROP'], ['WEST'], ['WEST'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['DIG'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['DIG'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'TOMATO', 4], ['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 12], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['FEED']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['DROP'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 6]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['DIG'], ['FEED'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['DIG'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['DIG'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['DIG'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['DIG'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['DIG'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['CARE'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['CARE'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['DIG'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['DIG'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['DIG'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['CARE'], ['HARVEST'], ['WEST'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['DROP'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'MILK', 6]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['PASS'], ['NORTH'], ['EAST'], ['EAST'], ['HARVEST'], ['DIG']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['WEST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['CARE'], ['WATER'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FEED'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['EAST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['DIG'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['NORTH'], ['DROP'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['PASS'], ['WEST'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['EAST'], ['PASS'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['PASS'], ['WATER']], 'market': [['SELL', 'TOMATO', 3], ['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['HARVEST'], ['PASS'], ['PASS'], ['WATER'], ['FERTILIZE'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'EGG', 4], ['SELL', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'FERTILIZER', 1], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['PLACE', 'MILK', 3], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['DIG'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['DIG'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['DIG'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['DIG'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'EGG', 4], ['SELL', 'WHEAT', 4]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DROP'], ['DIG'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'TOMATO', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['CARE'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'TOMATO', 6]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['DROP'], ['SOUTH'], ['SOUTH'], ['WATER'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'TOMATO', 6], ['SELL', 'WHEAT', 8]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['DROP'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['PASS'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['EAST'], ['FEED'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['DIG']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['EAST'], ['PLANT', 'CARROT'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['EAST']], 'market': [['SELL', 'TOMATO', 3]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'TOMATO', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['HARVEST'], ['DROP'], ['WEST'], ['WEST'], ['WATER'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MILK', 7], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['EAST'], ['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['PASS'], ['WEST'], ['WEST'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['DIG'], ['FEED'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['CARE'], ['PLANT', 'CARROT'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'TOMATO', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['DROP'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 2], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 13], ['SELL', 'CARROT', 7], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': [['SELL', 'TOMATO', 8]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['DROP'], ['EAST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['PASS'], ['WATER'], ['PASS'], ['DROP'], ['EAST'], ['PASS'], ['FERTILIZE'], ['NORTH'], ['PASS']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'CARROT', 8], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['EAST'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WEST'], ['DROP'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 6]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['DROP'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 24], ['SELL', 'WHEAT', 24], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 6]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['DROP'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['DROP'], ['PASS'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PASS'], ['SOUTH'], ['WEST'], ['DROP'], ['PASS'], ['PASS'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 100], ['SELL', 'CARROT', 100], ['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def recent_demo_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_demo_agent.telemetry=_PROXY.chassis.diagnostics
agent=recent_demo_agent
