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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PASS']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 1], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PASS'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WEST'], ['NORTH'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['FEED'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WEST'], ['PASS'], ['CARE'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['PASS'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['PASS'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['EAST'], ['NORTH'], ['WEST'], ['PASS'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['HARVEST'], ['WEST'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['SOUTH'], ['WEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'COW', 1], ['WEST'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['CARE'], ['PASS'], ['SOUTH'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['PASS'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['CARE'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLACE', 'FERTILIZER', 1], ['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['PASS'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['FEED'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PASS'], ['SOUTH'], ['CARE'], ['DROP'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['NORTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['PASS'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PASS'], ['WATER'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['CARE'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'COW', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLACE', 'COW', 1], ['DROP'], ['FEED'], ['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 1], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_PASTURE'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['PLACE', 'COW', 1], ['EAST'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['DROP'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['FEED'], ['PICKUP', 'COW', 1], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['DROP'], 'hands': [['PLANT', 'STRAWBERRY'], ['CARE'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['BUILD_PASTURE'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['PLACE', 'COW', 1], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['PASS'], ['WEST'], ['NORTH'], ['WATER'], ['PASS'], ['NORTH'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 1], []]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['SOUTH'], ['PASS'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['DROP'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 2], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['DROP'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WEST'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['SOUTH'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['CARE'], ['FEED'], ['WEST'], ['DROP'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['CARE'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['DIG'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['CARE'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['CARE'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['EAST'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'STRAWBERRY'], ['PASS'], ['DROP'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['DROP'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'FERTILIZER', 1], ['DROP'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['DROP'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PICKUP', 'GOOSE', 1], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['BUILD_COOP'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'GOOSE', 1], ['DROP'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['PLACE', 'GOOSE', 1], ['WATER'], ['WATER'], ['PASS'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['PICKUP', 'WHEAT', 1], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['FEED'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PASS'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['PASS'], ['NORTH'], ['DROP'], ['FEED'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['PASS'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['BUILD_COOP'], ['PICKUP', 'COW', 1], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['HARVEST'], ['WATER'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PICKUP', 'COW', 1], ['SOUTH'], ['FEED'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['BUILD_PASTURE'], ['CARE'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['PLACE', 'COW', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['PASS'], ['WATER'], ['FEED'], ['PASS'], ['EAST'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['DROP'], 'hands': [['PLACE', 'COW', 1], ['CARE'], ['PASS'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['EAST'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['NORTH'], ['SOUTH'], ['FEED'], ['PASS'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['PASS'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PASS'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['PASS'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['CARE'], ['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['FEED'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['CARE'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['EAST'], ['SOUTH'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH'], ['HARVEST'], ['DROP'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WATER'], ['FEED'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'TOMATO', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['EAST'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['DROP'], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['FEED'], ['WEST'], ['FEED'], ['WEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['CARE'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['WEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['EAST'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['PASS'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['WEST'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['CARE'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['DROP'], ['WATER'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['SOUTH'], ['WATER'], ['DROP'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['CARE'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLACE', 'WOOL', 4], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['FEED']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['CARE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['HARVEST'], ['EAST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'STRAWBERRY'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 5], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'MILK', 3]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['CARE'], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'MILK', 9]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['FEED'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'TOMATO'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['PASS'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 5], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['PASS'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['WEST'], ['FEED'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['DROP'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['CARE'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['CARE'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['PASS'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['PASS'], ['WEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['DROP'], ['EAST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['CARE'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['CARE'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 13]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PASS'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['NORTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['NORTH'], ['DROP'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 2], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['HARVEST'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['FEED'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['PLACE', 'MILK', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'MILK', 3], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['CARE'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['DROP'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['FEED'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['DROP'], ['CARE'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['PASS'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 2], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['DROP'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 11]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['FEED'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['PLACE', 'MILK', 3], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 11]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['DROP'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['FEED'], ['WEST'], ['FEED'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['DROP'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PASS'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 1], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['DIG'], ['SOUTH'], ['PASS'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 1], ['DROP'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 10]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['HARVEST'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['EAST'], ['WATER'], ['DROP'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 2]], 'market': [['SELL', 'STRAWBERRY', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['EAST'], ['FEED'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['FEED'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['CARE'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 11]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['FEED'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['DIG'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['DIG']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['PASS'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['DIG'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['FERTILIZE'], ['PASS'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['DROP'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['FERTILIZE'], ['WATER'], ['WEST'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['WATER'], ['PASS'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['FEED'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['DROP'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['FEED'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['DROP'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['HARVEST'], ['FEED'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['PLACE', 'WOOL', 3], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['DIG'], ['SOUTH'], ['CARE'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['HARVEST'], ['WATER'], ['DROP'], ['WATER'], ['DROP'], ['FEED'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 16]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['PICKUP', 'FERTILIZER', 1], ['FERTILIZE'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['PASS'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['PASS'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['FERTILIZE'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PASS'], ['DROP'], ['PASS'], ['PASS'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 1], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'STRAWBERRY', 3], [], [], [], [], ['BUY_PRODUCT', 'WHEAT', 9], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['CARE'], ['EAST'], ['PLACE', 'MILK', 3], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['DROP'], ['WEST'], ['WATER'], ['PASS'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['FERTILIZE'], ['HARVEST'], ['PASS'], ['HARVEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['EAST'], ['FEED'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['EAST'], ['EAST'], ['CARE'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['PASS'], ['DROP'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'EGG', 10]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PASS']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['DIG']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['CARE'], ['FEED'], ['DROP'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['DROP'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['DROP'], ['SOUTH'], ['NORTH'], ['FEED'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['DROP'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['CARE'], ['SOUTH'], ['DIG'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['DROP'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['EAST'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['DIG'], ['WEST'], ['WEST'], ['HARVEST'], ['DIG'], ['WEST'], ['SOUTH'], ['FEED'], ['DROP'], ['SOUTH'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['CARE'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['DIG'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['DIG'], ['NORTH'], ['PASS'], ['EAST'], ['DIG'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['PASS'], ['PASS'], ['DIG']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['DIG'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WEST'], ['DIG'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['DROP'], ['FERTILIZE'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['DIG'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['DIG'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['DIG'], ['EAST'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['DIG'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['EAST'], ['EAST'], ['NORTH'], ['DROP'], ['HARVEST'], ['WATER'], ['PASS'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'TOMATO', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PASS']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 2], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 3], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['DIG'], ['HARVEST'], ['FEED'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['DIG'], ['CARE'], ['NORTH'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PASS'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['DIG'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['EAST'], ['CARE']], 'market': [['SELL', 'TOMATO', 4]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['EAST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['DIG'], ['NORTH'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WOOL', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['PASS'], ['SOUTH'], ['PASS'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'FERTILIZER', 1], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['DIG'], ['WEST'], ['DIG'], ['EAST'], ['DIG'], ['PASS'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['DIG'], ['WATER'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['DIG'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['FEED'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['CARE'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['DROP'], ['SOUTH'], ['SOUTH'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 3]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['WEST'], ['PLACE', 'MILK', 3], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['CARE'], ['NORTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['DIG'], ['EAST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['DIG'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'CARROT'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['FEED'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DROP'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 7]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['EAST'], ['EAST'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['FERTILIZE'], ['WATER'], ['DROP'], ['PASS'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['PASS']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['DROP'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['DIG'], ['PASS'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PASS'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['FEED'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['PASS'], ['FEED'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['DROP'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS'], ['EAST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'WHEAT', 7]]}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['FERTILIZE'], ['DROP'], ['EAST'], ['SOUTH'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 5], ['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PASS']], 'market': [['SELL', 'MILK', 5], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'FERTILIZER', 2], ['WEST']], 'market': [['SELL', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 5]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['DROP'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 3], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['DROP'], ['DIG'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['DROP'], ['HARVEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'CARROT', 9]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['DROP'], ['DIG'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'WHEAT', 12], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 11]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 12]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['DROP'], ['DROP'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 1]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['DROP'], ['EAST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'CARROT', 12], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['DROP'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['DROP'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 12], ['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['PASS'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'CARROT', 12]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['PASS'], ['DROP'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['PASS'], ['PASS'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['DROP']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['DROP'], ['PLANT', 'WHEAT'], ['DROP'], ['EAST'], ['DROP'], ['PASS']], 'market': [['SELL', 'MILK', 3], ['SELL', 'CARROT', 8], ['SELL', 'WHEAT', 9]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
