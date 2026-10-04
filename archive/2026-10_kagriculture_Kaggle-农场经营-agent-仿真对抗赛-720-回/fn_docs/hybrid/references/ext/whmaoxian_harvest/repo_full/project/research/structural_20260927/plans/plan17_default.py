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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<O>bODa{Mnm^B{JU)QoRjsdq+L&Tv3d+gJ~T!2n*vfU!P|eKY*utrh#@^~=bJ$b8k**w~YZ7TK?=URG6RWMt&e|9$bVzy9{Ozy5adPd{J$bocah@#*s7-+uj%fBDbPAAJ7tZ@>Qb?|=QT&p-cs@rRFp`Q`4%4?o=9UtC_id)QuFUVXZJ`S_>DhxZ@fJ%9du`~Bwb^S?KrKK;+-$ya}P_ot6PP5v->$kXQj{`fUt9`OB#$IXTKfsF0&@zeL4&F2xU=R^C$#}D`KfB8K3=Z{~$?J%;*sCR$+<xBa8$A`z?<5Qil*!|tR&F%|N2DRNhJ%5?>;fEg|9-qITd?c3?zO$?Jo$Y>MeKL&sLr=yrThnMr`ssh%Y~G(veEy=Q4?O;~U$>W4AGH>{IZkck^f{Mke7g<x^ToS6ybMo&pXBAm51adkA1^Lf{&?c*ygcF(4QysH(_zSIK0SP#zvehkWOitJauRcsyTb4GWltRbhfHX<D#<$i_<R`M>_J~%Txp>u`{C|+^T;1jUaI*wO&+{kMLYuayxls7=k31%ojY+>;lEzK*4uoiBZ)W1>{4=9diQ^7=2!Z8WWMEvHXawg(_Y}-<C3q2pNwDB@ZG0B@q@)bt&d-MJkU<gm1V0so6Ku3FWaqXS>y3$J!Zdj@OmIWk#qD6U-|Cg{(kfB`IkR#9-lwlfB5Iql{uZX<6FufX3u~B`0!KmE^?o#bcN0Dsp<D2Ph)rRP8Ni?J}bSM;0hzhR9>TTZpSyBJSF&irCWOML4>u~+?_07!DlO(UvzO+Q^zI@>*zs(ul3)u>t}}9?3M)^ADqd4z+j`+#wbT}aC{Cw@Q25T-1-ZVydfSC9ma$IS`BYq7+$zw$?BlvAH10relwLtix%Q87{8(9Pz;v<oTA0YuNKCSGq2JahK!)*m;Cf-lV3-?Ll|n;zYomX`J^%MnGac7*7$WG4EDcnzhcvMn4AoAw{XEQkN!Y310B;wFLHjM3NNza+<~uN_J!yt?SK@V#U?h1(Mo+}wEV~t+SBnYUAS>}(-mTR32!=6i%*#Ob;*%Ny~{Dzp7Nd#<AVWlj1UVDUh?R}1(B|OXB7ZMDITA#jJFQxhBofu<LVs75!b^o3-MrpbpoGI1OwTBK*(s=3PDgdo(~9d@Xm+pnWOpi{CKzh!{+hvFI`729gDFr{OR$IJowkqGw2|)^zq-{J^ndjTS?q~IsN_U8}vr7_g5yrl;B;7Hw)Hh*sIVkJ#uB53lVM@xY+TB>8~Ar?s<9a2lSrs$D`)&49h>k&++h0KM-=hKN`UJ*E%9NsGH6CfZR)f&9hmNob)-ob)8rsUaE(avSCMbk>oR@nP>h&g)p!hbvZM~etAei7DfWe=)P8`a`fkpe=HqZ%dM37XUO>HpthH=>^kuCO?iFtY-9oG>^HFCsqGm6@$rZ`VxYvgMhD+<y_~BW06o(9n5(L9>*AsrVF}8QqC;-XMeb#2Rv5<yFK4M!S-Le(?t5xKWvu<It`{`r*K@wUvI{yW4qEnXm7x0FKAVBW;2tffR;s53G4rv{b`~9=+pjk7C9wi<-W#FilE)Pz1PciTZpk<rNEtP|t_2Ao&_Td*3Ec+}vkVmqL>1=zQ(xk&-oN?e7w@9!@Y8wHIHaAL>Y(K@DO`#-Kn`>n=Rrp}g(+GTf~D@VW`Tf3Lg(1bnJw8}>LJH9Sg<OE95yho)B_mn34_HUBj_Z>*|jh3L2C^brSu0+NV_lphk?z1eE%zczsv#+Gtks#m;0aK85JI~4^<Cjk*w;D=~`XnO9&;*<!qp?7QVa;*sTM}%9Vd5RM|lL&x|s=Sw48{cfn_{K+$sb#0i16y58P06ex%6Ugk`l9vN%$JUPcflPx?59Lq77=}tW(OXHc2d#=S?V94c|nax6$9#!~UGtkK1Km4%&_us#S0$QLXE$2K~2Z(+~h`Z0kNjCk<w>3r@rVgSH0gW*Ep~RN}ugK#eFy4YRy-3{#3Cc@Yx_$g<`X`4+lN)FI@Nob4k{A(&ygeBg$kI!9cXs_PuE{%mjq<oqYI?WSChK&+MmzJqzx(n1h4wrT&(OZGLD5Z#5zdHBk&}WlON@7*z==vz0Ns=6_CEUNaPuD)r&Z=yuE9Kv29Up@x&W7@K${Z36}cCpwgxi#!$yhAI(=u{Q8fy_bL{yjE|OY&oJx@1I2JvD<#%f)Q`;AlGYubKVKX5T1n~oz6k<?iTs)f=0P16518`H0rW9T=tN1IugLRF=4bP!KcZ|k#WaO6>5A5o!2$aP4%@4gJIq!J-1(3`?TG|U9-?unbHc!v`$dviixPXW6V=I}z_4H6LAA7XuUG5I3OM_%ihK-Kw0FH$MTE(!N0$4Q>$Vzf)V2^Z#cH(g#k4131Ij?l_>Y?OnZr>5f0n3z*cfi82waDp0XuT?Q9vW>UQ_kb<g+&K9DjW~K(CfzJK(QsVVN^OnB|B!^a+J|3BsahS8!?t6h^W&&OS3$X`31%{Ce~@x`>LrRP=NjBV)n`vJcYw=06ssee9aDF?bMO{<$_`R%jtwXz$S8?nCm5aKG(^{1dH!LbkvI3xMH+R&y5f;cPyb($<ZnGs9b<dEGrfv=R4z)P{=fX2Uf-`89`wgl8_phGfwxUM)H9F3YI%HF&~k09DEdq2}o_@;91$M>nTm(okjl|_^F_Jo?q{!%O<M2#j#N8OLsY(XoC(VrBv3oCV7}6NSQm+10+B_J!g~8+*Ar>;@=4BoUIQyTEWYln|)8WhDBZ8)9V>iwsS#7BmZa_!*+t6Y_u7J8)soI7v0zBf64EWM}rjV?<~o?-wHo`xc}3aWE2lA;jJ$HBrmeut;Jy^QdVpIsZbUq-C;XVp@7m&H%9S2Q{V!eRIJi4)ywUAmm#^Aqe^A&WZ8INH^h$;VIV(<{A#MYRLo6Ax<NA9Lspu)4^~=yvYV{DC5-`qM~B>35Dj3GMCx$JVJ^z#N7pgc3qKP+-O9tm3{#<wie20Z_|Q$h*F0iVORE!>fb#`m9Ic=o48XWLz|jZH@Pr|x4X~RiPrw445TH3*&hv16+^%|vpSzkaEU=Q~oZ3hid03J^9u_Q^I#?6?B>?8dWvHKON)4T)Q&~qF+RkCN!%JkepcHd_XkxRp{|ersa$K_ZcfT|d8>NV7+*JeKF~e?A^qN)-c$xD~cMfrW;SCLP=hI)LiAMQ`osKBX&0sMyE624DqKd+H^d7pI+4CsO0q4D!gZ9|iAvZHJTAwpOdwlGiu6eCvLm)UBexD&2H(E~vylkvxx=A&ALHL_O=4-P^Y<H5pkaDlFTPet*g5b@3Q5Jyjhg6cHK7>PuiA{zaLvuqHxuSQW#@@=og%F-1m#Lo}FBy|7uF)Vnu1A!COvIe7>*WwvElvQj%t%7d3IL>v+u{8C?&0BSgE;V~)c88}N>(34?+cu()G@6TOA_=<GCcs0#r%Z`-6T?Rm1yhq<L8GT?w%h!{KIFKt3AcI*wJ%dz@2j^>o$p+8hK7S&pTuyKTOKfE{(6vMPRjA%w9qD!|r!>kIELOPQ4v46Sm)wNR@X>*|Cs0105rAk6y*bz!wMGO$$?&=apog-#zRuS$Z%A@d{vQ3S>3AOjf|4_T2Yx`Q=neCIsxxuLR6Nurt0=H&Kfa5xUC;9}`Z@AMFtyYEzhM{#(<y0&KFulVZJADK-I4oV9li+d1SjPSON8q%TQX6n+loa$z}>Re?Zl6DcwoJQYfm=z8#`1u~_=G;lE`uyx&)X+g2b!#eKj2%k$snSROb*|{iJSDcKp)}pHogsX&qouQ?0wi=SmvKBo+8H8hXUh7a;Zk?c;v}cQeLsi3JV6y||=~C~W`}vje5`rn~*q4kRCqVG0+|O;5U5IEHWHO~kN<kNgUSLebK`f6W4uIrzdC3Mn9___^e;DtrA+jdKKS;h2EGq4-*I(vF%~nqT1_C07k8(E+)2MbW^;Q9roMV;oV85{vIkr>^C>D)Hj0qobI@mmiMk%W6d<BYopX?t1$dYsr2?NV6Cn>O0`{u|%b2r#w21x3Lyo+Fs?ciYUM7OYVPNxOw8fusE5FM!P0GxFnaz~DUFK1*HC{I&TmrawkusODmQY3A@Si{0_<~LHDRe1|>dq${iHeK<4PB-E0LMRVdq?{AgHe&lN%zS!Fye!Z;=gO*>7`9MIbx=M?T2L|$O+rm%cLUU@Eaz}J_uUY_a%6qcwhVFnQ|zcleIl=Z^sA!uU6SMB)j<yE#}fwr4ZX;+w#2N+Z-YRkhK*UQ>r4OlAlplp!!45ixIQ~HwsJsR<n{X>rhwQDEf(@pTcFQqwe3=j1WCL=#XV7BR|z6qdo0F!$epWeQ6ULk6bbfpHz4ZvDhlui&RsE0113<hRQiayB8qXNe)05NMq+Tv!J8+_28ebcSD_HSfO`%4CMR#XsVqabezLR&-#+dDH18ORr+1%phfj~XYtKWbosaAa0n~E}k@UbHK%z&m?*dUj#l!lc`sQglA~79}{Bv9aP{{Lk9d06=T&7jp{&WPN`kTO+BZ`dXo0XAG(1MeFPr3h#1KUN7(<da;>1h`I8&VjV5^^`Fiai%#9C2~_*I5DCU<@QDgxrTg{dlp|tnT<Cc|7U2y1|uZ6ZC&-J8qTlIiU??qY7CQ4lOkMq2|muPT1|7A!szr7wrcY7;V`Ar4sRFtCc~6w_3F;?QTc$F@}ZE<2Ai8$C8(5xPz0yhG(tn$Cn082+rBSl=t-gi9i++Zh4T4P_Nl(z!~o?3=}^XT|qRcH7hC${hCaWjShhpmI9x#gJhajo(;IK1{y9d0tMmU6ao8o7(7@i0A&I|H;Hkjm5tYm4{?;0LHqz0_yoSys#-64Qn-1Wlty9v8dx)L?M~zeRI{GgIEa_53K5;HK`%0WO{c)nU=mQeVhq$&{!ZxVqSsAb7Nv%8GViN5i}=-k$sVv!XblFr&+cVf4GeU4g3GM<1w`<&a*Jy*deZ<Kqxx20B4pl1WaTnC>zwtYx<s9vy$dS<=#eACbZmF~9{?%?UM#OajnjtpiF)$UHY3hL<s@okVFAGA=nRG0PT%+vY`NS5IR@%8<4@&Cm3|$!vJtEW8#GCPIN&I=1cMN&6$sMYOnDZDM)r_?oS=^9khi0XfqCVSo$>VX#JCcS+&UtA!^kr<5mU$!%U@-BhM5Y+8DLQuuo$iZzRJ<`z{x$|%h=epg2@;Ov=qijPE#J$p3Y`L$;o1Dl#!Y;?+AlZF@SMfLv?P)mK`$@01;3s)CfwCK=e~EudFx9+ZxM;W;%uJYCq0QB>A|&0GH7=AGq(^(2f}8CS51qt}784uNYy3O0<yEJ4;ls32xx%N0&O@QM#8${1Qhga}L(dsSvOF_aDA1z5_)_s1zqJBRal`_}<%dft&HNvAB%a9KX8}afxitd|ib&7lofP0ta>@d?^^|$0)TXvK~~jfZ;2*-d9(lRb6A~ilyRN<Cp#SGlPtJ?bS(i#kg+hR!?9ZxJ4*#&n(|2jO1CxEXFf3kIMJ=?Vpxpl!8-3cV5&ZsTfv+g0!C($uoFkM;y)pyjFIcO2~ueY&i)RY=H{ehMrfk7o|we(Y)~o=+=wZLDC;dO%@g6M^P+w$Ssa2uwBLrpOHNvDcLYBzA<hACyJTwh3h<FQHB$(LQs!JCK7`cNE+0*oKZGX_xVuR12`6`>cn`dt#0|}){B-n?XKPZ91`nj6A>y^g3iZ+`p3zZn$}vKUPNt9Hn>HT9#f0}MSmIrWOZ1`UXvfuAcTEM8)uELffx2x=VW3JBi;f!ba^I=mbJ68BU*|FcdcD<YJe{N>Y<E9QSMV{g0kQbYE`@)`M4L5WConvo(nu;!f~AA#xD)D))mge31W0|bg$XbU7kMWUd7zC)&vt+hNZi=E_`UjR&iA;MUTXXER}s#h)of0G{Udo{rdi?X3b4#n=E<{-hbpZk!1R;<=}FWIEz=35yXM@vZf0r+O=N9zT)z5yi|m1%+=t{PEGrk=no63YW9j4J<9018FoyCDM(59zTi{bAdZ_-@5{lwJe)V8QkBvEt8xCSEmDO@Lea{ns!gU)v`>@ig!{)#?L0l$j=7X@TqH&mVjX-!T6*Y}$nx~#&*t>_08o(>8sL(Mv|`KGZ_AJov#zY30wLNx@lLaNFzo-*9>)VH2TV6FIn2R(DY-I8+H5RibWzzoA(8B?KliR>?d}<hSy4Qw_yq-lDdB!qF~t1=a$74k085E7q9+5?y<K^PO?Q{m2`Tfwb<&FJ05U*4Tb<zyNRwm4tNIjSW_b-VynYZ2;1(SU-M($3ajaQSObp7&+~Okvdd!ZSREvf58RWw4P$MVOD&g2S-+h;Ocpl2=l=Diw2`|eS64<o@^0GwUt5muA&^|<=CfBjY1!J;-7{QDLv9h>bT^7I4yU7N#Y>F1=i-lEsGoVJ22o?))k^(6m$fH2%QP4vlRkX`{C6BDGv2V2&0p2eaLg0N_GpIp8z>79k<vr7D<xE60>H#n|DUL!qzRZH;TPgUn^h@y06VRhUq5GyE6oXA5U^y-JV(UX&kx9CvUJBpaa31qTC#zxC__1?^7epqJ_9*Iy@WvDkN5lvg#bOjp$93zNU>_-rr3&o)BA^yrXcz$X;_n_eI=Tn<17%&7@|F`G+-%eJTFMnGDI<0W52UPES{?hO4Mo_?69}ow4efLQ7zYr#Mbv(`FiJKUPaZW*3leoUIrf|s(4((LrFN>WvxixSw|5lWAmM{Ym+|ByYN}oI<OC-Z$&IPVF2B0^9Z5@7iddGJXN4*78C6@{BN`EQ+H-Wdsvfq(FkB0_$oG&YpT*sx!9mG2?=TUkxZJnkWm%5-Ue*qcDkDl4awbLt(WR&y!k_|D_jO7$4gOa+Leyzc!sXUDlBv#=lvX4X^nrO;40H#TZ{{maj)k>brOi}>KuhnYfSCx~)B43%s|NMjjUXJXP9Ks}bE-izeQ{fmRRpWi3etF+2RsaO_1f<?GQX~C#6<xvhvZ4Sy=}@Zs5)szUm~o4o8sdiymoj^k7)P2-FQmtY-jrnLC?oY_J_z%gSFz776RPO@X1c^YIW*J-!QxnLgkKNf`A^!w?iTqBggh?qUV&PdiK^1$V)31gb_OSR^qoU)H*?Qxezxaq)B1H&S6lg4x`KIi~aC(Pj7qJ9UZc)G@T<mktk5;5@JUs0StbM!QJ+@Ofj<o>XN<9(nk;(QFUwSQqle=g*H@!X~`a;GC2i!n^vW9xZHGw)3B{;P<hn{X%nXrg|W$6gK4>ivv{iP@M~ac*(u=?@Pv{*L4qw9<qNd-)}Xx6UK4!9L7Op{Gmb!=={f@_C`)!zv||xn?%UU<%bDO@LMX`FK9uFs(o)x(!AKk^W~|i0^<=ty9IjL2sUmD5flS_3U0Cf^6oLwbt09tV#s#!@461cW0w;`|2%FqTFgBOn)1w~bS$sics$?2{`D?%Ar^OGkiX;?hr9U-DXR8_}n(5fnrZL>xAliWf6K$zFF)|TEpD3^nO)8`ObY!I4O?nHRkv$<jzpLa3r5(EsuT_F#Gp%^!KQRH(MntG{751DG%K{Su2FP*Q#eE>jHlsXBS(>lUxEw_*F%!mbKz2G({7lomL*QOh(b2vVlSZ(zS)68B!689ZD{e@IKWgf82a7}=41Q-K0kqADla|!kLdYP67-RE367**z7tC#Q8l=@2Ql8bM<SoBBG-Qv8N@P7&E(PU7w1py4>q5I)+d_p_srjXnoZHLT)Ak2`FRN7vSTfIMmX(^AMYbh4TscL`0Aui*TIA@nnEfQqyq(+>Omkz#Yoo@Bsf|hYDB$niz8*AIY1)Q6xydF?wX)JoP3CG~F)4u~bj2G%Uyz(Ytxj|e5DK5>M5RjQ%p_^${8Cyi$YW7$DN9ez<Chw?LaEI(cFk{0`3}v(Q3Lj3?e|~_w#s6&P`<$QC{k@?=vH#nZHf9JT4#oaVW1~gQtMux&q{K9)2=`<sV3s04=shf*dxn^Ee*v{t_FL)Bw1l+oJldl0Jx;Avujo-I~m{MWHdT(zbKry3K)hfn)=ID5jba-)azwxn%$ZcBruTVtXfP7F*Ss?9EIg{mHp}D_n#!4E~Jt`rC+A9eM*2wg15^w0yv9C*b0x<V}i~MKRR6mSjXD}#CMzr2xKE%A&Kl<PCYz+Z?@!$$~wJNbfvD?V(&h$WusF#gPfSGN3Pc=?ByMeXwqGk-80G?6f$pXu{-O3z*xB70&MT_m(aq<c}vV|+OlzfuHGWsdXoS#7DMV~;JAw{E3{Na9}YE)?X9Iq)!`<3lPtyR>(RK@4m&ASS;B7tyQB(NEvIoctJH>9RIWxg#PmBG!aZ+r1YWf*Ceu`txEgCLaK>Jk>32gbYcxc5dIcm=1FVxES{Y1CIcWr7<b=0c!7D(OL_Mb^n>MW9<xRV-oR*-7fVoD^^1{{O;XUOuBuX_7QbsjwczUu3yS6wHerX&I3Bk^{H%hyX&esj1DQBzpv5SVeDa$%`S?E{L-7GKh+f=?}7tpC~3WHGy5wnoIrM2g`3ovm|?|fB7NW;{@c~YO%im@0kQW45%<f_t|Qe;PHF(!)xSy!n3evPY>-C44N%3;o(5myR3THzS+|5>Jl_QL_IM*~Jz2ZC(zYH|Sp+X-3K5u0D$sM1Geqh{CPJ$WMY!&+eo$U6bXWJ?K0QY~~7E9V=wR?3!L1ZI9{tL^`r$qX`z6oR4F<=RO*SB<h1PWlzj^Vp9h!fO(CS}lg1UQycX1jR&9i4b}M_lVy+^J)>abU03qoc9zL>oA|>-}LqJFB7Rn-9HARgq9Y#ub=9IJ_`USUnWLjZ93%y^*hRd6BR3Q@H<aLCHb2DjcH&|T@r`c7Okf4;kB-Q6{#LZB-|DVQ=4j!sFwSpHb}ilfcFJHg9k?Sxf6Xw3T@>MzaY_%Pz~ap&V`#&(ukCp-3UjX>#bqYJ()Nj$QJ^Rp<p-`;6YxSvA8W?Ty1fxi-?ZypIj5M-oVoCi)N|zNUgcFP^)P(B-*AN%1w$nS*5KuBZQ|guKga<9?OU%^T;(J>(JmYbfuZDN|kXY&R~ZARsm4$?%<GmhQRTwh1}$Yb}$_PPGwfII9-t(2~^)LNUc8FbH=kxHKO+1&AybG?L~rlBa^WzSdLVPhn;W`$BO8yQIzF+j#Yu8x0OT3Lr0U{^giA#>W254&zxx7Ii$8eTD3-HkYBr&&l9>@OQz#UsLJn3cdBi5{W{uKXNRrqm$yLvs^3|$$EX4sLz+UPAatE7WjB8u3;sxS&cxakT2ZG~)zvO#U7zR=#-02^rIGB;%H!Mu4!0bqr7LQ0Ux||pB!(zG5LRSREa0MvD0P>#WT@iCRbZ4B^6?7?q`uVYh4B_9&n_*3#-dWU3|q8Z<wXU1W{?|C2N=?UBnUkQK%k#D=Nwy1X19FYsQz7@mR?J0SzU>E9pH*Gry@|d-!Ur`tvL8DqRLFfz?^9JM00qKRf7Ap)Jx@R-7c$kLtJN$@!DNLpuzk9)_7lnfyhp*8jG<N?|1JjT9gMs0JHfGI{ghTtNoU`X%wDj*qzhu*QcBsa%a(WBDRf=8nl-|LM>Mo=lph9N7gMU6(><>R7iF;*SDDExEeAFUJeCFGzk#b?;#-jwR7H4tRqBnJ;nOK9@6cKz<JjU=WuE5`!TexlP->5v68UTL$JX0D%25Pjj1CXtZFp~Bf|x$_3lv}2A7n!8o=jT3h5=>g2oF=n7e|{6%C42A^21|Un9WRuQEzUSYaXCAbC8`q?XCtsv=h94Y80plgGdOHfqR0RoN7R6T&Y|lgeGn(6@?LVUt9PMjCZlBa)O0XgPlKG~8V}SKxM=1bn$pz8RBA)(tKTl${}6x)R#XVVyL0Lcz!=$ZWI)9YeHJyFtscQ}Rl7f_tc0FNoJ&)hiwIyiGPB%f&dzbYKPL^BIgZMABdBO3OSJ*Q&{}mSKojLGau`R9u;Rx2})((OLCW&VfY{!Y3dl9DoiD3o${{w91YnCtRi{FbL_fvon`(D}s!+dY(Q%U81{lu_{Uu%YGgUAc1yw^cHx<a1*+9YN18Wle$O1j;%dv*BkDSo>c&`D%KU<Y%TyNn|@MIYALkzdqI&ZdQ_`3=~0bjVx3)`N``xrgQKEJMXGHIV`}N#oUJBM!dqVIQG{K22d8eU5az!4ND{k~i<0$aG8L0;^R<T9ElYEIJ?*s~?Lm3^h%&OkrWwjeOL!m+)T^)ZYYUUO!K+7@tY~5o0NklqC9A=uY-+`<Zs?Xd-t9}?XJ~;KkK1Y;=1J4hR<vzKes)cnkGjz$$zqwEqGk)&HFi(YsyjS}^TgV$`+mM4stJ!`3>qycP8CLEgVj1x+TWDUq7^iS(|jN;FtRrUdCn;p7W~G(7}ZL*AR-f@ZUqWvaC(Dx9W*jfeP)fU>EyFO-V`>!87XO~ayU)pMO7H96Q+zoodU|2M+?yaY!iora}N3${!AJ9N2rj@pD{EAsDMY7*3#}CB2z|G&=sR;-BLWCY>WLzhe@l72Xv(5a_4|h&k0#weCh4)vp1i-oWG(9RRkr*s!$E>zc)}a2f4dNZS&DB_ZU&U%bhw1FWD{JOP%(-dXZ>#s`8uAdbVEu)i7|$$}dn^bX~AV_K4P&5<JjCCp%E3vuX8`&at&>x~ftz>oO^9t%v4bwF+hRAXuW?lMvu(;qx`KS1-lY!7VCxj|e$%&m5Xh6kTAf&H+5UViUVHCsr<hQ#eDCQPk2r!^#ku3N{6}WEAN!XK2IlMfH2h08<HU7Fx>col4}s?qhVCQ6*nX^i@+`tYJnL19=`4yG0;G6)>sWqVySPMqK_KD%Y6yQ`B8HTDdOO^X{L*0FKYS9bP$;DD!mh9lP13X=+4oim^TNgaW?6JTj5ajpS)*Dk#}&xI<4Yujz~@%4In<BP#j8^@wc-pgvS8G3Il<mVf(g@|G!DksuPDahbtTNRM>M>Q;ll0drWTZTWupgeqY?x|C%kacaMwZ^!7ZlM<{2RH@qExx6W`Q7nay9#=`AM2IqByi=oIu_a)|+ap-Wg?u|ia(xK)Me+?I4_VW3A6L6)gRanVtYveJ+<iZ14J-;+F7OU(QYy8M?!`b+2UR4_$a_0AxE<3RPtV;FnWh5kNzhgbdHAb7x?*~MToA!6ficilnoSJNzJ=gbmjHrkfm{lvLN;X+zJ~KP3Sk+eB7Y^4N(4@pyi3~v0)khjWG9NiYXMHQ;-gj|f{_YY9H!y7l;H@AJ*-iL=9b&kYGm=D6NLr&w>Wz+956+E1n_A#j`yb_)3Sh@4<@d9ZP5~BUF8h`^QO^KLHd8RmO$3S<M%=tQLOi=FJyCU;Whwl6cDf_dTO9cXW2;*X#`|5oi52M^K(IA65+)yPWbXhKLkY(eAzFpj-c9BJS-4}MaB`HpLn^&+$QSh4xJ2lZUtx>_z8fE0Gi8uBuy$yfVZUp+aaD`1E+ZPdNeasAEH8{uc>o|l{)7l@dd&T)h17gGxVL_^eHls-bYI)Dvd=Lhf5+)D{V|Mf9glqJ~UX;uy<R774S8W(8M!`lph~nv#FKc5ijv6jye$0@+>CHD;Q)&@pe;gOI&D9$8y;t=s{aj3Px*Ad8?nGxs*5T8qvE)#>D=`l12IzIIE*xy0~OaH>j%!Hc^7HMIAt*n@uXJ5Yut{8>kCe_l+Be8@feTm2Ohyv2uc{-w#P6F!)opPbSV458u7=P*=Og>r+xW!>(2%0(1^onVoN#qWaLZlfAYatF*LBr9q8C9%c0;6Z9zS^qEeVL5ii-<tCvU1ie%wfrp?2@ZiR!z!UqqkQPIMt5bp}u8`FBc1@#+v?3@){K`!zpcMwmS$?RQ2=7%3;bqh*ZXc9M7XFm_NViD!+yH+<d&dI+1&}CJFanS*6iRyPsQF}q5|y&PaFlW5y?srMcU)9KW!^(02D9GsO0k{eAK2>qN928wYF9(UTPKsLWK)TA0&YjUkzt&gtYAzPABXgRlf?xx=2gOCa<HoBpReDZcl@r#pR}JkxClU^s1`j#J~7DA*3``AolxYp<f{{Cg{r8VpoO_;TbBxyXEFFm_M=r%Ac84ZCj2F6y~VK30??G<k2KgoHgmY<3+o?T7tnk7x`Hj{t(-hn3M@;IH+UMsqpFo4E)%Us-J$fx1-XNA7|U2(R%Kn>1VwjU%KS0{1%_^TzeWSjyeTOq%R>?>%?PsKQt3l+EHaw5qeRGeSgYEcp`R3yup6W9Xb~lfJLOcf9=0UzHON1==)}$V4n};X%*Cx$7wWb7rPS=!%<(Kv`}0%@YxpK~Q1c-uCOxs%+`FjsMn~_J$lymQB^U1da+ThQDza&m>nJHDnLZ#l21`pQ#BrFahk78|`F@Jm?tH*qSM|HjrV(|@bGfahRts_H<PD@~NrPy8g3V@(AfIBg<$9GZ?Ig2LDzmh!1@br|D$h?#Ke%tp<M?4@D`Ve3?@Pg~kUA_v-K(a6faG5b*RTP#F$XUlMJqbeFSMubqh6>>;;HTcH)2chKU@FFj@K$FMvot^T4ft?uIvx(>$@sv&MH1zH7V3dLQ_Y(b{$eCqXyn1h^e+-d!MGh$U0R8Zq=Dk8ia7XtDfGGI$he-xNkNuCoD;K69t!6qL=$WB+!Y&r)yhlRZqxlq?*HYNn6r$mF-UzJOof1k1hKCEhQ4cO0f0AIVfAG7Jn;SNimbvDMbt8+&WB_N?Sb;RJ%IgR=Gn_P6vz?NGV5jG75Unl*Uh+s(IJ|D}E{IdPgcmqU01`!94yKvL(jlV8a?)2LqT2BxbCNuc{T@2`%&5o^E$Nx1ZV$-3U;FIx^_kOR)ILH4h5tDdqwvZ80sD5vl(QZ@w8uHMM~XRTzpBy=gPmv?F0=!nW2&&A08j-xLYA8ZEbDW&B=5>jp}mr~yO@N-^#1Fkptb)Jl1m>YnLNJz2H1d-8SNQr4iCY9J7{xb!lWK7m#6;MR9e6(8#{oGN#rqvlSiQImSj>7ZFR+^ddOjoS+|Yoc?S;wnP`R}N>F%!2|dAox1io#n7{@B-;cR044j%2J+vo^9iOs(Fg-_$CU>Z*gbDA7W_1s`<Yd__Z*XBC0@N#gSf+<}u-KS+g;Xh^j8cu#MUUn8vul(}A+cSXx7Sn0!;(<d3V$Y}m3doKD&Z%CPg;?x{9n`Ge?}^67s8(5m8o')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
