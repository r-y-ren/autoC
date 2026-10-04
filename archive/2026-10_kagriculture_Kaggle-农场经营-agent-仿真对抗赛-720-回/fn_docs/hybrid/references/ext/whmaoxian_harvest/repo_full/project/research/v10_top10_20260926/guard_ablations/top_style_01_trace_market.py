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

# Public demonstration plus local stock/budget/weed guards; a proxy only.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rlKU5_M5j@*Cg=YHt;$gC{A_081n4z725(KDmMX)#zVa3=^5P7f=+3HtAv?aGhHpwVcgdt_$M9?-zlL}gWF(&=<MX*B!u|9$u0|N6K8`1ilP`!9cf_ot6P{`l^f_wWA4U;o#?{qJ8N{QBj8{Pl1D^WXo^uV4T9-9P>OuYdW|m(Sn-{M}FQ-oJbO{maK+|2zHi{?G4z|HGG;cj^~^|203pynKKCJMeer)8mhS{NWEDKmGcRAAkSy@~3z2hhKjAfA6o}`VZgz%g=vWzTomP{`~Is<;S1C{_#J4{_@lBzkUUN;O~Fxhfm-C<ySNO^z-rE+Lv7!1;6dDzw5`BPoFN2#^Yzaembmv{tqvoKL2s?*qD1HfAIPT{`uw0Pd|M6;lI6nS$sP-<EM|`y?9oHCW8+zW`6m2ZF%cbsgLfM@BF#G`}`U|cK%{$()AjEUw?dm*T!Glc(u!x<~lp-*{qk}4IV+GIyUlM!~LWa{3i4)Wx3|)cdZO{GRwkJV1vF{b78vG7tlE7GdRy}WLkI)`8jNpK@Jy+E$m)hY&UC-H$$<IUS8P24{o6|#_=(*%&%tn<4@;>arPD1JJyvv=ZdyhTTI4Yk~%%;8qqEG`the<pX0Og;yFi0yV#Cyv0|{1Jz&)KEBFJ_p1N|T#Ya7FE#M~CKa~u}LN4I@9Q-wUVDjRiXEL(cPOgOf<-3nZODVCrC01ykE@hN>$6Ue;2sqbCgXcMKuZryf9bx%T+Vzs-Up~t}|J@;-K=5V_mJ<U%PC8{KQVz*TIg~sc+$R#AT@7H$zW0oui2Ey_Tsgq%TL}lA^vHaCFFY`xSK|_0Rtpp^g7$85E`jcvx{(rZi=N%fV9b|HyGD#X7SH^}>oxP<bLV9|y$igIc0u_S7A9&}5xKmY@LUm=vtmB=@|!tJF7F81_x#n5pMO?vv65ZQ`#Y{4T<r78+AqYLwf9eabH`79WxUgU_VhjY=<R*p%3|j?ur|-~k+h1dKlR<`PoG}C`{^%>Q_w3vhIznSfpPT*zW?(1PbfrcMFIH7=3IK=y)&?HZ1Ly(Cz(~}N`9od0$(5Uj)yQ4a4)&XfALO%Z%#S-cX7fD-@_^WUB2}B85>02poI!jYWe*elvhE&EYi~0AJ+x(^UG2Nw#5=)r*J(0Y#7G_NYw_X+r}A=Z|RV6$5kN`1+VMh{^b2x@2WJmzY%xK5d-1f;~Y2PS#mxv;@a9A>=5oh(b;3u)U%Hxzas1D+~M@V0$lrSrnfhhFjL?}gSObQAB;+E*0eej%ReSR!H9h#8D@@7uz1VI975So#AE%7%1(;*f%m75jA{L$j~9HjPH*1|^AG=#ylwH@--ksH;X-1MHgz>)hng!DYWAV#*d@<tMrn0=eTcYh7yDTvVG2G;5DJ9YbS`tn?`4v#Dz}8eDZaXrCJiGufKEB>@#j|QEcosz9yVBqz9E}2T<)6SiWzVI%#Y{pqXgx$-sq{zDXS)G$#(k2iAqiS{VFPioPiR*`~3OG7p;gy|N8QaOHo9=+Q+50OZpYO4JA1+IlT8Tw#xa>kw$-qccQHtD?mpETsKZCx3yHqgLyx&>bgwXZq9s126Pk8OM#1VnINHhp}i-u8hPGusrSN+WS6tAVWd?g#tN2`S}tRU-+%n_UsLDE>X%=B9)66sCiZuquj1Z&+k2{YZHn-oW1h0KCu%VXRsEg*)};7{TE($}c1=A5(BZf|TDr&i>+Rl)ZQP#I?BzSLFN+HV``n$kk44W#qSZcFv}<%U(7sopH@s(E-rm(4HM?e!O~qci)!Vlh-pkuMd(ZicR3mXKpCL`NOIh*b8nfEj$1^Y&bNgMrsrRN<ch~nD7LrLj_a5(eod|^2<@5}N2#cE&btbjjmxMoMtCh*mF$yjJ7xgy6?<GmFEo+qcor<Z@cXU42ITJ43!u)|B1$k;)Oz9f8jADNAYesIJK<V=k6QoQ0{&E+Q^GTD0F5tPDnm{jqE(MZ!re33lfhjk!5ZdeFFN>1c=>+FhvWB2BI<?$%<Z&PuO)dm(6aGe1D<;8^RTki0XnU@GBUK>u?{_@^@D{xS2+kco`ec!f1Xr~Mc%>9SveSbK0o`t~22SL~>j(yez(Mhv{B$Eb_k%9*vBLD@PhUR1{?p5sFaMew_(%-9u%q#^xTM{K>z@iv;JpS31JhMYyQCn|=ldeAl%bQ2!buo-$6ZIE?{PX}Y=lW*LUw%+$kuq~vMrd-g+9@H%r8<|^5x1Tt2Mp6YZVii*<yvEl7%x|eGD5w-#b5KW~s2%>lI8g0>Av+sKl6s$1Ku6ak8bn0Jt!@8fH4X%Nl3xEC&0i&uWMpy%qyGvcacWx%$-#C2$SH7<6Fl-P+Ff0pvO;90k6Rf$|afk_`}M&PiR;;X|TRW$koc1smac(bc^Nxld(yCaQFYts||EGLr>#E;$cSLz{$hOiP(eYJ1z+0XB<3?Yv=SjB$Fj+*Eg&KtH=1(1L4<H8KrgQKU*x@T=)ETw8Ul0sx{_uk3IFg};*{)C8cgtK@vZbAa}N1QnQ#jEIYFLRA<nt!OPeoQ=!wt=~jzdYNJOw(^Vt1WHxB2=bGh?$L(>;Jt_CH#Rd@tG2sDf&)?qVY{dUgX?z{jM?&@L&$n%^GC>P<w9M=mSa%=8ltw4o@)~93nF&0b-u)>kXl?arjQ`SaqV$2HSUAtRNPn2&2qDp5}OsPJ!XrLLqiQ_kih$hfr^iMuP}O*(ZN}m>5=hzXsi@flE`Yrn222)+R}%V0lSI_4aI)q4CcvPpn8H5jxKLdpK4`DD2vCrd~b#BvUEP|6FfDTn2aTQcpL}H72hyhT!CCAFLW{HeX`<Z$2Uie=oY7zU&Lco`}nkI7#=2o$XvyB-_izL%>d$j$L#h#ZznN{vlW`EFs);W8>)PiD)q$Ni>IPAECfHVe1ELg)%?FdsN17D=03NwQ?#IP^n!z2+?+Rial+T^&I0r@WQMnTf1ftnXdPeN#Du}F6KYXla<_;43AcN3_9R=4>ovR3{4KapqNtpxtijlC+mPaAbxwNObjugd35yXNA(#lj+xE9$vo<gDPeHqb*N25xQ1n4q>W9ARi`&RE(N^XAmmeq%N9*{oCT1^=J=Wq2?7dwqdd=UUe`bvL;*LtOc0qx7Y|ISzJgy<L<OLRK;(-dAkjc@gL$eji9!6O}>;PfODD8*lHx%3ex~xpUF?RBf#|vY&6n_3<-5PE1vE6Uf$LzW3a!!tk8tre_hIWLPa*$tNKK|2gboAM4Vf@z2Hup7K-wF3`@ita6oA<>(u(y$UfBVI%Ggd=pewzl3!D4-TW#JdSx@MpSP*q*|{Q1*jc|U#p<M;0<-KalqMsQhdcCR<vI{5r>f(Y1<_n))@jlAWCTtRCi%98|rJ4Hx4gITs@kp^IjH_Nj_$5;cfw>mT_FGW~F1sC!OD7)2nGb)ed?B2R$nlgQAu|{A6f-%$(aql=>FpuN+gNQb2mfa+n&JH2?%eWQ6@vRDuYY+%~6$uF^g_mFM-ByRQ3msiHkY98cvNh&#fcNrqFTeX81MrjiJwJ#rP*QFmt!XV(oIEMhx>Fy|@kCE5iJ0OoW-I7Gm@(X2fct~K5*qQVA51!5JO<(Hk!PVn)=nYtIn(5&C|!3nBebh;PGz+2Z1;3If28s#;XXbm3Kr^455i~&KD}k<wKe7p(ax;q4i^V^cJeG{$w$8qH#gD=C-SS&-ZhiR^=&=^%OqKkLV_SLJg$=%d7`v{{iMrAo%Ihtr)ft<kphRd#?S%bfH@hf@s%s)cdv?L8i~*>-^E#qov}2_gN7_$cvuUlHVXQG5&%0fosDH?v!pyWL@})SV#8UW0Kmx$@|QUsuqgxOU(b*%T|yg6_38^%YV|Y&<&Yd&Aj=8X4n$e1(V@EL7*2t)c>_OfW_%q$>XfwJ62f%aY)L$!XE%(`I-&%qTYVH?MA&;rpeDtFN{3G}a1TrJTLG0PcF11UB-rgkT2WCXu*xkBd`_pPwN1tKDuyg78&s1E14@oePa9uNmG@PgSt?0kjcehff+k|r4Dky?Zg;3k-{IG51QvKSwgTQ^t`c97`0>M(FHIUY^CG-3WrAp)hf9&==0$bOu&k&IF3~<hnT&*+B<kEC5PrzCq1)yPAs<UHA;HNfqnfR^3y?u@A%+3K?QKt}W^*ML9UWfbN=yh4$E#@}j}~VOgJPM2hYa7FqLX=$qw5KKkk2w@Jpn*s^8`CWnu0lf+Sx5x((S%%<3wDYZr7+nDFK@B35|~_gV#RzWL>GaFN#+m9kQfzX0JX9(<iNpPu@`=NnNkne4>h=&v*hr`;g>kP43{=U<W##;8(>=n@LLw_8MCmP?uswhXf;c6!)ABkRm$T$)z!{o^H?^`Mq~4N|vP&caDM7HjyC9Agc4w6XOiP4e13|1)+xQd&*{x&n=vlphiWDsAN1KSNtWN<g3uA-^d9k@rrgRPh}B14UkgfLW=qOT1gbsp8BhbaZ$XpK7@=4q;|GW8LY^Pe}nMoi?UUh#g^$<j<GEEuS(vD3TlR6Ak<*?S_^qoG#2y5&0*B-WxdJK>m`WSg5-D_^^_P1fJCUMKTq2E3{~D<YYX9UxcIO>a3*?!_Mn80>y&!|XU?Xz+bXWtPV|Q#KK%<T;Eb%11bDzL=1m962Vl#*550Xjk{ShYxwoIM;dh19tzZ7ik?5d9N6AryrE+2TDFo~jbVTx6-+sGXayg{g3$EVg+=3bPGwMZ>cy!%or-iJkP}era2OJ5!vVE{HlQG^Dx7HDJx;L=AZ}nHXIBG8XuFsO0{6$Ow#ylh$Vi~&!a25<!Bo3!SMrdJpVJ6oI0wi|2o-)h!G;M<$;Qdj*gcV9E+KhX>bm?Nu+=E&Up5b={jR$a*G8Y&G53#@=7U8m(vpuw9S|FE!zWhd4LOls!@M0-pK^!zWY>}p>0YKz1eXLx|LB|sAUFJKjd$MMTH1p6{k)`&5=KwKBb|@$lxgfl<A$R(wocM(<`7@(-kfQU`7N$f3{ydsg@jvKiGQy7?f9TXh-}PzeH~fH!K~RPrO`b!-FWurZXMjXQ2IUBj9dK6%zP!AF*QSoWJTcd{jq*DR!Ub7BEkMJDS;f`Q!zsZzx%Y#Yc+UikMF`|y+ZR`57=Ns>bz=<HawREw;Nw`}#;doNW}EAu3RYijci`;Bt3A2;2yo8K{EqIomAS;uW8OWPg$1hwNTs&&#a%o>s9r(AX9TS$yLizMe|JxfKeI}Tvo3Pnni<ENT1UmCpk9xLJTwM)Qj3hL$X}T|MhP4D_S%54W6}zs=U;W@1^cY$6KZ%Im{A^D#^+|{(LG@=W%Mg_!nI=^!XZysg^I?DE2a1eI-6n%+L&8AQqZ^9<C4Jn3m~9=OiADVfEiK%4%G_te)~&)2jCDASPZdERTLFa!y0yp`ue4+ZpI8@6x65LcyBVZB@e2T0f?wfufW<gw(k$Dba|8?HcfIZ$fDozBi0C;DKhbc-Vq1YK0Ap4Y759tq-fDVK7{71=5)+EiP)#fwZ?WiWrBON$uciEGw|mj%kQ$wYxPbs!puKNPHzVWJ8VO6sMt;I%0ZSqapp4I2;t+ASd=)A#u`q}o)Kp5JQ4gdiVcyQ<i&8;s}3VSz)d2IJYhuRurcAoJB<P0=gUmmLMcglNa0-SiPVA*1=Ks{${)AJ7$PmAl@#%%Bj2|b76FF6ULlrcwPq2Yozc!^nuQ|PnfDvANa&r|83DANrY=Q9Jphpr>-UI$#NK>jhRfL#Hm3sb8LdIWZ)&F35G<9g?)QUhc!6S@4fU*F2pydTccwKz_SF`(sy%EELHpTgJN`x=NuE|8<A`v1%kWeMGe5R~yZlLg1o^4!=5iZ$@Ld8qJwp}<D)r)w!c){2Yv)3Vh)*JPAR>DKAx8Ybd!d}JENtTh#rEZPonkjrhG+8xK6KAVZtfG@FT5yEkSPjR5gnI7yBJxAoiB(1)xHY#|FgqjG93uH<%-`Ln&!=1`0&9A>~M@Oq*Kx|m$ei?!4ht;fW2f?Tq96&j*>w4M|{3X^)}^xH5KMwQ(CjT)P!}EfaCkw)l)WJTY#o}1(PFhCwMe!g}Dn-+Zi27ja;&7FF1s`_er;|6LIOPXSXl{x6ARVPsF7%I_%>1AQ+po)f;~0i9L_7SDb7$r3R*kJ#Qg+u%^`?1qSw84CBnZ8)vugM2MoLBEW-#QJkg0vGPrjR-PtmvPb42?(M8r`OuK`S)?)`lmw5s*9)G!vp#V!*4yWNdM9x7L}B@2=mhCgiENO~1yRo>)%k_laszn@GPpVHvZ-uP>x(N5xD@k^jvjtbG%Lcqb<)YB52`|jJ+x1!T!uLZ)O6^eFJK}Ck6z=z7%=5!s8a&|n0*j$bGJl=%#CsdGe&#_SI3iS{M&KXH0q<B!PXyV`OYUb)2GBPM}7=u8fbZz6&{+CbhY`d-G~N3%24A#15FU>psd~S`jRG1OPEV%Up!!RRjTet36!E)zVH+$^I2ex*6v##`O{eVG!C$U<{-s4yZ*xo<}P)UgRkISy=}+uglHL<O3&@dcL1ZOhf0$2VtUDi)hMY`59b-k%6eU@?(4FPm<q$0MM0pZgL=}KIU*UEH=lU~^oqePu+U}po*(m+UBKC~60bQf(64Xk%jYyKa^Iv_4Z_u;CU*RgVG;s6iwdE$4Qt((L8G`?EJ>x}Kg=kSCA#yJ1j3@)$Y3?-nTig+uN(-z<NJ?BSTMq49%2T>2>s}>%g6Oz<4MyjCE&gmM!=(BEykFH?9KRN3zrz+WV39EpePaR;08lxH3Wmp1XT6kASbOo>MTF<;oEDtPcgF+Y|D7H$33eYlDq33&a>Ea!yBP5CejHKoM^@q6=Ci88zQ)hNb%Ugt?K$s!rn~SZVV|4Q1hoGn+W;(=>bzApH%HQr?|aU!p^4zx4+C<YWrH@S)e;5I)w8D!--b~^1pD@W_*T7erunQJO$8C>Ym|5B1j{-HReP+S}2ES3B$&8D`&11c&vQ^GL_y{x$QTpQuZnFWT9gK*&gg@?y9Rh>NZ8)dE0z%$|(5Ei7E=~wNl6QZvNs$GHc&agXgJR_Rz`&Z;f<q5G!&-2LQy2Vaq0Nb-}S`N(#0;1g)271{aNn8|?gHTN?wixVDnrtKTC~XyN*9aU(Khgmt<E(@IN1$zDN#d~sERDGz2L09-`mJ9V{`LFYMxP@M$E5tJ)s5UR9+>vz%ndGCDN7%MhTth2Iql~<g<j>$HdLYlR0&i+7^ELa5=R@x+&B*HqcqIG=Xv8&^%+<Wcyeonj-OuXCnkuu-UEAfn0o|ANJY{*QhfI6ne_grgyFubrpM80WWbtfOy$4tRg31%`jZMr-G_P1|HDLn-VD-d|{+1LI7>_{V|H2DliYE@N^ZH+nJ-<X0tbFilkY3Smpw-??rupvH%5?toHgu;y`hMbh00|L?44fKFEn`KU-5bjP*MRzyPlje}bHtP4;t7)zgixMf99=5~8`EJWAms)=<a>y>`P9B3jR&1`1A%CpUQJ)wa<yD*K?S3|Uly<pEh6s2aNfu%YXS?WAtiEGs9F_KEDCvvZ`Euj<In(?dYBkZUY>hIkpQto5GGq~M7q_Ez<U<xmX9<q&lb)SCz{NMjG`YI=fgRa6V^2_{Iu+KC!Z^8Rxs=s0ov9dfu7x}GioTAXvJGY&5E$nX!>T)Xf>eut5+ORuoPc!O_~4iR)bN#1Dvn|`Xbw_>wzwXiRS*~pWERkopJZ~{wwR6d07;)3UuQwgS(`f~k~Oectxy*>rp>4<BD27w0EVyeQmCi&#gxz^ys$320X}@1+4Cu8T0p7Z6&yT5XQ^UbF6d~;H35=BT(kq=x~s%?Od=%kB4yA7@NmjAb|?Zr3++Ko_AJo)(Hh)0?qvDhQ|~7tB=R9G*Szz#i560{W)*G6+7fwm5h|b$LJ0S)LpDikdva*|nTG7?97!OK@Yxo%A{^ir%K6$EoV=M4aZ+lZcI4sUP(4k`WI5m-TiS??Hxntc6>l?Mjf=Oh)^D3ptdvpL1PGC|ye3e7Dk(RTdC;j(bgasGb!sYI1so1ok3F+t_WDT?T))N-3NXi?fd=jm_5l~gz>4zcZC9Sy+HDEbtBjfWA_roF1a?bt_MOaqpyfSmZ<iI>x>|2bV}NMwxc#KDf1DjgBPgI^=uS$57E0Tc^Kb)u_nY3&DLXh;hK2NsvY<cE+1sk5C<Y6zaZun|8lrVsUo{W0$c`eXFn!nLmt?rPf|g{HQNVYXwuc_=i$RsS{$m3Uyu_SNviCJowzJ`|l@MCOl_^@9e?3=D8n92biFyM>u@|^tNOj1tpak}Rl8!7pTF=L$K(35_;2c())ObA`&j~cjR4Q|LMQW`gZJ~d{DCF|M58H$=(SR@`r5Kp7zlWB-J;<Urslom?&S@Yj_!5o4h};8S6n8WpUSta-I`3S}+_!=<_N~+g9W_}w=@Vx7#?_SrC;wJzXR=i5KEqE9JI}Uezz?XDG_X>I&vkwWhH(U)E1!Y6@w8`|73gOcE~`yy)ynkO6LsT>^Q{(UAqqL}l<Gh+xV3oW()F(ArtVRsWAVJn!2itpicZX_uql9B8s$)^mAK}nPJf;gWJrl<Ph3|Tw|!GmEHWblo`P}f`8DU?Wt;p5cn{cDHGu{}?4ZE?3>X7Uo<bWOzOF5V2PHW=rvkrubgV`(Yvx)yD$r<39jP@Ot~iFg;n1995v^6>(43D=P%ffVsu7#lL<%b&y_X31*?}ssp(7+t9(;&vkzS)HLdx0VZx&&gZBOT`I%r%#f)2z|cw{Z+99=X>N3irT1KTyp!%`L8NzWg>5&9upWp<@8{UebH2S&ouk&Jflrn6^Pg~&xzv2vGU7Vhg|=V%!*Ah3?AfTVqOS3aCRXpBSvbh=8;KB!}rPc4EAI;l}4`6}^j=OwXsI*ZhkjM2qIr&w|{h_oIG(NB{(_fA>yV=oxW41_P+xnugUdyb2)Qy?8ufEor++aMYP@{KOk?eUaoPll+m4HyL`mNB|;arWmqA@+ANTOT?IW6(gr97)5{YEMr}h=(<!aU@DtnB*s0jV$$)?1`s7Bb=(%rCODj@$7t%9R(8f6qLGx`j+?f{B7=O2J--td&~!GISxIkHNuPn9rIKtyi2x{PsXG+>;OM{2zT2YJn(!E@PGg^g+vW1V!)P`W9ZbBB4xOW#mkh}M6G9bp$#Jbf#0A@{0-+A#5o)6>~3^hQ|K&-tf;5=`xMiihjW#qZt|xL@#oxBAcm*`q>*4z8=TmVbJm4TY`Y(>rhxH?f1)|jNJS}k>9}bkzdi30rp2nLEo%f{xdGI&0AT_P$WfP!$d0v!(4u6qL{Cj%Q%z>>iS|4+9A~8h9CYJWXiIXr0gp0+U@6s_io{J=ICp+N_bW0DC6Qv8Ls>hHm&*Ktop9It%u>v`b5hr8Np?#a-E-sMV@ZXes2nh*(~cC=%#Z;a#mYm351x+SZAJY$HNfeTV8zZGK}S|IJ%bmev=u<{I*Y^PGoUunn6kMkkWTb;t`^hX&byo2vnnOQtBgJczZCFaZ%O34IV=480zxeX(Etq?u8<IcXF#r*MbA8#{8VE{f+9K?$%C;U98znV{%x`J>6$d%o4cA-1F$3-iR}ypR#H?_db-Gz6p1u$J+)m@=4Lc?XmHCne;3C^R@IDUY}`p!OoMcsh}YlhNN<$uuL<?|kafYQF&2xkRX<J-950qe*R&<|n;e#uQtCwFDlm1)V;idBgSznj!-q-}K;Zm~wQv!VUCoQ04Yk-ZcQY*zZdi;M1~ipuS_`LlZ2-G((z4o_2k3`nq6frbd-Cdtq1nULbyg=itp++*wJ0(Qv>Bq<6{ONYF9f#k7kTHd4jfo41u+O|8!WYWRNe!fv2bE`{WDz<rRa>yC3qWJI)k<dDDEDGvB4W+_c<EQ5AD)kwxjzRE2D9}=SV!9V(2yC2zU;(*S*LJT<2=X_tnvuV@w8{Oo-aq&AJ&9-_@!?w>&?zk&mT;gTW7XwwD!oN!!}HL!B+Fi(zD$1fo#rLWXv={<PNf@Gl2@0lu0UkPPGl_{Bl@{PpFmq2pbqCouf?$)ay!82d?=-Eis?D9?h)F9laa$Ol_{sV2l>L|NXFgEnP0Y7E&ux~=9y<`G)^cRz2!t#wFc>L*Awreu*c<?c++FR5b?box}G4Q1A{YY!X~%Q?G4){+qTA7qgZRoZ|?nu?RpS>nBkvtB3g2b0FaG)kzE>t9@Ct4yjII9ll;;w&jbBP&+s=IUL2tK6J}kC6n;KQG%P@ELo9?>iSlXKvs)wxT|;(^I0;?}!bn9+leAmp=}EkrY#Eb<}`kN%zE?7eE&(k8uiwap)nLJ_)LeO1z+6r|Kodtrku0gS22#^P>MtDOEjjz(_J;7Wt=ePQhC!=qp?{%`&g|!hg}Ia#4xMB^pWfWkS);8+o|KA65R%?6cG7-E<B72%a4Ea4Q5yw@(h2Ds8=Rc>MYWAkYKQ(x$*uwQh~#k4J1U!^NwTy)y}MWqON-91v!}b_rKt>U8HEwS5qfA$gO1SL>?q4T@@dtko5;P&oS`oxw~SfPPtTG1@L(b>1BH#|Lr4F__>83&PF}4&h$u?)8&8@2yR4Na1NLN{oSXG$bDkkf$KR<OjYFYUHRUm^5JYn@ETq9@J9^k+O_IMX~>_3$IO`7eIZ?v~vN>fKP_RKmo9}!!&q;Cs0xs=XQj%O)-NU&;@dcEQ3x%Op7q(*oVSlZDZr3uPzfAi}ip|8;z%gDFCSf{HmdRww-zg4makWNVckrlmArIhN6To90gi9IV5rr%P{yHUr)V+WEborq6+-fnaE=p?g1(Zd*V&XA2}Y6<-#1$%J0<^f8b>~BPPuUKHG32moVkyHryk+dFN(JM$={!uAN>yW#$KSA_)Xr!h9Q5_s-vRF3vYLT3(UC?})`0V*pt+Uj(PTP|a8geciymxXdOtvxN8HXI69t0)8emO(pVXQqO)n<H;DxSh@SwlxP_*e2#mh&WK?50TNw_{W?NS3kq!J$i}Pm1`pdeluS)|Ep_$n@)MnSaR5F_n$ySI1)L3RYKt#Kwg)^k?IS?vn}KL0T4;*uE<#a(dX&0C7NoM(f~>2aw@j<D#358(PS_1m#Clt@)Fn_8<KuU`Q4dt$xbQl~%3n~9=<^jBBdDTz4bXhxWB@9SpLKn1<yo+qPrkCN(jR%IpPEkW=w4+_eDU(N%CAstRr_mv1-#<PQ##L@Zyk%suqi}#UbU3rs0ABLef7CY$_4MC>qfDR`D@=!U{+KtXGI_i`}jq$lr2NZ$GCGo|5MV@2R%jvX;8PSNNT1%fLs}owS@>0BHsn2+vvzCgP+G}_Rri9^GtO&;<Jlj<OXf-H}!q`@UR{_d}wg~U<EcP8TD8Jp3lJ1mZ(~4^IN!6z~9-9=7fg4e5e|?B<tanJHA{plxg#sQ&c8o*Mz-i>L<25dK^-xnY5AxDhb&_D-(9}CXXNta<d)qP4IxhYJ*VC1JI3gryF6WU-}??#{y96UJ4xK8itzv2qyrH%bJj_Xj01Fqe55iqi*7~8PBPtkvvJ7R-M{<s)BvyhxAzKV6?`yUx33?A+k@WiYn;pHZ~9GP!e-1xyM4$Ev&^wzq;FInD4(CrrxNR@qwsRSQ9O!U*l?=i(FA(7k8gXP!IS<QIRX1(mm6D^eLAD5)q}S?ne>eG*_q<3n_k?qgh#=;F6e7Twv4pb+(&V1~GVTn>0yCEtE~3FN>E8BVN@u;Gb|H$A|&8$2lsN(Ho=}?hb>>BMrn+TuY_^b_`dH3Tx_9mL(zR-vu-XiLsRpgt;thCMq{^YHyJ!gqVEZpdj^VRa?di#Q_@B#ZjZFF~W2|6~?=s3an}p!YD<G9FK}f)P-&F^9{N|U4o4>_J3iU@Qd1v6o=uL<i1>c)N!Lr&$C$8bL+zn5bBy!f*fxP+>(jGw{FjieVZzb9%v9Lpf;f17<Q%`G@EskwgP3mj)5}r@1Mn6p0N)S+0)=i(CSx0ItE#+4$_+`4CY75%a2;yns#(1!AKUm{5rCCG50OZ+Ao+$R5}4gKFeV!9JsrC$J74v)`7nS>I!s97`GX2+TTJ%ZKxP~)AoZs8RMHf7eo?{%&-MFHO$m(;lx^sovc7oSg6fU6yZR)c3nUackx!J6PTFC@XQ485kwr2Kgv@jbmi`7VWa3G!2=jR!UmI0s<p0i<;f6Rti4mHD*DOr1oD*@QR3raIW-W!sd%9K<^!&Uyyo)D0{JtCOx5gMr~c#;^N9@aperFt!}NC4je~W9;XS;3Fl3bdf;XzW*;!TZnr>?60$gO#uDTyPimvv;F(Qs;PMRyl>gimwq+lM_y&yi}`M`4mj?zJ1htYBbSIq)DiU<NRQ^1un`PB4-J=hG&ICM@R1UO(@=~G@CxKpMY!^z<W@R5BZi(rngHxdqmwH~j`(8f6QAiOueBn{Xfvno`=%b6iQjkAQuG}fyzr}FGxe%ieRB$2oyv>o<T9OSSgOK>Z278Y2q?mA343)4r+LY0XU*5^fr`i7he&VZ{@C`!XZo+@lM2^&ruP(*|ggZ1<zf(WOikw>j7)C^@@!M+4}m6>ZUxA1J;lTd8=!tEg!1o7xAWiy=OfAE?ACq6Bz)J>jU!5#ctN|6FQTCk-+>;@`eh-5!kqcamZW3o;-X*{BbYC@ywMGAw~mWn2<cz|kBjIT)_j?1O-nW&KT-zbbgEr0tyAs^_=a`r^jM3-2(FKcHi@D^beYCB%0?vZD06HG}QRFVU3Y}p=AtlU;wW6&69<p9O-s0k)b{Xu5yscA4}O9*|lDy?UIiUx@U3;5EhowGwwe%)#!V*ePpWV!;j{28gm`JgLt4x$HnfqFr1Ak9o{2i$=Rk7$0uWgt#;h1<yb61~Ag3`LOY1E0j=+?EJkPP1ngmUOPNCK;{PptB9LR));u`yYPiQes9~@+$QT&+z>=+n^1-zb(xcMX&&ytE5m4JILx7AGXw%8y=Jt#3^e;WR>8|wu?bDS?GnOE4fhA4SyWk5F*zM%gP{?VyCmpV`f^u)tKMk@&Q_=1oV=RUeMd52QI1H)$$*T%}~nEL+W6jR9&=?uZ6oYFkMvc$URmlbMzH)fnX7ADXZ*vJ50^B!qu%|HFYqJkFfE9HH)f^`<fP>7OHgLiGd}5gKtCM*v=>cbreO4WIh%NOVBRAvdN2a3w3JHcCoMxJCEjF?<wep4mou4<BjE|bf`xUz*E5Uh--?~gKl-{R99zsoUPDO$Irr_DDj6ydjOCQ+93dws1Wy$>4U(#<S&{kyaSx;RE`qK1r1c37@@)?L~$V=I?ZW4uI^czj_b?ME1NdS<<)I4RN}bHPuQ(5uQywm`}0k$p>Ji51)|Us-~@xK?hU9d5@GO;6kv&*3?V20%@ht}pc({I2-f8asJd<$z*0Tm-t>6(-r@j1y%UB`^Km@hZMRG#soSl^#&AsH<znsHa_-c;aP8H5FUY-w-#~hH%`2dSzr^HAqQqV`eQvf=B9j5Xy8GxNMsnrBs6DtT(c+6Pn-p=uuap74p@oQbPR->@`$%gO%zXxD3hJMDoIpL)ziG;jT}A1KfqYJJ-U~dZ@1OpA<HLIV1`O`gt2yVg!&1XyJZTPZ<?9b<dcy8uE9w?&!e_#eJc@FlwoujdvAyN0Ts)B&5{6s_DuVe)%AOE6WC#4!^OPIpo{Le(ydi!Hr!9dz+T`%32lxOzRd=sORGx$41(+&Q)SY)4b<M^I#MP4J@)=Ng<B)c844f9mlrX+7$f;2M-20?`6dotxkVPY4m>e5~dv>xew##Z}pdhNcZD=v-SS!)mJ~_LGYlbBs-q-;*rgU82bvG%EJvWeF3NJ!YZ5p(oVSz`~^3=#VWRn8h$gdgi3F9#v`L}@N39GC*aiwE}<si^~d|gmBT#JSO(!JaI<W(D(hs@&R{Oa|k6NJaY6;uwI>E<wnJY~!_9VA~zDYqJ`#F8{DpDcMQbFwK8qbJExQmtOC42#uqO-_OLQB|7^!B_c!YbQpP=@FJGkpU7W7mHU6(-t4`!;YBg8-!ZT8v_xe?I19}{6>&&-EoLS0pe8?e)D;oBYhd|h+LrG5(eoBmzsLd5Rzj$NTonhwJNk<;}mZtEY^txV80Q(Bfu4cQA`HJwS`7|9Zj`Ct&4BCAR7;7G7+WVCdQ@SUePGC*Bk1HI(sasnXZ(M61YNDH$b4-t^=9VeI%KhSYHA;C9ZPFD~lafmXL+pB?>wm3wncsb|Auw6P+6OTwGzw+yeMA)+fTZQTBkRYer#-0gYZ1k&4YEu<kf<KXy5D{obZ0EoO=l9w3iF#BOT*pjLYGar_gHKWlta*<g-o?WMC<8NEmPA9q80nUO5k<doY0AmW@cV9^}-EO0t4dY2n4mb+Iv=%a=;P1u4)^riu$+7=PM#lyXx;GF`DqG^L28Q-v4Vs|gIPInI|q!t4j&;h)WEYUwiyavoEtjglxvd#x7I3qQ?D*5*o_Pz@@jY4^Tw&@x4L%mlJlk9>GZLu%qM;SN7vo!P000(D6Pbva#j{*R)?EV1}a1Asx<A>i0cm>fgrtm7DX<}$+3?qA3Grpc^%C=F)8d9P+^Gp$q(&e!z5cRfJLmx_%t)y<IZp<4U^`JQOhKyIay@B&^p~>Y18Z%G_fI|V98cxu1&i}wlPO%0E+W>*}ae36VfI-XAHs`s2$LNxMwJJZ}n#*EJ!yR@NCXx&MBw&%jdm)<jCl#Z6cy=+$cfiB35Co2916K6M@<Uy@?gN7NrF|)P<|VwSr@EpMETcB^MqS}9$e#Nyh*M7$x!VFzVicL;v*J)0ZS&!}+pSMO&V8mk0c)oLO#+(-%?d4U#HP<UCa$W7DVuLFV;)Zr*#ye#G^{yGmj8FVBg9O7W;C_mrcAg765B-?#g!LPn=<V0la9n@K$h)iJ*OswkP<ZlE;gnmNT9gE2=lfaA!w;qBrT2Y%95%RhsQ0F9u`8@<=jmvDp={fv=8QP5yZ0!XjZBi^HqJkY}v8otZ5s!nKTe$!U8lAdvnkOZnW#LiDy!~I&)=#ZAEcsxbrz5tp;d7yCDPLrv|LF+0<u4L~(|?n8z3DS|(h-$2kT;a~N^Rs*U)mG5S`XwGHYgvW=)^iAhBftw)4lYsEbb8=9Mkqh3z^N+>9i^#Z;u4i7A#0^@kQ#d>%_eNvK*msl$Xv^cbS7KIV!vEGPL-K(dZgY2ZV>-S;c7#a{JjEo7LUbbk<DQQr+)~|y*738o>Mb}o)ND0t)`TQ5jp-3^?Cl2%5qBW!Llzklg=J;T!k-M{=_=19SU#b)9H0(%*>+XmaK~?C1tJ5o`<Wa_jQ~@GkyH6a*jclJ><Q70kSsP@_LEM&N85>t8YykmdE6Bk#XV{GAgz@`?7u%-{IZ#UFBhyF32BaJ(Hp@cbhHzW0T9_%lsRzNBj6TMsmsYVwnRtwj9+O6l368N2Pfh5P)}Rw$sIp{D8pXg>XDPs%yb^&{OIIBcQ@<z_9BG9qXF+Y4+N4$AJPt{lQpl<8Trs*8Lf&d;?lP2j?XfWXG<MWErTz1#UzoBtb^vj(tkz-E=7g@7`L9~p7fO-jsUtXI-y0wl%<2$9b&w)6Gz1#wlsoZnKeXreQ0^TKYJypjN?4T14qVDK<YB8qkubvPfQadu{xLvyaTk>FHA`gXHe7b30@+GSZI^!WRtgmgZQLs>uj8KfipOpn1(r^sX@3JAC?|FW98cEkDH@;=1RPZCpDI<Wo<u|$hTCFul?|BX1a%mNR4AjM8D)3#M?)WIm&<q{dpFhEiLtyb0HeDZUobIkH3i~-TogpCY-I5QcXRHx9HyW;DkJHlGnUVrRRX(mE!d!ERd2<@;!+eI>|v@3Dy!&?L~z;0oL$mJ*5{@tCTO%WoDAi}skFc=Tv>NphfItCCPs9W0Wk&Cc>4PJkL87YqMov{qWdx2n1lsgFl|o_AE7oSzZB=rWFlW{Zn+}OQ%CBcEVjQN`3gPa2y6o#h^N9OP<&cc%zRU~5{Eqs7YL(V0rFJ<@C8CNWet!s3<T<8&O2@3y!Yl?Iec4mE8~r|g7z3cgEfK1B+bgG4`BvZkwd%;Z;?MqV2>!!irg!g8iODS6qehCt9`bhc1SmAQaT!0WgwQ(5*eqcKix|(=q}1Zm2Zcd?T2iYZr2IVL6J4-6K-QFmztuGk0A6PJvlVW$(D6X$JFjGyV1agNNggB?<J^!^b-G=nm1ZE7AcQSK{%?s@~qb?3LCH+^?>I46c~pM2^0_y_KU}S2ysvwaf%GRVHx))d0{;J3LKDOH#gCx*viM-Qoptlbizz{enJ{=e56KfT5xLeX@jVQstlWIQqb%vAh;7XDhRGgui;k7aXay^^xPWt;dKZpgXe}1*#Moujio4L?u#3qzv5K8(&Fz#`6XqmRkKgwDBpDdzJ@3+Bsp`~x+_Qh-qAg`99z`kabMpYvcX8ZS(1nZsS71ZjT&J4IZIoSXQ9L*RlL;FyJ<xrgT@d)Rp|jXU53!+0V!!%OHctwQdp_<N~g!4$+me2kjj;y(LpFGNVK*Rlk5~)7rZ1}0a(C^M`i|L%qC<zg$7@VYv9qsH8>y9kflWcXz*Kb7gEVy_A1lBlqbEI?q<>x%H;Is-+(4jdr?+kLG^se@^9hf&`EG5%F1_J@fiWzpPT>ZFL1q)jp|tymOx})#JAWdSqtwH%7-DBLLqDe**%L*p^Yb*)Ch2(H0j;!l`}48Et$8BCC5)157JxJCI)N)VHr$C7Kr}n**D$TmYYIbhPyDrh^jG3bj$gnO(C1qh4wK&%mHRQ-BB$=GhGa$8X-CbMcuC=`lUrcWoqce?wXran@&{rR|xu+#cFaD?t0DM;vC{G`W>(*sa-H8=w#EcY=N24MI$wT1Q-HPV%mG>5R`bdZ{LITr7z}0X2zIvG#HaoR|>eMqVF$`C53=I);91G?X-<Hoy6y@X{8```VAG5G1#DthdS{M6x{6}@|;mfY08aC2d(9CC2*LEO4ws7xU1JZ@;Z12y0<=4?E7>GE0Tm#;14-*D01B|4s=%gJ`0<cPm%&?Ic)p@`onO&KwOg8c<KGPMeoLQ*sU_*{FQ^Ym32l!lma{B(}V&>)Bxzgq<&ulg`)%GX~h@!GOo5YS-#Yc*Ln=ostDC}q3q3LgIQdFq~=m26tWVYyy4C2(6OnXIYeP>NBL2<2YT(3JPT!L3nn024=NSSp)RBq@*xpNab`8OONV|o<LTP;;L|O{7y1$wh2fmxlmqltMtxUpK~q|U7TeyCs>Mcblu6i9c7RcVe5NjUV@y9Z*f{#63Uh6uwo}uL0_ZowqCg96G@9f9Sk|7#ZoNQ4(X+OG9f%mvInTVV5vgUM&gzgo<yc3l-MzG;62<$BR_rpl-{p#bGC9VjNGNj3q#Th|U-2xQf(oxm5r*|8Prhi~kukSiwnChOV5Hz0^YFd|8&B)29*v7id3V#76XNsbr7>Q`_}YrA#tjpIF^&c81gsO<dsIoZwy?KiTMJeJpb`oX3U2Cv$df1vd<7g#f#ZfimQh8wC>&aQX&`;-2vZp!Ot>hCOvyEVeH=>>w1RG|5!uvE>>zh&KJMbhDfAbUAc=UE;3XF1wdf#2fZv6FdK<ESfqFN-I^?vBz(F2L?1ZEQbfs?9?Nvzgo#4$NN_|C&0?jX-wBzpm_9=^Y=n7zIQz#<h5_nxuei1g?Q$$XAu*$alMH(z+Ov1b(9w?kIBRXY#UDOJ!za{Kl{>P>S$_rHaJvcAiO?KFaRr^>60Tg>yW&4m)YkwW-?d!>J>I5idGDP5eD*gerccS6HB08=lbvDXild<O0yN-fGtZN{6ZyVgi%UJi-(VPyN9=m422nUjt?~CE6PidVTjFEI^Khc6~0{N@44vm)pm0HpiS60yY60ujB$~-)8+muimbbaak+@(X^45bQv4>69LWXEaQg99LJM?N(`suaf9p@eTM?5jjSo<h*!0ifwIva^63yg}GMbPD?e8dz3SrXnp0gi=A@Rnr;VJ=4zD4q@d{ILaB!fsuxBk}<!trV2&0C?GzVi9w5!q3YRGqYt;j2W{swQlTd>-9>MCZb5C}_qQC)PHS>|y9B=~hNY#NW=|EGHnTXMLdV=NQE$TqN{8+3hE3FiwmU#=zNQjsC00Bh`<jgu9;PxVkpn3St|ggQ;r`7So#oc(;8Uo7gTni(R><vT)-ZYNN4^}|*26!-D#;n^;GcUWh}heEPS|Id^huq4MIXgWP+9`CwK!pnv1LKZRR!gJje5=76AGuC=`A_pMtM^34g1Q5NO*S8gNP~Cqi!DhT^6TuX)^h8O3Q2EOi3@i9OTRgl_H?=VI|t5u7oJV!;1ar3P6(BPd}ImR{BAhC7b_$KzO4|<&j&`9j<k$$3dT{T|C6f_N;ge;tt=lq_v~;KMs;6xzffMvseViE=kBss)3L4n#kCX2KJ1cIiGZz2d#PD+FMr+Dyqa|sY9C;u$;#&t2xW#%Orgog;G3gmrNz;Dr;%#^D37~y)v9_2+qCc)pd+Wtf4TK;#P<^jQcDpX&rd>h6pFMLoN(6jsaRUpl+DDP3<yB;j1sSqkt1QX~24qmNZB+pxa(LN#%)YWjGANO5%h|qoH?N>Qb|%x7Njce_p1s#~E&8SqKACa8(Y!Y2k3W<4GbUfpKz>I@}`<M+(T?;;bFK_>qX$ce6kwuY#WmXPXn{b3eqP+nwQ^C<rI|+9#rw2Rf9(<J2*JP0jF?z<MlpA;obvYiLsC6d`ku)2Bltx~FadwHB<yFJbOA(zqx}DQC#EVf0F+c-mr=8708_grnk=t4TX(HkCXyt)`T`O4~WU%dk%Hv1O{J6yHYJLX@LYPr@5T-5}MZ%|J9z$R>Doe&bLm{7cOIEnE}Bmd$S^^g|-IbumivX{PD10Tbf>M$`K(VFft1!*&~0pQr>75BjE9xQ(*#MlvjkO%aaw1E^w2S&UX>HK*^><BpVAwt?B?`rbahD)eOq&u9?_Eh0@7PrV_)H1ujOIGbbABF$k+1N2u=J&CyW@^g66U1ngZ5Fv_uW=aS@;wl2Yv9p2H*<Dw@<|ZmZj{t$D$PEZ_Ne%CUpO0`7Hib`tXAmUj^h_DF_|_DK#t#pyD5OJZW)6|r22*2-2e@pu6Tno@427@}uS*N!X;Kx4dck!Ffy<Cl2zrhU>gC5Dc)dHdN<lAp6qdwZ@a)}BlG#uoIt^HkJo&)bNQuy;rAM`G93&fs-|%8aKl}|_Dq)6LT(1g%C;1oKX<P_0Claoaz&Yhgh-*uq>ZaJ)u1q_J?1g|-*746sl%}o^^k^(ap6-l3m)y_YRe_pdoIj-N?9^9G$SdY#0|6RNMQ*xq8jIHmkY<ri4X^ekbd=iwrkG_*!F_<2x^IYWwh}d6q%-4JqUZwkL|e{X7!(xQtL*}dqSi(R=wOvQ(M?W8Y-6cR7#_0Z6Jv%guvl~rE8S>(|Amn2%S3-%dV~_X<B?^08x01WN7b$x(FA0!@l-{zvTIu0p+y?Wl=p2c5bR8RHNhJylBNKyhk$q4EJ#$W?jW`1;i#lNu#(@Alh6iD2MDraAs|Wv#ZvW@vSqNDH!f9=MXZ`(kyw7vH!cZ3FhC(<z<gEi-Ht-HZ@PCin&<;MaTMq{FybYxIg33pFa~W24tMA9@vh5GT5xW$BI&IpbT&6*zyF50Ibu;KU_^`)hwMLf0;)L)>AKA$F|9Smvr|E?h?f6Fnu<}j=WV>PhOM)J6>CiNJz8pD0;`EEOTr)G2jguwI<2=@e?^%qXu{M%a)*btZVm1UEC=8}6n`Q3<Z~~pd6?J@4QX*eQ2obh0|gm<ln>-UZ6JywgXSXZrZE#X_6HRcF+DIO!k4nqdhZFc5Txz9r<!rp1D=FBg+BJ0(Vnq7lTo|1FjtmGFUYeosUGej(|+9*hWo~p6jNkBa5HJp`{^`(uTfF7{*qB@BDN_AgpdzG0D}Y5#ij1uu2rUEl6n`Jg_=^EKrpf(j$Kvu34>3-hqpKllBk)=_UWWcLWhMJKVHE4=vTCFI;9<+jd^s{s;Qvd=?SlgLvR|j1gWE^>eJVh{H9|Uq?G}#a7rk=X0$~pw||7upcSaQPzXe=kx^<#O`QZmVgV?`=<1{XQ(?75onlHVH>Xt;NS~{s4dPCfzbG8@PDdr#tIqaZU7O{hi(-5g&oLNx*FYA`R7FSKB1V$_4AHGbt^FQNHL7UX(UXmwZD{Wj)fT0Lb*Jhzh!|d#pA}*G0B3$gd8(1+sYBpFJlJhJ4GwZtMEOW?0^8|cF%phlg6(Uk-@rHMyHL9ZMg(@>u*zK-yo}~%yGI0v&F?Gz;`I5SxkQJXAgjVO$2>~mW70l<c3yrL(4V)tE^H^9zX0AFN9olqIw_L!+%Qa8el*DxK_x`ttFf?1f6NP=eE4wR!d~?N{cRz`l>}r_;_J=yFj08GhtAj=o{D+e_9O$mORJbPDmlOyO`^fcwg-^~<4`=@?oHspLPPL67^hi&U=gW7o@+V$E948AyrKy^xZt}m&2Kty34V~bi-?#B#bEA5Z{GJ!t72o)o<xR_A?(BX^Gc;7ZBk7y@ebV@wz(b=6OQjq!3GgY$1AUjW?QxDY%D6wd|=d!-oWe@q|YftW7OkDNg%s8R)$I3VWhx`7v*DhdQ2s|R_0-q{s^q1DKs+Dz&$f|h>{q)sM@=02PuE-Gl^9^wpXf4jgJQ@!xs5ACdq*Yp*gZMgY_qiS0km23gQa83RA0s5}Hd!aOZY+`bcAv5;{nDgW+?%6q%i+fsNrxGy`5XfG1i<)154bcjL$>gU}dXiJv_WI>4ypl3B#{z|2)%ZomkEe#lmvtq&dO6K8~Tn0Y(GABa^#f4sv2+GA%2*MaU>MlK*Hh@lv+Xr#hoaDqKox&Rp^dQ`BI`YOW^+$k+^+hZFW4m!!qE~v}c<i$Y{@sf$x#FmLmOf7)bqjxfZXHeNL!LI(mwlLLGA7Us5NR&}fj8QM)J}-+JkMgHOMbtss+CJQQ7-?2?xpF3WN8nWiRiQF>7NPq$&VqN%71o<<B{fKjYKWmFsjw|5>oq5l`_mt0m}xG|%F=^VfE|M9yA0$ua#uAUOV?yjoXD5%5+}<XCq_FqMB?xBVc`8nCk+Q@JslA|dF$7A_U5Z}GI(9{NjfJGogD@p`EwO8NWU7!-9b62E*01WgZ@e(<*Px@B)rd@iGg7cwHd<W;Xenv)HYeJ`E!X!%EJj_pKGvNB0-sNBkrjUaIu$#2duu}gu<vs^&A}K{<a<Sg1<X8%TgL9V2@)j_2&0Z_C4EBpNPsw-!ajlOAH{7TBNR(cQv9F|5bo`T~OHdDMRcaz^Kf}fc$^oR7?u$pLEK=^4*`U1XC>QrL@JfZmotjfI-^pJEgqq6?12L6Fx0uXeSc<E+!Pdpw%YhRp1!9T>F0c|10wQ7y')))
_PROXY=make_agent({0:_DEMO},budget_guard=False,dead_stock=False,sell_lead=False,clamp_sells=False,room_guard=False)
def top_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
top_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=top_style_proxy
