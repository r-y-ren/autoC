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

# Standalone observation-guarded reconstruction of a public production plan.
import base64,json,zlib
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rlKU5^|`lH`BkGaov?>f_!xQm-T|M;wsUHRcAwV1V7l0f)VZxqCb8e?O@|vNAKw&CNX`tD2;qRH`m^S9*AOc(|LJ{q6s~`Hz46^FROnpKt!#-`@P?-KS4)etrAqfBxft|J(oh?Tz1F{^vjb`M>`C|Ni#+Z*Tte%U}QgmyaL5|K+>SZ{EIn`0@VTZ~q;BefzgJKmPRb{*C(L_h0kr{{H*T@A&z{hrbv<A79>n_w!GGe)s;jAAI`p{{Am--gdwK`d@EX5Af4>|N6^cmLIr0%=~!2|E-Uoe|&re{=x5m>ZkYL|NXa5fBxn9J3rii`uyhCwK+cBzkk1Z2HQgO)1k-w^Zok|KhJ-A`78eA{^RGL-v9JJ?msSmyf#iJ|FY+Q(CgNG|L(hc%b1Q0pDebr_5Hiji228zzx{U~9$ec!KJ)W}6@O&4B*w38vr-%TzL-XI(aSfQKSlhqczp60;Gx&vJ(}J$8kX(Ne=%{-T&+g&5ygg|KK$}*x^g35%zF9M*1&9=ABZJM1nc}K8^G@S`SbiIR!=x@u5yPie^@$>AICak`sFjM|5abU#XjEgU}^vPZOq-6?BU(#-+XUns_)(vD{qDO@<*<rj3wnEhPei_uf1os-^|}57i$#0wDlI<ZL9#R8Yk>6of0s7w;?-ij<nm)yc}oHpQ3K$esjTQLPT}kgzcV}pRFwd{e?YkA6ci+4ig@~{$v43%^YOcf6|CGdwK#-_K4~1oh*fNeKRerR_vyK`8_CZOuKe4$*<V495T0IO@GT=g66zs%IALieGNjZ@l0NJ;%6VvkFk8P`FZ9?oEL3*h%6s4dt=I_LK~N|zSL!HT$l1Tm*5T;t6f5<;RP30(Z5*q8<xwuKIEM*8d%?6|5n?-1MTNqEwixoD_s0>#c;-TIBh|;UC|dbLsG(W%8P10SbX7^1Y}OYF4tjk^+{R5&kKMH5Z5ffq`&T6-p<)%=jApG9q4jZMz5Y8?3Fzaz48EGie7cvebetgynlcH-RHkAj&`#Go4XgyFP=)Uo4^14$H$)*C&Hd4knf6GRRBI0OW(Ii`$(TwD}KcT314~R=M8E&;OV4WmJl-TSHVtbAGjI1miP|hL-b+SE6%9rD{*d}$X2mxsG&ko`jYJa73vBks}xT=@bp9FwsS1$-g9{n8;jg!(>p6mkDe=ps_0IAo&8c)-w*aV{E%R5jwjo=jf=rwh*P9nF^Q*B@C<)W@)nOhr+s3FW{8|5Q>1iZt$ZLj1b-rxT#MZ@TkP41vWJJZeL7`_M}O&<Ul%=?i0L-?;-hzNvU8Z*Y6>4dYv(r_&&v;;&*2TmAF@TZ8VuR)v1vW{OR3FGQ?)E&h-BJ<6kR&ggzRCPpAXKFvHV!*t!!UKNjEY%HA4jWjy~!SJBaa5SnKq*7mm?Ov&oHmV{oP2e_ho)Dj#L8mB)6net>eIjk_(n=CzsN2{#)k|Mm4<ojwjm6LNO>A`pwxX4%VX&C8MT{4btP3&n(i(DU?HdCs9Hc;#NMD2Z)~Tku6_)k8(Hx9A1y;S{bJu3e!rW}6B`ewWPnu^&Es_;jzGYxFxWUtG43c$ZQt_Omm3U*mb@V^F(W+jjoan=Dx@bl>)QSWn$swk@nl+k-71Z(BeK>};@V+vf50m&<t`+7F$N#(Ali4_5@TSGQOa2BKoIy4SQ=r5k?P3*@*VU9E`Seth@wzlU;x%`d<Fd-xbn0J85stWF_-*2v)qhAevPG38v^lYk7^SDQ#lDRVC5AR&QoK^x^D7A)Oke!bs!A;7xjH(7M=*Z)AmzT@(rT4EYQCY|e^n~ku@3jOsBee+RYfM?sn``*gL#dayc6}R~MWh-;O@olOVLBPjeo<a&lv!Bc_$bGZw`v!W&<t2Di&{}@YSMYsFAB%inzu2(X_uZcVZp|n>sHn|b)I5WS0x@$6?=qLmx+;()T}^p(eiZj+$M1M<<69_t$L-W>z<95zWjy<wk*99G88^1AmYnekqBYz+AMAn40mTbrS}z`2?HGR2p~|QdqRF+D>ouDimzB8-y&(NgxHi)<*K5yp7txKqjIF-wq#LMt)DdWWXlJX|#Elpa24tSq#^dVQ{;Iu<SlEVY|6aK*Il~tu?QxJj$3U-KJ$&d8yU^+}fd_DoAZUZJa!f$Qtq9MK(EH__G`zLHEwB2)+#?Mz$>6S^YiFN6e|-1wr~8i|{|bDcm7~EXSek<L1nq*fn>Y{hu8t9D%)v5MR4V3r7Dm;eDP3Pv|6H$O5+z?h^?LCLyeEWu-!Tdt=u>#Kx^bS%U8JZb6iFss^gAD1W36xulov#&z?$=NO+nR%w_)Q12k~TJA~rL}kXJi(@wDa8{-wA0vg(`hR`SH^<hit}F4pC&jiha+^UIRn1yjn3z!hbXLwIkG3822}5(u6Cj_|@bCFTf>95}L!H;PuGssU<cDfL1FAyiz1ll+iCl^@CP8!`k1R%9SG@cD&bqCMpiqWUpcOYeca9$fJJ0`ExoVdUzf6&P4(2-J?O+Pg$nCPsSI^M_O!wy)XosA2};gborQ@z8E9%*|;Juc8^yu$V7lmt3>-sZG{`2gU+3l3Kt0@D;_#+DmqyB8JH&=(KW~oDU8+P$GSUE-_pfo>SKgobeV5I`TjrIDn`P`CDJZht_hQ*WDM{wt`(r<UAy@X(z>LPAQVfy7{i5K}%vwWwNQY#3=#N&KIj;N;`R=3+94TP`W}h*i`qgXX_p=RQJ)LGF;2H7<xgq4&?6uO||`0rj0R*4LvQ#kmr<R7AoDS>~=novX_eG9TNv*Uk9KMI0dF?2GnHbjfjI5<0Q+;qFD7z1j{g&g)rmrVlX{rp9J}GuQE-69N<#ou)+Hp4x9yx$bG)mOnrIk5+Yy*wjz^!j0JqzoC>w@Q(UidRmhw{hn&*jDB0|yv~x7&noBl60pD$TI7o%D_!D>gKe0T>zyJ^t_m^V8E{|G5Z$TS#JDr<=HfU=*?Ek>5ya%oqYsT{#R-b?B;U-VbNXRynDTwQQdA1p6f5sNmO?Ef1#k}yF&IN3D`enyMf|6(mfZ{KHig6YtdS3j_`%oPun~r6J39+khgg~+*Lvra_q&xTK7h1bdL%z)YCIA9d)(VqANl%#=-0mXud3#Y@<~a1nT&c_TvN1M%)Qreec;pUDF;*<`K+rRFLu6wWr*N!gQAfhCi|;quD5D=1K$jZQV$qgG#jL|sEfw;&8j2~Mhy>_EL9?p`)R0exHfzfdYlj#sJCpKi%0tI5&~9pw4wx05k(G%2TNrAmL&>dbUA8kQT;T}thbfJk(Y(b=$Y8iOHhpW3=xpSRN$Igv*Nh3q|68v_mV3P1>B|B`s@U@-ZuUBkl@blVA!>vfQbjuSbr|yAgjbX4l2T0WTd`x5zmG_erKs1xUQYzK@WqgGvAM%+i~Tnj5y?(&SE%?Zj92!gK%%H=X*Q#m`6^tHK$kY%g>Tqyu80Ec5jJLDdi7V9DMMOiz4*i1{xDn2+X&@Ya60Ro@-{HR-M01VzG&6g1bvPu)7i_je)#ZyvGDKT{rvqKGCt<u)KzynisfGgERbj<LT(OohSMDnsu*qQLM*f1oDO@`lD%|;6DjY4VZ3{vrik+g>>m9zqpanMPmE0l#4fiOLU-*l1}S?KZ%a+rD6B<9RDTWr7_estf4~53I(F@`2dR*6JF~bL6wX<+HeKsOo<6a2Imgxu(8tMN2A_min3w`!Uf144QCkR`CvQYPOah=x%nafIs3AJQOhBZO&ZOp@<4X<O%V2T;!w+GdOn~uv{52hWW19)+`|lKC;57p-K&^Ynz2WRz%B$LbNX3OA8hOxaKCYC^6e+demrJS#5ke()VQMFrn!@FrHGrWva4bmR$HKZ{G3Lzztgz@D$WCXN=m_MC-Jia!e}{xVRfL0Mcq(`lX1TPp)Z@Y0Al*?Te=`L@(-lGqE>Q7z#Ov+^;nIt>ooL*pIP|*CJEpfWUvK!MVFMUWT)si~0<>{*A-D{hJId@KJ>NTy@%<}gne~w_s*`)5`%Wfau#9390;j9o-B&EqDROavK5L<LRmmMx>9Nvh{kd|yNu564(TW@Sely#0*_${*%q8N;UQP~axdUut?Do=3YPR$D{pRfQRS{XnU=@@$13G$M>@w3j_uWaWTqIaQ`zoOraDKs2LRdQ@jNxL$Wwy5GbWWk8Cs1q(v-1rR#40j2xbs<o0uONAOi{2x3cI*6QTz%xmw+9_U|LOX;qs$Qa)~Sg6ex)u%$j()g~3r}oJv_Y0{b&uTDMu2&-(Zy8ze5vxcEL_jue;ks=MvFz&*P>L$!TWq9)9s9qqK#3v*9m+6FYlP+Jnz96%wH)+4Sbu$wuzS`5|}&rv^JJEe)|%r^5u9gtbZX8tV?VJ6KAZHR`HkrFwd%YoCZdCH#|q_#4@{^dv8(=;3o4u*L$v#csnK~!EVAs>|e9m3^+mJef?j=&^fSUG8oAvbhd?hM`m^b%$>3jNH+qm}1;$Qs0Rm_rxP4N)A8+NWFC(K=Hnb{PYqoFr);B*qBwI+Nc)HG^D%0J2^oNx-@(T2NW{hnU8?q593^krLM_dht8dQN=qOlc)lNA=;Q+K%Bu?Jf@fvrvLVHyF%|g0LY`c8x`Ih8mmT~M=!+L8?17TjZ;)m*qZn1+^9(?d|tX-PO02!QVlx4>liU-h^RRd@=7{1#AmUIhsmSU$?W^w;gJ^dVoIN-UDVNPC2P=v%?a$+JE!1poF87TKShv>l2Rs7T<bM48I|mXg|c8S2u>a3pjmGiqD3FPtcQvOtFPHe3<m`=fbvC%Q(Ua-<wu1T*#S@N&HeIiYH}HZek%=TY>-6iu1;ZK$W(66Rdrv5b_^A>feM~LDw)PU2H}hd`8-uoVfBe(rXVg3xH~t@m1W~VyMIbb8bJ7v{CQB(6xoc&2vFDJ@J!YyA_M&%?l*s38yoivrrk%<>N^Lc)9eAqh`Owu-(=_xp`2(;6egh%EVyMc^c)-DyP}MeAOY5_^uH{~njCCZ9h5ExbpP{D@BdY+p}A$1)o+~qF;8$u(8G~42og_5p1$@`nlD=z4ZsjqAL<+Ea-l!1w^Epfj~w)agEddz^1w!mlncMAf*Mo<H*5&@Fgz*6E3HvHD3OD}gNad3hEYq`8x=+D0HShAUAlBQCabl>_*&z=a`g{19!l@NR3z+p;0&dX@j&r3rykHI(T-&d5PU2~KRx+sSl20k3AVELwR+@;rG98HR+I-2Q*batF<g`n0-Y2s*^OH+(#M&?m89N3en7FSz<EhXR1iY}xG;z*Jc`xCsB-dMEV+jBw$G;i%{U)Fpv*hb260Q1ywZh!s=^Uz4#2wr8$$@U6h}IJwERC+;zklcC}5O_*+Vo4#Ecl8Sw5tI=mD|`L=NhWSb#_X#1Jg(s1#kU;Jktud4L{9%PInR$b#mUW&weK5|_a|s3V-=)PE!c_mSW(=n>IKF#izir7hnD>ropkrjUIj0IfbVoz;b|etK0I^qWW|aWjd<JJ08kNjcFfxJ>PW%b1wc?*i6mQzIaY2D<}>6l+$Zok<55t3z`D;AAvG03_}EZ0u)vPh_3QURXt>;t*Zzhd_S0{nsrYJ5UK~tH&`WjuWNrY6xqVI|Z+lbE34|RTL66L5x(eXs2m(iR5P`<7VOfV2tNdjUt~0+k+kaH@CimiVRE=0`=6=UCDHyRtm5V-93-tNk;(s?IMc+h43x`3z6S)%gvo+99{jHTkwurmPfT`r{M=O1iOYv_znkXZa%W^ait7$8tI@^!9DZ|QV8vxpD-(n)wqp{Y+XNVwIUT+N}J0iz;2S1$b!|}DbT1Xzkhtr$np63$4e8r>mXHmcn_R41BNye!p8{O>KLS2EkKY@qx8Q8_s_p<#UVKTMa<Xr4w%C_dy2Gb#i18#4n~E^Uy2B>>z556=*r9F?{TXve;C)Hb&8i^RFKL^xw57cBSd&nD6n;z)=}98UVcZC4Dv#QKGrs++LA=meH0n`?ENt6vAr}JtZJ0FR&?h?fk(wg*yA;{tH}`j>L`7$2cNTl4!AZ4mw5mi=0_$@ax^Cwp_wNE!!RX;?ahhjjNw3+;^jqoRMMbY7QMn?)}wka>a$g-PD$NE+y~ac=be=WI)Q>@Diq~OsaI3;vd3J5&gt)u!LyXF^b|lo(Ilg^Hl(MrGwN{P`6NVTr)QMYJV+A(6C9*Bm4!@BdFRk8ahmNIfj<EU_J`s}?YgcP_SkG!IT49kJ@@9UGl9`pOni{YcTiyQ1W8tzb9pmU4wDCw6F@)Jym23*K3(0|90pXQ8|}r3!#a~xM_?0^IG&Boc$!MXu>_v`hg~+VAGl)is_UzqslP*uu&wU?^n=xgK;2kZH_9k4w#XXgIi0~{%nyz;Zxafm^Qc*g^ld5(r@2?WnI)4~L^9+uK?CO@^Cqx0xA39;Emj@dK|u|qR;y{9!b}$r!?)nsKIO03%|cRHroT%R?9aLbl5$zu4g`f9Ch!*3zdoqfgTd@hffkgay5-!dRRWAYGCV=%mCG?<VDPAQ<w}DxPIbpc70lE|pIvr=pk6s#<B=3u)RV?DPhbX|5XlbfhMu2RaMy-7aDHK=Qf-8TtsylzF4(RpA#67^n7x!jgl3tO<?gIhCK6$me=8!`l5E`dRdghZP(}${oLiwRE5+G?ch{x{CfV1;s2rCTWSZ+MMYiZQ5{~cVE+#AKfUBhDxFD+wkt05h6=smnM{&Tbo;wC)U$C4r+iv!4Uw`CY8fcA_)fa=BM4(fOrbB{^=vn4uaH9G8(_M(+L}!6rTxL1LyN|owfJd?EpPuHBxH*i(mSf^R<74ECG9Al#fhYi*%W#uL$~o}t6N6SbdinUBB=%Ai3HfEvN=0okAE55>LLd=>6G6;3Z|JkG9P0K5T>2<Uc`kx^WUgxx25Lj(TecLgdkHT+o>7lF#4un-(W8NGhXXeB`cw4AZcU2`>;<`Digd>9_4+VNlZU+KQ@x9LW~WaAVbMY2ja?oU!W~t}fY!fwLeVe?<SjFEniR6q=yF$FSXGq7adjF5Iz4z)EL@6;@zH{1&^g^<*p}vb*%Sq3`enlf&rfj5jN+w}$SgE(^dq}5gT;~P2$RlOfg}Rd<=(Gh3Yh|RE!H~OW}5-P!2ET<|4A(+J45dsh{58IHJM2Vfs>3~f!mJU{+mEEYGoEY-&w~3LhDr^(u-q9qPa5p!@=MWnT+?lh}z>MTtX?GIJmf%ff?DFfNjeAX2`SYbX(6|-M!FsGQdVDTY;Do@Nb2a$d(#b*eU&Uks2OR2I^`cyxeV(-q|q(qPjI?2`y=t^Zm86up>395uiJzoY-Xk+sQfjcs^xMAPKey7*lTXN=L1c?fXbjnZl!rN57NltJmqw6@c_*)0D4^(CbmqMof*C2~D=sZt$yBrJZRafv<knYw*wJC5Tr{s;9!y`3Oo|EeN|58JA^J?I22%JUBq!$pk)JH@I7$ag(~>TLJci^h|Olm0vAxNfS_qK<P8rpGg=sI!bRHgbndUqAg;60n3e?Czp~DkaOwj%)Wz+JEU2Nrr<Y6d@nX(-FBmDW65eGEzU?CL@Es6jX6ZvTb0Sls3@!qyB>{U6#Mq#!r99PN;wA1gtbNH{4i8QWn%QiRu18|)X9<!4FQ=>zUfs+Zi<CqGn^1v4VfIu%Tb-d-#|mropL9mAQ9mykl50DASo>;2C_rF*VXi7xE9op5w5SnI}^qrxY5IgfHPp7V0&ZRvRY7VveNO^h>li}RN~a2O)J*ZVyW-uw>zLx1%lwz)CS3Vfgx6@fLt2U=~P(|g*yG%MfJvSZWiWp`Q>^k=Qso;9EF4fFf{~77ji=>V-RrBX)_io5(BFN*#IY_nv96POSMO@I#24Gnk*0jIF9-u9w@jC5sK+^ByjWUnk-c24PST)D%9P>ryMN~m;f;uI-t<D>kbT&S#HZZBIvy>&Ltyq03ce})2#8HQv^Iy5SY6%rcVS7C>K(L@6n(;u#?a@8poPKd(kYx44W+M0+$4l7CJeER$Sq18+7*`n6VIk?qXuIDeZPJK-&RZ5|!8?ZML9j(ZtGyk80)aixy2lx?K?v?4$8FBKAiu-iRApG5SitX7gSjubU5it*l+3gk+_eQ1~YZ&NkgU5xd+qjI>*Wx&{$F2PMX92Y6v5C^v9txrf)-#6eXSFNQbKZg?H8>*EqFo5FEHrXDmWW%3ai9h!=QxmPg2&3j#%>^$wqz9K=%_fBPJ7DmM&ARzjxrEgQElTLMKob9AlW@TX)*q(ur!%D95U6?uT6o|jWe&N=YBa|x(08Iiu1$uwg2p`pZQ65Z*Pj-tJwfKha4}3$xaDFa=&LPC*e+Hg%hP11OM-eCmx3w#+Pyu@I$Kzyzg-uP2wSeU$Db%j*v)G3&bJ6u1qLYN<tHVRMpcU^Xtu9lBjKL#(8e9@jo8q(x_QteGq#a*2GjMfcefx^VJ@D6jf$bqY)I1W4gH8r(woidsya3@A08!KF3`79xW*_lLq|3gH5#<ZsOZLDn&k`NQ)ab<xgCT_vJ)=_3whkZjR*m`Q5D57f)e_5PiMR!UTa~}q;_734e9#sp-43fDv5YcsWLLk3^dd|oc?b$O?3J-=!9B@j1&4F0CCjRCQ8BtPrXOzuqC1JF!A)a{?f@moFal5M>y%rTS=KJg)zvdJykWrGR|iC+X(pus7z^?bOlGtMA3elt8%jpsla&2AP5Jcs<GY7H-GBV}R~^c%qItWa61xlxRW`Fl2UlrHn%AED;;ifBEd24~3T`(-LIs`M$6hi}#v1y${9W$Y*{-#ImA69Bfl=oN2C&?&qf7G9-VrSFJJ{vcmYwm)HR{PsPS_s3z~xl<=si^9cfrXF__tw;298kE&3cjP9zk<6Rft|{YFSt$kZ+V7gvA<@X6!1Pe1wEOJ>nA>j0YNiOB{l;Kw}oQ!H2u_V<3=HN@OSQ#b2c@2ymrTj<-$$Ftq{(28?dyjn!t`3?#%7k%0mB@HiqcmffrarAJw(szW(Q=6{wXJ-}8v22kwa943AG@|@koFff1=9qgWREJ}=VC(bWxR&BaYfLW`kw8f=MNh%rCb;BP?PJ=#}aK?MTPOKT?_5F1=6hfQ0F`ng)hL?l7G6PXCf}g3Do~?H>C1)^0+9J`zw~RLcM}ejm=@oZT1zNRBirz}|@ZOmS;|)1jNH-E+oE;(>5L<w4%W4i+-}UO4ET{;K4k{gTfZ3!ln0gmJXyKz;8y(1y;MS{?&Lk8}Y9Tw(w=Brjs4!^$!MqVgrm$Q0qSinZK3}4Kq33*zw9-Oo@|{2_=8#kZnUZDPX~)^&!GBPFRc)}zLPRx0+m~wvvPpR=!5o0`<MK_Q(lw#>yG7R!R_MI*?r27RNp6DaSe<${srleS&}z5nAaIi@H43XP;xsS2#NeTGbpy49`GtRLqYRlo&k3xxAa+`EnWb$R@lF=N4EYg*$<da#-13HIw`RaKTN4h`Dx9_&o>%+qeZWHI8tk~PH&0JH>Q=?t=WR`QTLu^8KZsMz1fr>PQ5~gggVp+e%O`Ac-vC~66C@mTvPx(TG9fZS0g;X(lQKQw*MKpXViME>ePegcosb%~nQ`aoT`h@%1KPWc#a8?!oHCWjkQ6Wcwkd9PTw}_z1Y9+R&cP%l2l92ChNSU14Sc`jAZ&%ozYp+AMu1O9`=Pj|6!-<JhbzuOH1T|S2GP2)4<fCm8fAu>8e6#zN{;6<DoF77R!FE&g0eB|DOL)7{!{wFT3#fLTmyo-5m8NX4m5&TPHl^tetDqi`YjIylTkI6h@12^2~H*No|&5~tr-O+<jrmu!~tu%U^bx-#buPKq74SsqdI<Nqg%ZBtbEoX8(mtK4ofpYEWLetvm+RE$?x;-{gcs!h;3M5?jx#uqXi~QN|8pN^#@b5PHw3XO$Sne&+Wx4<oFtr!vPr#Mn^lLsE1EenK;i25_~2KwS6EMaG!9ltp$$oN*#C6z7Q{`c7X+KeOL^j8saXq3+a1DAxkDHR*c@F#PHa$MWVd0^F)w&fGLrZkAXIIwqy-rP^JgiSR1`ZpDW)A#Rgjb0tgZC8zr3m-W>ZYXUi5lpyX_sr!2#m?L#GvOD9B{?wYht;DoC#wRq7bA+>jOVur`v(!i#-WE%O}@f@b`1T@Vu>Kv3)pqnTwiAG;>jw>nL-Gp@noI=S#-j>jg@(|0+pPYU0=Bi+1-RMvZ0l#Y%R*WwcAY&-2s-}#if}c|XAg=OLG8hh$c*sQ3hzv`_6e(YqsRFHLWC0-*udw5IV-wwPT`xqbU!y#?Oppx`YmUcNG#8}!(&y0|2P4b%bf>#scWCAIK|+aBmk<a6_7PeLaYnI{+bWrs`;7u*XGn#Xaw*DQqCLtIbMNXPk|FML>5N>=Kl`hJ^Yg(L*5dPrY&JSEDKXYlGVBaQ?{vVbT*XVsJ2_MW0{?i!12xIpUi;RlFNM)ADEW>ah*2p)FzHV|1h3@Pf&@bl;?RY$LuxdOsfnB0V;SNRN`jKCfq=B<IdI!OF=cUsjH!Wwe#*pYr&PUvh1Mkr<@Z1Rz_fTG3;;1+m=xde*RU8`ty^O?;(cM5?KmB}Z(<2Rj_LR@6?})R@hIBwLb~I%AqEW%dPR3P$rnp|7K{uyt0D4CiDpAYz$2oBu<J@F2WpC>#p~+`Qe&>ghnq=zbhg$Qy3vXU?d+wTcnTG{&?|=M@c?qy;asbeuIR24Z9vDKBTslGZSEp(mq%32jM9v-kTdQcas=`mGu12G^tb{B>hQLV#qNSO<82R4qZk07B^RZYH9dl#GvWnN;Z#Q<<*N~2ab{Ogd``w~5H={JWHSJaKLqMwpyNG95!LF49i(mg5ZbEFuS+RN)SL){P`JF)^36-s-YDgyFetTRH{EShLe?jKf=KKNI(c4;pm-ueA1rdEmminM>t#oqp9$knP^{~E%;ShUg3F~o;YMN}!2?Zokr=Q+;ntgVIFW-oUiW0PgFf}SVmc9;yF(ny6O{VUbW&X1ua_eP>Jre|UdqM>m=?-bji>U&XlGUa75m2rj}PDwQ=hm?$pmc(1UZN_wmV8Jgj^DRhKx_S4Prsxjtst_HD5FVlCi!e%+!Qn*oojwz=cH0(iWlKFyqt~$D^ck+WS$~ofbrJ!H$|cFYgvR_*B!_=>0wdA`uCmP=F8Jx6`v;dn46)VY9CrN`(Jn-GE*GA62>%U<f<)#BD29sUXqvma(f~z9(^AUTa%L<ZUI1tgdEe7D8Ke79meDoAcXm8y?LI?5S>EF{v3-9q80aa+}r|E{ee??J$rzD=DVSSJ??;Xi@Bo%MbvKNm@w^tzpe_;!W_t<j=2b{?4`b;7-mu$Z77+YJY+ageZwp$L<L=2Eza(BW3QZ{8VAmV(L3!YM@+(@=8bs6Pb$LekW-@PK;HEMs4~YAAvS;A<XQy*S_B9f9yqc(}m3KL}7Ogh8+OD4lF&Se&opewqw;A8<~B~zZL00GmJ}S!j@Mu<{n4Q#rW97;jN`$@x|}t<(*w0jzoS>sBayFm;@Gxc3In-Ket~3w^nd`VggHWN|fiUjr~pAcdWB-^N3$q_r>=_>t5=kHuPVdzYBBQw7=qr>{|O_=|G<CH3B&NjxCwqG_%+_Zg}~$!ugQ%aie}!wl%pkJ5eW^ujHf1uAZENz7WL~VfqW?gs`?qej3+x8SD6it^qo)<N!I{f&#>?hrzzI%KA~x_xK_%ob~BxyWHsvMMp^`K{TM(%{Q;AS^f_1zyZ-NI_1~r)CwNx;DkL9fxomDA;Rnud}LoxiAnbTNY94q61)4*qW4u~CZB1iYU&+;w(+I*9~r%2j1lwsZapf$6K~KO%n)5)krS2L!s`eWWyKXou89^1A4zhNb&iyB&Ubq5I~K29T<}s7awRj-A~9u*zbYVd=@_jOPP)RFnE%shx=G5>57IEdQ&Iufd_sQC41Cz3>(0(PO~8vbgA+O&xn@ll+-|WzUT!i0W5HYj1af!|xOm+oLyaoWZ9t;}s$+mAhIQ{EnfJ!-yVhk;bKfaEM2|ws(8Y8pW+zz}3usZRo)tb~wGh4}FdzYZ3S)=Kw74by@k+{07OEt41L!Kp@<E#m_#v>QJc)lDWP|LFHe1-+&_uW0;YFC<DwUXeyNtBjpq-m)__OIx3}zW;n!C)kjK=x4GP7&^E2?!*W}S+6YANGFrwbti^W>>9G<OT__hI8TXq%W(!~It~qUv2(Q-8?FZb<00q6VH=DsIRG$-3O2(>35?G|H${SJ80_BZC!s)o(qi7_bG<C^yLFw@FIJrs$(L=SiVO8MusTXf-yQE*Fbf@_;o=onsSJXIqjm^@^2WE7usfcxgOVT&#x_d;?97E;z~6i<8R3_3=53Aq9~c&O`<pzu}^iQUre3->s)d87juY$1Bd=Q;q|91jZ9ZaywC;q<YOXepfj3fxTgq1s|nP9dfvxuSpC-mnYaq3Zkq&%)U@8eb?vMsr!IvR=<<t15&3{#)n(IT_gFRY6|6Mg#)SCF`LK5aqmeL2y~Ef7!%(mxyE=VJf`!yIy>tEi=a%$qEB*`A5r#J+~fB9u#IsD5$*T6mRUKx%SV|s=88lHJ+!>#H{#Y0E^Q$4$QMMac4^gLuA?HM3Fs;wUwb&DPXbG7-s7<5A|89whVN?qX(#JTbE;`D)^+s@qKlEvlj6%4SP@u#!R0KkiiLzeF2sDO4+VOhE;Gg+M+cTFX6p30bmW0>Y|>D(NlkAsEZIkL7B@W|8jY;l<N^+ptW92X6(anmqrYvYB#GREz;Oec?aI9H-pAxCw6p}Q;nEt;sCK2k01veL4r0?KVKlSJqYikvcj@$1bj$ON+?{SPt=Dc6bqw?vAn5}f9y8vC!`cqM1@!N>6^ENKu}c*B>9vZ49XnP_;1)h!viRjqwI0$YZ8zfQ9-^oh53}nBK0_f~ZHhk?BFl}E#_i<SP8;+2gHdXB9-Cc+umhWWApA(z>t~Kv3p#iaqBI+LbyNi<$Nphfhg(`d^PaH=<-kqZum`F7{3(4n37#0=ikSg6xwIf090Q-DV+X}6H>h_N+2XDyO@($kMFw$jfPlFCIGA`vHqWSVpy%&84;|qN$0Tx?W_l1=6$s;PI&DnoylVtGI{4<DaugoiH(F(nsvtxGi+%l~5WU5y;$fR~&<V_I_`tvmw)Lb@*P}i9{J9fDx?WW$g6=MF(oaN?l++K_h()6O5M!6?vbyH7)B{NBb2vSCHx9I^cxw;9N~~i<FjuJBA7Wu}_{8De*gOjq=Qdj{?KltnikV7KmAWL0lmNh<AksJdL!<~Cuhn9B1%tNqqF)yOEL7`-L(4kvAikvPq#(`d!9^PI2xxN4`kUb&aAC+VT<WXI@3S|aZ|?v}V4-O*V~~(U#YVBD#5y`6rq8di{<7Pu<JB_Q=HGJSlVPD4Wqr-A=qQbKKz=Bwqf%1fNld*V#iuSf;5}5dM@2E37!y*7ZA(Vg>oL&##OZ0SXm-X0pq(sfEg=tHS(^?N?x$lc*5p!M{Gk;%0vigjVSNA74{mSZt$t|k+APjlyQJ6(+FwsCnjKw`Nt03HiJ`c(1-;+4ZY;}vv<TSBtKw0l3MO%7>LHthkx8PS8YK!tY7fxpFA5$BD&Cto5^4l9p?b!ruH|zUUsI;BGc+q_r%JC3r5_!{=QL7f-j`2c&O402_UVP-Rj9xiEP`YiNEJq}_~OLN^muc*v|uj}8hP1N=nA*O%+)m81|j|%G()gz;!AaMtZhsmNh4ma=wr5Z`go|J6ZeeN$>Dh_ChQEpqK9^*YHd`ERR6BTy4h3%zF<9*&H)+F?kKlg`!Jv*^EkwSU(WRr`l+&LkSL4v*N(r*gnSBQgaD<<>9Sz?g`(V^u129)p;{&nZn%czLdjMl(*xp0;U$|a0a>Yg{_$Fgbz||C1lvYY-@G>2MxIr})?aY1)$_k9GW#SGM_GP<@sWcNHCMCePFhyddtCY*bz~es)HF=MktFCKA`xzl!kzRi*0^ld5pLB^pMnpxKL|yZq46#1NYG)%DvAtQr!8E4??P*V-fp1of+&_j5}I`IzyxF%iehx(&ZdJNB}RZEWn)kj8<lW~;53+^FHE)2765Qnk&-mT6=PB?fs?xH^md5|B<QpPL&?O$7y!`hxIuuSP4w;1z|uP!fRIp^zhskGWXR}h>hxV?Um<;XqTgUtHwd#p>oK%ld1!X07)n#jNpxBMWTCJ3N=8a@#nu$6s)F)5%BoV&8B9_(3x@$oY}nDYm&Rxt6_~^bvBxB{;VX!HYjwx>W&tG6^Fzv3_n$rsQ^wf(FI`Z3nr)vIkPzlIi0a;>dh;pZG64gYueg>5hX0v#2k<0l$h$u!Z_y?$uv*8!xEwP%TchFQU<4b6oB*-FwdujzDaec7TqdGq{J04_`^}ix0sdI01%f>W7Rn7agED(;HoYB&65hzil?$TTo{=W#7b<?wN2qwu3<2NvYO~42_;o5N=yvMxqC`Q-PAQ|^=y4R#T-QVD_G~RPkuS9@QbwaqD*0^~mtCDgqQ>wP!1qdWjEeo`ufg=N@`+rV9i_m61mp}()|j?QeNb;jG|{`@+ep!ssggM3C=y4<e)DHFAh&TZ#t24-;`Lyu&O9jVfC8{+YRLA`O-_p&Gd_%0&JPoyi8b@Zmn2V8ftd*Ee$()_>YbHnibp><!}B6MH$T5<Cs0y>kJw3|q_WK)sJ7SDPwPtj$4H4kz)=qr8q#Vdv>n(&qU02;;a#!F-L_;()vq};(4F1cQ#RlWY$(t=>vnIDD~DSpbgw}K<1OJdx=bY-;)&Zx@gl(E^XSaeA$L~r31SrDVkNsW@j@(i6TvGW(9|RXQH&T7D`A}0b~WYNz03Z~2{l~aRc~L~%Dnp-zrxY$#CzIGk^q?)ClCe32w@Q`F=nzaWq#(=?(3mJN^=6}Z;%$JO7eSk0)*Gn5283ZS*Ku`OLB~yNlUX^=S>!fxJ`@MZ>Wi?9H58)6<aoxwi7q>Iq;2ZR*;cu?~-?yB9<6)+<2V^w)Vgipvj3?RZwS>^)qi=5RVnVYgl}h<I*V-xXMfFCHAUv8<lj`eY2wy#|e;Lz^QJD)#)3uFOxJOP)<+ygh<9*L6fR+*hmg{8x=;1zjWg_BBC*1TCb`-*<Z0exsIlMd>-c)90m7UX&~ef(hk@lPmwrmgcsI`0s_8sLd~o_sfl+hXJ+g%&|C`zR)z6lab6;DVTgdk8V{$<_tpX!S>6qRX(+8#TA2aUX1)^!<rG6l0L|dT8QLWeb@C#~&NRS;0G5qPUQKN9gMunMgx+{n;E~g-q1#~UB4Nac2U;isPk?g6nlkK0OL+vrkKCd7%Rb#svRr=Bh->4emh$v`7C$=`Qrd}XBgQr`2CM3QOk0DCVqh+9$~%cPbh!A78z3nihh<^h5K>3tD*AYXxR_0Pd}zp=^^ySUEQp+99d&gTR9W>Q2jb!0Zz~kw#H(2kP$0oA3cxmJ0N)-`&4(6}LuR)DWK&GJ!-7G?Hw&p~@;USHaE39oEhlV^m=Z$#<%7!%<k8;^5l&ohY>SnD@N^OAX+c+aRZe!d{-`tiGzLTk#VtT{&??}UW$AJN<QB{&!<WKbViZvUO-Y7S3v7}$bCdN<0p!Qtl>5P0^n=HtHAEV`1fiyDX^C29UoN9h%e1yEuCVdp4Y7$$wFTt^1Sr+b;+D@My(^yN<(w4;i9zSg|0v!w+XC;dVA?C0cF=wQ`SCfMy5HEbpvqi=o@Y+xCBX^DQ?g?r-95T|JlYnLo*tenI1sdtc<_=;N%i=?7CzoeEWOU)tcH%6cldCMrc=^Z@vFvqwJnKcQxlfl9t0i};Pd7jYul;#8Y`RqjJ}y8moZ!9XVXbC4T;<$xEIADiG)UB*?tvk25T8^97mA>7I?Hw(ScIb<}JewjF>$#o!$!~%N7I(E|KS@|B0&FRuWVTYOAq-4iVI~??IzzgSekd_hs$<trYC83eYWlUn1ccT@nsP4Z-r~03HbBnw!IUSLpXHhIc?KhOLW)Wg#X(5GN@8W}ly5Al`+_5Z<dGi_?`kI<_s5CmTS0DUsON8_ERM-C8~!MTRRxi-vMu6$qC8CW0}GD3+FvIVhcdh*%jj3@8?Xe~DSKS*$xp(f+bg1@J&$k6@9prvMuXq_o{JJ9_STnj&OYS5tdA0plM?gP8$mL^%iG`Tz!0UXj^{+)JKoWx3ZbC-{Ly5{I=0Mv;<ciSZns_PSi~knaCcL`$^4rIk<5{G-ml4uO}3M$jWdF5r>&djmIOWx9^w+~_xUlb~r8ZK!GDGN4fBz_ECxAAyCIKWFs1TE5l@zZH=Fp;akS>t_g{hK$A|YZEgfA2NSx>O)_xA31(0I0~ehi<*<$St-nEvYxN<8k&1`Eca^eyE5nFo*X~|`jH<W59}N<3g*gmW?$dhr0=&R>g$^wI|cxWmBhXF#XRH23IuQjaTD-vvZHPVyKo{Hgq9MfI4y`7OSw0@c$Nj^8tYJ&*SRJiWm35}8HTLx>eqmKnWW|^j5{s~8Rw;BUQa2p6GNfOA+WD=ONaRs!Dmzc2wPSR3geY2mX5&~l7V9fY=s8&(uHR{!8R07?lmlY^!Usc*qf^jG}qcFr@kRH-5K|omm+!|e&L2?H6B7lQ_e3-5F&CU`l`acq?;Ti&P!n}v|0VJ0&W`^788e;+$J9n*-w8_@phlq_S*O^e;Lpj=v-iYm<s3=RMOcDg1SgU`wq?QOTnJy3*O)7c#HCYZD(%JYVC;K>OlPNxR+a6E@>&i!i7u7oRqd2^xQJ8gDe}PS;|W!@mXA|pFvj(9L&oCfDU9?hgM-0XOD~J2DB@_gFl<cLBV-0JsTPIbU9sCszq|j*;=7oNxyYOpK8d$GQAoW7L%M}R|=LPNWsz@k#G<i#gEQ$5_Em+llu@60m=be=rRz=p9nXL^*6>QiZOBAi}cT|p;oPR8tue@6pIug0_-e-S=UUvINmNfNl|a&_%DZ&qKgdswbSO&iCp-FBfSs??~42{re+)pyu}}bvcyz*7`(!pe1Io`l>wKza*^X!GoZHBDM<&Vgk+D|CBrHv=pyLSgw&4G#9X=#su956ferwvSop*s+d9dYC4A8i0Kv2{$O}iu)fjpZGy}c?lVjlkHJV@=T07)>-N{!YR!oD~hWV@w6A@$HN|4HBWJ}Ur_DBO#`Rr|!VOWNv1$vTZ@~c790q|5OVFwF$eh<=3ONv6ND7>=+EBlbiBd=jr<AM|#A{G(RkX!|=Si{=&&;Twa=cF+ey_h};ITzi|BEv-cc<HN%KMXey;5Lb<AkyWgjMs`SG-OXggYnu&qL>6)5_P7s%(q}+KF8wGQqg&M;PRm1URhANY7lW%eVwklJf^}aA{<nMrvJT<*ms86p{2t|P}*3!3lwk}oN8yiu8e^vi|4<I(L-{UEC_?t8$!3s6mf^>tlCi)zieh-2LCPL92n7bVT8F)DoN>?GY6UN<?{-Y$>p;#RjIPgM!8N1AEC`~;yUwDB`fJv4?SEJ08&D1qC+klR-?7t6#i9}GCW_p&1+yFhg-lv>Xci0pYEgxIeQ{Q23jzFDW(+Z&=KN6B4g|g*i1CijLT)q6f?@o@&trpytBP)HKMcH+D>_W@{sNw(cXxV{&@B)s|*O2Q>oRX9OaYFoN*LvE5QoZYdPvBM^y8YquS)!)fzs0&6!3C(>6M>Wod%yk%tUIDn3C*j+m(}(sNzOC!v*X5~J9VB?qi?q``}8FGQnOzS!X+-Dycl8D>;LBc7DSN|#aNQt4Uk$@nvM6@NB}XcYFGK}A?)GW8a6r~tooZ`1*`Ij#T~)1m5MX0y2-54u`8Das`41+bjA3nRdKcwG@>!Gs}<gUKwXYVJS}=A)!)0C|v6ArAa_%trG`g^zb#1OdKriJ`n}<asX0tf@c>pbW0-;k*yZZ;sGCxr5{1bY}CwtA#m`$iInbU99ZN+Xu8R1@{ka@RA|xOU#I?L0Trf%uMKPmA#{eyU||O<+)KG093fex;8#3j82&geO;Y~wr(%_G!9tG9&unO{U}=<oUNJ+6jnB}n`5M7tS~h2R^_!YB@sn?rluI`zsp+cH47K!Z9CcGM0T{m38i*a9}+44LAt%Fjb1KlbnnUuYc_>3<YXn9#)E^(+gTxxwB)QJRFFFFoGoAEihC*S^kt7sIVn*u>_Ftd^*)82>>Oay7=xXGI00}`7CMI{Au8jn9-^NXW|T(K&X!UDk2I_9GXLmP?lTBv0U(jP?D4sC22t~nof)BGmpEAB)vy9TG6rhvR*25IG7gX`Kc$+A4<&%u3To=CBP@_<0*ZiuI8>*EXCtn{C^AGw%*yMe&Bz&u+PsiL835?Mpg(l4HG!c#Hz}}6UY)m>7L7)S{+*@iS<n>WWk68{$&G9{GCbF&b&P1y_Q>)MxI_nqhKLeGKhAtT{;p@?x0$4+!0JGCmJ<7*+)>QzshgBLVOi3ECL-%JJ8zd5u14hBg+7p#KA0*64%cK39CET!G}_>wu8dRviX?6Z83@vfA7pHU0&yz8jY!<P4ws8Jj3A9QZ{U5XiXQ}k63~I6nq|=2cnW*R6e$2$6fc@|aG(M8a@st(;g)9*7uZ{|hJ@EgKs6m=HQz&yc0b?Y8u9=)03ruB<P3KRFUT>>h*mM2axjpSu+(NVUQkKsLWNA>TISuD(GIbQEUHIe>hz45Ij5YE)YK@PVJ-kC(3CPp@V@Pl2b*NAc6Oa<54y-3p@f7QGPOz*u4CyJcDEbAHWHap^(J@xifbR<J(^kB^)rxu1bH@6P#__`Id?CPQYmpmDsFVJ(3_|ZxM09Qrvf5<zpDZ?ju8s6At<b4^ePoX6T4{%Rqf4Ae&raZ12{b3OOUZ;26+%(Yn|pbbh!8Xyh@-XspbK!%j+T9t>rn${Y{&8?__1aWmPf~pscisGMNN!kQAyE0WdOIRl7m7LY>6(<*qk=y?0Y_r?6<n7F{8cpe<C`Lsd(TS5(gitGYPS1EO*XMzxh8;T7>HVWA6P0O%Z`kV@!g(bbyq<HW4rN6P7%3~g6W-v&CEpwH=~Jc#-YtVf8u+v@q8eg4Sa%5Jt+UTgwM{Zx+@58UaXYy!-282F83@?9J%(d%qUCtd&PBt@n^JPv!WaM{HLmKT-uNCT;0*cV~^U4VI`Q+s&icy-~-rQI(kD;d5vlkphRi4HuanIw$V3w|XbIOQ6Sd57K7`9GQpii0qc7($n9fPP>T6a)uPFWBz@TiD}cv<5dhm71jTXK_7ov=j`88x0x`Q#Big00<B`S!LVp#M1x<3X;gIdlsB*pgqU72|Qg6RilmF%%L(@;Zy^yV&QZLT1!nk2tZ9+bY&@vTJV|x6S}Bl6h+e9ucZ2V4hYHh3N_LooN<#{_n_G^Oof5@OTY>;bGedFuofCSriz&z?LIL{hw4F4^gAouf9}i^0Z_StT+Nr|o@h{A4Ah<KB(d7!R-AL@b_kZ2EK?V?;Vc^iN2)+Rl$ff`%jzF7mLxwS?F^_)QbMqNF1Q*+uIjY<kcRpNg#Hr#%=G9jgez?VbM?S<uh03!6$pZIDREFhWQ<xZ!AI1F@Y}I=RUgcehA?%2luP@g?@DBiF*q-Hw=T08MWGm9COB(`3>q3d`h)=BOTRlh%0mr=Y#@{o6dgdY@(OI>l5hx2;!$VxHBvy9uQvc(1r7ts7+_B{WdcfCc%#z7e#t1%;VyF?dS}2_GXbw4GLb03yH3jN;9GjKuH6+(Vh16@%vmRj8)ZXJ(eMSO<dERH0J6-*g@6j&<e#SsM2$uZ8NcR(2<%me5lX33%H8P1c%iH}s$MG=I3;px(iw%7r0|e=D;cn1mq64>bX2NpV1SYMCCnJjZp1C<va9j(hSd-aA@;OHx(ku{IH&R{h_`$o<ES+JAZbKL{lFfP3<)ts*<Y+%6hXkAbU?DR9)V7bNQ%KJslebGyWqxZ)2HB|%A^iT4*}F3y^;p2rw<|?)gwXL3?Zd;#cJqV3Ik)AiB6Y=?sH5o$Ux9nW$)gCIpX0WIf2#Pv0P9^<NJ5m5alQWN-sh*I~5UOJeyY6TL8ljiOXf>7!p#RSya5)w)*xm;-kB~eITaTpn}rr)z~RBTd3$uWFs<CLPZc-=#OsMh4680Z=dO|7VbpJ*Ycr>)CZ3CT_n9j+DeT5!b+((aD>o=yW)~vs1=Cc==7<>xC48@4T?7Kx(*rM0N-18U<C;M@)Y%uF<Hrg;h?Xk<Z4m|>~Z7Ogx*?{3w$Dkb;ulx$LHXTGB7KqBm}DSC@BztgP#k1G<uNXngyWG0&&<q@x)fkC|rXh6puF$5=@Yayrk84uSjdgRx)WJHxoo~^y^E30w!=#9L^2vsBCYKNyq^jo^_TnrO(8XG)0C&7+@ELFY}*A{HBYErU>*HR@$Yi0;$c!DFVkCrI=gfRuVOgy<@6SHXb{4cbz(Z??F7=QoXeVXrC0&O{;Xa1>@s`F(PrIUjD~ykGcy2pCT=+u5z-t#DV)XM@*C;Ap}&#D#C@#ggH$Y#HT^qQsU5Bl)*}ZLHU?kARo8wS?q{w{Ju_O{1DML_vEYsDi98OM(gU2v8Z}vICAx1)#k5}te9^d0ER?>x`zsB9=`^TW=Xw~OgovdZJxr0A{3FMjV-nOBQtt#)oREM<{fk}UDw7Ftqw*po~}3PQfz&QDMUP6dc);BtfwCJfMPf<5o$?RFl*A16@H-f!5p{K8ISEiEC3taaV{IPS%8p1LV(JTUO{XR=uhWG4<{7&5nv8HPP`FNzP)9xW;greWKO-(njOPHkRgge0Ad_OlFc}+MchGCA9ItVmTz@AS~AKYPIU+~P=i(`HC3I{<_kzaa`3^XS-UBbbq37W-u>H4Q^<vJ6EtqOc-|k-L+U~bR5@xr+SGNsGEuC-P>bmp<Ma}p(9)t}(`B(lMS3-MNrILbowf}5Sf{hlNEj{x)-qy&H7DeFZ<7GahKs#{V+@n42)+Son3Dem1W(qfP2dg99XJM92E2c7*-&c&_7M*)DM%pafTJ9h2V?b_(!JF_jXLre1UhPpL=dg%P;+5$hK6HVX;&#Me68Yu7+mcoPWOYMk9s3Lz;8DRt{Vxa096CTX{-kEvF=Fs%J2a5GVTuucrN${@BpmqKX~nAZE8vE<Xg0j7Ng)vV80TxJD<0$ZtR~T%_+oYjV3dj#$32Xm_&4e&2q(z4N8aloOPosI#ib~PKtD4KOT%B%G9V%Ob65!VmudtTO@-47YBW#iZZj;5F}hsPH0xlM0vSaGv<=$HO^@&{MLx__4?SLWAUiAB`t0u`p|NaEvs0r^~ri23>pB1bYf4b)%oTD%biwlgk%D=#PEdK;6lyrYUcG1dM)l0M)894Dxm)2h={~A?qik!me+^;eEQO0Ra4;-_e7~Qync8nPvf$5gh6_3%u<0L3Cfic*MKq&@2b%bcAszvO+9rAu0y)0-X(_e>yiMU3_pl7lH|Z8esMML0;i%f{HsQcDVPiZkOP;cr9+o&2;e|f*hw8II=$m0s|xXG0A^Dbl_Mni*qCK>;YE5wMZgiJBJ%>k@~chYb^aqbPTw{x0TquW#Bf<Up=Gs0m8w|5G2-{nbVgVQm8F5;SYftT8WxUFlvZbq_Uuz5c5ZR}{u3K<gs%;vdi$obIJOl|jwv#4e^exL&R`7zW#r?5;EvbQYA6M8GNgeuJclM1OMB{x4US+ZXa0!^G~THd5a6g~;b+rebf(265J!;(n|{*Y`C4G8lj|0jOkB-D(N=MC8g!p#m3otw%~wMRQ1kS0rK+BuR$gbgi=Y#_?CwV<o^hJb(dMjS5r6-KJeC@PbBJ>;9x?{A>MSxrKRTM6vhdtioL{Uk+b^jR<>GY%>_mgX!s-g6{%pC<xqaF-yknVkxb8{M@D;D_qi;U`+Ku3ybLP|Bsq3_0<^x_V#+)jK*G?VBcy=>1Rankfl`mW_OiR46-2CMD<$ZD17SE%_tVlB^*o*{E+O;_j$Y@w8h0dq<Mh;k%#wwfNEH%TaG((bae|B*cBdg91HMreZ+o)WI-m$Mbu5qlGYYvSl4g!m8a8y@iTB2}N11+gt4=L+KLp_Y6G9uAcc6m>EFoEyoWeo>{{T-NE?a{}ynF4Cps<RGyjSSyuY(M~MZ5d%gsUh}}K}biEDFCDxq-eqy&rh{|5GpLIxn0Ht1<*=MM{V7l^${p{5+YUD9a3muyuFPQC+(Wk{P5&HQ%pb4l+0>GyFID2=`Jw1%)))5c}7aivs35xr<Kf)ai!=^Ethu6oj?#Pd~oKZA{yNeXv>u%?D^R=KW0zGO@Sp%1NACsUQpom05IH{qb&Yb%(X@ZAfB4+cn|X4E3(CR0Svuzwxu-^5V-caM6xtksrbahg;ia$@G*`=ycxsqA_dVqwfIS42@+|C7Y0~m?&bTQJ@6r{hUmE0G?viK_C0VBvrLE#^r?!c$%(`FrUV@RE~xBK21J7M^V{60|0Co_hlnirqg@Z|t~sUkV(MuP=2EzW2`qn$Y@x!j=G9lCnHzmb1BhIF&dT8s*|DU{NNzgeK(=a$S|iQY`{a5KYr=!jfAhLw5^jTm{ayMu)IcjK61I*`qT--WjjtTt`m8lK`sBtUNe}Gi-udy-VRkAwC7fcN<f9(QfS$@)X|$7D6GIi_PT9i&5%VR>o1g0(pdcg!|Fk5kj)OwWAL1AGPRq}afjBay5P<Unpp8ElN5L`?S#{cIErvr;<K$dLz0n0O;89>OxZ;37$(mKj<<}!EG8WDuYa0cKz$naSxP1&0iZ9Ggf&x4vE&BDpe*OQgG;qN')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent

_LM_START=144
_LM_RULE='cow'
_LM_MIN_SHOPS=1

# Causal livestock allocation on a standalone production plan.
# Initial animals are preserved; later planned purchases can use another pasture animal.
_LM_PARENT=standalone_plan_agent
_LM_ORIGINAL=copy.deepcopy(_PLAN_IMPL.chassis.routes[0])
_LM_REPORT={'decisions':0,'cow_modes':0,'sheep_modes':0,'rewrites':0,'extra_harvests':0,'extra_sales':0,'errors':0}
def _lm_decide(obs):
    shops=obs['town']['unlocked_shops']
    milk=sum(s in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for s in shops)
    yarn=shops.count('YARN_STORE')
    if _LM_RULE=='cow':return {'SHEEP':'COW'}
    if _LM_RULE=='sheep':return {'COW':'SHEEP'}
    if milk>=_LM_MIN_SHOPS and not yarn:return {'SHEEP':'COW'}
    if yarn and milk==0 and _LM_RULE=='both':return {'COW':'SHEEP'}
    return {}

def _lm_router(observation,step,state):
    route=400+int(observation['player'])
    if step==0 or route not in _PLAN_IMPL.chassis.routes:
        _PLAN_IMPL.chassis.routes[route]=copy.deepcopy(_LM_ORIGINAL)
        _PLAN_IMPL.chassis._future_sells.pop(route,None)
        state['mapped']=False;state['mapping']={};state['original_pickups']={}
        if step==0:
            for key in _LM_REPORT:_LM_REPORT[key]=0
    if step>=_LM_START and not state.get('mapped'):
        mapping=_lm_decide(observation);state['mapping']=mapping;state['mapped']=True
        _LM_REPORT['decisions']+=1
        _LM_REPORT['cow_modes']+=mapping.get('SHEEP')=='COW'
        _LM_REPORT['sheep_modes']+=mapping.get('COW')=='SHEEP'
        for t in range(step,719):
            action=_PLAN_IMPL.chassis.routes[route][t]
            for order in action.get('market',[]):
                if len(order)>=3 and order[0]=='BUY_ANIMAL' and order[1] in mapping:
                    order[1]=mapping[order[1]];_LM_REPORT['rewrites']+=1
            commands=[action.get('farmer') or ['PASS']]+list(action.get('hands',[]))
            for actor,cmd in enumerate(commands):
                if len(cmd)>=2 and cmd[0] in ('PICKUP','PLACE') and cmd[1] in mapping:
                    if cmd[0]=='PICKUP':state['original_pickups'][(t,actor)]=cmd[1]
                    cmd[1]=mapping[cmd[1]];_LM_REPORT['rewrites']+=1
            action['farmer']=commands[0];action['hands']=commands[1:]
        _PLAN_IMPL.chassis._future_sells.pop(route,None)
    return route
_PLAN_IMPL.chassis.router=_lm_router

def livestock_plan_agent(observation,configuration=None):
    action=_LM_PARENT(observation,configuration)
    seat=int(observation['player']);step=int(observation['step'])
    st=_PLAN_IMPL.chassis.players[seat]['router_state'];mapping=st.get('mapping',{})
    if not mapping:return action
    view=_View(observation,seat,_PLAN_IMPL.chassis.cfg)
    commands=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
    for actor,cmd in enumerate(commands[:len(view.positions)]):
        pos=view.positions[actor];tile=view.tiles[pos[1]][pos[0]];bag=view.inv(actor)
        original=st['original_pickups'].get((step,actor))
        if original and len(cmd)>=2 and cmd[0]=='PICKUP' and view.shed.get(cmd[1],0)==0 and view.shed.get(original,0)>0:
            commands[actor]=[cmd[0],original]+cmd[2:]
        elif len(cmd)>=2 and cmd[0]=='PLACE' and cmd[1] in ('COW','SHEEP') and not bag.get(cmd[1],0):
            other='COW' if cmd[1]=='SHEEP' else 'SHEEP'
            if bag.get(other,0):commands[actor]=['PLACE',other,1]
        elif len(cmd)>=2 and cmd[0]=='PLACE' and cmd[1] in ('MILK','WOOL') and _shed_adjacent(pos,view.board):
            other='MILK' if cmd[1]=='WOOL' else 'WOOL'
            if not bag.get(cmd[1],0) and bag.get(other,0):commands[actor]=['PLACE',other,bag[other]]
        if isinstance(tile,dict) and tile.get('animal') and tile.get('yield_units',0)>0:
            if _is_noop(commands[actor],tile,bag,view.seeds,pos,view.board):
                commands[actor]=['HARVEST'];_LM_REPORT['extra_harvests']+=1
    result=dict(action,farmer=commands[0],hands=commands[1:])
    stock=_PLAN_IMPL.chassis._projected_shed(result,view)
    market=[list(o) for o in action.get('market',[])[:10]]
    products={('MILK' if v=='COW' else 'WOOL') for v in mapping.values()}
    for item in products:
        available=max(0,int(stock.get(item,0)))
        sold=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[:2]==['SELL',item])
        extra=max(0,available-sold)
        if not extra:continue
        index=next((i for i,o in enumerate(market) if len(o)>=3 and o[:2]==['SELL',item]),None)
        if index is not None:market[index][2]+=extra
        else:
            free=next((i for i,o in enumerate(market) if not o),None)
            if free is not None:market[free]=['SELL',item,extra]
            elif len(market)<10:market.append(['SELL',item,extra])
            else:continue
        _LM_REPORT['extra_sales']+=extra
    return dict(result,market=market)
livestock_plan_agent.telemetry=_LM_REPORT
_MP_REPORT=_LM_REPORT
agent=livestock_plan_agent
kaggle_submission_agent=livestock_plan_agent
