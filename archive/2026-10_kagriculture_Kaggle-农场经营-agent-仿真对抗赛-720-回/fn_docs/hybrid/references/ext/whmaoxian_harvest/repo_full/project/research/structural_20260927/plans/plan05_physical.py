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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<U2j}ha{MoRo(GAfX>HzQY1S52HVsnR!Nw2_1KA)zuz7Iu7UaK&D{}74+^(*w?sJCH26+-OGrISDpYH1F>R<l*;$MIJ{cnH${o<c~x%m0@{r$zK&Bed{_8<T9pAR2A{Q0-ve*gEs{@26bzg&Fx@h`u={^{M1uisy6F5cYkE;cVeZ5}`V`R?}Z$2T7yKHvSYef{w7H~Vjv|8W1qcKh?ue<^(N>3=pSt$g?9Pal6iYD3cA`|bPphZcQ){txf&win`$q??c5ubT4R$9M1F{`xR%A3lEm-%Cr5T6x?*{^8+e*6(<4*Ms){^_wjkvtKTLy1o1G!{@G}zjoXE562(LF^20QpTwshT%9y&dFlG?n>gl4%e-d1dA**u`1t+M9nZy~Ipo{ep!@Ci?Za<>+`hm4>0)!~57*N;9Ir3%-lyK6@q7G3w`ld=KmPsellR7V#1VsI_|u2wJtys0y>a_`-P8Nqk6~4=mopxZ-RlqAJJRcHwD<3Un`G6M!e%kv9LM`GgO8m#eoJi1{*%Y&*XMgb)~5?C?eFS!r>$%beq8E@XVUkXOMN+T<a>|ib$IN>@f_zpK0myA=BUSm&>Qvj+OJ(oD|=)41djO8vitn2@(i=r<zp*9DUWq*$Ki+zGr0llaKamx4kxGUdcv(eReA3+^m<QEc<teBae-wmA(xc%g7lTspBuNsdUM~tf4_b6;nzQI?>@YH|L&hZcRaD0Gs`%!CyyTKo0X)g>=dTYSq__3ixLYf91eVpjutNbAzG@^ut}bDbQq{-zP-EsIXg+7zFR(G%Wh?iUnY-SY`@1p<nZSP?xl4Bq7?>R2iLxJEWKr09hMuKsDZV2sV`qJBS*vkxRlDBCC25UukqP(hdw>`sDY1buk?_mDa+H)Ek8ES@vTdX4~skwJ=-}eD-Df`e@^f3Bz|AYr{rVnKZJB_ZHF~`*0{&~>+$~|ayA2@39HSwB8DvshB760vu}75%?p4b026(lk&%6TdV+hfU$CW^S@P7vF}uz<+08d<n>;>x8Jpz~3x)76BLLrV2cOwqYb@J1nIj;5XxfyXf(_?&RW}}jHjPG83~+hO53le3+-W#}`tl&;oG-6T?Z5jEcdvKfZSU^>;?4JQCzd+{K@xkT;OGU-R)GEk&=|C3HP}UyBcjIpS1b#>U<n__4W2v8vlmM+Osrvm9gnqm&vMWmPpI$}QWQ3h9ymv%jjKBruc+lIsbz^DJd6cJWH0|pcMM?Xa1&(+)Ypv*onHCh4w-$?J~*eDmxpJ*fSt!|&S$jqmbWuI@42nIm!`>*698b7kg;JJQO>;;twFw~vMXG_X$8OGixHla1NI?k2lG(EYHoIMcY1%F9G8#x1$i)`WuWzWX#MfU88J?uQUR9S8jiI_i21DXLRsN({(f^THf4{X5NR;3;>-;hu52*qFc;oRqS3%yIlOgpSCMxB-YTzrXtN$330(n#$QBpL$>Y&)VMw+EF5-u?P17*KPz*7w`37D)#kea#u3x9oI0G~U2XRhvV{JDOC;BdF6Feufh^{_17|&&Vp4SYun2a40scMgc3nUw<4v+-kNn)^#+M+Tp4!|sgNsK_42C|=9%DtFp>_4%At#xe~t%uPB%c<bYG21m7a$xXQ_vbX<&a!yp!d_jw1{L_yu`j{>jso*Xze8WUE}1(<(1ruXC}Pe<Xukz)0g?njIae|Lo-rJ68}M=r$lI=5d<PiL2zFMSUDA!rX5=HNIV6U)M|<GU5nCbTj|ln8ZZ?t71o-d0XpY(cY%%v|w4*2U`y9KOnC{O8)IO`xobuw%XhehPSUXhDGk+L<3yFV)QLOpkDg7|}LQNcl_XlW_S)>fVx<zGl4ROL_1i5X8kCv%kuGk7l$`ER}WB{Qx1nRo6d(Z=b0cSy3y#VOT!JE*RRrjm2ECHPpTFwmuYFuUXpaRk57VypzQow5?1=bx*U`#=)7IZ9K_m_p~b_~8a;n9{`ncqCQrDoX%bB@|44EXWM%_JYE*dc-@Aa^P=M4H$yShWg@pKL6r_Vbw-5YF?%xq1!*+_%kfm}YBPM2t%6f#0<Q$%VEzocC8~P_$kb3nI17z<Z86QEbp*Mcm##{ByHEJ0CXE+lvZm0BrcBFBHvQ<9|-;67>dn;CH_(x>>*)1P4?c5_IyeJce@oJEM?+^}oET=ENljtzoUzCK{x>)k6IO7>JjBPSKp;xaA|4=GiYx{rlV7`z;IFEI;5D#yYaUv8{e;8dwW+tryXQO_zmqASww10JulV^sF|hGar)<7?i;mQ}g3w8v!c>_#9s}aL9&I1qbH)aZA3rUEhr0c#MC5^(#lmpXuayfg2Cpd2+}@&PqTJzQn==fIm^v0I4J(YIEF1PRnn&`J){sDT9Z$o-ES@6o|`m`2-QF%i*;q1uNK?$FmW|6S7sx^E`&aFtsH|Zm81!>mwaLr_hW<&~?(lL`Ij4Tov*MOOI9?$D_`S13lz=O}TXdGNF4X4Oq{eAA}Qw9T=G%dhW7-^bF;xkdv|=cSjb;LwE)hS61)lND$2?B*9gkX*j}p<bOyG!3>d=f<$3BU2p1c9JrI<g*-}Q<PwqKo3rHfMAp!_jLbLwbSNZ5g%44d+-kC}o4qSY@Tpds@p{Ws^2RlSfhh(UL(0Ib7lx&2+0Y<2w|Y_3He(wO1o6Ic?j8i(7z6}hovhh=Gh0r=k9do4WXjlSms8sxBV2L9(GH5&Xi2;VO!(6E_=gcpAnzhm6w}&JWOFEBSYQ@`K^+oD${!=0F-eAFDNzVOCRd3xZ>p>ZYV8%-IY6A!N<ma$rRD*sOFM28bo52rw!;^V`vj?FW^msOGoT3B2OBz1ffyvtl2;Yf7n|M#@K|)OsH69_cB`X^A=lkEXAh=F3-Pdnpn-#I2J`f`SXMv2d;h1WXdP^D(^U{TZj8W`_pW1-YtK`M=^>+E-`>JKVbZd~gum97aZWYECo|9M+1B8DNIi&V7l^LY=w+4enlHGxk{+AP+8=NJXphGDkI%$a76Oa8AMIkVGc1knkh`x$VJW@WTIgo-Q5L_WmLL<<JjQ%ce|!OrR0mr{^L+hvH6eu)EIOljB<dlp%Y4!{P1$#b37$S2$0JhZBxhb734OEw{VZt^6F^am+^VNMB@L}_x{-oZ=57P!!stQbCx#Ui#HcYsI2MPsv|4q@?<uSEZ@OhEvf4C<=yqs7SQlt*<rcz(iXzcxh08lyB<RexPp`4V$hK9|vj^l1cMqHLN@;4ay2~dMv8#)Q&R|65a$Ct+IV9fWFMF_zX%vYqCgda!76plmp9)48HDJWz*fJA0Hu$=90htb{sgF4CKmnIF1)H-<C>x`8OfhAR$x3lmRs!8Lvf1Pzas7p}9{@pvrj{vhPz0}4)ZGpMi!=&|I!QcZ+sJz$!LeS_Mday0^rq57Nk5f28P^4-1ciD4qMwd-90{|!B9T#9b*HY^2y!f9RwmH;Mv36f*{T+dk^Wq~-$Aro_}k0GvRNze6<YJ<RG_3pbY(?Sv{9m<GJhu|O2jjuji4}n{Y+A(l|s#S$jYaqS~_f70dvmW6{X~zxSr6)01n>)!O80@W#8tfokavIt~m)P<;8ri5~>f4`nQQxmdZVKui5R5YYzyir2<;Ra-a}zDzFO(GnEk!+VI!*-lV+(@w!-g1GrNjWvyT06`_W)J<28o$&%Z$q=Hpxl_?Ow>Kmi0REqXko^rez0jd;hDD)SrSz4C)$Fa?9hNdi3BCCrwGSx{k<7`&^Su{KHMIbT~RNYAab(((MtYb|SvaOV7e`C{D5CkC-PV$^OPf&%aD^^hr%6qC;bkZ05`2`;;B1YG>4;d5C#XdL)^767G)=sFUJSC0O-2qRetb?9YQW0oOA@AtJG-Nj9rJsC^v^dH2o%4sUYo`1k^kFPSH<kg1_b>lhp*R!)v(%94s=c&?ceFW@f?j);$zv|~O=0tKI15&Z0_z+c^T+=KrHrp0Vl0@KmxaKMJw=ps6>nHRqb0MMAr@(EMWZb-ddcX8PxXHv#fMkRsGjt3ooHS7Tsydc;xR-LL$c<_)greqshz`)_FcABMwRL`cB+05am?HnFOBY;n&@h*u{um11kYk}Q<81NvuTA#b;GjTX_lMT@ri5HAK^}qQ-#cGm`e|3k<=6BR_Z0M?Vs~_$PCm;dc^jzzGO#;W1QGS)8!GWnw`Z<uX`C|CT7C!U~s@oqtVMN;{(Ska3qU!G(-a?=5*Z|!qyIXbB&=B()87*jwEJ!5_mEpvI8v?!%lwkgfJ=cdk$#h>g>=4(AKuGi)?f$5&*wNCmRdwJTBC4I^A<}XZ`glK~!rruNq42RtZX<U4z`SAze~`H`>|?>a^?5k$;+VV2WmeJHf0p{b#gd^XZX{E<ycUH%)s&On{j!5t)%}R)~zqoN9ph$*go@$q@R#dhEPli(Avo2nuBjhIO<VSY#EcIeI}AY00@yxF4B24rq=%8$UWD=`JPC6xbM3HYHg75v8G-?X2Wf+$cIIfcB%f=fDs~dDYCqKb{MEMV$u|I~qs4y(02z<0Dp*#TbPf>^vAWu#zUypvcr^?I9Gg<=m%ST@Eu^oEJv1u5?ai;0n*(m13ve;N`+Q>g?bGlEBnOy$lp0&*@{AT?k1OAQa>lc27E+Aye}0OB8a1i%AmmZmrZhN`MGiA*l$+MsQs~8VPBltiXW|)<m-rXHT8KV8;p6artEuS7Zvr5S62cYy3g?1>6cT(Bx4#l5<v;Gr2Bp86X4*A*BFez;KO<$Qq?gXm&s;X5US~pb_y#f|P^`Y}*r(1f$Vm#^_5jF-?RYyZ9<xPdRQm5H^OLM>h((B0eb-Zj3k}13`)iXL!!($>B=urS&SK<(;k^Bvcuf))~pdlkvXiOrfXNzpB-7J6NzvFVTj6sWr8#fmlhb+6(SfsHJi6A&SEZ>`n#GN=O?Qsg}V~$2ZxQx&L7JEV2ye6(pG#$89Cd$V_9YDf8Z0v1}bU<kZW?^#jdEd4V2}>FJq_gS-^$vk!DDJa3VAJkKyU7-lKFAg!@v1i7Ato{Y|k;`4mC3<D(F7jsE?MC(j4JEm$b20d6&>n<NfAI*4^(kvRu(dgom07->oX2lU)r4J(?bd=uaCmH(sGvaV%=2wi`1l$C#(3%wM^2f=-BBHQMJGb9||92y?;D1g;R+3Bn^0|2>)`vF}fR?Kx4)(#lkbPr%gaNhy;RRvj+Dwv?uMA@9+bZe42&>Ey&Q(_&7Y9@sEj1gE<%%-aWwRowfd_OzA6M3tRsxcwsnY6%=`N)@#^}m$lkl~Z!hjELA7F@8b&pOeL<ShX(N@x8S^5>IqrlUS=|BJ%W}Y9OcxWQDlslVDHcuURs9uMg-H<I+5@~Hhvyxe#KrcK&Nu&5>V-+&X=+LRMfT}p-WYt;1(^h078a?Gqhp8T>9ipHND3(r}7I&|pn*0J|i6N=b5Fu<ZHX4pP*nU~I3QUDJ1<u;&G4^{r9T}QeaN0qt+BpUrC%_U(^-fFPanuzL6$FY^9tKUIr>HXbwv#53@=Ly&T`q88PwU!J`L<$`n5w9rR)$V$=@e~w21Se*&hHT^YMcq*spqXXB_(N{H<v##k{5Dax|G}!fjsJFV*t(p+(RflP`gBzFkDGL<)R5>po)<|0YR$f5h#^pH$?ZWp+#?uE&^dB|CD?8MR$!z5$6O(oy6d)T=qr(cb4J6aq?caivt+4^H8-!3cbzr<kSu?En|xaYewYGSzm-Y{-roI50;$+J5Br%q=A$pRp1yLR<h&?f5_uunb9QwB>@bFQ}DM^UpU>e(g*BZ@|Hj<OJ2ycLMvhccDSDN_Gu>6h=6VXXoyLFR*H?SW$&zzZNI*f-y6!B_3CZ#pm;X{gVtZ6SGU+4d@`7Z5O&Dn;f4wlXR!=#Z1E*?mT}f5r>mjDvxh_!|2TSnQ=#q)IUtmvmR98fSV_J%ZVbMDPJsZJOiY8(6bds^A8HafatUP$MJNONeA=RYQpA=1WhfQ{^w`61ViL&dPl)k;X>u$oD*A39hp;h}zpcK<x@c~iaHsa@ju;)NwxJ_VKO<Sh=Vz!f9WNkUmr|$v4YP_Q^}K|D=;u@B^3!l-`$E-eZmV`=K04AgNF5@xGwiA*h1w||$phqxsOWEIdEoGJmoI8NFeKfGCdz^+5%Gm;89O3H8HA<0{0mR1`s~$6fuN0)IFej;y-Nz5WRFfnK}cVI$5MHmSjZOg$BIh{mZ2na#U#i`odM$CTG?mXbxBDD^aP#9=SWtTK-<0ICD<1Q{${uK0h;^-vJ<3xSaR>Vjvs)GmVmzelyMJWV*I=;QyIvGgvQ>>Y7zoy=bM~@mb4GjgBkar3yc)8C572?<PQus2cyJuQsD6dZAXsevf_dqJz}`qX&QwFf;@;4SNg)&7q1FN7D874jTXW<l&K4~b0|<1AtA1$yw2*`oUY&Ne`NIMuwZS(2QFkoBge2;FueAv&_xiZA_?Fz105Th097#Ig%Xd_OH|<Ew(@|-XDK_8DEm3{x<(5IaNdw0;n_r&7UyGGHB|b%z!8F7#4FLP5Hp9u;HT_t37yW>$}~?2r}{kKH*xy|CfyvsE!Aa&mIP=IsYwSeLe>w&O)fPWl{lb`KgEEt*cCu7q>yg|YbWtjnDVYwmuQGylI?i84Q89rXp}<%!>0|y_d#kyc6>Rgw2}4T)$1Xv%8agD7AQyqV3InNB`Jj>clfrX(jPs^P@*}Np+xa4Q}tXbG_z(uk~5iwX9zSvC4>0gG7+4lOc0lGl}{g$@ZmMQP6DpSF<S~>?x>z358-goIN||W-<@<x4sWaEI450E#xAi?IW@Hg;cp)26Xe_;(K|i!&zR!q7Tl&OjzS=a89G(TC{L4Kxb$AYpE0X5FA?B7$Oz)@9%vq6k!8nmMIpt}zZEIPVuz}lP((%;Q>@CMR6L`<3T6_^{JN?ES);jM8D4cWB<d0`QbaKKU5O66Wel~l3jz_;WVfBfENVg@&?g}5sNyI$i#bo?nZ$8Nhp7gmDy4ax7zHW#YeP{-fC-LKaDqT|L(Zoum<9F){Z1szpw0~J55&;sQ$Y&mI(Z>oxs(Vy$@0WZ)gi5=RA1J>YzBxD#4Mq!C2~S)R--3DgHnwvWqH+7vB_Qo`_G13XoiPpP-kq7XLD3!7=PO@6-JJoN?xVl<+(LXbW|Fw;`PP%91~H^4f2c6)N8kGW)yeXsWLd;O)#96%~&p8H8WjKmO0H8t~F>YJ~L=Qou+d|n~AwHg=8&eIhpl^bo`l@4(=std9}9u5>QB1iCu7Wlg+%|Xgl61W>{D<w9PtI?(}oVreNF?iz@zY;=gyN!&Bh_ze=e|G}B1{JXa-v=fzh=KDw$VJ$XDNb`Ew4N4Eb&Fb)n78kLc|Bpol-z1xmuuUTr~bJcxqEn87z5zb6Sz$hN0l_>y_4Q!Ddc#pemEvBlgTPc=Q(A^az5J73EhEZ6$9-I+g$(jb_9aNK5Fx;kqjZ8DADf6XhqL6<A>jXGwHA!fRi3^jcV#ZraP&PhRa9nk<*cmFx5s1YxN!bBM8kLGU$s_2M##!xpJa*}Ba2%AmTWxp>FXLrZ#rV;vkaTBSu3I!A=3&BF1RO{Zc?aL^+|{+2a`CC$F-7yx`F5^23uOwHG@bbsM=>ro6mQ>s|18CXDBjC6nz)6*gxmB*<8|k8kZ93FG`2MF$klQmuuY&X2v0E(huNB3!L=EGrm_Jl5NT?8Rq|v@XSGYed$AgVhnC&le(<D(guYQL<+D@qbyqgv$_N`nu7TqySWMfZKoWFH5K{z$Ym(L|DO4+Xj-XTBEV&Y1^;IY(UDcqgGbkm2nv;f9($Q4|jDo?ER8o6leXffvG+ia2F2hsfTlfc(>iik`O7;X4z&e|4JXXs9q;&wJ3vp2GTd^lWMTC-(@TzCu7naU+0cCcit93!Gu96ThG=pRoXhC`;_u+?`b6i9~$x>5WwkE!-BJSBmk6o6%&n2SY?ILTuYL24Mcr`~SOK0qy@OM}Wa}?0dl~GnmO0-S^njkNQTnF)1T05q2Zb;{3zd2gvQ#gPC){Ur2rUjd3ZGaqN5H(2D=1ub&bK1zPJ`rfb&QUI|9!)L6H-xcA+R(+WD(gd~71#`0Jd9TbtXPO#QJ0ryV(okJ1b@uPgB2TQf3C3km+Csrv@o8JSLfn1qe4uD0AB=NlB;{=g8y2owZ7t4yjX)ChO`wd+P(Y{&;28pKhlR#YO+WaljXlJ>pUXFse19%@`^6Uctr+DBBPm&$Qq#tMUhxE%E2M>#%JITmGO!x!PbV}G$nVq{VCC%6X{V=?WLM{&5DkeoL4)k%S`sg-3LzlEJ9fhAL@}~anz<3q}-RxK}v8PT91=NN=6J3kN3lZwJ{>n)=LD}3fNk9A)B2o4J`M<IG1GC+W))+4!v^BSY&MyY^^b{K4KW6M5j7sy0lY+irHctSi1$AGe+9zw4Nz7GnFL*dr*=)!8d@<R=O#<8C%2gjYOEeV`+0myrjV%pMht6qVmyC&MKxP<)u=CF*F_2<Tfs;1nEiSsTy=mRECSSfHhOF$*M~FQwTEjW@kXASJu$kPtOVc7nC+Iwp-7wJwqY%U9R3m2V9)DgWR0tK1nn3;o5g9l)2gc2;bp6N+6XP(Hh~lWtf!r0JcIlvmqcmd1?yc1NNuVsfH#7{9nk^gyfp5s$7t$P3F@P9ya8g?P;;P-C%}|U%Gc5QNdORLh<#!802&41EI6~l-Eql9XIP5)2sw$Ta?^DTk0o0-P@JlJ@SBNo}aNWHYq*k@kLCBts*gF9}Y@>E)@oD$HW<-DlyAT;u#(|KNvX<Q!Y!pTf#%Lty-R;B01I~>MwEU&*xv+`(x1^==``M6~!?AnS^`nx|jT@0DE0doV`JsOfR0cULf&}hjZYHsq#2%u^W%mM-doz5u2J-jmqd|PKb>(o6&c1$hhDIPt|iIja0fNu%a-D(%W$d57YC7xv&mO^9pP0sO1zVnxPV%g}6*bBYLQilUe8d0B2j2uj2rX#}~m~cQVzc5EM$#QKRW-hP)_cPUWFyuMk%O$e)Q>e35jbO0Dk}XJw}uA6^W|D5%~D`ad^aMOL|nRUc)%cC@zp?9>oySlGq3=#?nSF*@6o61sOe)536Bz=GLd%>|XVW_Vgu;07*Ho?lX~nk2Pt;<l_L<1qUacZ}WO7Aq%ed5}m9FQe>P*9qv*b6%M+B?wfcu8=c|<%n?y1#wHM`_iQhDXp-aL$-pQ5E)MiK__9$=Na=AKryW1T3>c4)$2^$*~zjA?k?t3Izgp3lPVCexuD}JX+2)CXx_WHGS4ddYf}pRT}~DGr}ik%WC9Qa;9Naz6OKFLjw9mR0Nhf~Uy_n<01m)+`TAe0eh%MNmnG<cNgcDJ@2F?wqudynL63>Y1&tMgFFOk1Wes0i;L9vO;OZUbI8^zXfk&3eN7UiZ=&|xVF1r*dj*D87j`XI66BAp<Oy~mDFlIa5lnP(?vKlB+jwU}<BBx(DZY1Or3giTcD=})t7+7?m8kqpmDXZm1(7Sx?j~WqXnBG!Rtp+hu1)1g`*bwxU3Y~bis<9^L7HcKRwn~?c+oHo9&bl(D9RnuYf$d|V+0Y~#B_(0adR3yxYz;U>hXS=)XqJ;-I?1w@qMbkhym@uuR@O$E$}t7^@$*;eBARnuL1JW4&8Z=c8m0C#nbpIQA+I1ZWiXX;QzPLYru=c$366zy60xZpN_s)vOHj{})r>j2gi8`pR$?>i1{KwUg&$PNv|=YEIzDKs6#(4NMCzhNjrnb;#fbKa8fLHtZi+p=^lhnjlB|V+&@|+U<eBny#cCeWqG*G45ATR9tt|=CO4>#-HUh#5RrqdRJcd@HorOG<WvwEzR8;@ZwtWqRxGo&#iSo1}Bp#V`X$^zHMn63m;-HW$<1%QDe|nf7Dd$U4pUjk~Az7LKQ~aD<&Nm*LMDe!+%Ipt*SkHYfg~#?`)eqy)mhc!-WZC9VA=@UWT+bjX+dQ47Byk_Gd2B+}L5D#ol8Ft5-YO_TavwW<hk~Fcj{_QIMQIW88LTQ`0C$UMwG?)d5MeYVs7IJf(Ls}+L~Pr({uICjMrta$m_>P3O?<engrmSASSbDHX$-ZP=xxk|?h?*paP*Z4Yh_la7}qSx$Z|BI3$E$e;SAuN)~Y3WF;J=!z$gJvby+ua6T&QH(JuEcXHk{VZTYf7uw>_mqX{6Qo;K+-y4VzW^^7fhW(Ac_V+}F+cn)^+8$aD1T=DC1pS*OzSSDvD6#9X2AYhW6x11=6#y1*0R9UVm627(cmy0<*%6z1EKCQ1p7ELK-3c#gwDF}rdayusaIi*lUIt!EyN0p+z5FDttQY)bTm<i;dKVU({<S#Ru6#$GYwc|RZ^@PGzYgS1RYXMxYz5r9G=GgnBp<E89R<nwxA0CXUSv9JF;#jdN)i{-?SFg%SRcE!r{Y<H|@Qdh?qf64YGUP@?ix}@k1xL-&RUBUtr|**iHDMN5B@%R<==v|a?NAO{DSys!TcrbQpteSAP9QpFY7QkUjU?iTFdpv@*s3LnKxGTkkQsNX$Ey4$xCnuxTfisJsOe-r8S*JUjg6^TrATC+J?FGD*|_x7fR_F!+F{WGO50eG@CKq0el}e_V^kml{%RsHN`71$)JR(CTtaj+aaF5seG#=|z?aJCnb|i`+JH&z?MR*QW4TJap-jV{qC*8W67MvZvC35kSx#~waVWq9-2l#cigIc4NN5TaQn`I54M7i7n&4(-5mIOYG#V(+`x@Wb$O5iUTmfVm`;`rW{RoyHP|`+5Z}3ZWQsW7%lPCl~;w%Wxkz!s9Nd_#ZLna%6l#jA8Gel=DJ88d%uD>2!$0sJasbHhJ$8i%JW`%c})s~`SHCDBvGLp~`R$;ZUBHT1A%j|2wGzE`k-Eju&b1g_;!)ce7Oz?~I`1Qjx=c+-u-fx9&?w67?q1tesG1n91A^f^R5nkw>&<vY1YB<Bpo%J%;q8G%e8P($~CVcQBTQtS9q<*ur3X2E>zwHZ?QZE2@u2ksF6kX0OCSE+CBJQvJ4KNzgt7(bt^60Qf`+!>yxjDUJT-BOp98R~>h+BA3P1?Jx5M{CPWbu?PEUn;Tee&8_F>*e}QcAtycH;m<D*kK&WGp*RC~tTwUF<purpy`d6M!RW`7TCR7vk1jBC450Mj6(iX|erTpBZhfSWztUTp|pq9J*9uTcjmg6<6A@aCS(6rGV-<Dn4MfT9vNzB<WME{5aRAlyI7%%o8xCj4I$)nhcyH&{s_zx{*X7ZX|tast_<WyQ)I$Fq{t`g_GUw9w?b*Xn#n)@-r8m@}qsF$}T26Rtq5mGr<!TV#oHNh|svrlQ>*;x=C-?C&*I!HJ(Z-ZL@2vL&(BFQVf3bG|4H)l&1oTJ90yj3R{yGcVY2@3}924*CZAf9baBWm+(B90<0j{FpGt$3+4P50C9L~t}KyYvTU=00yx;bz5k#XPCeA0c$o@FHw$FVr7KX}Ner=KtEI3&omPd}2O`@h+c)3{YzhOZ3KS`;z)Ej60^=_#^BJ9|#ZM8(Cm3ii@6cI-a?0Z&A1fTDfyZ8{&;#+HauQKr6x%e3-#83mz>DaF;kJJjd?#mqB8F&sysIRaS0x6OsQw8#+J-!ok&bQ>HzE!L7&~zT#(L*5j%k%JN0gZZziJa1DwPEu;fnZ2JY`alBTuZm`G?0ZCgeIXg4_IbCY24CR|dBOaDH5>_VJ(^F#`*1)gT7FPtM13OVH}-)lR`t#+0e1F;O#~=9*O1I`rCqS@Yd|s7uQ}aLVV1l#!?uREbp1hf`>k=>kqgCtlLcgc1&g!xGpH52Yu|ShJOR0WVQmMY2hR`qGHo=11;%bd38)!{?1IWNI?zO9?4XB$1M;8%2M5_*NF6^A8f5^Z+$<sodV6$JR(f;tr9<<b-HYGFo^CXmKazup3&t<W$qi(ezMtGKvcjLJ*YM-dh#e;MY{7R`StydF3BHi@Urrap&m876*ow=LYixRv?4jYU|4^B^?_Ba$nXTnaABhdRm3hLHmhAA3vd$hSp<h6Dcz7+Y}j!Nnndxeu!)3?mZZJ&>e$A^s26Qvff$j`B&e5fkYTaK49h~IXz9qs-%3{wn}7Tt;DyDK7^pf-PeJoSvJOFJ6RpdMwH%`1Os|W`#q)wjnmZyol9Oyi3kF3XW_)w+-JLV1eLc^tFGvyxO8VZBt*ckw7R6VLdgVXOsl=5D1V_T!qU+dQ2uOb>I4(K5Owg~Y<*YN%sV?it7>6!HaX8{j`mJ!NNWm#2qhVH1A2rJ)2TvVvZfsyk1s1FA1v-RvT9fiOVVv)w2ZlI)bQ2|>BcdpN!mG35sW@T#;$6c(2e$iaUxN@bwd1X8{cVhRxkvQdZns}<5}^%{Yvv2Ju6k$NaYi*&(-Yg4>stRS8kI({Vx_Z?BD')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
