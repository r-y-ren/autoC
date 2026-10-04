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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PASS']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [[], [], [], [], [], [], [], []]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 1], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'SHEEP', 1], ['PASS'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], []]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['WATER'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['HARVEST'], ['CARE'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['PASS'], ['FEED'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'SHEEP', 1], ['WEST'], ['PASS'], ['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['PASS'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PASS'], ['PICKUP', 'WHEAT', 1], ['CARE'], ['PASS'], ['WEST']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['PASS'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['DROP'], ['FEED'], ['DROP']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['EAST'], ['PASS'], ['CARE'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['FEED'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WEST'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['HARVEST'], ['SOUTH'], ['FEED'], ['EAST'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['CARE'], ['FEED'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['PASS'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['PASS'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PASS'], ['HARVEST'], ['NORTH'], ['DROP'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['BUILD_PASTURE'], ['PASS'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['EAST'], ['PLACE', 'SHEEP', 1], ['PASS'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['FEED'], ['WEST'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['FEED'], ['CARE'], ['WATER'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['CARE'], ['WEST'], ['EAST'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['WEST'], ['CARE'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['SOUTH'], ['PASS'], ['PASS'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['FEED'], ['FEED'], ['NORTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['CARE'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'SHEEP', 1], ['SOUTH'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['DROP'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'SHEEP', 1], ['EAST'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'SHEEP', 1], ['PICKUP', 'WHEAT', 2], ['FEED'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['WATER']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['PASS'], ['PASS'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['BUILD_PASTURE'], ['WATER'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['PLACE', 'SHEEP', 1], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['EAST'], 'hands': [['PICKUP', 'SHEEP', 1], ['FEED'], ['EAST'], ['DROP'], ['EAST'], ['PLANT', 'MELON'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 3]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['PLANT', 'MELON'], ['SOUTH'], ['DROP'], ['PLANT', 'MELON'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['EAST'], ['PLANT', 'MELON'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['WATER'], ['BUILD_COOP'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['WEST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1]], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['SOUTH'], ['PASS'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PASS'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 2], ['PASS'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['WATER'], ['EAST'], ['WEST'], ['PASS'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['FEED'], ['FEED'], ['WATER'], ['PLANT', 'MELON'], ['NORTH'], ['EAST'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['EAST'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['BUILD_PASTURE'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'STRAWBERRY'], ['FEED'], ['EAST'], ['WATER'], ['NORTH'], ['CARE'], ['PLACE', 'SHEEP', 1], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['CARE'], ['NORTH'], ['PASS'], ['NORTH'], ['PASS'], ['CARE'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['PASS'], ['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['PASS'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WEST'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['FEED'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['DROP'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['FEED'], ['SOUTH'], ['WATER'], ['FEED']], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['EAST'], ['CARE'], ['DROP'], ['EAST'], ['CARE']], 'market': [['SELL', 'MILK', 6], [], ['BUY_SEED', 'MELON', 3], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['NORTH'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['PICKUP', 'SHEEP', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['PASS'], ['WATER'], ['NORTH'], ['WEST'], ['PASS'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['HARVEST'], ['PASS'], ['PASS'], ['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['PLANT', 'TOMATO'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['BUILD_PASTURE'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['PLACE', 'SHEEP', 1], ['PASS'], ['PASS'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['PASS'], ['PASS'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['CARE'], ['PASS'], ['PASS'], ['PLANT', 'MELON'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['EAST'], ['DROP'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['PASS'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['PASS'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PASS'], ['PLANT', 'MELON'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 5], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['EAST'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['WEST'], ['EAST'], ['PICKUP', 'COW', 1], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'COW', 1], ['CARE'], ['FEED'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['NORTH'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['NORTH'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['NORTH'], ['NORTH'], ['PLACE', 'COW', 1], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['WATER'], ['FEED'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['CARE'], ['NORTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PICKUP', 'COW', 1], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['PLACE', 'GOOSE', 1]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['BUILD_PASTURE'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['PLACE', 'COW', 1], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['DROP'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['PASS'], ['EAST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['CARE'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3], ['SELL', 'WOOL', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['CARE'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['CARE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['EAST'], ['CARE'], ['DROP'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['NORTH'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'SHEEP', 1], ['FEED'], ['DROP'], ['WEST']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['EAST'], ['NORTH'], ['WEST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['BUILD_PASTURE'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'SHEEP', 1], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['CARE'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['EAST'], ['EAST'], ['FEED'], ['SOUTH'], ['WEST'], ['EAST'], ['CARE'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['CARE'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['DROP'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['PASS'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['PASS'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['PASS'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['PASS'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['PASS'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['DROP'], ['PLANT', 'CARROT'], ['SOUTH'], ['PASS'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['DROP'], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 4], ['CARE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['WEST'], ['DROP'], ['FEED'], ['FEED']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['NORTH'], ['CARE'], ['EAST'], ['NORTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['EAST'], ['FEED'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['DROP'], ['WATER'], ['SOUTH'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'WOOL', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['DROP'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WOOL', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 8]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['DROP'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['CARE']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['FEED'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['CARE'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['FEED'], ['HARVEST'], ['WATER'], ['EAST'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['FEED'], ['CARE'], ['PLANT', 'CARROT'], ['HARVEST'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'CARROT'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['CARE'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['DROP'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['DROP'], ['EAST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['DROP'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 20], ['SELL', 'CARROT', 9], ['SELL', 'WHEAT', 9]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'EGG', 8], ['SELL', 'FERTILIZER', 8]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['PLACE', 'WOOL', 4], ['FEED'], ['PICKUP', 'FERTILIZER', 3], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['DROP'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['DROP'], ['CARE'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['EAST'], ['EAST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'CARROT', 3]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['WATER'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['NORTH'], ['DROP'], ['CARE'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['FEED'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['WATER'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 6], ['SELL', 'MELON', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DROP'], ['EAST'], ['WEST'], ['FEED'], ['FEED'], ['EAST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['CARE'], ['CARE'], ['DROP']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['DROP'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['CARE'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['PASS'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'CARROT', 5], ['SELL', 'FERTILIZER', 9]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['EAST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['CARE'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['PLACE', 'MILK', 3], ['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['FEED'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['DROP'], ['WEST'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['DIG'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['DIG'], ['WEST'], ['EAST'], ['EAST'], ['WATER'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['DROP'], ['EAST'], ['PLANT', 'WHEAT'], ['DROP'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'CARROT', 9], ['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['PASS'], ['FERTILIZE'], ['WATER'], ['PASS'], ['EAST'], ['WATER'], ['PASS'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'STRAWBERRY', 3], ['SELL', 'FERTILIZER', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'TOMATO', 6], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 15]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['NORTH'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FEED'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['DIG'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['FEED'], ['DROP'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['DIG'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['DROP'], ['WATER'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'CARROT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WATER'], ['FERTILIZE'], ['EAST'], ['DROP'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'CARROT', 5], ['SELL', 'FERTILIZER', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['CARE'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['DIG'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['DIG'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['DIG'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'CARROT', 9], ['SELL', 'TOMATO', 2]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['FERTILIZE'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['DROP'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['PASS'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['DROP'], ['WATER']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'CARROT', 8], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['FERTILIZE'], ['DROP'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 2]], 'market': [['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['CARE'], ['CARE'], ['WEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DIG'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'CARROT', 8]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['DIG'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['HARVEST'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['CARE'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['PLANT', 'CARROT'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'CARROT', 4]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 5], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['EAST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLACE', 'MILK', 3], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['CARE'], ['EAST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DIG'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['DIG']], 'market': [['SELL', 'WHEAT', 12]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['DIG'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['DROP'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['HARVEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['PASS'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 5], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['PASS'], ['DROP'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['DROP'], ['WEST']], 'market': [['SELL', 'WHEAT', 16], ['SELL', 'CARROT', 3], ['SELL', 'WHEAT', 8]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 3], ['SOUTH'], ['PICKUP', 'FERTILIZER', 2], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 1], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['DIG'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 12], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['DIG'], ['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WATER'], ['DROP'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['EAST'], ['EAST'], ['EAST'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['EAST'], ['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 14], ['SELL', 'WHEAT', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 2], ['SOUTH'], ['PICKUP', 'FERTILIZER', 2], ['NORTH'], ['PASS']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PASS'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['NORTH'], ['EAST'], ['PLACE', 'MILK', 3], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['FEED'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['DIG'], ['DIG'], ['SOUTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['DIG']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['FEED'], ['FERTILIZE'], ['PLACE', 'MILK', 3], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['DIG'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['DROP'], ['WATER'], ['DROP'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 7], ['SELL', 'CARROT', 11]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['DIG'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['DIG'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['CARE'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['HARVEST'], ['CARE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['EAST'], ['FEED'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'CARROT', 5]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['DROP'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 5]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'CARROT', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 3], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['WEST'], ['FERTILIZE'], ['PLACE', 'MILK', 3], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['BUILD_COOP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DIG'], ['WEST'], ['SOUTH'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['PASS'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['SOUTH'], ['FEED'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['FEED'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'EGG', 7]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['DIG'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['HARVEST'], ['BUILD_COOP'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'CARROT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['DROP'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 2], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'CARROT', 12], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['DROP'], ['SOUTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['DROP'], ['NORTH'], ['DROP'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 7], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 15], ['SELL', 'CARROT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['NORTH'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'EGG', 3]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['PLACE', 'MILK', 3], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WATER'], ['DROP'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['DROP'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 9], ['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['DROP'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_PRODUCT', 'WHEAT', 18]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['DROP'], ['EAST'], ['NORTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 24], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['PASS'], ['EAST'], ['DROP'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 14]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['PASS'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 8]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['PASS'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['DROP'], ['EAST'], ['DROP'], ['PASS'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['PASS']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'CARROT', 7], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['PASS'], ['EAST'], ['BUILD_COOP'], ['HARVEST'], ['WEST'], ['PASS']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
