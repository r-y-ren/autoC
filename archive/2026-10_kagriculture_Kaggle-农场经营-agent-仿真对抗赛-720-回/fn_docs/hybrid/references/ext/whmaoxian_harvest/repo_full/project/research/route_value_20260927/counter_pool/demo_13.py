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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 3]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['NORTH'], ['PLACE', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['BUILD_PASTURE'], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PLACE', 'SHEEP', 1], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['BUILD_PASTURE'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 1], ['NORTH'], ['PLACE', 'COW', 1], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'MELON'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 5]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'MELON'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], [], [], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['WEST'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'MELON', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['EAST'], ['EAST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 2], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WEST'], ['PLANT', 'MELON'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 1], ['PASS'], ['WEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['NORTH'], ['SOUTH'], ['PASS'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['EAST'], ['EAST'], ['PASS'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['SOUTH'], ['WEST'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PASS'], ['CARE'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 2], ['WEST'], ['PASS'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['HARVEST'], ['WATER'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['PICKUP', 'COW', 1], ['SOUTH'], ['HARVEST'], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], []]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS']], 'market': [[]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['PASS'], ['SOUTH'], ['EAST'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['BUILD_PASTURE'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['SOUTH'], ['PASS'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['PASS'], ['NORTH'], ['WATER'], ['PASS']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['CARE'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'COW', 1], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['PASS'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['SOUTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['PASS'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['SOUTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['PLACE', 'FERTILIZER', 2], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PASS'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 7]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['FEED'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['DROP']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['EAST'], 'hands': [['BUILD_COOP'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'GOOSE', 1], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PICKUP', 'GOOSE', 1], ['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['BUILD_COOP']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLANT', 'STRAWBERRY'], ['PLACE', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['EAST'], ['PLACE', 'GOOSE', 1]], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['BUILD_COOP'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['PLANT', 'MELON'], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['NORTH'], ['PLACE', 'GOOSE', 1]], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_COOP'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLACE', 'GOOSE', 1], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'GOOSE', 1], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['PASS'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['BUILD_COOP'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PASS'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PICKUP', 'WHEAT', 1], ['CARE'], ['EAST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 2], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['PASS'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FEED'], ['CARE'], ['EAST'], ['FEED'], ['PLACE', 'FERTILIZER', 2], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['WATER'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['WEST'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['PASS'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['NORTH'], ['BUILD_COOP'], ['SOUTH'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PASS'], ['FEED'], ['PLACE', 'GOOSE', 1], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['CARE'], ['CARE'], ['DROP'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'MILK', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 1], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PASS'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], [], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_PRODUCT', 'WHEAT', 3], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['CARE'], 'hands': [['BUILD_COOP'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'GOOSE', 1], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['CARE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLACE', 'FERTILIZER', 1], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['CARE'], ['CARE'], ['CARE'], ['CARE'], ['EAST'], ['SOUTH'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['EAST'], ['CARE'], ['NORTH'], ['EAST'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['FEED'], ['CARE'], ['WEST'], ['CARE'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['DROP'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 2], ['NORTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['DIG'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['CARE'], ['PICKUP', 'GOOSE', 1], ['WEST'], ['FEED'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['SOUTH'], ['WEST'], ['FEED'], ['CARE'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['BUILD_COOP'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['BUILD_COOP'], ['SOUTH'], ['FEED'], ['PLACE', 'GOOSE', 1], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PLACE', 'GOOSE', 1], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['FEED'], ['SOUTH'], ['BUILD_COOP'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['DROP'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 12], []]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLACE', 'MILK', 3], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['DROP'], ['NORTH'], ['SOUTH'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['WEST'], ['WATER'], ['EAST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['FERTILIZE'], ['WEST'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['DROP'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['CARE'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['NORTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['FEED'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['FEED'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['WATER'], ['CARE'], ['SOUTH'], ['CARE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 5]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MILK', 5], ['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['CARE'], ['FEED'], ['SOUTH'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['CARE'], ['CARE'], ['SOUTH'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 12]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['FEED'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 12]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'TOMATO'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'TOMATO'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['DROP'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'TOMATO']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['HARVEST'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PLANT', 'TOMATO'], ['PLANT', 'TOMATO'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FERTILIZE'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED']], 'market': [['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'TOMATO'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'TOMATO'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED'], ['HARVEST']], 'market': [['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['WEST'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PLANT', 'TOMATO'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 10]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 5], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['FEED'], ['CARE'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'STRAWBERRY', 5]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'TOMATO'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FEED'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PLANT', 'TOMATO'], ['WATER'], ['FERTILIZE'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 10]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['PLANT', 'TOMATO'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['CARE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'TOMATO'], ['WEST'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['PLANT', 'TOMATO'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['DROP'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['EAST'], ['FEED'], ['SOUTH'], ['EAST'], ['WATER'], ['DROP'], ['DROP'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['CARE'], ['HARVEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['EAST'], ['EAST'], ['DROP'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 2], ['SELL', 'WHEAT', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['CARE'], ['NORTH'], ['WATER'], ['EAST'], ['DIG'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 6]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['DROP'], ['WEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['CARE'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['DIG'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['DIG'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 10]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['DROP'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['DIG'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['CARE'], ['EAST'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['DIG'], ['NORTH'], ['DROP']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['DIG'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 16], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'EGG', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['CARE'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['WATER'], ['FEED'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 16], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['DROP'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 6]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['DIG'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['WATER'], ['DIG'], ['HARVEST'], ['WATER'], ['DIG'], ['DIG'], ['DIG'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['DIG'], ['EAST'], ['WEST'], ['HARVEST'], ['DIG'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['DIG'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['DROP'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['DIG'], ['HARVEST'], ['WATER'], ['HARVEST'], ['DIG'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['DROP'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['DIG']], 'market': [['SELL', 'TOMATO', 6], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'TOMATO', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['FEED'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['CARE'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['DROP'], ['DROP'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'TOMATO', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['DROP'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['DIG'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['DIG'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['DIG'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 9]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 6], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['DIG'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['DIG'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['DIG'], 'hands': [['EAST'], ['PLANT', 'CARROT'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['DIG'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['DIG'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 6], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['SOUTH'], ['WATER'], ['DIG'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['FEED'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['DIG'], ['PLANT', 'CARROT'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['DROP'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['DIG'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['EAST']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'TOMATO', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['DIG'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['DIG'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'CARROT'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['DIG'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WEST'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['DIG'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['CARE'], ['HARVEST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['DROP'], ['DIG'], ['DROP']], 'market': [['SELL', 'TOMATO', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['DIG'], ['WEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'EGG', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['DIG'], ['HARVEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'TOMATO', 4]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['DIG'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'TOMATO', 8]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['DIG'], ['PLANT', 'WHEAT'], ['EAST'], ['DROP'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['FEED'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['DROP'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'EGG', 9], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 4], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'TOMATO', 8], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['DROP'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['DROP'], ['EAST'], ['NORTH'], ['DROP'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['DROP'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'CARROT', 9]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['DROP'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'CARROT', 6], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['DROP'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'CARROT', 1], ['SELL', 'EGG', 10]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['DROP'], ['DROP'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'CARROT', 9], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['DROP'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WEST'], ['DROP'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
