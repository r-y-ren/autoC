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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['DROP'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WEST'], ['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['FEED'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WEST'], ['PASS'], ['CARE'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['PASS'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['DROP'], ['WEST'], ['PASS'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PICKUP', 'WHEAT', 2], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PASS'], ['WEST'], ['NORTH'], ['PICKUP', 'COW', 1], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['FEED']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PASS'], ['FEED'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['PASS'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['BUILD_PASTURE'], ['FEED']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PLACE', 'COW', 1], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['EAST'], ['FEED'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['DROP'], ['EAST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLACE', 'COW', 1], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'COW', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [[], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['BUILD_COOP'], ['DROP'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['FEED'], ['WATER'], ['EAST'], ['PLACE', 'GOOSE', 1], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], []]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [[], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['WEST'], ['SOUTH'], ['CARE'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['DROP'], ['NORTH'], ['WATER'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['DROP'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['CARE'], ['PASS'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [[], []]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], []]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['BUILD_COOP'], ['DROP'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['PLACE', 'GOOSE', 1], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['PLACE', 'GOOSE', 1], ['EAST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['PLACE', 'GOOSE', 1], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['DROP'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PASS'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 4]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PASS'], ['WEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['FEED'], ['PICKUP', 'COW', 1], ['CARE'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['DROP'], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'COW', 1], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['DROP'], ['WATER'], ['WEST'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['FEED'], ['BUILD_COOP'], ['NORTH'], ['PICKUP', 'COW', 1], ['FEED'], ['PICKUP', 'COW', 1], ['EAST'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['CARE'], ['PLACE', 'GOOSE', 1], ['DROP'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['SOUTH'], ['SOUTH'], ['FEED'], ['WEST'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['FEED'], ['SOUTH'], ['HARVEST'], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['FEED'], ['FEED'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['PASS'], ['CARE'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['WATER'], ['WEST'], ['CARE'], ['DROP'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['EAST']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['FEED'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['CARE'], ['EAST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['CARE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['DROP'], ['CARE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['PASS']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WATER'], ['PASS'], ['PASS'], ['WEST'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['HARVEST'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 6], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['FEED'], ['DROP'], ['NORTH'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['CARE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['DROP'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['CARE']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['DROP'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'WOOL', 2], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['CARE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WATER']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['DROP'], ['PASS'], ['CARE'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['DROP'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['WEST'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['DROP'], ['SOUTH'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['SOUTH'], ['DROP'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['DROP'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['FERTILIZE'], ['FEED'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['DROP'], ['WEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['PASS']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FEED'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED'], ['DROP'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['DROP'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['DROP'], ['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 8], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['DIG'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['CARE'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['FEED'], ['HARVEST'], ['EAST'], ['FEED'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 10], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['PASS']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['DIG'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['DIG'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['DIG'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['PASS'], ['PASS'], ['EAST'], ['EAST'], ['NORTH'], ['PASS'], ['SOUTH'], ['WATER'], ['CARE'], ['PASS']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 10], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WEST'], ['FEED'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['DROP'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['DROP'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['DROP'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['DROP'], ['WATER'], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['DIG'], ['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['DROP'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['WEST'], ['FEED'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['WATER'], ['DIG'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['DIG'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['PASS'], ['WATER'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['DIG'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['DIG'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FEED'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['DIG'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['DIG'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['DIG'], ['SOUTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['DIG'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['DIG'], ['DIG'], ['DIG'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['HARVEST'], ['SOUTH'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['CARE'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 6]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['DIG'], ['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'EGG', 8], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'MILK', 6], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['DIG'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['NORTH'], ['DROP'], ['PLANT', 'CARROT'], ['DROP'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['PASS'], ['HARVEST'], ['PASS'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['PASS'], ['DROP'], ['PASS']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'CARROT', 12], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['DROP']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['DROP'], ['PLANT', 'CARROT'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['FEED'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['DROP'], ['CARE'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WATER'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['DIG'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['CARE'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['CARE']], 'market': [['SELL', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['FEED'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WATER'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['DROP'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['CARE'], ['FEED'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['PASS'], ['CARE'], ['DROP']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['FEED'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['CARE'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['DROP']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['DROP'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['FERTILIZE'], ['DROP'], ['WATER'], ['HARVEST'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['PASS']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'MILK', 3], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['PASS'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['FEED'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['HARVEST'], ['FEED'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['DROP'], ['FEED'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['EAST'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['DROP'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['DROP'], ['DROP'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DROP'], ['EAST'], ['DROP'], ['DROP'], ['WEST'], ['EAST'], ['CARE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'CARROT', 6], ['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['EAST'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['DROP']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['DROP'], ['SOUTH'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'CARROT', 7], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['EAST'], ['DROP'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 10]]}, {'farmer': ['DROP'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['SOUTH'], ['SOUTH'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 37], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['DROP'], ['DROP'], ['EAST'], ['EAST'], ['SOUTH'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['EAST'], ['DROP'], ['PASS'], ['EAST'], ['WEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['DROP'], ['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PASS'], ['PASS'], ['NORTH'], ['DROP'], ['PASS']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'WHEAT', 23], ['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
