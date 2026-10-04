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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-qxnU5^|`a{Mp*JP$V?`ys#WQF9V;l$PKwJva*sL4eONV4NRhzZw4TCb{#`-5D7XncdXVPg)Ikr@N}Msxl)ZBY*jytAG3L_kaBT_p5*U<?8+Y<Kxxy>gwNr`_F&<uTLL*`tcvX{r(?+|L;#f|8n)?+YkFs|4M)O^T)sa`u@Yi_aEOpU9GMTKkn~8{df2L{J*QwbKbuB>&N$(Usw;G`ODQ||M>Lf%g#R>-z)y%_Idn@pC5n!^V^^9-+lU>HxGxa)#mh8=Z_zM-0$CierEPk=U=G4)bWAjm5yJ%nLhjHhYwFbUX>qs`MU7P$Nm2MPrvcg{@ugRV6fnU@88}3{B-^k{Nz7>eEaVEUqAit)5p&XK78!t0h8YxjqLtu|KZEmo!(+Nws-e$_NTdA=L0)i&U6)zf6o{3G}f1I8NI+?K7W7xxi5c)=JWE5%fQc1dvh=5@#Pon={tT@e*NRj3?4K1@_e$0J>bW#EbE+_Vs%!D5lzQ^{9|{1U*@Siy<ofT@3k#{<I{UNNt+XVnS+_T@AySk^NqXjHK+CQ;p24gRwnbZJoVEW*e5!hEd%(&rZB!&w4QkrC{O2jY=X%e|4_cF*_>1!rl(@g*98mme8-L-1n#)$rTOsg-TuwfuYcKpczXNp?Z1RIKYbPaMdt~}y^0O#`wtKA)2|=T%j5ptXTNap3()|;vo4$SJQRI;9A685&E=<;-;!?`T-a&sF#OJBnzId24<L5QgHKb}-h5z#2RGRsopc$~o3Z8~o=oCwhiLF{O;^hW5B|}?=E47#I1kgs?^{81FTTa`f<Uo1-2W%*n|dfqxaZQ{SjfvDUlUK%#=X4AmozW;&UHVDwBQfwTJ1aq+^E_MU_O+*{l3O<E)P9lAmK7>jt96m(~sl@vwimc=N#Oqcn<N2V2A-!#PQkmqf%UOJOt4x{p0<If8M9py>(&(7x8#rW&u1r&1()X*fOoTiYr1U%Xf?}(~4#VI0xsaHkNlV7a7PmcP_vicRkOdxiBwU4<LETSqlKyHZ?xJ1fvc1`1Ila@aO%94}T+(_~4iD3q)MYH(T!vK7Um8@z>A3gAfm<g0IDAl6WO(l9zUU80fR0OI7n4CkAaSrSECQ6H9p|Jk_RslCxn3kii?+@$-VqE<G;o(9v(D1JS!!zMe!c;i-2q<%>gkUx$0AI1<ct=s{lonjib6%k?tE%hz|HUbzBt;wbEQKI2=C_W7^R8wce=z;4-9a(TXu&>;4(cds)vW9NWwmXnz0>1waDkk4vGDc??n|Ml<cWp3tg9oi^n9;UbIM%=m1F-$Kl0C3FDpTzj={7DhaIOGx9#S+dRnJ~jTaDGlifKE&sS4Yzd{0Te{ax$mQ=xuPto##<~pL$so+fL_+e0>DZ!IkNco@KFs$s9kb-=gt!0oUK<(P!VRbYLO)@%$7&eQ$m7h!J7ZW9TG+pQKkt-gN4CYJNuX+Cnd!++g~MBm)_S&Ec6#4Q2qJh=3Vd<}!~a(BklIng$kcb1;YU`~FZ6<11npvmlF_mt!OxCXUKA@?O?Or^UYm5XyKu@aJb!X2$vFVHkg%dp}h_ibcC19+mhC$zaTXHQzS@U_di%Mk7cau>+@T9vE?%&N|6#K`S{==Zh=W^y5s&{8|$$3b_XMLM=eS1~rIPb`Xd{;)(2~#+}m5A1w=2H;4l`{}V}JR)Qa7%NLD}kqe&8eBnK!^@AV~{dC!3m5YvrT|*aZ__GVhi`2m3;o;MNZU#vKn$U_9LvJqU?LaQWjVm|L{<=*8<P~RO#}hmCUC+$EPY&w$SNfGePzJqzgl1(<um}t$h|LcV50CpuNt~6RJ=?)~Jug(20P+l9KtypPJ6&%QL*1nHao5k4V;*6I7*>oh%j5?=|64Nun^I10I<Z^CUS6TXjg}!TVJ{S?n!q$~9s(&!N2@FiH2K<z%RE4Fj`O*O(`cR!h2RW57G!jWzyG?cc%C`1b`zv&!R3qVg-l%TM`yKI@zePM2>hCuSaYQ+p!#&LM2sC-R|`Yil-WD!@WUH1`2MoYVoj6MC~E68h@C`~qj$MnAAFIIbmwLURdZhBiTX#a?zkxKV)T)rg=fevC8;i8sHz)U8pw-E@On<-bP|d(6!vukMd(P~Ja-Gh09|_OQ{8kKHLa*)k$fG9U`$fUI-O(V`Wd9*5`Y1@tGX24&r^o9^vsGr$`^6~z!*N$U=Jm}96miVLp6v(DwjI=6BDZtm{u-(U+(8LG~JHYOWK;{Qx#^;fAQ3}Xp*c_YCv}{pj36I_%v?PNtCrj4Ju#+OkDKRJqdEu7e}U%{s)sfb&PsB=rq=8zF(ZZ#@9txf~8QFVW<hJTEhmILo_$}_%(ra?}Wu1V@gm%{)TTR>SUC+)(~;-;LMfywdTsrqQJ}Zld{N%PY3rEdySvozWZwn#=Nan=|`vpT9+3n7V?S=%c~elENiB^5BLzZfMsv`gUQ5-X`s7?5>_ZmZ?OD=2Qu}>i;D{C$RoA}fV{$4M8vjC@3{&g=4b8Yn}MN*yiBv80`Nt9i$j%LBHoHVQmYf!U)3;G;U;Mglh9`FrU8>S2~k8Er?Y8P^=NL#9y$?EomkQj?067JzWt#MujNIddjFaTTeB<#<xjz-q(IP$ghhNb*alJPLNbBaFo8Hgj$zgbLmW_?!!R+xMV3Qn=O2W-26!@esxQDay1kJgq2o_NKYzqrCcJE4+X7M#4RdZr1tIHrv1%MJw1l+cDFf1e=!z{x57jx`=)*A59U@==mK$i{<mn;~C(n=}C2NZkUMc~luTCBblIt17ebis8OxfmnJ}M68v}T$`gJ=nOvg;VE{CUpNJ?maKC0$YUAkMdArPXMbwv|}|5~Ege-Yc*2-f&33_6BZ-?^D=d7yzwVL=g`FQqWldgSO^TK=5FI0cGO5y_E-f!i9v_)0ED-;wO0oAH+FDV=#oQqW5=JYtPE^;yjqirlvcPmKxGh&$gk+_Zii+O;p@z-l<LCB2xlDmkBp-I9;Ynh;>R@**uUwMw130H-CjJ4S#aqLQc|jURmyiY58X=*O)XtsghXDtDDG$uq|z&1!aL2iFjv|W>`gqCqOVccsHH*X2F9D!f;T?e_~_o)G*=@^%7f}$*puWc_PSpVWB>>RBEicM0DYxiS2**;Yd0u5uXfiT;L~m_Ed(k3+FuJNY18WJPC0PqFAUL6L9Hun)0Tcr8Jy;`Kka0fD^_rG-wRKnDO9WbU<&)M!Zou+D$SOAoOAfVbmax*i-NvywGj9i?{wjnM7Sol~bFJ7a&A<(SA<E81iNPGR)0<D+hTXSV$Ce2BwJvYmmyH8ACn~CL#7t@^k`vM=^ze-^Og<^t6+!jJt!ax+$MXr5Ju^jMmOCK3q~hJuyL9XkZhqkQW#N<Ols)8YGLio9;5-u42%E-hrk$X{b5Lr&)HC@0z*EmO=4I2zOX(qx`5}(Nd|j-`}PSD6nWAI4kJrj+Y$m3N~J(^`;`Q!KfJEuBDPpsm?On2;FQ=yen8Dj%F6oj*rzT9T`i49Pp_$XS{PTvh+RLby-EP;ESM1E%#nqEmQ8KDn!A6JhBG3-e||Sq3Ih6B@sc&C16*)+a0r+g&TOm33KGIsYb{*0$@q*#;rjVf(0X9{nEANE>@mESaEp`O?6g!ZD?b;24X7a-CObr*;JGXEO)qsNl{g${-4oXZmNo~ZeJIm5Q|l-&=PTkNlghNGnmTTet?q(c3THovMKXurDR%qMxoo<PL^8IATR?2?xvJ^zt%yEV6+UD_vzuM`=<w&gQnI9)N%Eh*()MWa9Z%=>o3Z7h=Yi3J>eRUG%ZmIHq%g8mX{M@u((ImnF-RiL`+0TDx{XiQmV8n0fc|xRAqu9v&{$!#vNxfNv%dA3Uy4mIdN(-qpP$530i-ePw`+2<er5|z%GchbOIwPC&@C}{E{w)-CRU?(E-OS%h-r1c>y2*JQQR>VG?dK>z*QQGnh8<9wUxL{3l?rRBn1v`f%KNl4V<s*jeYSuf#cKf}F?&0>;QNxj3Q}F)d#W%o#+eS#D`)b)s*A&;(9K^ZP1GQ(~?HPY(dBEBf`vUWnC0FLgO+b0nn=6A$K-`yf$X)b+S)a0bJaiK?;GfZX4BDBSQy9HL!GIx=eG5&^fg5t5I=FDIBUH_oI*pi5DUf5vq9L&D=O$yqy!1K$KhSZ(FAo1-wxsAP;b<e@OtxwsB+L<YJsSzwS&E2#s!dd?6-OL;bHMkm^)M2kj)Uj;kioICJvSyQ5J{olc9jf)^7bzxa@o68j2vC0ePiDhCo5q+Vi;+sU`q9Zs58wLJ?8OmX)b6mJHd4px%S;z2!m_JY`=3Y>wi&Nd<e)Y1*Nk!^nm>nc+iT7Z57xCG^m-R~dflj&~Y#OXpv@|M|4xVidF7bux@r$q>A!w%@v~&$^HEa3A$w1*b%h2S;Jj}31MiZvdGk(2P1A1lj_M-mxkr!RarGX3I=Wv2F1qI|d1GWR;Fdih2#sK9!W+vjCShZARUdc@w4cT%|m24U1ZNp@raboKHcE0e-ve?TEMk<3Y>PmU#4^1WHc0OjW_oQtYQpaB(-ZKc{OwJ$O?}|%{&_g;NC<<=Q_2nnqx_9yq6BSx7p7It!-jgVHqC_q|m>1I|HwlhrOZ(xU4DCQM0A&%^?PLReddi0f^NO&Dy|6kh<+vUn&vjthE!RB)U#w|iicA)wH$0PvXZ6sihUIjw9OU(DA$}B&)P*wFDc}y<A<>TCv4SXg2g$!wI(U*o2CbMwq>>1J(rweooH?f9X}w)eJ@4KOQ(IA8B)}mWfkW@bixV4dKnBK+PZ-yRw#lBlqry2dqJlI5M>&#Vord`}8#$1hXUuV6mB5SWUZT5N>}nOAdR@N#EdwN0S>2hEE|N~zcm?3Fg>P7>eo@O3-66B2ByeRg4wUaE$LWg)5!&4hTdJCkpOcUVt+4WJE^`mBmy-}U9REGxc2_+9tPYsApAB{ed`E`K5k3zbI3m`Ka`<=At-N-N(^%W-82d+&{T_rowl1}A=bWUJLYPDKFqAhDVi8hzju?QXQ1FhbnatEytRzWk&6fk|f;}?4_Re<0T8+9bafx#J0Dl-=l+uBqwviV@)8TYoR)C$zg7$q{K<Tp03xq<D9%mNOK5z0(v_wbi!fTx`4w~9D5)I^v$do}~<Ktd9mzMIb3O!~3?&1l5%k5BOc6t9c`OebJXUNYq8Tgga9*BW3Dc4GyI+!isAP;mhHlC8q)}(liSKv<12Mv!w0OsqvMEF7o#=w+dySg)mcA`WzzOTAwly6wXc$J$Ob$mS!31HT=LbBQ314(=V1q*f?i>Rq2luIRDD8!D1V{H{6#VAqBJLOB(NquxrvrH3%SP8bvHOy+e0Ga?y8!`T$;8fbEbd$hiAB~L9GH^sOdUzq01`JsOLEC0a>3%=wqMT)1@@AXPn5U!urx(2ys1fZ%AFDS&pN-ALr;7T~a+6>v7+QRM1vSiWDq-7)lH&f&NW4s-2ZNTh)Ql@)&9APt$+$G^=PFyD`#bUO$+LB`xou_X0d@wE{tDd$0y_n0Wpc5WQXd+PYa_1?rS${iA_u-CLI{_*z0K(dm!TzjCnPnLgV4mDyf%C=L~`{2=+uxF&XwuUv0X{D$3dFW{2Ag$>px9HitpOkadzrtXAp~7Nr`yGG4*yCafdgv31W;_>-2@=^88b<<GYHc@oPX&T5N1xjTK2RI7~DM=@0lXJ9Qb10=*93s-nae-b@{uqk}8`7L^)6Nt+bG`|3m@*;H6cl$V$jCdWBC{IrdZM6&a0*XtG=8@d^I;ptXe;sTDBqk&wKHr`rjklfk47-rIhqrlDcAQsWVMkXTx20~A(BZ;5_lPRc_x+Z1)*qrv+$d|%|`*0%Tq0)(j=)q7eOzw&2z<diOtDrP5oSK9%)@~t4bwDf<Xo1y7;W)qM8bsE9CyZnhv!$S=?tY|7dEH<g7>jr*+Jh`9Z8RxM<llUe33wwG2_UrX&}{4z<S4TD<3-<tYN9;mk{z!-u9d0V&OV}<J;PSi4FD`%ATqg$;6F6ey9*$daki5~oZ}g$zPo=6E!=&f)BlUMg(a;7XsSd)Ix&jLxVGKBthO-57bH^=kkVOmjt*y@%Ly>Cb!KC8H78jQ4jdoiv5$7xxGP4kW-wL&W5c{L*<H!b8~=$@Rz104>p2k_T?6v;r7;2`4NpmBnef;QqMz3ppj?tjf6a0k_ODMLW6dQAc`E~@a0fskTkFu~2mG(&N2j9LEo&lH9ef4BD3u`55ACjmO(v6qEY1<88k>wG`h6XJ`F*Q@XYRm3V+2kYQzrvra8;^=BYU9un>p{2Lv9%FgqxUf5VHDdoLGg+gy{iHAGuSn={9?4QKL9xA_5^qf5q55@VggD8`GEsP)UPhC3^ER<!+)Z;#d)m`BLmo*;*DO=KZ~MS`Ky5kWdzmE5JsOR*`*IS_N6+qoLge@W1XolB-<##W#u8FJU)YftVsU39u|KV7=`_TeA!C8Q>t3l#<u{0oeXc<npg!H`pZ$lv&vzWZ+VG!BVfRuO;JCm~z=(uPvjDtl^p!u9Je!R=JlVaLBCw9%HSSN{S=7YE({{M~^g4;tF%ak$~Ez?E>^3(khLn%s`3+x!I2BT)%SIxFadCFfWD9wJmFiHkdhVI+lc~0Vr4fEMMopoJ<y%rUOe4-L4nHms<`!J?vA5%&#tvdd(3Tf{i@g!zvQ^?re>3mZ<{C=5Fn!)B6*S?QS}>onpdmUl~QKYU;1+5DJDZyx-kYG;f{$iKfy3zi!6_j`%d9L`w+ID7DQ#m^3aVXCTXa#p-_6?cImm7{9>$KChLd2%x|<t21B`_Q<%^I4GZ9VvDdm3W`^>rqF8p=jXtVEHxA!3EPVsh+n{L2bn`)1&O89ByUqF(v>K|yC*D!xsv&OT9Ju3LTW<EmU7VMHodgbXUZ#3@GR+NUfdt+h&Y?7F+5?w*&nK&jguDGAvUWimzFv~sn-FR0Iox;G7j(w@`$}`ut48O#$%!<2|<Dg=9B0a$uo_es*>KrPGUmOC=|PaoFSugWp_Ilqo*gb3`8T;*=dl#`{+?4R+3e)HMj~mqX*8kR(Z;VF?w)fIn9+VCNSpRH0+201Y9b`N{e3#TOuAgv|^JxExbn8rQ$XTUUc8F8az(%-!n9_z|2B3Cv#d9151ymJcfJ0iFW;ZdDWzcnRubuQ%Ta88GQ;N4G^=jzN*(6n8t*R9VRe;X0W6WsCQpifiMW+QHofEz`PD3CkvESB;N*QtO7%szq?LSKAe+A%glwa(pluqA9v(U#bz|YKcJO<;CS@O5x||pz+>K|!=Rv4=qhzlmR&7cqvQi$@VqkqBGKzb6{My0nO$v2zlVqdv8flmE=t-Yjd`aYm7NOmn9s4H0?S$Qnj%(PQnH1-PR>kxODCc>cXoF|*pEGn!&PBHrfw$0f@8j+NVlT7YOkkVM6qjmU=}I)+eb|>WV=iQn_3jUCoN_bi7g4?3CJc7FPGl{>)0#O<}TQwy?dtwH$(n2qc0<aE{a3B5twBGf36dxXpgJ1FczkC?lbh065JA$wrzTLyG^RG4T){DX=(v8E(E~^mJMz2Xa}}n!`!$~Iuo)*kv(MOC6FmP3scNvcKL?^yz0`}0&vxo_CgIU+`=@<KjZyd@?3nWYQvW5QioBAk?AS(ZQ7AL@EoirDh%m~jr;8VeCKkV9CZW)(<ny^B0mBJI{!dQXe4E(1plN!#_Q^TO+VaKVIclt-dJ#m3>ku9mjg;I)x6e>cTK6VO(JxV&jb~|cRD@hQ+LDva19P8JR7@KIk#k@P_=m4Kfa>6Rs)wAxaZTrz-1nZQ}y;EB@o3f$4g~Oa)K9wvYIXiA^66}0%0=Ht<7%W2GAS6#LG$m31vmr(^63=i{z#WSiVRX0H$;VGvtC_LHTBm#%gr{HOZsG`+Ic&6-%7A&su3u(LRHvrwxUc=HYEqj8A&toSH)U8-m=^s^>{gV%(>lls5D5{p%YW&ECdi-4hYA#Pf<xaTSh@8<`f{AZ8D*^j7ovoLy^V>>5uYkRAhsIh6`|&1ToAgjF`%beQSY>66i1L|h@nILyt?*P;#?1p}?3sAGZ9sw;9pSf6^wh`M}wF;ktW#mKQmc|Hqbo1{o8l1Fh%VO@CmfL_mUPRv8<R5R)VIOaH6@>2Lfq0R-$2iG-45SRhCx=B+1Em?UPu6j5hlyi&CCdFSm@?dfSHc1C)r+|~uhhKvb#sV{lC<(v`rAd6aZzo7ovCTpk$m>O@vvC5=5raIrQ0Au{ATS<5B$vURTgS=B7xTN4DR|7j*R8<7RQWfhwu}%@vMN{~OVx5lGvqw}J(b>IYIZbER_+%SdNZM|uB?N<UwG^E45U_sDt(I*$p<Uw6@(<#SP9oMm(;99_e~lxmbHR(CXmTlh7v}~T&p!D6N?}iC1=#i+|5m-X8&k(-C_zx#yR8_^jS9{OZ-Fj7b{v)v;ZElbXNhm^B{w-DG7Xr(``YzD*M7lh}p9-OH@#ZkV`%|w#H~!1$C}kf4W+^Rg!-L+mEt27(LmqO)`XE3@Ha9u>j*cx;^2a#tfiYPU4lC+j4CgN5YDvFB|T7phE!}xk|>t5?Jj8+eihF<nck21bDtUt9<Akp)r2~{p=_nPu`yabSYW6yle`}iYXLwpL#tHOJINPpkuB=M0luLXDPy&{yoX?+$8u;&gC9k<w@{-U64&;O&Jnlexn)6=}1X#my?|wU)TY|d<`W_dd%%q5w*%HW;m_gcn$20_bkuBpT4&Ln$zjPhDxwIXci}4_BN?`;Iq-XZ&g8_EhUzq5OgsN3Sv72p<X;vo;W(ECXz;q-9od1lK(EfhcOWnXUv<;z6b;h%4}IXEQOueLP?hzhgF-Pq~#UBpja1L8B0~@_#E(|_+MRzBgYRAi)#tnFGxYK2(6&#MMN|7-0Qt{5DL6H&+e*Ag)PuNf0!BY-dF%!Gyxqw*V7^joU{P&K6(Qr`dV!edh2j4Al||v2BuEK)!Al?k9h=cBQ?Uo2D!6Y*JHLgFN!WVEV#&uOh*?-tF8!@DG)U)kDSNJ6%8oE!3dL+ijxRQPmux<mf(R)pucbu_g3pp(on^a_p0=MW{?Z-s)*Ad`#LGSl*hTy(ZpU#qj}#3v4<NM;1q|;)B<;OWLZ>;j@;qpnwERu-Pd|uXLF3s<#|&k7sY&QRE@-H&?yRlG37`nG;$*G{(^#`duB$zis5S%Nvk!MAz?;J&1<=Og&JrEaaDn^`1|rrzfH`mCZ%6d*f$HQ@`6n#hxF6_-NVnYNz!&6`_5!rQ3g!Jx!^=a-`=eNbzq1^7T71-@Z^5v^d-w*t*?w-Lxek{zySL8L=D|+BqHm-w@HpUhIJ@6%gM$Er#Va(@=*ITePsYDNsX|OLIDvvs*mh>_&#78XEnYcsjgv#di8vAE;f~ySWWFoyd$^_PXnfVs;rQly7}M`h3QOYZUDCt#6S=dl(XgQ8>_H22X53keDDcKIk(VI4C|xce%5$W$aS=_5!)m`2|Sq>+vH@%-`1PsqHe&*&LkANEvtOb9ClK)JD-$=_yk#DZ|MpWAe)ipXR_F*cchGZenueRP1LHjO%FBeW%eYHShUY_gnofWDxy7&t|ZJi2st0T*Eclo=aFe$1|tJ_<n3$0Q0wgs6dRQLTABmIFQUgt5!f$ONN`k)!c-Cs^?SrxLeA`N!FyZK+eJ(HIgB~#AQaMv%uWLRK3+Cn`sX4cPqfn*-7MQCi82sG0|CN_&?f=+vdj^(S7L<6XL8L54UiQmW)(tNh9Z4qa{rt*&$&+!GRkW@y?@D7;>?f+fzsP~6|fauPopM;E1Pj>jzE_rtF`6DubahDyF(q-LbH+x<)#2F@umu4F1(c@)Ygnks2Kc$1c!($G@(?Vd_=q_QxlKau)}_+2v4K9H|m-)?J&gwiRGy#@U%5EV~`)|w*-!4mbx%j-ZHb8A`^0HhKgpA!^_gmG*MF1JJ0j~;l5>g8p<S1^@MV80L0qW#+-Mdt<+6g=xS_3T2c*|%Lkb$D0FKRWtZt;Q!LnzXeq-_nXL-tf&|9=Vi1d7Ac*NnXgibysH6c2H>yzJo(esx6M!{?DG-f2k}<b4@WfWF1a(Awh8)M|cuiH4LnZb(W%ROS3?f;HixBL#UP&`Z`DI~;RW1n$nK=+~ko_o@AYl3pS-@SW3qNd;fN8SLya^BvlkMuPHC=i)Qi(3rpT(rGaWWg}+qbBEtU7H9&B}`%wx|Ycw;)BWjZPS-bVt1Y%bU?>6i9rQ=68$$81%WRb((KMK-cCuoP=5|rDj=g0%hd5DHCyG5_N@o6UrlucLcyoV>xy#?o~9>&7YEE^BOGUuEM>bVEXMVa2x&DyaxVl(hrprSgGfI2>>(Mmg7e!KW@966rarzRUEz&9vKOIDKfiGr$6OQnLw=7Km&Mx@!xV7-d8I;G#gqmQG>k`pT#~B2VM?5`u38BZJap{*XQyPYAnS`ti*WCG$^9!mp1uOyW)!g(2+Ii;3P7bCLT3(Hn_3v9)Jv{awtogEVFVsg1n1P;TPYY(M#P(qmX|f_s_217BkT}p`A7uc|L8yS2_z(x9cK4$m2Rw=&N*0RvN?l!U(bjLX+f$2sRb<L7v5}5Fu%>*r>|e6asIo%V5MV)y}!p^f*4<g8_YQG7m)HR?Ib#TAV}8(}Z4-=uWAnAnoQKCM}t6G>XqleKc?9r4TNG_(V_UV@bV-6Yv~_VgwY3XS&_6_5mb9D^6+T8B1<|p*g&9+_9eP>RgUTf=PaL(AHX?crwYn3A8qYEQhL5w2^LC0K>m*i<`_>b}MI`E@OU&4Y2#oTS@5M%x+iVkq+rUQuMi^u=tgkhXrKE)s?aEE(1&p(s}-`Z}=Cn!o?9JhBCbKX7#pI^Js}nfl!Cg@FWj(SL^z5%~{YDSrNa<tba*c5=E*Av_2*(4pme1M<QMV7e!BR@w}8kV^oWxu`TRrAECtQh-(64gye&IBL+7ed*@opBX`C+a(eN-jE*VgUWsn9xj+|$$fp_v>a*v!=!A|U0C??k`$!^K$a6ZoI!T_I!F9C90n2!by8fo@rUAsra%0hz6`O+7?9pdViuLu+7R_AcB!PO-8ZW$_VXc&2XzO7TL!`y<s;l5vs?p}>mX-FvFU-W-**rvt#i*=b5rwqljNF;FPNF@g!0cD(muXO@1pgEqs<bbrd{Y*t3km9j6$`3ksY6}&%g>Xej7!X0y=iqXz}wn()IFe*oEtYV1;*;wz?I`uX|P&K@!(eDQhQ9UQgF<Qc*tvz3vYir=PCt%Qf;`o$uug74E$7#u@;(BPb0z7TBtVk2^la3N{Ya`p9!0r;xX$r#W{=qT#^^ivWrOz4{5e68zMDtIw5=&!8}J|Qne}a5^3$CT-onJW8|!^=a#qdwb_T;Z?AptJmJK({o$={Rl6?z3dLwPdM<3<5hy&%-%UYo7Mg0SR<?<QRv+guILZ4XEG&DJ7tU~5Y0;<pPyv0~DKABNEImAPd7?j45ucCLHlsOET0n}9XL5C3B8F9=JIQJ>Vg%^v>T30C<!N}*wPkXs*Xn3oQ_POF4A)sfOCbpwPo6)b-GSS)*ehL;%}Z5^6*{j6Q54R#<hOt)Uyza8^qa^@)lCqD0|GP=cpxkZn9wMhCaqX8@I%RwFsRUVO<i?cagl0DC#U>WUiaFRGGGn`Lw6E2DPDBT7DlN=<?S0X)ey85`zQ-x6^S;tHeFA2cbX2u(Rc+3Ah>@ao@eX5$&;X+P2efU7Ia62G~k(1&0*5aqTBkywG#^Ue7Ubc>xLWF4rR1&z77eDiY-akmLDxdmtCW>x6g~@GwocRN(tqaMlu^PS<UO2t7$5(Ga*>nO^M~E=eJz!c8`WfqF*O&Nse;2R&zRq@JQmgu9vq7vln01^qvbDShR3?W=HXQkHsk=TgDH~K~=VquhV|i`W|`>oU-Z~?{MUwY$ThQxS`ZNC8#(#ICmyrbEBIisG!*ai_{tF5*jNN;-_=ry6170`^lCIEbXFI=&zZ@b*zI%iMuenw3d~%%NMF~N?BUZ#t{Q%$Qy}Of>l^X;r6(p9ZQ)@LzU)+&s+dbKwF#TF-D#;!aYGK2wK(Ffs%Ep=LjQg@~B|{NSO`2GXUBVX%DW-)GO!}xsYyo4O<qfRYGj!t0M2+6!B6=bV;jezeERUF6>H$CJY|Mrogabq+K%-cHPlh?jN(%i5Mg;zrxe&K<kbITfi$8xJ9z?OVPY&O2ufCQXz<yNVqj23Pv-{xF({8R8=4s2#VAYHPA{ga<-U@0GO&$spnLB9eCh!n~lg%r`x7aEG79RkrY5HZY}Z>fRD!UlGgG_7o2D1Lbr@X3M*uYNYzzcwyS<)gbuM=7hom&T+Z_vHG<%U3f4b$iOl?EY{i`mLSwa=BPH%MxVt1Kxq(7&j@ulOvnUieaxnQCUwDBN7qiwsXQvLQS1XnFTJ>;{=Gv&&<*ks-Ho-nJwEZs2I2dzsT~>agI;MGSoVI84aKt*V%~m+{QzXz|kN_KlKuZRhQLPlRc>t{Y<c^<#iz#=V#Pfw(-dd4yM1j$=G~4jdW*1-%oW@qT*)8LBvqlIYE;4~cdThp>m8z=iw(q9Qnh0eJ&Hvazgo9_#vV~=a>|cS`D5dp;LL4Qkm5xxi8%Rn2jkoYvgt~0XE16_44fAj=a^8|83-Ys{88573mfMmbrz`@O5wu0hs0C)`fg;*u`jT3uipZuESg}D~2i&FnKqWxttEcETL5c%^@^B6Qzu*3@nBb@vD8h71W(#ifEXK#Pr@vZjm*grdiW2-5DbB3jQ$nAWQvbDK)FaRX(1O;X8`vEL4|G+B#iK#2Z*?uT>I8QwduAoMw5&jqBOAp@AnMhlb-O8GH?NI<m`!Sd#k1p(QRq2#KS`{tvsSWsuLI|X)nKIn`;BpN5>t9FDKE7ae#-O&eShorEBOt!v<7pi4WA|qt9B(^{`|c8BLPFvTtVnaUu#x<-==K$Oq2kxjx6XZ&HBCyxVbN{?4*eja97>#X-L!Y2XZJa(ceKSKe(M8h#GrI5+G6u<`S4)9eiHW<uR(p)lB_#<@^dH`OQYdF2~$`*-C6TQtKzzVX3J(^L6%$H&htwPwuX1;P|=l0;*Vu9fft8sM>vddG-QlBIyX+SY5IXnL4=fP6x+tWL|IyK&J%^T(+$ETAfqdPOHK77Al&1HxpOsJ8d;oAZ-MxviV`3vv|RYNzvGC+Uisf0O_rq2EdVS`UeN+{j;{LS-s=kvtJYh-VO{Ec=z4G9Jj(YBSUUz_xAI)xur5m$oD^S1Z?j5afE2r;w;2}D*cWLl-!}I*cQkzU_!2Uh+*>le~IicsQ')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
