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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 3]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['NORTH'], ['PLACE', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['BUILD_PASTURE'], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PLACE', 'SHEEP', 1], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['BUILD_PASTURE'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 1], ['NORTH'], ['PLACE', 'COW', 1], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'MELON'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 5]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'MELON'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], [], [], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['PLACE', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['PLACE', 'FERTILIZER', 1], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['EAST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 1], ['PASS'], ['WEST'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['NORTH'], ['SOUTH'], ['PASS'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['EAST'], ['EAST'], ['PASS'], ['EAST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['SOUTH'], ['WEST'], ['PASS'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['CARE'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['PASS'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'COW', 1], ['HARVEST'], ['WATER'], ['PLACE', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['PASS']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['FEED'], ['BUILD_PASTURE'], ['FEED'], ['PASS'], ['PASS']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['PLACE', 'COW', 1], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['SOUTH'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 2], ['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['HARVEST'], ['PASS'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'COW', 1], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['PASS'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['PASS'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PICKUP', 'WHEAT', 3], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['EAST'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['PICKUP', 'COW', 1], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['PASS'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WEST'], ['PASS'], ['PASS'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['PASS'], ['PASS'], ['HARVEST'], ['PLACE', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['BUILD_PASTURE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['PLACE', 'COW', 1], ['PASS'], ['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['CARE'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['FEED'], ['PICKUP', 'COW', 1], ['EAST'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['DROP'], ['WEST'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['NORTH'], ['PICKUP', 'COW', 1], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'COW', 1], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['FEED'], ['SOUTH'], ['BUILD_PASTURE'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'COW', 1], ['WATER'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], []]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['PLACE', 'FERTILIZER', 2]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['BUILD_COOP'], ['WATER'], ['PASS'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['PLACE', 'GOOSE', 1], ['WEST'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['EAST'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['EAST'], ['NORTH'], ['DROP'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['PICKUP', 'WHEAT', 3], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['BUILD_COOP'], ['WEST'], ['WEST'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['FEED'], ['WATER'], ['PASS'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['NORTH'], ['NORTH'], ['PASS'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['PASS'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PASS'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['PASS'], ['WEST'], ['PLACE', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['PASS'], ['NORTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['DROP'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'MILK', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['WEST'], ['DROP'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 2], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'GOOSE', 1], ['FEED'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLACE', 'GOOSE', 1], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['SOUTH'], ['NORTH'], ['BUILD_COOP'], ['FEED'], ['WATER'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['PLACE', 'GOOSE', 1], ['CARE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['EAST'], ['FEED'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['WATER'], ['BUILD_COOP'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['EAST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['EAST'], ['DIG'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['CARE'], ['DROP'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['SOUTH'], ['WEST'], ['PLACE', 'FERTILIZER', 2], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['BUILD_COOP'], ['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['PLACE', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['DIG'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['PLACE', 'MILK', 3], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['WEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['CARE'], ['FEED'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['HARVEST'], ['FEED'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['EAST'], ['FEED'], ['CARE'], ['DROP'], ['SOUTH'], ['SOUTH'], ['CARE'], ['FEED'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST'], ['EAST'], ['WEST'], ['DROP'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 7], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['WEST'], ['EAST'], ['CARE'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['FEED'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WATER'], ['WEST']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FEED'], ['CARE'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['DROP'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['WEST'], ['CARE'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['FEED'], ['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FERTILIZE'], ['WEST'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WATER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['FEED'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['DROP'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['CARE'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PLACE', 'MILK', 6], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'MILK', 6], ['HARVEST'], ['WEST'], ['HARVEST'], ['FEED'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['NORTH'], ['WEST'], ['PLACE', 'MILK', 6], ['PLANT', 'WHEAT'], ['CARE'], ['CARE']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['FEED'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['FEED'], ['CARE'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['BUILD_PASTURE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['PLACE', 'SHEEP', 1], ['BUILD_PASTURE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['PLACE', 'SHEEP', 1], ['FEED'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['CARE'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['CARE'], ['CARE'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 1]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'STRAWBERRY', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['PLACE', 'MILK', 3], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['DROP'], ['DROP'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 9]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 10], ['SELL', 'EGG', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 9]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['FEED'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['DROP'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['FEED'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['DROP'], ['CARE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['CARE'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['FEED'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['FEED']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['EAST'], ['DIG'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['DIG'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['FEED'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['DROP'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['DIG'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['DROP'], ['DIG'], ['SOUTH'], ['WATER'], ['FEED'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['CARE'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['DIG'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WEST'], ['DIG'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['SOUTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['SOUTH'], ['DROP'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FEED'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['DIG'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['DROP'], ['EAST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['CARE'], ['SOUTH'], ['FEED'], ['EAST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['DIG']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['DIG'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['DIG'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['CARE'], ['DIG'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['HARVEST'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['DIG'], ['PLANT', 'WHEAT'], ['WEST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WEST'], ['SOUTH'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['DIG'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['SOUTH'], ['FEED'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['DIG'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['CARE'], ['COLLECT_FERTILIZER'], ['DIG'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['DIG']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['DIG'], ['WATER'], ['SOUTH'], ['EAST'], ['DIG'], ['PLANT', 'CARROT'], ['SOUTH'], ['DIG'], ['CARE'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['DIG']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 7]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 3], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['CARE'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 7], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['DROP'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FEED'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['DROP'], ['NORTH'], ['PLANT', 'CARROT'], ['CARE'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['NORTH'], ['FEED'], ['WEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DIG'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['DROP'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['FEED'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['NORTH'], ['CARE'], ['FEED'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['DROP'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['FEED'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['CARE'], ['DROP'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['FEED'], ['SOUTH'], ['CARE'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['FEED'], ['CARE'], ['WATER'], ['EAST'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['CARE'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['DROP'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'EGG', 2], ['SELL', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['DROP'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['CARE'], ['HARVEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['FEED'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['CARE'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FEED'], ['SOUTH'], ['HARVEST'], ['CARE'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DIG'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['DIG'], ['FERTILIZE'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['DROP'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['DROP'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['DIG'], ['FERTILIZE'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'CARROT', 3], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['FEED'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['DIG'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['FEED'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WATER'], ['DROP']], 'market': [['SELL', 'EGG', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['CARE'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['WEST'], ['HARVEST'], ['EAST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['DIG'], ['DROP'], ['WEST'], ['EAST'], ['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['DROP'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'CARROT', 6], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER'], ['PASS'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'CARROT', 9], ['SELL', 'FERTILIZER', 1], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['DROP'], ['DROP'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['FEED'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['FEED'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['FEED'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['SOUTH'], ['DROP'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['DROP'], ['WEST'], ['NORTH'], ['DROP'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['DROP'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'CARROT', 8], ['SELL', 'CARROT', 2], ['SELL', 'EGG', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['HARVEST'], ['DIG'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 9]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 4], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['DROP'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['DROP'], ['NORTH'], ['WATER'], ['EAST'], ['DROP'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DROP'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 10]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 4]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'CARROT', 5]]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['EAST'], ['DROP'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 9], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['FEED'], ['WEST'], ['CARE'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['FEED'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 13]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 13]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['DROP'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'CARROT', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['EAST'], ['DROP'], ['SOUTH'], ['DROP'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['DROP'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['DROP'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 11], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'CARROT', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'CARROT', 6], ['SELL', 'EGG', 8]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['PASS'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['DROP']], 'market': [['SELL', 'MILK', 6], ['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'EGG', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
