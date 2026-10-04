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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%O>ZPua{MoI=0WW4`Jiv3nO<qIBXPjtY-2491OZ;dfU!Qvz8U-9O_}WK>dMH7$b8jYt$h+ja@h4=y^qYuh{&J*`^CTh^6Ov!^6QI#`su}|x1T@1_<Hr?-+uXzfBDacZ#;bY*I$19_rLtt!`DB(`2NG){^6(I7vFyQ^UrU8{P4ruk1wuXyt_TTxVjGC{`~!Z|7rGvPj|QPzr4GD_{rh>{o9BC-hBP~x2yRBe!l&3|NZ<4Pv3fY`Va5^_~p~$@BVmuxBT(xY2v?_k9hIf(=R_g+~({tPM>r7>ahQO55ILjub=lHKc4>V^>WPb?`}Vx4;lR3(^ubq`S9`m&kt|%{>#&=h@aUU*{6?h-|f@+J-vv<Ba}va{Cl$pc=z^cAk!CdjPW~9e~1hld=whZ`w!opzs;u~oevAG_r>S^VZVQW{&DfC!6Kb4@Td7d{R}Oq-=5_2Zy$B_;)ngm+aJM`fNgXfW&DiO=V$X@dckoP9zOEN`{`-VK4|)4|Mq;z^N(zvKVsIv`7+;>Z}0ba`8ibh=J|A3BYk@EY|fvSt~jpP0XbW8kK-(_x%dq6z0;?fj~T84=M{z%48Fl>tH&?acsp0k2|GK97gLuV`vY$boR9HyXUjgE98X)leM~Js4ZbUI-A<>*@ee%CeEtB{H}mx2=t>4N6c>|tA;rf5@9A`Avqi0T(TWQ;%+J#+alX@DH^;w-qs7Nq_iToiUtMs)#JzkPKRO2Ochy@Q=p#X#vz+Kfz5wTU`eOMr@`vBue*Cz9cmMMr_ILLmK7RP;^VzGXB`~|#=t#TtCiDk@myumH@M4)w$K%=?9x|Wk<mc(PY3ic`auAl1o7l>(<QuLHF!^@pQFzjI+ACA!i#}x9zmHd*w`jbT5l{2!NluRhj?Tgq#8lwv{mj0AdG+E>tL1oL;*)PKFKjoHpU?Q#pYb>yc@(@!AL~+g*i%q7d%8t<hbN2$8*;@>fgF7kX;7LD{qz0Z+rzi}ySqPIVa#bWPD4I@I@k=4->PRwF-n*|FNCzSAq)n01ptP<-!z*eZ~STQybG5eJi{Lnqp<pv@?}Mm1~jfbU>4a_;l+}u?+V9>IwnNpT<i?^#q!2$hMmQ)N}m!#S{CG9>Jt`U{9{Ma*{&*nCIE@NAW}TWSO|rV(r!HMhdeQim~CVgPP5e%0)Qz<D@Mzws1^Le3c(yWQ|j53j0)oEogU-0F-@0#jE2LJTsw#(u70}Omw}ZZ*^079ynj!3n};|P+^i5n(fnzp=rsL^ZW$_Knx|*}{_WkLcqmW}NLUr|^t0)6`w$|1Fcz>ykeMWirMF2DWf}mDj10`>VusJke<Nu2`IB7@7Hv3MS%<pyp~2qI;s~yt5F~kKDME8~jU5)`8iF|XbkeF=kuxg>f>4HYvFh2@Vww~H)_k1~g`NzxK^wxyLt?-s!$gHo%5a2%AE#wC#UrQdsTRo*<SzyX81m`{a&cC{4w{07`AMwCXnwvx+~Z1#BnWxRQ6xQ{4%2YuACBj8vg80}HjU%)U6){b5L(x`A@g^#$(bOfyfQ-baYoB&rF<p=%!9LTnx!;SlOGu0`DwGJIIne^F{og^^9JyDoApBjH@*%me8ZX$PB9{h%P7*0@ISLKUbsPG@Hl_VXK&oZI4=?6q8VUeZxfGYAIw8id5bTzH?y!v(S^chVI(U)GXI8)*y$`#4^b+s&4{hOHRILm=ZII=z)EB6b(v~D!3zhAx*#i!FHHoeGHk9#c5z})*wYd}s0|oo0s(shlUoeR{m2v~v%_&Y2w7QyxtVx?_%#A+U{vzhAT0fOuSMvhO%#c9BvE%%o?ba31(O=D8<_^MFl9ceAUTKuTLaJb$IAkR>FMT=%#|m@5Gti&l2_6t4R|03NE<rW2nrk^OI!t%Y|#%ylpN&+HK}rmzw=bN?qWeD0a-0Q+>PbI-XRKlr$-<{6CFv_SQQ~^T@Bw|!b&xCn(~yVA4dM4xJ7pV_rqEk6s{iBBFshIz&hX)p;)~2$HPDC76;2{jo>f7JPoN?ar<v;=V7bAe^H?`Mu<^!`|yV-cJ=Y^GloX#6N|v_64Ez6CEjpOs2&4ZAE||p0odGDFrVFG@I!d`tqLyFyo76RaO_k{02Z)}@Z3*HMyv`Yl`x_h+Ai_`w3L3Kj|HEfgjV|g&p!n%Z9@Mqo<ygQQRN)^o3#K9+*u@j8eX}S*HOO17TePl;(F|Z3XuYi-V^+qL@4$-)$uH&*~)?$mPGNO^>k8L3XE<3&1sB`T~G{f!No3NP1BQtN8iKjUyFSTF|v~S&bqvJ`23k}=~Jy5&#lglg~!M3?Zbaw(VLxNDUr81jR9o4CNHFc1Y)LVjHwv`1~5Irg;1N{B87LFv$z1JA3<cPFvoUnVX-zEC}a|KIQ}Wni6WIY^@=o{_q{-87A#NpD0W100St{%&7A=8q?TF`pd6k?0T7N`Q=xw#-3A^LE)?6Uux*B<7J#l6DMQ@SC>{cFd-T!?8lFPto0(kLtcCF^P+|Gm;In%UF-amJ5e%c%>>Q#cmbiD^r>pF8w}MMfq@3a6!R7=@67vp1++>x|OpdD4r%lo*5N^yQ4`FcA1F$m`t)%eA7H8OVP^6fG2fY5XI;Uax0?HYu35bwMSL_-wIrb>1Ks7zy;$^I%ZXh}zs(<bPCg)FAyGsvJm%<+^J~`goB@PEzH-x;1mt2AC(L^RXg|!T<xRh_pg-`)xI2go@>~?xKw8DpZx}w(s?eV6sh;F%+A|2v7NJ7Vd#ztvcx?@$N(Jac`v=S0~L*=$g*UL-MK#>e;LwFKk@&Q$kJ<KJ(MRF1}1b)tofhnp0dXni{j6%-PuI_@oso-oee}^d*s^{dhb74~iR=Cs{lm$i+^A%w=ni`ZSNU|jX07?AxAy(=zG$&xzS)d<}uo0nQb{^%%JSf`3yZAix9}$RgOIPDs^D1T$hXz}GGz}3IFHm-%NeN3le1}f1!AA7?&I5qg02#$7_exZg>l><C2D}WnA$w<frOOkieuy!{C-*C`)|%*@XAT8kFt%b?<oqQ?5=Ej=3VN>AzhsqsC>Qn9)OgB668xM@SWZnw62dpuk%)LIoLh?5lB^Xrc(AYgL;+CYp->Yd^5<#a4<A1MaaPXMHzSc5$HQuRJX$ig^L9VLJ!AW<0WfS>B3qy{^5QIdEh`R_qYVJWZYT~xaAd#A$5Fo=VUx$awW5b}E;c*Z^woiJ;}pC?RO;(1*KoT90V#QlA6)5DSH`4<vu-DX0wh5sqw2I-BNx%Dndre|A(e*MY+cv7DKU}wtocr$H_<e_zGR#7Hc<0G=Q>clfvL<TP^;A>sfvy|?ufJqypHOlch5a)S(SHgIlVIQc34TUS8y%#U~)W&U8F-(5HA0Myeyy4KIvYGoo5PKTAjmE%s!&5uE|NWo^7p`Wz}41nb@*#LP}Q4p6CcgC!6#uS>r`#%nE_8jyu9^3wY1$#fW5%(vjA(^hp({c+y7v1M2|C_EKm@Q6aFCD;r&-BXEY(FB2RR<!3ZYhdVDvD?&8DX@ebd$})loXqVq=%B$gxh7L6;I^e)Y+MI&W&36e9uyJT(`dzV;1Kd&O&5sHb`wj=(=XryV^hyzmtXrcn$dudSuCm69$l8ywZujHdd*9*~RY&=r@EI(bg1NDIu19btHrp}mlyo|vA02S~2iYFWn5NIfW{%BGkkN~We0#u*8j@zGzy>vL%KxX5>JRboL3dvg;(FGIl7B^;qzvO3{<|XOcFM}83eU5p_}%U8=Y0XnEfe^`a~7)xt2G#+t~l&brp+*)EzTlmCn3c-2F<MaQzgFr%)w{r&)b1BwiSXH<=^MW8B2GKgOZ1&O+vr7x*nIqyITY6qdanj-4Ch~EDwa^(wJ`)cqYds*KyaaFg-ZjK!bg@?2ZFz;$|>qhc|MvoKXbh=|+e*m$iurdg>@Hz-`4_yMfe{+;cq=P(*~#br2VCeweOHjrrzM&{0Y6xzjcd14I}Ow>(Tig|SFEB)pto?aOhNdc8D8QalX6O>Fe<NKX;%f3;&=g>j}Sl_8qfv>3V92c%|!2p(H_y}Hao>|K|0m`P9N$9J?XtUcz70=tdi_2qR%@N4305udKFYt}0u?Ii6+&%TP)w3@buk)s~*K<>}NJi2W2Ecz`NbTA0Tbi*NCcPK8+nzfqK?XcBNpGI)`fc}V)AP9a|GOhE;X1!GeAZB=Cv5|o@g>p8SuImVnyA%@&nk&qeQvHd4M@|pquco1;gS!%3m~zzQYGqf>VpVYz@c#CPxA(WIj?=+MW7_ugS>jt+!}7SC@k!?u7?uuI-K7h2KyDjoD+Ph^l{`g_jr#I}D<iiL@`(wQWe(@t>W4GZ(1OWNB2H9T)b*WDDzytH{i<yNJk7mF86sXc(>&;Rc!3(n{1iKT4hP)i{jj1_SzgUvp~%5~@kUlG)AR8nV|`fmwq)Uqw<cwMltdoYRe3yFORE*6yUgyYMiHeVo>KE`2Jf+UTND@tXkZEgvK|FDUt7rEJfcFG@9r7FKp5!{eiNPKJaHq}&u%TSGwNt)gn$?aF3k**LTVP(k*XTMFk9MX?zg>`48D|#&uWvO)ahhWV|h?gq6ol)IWEbo9`WQ-G|X}2NF<8iA-VYK^h!u2DJY_%hKy3l^^KcMOAQkS8)4d*x<dhz4yD8F(b*b$T$Mdked`+3FG?H+2^v6ha?1SDpV$*3)*RvLq@-$^4<OEIiIrnwMr!s^SNd>3Pmwtx77j{@G87urSc{0il=B3S@8Hh3s#`r1)?9He7qr7KP{zCR7)!C`3x}B~%2R-?$5cUA?)hq=sU_lnq^acj-(64gb^dojmam>XTp{q^CIGA|hc*d;xX_7Yz7BV>+8nIRX++^PelPrbrcv!OC0bSIM%OvIILJ=TfQfa8T5%>50FS3&S?Tobs-QRO08t}=Lt|E0{GHL_4DZatDhz3npY^LGUvNy-VS=qn`?`5n!Ju?N^1oRY>3Q6+f_X1Nb29RRi|7>Edceol);l`^>=Yb6)OE)C@0Ex%o)NEbn#He!^l&UTvDvxV0I}I&jY!-C8Adk|9kN=Z&)W0wsE63`5KN`fKe2*(!Z?tOb8C##)vBodls2h!?XJ>*tBLhe^jUMVysDKx2vGA)F_pGOHm1{oO#(#XMn&djq4LbSn~@eIv%M{G5wnkPc?>@N5G(+yv^9<c@Zx%<1WL@PlA+0_WG?qJ5a#?X7zZwE9&IV$sOJbZRhi`wWLSM8H*h3D@k){wfw5))nZJ_krq-U;(9YL<0IJ@=!`fsSi3M#Da7w{&Fwe!i?1PQn%kDIqEIVOglxr{3K&cWK9r02}u<34hUg{#ui9`6>C3GDM$RABNuDaqwM(j>WQ%rSf0=_FcO{>j`&k`8T=@E|_eWxog7O<T0Z~-#kf_sY@r0XVg4~%(nWHYeoh-C>pMLeGZG}7}~w)AJT-AVKSr<^GBhkM%44y=<Vx}dCc!3@0m2j@unwN)Lx?n0=#5hHI=(+T8e*+Y2f&KmuQ2($)q4`%IZIz|t~tyG%o+2r~NO>u6WHcE_WCIXPg<kpiivIv-v%j;&locYo^WfDBb3L(an=-~#|rj6^^@bK7eSV5`+Q7d)B-Z7e_?_Q}vg*Rq0RAVd>beCFUFgXkh{9jj!zEEJJ;4+x9Qln2lZF#-803ZJB-R*rIIM&*fYN}KyitwU=JRz$qay=FctCXmd|9r~>Wh1Q-SiD%a^cm1=DO{dbjeOulC_swu$T?8#8%C6%qtRgWoBon1AZSAM#LFJbm~#zxBr0C!1PF@7p+6$d+^3!ET^t%pa0kR)bo}G?(b}fBf|Th5u`w<a`B&(r&ENoZGBSdhf-1ZIg>;|7qg^0UaC367h%$akg$uJ2gXi;W#nMAPY1!PLO_>GHsA@&Qu?k$EdUzLW-WCZo>Dr=!{G~9K<7&JCB|?9coNg0)6GP;}v<<zKa4o_Eg*N6QsG+3+YT_j|Vg%b_wOKFxaQuZ8qj}fi_9$hZpP9p)twL~KK)4+X8Vg%wR*r6{*;^;243@@=234R3es-WhKNbf$pVnsP4pxaG!j-tPMhs-P6-_H35hF~4IG+vtv%o+V)FFa~GXFtVL}kB~gd~kc+%d%(iRNsg8Ei-~Xgnd-4j+KoM76<R=NLGW8w)ZJpfvI1y^cE`D5Wsr6YvW@`S%6Q<sjfF;4SX1>oFPUBPZSIj;L3&!#cYVZD~g6A=0BMW|o>G`7?yAY5p!4nzh_{|J`>uQRx$P#;=6rbZ~C?6(AWJW(`=nE??gYUjHTt#Ijql{&a!B@F#TLQYi~4(zRxIdOAX*0bASgDQd--Nl=C7JFFO+9Z=7v6<dq)GJiW-ITm~J5f#kQe)^k)A+#Ikz*wFEE>#*dbO>E`a>!<@u^G>CC4y_jYDh_>@poHJ$d+W4LT0kMtnyvj_9;25NL%U#4CO;%NvuuV*VX35urBh=Y+3JmCw{YXi7Ic*<-V|H_Dr0@tAj9q7*}E?*~<C<Q3+7S#?ittB8XAoq|;b$Lz*6dhA)abwkgP9IQVX<kN~yt9E$0QsGuj3dp49sF01ymDl7$RN(8w^3vx<@Ldfh-d3hOWwiL^Mam-W>T*}T=bz84@EfPuAj@gXjM%Y{>u#{D7)YY<zkDz#LW`837smAO)7uS+H#;>?}BE(G!e-*}}YTa5KeK6HFl*=+epkt!(e5rT}6IyIq#}P+jr!LjSXsy_Ve=J8E95V=L%Dg%~cY{#^X3Cak6aes^vVbAk)>3gKY}*5_;(7~Rn8$MS_o1=)L<!-sOyUq(z<RYlUxkQ+Ollrxi}+C~fz7OL&4vPOE2J8VDMC`kb#yy1?Dl<|Jv$QC!<eu0QXx2MHm28xqf<QfS$q&hB8Ot9?5Oo<+SV|0TOSu{Fk;LGGOO4cy#MfBY0DI7G<(tIYanEceMM9*!fbHqPV)(h1rmE`><q;l#v34%5!L3mx?RBgAOcj>%#X~s+zCF}t)oaQ7`+ii=s3LS=eX_y<vO|^1F>e`lgdIN3c<S-NYE75KWHHCCe5<6?b)ifNPY!#3K?R)$+EPm9GqsERD{DUM7aE*CEoSiBB+$2kH=6&@35UPRqx>y&WT1;wzHnad&%}0z>TVsfHdLDRW&OGR+wz_I`$K5r>2II7YAGRu$)K)!(d~{ZNKZ6*xB5gjirE|-YD6vE2c`Q&Gc^9;`mhRxem-{d@Ms$O%Sl`9TTu7iZB^nz0USB`Sr+1S;y99+a#^D!KerbKv=2g5$(D_7m%szWP-MZF%vW)!c{2J7FoCaO$ZyA7EhasLs8ned8=$8e8Vasd>O^3I5-H7@rG$nL><;br<fUzNiJ>5x7danMWTpdPPq)9LL*H~1DGS!x`UyRJ1L)c0I<4qj_El-TLwq)YsfK&@m%>`-?0h0WLH1V<gpxMsUX!b0V(Mqv29M?jnxR(gd@u(V&J9(u~;(UDkToLWHE>6u`&`%$7IGVG^dG##qck6jVWuC7^=hi3>i-K_BnLeYd4#Mf{dB6dE#{GqR}A!CFH*D28;WuLbd7GzpK9~`k2h{nWtJ3{I%@(E^LjIsKo7>^T>zt#~F0Pnr|<*)H*OgSsB&pk~mtjV`q*F50}j)Dt)|a0Sy4TEc^Ps<z!P0T51;{Qp&id!7|P*<IZqE$L+jZsh1da6#^S5H}!Gb;XL}!JMMSv4on48|KEsEk28Fe_=xWYs8L%%jiQdfXc%(7O4avQ!nf$R{r>6h_WhT4_jB<@ohG#rS)~v}%Oc0A&3X@%$__g{_=c>(bIZh$kc}Z|o(KW4qFM{Gs)Pgv@DsY^J-fLxLp4BKb@KFy1%!B|sx()V_6YD&tpU7*xP%4eGxgl0Vr>KZd#Sg;v1*UDOe~1b?P+sj(TNAb3gdJzV}|Bn>U>6#9|i{z0{6V_bR#S%KQ(XNY78{eUrOvtu!jI;$aF|Ro76Lkl~gDYs~0qRUiV_wS)Eqyms8<U*jwDM3{Df|ZSZyrzAx+m$oyNj?ltIPu}o7W3=8IHAq`@SHreMdw6b0`?roP{Om0cR_o?kh!n0s7^JZoD^e_JxJR3Vl44oKt`GIAlJXy%aarCU1ry>rxM@^8Jrk>TKDazzInO91qE@;Q9(78eXBL3+GTa*S>EsPi{$+4EhX3GcHnHPM^F!I$d>yH0RavA0w?{)Oz@U99XK8B`9+RS==!7?o1rb(^p<6PVI%&hA+)eh-}c=gJBWIYm9nJiWA4(49am*+@nnTDMZ!u*#RS*(LG#Y@tqy?|(8E&R{7T_Kx*68>p*d(3M`;zoohRZ-u8ShKSvM(xT~!(b9tKv>flgKHRdNK9y?hZqYEv*WQ$dCBNV?5G3>JL$Gf(Im<*X!r|N8mMK?JHDpPW4{Z`rcet8haC-y7a87_Wr12b69>DWQ5ScMC~-)7nU@asIOBfT?7WRxtrs*Rn@Z7;#ZSp?p*+%D^^gL;5BZB7x=`Y0$H870O61Mlq(pvID;?Lwof%u1+C$xGX`7V4`&`J!bH~70<K?JdF{hS$%!=c_am{$b>gK$!1whWs)woVIAxjNgPeWyW6GcULQMqgQg><djvKDAPB}+Qjy0!Slz0RA-(tth0@H8;U%p2Jg9qIb4U=jEw$6CcscdR$@ON)|4h1k-jYh$pk$|%)*C1moym(SSM-tDQDLsGOxnXR6-UNLq=<BijO;3+0I%4pj}${OgN;6|0`DY9Mkx_-&{pbDMVpVAVQ8RiM6PSl;Q^|`19_9?(NI5k7<HVbN4zvo@f)Gg2xS*~IdMO?$xkt01FBf{G(vRUrn9uFeV@yWAALzwtP6s%#fkAI#zt{z20;LfpCA>+xn;N?#hd5Ba)#*NC_)u@)chyBWRWI2sFCgRm=iNeMA9ML&z<(=sZm;!NJA*Ltgf@(!Ts5#!s%o@g01t0bfrIv1}H<1DL%Jt3N>z>@A&8h8&O}byra4@IIsOaRL?=9axPCH==X->b%T`$9BOUvT4nPNMV3(hy&ro|D-=T{ThIu+>UonB%Y?yAaQ{bFOR?@JzB6FmqD4$AP!Z3Np^<yHaQ3*D@nbZzNiuoqs5)|aE|!8sYMwST%ty0~Jjmq)F_GMr7eC%XZ_*Y(C_W_eO+(K3R$T2)%_sG;t@uF2Zk3PsxU8(|HywftTrBjE9HgS#HNOCpES#|o8g>UhZG(tE9~!PX&x)o`3{pS8==#wr}VNHU<k*ODk@gepdxMDxyHJSgaPxoTE&_62+fP^$3EPX6fy<<y!E)(V<I#3~wzGoMn|r^siWXRX(Y)&xEmH>Gy8A|J<Y&T*-#47YaD7|wA#g%Pe?v^1#|h>ZrA+U<Vf67JBh#<_-RLyM*lP%hZg{GNO=j7qCMeNbT<g1xHiN=$+}J+e29F*A@qrz%C!(U1B%n<$llhej>61mPI=l&NSlEsDcB<Sn!q6?I2BYSEhXI7f!@mt4+84G?jF8eKTrRySIKR;xS`TvDNNjmjPL+8hsM-ZHWvH)f@nD;((xk<6h+przKR$fw_LT2U|rG~Mv*GQnv#v8oaUVXktt&3G@Uh75^i+>48wjBxOmjPZz|Z8I<Mq8BOsDiOYiriGAJ=T^8<cG-0wO}nVp@%o!?bG+5?vx_*&`v6+U3W_>Caqyb>-HvM9JgAHyf(#q--LDR=K~NXJu-Q?OX4H^>+KN}5@`19vjkio+98(*SDs>@Bf3p=DQo6=gUb7^AyW%&?hL!q8lC8pMa{~->ZQj`nBOO(%BUjDwv@`#RrS(XGl4OZlQyGbm^(}KIAtWhaziUuNl@VH|&n+5aDWV=)pTxu#(`}M>lGpRc*>=$AO>IF-QCe&YPEX8(B^(P4RjDhs+n2cPn%^Xd@Uz;M=P`fmz0*U`Z*6!yRp&wcal|iUSGN^1dv@yy%e#H87fs*U%2O~?G7NMW$}bU4eO-;M1{=HZW)7l)K_`Kt@O7bp*PkwYI;zECgu-^@<d1&}v98uYW@X!j=@%FqigLIvfyK5u?&Xxz9Mn*!<%N2{WT>eh{5r>-0+f6F=<L~BfF;MqOe^mR9fNR^37ACykX{uM{9?BEG^ZwS?e~g}HGIIfN^7}!c0lZ+trS6x;S$DQaHU_cd!pIs?irgWf{CVW;@G{X*buTp+~63399=PpxZAk_CB55Efzz&$o~_YDu?uLe!!Gr845PdmDrRHNMg>CGDm}8!m1T53G5bh^gq~>G?4)3C@j4}ZCD%Mm5da8`XHQ|c$?AM#>9yUZ)6x!|UIQlzP>m-a#DmW+WAMIH`$b*_Ui@J#Eoawd8v<h)-v}%$H>s)shL<56w;{`eX7*JKBi+n@snfa|aR6kJT)4jiDUisz4kOT03#6edjWx&4;FyK9DLbFmwmegnRh}igTIx~?v@SfzZeVblFspN?A#|-WB7*8Ht)Egn$kYt?lhsV93yiayH2%yjhoj^sXUMV2z)hQb#es4#0$_xsNEN{A!|5vXW{`@RY20(SAHl~$m>|%A$6t3`7A9!zWw188-ohG>BkzocXZj*W#k|N#v!OZ-wvEd=AET4a#clX4YFY(Z%GHam!qcTUuO{DgTQCy2P*F!BEV^7S8W(bI7*o&B?}_`>^C&x8e{Q&)O1zn=ua{WIZ8n>uUXxa-Jo58xyBjc=BW|NjY~WV$k-H+0(bc}OEMBDuj&(^cgBzf5vL=#LXP9{ZIC*lC3a=5;k`AR*kG(hQ_6Cn+kWnD%n;riNO(*acR@?L$rm^xsmvzzX7qp(elKEMRFK~E)9D@O|2@^)Vu?w*ayt+JvFXec;m<S*g_`0FeI-*1tOV4?I4VZ1i-cW|c5=MqBm!)Hx<Pw;QJl{#_YK|739ohq(Asdv8gj|X|q`70~?=o7vhRI$NzoyfD(Yc>eL`4r&STaZtn<^ImsxNu%xN&+dK2m4(6&Pg{SQU&TQ9X-hDyu!U;3e{1V&VGJR`RF=eyDK#I|!YNmKL-PB>h&}FoGg+*Dt}P^lBAZXzU^YA|%pt0F05fah2|P!=$&rmyKGvhrq?jZWpvki=;Q^RqmOjNff{CS!H|dHC4WZ<Wx|E5+TaP33Eun8gVFe-VM0!tkOx-CC{aCVjfQqThcYD8?h!<VbSr>M7hP#-kV)+LL3m9W5$=GMiNDWN2jSM=y%{PYTZ4<^aAef4$sJt@9+$O$pjQ@h|+6~D-AAFt+Oka{hc!2F*u+Ct|c9BfQ6!)RR`E0EX0~PnKBa#m?tN<Fb*_pQ&DtVCMMp@2NYS(vmP>lKBCoaV~Z}H#ncGRURc6lKG8KJsxXD+zJY?%kzN7?J0phM7;%uoo(k`b(LEeRBkQ0Ud*^~sp+>k8iZzByBmB&>Yjo;5ZGr(eds6hitcHWvon?hJVFceq-0XUDsev-IQVqrubm*%H-lDD^IfuXtHeT!0cSOTjDk7tolBa~%Muaal`I^CKvC$R~KQM~r!8KZSM6j<MTZSAHJ1H8Z5gO@4Q1M#@aQGP<c<L}}GV^}7W@}D6qu-CBbeyoq98SPqL0_?I_AozfQ*Ja6^XC&vLEC=X2JqdcpKa0^U=rm9YB4RN6sZ->(`15eJE@H&Yzpl3-$PyRLzs`6q9T+|G^Xj%0M#q;npJBrF9TTUAY+8A<;qly`#g`%RGhW#a{|?BW-S59F6U+$Yw!W#o#vscW>#jV>#sq!zAY8GX&8&CW4HzAe!#}2;^jqO0+GC%#`GRFs&aq|n$Cfsj#QvW%^21b+L4q4G9U`A(Y<~<6u*Cdikags$EpG<f2Z#}U&QNDUnJ#S8hF#DwUm;&nyFfXQreDBE`gR}9F>guszHke`;MB|`?j#CbN9aB6n{#X3)VQ?)eR~wz3#vzapm<Z=Uz?Lm)&HDg_{gX;<!~8IL;tbv3*_7oK&w&`&?>*Gbf8hKYfmrvsaRil$naXbY+`hXlxh>7dL(()?kUlSLKEsIcCqs4Lf+mut16O6<!T`*vu5L?Sd8|5Oj;_oEuVFZQQEs1VVjzsLjrrLdeocgg}4Mi|u$nf)+6}A{w6XxGs35!cXkFT~jx0W23~?YFJEb^|EL7w}n=sZf7T>P*gme6?TyX4HcmndPLVxw32*)3?JOR$tpS2`G`&{ooeWZSd*r8v9esSa^IUu>RaKlN6fe41|*JE;+mls5Wm|FRuDwJbPNkw*QO+vZ;UevtO~CKBcrY`PFJE4U<aT)ScIvmRIfSNo4e4}naR;8OT{W^cNK%v!`^Z7!Eqm}_EV3B6~(mGmb=oqE4BNqoaCI{!hJ|6K*x-f44To+VDkn>^gvU{9Gj;5jO{vy@Ijjsfl|C}kU0I@$Fqs-B4$O-VzDX*73@f}2kFt-sB$Y)mX7Sq!G36$k0*ZICK73ODZ|0pjds6fZ0bDGg2HzeUr7DjE8}q~q5bAkP{`BzM@Lu@3Tar#Xz*iWU><|S3aYa{>>ZkjuFhxEmMm6K2GZ$g$49w{BcQ9qd&kAr*f7S^(+r*uAS+4kB*-RfEapNZIaJ-XqkDlNXlKqmu;EPxBs)xKfEvx-1SZ5C<p%s(YjLY3o9d)*M7>{GiU+HaywYL#opQW7{A;MHFZwHIDmm3V%F(DwyvpqOoE=WK4PMPI^|~BB(TuSALkBvzYP5myv@^8#X}Wsh!#>fteY9OEFAn?M2bZ3$RT;*?Y`w^TkD+p6W9up=ngX7}sR*Rl-+k)6Qm7?EW|Kf8D8ltPI+{4`z$y6}h!U>dk}^}Z0UH8AtP@%p7B`_0=4^e|<5Aqh^qh5wRc#rRXYK@ki^X52X5evwZ!51~vzd_-81ZQ@w98U{sBW8unAmGAZ7LCxx&IAVySv8qM)84HS_!f)Zb0>jW?MC4)K*%+*ZOgpl81T})9uM(vL+rc1Q7?b344BfR0F@J9HWW`tqVF({Ux>5S&O_NxZ4#}gyOAXhm{a)@iB!K-Gtg-%#Q3(nYYc!j&$`%ZtLDk&S-&jmDR<1bD)m}6%zSwWgErit+v?}ZDsKkrj=$1fJm7R?VF2UQpxg#(+KMF5Ad{tQmZl{G+3g?m!ZvT9mbIQ0)G9pT*fb9yW(`#A?6#vJcni`XWyiHZI;aPYBkFW^AOvpKV3OF)l0+g%$DZB?GO`y)TC7oYM0q*G-Pej0XR}Kvpr4zRWXbmO&r;-HvSzw+^?B?!I^ozQ?4b)0%1$2^DVwbYp2Y1y=;j@tA!A0B6c~JeavxbzsZPsmV*QtNL=9NIDj-l(rDgjz5;tz+FuL&8hu#z^n7g|H2K@O3apK<fBX7BiIp^I')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
