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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<O>ZPua{Mnm_hH%OP?T@fOs_Q9kvQOR+*k{QAi!%FFxCgzH^cwkv;3&8u8fR`%va6PE__mp-Bb0xUuI-v<j?<e_HV!b_Se7scJ@y{pMAXf^y%zjbN27Q{^!5`*Oxzh`S{mgfBTQW{P&m7Kc9W~`Om-H{Ph0En-6E3v$wbVv(5R#X7T4wKkRlNhralDcl+-1+xsuy?0?wZeEIL2hll^&9JTWO+dqB&IBP@F-cP#^9}bUse8CUz?{;VI2h`t1Q@;EB{=>Upz6{&_=f{6EwPe=Hc?bC)4`XWmj`wysXdiCg?$DV1eD>4r-Te=bJw~7QyHEG?KgltMlX#v^;`0wKj+!*Rbous89P^}QUNhd_Eaxpg{$=Rqb8%=6`8GD_({A_f%Wr?&eYpMUY_s);>v<gJ>kGX1xi@J1o<8UnE#CXbzkPl5-uR9<VsH$9x}V;2)Q-g)cQ?zPf;F&Q&3HKWH}|_c(&=olU*2;(+Vl2r&|lm=W3(U+`*UA5N1t9^leg~a1@(FVbo+TZ1n6*Byk-O1srr6lEp^^KJSxp4AK!nXu`f)1*v{pFKR&3p`W!sG>d7dWzhSx3%X7RmG+>9w9WXk?@%@L+#g@ds%m$!&#>5u9Y&pE%vhi8r#nS{IS^(yJ{UM)T5<i?`e97y;ls|q&t|{mFXhv6gaQ1;b_U-M554*Sbzx;7`cmMvw`+s?CPGUG`HgRH7&K~JomZYiR`UO`jTK><6+@e8=jTH_hK18!u!ylp+=}R?v)Uy#}JoDY%?Z@mKdHxQ+g)PB_ZN5#OKbeA0&6RVp_2(kqfyruvp2SPj)ZK4cev8L1%zv}%`7*3r#fR5EO>Mb<aaf=KGMmge`$q4y4fWE8>4kD>$A?U9oSm%or$o!<sZDH0EQ~z*G<g=k+y?M~^B<ENQ8Qa~;AzWCYu(%H{~z-D52+XdL+II>mO{~bAp0Ghqsjftur7M=DH|d+WNL?61WA&PWPg4+NGB7)K=;B;#cYqsf-z??F&O0Jnr{SdgnaZgHq!?SWbkh>fYMn`JhZ6<QVs4LfIA<Wwn|UIhV!~wxiBd@BOC2G8$aCK{d1?`{OQw!4vYBk?exmj$oq7EceDR)cX#(^Z@%Z9;6CcJ88Lf7vlXEK02>BvSqye<Z2)xm<rUKcXBPb84To`q=gz{4L=$URmh-U|@0kv|`Gg`r#DGb_=z()|>e+ItN>|kMl+@V84<5#Q5_AWCr8@?^_#Ei@yTg8tul#R@%)V$JoYKt8!!KXK&SN&`E82O}+nJsB+E(4UX|m*Te%K^rY?wxrb8kg!kguui3fFIn_93_!;W_D;&<NrRw<9u0^vTE`y+6LFj?P61zc89b3>h36KffR&BIq+Dz)Pl8aCn=#y12a-qn_~si69!nIoXzTnxagSIH&vLL55R0WV*7kpcCMaGCI)?kA8*z0B=Cv?9eow9)9Gtgr%dc5qBNHAL3wn0~)3A=R$7`+v@O!0~#({oR9yA&Bg}e>)3)<WdhynV1ciW3RZ%T<M1FljaWlo%Yr<uEore1J2+U?s03$DHc}ll2w;o^7hcVv<Xzarp;!Z|)rhxvaRXT;hOD)KiRB59Ot5SUj+aHzWn)L;neDJGuutMrT{sX15qH}Iq5w1D2w*{9yPi_&mKIEBXpiN*IgEw1AgI)>!l2ZMJqxasmwg8<PKY~8cPzd|*_#Jj5Pz>RM$N+}tpdiQHSl_FBl1fuK)reZw?>TYh`~whZZJGq57z=sJDi4Bi<+-tGJ}I<eSj5xTF++QXtwf-=<BN*(J6`Tghn+8d9~y3JZp!6vY4gkk7CUOPq~8G7i!`PW+^*fNu*QYhyyN9BowlYv%{aJNt`a$!YBYYBwY*J<7WdDx`jOhlnA*43m2?oywaD0H?7KvA?YFqiwKSQf{8g44hu_+o<Gq~Yq7$SVO<3iYP5+3zMb${>emS&ML?p9eRJhJYCw({Wa-335P1W|WFl$mEpS>naIzCkYjR<?t{&rmB@%)2{IC&EVFCNbF?P9kmi@ulnE63cbKZ`Q4`m}$J3jqW$yPk9)XWwF@0oX^*r3CTxV`=G97Xust@_2&e0NrfyMya|>I=n^m(YmQIv)eNt~w{c(gHVQ;)w&82f>fc@C3t^iXKl2fWkaZ9659*3IbMknvwRb<IN0g_Z*<S7#X^Z(>E>7?{9BE?O2dw`T@59mT_(aV?&noVml795;j)0cC@9YRvd^r5sw2tMlv0ABRX@F_i@`39*C2x^9T|Ckq5a>F>{G_%G=xJ1qIHt`JH91N|{)h<rP;ZFjZNB`wmP7n1Yy^G2?^O)}piI0H95TEv7cH*vx$3@@vY6H=J&;1ik6SM=LJL>{Kgk>UaPrR@y$L$XHx&*zZYc?|F}vbV)Hp#NSf*blQXk#d)%%K$g}_mcHA>e^y#MBuy&jc4Nm{kNYSW(OyU>?8yW~M8vCbq>ikiRM#b2Ldzp8Ln78^DozUm<%rF9VmOe%!jbT?17d*L%#yKHXmd5*pbj+Fz??N?I|_1l+GC1<LLOhL#Rm&2Zhv?<Nj69%wv-QLtzM|$0TqctH{sHfxh$gI@syQ@v>HN??3D=?>G+Cv(^D`D*lS?H&h9-CdmNp99zlih0q6q!9T@U5_epmkMiinfpC5OPnFGnf@;N)T=p2lUVVW63hH(eiTsTC!WuKG$<(apJ+Di=l#5fro(ijKyg^%d0qAeanT7FVsVGrbKXxxn{1=fHOPZmLi@EUJY8tNqe!hVRUOhdc;jBr?XV96@`1kfoXIo{02GT71x>1Ru8X%?@sjcLYBn%>ik<gz6V{=~XlP&N{u>Ky}%+F@;Wc!|JUV_wI)Bu=19u*#c2IM=&HPa0$<UXNu!TqM{VcbN!K`s4c#e>zIZTF1)}JQ{Wq<-Id(wyPB_{yin2%S%N0Uj?2IaLbgfpWE;_(u*di8V26dkUX<>qL~MxOKr|28)?#DLPLt)29tIg3?{{$TA@9}p_N7tO%lp?aU(G%i#vNZIdEff$jDSO_4I;OT+dhIRx?r|)<k~Nym`O|?306w{U%P`VQZsCFCc0rVJ&x<srWq_W$@E-5f%d=Z*Yd8cwt#A-`R02Q4hVEa?u5p6kF(opcrru+7Q=Gy2MPma$~*tg*brCy^PXmvHoNo#XO4cLNSX9#FZS)3bc~R!YVh_xxj_Nk)AVzRN=0aZRKPkIm$likF9T!<5&_w@^*l)Vh%ap4i<(zV|zUn<|l3ou;tjX$QBz2OAZ!MAV^?=kI-07!{-m!2zH>0o<V5IP?4-bRYZFM=LJnr!Hs-jRBrrM_?i7^I1gZc!d!giWPliMfD|yV&O<kLef?0&8Gx}}={oNkB>$0Qg2<1<>Hjba)S*WcZun&yRJ(d8AvA!cm5yf|04FES>4nJdMA!iyxfqKB!p|syc(wT{<}v2T(M?)t4w!n3ySdslSV^|5fL(N|!R$y3sBG+w6IPHAO(6@yg~}JstZ~%7si?=(#D?g9Os!#xG;4<cSw3~d3R&s{Y;m13a$y)vaeJzI1TOPpNbGepPz7?aYndF=G#hE6bziqT9+niw0W_PiX2xr-fio}|!Nir<H%@j*)my3rM1T-v=n5m5fU~39RzeLhGsrL?nX_e9SdGN{A&C<uw&r@P)T_6sV1M9%(@31rRL09he5Qnh(@us5wRm;0jSUAS*xoI4pTWZj6J&zBV@wNPx09l#%P*VS+Faz&g97T>$?~H8=H%{vMP%l(_D7VXXZrmnwf_9lu%K$j1UlR~HyltSs&doBwn*(AVbl>@UxO!-->KYVdd4A9MY4VjH|1M>>SF>6V6?}IFwpp$|7_Wz9{!`o)OB2wMSOTq=mI8PJmnl;<(sc4Z3b)ZFu7Uy4}g=Yv1+63%AAdf)M~yc=_uM6RnmUl^<qSww3?mK#0({3%PL~HzyPM19JP}PJ`2nXR9{^T4&N>XSubY)Ijlfj|4yCv4W<S^S*TEnyeW(msKBphlnhsEgywvAOU5rOY#z;?V`|UCCRq@QV6&{>H5f((hL(2fJf=7m9Xtu&2kv^40mvlzRw?{APs^S!hUNb)ZCZe~WP5S`Ad~;I5?_Yq!JsdbGLn9=L+?OFt|m4ixvqS{IaKFzjxstKSv0vnkH<G_2QVgZgfZgA!Lw|%$v>421|?qoezF@wyasE3@u{X3X39G`HD+;s`dktqS3Cw)a1S4TTNSTS=_bUgS(GZ<v?}jtm9EgsX5yg=wVD^b1r@dTznTANa9NHI5IM{;uaYA~V9Y>m8g_#&4VKXYv~s#x?G9vHbwenms0PXNPINhi>Cve{p+a(TzgrF;ee4Q@=)DMH8q|R##<A7X2&GNqW(dZrd?d1BXv2l?3WD>^vZeSs0OKs`)D+w#nPHOot$wsMtB2W?$)BH=*vy+Ci}{+t=I8MvY?Tuq#xOI)5x;{l_i<;;L$;!?3BvmOoe{;f2*1r$417=$*@rj)B}^~9)-^)uY%{Y+Ej?tpT|z8YJK0TXHj|c9chC6cVsrQI6Uqwj&w#rj+gSlDIgDPw^LBXjd%sX~!MtD*|0Civ0YCFBPb;<fO@%e$om-$Cd7V1J862vl#_B%9VE3uY8N4z^0Np5=6)?nZ$emY(2xP?8v=W5&HeyuHqdmYokfRHvcZT>O&d$h*5HLWW7?uRsr-b!VjzgE`Poo<wepM{)6>Xq`ArB-6zyX*V&oUTE(0G7<DbY#TpcWujS<}FBP)*i(RLZRP7?O(v<f0;*0XL5sg+L2=W~HqXo>ssU<52O_L`RWW4m-FH_+Y6ZFU{M)8Yu($ywsrNfT9@-OG>FZtAlMd@b=@8b)zYi#_yOJED%Nm-qcrb>MCla3y%?^=}}*1Jf)!K3r7GPiu&a&^i!oiWDx;ys}`!rg8;cx%--|3WZ1&XDfjaXeAt;9+8L||*JX{V3y+#?tKbRu1qD`2Au=-#;7|!_K|IzvrLq}+nG^9?u`+{TVJSZdrb$bugC<;Og6!~Su_XL~d<LkSu_zc08@K!Z`!7wq0<P#EDn63L1FqME1MJEkufif|SG##}HYCzP#D1a)3~qId1D0j4FN<bL9-Fnv(MDG5fTz*)<|)6I=Iad??WPXApCnpxqh%!AnR@BLkpQ8Gy2(8Qvl5K{XGAhWb(BNKnP9s@W+EOR)vY4KCPGAn%7CmR1oIbbX>~kZ#RQIq4@eKS!zqnI)7UZW*1}XaD9pcyPI=RtW0GG2cILHOhl6N#_76;FgH#9Dp(K!5XNNP;!;3;9$|&<q%1nXzxX{BtIXLM(3LsxnH{i*X`nI3LK#MAvfi*vdB4=MEGlJETB4HLa#G6`4yP>>9FA!WzF(+gbb)VzCdQ1XTw1c@DwXK8=VwF%ZQE^kVc!8r?{p9btI<CYN0M|W^#d*`;R>bmIYz$jq^>k~BSdRmI9sTK2*~!T92aP~9g#aF;_q$*obV^KIeT5Pey?B2qv@g8)L*#9PJo`*s3HHyF+M{tV`}k9|U+(^gxRgO7q{SR~z^(;f*X{8Y<NKMnD3uo!9hRU$)u_Hfs%RTE5_}0};{3J1{6iXg<Pt<iZQPzc+8|2_Rkx20Z4_3pol+R#L6I5lW`vKRLw3Fd!$wF#e=k&klMFn=R^nZ?JwzF+V2iuslwKe;<C`lfQPzN+yQ~Y`i0zBBt-z_$Fkf>oi&Z?zl>#!i%991a_*9x{utt>%Kk(=w6^Z&zAEPP)t%QYD!pu)lioz=~Nx(qhM2dL%Xbqg>MJ(((pTO=w1)Ty6WS~@&z$WXCr;s`aO^Oh_wZ+7Mb{k8J0J!kFZ<s;@Zypqw$F`r*kBUATy2TWU%gC#c>ReAvy?pTH#d6g~3A9_K4VE77b)O)xE=W*NKJ173FZ3_xKK^A=#4Y?L(u1?d$d!JSQ1HleKX2E*bO;9U8c`8_7{PYw*)P57lm=wE^Rjl~?o-=HT^Vzb!^+54s-HFfoKNJYfs4j87{(-V{6XT)n}-s8fb0&PEA3Q`Z4#tebC|Z2=BzX9yHc`zXKE|jNrSoRyUNNX5-k$ZVfN(i)4*zV<2RVP?utAV#l-X)icm!9oa9Kc@YBpv%|%7DZNV9Gg-H;dUE+kp{D{aY=HN~i+h^N0cL#l2-iuSSvreIUM2Dw)?eJ~e#aV0!O<zegzrq%hIPTq-XWrd<ON|C(wZexqAd+LqOGrWokziVwNj`3loniPF$~RD0R<x&@aACGq6&m3=Lh5kDe!Ip>xbM3e6<eYZm{~6&>%1cTZwu|jfEP`Hq(57JNlhQ`xChQp!r99XK-%I3Ekh)EEYPN_BEEM-XaFn@oc*Eu#VUCuEQQhhk06NndN@xk6eqDA0Z)TFiY$i=fSeET8wS_NPBYyjC>8uzlxr6GmZ*R!Q0`ZD;5qgtVV`Suq7ziOjVH-0vHe^aY*vcIU=~=)YoTxeN??ug0w!INon;HRxhAnMMjJvijVPUDA;~@Cc(!c(mGcd<{32so^I8{12(9DbxF?uPvNN(koqf2W<cua%Mm~@ruo0J%8-T(2$=S#_H2DYW)N<X){^|w@$Qt-|G@G?pV|MlvlXYdZJ4qp7;n^g~NVC)XL0qfc#(w80y|OTbmonwKjEtF{4-q|oVi8?lgi&wfk{~Dz*{jPS$?(sGZE1Cue(Db`(*i<24G3$Rop@)G;yp)Mg5OqF6DuK!4NAnzM|wDwI`3v0IqGepR4UuO;78d_M-e9H4uNqC&9R22ALtV+;=sV76%JNUTa?1FKDbD%yc$QcVIjymdz~S7ZU&E$1Ojn8PhZ(lDsj?90#LNA$%FXBIj*-$;+g~~dSWMyON1PqRNLPTBZy@cUDQ&I91f7TavV(Q%EFZVP;2xu!7VOK){db+1{~S-NeD}b=7V(wJ(_|fiJV?aY!Y$t(FrNQukm#8MM`A2xH1tsvXF{ck?Jdqlie`rZ5Pf6_`#5eL51U)9P1UKWGa80VOWuTY->*1!bD&QbygZpLY9aBWj}ozNxfO<oUd#M15j1l(~&Q5LZXsU$YSk&-i}HqqD)9nLbQK2aJkoAv8)K<1H({jyUgUaRJS1ufvcG}WmUZ08D!nN<UCG*5lItNpt!m%743zR!pu_k9_6LLZAmM&#X}k-7&G~NQA!=-eLiH|(P_m;4NX)X-HDbcHqF>(6^jksvvP}htvw%AQKDvI4Hl?4q);#~mZB~k9t2V*6Dk^1hcB$meIn>gPmx^eARqp3BfI*lP<D`3VNo=7MOIQOGjCRfU;c4<IvPB`OyCryT01*{?r(p*xxckMOT;WDL>(&q!{F3LETJRyXHs+8-B^*9W2>EJ(FB1)R1)DNC{I(@8BvE4F-=xiotxPr=_nh=Ayzn_A!bk;dsdZ`-A}Y+2D9kf%@Ye7!h|}iCxkLOg)0zP>=eLe9BRgyC@tr_R7FSRMai@<9Wuu2E^b01Ar{wg1pl!@6Wx4H*hgBxT|wLhHGuNalY{fc7=6CqEBV-Nwvv!i%&E59E|H5lK-B2h&=O0%0%OTjVWLPTT!9`bXFfI870<SmX(WsWSS%7vYlWJ|q$H^@{j@(wNvgw<p{O~wTIw;FU6=_Wz5=TQ+0+|ZCPi(JOUngjCp`%)F>K9>&n#{HSh(^1_l`KZ1+bHt89HQXEO}H)Yftb|N;($U>eG1Hw6p7q0IUiqutfyaASJcAntxsru=ejIaTAhNWo=U=)ruv7Y;Ydf8kR1vI#o+DLDzq0K#*CNXOM++5;-0PBDD+o0N|&pxKqG@Ix;nrtw57KI_f$NqVw0R`a^SHeeK*{T?nrNkj!pvFt7PRG-I1NEM&qt>(mUA;b4WvRf$}Lb4G|2u3#!x7+57qB_1wP(t|3^DdXR{VC|V_DNcoy4;AV%#MQWe>=s`JR-71YI8~LhwlbAI)u|Tcuux#YJm70Ct|MVZ)TAswhB^by>e0;a<E#|HxS@fa$0fT>j_0jj%8XZE<lr!fNO@oIRrSOSPhp2*vBj0-BK=+2Rg=%es@7%qPi8b!OSQcy0$sHd5V^{^ki#bY)-`gfklL`D!;{2S4jAY&%pk0T`caQxcLcCLzdBMgo~KfiQVJJTm&~X(9B8xXh9$AKMm=<Ps4Dgd%VJ~YjO6MGcShy#bXZ*~VJSx&EnZKWVHFi^p3oSSUWHq>2xkOT=dhPwwoXy^=&_xb3eLHxz&Y2t3el<2os{KsVI%YxCf%n&^0^#R-C<-N3K?`@n@-tVM$}=&TMPO?Ux}duU8&^Q9I7L|cY-)7FG673M5MA#<5G^RT-6n_j;4+<vS*pEk*UwemCqPEuJ+-M5KMG@3S}-d6p$MvKZGwy_6WGyi_U6deH)ySme*RM9IJI~o!^eC)N*b20+^Ai1J-kl(j)sFfjTZz;(XiBHmfLH_~8Pp4qRt$y2(hCY`@<*X%U|OPlbEHw6A=@a&eo|vy;Td6Ukt|7?N3zjd&wTgt;JV(S<)s<Z6Kuv%=XgyPx00dX}CXsR4M$t~CPOatSiCAn`VNXi<qOx(~s=YDobX0$DTtqvu(r2-z5Wz|F|zF)T3dz;c*YEBHBCnz-S9^h<0jo`%UIV)<y#oz9Db06~P|pn1;2jI}D((eR3CUquD-z%`uBbm%H0Xn{V}>a<^L97xys;Z;eb4pJ_FS<1^PBSV$!rq>|)T&w^K(KTYKGKKXXQo7q3Is|qx%#Hodt*6z^Gol3?Q^gQPsHpV87b-hBw<obTtVm`@d96$Ek?s=L2jl14m~c)clz1dyqe_;)P7HnyrH!{gbrbps2V8(ESnbJ2H)%n!b=7Y=RiEXO%sFSn-leZ*M!`d~Bvr3mIk&>C#X(p-T8=}U$O86uk0c?~L9M8o*kuJ0k+xq_3c0TNbb(FrmIx`o8fyC&d3kCgZAxja)($P>J5X(hL3xk<%4$5Akbz?s`cc|Hn(48e#%`B_c@Wlzpj_#kWS=(9I#}laaDH=5bc=!{(M5ES@7OQbqudN(msFd}<Yc0|)2?|q#(Ro14Te#PgfPY`8q@-2oC=C>*0#OgYAkHzb4-t&>k+z|D3JhEz9h)(#mFYHpp78!(4Z>d8v)~U`jwShW<(vUsL{(pz4`}1j83f^bTI@NS%GM~R`!q{5Z$PyBp60D@~`w)7G7>Kkdzy?nm~VpgoI*(Bqz*gI~Wd(LHdT(9Hhr>c_o}&y?2V37X1-cq0cUej!dXX>rlMwex?Bd9`;rQidm{0cniK&)sJ6pQb*6Akc;XS4L4)R6{s+&bo3(GAEJetpjQQb3=^$b^(z-55xP@pch}2Ki3VJB8%Fjq<3C8O#Mr~A>II?cTclYQ-M2RLx*R{L0PL%BRw~J@1)Hp*9K6r>M%|8d@sfc$@LV(mD!MTz4$m+PxOb~MIp;x6=jN$aN&;+EzAQjYH3f^!0R^@k-iLEwJR>9<n@wo0$K+BIiJ|tn!cKYrOrfR4NfmdMwM~u+6652igKQm5<iv3ph;rFLF)QF++d8x}tjrka4SAKHnRha;D*m$6FN}>3mFtoM^k8IzEfaTiMQuT*z-=o;r#HVB*h-UCO|+`YZ?YAN2rOkO6xoGr$EyN2=^rkmp;SMd>q8IInwV@0Eg|bsb-T<lmbXtN4gHY6p9W_aF4$ITYwNfoWi+v37g`%ir#QPv6iYBDmGrc^Pz@TAoh49831C{)o)k%G{R3OcsV{F;3?t=<O6mI!wVx_2p%aAU1j=KCs+r`D6sI<gl{<8rt<;=(Vuo@dl#Yp^K@|N|aVO8@3sA_r!1bw1f@c{ABhIYG;zFF*O<Ts3q9YOO1Qx`?1I3n*u?d3Xd&+F{Seef`7SRo{J@KkCuIMM`m!yZWu&4)6Jp#naNENd9aaJ<Af|x5!jHNdN@d{fsh$(C~jvQ~1zRZ!6H){frqOJzd|MfMmBl4gzZ+61-E6J~B_A;X1l=OlC2|%L20?O)=l|sgkqx{9#wGvA`z@Kq4%))vGMJdwDE}MFIjCDi_s9wF*u#~ou7iXSFWw>a%i!QzbR%Dj_E|Q#}g7t+VgniM<o2%kVu|{|!Otm7MWXbF1Y=|1;>8n(i_p6u0EI)n6co<p9o5nW*@HMj#6@f|nSYusH$th^*3YL)GX7^!zRRf|Dt?etSRlG{NTs98AC{<2hT7z<tu-l-lDKj%^V5OKk=T?$0oGb(YGdrjRQ~N|127OhqUTJu`lB6jDxNeQ~5uK!c4zcxeH`iriQFYOss*eP3X^#t<NWj~UgWxg2j291vPnM~noXtftSSDAk{w7adE^BYBAtFrhAgaVqiAd0;<-z=Q(Is#iGn7!v@tQ8JSx$<3)|MDyR1`F|i0G_pnuVb*%u8JG^fyy?8W|5tHR+qm#+DMRM##ddXwgnW;ptVGsFd2d^h?jatYr^X<>di(&vJqJ$|@?Pi+$lmD}ZKp!Zs>*X9-i4lIyeTh<!xqcf&q1VWtuhDX*mF0Z7NVTQsiPY$eCi6IIk|;87YZ`gnKy?(^IGl5}yMuB4DM<lK@^>*vxj=28Xa7@n1y+M!BV0scdwyup5F6f`K7%Z*z=ga?yi(~cqR)Z-%rs|;22F`FV5R<2+pcWOz@hH~{NkIFBAR9oJe7=1269&!7kmSHg!&gO-Ia8m&)Ho=`zV79LON3DGyt8um^W3VqOT7_<8b-1;YpHXE<L!V7uP6p9wna0U%>0c8#=yHwlB)$z*y<i^mU<?MU6f`u`sGcp4=8*I##+;BCx-6~+3*l&Unk=PhX0nqdxgkhN3OfSz3_Og<b5q?cTS`Vy;8S>ZjVpo#m-)V+(T75fjbv%(b9P}ARd;3Kc>xoOC>vl%jXlM6DrgdyQwLJ#QCb)tCc!9Tm1&^W%gs%*u&gE3C{1W2s(I;Y0$3q{Dl#5;##-mX_i!&pPqJVlCHtm?yV|hP_VO#hMl3%qXCFZrML<N`uLltw=do=u9RvKRN_8n?6<Ite07%AFA#118X|}75w6vM+WH&`qB0)Q$3pbqnQ7j3^vS@??1HfMfrI;>P5HRx9nf6}!nw}HeBjm|S_l{CfUHhX&*@&Dxw3wV!lm;)OmQe(nYA+6<k31AxD@wOQ8x}BUqD~{I1#0$0LczxDkXmxZlI-&G08W*nJT(Q$YVqD)QeA>uDczITsDhsOA1IMER~MnVq&0+V>$~JaOhqXs^2HW$T}IigXfq2R6^LZ`{6AhUWQ_}iI!f_I6xwRJo!1>*@Mgabs>iijN2|DUCm32uTwcQE0ugG@<RqO(UXq5ItgC~X8)+un#@_U$YQJ=q$ye`8;ySPIFr>^RWco?UfNzqj-NQCWG5eb35EL3&R--ePm#%PmVQqIyTS{O~G!@8XD_v337Q;~Cs^EvnHz&uQ@PTSeeM=#wh;Iafl0#zJYr<Qs%yOCKzVjhrqFjjx(>4V-1ohaf$W{u<M*kGf+&))kEY+8<N+Ombunh<b5Hh8WvvPJKO_&0fb+iW)Z_O+8Ugs{c%3}&(>Oia2qA`9%R^Nuf04$`o^E5_P{Is3R6`4M)@RpsA*5;?|Nfe!h({<F)tH)K0yb*G0CGRDRkOI1so!$ivKLdO*s`_H?jHs|BmyQ)+H(X|DcKEz1Tb)->=M3?tT}dpJDa~bPd2-nMiXYsEE;52FN*Pa&tCr`)Mw)PyQI=Jw0xMMjVEJNg)-4yiqM(n*TV2$pu+yhf9Vq5h;;e;S0W<fSf#n9qoX|;NfLdJ^8zm#4?rAZ3EbR)89bc}BO>_Ow%HHSI7-1K^>?_jVBKOaV4%nJSP7+^TbC8aw)bL;o>Lmkpu<%<&@+~1D>&pQL<REi&0ouUc-QWIrbAOB7`pYHqa#7)5O-PYZpfd<AO&=2GI_c44OWzo_(br}u1<C1Qu9ET(>9y=!Z1E0wQ_0(l8rvkJ4U07P$VVs3`-+~~utsYyZ;ge^q#%+83x+k$+o!*iMYSI*pUXU#u4W_^o%4`}lDe~FHG5Wz7+6Ihs1z$_Qm6oyX}Z(}$5iN+l&JCsoqOk{9CqWn7LAX4M9AFZ>7M=36**Nx7e)){FG=TZ=BAMK)Fn?mE^SRzoRY`gZJwq^t^*lzWoL{FP~Eqx#D9XWl>|dc^<|mSO2}L#uvlCTu6TSVf7Ju7GbqldE+l@;ip(vraYWs7Q7OHt=eDq`uXUD4<&xnd2)PSi(>?*_1Rfa$EKAguZWb-9d#>HqTx$rQ_vAxdCg$Ne(*8Xg)mr<*zq6svOk+C5MV`HUeV8ykofOWDctQc;+yBnM0v0mio-+7djsvi{-kt;RzY^JrS;c!N4&XNPWk=OCB8<ct5wK9{Hl0#CwAi#xJm5BUuOPb!|B0L=W0(o5o$6WP=mHR{Fv>r9<-|Zg<#?iGm`)_$$TljPwdKl<+zWG12)MYEiLfthQQ?cVGGRw8a<4wd0%ci6FR+4talZjoJQ$qpR^>h(6{|bb%o-HTX)reVbt}XMHX$Z+?n)>U0`_#(vRcs~N1sZv2wx^zevT}Mx=&R_T+8XHZz<-9O@kCa&;?;7J)rS?j%{r~U7EOj92spe^UScOf6}&DhMr%#x;v=GRBUdHA~G+hqIhUJKPPN=zQ9<*#>Q|vvq>;co7mpi6~ySvzN3-qfm6|G=Rq|l|H`yf&yzCl&au;Lyz`r){PVJv5B~=_##zq')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
