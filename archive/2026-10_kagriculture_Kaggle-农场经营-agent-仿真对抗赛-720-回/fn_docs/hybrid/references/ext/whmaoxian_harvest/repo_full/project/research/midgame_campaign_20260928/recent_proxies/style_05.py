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


# Public actions only; no hidden-state or rival-identity input.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<(QaJFa{L!Q?}NytXeDp7wAU7{Yzh>07dM7r7|0C*1UC;(-h%vl6q9@Q?CI*N>OQlS9Oub2x!N;lre~(Ry1M$O|GM~>Uw-}j-+sOL$Dc0V-+uUT@o97MufP2JKmW()Uwr=Y@4x)|Z-4vG&p-ck@$JXI{(Sr6+aGS<U2HC1-|a6pm!CF|zkYvz_vYj4htI#?f4{r^{NI;{zfAw&!}q)0``JG!{NdAoZ%#(}_Vu4XzMqXD8SjVPyLZPC{r3IezrEjGh#!*IeEj=jDBpg3`|i!ppQr8N<8S|Z8p&*w^Y`PwJU-0&9Dm#8q`kX+y+d>M)5VW>_YdFy_Uh=T{qDoV{8w_0p*`e_`1FD8$&jXpE}y=MbDoUM8^-I~<+{bMKTO?xEsnz>e~knBu-m=){MjFN@9uuQ*j)M3^)wH2`vT8>dK)x<k3Z-UEuQ<Q|NZmHbK^7OjKMkl@nL$-$v75I+}$qU^uyi9V3kXA#`Ceiec0WTx6Wq!@Eo{F7Ozs+EXI@Ld>>cv@nz;ui9<R3=JEUM>wTE(Q$tJNck#H>QF@cV)uw*@PWrr+rXHU=Ti20u@2`D)MtHnE^QR~El|Be(v;OE7%zw2s`SL0+T@C(f@fKJ++2r}m+|p?uIsmZc7X~=san5CbmWhsYC_IpHGt5@@VC0J*$W;{|aJ;I(?wNjg`c&zgv*DEn{QB<QyWQ)DpZ~PGe|Y=u?LYlC!o+*dJmkc$oPDKoFUbJu#mgMf#p4(5eDJU0@keLIbEx!H3ZF8!8uS73h&T6l?=u6O{Io}hiW%F&6~D?%`ta(HkCp3i<xhXS`kr1bowLW+Q<uEs*@4%eyioL4&;Crai?{A!lI;-~Zyl%i={K`^)|(SJW?7gva*pC-V+azhL4L_J1Jjp0{)TOog*!%PLLc&nD*}DZ?EbCaLdOds`lu_uZF!{)xxfDZOP>ErDsDg%L>uKR@SnyUR{164pJqjO0(jiZgTrw#B36>!mh2K0w}1>CnHMtMV&*C)j)YuX^NApokY7E`&GdtXIW%suJnr*-ttE1;?;HR>ABQ&NO~HoqUR4hsLNtv*)4*f;n(uG#|I!&a|MuyN5YRb2GIjbsJlx;zzun#6|J7UX`AaNAQiy)c9?%>Gcz*y9gRv|oyJi~zBR)K0GVtR>%P{FUZ}8lizWeA{E*I8tE$4GBo--YE^97A>VL>He_P{why;%Xth*#9~ElVGF97ICEo$x39BoN3`oaZcl@-sPj->h=*q9^bNcIb}3dPa|Kfzenqdv^crvgN-aufg<&j0Z-qj+;z&73-T0+%@2a1IN%RM~?wrz|ljlM+?CK8{xR3)4?dA7MhHUk<$DM6v$xJT>{UYOy)QMxO^+zBjg@N4<k+^2iuxc5Ph|Ma3GhK)SC(DV?{p>%*k;nY#1-|wNemn6aBDZW(Ef(-c<Slz;ii%A&dj2Wt86ymn!6N7q1gdSi4ASwLsi=bj40zaNKI;&ROBjND4fBt-mld?fFHV%F7ouuW|%_2sUw^@HUuZ1_nhRDZPs??V7SVc`hf_d3f7fWnjWU*b#AL=seWCNq|N&1i6EoOh?V}hh+RYay1UHjP3xT%N~D~yVzc|Npf>AVT=%g$^$(B5@J3}T)O*|>E;4fJzW#!1aI?(U8HvBuNeoGGKBOoZb6fL>4BS=ptfh2r|29nqJsoz8;0#dKX7*R#ppM}h}v+K7s#F2h4VDtAB-jmHq(%YBUVxJcJ9NAQyrHt^L?GC)tqZ*Aq_@z{(ux`XO3|o@%SLFW&B?%U(ev&^hms35A0I!?YWWNjQRJxxNfX`2$zVSX&pa-n}6EV%agqBKl7R&@a*GukN>hvmW1?rJeBDm@(5~>??KMg<&9FGf9Ige(dwF88NV6rYW>w<)dIMaLbSa@dqD`S#Bbh_!=@|xy@lAAeX)*4mw{_@Ri>|rnH>27WK{^A$N6T9*BCjWhG&|8G4O&blWYw+B@Z>fn3bLk8uD3bk6**rhHdDfAq{}k_vJWTpL%oK3`5&Vq^;(YpJeb%tW?|qt3btLL|5<y<}Xnk(9v_hyZii~n*%KHIT(9$@u`3df;fA67mANA5lm-v6L|OC-Q9<sLNmI5D|+mc4bKM!&f+*N=+Il-Vr4)lqg;VKaP)giu|bk+0~Ya|i(QUA9$~lFcOkcq3Nz6X51F-$Ko?&=3vP}>0-?ryyvvj|ULcxcK%+Hma;ZPyEMSaar|}#qG`EX#|Hb4&229*({u&HAQIOvpOJ@o;cYLYTs%J=(Z;5AG+i0CIdmInUa7$wQM(1iq)6rowJ2}AylD3%M@L&%{|L7UbG;Tqr%>c?37RCrITH2*aI%3tI>$c_zLp@lXDCY$KBA#P3<XKzmN~#E{e<tmC_EDapL@Q|BafG*oED%J!3kw88K3Plp%Dn_i+(f+MAzzK$kdQ;!lx+~n7=(o!voL||J`F5g2SG^b)e_Jfj>03!Oq+Ru`q+16<A@=#!<p7R)q)ZflV@=xOkzpN0uNdVp@51QfCeour$Tag1&p&uipT53o{2`5E?2GS{lKO8z+cKi8qdgxTwsR-*Gd-3N7|syii`hc6}M1Dx`@w#CY-%PL2L~?PA*^}1Yeb>)awWM7kLFiCko-JDbNFpsZ=oAv}(}H^RYA#NGrwgohrR>pI&bRkUK(W31Z=M_7#AKe9@MzPL={>6(o#OV7yDqi!3Hy^xVnb0hh(i5*A-IPHS%Y7|kvu{hXqEgi>^Jui#leYgVyaW<#qTrOb*s0&<1zyR_Eg!UIbRa;L5co|Ab8G@Q89(H+h)*b$T;R^bIABgsc&_*lsw?mP*gg+m_2X#a)!mS#MG_H2_p=ou=L797kj1eswu-j`?3SI70vTzTXah%~ktp_9e?;qALWKc&Xt@MVrtu=q^Ei^}f#%GfvcSda%FP&B0#DcF=Bb8E$6qdN(NKQw8DhS<&>!>m8?W@3zpYB(~RTRG{+0oO*4K)g`w0W6-&WxC1j*$(zzfQTq6_bpNmz{|jNS<!AJf*<`sDggjdd2|_ql6XVFS7pjl)qcC=F@l{G7yyYrmC@`AHxyqQ1c|_b2C8C2^cY#+IO%6rTPQbinxOzE0y-^R(df;%jsR$05vEKdKo9}BCRR8GdQc>f&}mzMT~f2xF*9$;K%y@mx~Kvf#G5IL!#Lz*{=2Y!XkG`RXzcoQNgL%OZpcZNlCd{jLLRHaoXN;Ye-sKlv#uVIfzjwTU|yuT{xq9nbPk}SjP$5bGBMq&-=J`6P9T5hecPsd2?@&jLwl5pOLaRapt@|b2mOo@cqwvcbZv!6#xblnP{)KlI5$~oW-}B={*>!^4lP%>`NHK2CKR+y@ga$~TX1&@rED61sg+3R1Sm&m;9oTku%?azJrSH37%o!Ocuix!F3=z-LNvLIX=N-dpEVFaSru~K7ynbpM1)`fvV{}`>+4}g#r^W#NCE)K?&)u7Kf#eJ0ty@BTt<V6berR+Su?zqt8zJx)B+mPD4zgAFUNhvt9zO}OR!^rA4RotQfkyy6Pb`3AX;uy{+}vnEwi9?mp$6PAzGtuW>z!Po#Ku$C+#pNtbnpMx*S_-u7HNTBlLGQ(cnTJ5=byt=1PI(UH~z!{U?b|q7a+crLtdRQ12lMVpmE~W3jW9UEz`|;Xt5gEy$kGAgF7kGH1(p);6L5PFT=ZVk9k`POgY2li?333W(!#5vJS_N_?DDJlN0r?(@bA{^KJ#lScGuil_8+Sd*vv6BhnarTfLc%0Fo<%K8WdDm+71B8+PV5uRz>!_&*8`d{WW+<&NC$uUTxCx^>N7oJ2-U>X7#411@I1(M60FbB4uDr7k2*3uH0==0`O=j$%<KT7CBR3J8+kstGeQ6EiG(>U@Zi?7M$J)bJDZ`d|1Ax?;$O?b>uBzFEYxbFNyh)bh+t4}8faWv&t#gf5sQ7Jj~(nfiBl&Yr)BNjfjaD6P<T^Llone7&{!&J-%)_{~ckbc0~(4)<0Y9Q&C7fz)3VQuPVgTWrWrtn8EPZ^A>J1Az|CgiiwTPsu|8zi}Sw=GvQ4vN-4jogmSRq)vz?ee`VfITA-#SLM2awCE|edQQ{4Lj#Y>||bUm0eVGo8fBjh1h7hoQ5tlu$5|_nsSx#vK1sS*AfdHDuXF&RSS}-U3em427X=>4u(-sJg4bQrNU8}QLHO<M~L0&_Bs7OYK<I+X$XqSEy*{Gi=3_LIjrH2?b+cE(sx4w9VR`)U?dQJvR9Vlzg~0`h@UC13wdyo$rw`b4RXm<s*8e-E5)&Z30_K7qC)xL*=Kij2P|j<Q;j$VwcAE1hSPu8Yr4y<Te>Z2C!HbgBq`3doU-ZF5*b!7x${rPe_pG6^&NI}Jw_PBttnc|LM1$Ts$t92n`oV4*FGW~2;x;1xk=PxS8|GExXmR(;)R3lmZ!%UN<7;hBVweYA#V8koFqL7Eq7oNzaVbGx=uOSeNLK5fZ{%#8CgrEURs}x^MiIZ&&DEHB-c9F*O2F;p@js+U&*kbr(r&)bVp~lHvq#_*NoAQTW@ATe&cyHqm+KJ*3K-$JeE<gGJ+7tlJN||;I+a9+bX$^JmU*6Y-c;-BCY<8#6CH}XB;vKJ~kwJEn49g)LKCPn7v7<ZUl~U_uY3Fn^#^}ZbD3n3OcN~1!`iC@3C=t`DLnBdSnp}mQYNQ0VD@A-0GJ>jq{$Unun8`OQE&2tP+RUMo~(10-h};2}g#znm7wBDkwEhQ(4_6SAyiZlE6ReO1IR=7}E{(l%l705!z`)J(}5ruj13+V+YD7OL?gaNYA0ZN4)H$wPfnzWuKbX-ddH^9Katar5Ax58NHxQb^2LqdF_-Dh*a#5#Q}JFa*SPJD68r`<32_3aEQc-JWf%9yvoDI|8|(BI6G(UephVUYPt54sIWphgLs+;-;e<(=k@uN7(f@)yqG|(PIm9CZcrcsFFXdI7FD<Pdd*+EF_%H_O6#1jG=|IQ8!<yccge;}80MX1&=|~QyaFZoF?AZCysBU(Mk%0VE*Bwx94I3ScupbBxKh?O_ex;Icw<B)gEOd=W*w=*=cGXSF|F@dHv!7y!UOFvpj?|TNr=D&{IltREoweb%!hPb&F39rF3aKHRCwzWka<;UYXMsOTs=3h#s6iI^VNZ8h>*I)Fz_Af5!egS$+8Q*vwqTJI*T+V@t9t0fd?wH{k2$?iLC;7h4BfKASL%n{FRr$6^lzNX`gmQu;G+bVicadtdmq3LK)RZ4^anVr5Q=$xE0Y2ROq;lycLJpCWF964(|uV`!>_g&akT6ULrsU#zfGcBuec>C0QCZ41oUzuyyjicBU=pA0!a))mWh>4e$nY98~djm2*^^+=5I;XFX64jx5@W5}jTP05<Fyde6a=iro{5g(r10MVe;q5Oc61zVS1Q0DDrD&tluO`|AjYg{QUfiMW<_17kX-<%>NC%2^P5a|B0AM)kD!gF?FvnFyvLblRuUl?_JyhITe0aaHOc8c7kXI*y{!W1t3<;m<qCWE-3@QkFv7IW~2@9PRa&!5T*Dg_M~e+Z3ndLj8<VFpmo6lMJ8+zd}CVYJeIt5NoKWY87RWYLW7iB!WV)Q?V2w+iD>wtE=YP@5j@OFqldn3wC_2fdtTAwZjXTJlreSXk8>+AR6e3n4EE6kS!b8+i#bO#IUg3R!4JOEhGWp2pci}Wy^^L+a@APpc0Y0TgoWT)cb&Xh(^j3ULt8C$@lip*V{ognNT!%^f}h6t<XEw;YBf_2#$QLgAHZ|tztxtFeKNPg2Wo_S$%qr0p<)rLs<Ys)3Li&rHp_^*X*smLr`n{l)R|)jBh@b?h&})*fRBRjd-1gaeGcV7f1~=0IwdV&LP_LQ4=>*_9zpD!*@@HViII{B~3-);M$t2ye-;Bw6x8Oow$10lYuJWfvLepn1mIP7^}<Tglm^lQU)JR50@_hKJ*z3Tm8xTTwN!P6T@d>Tz&cxQV}sHwkZloH&6k2!|3&^9G)a1bTNAtaHGCUEZ<@G!?M}B-Dq2?p#mK<oFX%O*H}0+3%~)m!6V1<lRYwv7Ys+Jz?j-ddX6p0no0%~TvSG>3KU4_X7*Ue!mRFKHQ)j6(#V7-OdswWNMBJyAe(dPO+@6RGquI~XtlXAIG}a_c9w!Q7C5U*P86APu_)^$zib0fs_CGij66URQQm3B#;2rJm_2#?nMi$<G8!nl=f=y!C9`J76W<$d|2(GJD@_IkDz*!cbhekv8cLbmEC*766b9TJD18QH!8l<|9!7bnS;|BK36^-y2q2lS8&h&!akELk%CG-%R8^dwD!`<{7lLXtP9DaC&KuEGoO3#4n0)kV<g5ynis3#I11O9`TH3^FCsS~RK~SVX#RQ&ye=rX3pXx(5%o>(ub1U2L6vVPf{>q0`m?Bs|zfBptEcP?SGQjNn&7@=(^qt!$g)2f({$!&G7BFydK-i^0NtKFXANoeIx}yST8gcTZ;-`|V9w#ScuE`o1;pv00yp<`6vd@*)0%<Yi5<U?|h*v0o7gl3j8n};ruxc~rb%SFEzMFLu%w;PfCSU3Gg3h1J?=E<tq6&XhOvQ>Y?V2`9=0=wY^-qVly+ph|*#d_8*9F}#hT#p6IiXc55}V_1Nm{SKz<Ee0Y$Mef%vLtWl;<>p-GX%1qVq@yFUcBu4Gul($aP;=L@U>`3Rrk{f+l1fx`XfZYVl5=A9a8C(C~jWa>_ya`Ool$;6ZP8$-;WGnE7KjOv@6K2P1u&N)hzn*&sy}C&j-nN+%z2JcW#kUNe&}OWQ>kxnjvZx$9~Cs_7qaDl4#up0%DHi$jM?wu4Qav~<yPH_ufRs_STQMCcK3lBJMLwia&=@WIG!aw<!i`lmh%uD%-bkvz72h%1*>G3j#~yGpD}Cps;Nx>5PjQrER&GPzu)utKe+(QA}o1FI`%Y;l==4(-Vr1e1GI!^KE*WyJR~sv}VKeT|}i!pXZVNHU@}qO|=9@|LP<Ivo32Ez8JIY-U89Yqh%f9`sxY|0i+Bwa|n|o}xuUj0Yf39FP7j>w`wIl@!ZDxTRF+VMTk~%@7R8YJ-3_M3tle9DEJHf25KjGPjV0e3qaPp_7m-leG-i5)B|^3|R}N6xvgi<SnF%B{dB~FYId(@3qQxJbvd(fh}83#ixIuyJrMim{8Yn_AI#o5yV*}P(&?WnjT@c1}b>Cg1ln$vd-Dnk{yw4kuu@pnvBjA8+B3cc)zp6!js58ZsHzQY+ZLo+IWvM^PpSJ^Z=b|_pKf~?_k9Z8WH?M$$YI9laic?-oMrCXhC)*wQ4O^I4@``^q~BmF`l+IaI|Ig6k9nbmY&TInU_+l_~Gt{+lM;@$2Tf;hzr>0+^4d!0#q%v+9a|tUUNZ^(i#^fE24$pMph?7aJ#A1!aH0OL_v(`VtcaOq!`k`-CwNGakUqOdZQ5isH!M)okV8Yc&<T^udCG>*dgs02|TO>1L9Q1hOQNCx1Bs(bPmaS`kV&zBkF5tHr@ueL%=@UV<hGnf?*CM_FL_@;%YS<8X7Y(&k`GsO0ojq0J<8oU8(QCJ3nN)tl=;Wc+SDT2B4i>TtYF2rw;<l2jW*AZO(IDou=|{zvHRPt7PbjQmoru+ep|jagsHVPk0%DV%smTxQc3#o9~&DlfeDWE2kcfA&2A+f8QJLJ^~tI&6t5)CG+0sa-L5`*wV{q#3KO3I5NluWGhaxAl3n5r-{y$XdixSL742~O+T}rk2L-#Q~&M17487J@R$!IPsV5w;9CeJX5EVe^ox$yT~MS}u;Sq#(0+HkKhtKds`B>hQdMrYYuXOw7(u<F?Rp93`Pbca3h9WPsm~E<f{|udsH-AhCvUzTISjnOE@ilmZvy3G7LpI$p?38o8N7~AuA-eZvqqyR;OyWV8C=BRtQ{<J<ruH6(kx4pvc_VKRzSHXmNj&o=mM8<+Rdg{9>S^<!I8i!b9n_i%chNDQ7T1Tk3i-TXbMfu6x9knn!1rG1Moc3;u)yOH0Dihp8?folv>I}(HkPzeyz{dngSRMyUC0c=jpM2INj9<I8RRCG9F(7&n09y0?auK)|SeZz2Ata@*y}plO`ACn!x5V2VBNf$T28#BjB4N_m%yP-dI|@rrVVd>s{>%-KY()P`4g0sTk0mjs`0GeMw$bwqE7=wsy1I$UNejw4Aorl`U@7fcL|5lnd4I%IbYduE6hyRjvhd8F>7!MAqn()wUS_&1$aC7w?c|;Wk?<88@I+Ry^Lr{0}M)gW!EA7gNd0p0=p5RUC#7L26`MGryWTSAuvB`DsUCU|kRIX2eFZ8=t12Q|0S=cGmZUvJ4t8KvKN~rV5nNSG6u7mP**_GQ+*E743mRt~i*Krtx>Ih3#1VqPRJy#e1W19bFP?NFE>DHr-S}p@2Yil-ws&Z~$yJD_j{K`Pv$Iv=YMX!HTOYYk+agjHU_*A?E=KLDcp$d$YF~K_JO%*8#E8%wz*tyVXwB@*F*YIDyHdQIc(dTCw*nA21edp+uI9wzhU!2sezj6JO82e_Y%La5CgYaM@&zm?sNO%MeRSAcScVamAJ_VRE#I_N0v2BCz&0t6g6Rlb5?h7P?+mMitd_)RbGRS_ZH6x7W8p3DN^AiTaV#4+vc{l&cPdp3`m)XTvvcf35)f!CS`ZDXGEK$nfF85hfK~|3T23t6J3-CeRY(PgihV=9OCS@9*AxeEl$IPz{81XjK}%A!M|Aj{aee&OkFJ?T~PW!8fGN4Bg3tXM8{xF*UoQaC-j?fDJL31Uz@UyjN;QnhmD%j@vv&ph-4~n$@bzh+s8%pa)cX-B^Zp23H43Uc+T~WEUiXDyTyf3U+yATs5RpQEd8MARKrJ=OWo_a6yW%KE&c!O48tU#gdySb%fxG2*4S6)q9f8QidaQwN~dUJGcT{Q3$u^-tkSP(|PU$Cg;fR!-M2l$$dyvXcgj>D6tu|-{jEf2}_0Ihy>5_%~n_lnimoXb~+}p<Bj&lf&dWatGf7r4R9sJ@C=#*<HorJa(6bJk?a5hK&e#g7T0FIc#AcZfhU#F9%pAW{gkw8yVbbz2hHYndr~%>7uDGenuBq_)VB;<5Mb9)X&Ic`OL67G)v^j_dHEGoJZ(pc<Ir|sJ#1x2+0xlNt{W}D+};MHR*9e6<CKpJ?UU<*H~h%)C>u@j<3_|KROfZ5Q)kRW`U31hD!XTejHit?X!-~1#7Arx+;+6rt1Xe*1kV6brO@bIP-MAXuQ)A`)KN5P9;fp3KG|{g(9mxDCb&Oh$h>XJnMF?3tASWDC_qHJak(#*+$V&q$^NW{MKg)DSnuDebppY$mbx-sTS8sXD#q8gE-Ps#$XcdTX(X%7R$Z^S)U$|!KBCnmZe6)p8H1ew3LJPdOpa-u&={5n7cV9#X%P2?XJjzSkb74^hfd5{)$hGJl(j-gG+Zqdyr((-{0B#L#yshh+lbN43UnP3?E|kmmv<>}bhLLR1pI)Kq9dN}iGY>SMVfBd2elUJ9%tZLxX?@QGDY%z^p5sk2g^kXs8#T&sZCQtYOcQoBSxydu0m+`r8dbYJ<!(GEs=Ja0CC3I>k;BI9Vh{d?&i^MsSy`La5{BL4HaCg?OwZaRiieE$>J*Y{~qDxEVW5$1%x)7)$TLPAeU(wwRAPpp%9&(9Avd3M#6vx?HGc2$BlwvUyyb6NrW^<vv5>=cJW>72rN*LC4$zu6rjlV6;y~Aoagr!&qe(p^q~%$XRk<tXNO{yA<Ib&+N0JDQ|TaukLqCHU3T1dHm>I0Ra0QZFXG^(C{Bq<0oTdwfOXRoI0_}$^@^8LaD+fWAjn`Pd+d&t{2RONg<V%hbA7bGpH+f2`&GTsYc+kv^25u*8B>xB0P6LU8xL9IgcLAX-Kcaxy$wzLMv{b}cUVom3bkRZ<9wk-J!XG9#Y;2gi}ubF95t}=z$!S3>c7es&}B|KlBedw%4=zJxZ^~Src-D?>iVo#&w$^Y&eHz@noX`89IJ!^cva@%oVla<8QD5#)EIWu8VGO4XdYHmw>$?^$Kn#ND=l+a@}9g11%vjvu$dlzeo<GWfoSS5m{tsV7uG6LO}Od|$h?zOXckNq1WcNGz9bF+;DDHO(Zv#`%Ir?M1$z->XVnwc^7$yap&>#mms*9Hj17_3;*TTuq?KEo!r*48&85)5xQl85jt_6Lvp2l&v$j+hO`@&xGRmp3NfQ+wr%eU&E;g?xnqqc}?cS1yL25OJ|MJ68GWZZLVyL~@)!;cgjQNJJX3eK4!hHTPkc^15b6^G4xYhcEn-OhYLY(nXL?wH67sao%q&V93r?iOIzgt-S8X~upHaNq>K(0mWov<F}a%8NaN^lLUs3@ES!iA<5%((IZ0ImC}ls43nGrl&cO-X0+2ph#8vLtE>N7<vNfbZ9gA)S{11f|kbu*jkW%^1+<Cj?~&i%j#H9jneu1FB&pz9_R_7Bz$&#8_kvg2fq#K!#UkDW!D}`n5cu3Q%IXl4oJnL=Rx^09PdIUX{6#HFB(Vop7Q^=vi>9*p(moGxD5s#O5lJHFmUWk!@6;<yti5R(U<MaE!c33MEOzw#b`S!uZYFQmfqhc#%V9sm)3@Rc%L0b?MQg<WSrifnqf4cj9HQLE4tF+_UIRbRLl|#fFki)0ou6z8arrdMN@^W2KKcIs>o8g5UEsCl}ofETgjfC^II*>ArCH3lW;4Z(}JnCC3(DD5?mO*q2hBcKcf8MO%)Pw$XZ;>4{mTl3v%h!XSwOXuJtBlar%A-3baCD3FS%?hh?=hel521PKpEX(C^igtLTH8>SE~Rd<|1PSV}#>BxNfhvp559#(7VLBk-QZtp522G0AM3`Bj_G^w&2{#M<W?@z91P$eMsGdC0R+ES64cLew>1oUgwG4P6y6A7nH7Vj7NYtLJ!L3AuS{fc-WcqT{NHKs~cAZzexsdlWvWdX;8tMlp>3`Q^NQ7Dm{!x~e2+Ug8dyt5+eDO#F&O2Z_`JS)ql%ivTxxmHZly%QwzR#yI&yct~!Z0-@BXs4n~qR#{A6&0DL&%l&R4#T>VIL{ckrDPp8Oq;)2Xil~&^5wXv6L@R?^PC_K)l;Uv0DutELZ(U$UIS*R<>dmCnwzo{mAma8;_+KRPMTgAymh3|U`xs>Ql>n??Gsg#MfiVHsiVru+ufuiC>5!QDSsooc_$$Y>trVSL<1m)G#^!h*4y80LD<umKivIr`*8R9%dd*W9!Byh3Hs#aVJ4)roTjUF?4@I8Gl1xLjehLn7whIaSX!GCj25C)?X^x!M_vzG?drgHh`@#NY?AukCrE|Y3v{8v7<S=NSoHxc?4<RDLki-hwng4c0O~QgbtZ#kV@*yCubcr+N7b1iUA@r|ciID%t*-`%*>d<mU<w-Jsa1Gwx&-F+Y#5b4-|y<JRE&049+u{59s`VF`K#eD6bIHs$hin><3YOQ)zsh_%<53<Sm^^$Xfie~dd)aUlD<n%W7=3)glEIGWuy(!V4D?s4LC8QM`dQHRIO~@I%Z5)BU8OrG?_><4MT*<tv+s0PK#gZtd%G+;<jK91;m6{TDoe!5`)teo0mg!wAbl~Muta~iMe1GKIP`oo#B{9RH0Un<kI+rj*t*$6)>(-2bLi+uQZ$#E2#WFr+{fg>afW8DclH*oFXk(*XKl9UI7t^8PKq8$Mg_}Q4C0~!DHeu+ZNISDn<<inAgMXSC?QQindK1Nsh=KSkkW0)r=XR7e8u}&Gufp&1yFEx*lNG2Z-F((NaYRNZy9GF^?IC!elFy4Ac<#aLETg5^6<&x@xc29v088qB|>+w8b)y8fMjc3}_J5y1E@}_}w)V!Q|j<Dl4WSv8Q7RAW6o{c4g-gCtz;Y;hBn0uvuJs@JrAwv&_p+owjvC>!PB?-dx{e4W+K+E;Z&+yH}S@(x#<pyIHC_S`%It%`N~;pbMCJn00WWQQGetr>V`(MfPDF#i2h#u3}r$tIsBBsaPtpujLyQU^rSoLBTbqFkI@2DJcTsr1W%n@n)hb&I-h$QD{7a=oSVSNNhyp)wfZjeC3Go#z|&M(kI-2Tumhv>7ko{3pc-FUF^S}_`k$5<0i~Wt!CU_Z<XYMuTeHz;o8OS+X*p3it`zfkM{FZ%{Q<5g)BKNAkoA0qiOZ8%Bri)q*o)~vENw|XGKDD&o9ssBCw)vux~G3UD{ZaR{M@@0WjlULZRuEW3qdH5e11I*{)5%d5rm2Q1Q(QwqhT6iols5{8kTMgoR)f0%EIibG(>PwI=d)jU8hJ?l$a1;pe>-^v576>drom1-i41{$#n1JO^>p*lJHgR|!Ja)j3xVmSE1TD+;pH=y%ncl)jQVK(1^Gt5(UF7}c#rz|Lfid2XJV2^;^OaLn_#jz%_@>6kZdo&gBc4C943j`c3ch_ZLVks7YQm~<FIT<IBpH9k75$yF91)kyy&YtG&%eux@pE#S*IWe8=XW=CF*>R~8Z4fL*MF2IWyFTlIu4n$xTKm8ACc+}D')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
