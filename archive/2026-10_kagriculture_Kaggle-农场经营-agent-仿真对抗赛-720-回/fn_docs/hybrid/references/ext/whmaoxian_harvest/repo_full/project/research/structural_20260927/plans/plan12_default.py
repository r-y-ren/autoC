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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<U2j}ha{MoR=7YtdXeV!6Y1S52HVu7burUO~KsE>vY#yAv1^Mq`MDos^+tpRoea=w!W}h?|j_y6*r@Okk`ltWC_}5>4{p(+Tz4*tUE`Gdy|Ni3B<;B1K@*n^5pZ8zffBfq&zyAAQ{_FnpPZxjq_~)N*e|Yo#?c0mXi&uAti^~_EE+4-B@!j3)kFP%5e}DLHe|!J$%cs9A|Ka_2`~8or|5EtFr~kP;Y2}+&fBN|2strkd-|yePJ+|oc^S^uZZhs*@B;9=Y`=%*>`1t1S>!0t3?Zd~<|9ff4s+H^h@h^`rvwp{WyB)N*x3BhS%znD~;qKjs?>=`OeLC#le^`Gd#~7}Md=ejjusdne^3v_wFXNaeE%Tc3>UKMC@$pYXx1Nh*bI4y~gWm7=ukU~R{r>IU4;PnL{%}2x!+L#z_dfOpjo-ru-J;EV|M-7@K6!6^M;tLYhCh5*-gDB9%^UZ(+n&C^`xsW`b~)qmINW~NzazcQM*HbKaFcAhQrIlUo8x#NXYipj>$k+FJbm-<{Q7)9jrHk5OZ&Td-DxYEgCCdr@tO2}=2Bk{9QoeWyv`hZf9~Tu!t3pkKRv0h^g(!h9vX-3nlBIc*4E&Ci`T&DXp{Go*$%@!;l1(M<_5C{-s!ltzmCW7v=^@)d2GVNuht)?&op>P_yFeDf9|nk$4}co_MR+1kjK8dd;50(>ch`}+`s$q=Ixt*{ygG|@thgRiCMXNB(^Tm)9qUqo@AR>+D+!8klRirL({ofVMFq-Pwg(YdgPoO7v-b11?};CqwDT&A9t0!|Mk1OA3uM1y!>$Yz4`ZA23A=zV6YeK!}($GW;QO~!mtU;f?O6wwJE1&V8skwUU?jche=enreWwUiy*!&9&V#!4eZSD)}=vl8psB8I_96+TO*JjRsLh2Zd~-ZmHpv2Gu&CsWg2-dwH4}*8@W;c{<PoS)8b(@U?nvn#xYas()?69p%~(pSR}r2R<ytXp0a#kUWi1Jnikh$q!<ur@N*ykGq=9XS%kxDTx{kWwaXJ9y^PKB!9rx@a~YIr0Uf79l;HaMP6Ximv1wC!3O1bARo!?9U^N;|@zCWl-`&3Zr%uE9(*gc){Oj_{)cAb=;oa@w5BqoT{_M^7x)Z>ik5I|#1<h7~{sRCVv}H5cwY32d^ru$<6F>SFn>QTC4W2v8vyYbWc47?^cs<tQJ<CBCC$x@8$I(0b&7ot&ZfU|**`rO6Y{>R<a8C_&P&}-(623e#c6#4`J!JDm<KX|Xjd%R&8I8Q<?aat~Zj<hXX|Lo=2-qZKX_yw2+ahq6MGKLywd`8gZ(8oH<pa1Z!5K4TGlF(7uO%$<W*3)7A7^(tMj!4A@?b(+LCf~o`t@b{&=doQ28$D{#AS7ayP|o<MU?1>F^8sGXeqVgl#POdioxKDGdE<+vcVV}W)KJlkDlBg<Q9Op%Ih8)tH(z|A7EpI4Opuuk4L{<+eW78S{+GXd^tTWY=?@WMo@mugPLLgu@U-R*p<%)DtahbCD>9nMw7tgfYma|SY_>dF0=I<1}wn9ELP|^N(nB_Y(VB<muz|+tJDE9<?7xJ#5wWJ81u|+W(Nnd@Xh1%BG47K(>UaL1Zx83Rq*<dp%1JeFnpVv^_<QY>OMf`Q&hXd^`OlFr^uSgaDo|EU9^&Yj@JG%9x>o=dTc`|FYJ68>6&j&M_^#-e*BYk_n=Wth!4x3DlRc$Z31L*nbvsBNFTY0G=>u<+gH<#=!P{tf~Ni!p8ss2`m^D;O(d5Zr1PxjVdf;g7XP-4WDqoK+r~UOiXpp@##tD(n(LkNCbK`NiP9W%ZH|C6ig2<}8@I(kbxm->@C509$FG*D1{O*SN#;vtH5$M#7z^oB8*ACB$n}|OkAg!1ny6JD%(>Vdel0VUq#G8O85n;S@b7@a(aMTeUo<r{_Hc*68_lnDnO}j3fX_3&s-e|;=elTsp8y}BZyiB&X`l;*12D8b4@b|F(JrBHH-rMyVI?TNZxN?01}OcY%`FKfm80Fu8=7Kn<G9V<GJ+VXG|zjl(Ogc#qsj{RR#c%u(O?b0S1`!Hd)A#OHt6VO-QC^)bMtg1-f!gB7Zs`ixU81GP=>`8Id)o?Xj;HCvHQ28Cj|^ZaCO8XK{U^elTb$0GM*Y(|I4dtep+%<<X&5IqJu@TD+c&QD2;*HC=@^FtK}n?<|!^q{oA{{_j|@DT7JOIt8J+N(l+$N?cGgYD;eGqQdkz!k)CwB5v|yaF7Sww>Dg>hXFet!FgVL`n}ii7TgBICoQe$DP*Uf>d_Qc-S9jZ+5gd>416aRuboy@V)8>LZ4_tb3%tQJLV&Ojf%8WaZ35<Z)6>!(rZR8C74gqkq$1H(!Y3#{DrAP!cicp3^ncF$qQOc7KtK0Au(?kSo3C~}RTnGgnjFmMwpJ_<VcQB@4w;^=qoSTK>DBRr1f3S3LyUU_?Z{t7bzo<8z*z$Wh#bLeA%x?CCu~33m<h<yaJ7*h1I?Hxw9aW`Lpwi3q*}Tm}h0ut{hM$WC8L=bebbcXqnu5e*FvxC*n59Ho^5|bJH0vwO6q-9Hew>oz21Ge-$X|+(i3%;k+j(PUT{pW|kT9(I_fZ~4>#hM$V_;#Y$RRMqz$RE7Uqew<-E<x^hgb{f0{orFR4Ok0mpUdG<u1dc<EA_&LE$Bpnx2D!Rp_zspc`Zf!k*4tC~=$tNe#8zX7X~eAd_no0=V(@rg`5<?~ksgqfTJ)YRLEl(FY^OR|<opGismGAS?X>)NgSmq4CRfFKW{V;Q;%lFJuy`TNxq0)Q~Nt{<45HJ!8=5w8-Y@u)4y0V$@d_!_YXzLf#PSHGuR)ap|6g6Ak_-k+9+R456h>U&YE6oHqt>5<2OML)mF19}EQ8<-lA|i}w30+vB)8R>v-ZyST4L_Qv;b-u~&)d1*<E7PtXagPMYQ6<4wx>ePe+C<`R79?e}Q^2fp>xYiy)Zs}vRjb<B}@%Agql3-o|%UaRYkD;Mnx0p3Q8el}@lSzpAu~ruLSZ!Rd{Y-*^O4icE(9GhY18yaXWpRD#x`BYU2(1ADUlQY=*bnABq!bC8`V{@Yb@$Ok_0>d@xT;^MB+`Ijt2ZGJruB~2<UGNBKgk;5GBkWh7p75>B8SWdYE?vNhAf~<D|@CKmTD=QQN`(~I}_K@X30U-j_P8%9FI?JO9&mqfV!4OvII$uj0xpGSm7IWF6SP#KEHa$k#Ey7IYo3D>3ST~4<j`6tSX1srTiqAwE;-_Jwo!pGAB$Dm2@<D<e7QPBA+z5Yjoid6$y~S;~p$J=-fS3P(i1Viz9JBs)U*=KuzNslbk+2+eF7QJq$}~njoJqfIkEU0z(XjvypK38-Q(iwnhr!?6eW$$9hTinF%pzkpjZQ%cSDUnA@JezLz|*9KX?Z$JmZa1MsNd59Ix8e>OPY1F{K#-;30bvY7xwZU?zl=UzHM1RmWuOOY;W2QCLG`&R>weZB)C022@-?h}KVBhoyZxsqKWDc-mdDr8^b>8I}gHpDntU5BW7`8b&X?vd{Uglgm-Z0|Tqbpaiwl+AG`jLCV)GdSGCQQH-thuzkuGWW}31w4#0Uz1a`MWw35*(#>;qh*R}Mo?;0(g9p!p+Pt)5N6_e#uP}<Hjvdj8wEw{Ih7@6EXzd5HMD2c=JbSiMLkyVU6$K40i*)Cr(R|=Jrbqb81cJ6i<tXI4??O&IA>W#S1^_IcDQHr3&xTZh2vX}_f2HU-8$K@EN)$q^3%tv7(td@L2uP&QF9&%O!J-Sue#MaC`*YqIsXsM;(q;cF#~nt?9~SH)!8AGif+?&?MswOU&T*2kn-ZHVz3gFf!}Q$WdR69Sr|T2tBEy0t8D~9IuhuA;4174%t;=3{z(TyE#OydL6uHHj2{6vYyHDaoAlBWV9{7Afx^^4N)MM%reT6_QsC@qi9BS)-xRhW2gzX7thn02nY;cEAYQ|@ea*H<o6ozLlP1NxB)YxZ|2M;U0?Y)k;sIW%IvEu#7>Dt(D)Z+{Y`dPckBd$KloI3tjk{z*ph7b3J>MsCK~Zi#sSF>_r0l~0nZC$n$0Fb*jVcz$%LdhQ7ijbi;RQ62h~Po<2oB5{gR6y+7#aTI0hrU+R_u6ZHVj&Mn~|v{Z^SX_B+!7ykO+M@tWHw5aUCJb-i{X#=C!*6M7QmuS=lCvQ3X4Scyo`gLmRDW>~q2(h4j%UW*Zc84#jej;4mwY%+`4$;gG;Sx@>`!d3GM?SC8Rp**^ZnSg|yhuu+c&rl=Fj2$NgLe>D{X*_|B%0V2O+z(<XhaV?0^D$Rg1Z)9I1DgulTJG%xFN-Hc8tLP>}N0@6^Dv1#9r5g5OlPBcafd*CP&2pfLLLrCTFUNO@jHN_ehKV^AqLuvWpJL~N8WA}?MDUh44z3p^faX+kE~~ubc@oV)UK}?&F2eL@nOi3+;bbk1a2((>2?h;}sI4#hh|Jnlt~Cg^IsXOrcGb%(V=x?DG_4wEg%!LWP*%b(y}7y-CDIjpGQ|-KabozK8<v3}%(xS7VFGomyRv>ll3v@}YhaW~Nw8!Kv9P=I&6Il~dR%~llPwTdTzewh!%m{191EHuo;rsEFeE+XQM>ShXJnvh^cgWsR%7&To0sy%h!O0T^@woO)~P(}sYo=RfYq}{7Af<Rfn`WH7M*EHX+Y_$O1wofWtpGfs0XDz{TE**Uqt3pSYPg>h_G<%PnZr<D?=2hrog|50)ZZV0(0Ezc?=0j0q6*#X(EsT4EXzbKe9H-bxl98D_lb3&WC-i%ykK1E>xLjc`))MiXqz3vSiBtVKO0&kyLBB;1dZ~iJfIv$qktqADsYOWR(aQ5jTTtn&&rop*#**Cecl<@yv6YEvpy%&7h_?Bb(6N0InO?SOg*nRy<*o$9OgzF@IMCoXqj%qlF1$jVM^^BU+{RjD53J&>?5jKg_H#WkwLif{<eMIFq-hdQdFoV4rAQ8iABZt3@bIml8aU{X!V*+(u71_gI7Kg=%S-JdT30m%}(N6!Vc*AHSVz906e6vpO$0QyC4oN}}7Ee+?MpxUQ){6_``wcx42MDIr2^%u;PX{9n{6AuHFwvaGx&a6k~HCPK_3)X}ugfIZ?IjPq~#1qR_my#MywM-%S!ivl-#B0!QHvR7whN0d>N8wryz5Bu?^zt-(1#Hh&H1Dq*MxG!q8U(eNQ=OQ2Rg!CI;VM{dmQPIOP17@o2MR0?``q7Jum!>>V@<5*-Rcc}aGV?eyF-|W|Dx~t{!ushH4m-z;^oc4~&*O9x8WpF1xV9i&GtfHn<v$QUK-re-g(1m5&`$xLiE1Us73eiz12CYStqeCok*XY~<P3ncDI6(_Ma%W}7ljUsQh|2#nU?i2g6Zib4BS|DNWjJbaJbs?^oeLgeqy8KOR*L<JKGWfn6+A%4ml;Bdxm@^!pc%}Iz>+4fs(KnMpL*Bsjx))PEWUlWSMoDKOIg4Ypgn>y9yg@|4|x+M@8YGm?<SR2~WD34bKy8sr&27YIt!Aw(kkHfSbnjGk{)Zb~HwbO)EJmZ|KWU%>pVbJpZhmiYG0qCF^U1TCq!i$tvlE)CZw1aWX>JNe;y~$@edsqL3u3!jFZVGvo~C!l98<(H+OUv8e?%Z=B}*)&x69eG$NK@adJdx{|N>`FJ1f%E@cNyTIXlT2jETn&VXpQFCo_{f1dCWZyEkIj=9+%aF9WE7WMN#Wx^bPWeULmvi_Nb1k1}RVcDBwS$J$-AP>xOqs*YmBjK+IY~jZXvks47&wisUQS8IWi)1+8LU=#IrYwhvysYE#2AMUH5ZZ;XX~kPP;;n7iicpj6j<^+d`~zXXg9!%k!=d1S0UkZk~K*M93^yCNZLmkhw<9uVop^<cZR9Rgis2s3}!x7V(lanB1)uKCqvy8S7+3ITUwPL6iy}3?Rvl2hRd(};qtjIZb2-u91P!SXE^w?j?Wvj`?ANtIax=(GM9MQE=THw+@Tqytj#RkVW?9Vga^zRyFA{Qa^u-gMCCZBHp4>OzI4G5b6<6d$Bk$?UT8?qXF5bo(^m-al_FYM&YogMVyB6Of}tAo^?Y^6xX9?;Elr(<>KRz2^z!$@F^(B>Z8}uY7_iGate^>FsJR5=v&9x8o`P*yGAocDV|dJy3-S@r2w*WSx+HZiI;y-FAb=A7SS*W{SOV^vw0Uk!%CU4;6&1{a7?QUb660QkZ3slPsymjJ0~ZBO&X;WaY08B@<&(*8IF&SnnRS8ishQqx>C9)WtZJbR-6Iy6_4Ss#Ht>}SjKOBIjlkDEK^1ASY*)nu^>d5n&#Im#x!q3m{nXE_<kHC0a<kMdx<rVw^D(L>$^Ai>;l#3uK#KPjSBNAq%d_Mpe31$jX(jP-QUN#~ydyWOZ)f%rWU4YXXcr$r9<MEF-w9Z9B$!I}(zfPulDjz>3UzTh?-b0E(oTKCsjB}zFF{;k&gZR<QIp3XOdH`c1GIDy5!NpRpfB6?tti_@^_vM)kp9@mT3V$c@rg7=BDM<F3$Spdnob@_87z}37$k$RJJ`2k(Su9RPwmJSQjSI`B^l=4XXF7t{@}wmddoC)#FRHbujB)~Op+3uc_wW`Q=?IBbq+a0=t7ySAyxylp#0vVpICX*au+4}>7?`&JkN>eBDNGf%E=-__20>{c-pO4Hv6zQuU&WuwlR)6TTnWbfb0=jzveuBQxTkG^dS@akec5WE={J=VB4M!q{qX=PI<Nl)FabkrIZy;Y>DPhPCc2bRjP7knC}7yzM0JgBTqsgbMGzybfH^vwQ8XQQk1FV%g+zmU_Pz_<e@bkBOq`DSOTvnUOs6WFD-#|W{~P6ll$tozzo_=U<R#!S*>qT$$L46qy{@7nu-nsbf0lWjV7Ol7q=SC{<L*AinX&xC#8Vt61@#{e;H0{KIA1{m9JPDTW%HT6YTy8?j``d$%@d~2A%|Xm%cyBSd)n!9o+yg$HYD*h{MIm-df4=s_!ES;{&X2mc&crb^}=ytT+`ZIH?xR+4(x8u%o36f0=A!K_w93?s0z_ozi~Zk|AS3xnZrf?`0xNGLo4XSt*rhE2~Ob8hY+wZ^^IuS@Y&757#D=b`EV8U4=5Ov}^+<Xcl3uV&+?(M>P})wq=aY#LqnBmFl8Lfv<HToS7FDuIN`d_Yo}uVOKeJ<0f@A3!hN~qKv|}l2nPSB&>C%hniH<aKk?fhyj2OLU+<ar7ymc2u5{Ej_xR_yy^(Mvr00gB834}|2~;NyEDm&C=kU*Q=$V@&6c78fr)G%E0EydOrrQ$LA0X~gtY6lN~=4I;g0jH*iK-ugQ6(0%;j`3$&=w~Bql7Ke#TuWlsBP%VA20KQlIfmWL}#W2xzu49wvamLmdbuPSGh>4-hF*yva6uDYMf-QG5%$pkKOI+Vrjrh_e>d?xO{1ONojs5)NErmk(sv;lnE37M#@J1!)9DP^iG7h%S*7<?*YvANEb|K5_gr;KWo+zcOHfq&7z6pww?KFH=Sd1sBB?EBSR`I}mYHIO+c2625j@N=o>b(44`0(Gbq4oc6EZe9O}RT%ukmScBOh4{w7WxXv2%{IxNBn)MO-u!>Gam}K#g6FRQQBOi``STe7a`;pn77QA4SIYg8_$tTrqTV?^=;||Bb&+TLIszp7dOR@<AuFC|hr{qR=44^geaD$E_E9eVS#K;P2OP6{i%)iU+BtJ3Cj1h>aB&ef8p3T2oxWJi7I7abG%~E{E@;0U!*itAfssfratSs11#ussoyXY57{}`{6tE);Fr9xZUuC~v5sEXhF0E0FqXGZl%<`qp1B`g^lx^(NA^b6{Q4|YwcQl3>>@VH!@($1IB?z>}a8d38zW?5G9M|BBTOV+0p8=a|WM9@-?nuC_+lS_IK3$YL>B1xi}X6UOdc?SM)R9bU_d?&b8iQ3bKIbR~5;24$eE?_O>3v^Zo1tw*aps8$*A&y20qPCYGVN+*Y2%UdV+n;W>%7r9Ioh@@kq$`=cttQ7hAcQ$tSEsbG?DyQ$VFZsH%S#|3Q~F720nJOArleCXnXjT(V4alAd})FaB9o`|2-=EP6juylu{K}gD9aj-Sl7Xy6_{EEfUioNZHU?QfE}L|+9EmR7J_wEVK(Kw+vmy;OZD(EW}r^_0;|aml@x(0&J!n<Ukg&4g>0pQEbW-Qk$}>=31Px6@D+_rRuH({T0u1<3|=8O>41zQ$>gUK#+^!nmy8JK(c}g3>3oW~X(ev1u0~lN8DYB}1t+{GN(T|NF&5ssyL;;aDa|^~JXnu}$1Ai4QcB5!)C@7LrLQ>Ey>n#TSU!<3tBJ1GP^#Nh*)!sOjLF<*zKf9vWm-H{LXehkDhR-`xJrvF%sdWowG*@*&;aCmV<X>D^|6&4VOpw0<Bk9uvbh1+Q;P#(ONa0iH0g=kZrc`<o8anGfu?I#+8_pnUjp;=w3Aegu}nGv(y&12f#jvlNH<IPU>Ow5y^}<Ete*GO#acyvr$TOkbrdH_1<sxpzIpTm>J=~_xTdW_uYhZ*DPos(&KMvP74uml`2=D)at@y0i%}5gVKR4L0KF-T{an@Z)k>5kN{>7a5wGy|9O6GdJ%3F7XZQT-Khi2fC&P?v4x5VP>M>258Xp2>GAc^Z+KWog0ek8iL4H!39akwP138*Nu>4m{MODH2k`f>+Oa^s8><mFy1%sA$IwL#9(hXt`z7#i}==74cP8l6W?H)c)9cmq`oq&*g+5k6vGQo9))#GrG-e(UQ(mI2(S3Xz5E0D9Wj!5zL8Ee{~4ye^YYtZaP2`AhCJ)_2o=3Q__66?2IXmwtO4!<NVj8KO9N6&dK`2mZ1<B0*Ceb~%1oZJ}$u2g1Hti7JaB4UT)tu#2u;8K1RmkPZTpxoDz*06Jd={}cAXx8-tNq}4WDN*n_Bw17yvJR_MX;n?5+nN^yvM>@uXow*_kaokWxU)(>Q73vPA;*@}c}_&<i*s{UCwUvDnL@#lsK!K<A&1#s8rljHFsb~v%ev9U5Dd$Dgi*|Nh4gg;#{B6FAB+xKMS-AmBbTaM>QZKa?9Xz0GWV92MukQ|^sTZb*Vl=qsf7$2Mh=%(lIE1MK0o6t?o^mWgm*<{%lhQ{5x#<rrydC~TT=|p8qOE!I({gjOEgz&%arrB*#CIu+F2U&VZP*Hdju$b^b!hM5FpEeAC?E?C_c0x(A+QXrs4sLK*x8Z9$E{lxEw80hnCvYaze|BW?ZB~AJvZBH}Bouhemx-LnFmmc2D0twxc?`?RukWzx`BLj@Y12QKbk^IJk%{II3Bpz-3>6xr)1V^~Y?r&LAPV8Hl|EQE(VGZ1AKW({`W~*%}6_h)vP<kP|8u;R>@w4i<z8(b8L$TthnplZdTBi=8g<XsjJIp0?A$gDoi}bsfL(%x$Hg1&}I;Xh~)hTktdy2w**aUfK2Uo0#Mg1%89%BcYMf${~Y;)I+sQ#*vX`W&GqUa@q~fk)_tA1(EXLSFJROrFUeW@yeN=tF7838u`Y7B{1JpZ>lE|;C14aXFu%EM;<4_Mu)nSrx+XU6f?BUO-!>U=s{Nc%KGo&2#t|Nb*PAFhe<1SJQW|XVo3y)^iFgACh+i$;<=Y4Y|7y&l90Hq;7x1;%3ZJv9&PORF&L@pqLjq!Qtbs#l&g14vS@nY=m!ZFhM}Y7hGxNKv74I6!$5T8z7Yb8<)pb&#wuI)V;iPYRH3@%&W(LME*|bg(-C(w@;J+j>aTph5wG2>TH=B#!vYE7<NgyZ@=f}WjSW!8`ry<J^b5K&4QUY6>j;Xc;H!n((CuEW)t8s5Ft<>nXnc+S4^#9ozrod8T5CD4yRp-t0T?*OhN54AN4R>(4j!!Hzh{M$?w97P{qnw>oS10Sq7;<U(&AoCK|zc=f>BDIyFh8%j@?cujo7@a11T+{9o!eYexwLgcoS_!lHBL2D6b%@%4!5~6=eyFiZ4Zm8B@;!eqbhBht9Z|SU)S<lEPOJE-4D5S8g4u`&uEGxS5`|bt2k6McwN_$hsKnL7`5E&p(3^5|=@ZuCA-%DACFp^eSr=QCvkOOJpN)rc9xFT5Cyr-q%Dh3Z=WM`iKIllWP)2Y2X9|$MK6WSOPLD0>D}SX<npCR0si2XA703m<x-nvSjN-2w00r(%WjFf8@e40zjehG7SH;Q~b(B0(2Kacs;n(Z)W?lz|k6ovbz@v+y&VJN2+xWeMRUBZ2w0ER7?*s3MB9njwY)GRFCy2p!TlLw<nkhUfoAzR%m<B0ySCXU}<m{t`w8vXUk*zK??-e7Br=JJiuZDJs>{l&RTXLkj4(%lx5&;toD#+7gdxtc-T0H>B(lf`5Q^YgIOj9x@0EiO{X>??G;}~csONGCXtmg_96qNAdn<~s@r;={5@SPspzW~x+JJg;I^UMCThWXy2AEZU)S_uCZ18Jtwus96<JadPt%E~Hcx32CQi92|J4w8G2C?<$Rhc6Je8(!SkQdUsV00i*)Ez095kV}?#!&Z7_gvbc~R!Rod{D*>$H#so>I|C4{E}6d7v54%?e<L)S4^E135xtg@`}JIfN_FVQ0*vh8}DO-mks|PAuf_?u%u_X<;RA8-U^0pz7x8Y?E0JZtjgj+cf!DK|C)i`B9P`X3>$vE{K#zi>*`OB#L~&Jdqk_-XZVJ!!{|ULgKTjuo+QArKyIDR8+#nXeltJ-GXW_d-{1#S4~_ARxJlbk%OvbJi_AGXqDw_u2qVzGF4i_dk2)b$M0^&A(}6ye4T=HXhZW{5{SX<zG!+GVDSLa^Z28J#(N2H=pvPNoRlY{$!x-LHEdtIsNqaniD-v<hTyoyWlId(C{2rvF%x?mD-}}64FPNw0p6>LXn>Z$vhg*fRKym86(}$MjDph)USVmoyv|z%e4sb7k<kLupR^xkrb<**mFQJiWY+n_22{(vPY5#WyV6BWjbK(&O~SNi)E_O3I1<0HOO<VW_!=%};Zz*CPw_f4<Ey3|?AMI<#}aY_%^WE%zcE)}2a4>G3=NadKqRAQC~2G7Q1SRNi-u(P;(W~`Ap>nD)4DYya#&-=K4S0@r;Vx{O6-^?`aJSTuHuUfdJ#Hs1*p-<tttWu*1`gBD^w{i+(^?2O#qUVOh1ROC`uctfUz(~(xpI^f4#_+OPl8~+8T>kzARZM&?$+GAj~v^BI}!<NfK|CA*EA^jIlW@SOsr{KA|XQ8L_0S9Mn2kt_bfUgtxa~2N%pR`9F5zSBbY6!3{gj%tHXu&T5F`x|Vs}h4iQla+kB!W@u2<fRc)&jI>Mw;dewe2glh59$MfP2dNdPQj42leO4g~8U-H!RV#(y5vo@fTdp9KUCB)%BwWxb;kqiq#3I#uLRxYUouW2{SNulGnQTDoQW2a(UKQJn*m|M8O8Q_=*369DvT`to9$}F%ap|PjGvRRILHG2Y1t(QxkMOrNC2I?NRH-ULfs%xt*xnNaF0}Oq#rA1bMvAuXE7#SW13f9+E<p~f>I7a?OyFl|krxWxR?%VL6tixuTsL0=tDbWN%8SPXvZy_j<v*s0&K|%_itd>55d{o~L@b5%ii{XILGk_>u*u`1;N=g&a4jpKz#+1TLJ^j^j<lSJ115l!%HOx5^9wL@)Z^yDcO)0=sZ(DwX>LjwsYwytJhK$hu1`TKs6>qBggvzNCBguAl@vIKgLEiJL;IOmWH05H!Q2$91{<dUq)5oBSjwufx{3*5x|Calk>T~E(tU(E=VgE;Bq5<r+~iEiPzA*wMyul`>~qGBV6I51IhhCNAzg;BZ*9H#GG9q^3Gqjq4(AtQ(CbYn$hisWEw+fV_^2EkvHbeN(g#snNtCskumVQZbhu5;^B}T^%peD#tbsc3LNXlUX;!Bl6HHHoOvajEVkWht%c=Njb3+<Ug8K)UdGZj#ppYCkn%s2Rf&jex&UTn7v!y0_$=X^{trejDwqw+geyLlj@-%IgN^~jI0SQa^TyjU2MNV%j!xQ-$tkWyk-vx(i#gn4=1dY6?u!B=>ONQBbl`N3a5`GgQ8Lv3lH(*k}mOVH)(8DsvU!ty-QYY6CtEi$wtOH0d@&*#0%F47Vc2?R69(S{n%dV2X%^udAucGF!krq~y0W;GZW%i9WA8N{}FNgfB)Vp$3%=YCoR^Dre#@g~zJ(v(#TdrFUqttXPVG|7OZ>Wk;oJEUG*yTYOh`~v^X5g6bmnsB5&eY9512>=-<BL-W#*9$PN-Yq^x-HFZmHt{Uq?^9|$l8g|WYV7!+0v=o>Dl2uyH%fMz!w0~Fmm|Q<&<nY(?jr&UJ$ipP;2a=%O$u*M&U?@K+9QCT{;2UF~8cSO*Ol~9C_9S$K!DlMZWn`9RQP2>w)Xhqr8c{HOGolrN%s^e;BS}1%z-~Og<3E;d4`7eDxL3^7#6`fuH^tUd*#3')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
