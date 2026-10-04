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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rM%O^;kha{MoIo&%?QNRhr#WUoXlr4h*CHr4_m2=E#PjP*hG&G3IWH6PutUq(hmW>u5=00d~zGwfHdDyu3pGBWbV|GoJ4pMUx1KYqFRmme>Fc=`VQ#mCEw|M>a8{_Vd%eemhWfByW-fBxftKK=aT#n&JH{?p6v-+cG-?ZxHAtDF7B<<-Z_`;UKkck}wgtJ_bX@4wx>{Ph2)kH0zmgZJO=c0VlsN#PeC|L^i-ly6@B^}`Q~F(l)CzkB=kIHJ4n|Mtzh-G%redCmLZuZHsVhc|Cu|MY3vZa>`p>%&MEqg=ip|M2)Q{C9V&!{2c|Rc~Lu+M${H@#6cNcemf(y)gP|zk7eX{7B9$w1Rx;9{yl^GNi*p*H6EUGo6gg8^)`b>(z>1|2TEa6*vy(VW*H$yx;9!fBNU&?cUyee{s3-=jh?(m!<@U^6(01((ZrIBU(N8FTei!<hk(~ahl-7eSdp+&dE4dPu#s+zv=s%55W}IHjL+E|MGVCj=Xg?+mFwIJ7e`Kg&kr%InMWS1@B*G`II=6$4~CRzrNm&bA4)P>HDr8cRI@E<VRCKekXmNY3helMm~43uA_6W*ExP)c$7WMr$_NdpLE^~ukE}%#cNlBTX$+^Ws_ph%_ljXiV4q$rq!Nk<AH~}>3EtRK9a9aO_@9^{=f})=&R|Z>2C(}viK;@Q1H9vOpE;9S2u6p?q1#g^q1Yc+c$6D{OjGnOPt-zp-mjZ#aH@%AsH&YM(GzFj<D5`5_c&aG<=dg|484A@F`2Pkze}y-OUe~8S-yumbdb!H^~DYJS}|4l;+>KVIJOe@dJ9l>YW+iG=8}7jO8mHJn~aFspcRaf4ZMx<%AiLNIWs(SIgM~ZtDGFkZ*}jQS|>w2--BC_|%8DIXRQV;+Njz_(g~BmfLmhqoEZ#OiMJm^_U(Gefll;gDbrmxDoYjWxUzyhvu94-{Rk(f1WR?-2P3dYrcz6bQ?ebNHCz}n)IEDqU!)o(Zdggn?J%F$%|wkKOVz}`&3UX^EM97z=(%t9OUK`L3AL$I=UDZIMBH9P}EA|aOh#I(PZNYjgathXj9%4Y%lLs_27BH>kpcGUWc#w_T{_3bq3DA{qRKykvu#yb@$%izI(a<diU<#-@Wx-z66L#BWAOBKywt}{Q;H>#<H61qHhqv+{Z^844gUDt0x@ijfeL~zi+*;hNHBcYw?`JK^GUa4vxmzJA8e7G2&M=VWjM<&+;(#j0$9>Bl+X1f%U5#AhnnHbGv=(p?>x8_wEQDKl+TG;3}B^ZFquLrkj(e?Fmw)JVkGP!CmKpRQlT2PdeOd>@o$nQR-6~Z^z=5V7blLIehhT$quKdgfa+m0@>nm^vjD?!Y+jV0L<%P3E_%pMzAZSe|cS-Am!Bxq@*65@>fu1GdN#y<%S$vHW`D{3{q&|t0%t?3K7zLTh(zrekF_tRu0*K=X&z>=x-4`DSW-^OeW7|o2G%gfv<};uR+cncpY)|3fSpy(}kSjO9BWxC#12lKR>5W`FXrce)X}*=sKElM%J$7u#@RdtYp<Wb8VrJ=;{by%QU~2pqIe^j#snec7g*cB8bY<MW7c-YnpB;y*&?SFYtv6_z&6Q%-b%dDA;RItd21R3obl(#tG(`rw`p6tOo_61Uzt=Nm6tOoQ%j}oT0;hqORq*r_CJQ2%8}kycK#SE)xqd4>O{Z%ix_3!zI8YO<GkwV1jFc6Js30b=)l$OU!ZTj`OS|+7{@zTE6MuUkH494>+7N=kR^QG4OdE;B#ivDR3zrGn*_nOv%g9)GrFFo&#V7B`{O+@4U2z0j$Rx+n+VI10$sk?*{FW0xDR849CtZaH|wtUdR1M_c$o{3P&|SZuNafYD&`ktoVqyywn|z<dsN79Pm@~eYHt8G|gSIb=Ko^W*-i-KRSa@%5N1vf!yJ8qDUJAftcK@u6ke&%fN`1H4d>*VsMmwZ;hnm&?Qz3)@gj8Rc1n^j#_bZ3{*gb5lm(fmt~7T2ccy-jw${y1F`G7<Q({~?-}F7M_d{1B{2`O0FwfG$Vq<DM=lwit}vkJOCCeF%!vZe!N;IAprb|H+<f}qv&Y--Qy~5NqULiRy}Q%o;&QiB2EzJGaK@Pk6hKtxkMKLcaOOB6;0BHhf>5h@WklP`OMxr+Fp^rNmmp|)-1mj8P_AxtMRKMlmYSF{f%>Y>qe76NIGht;6_}-x&~52i&agXDdM2mo(#U?V55_?Nd&tPZAuUr#z()q@B|Z&WenuJ@7<x3IXo<!t*v23Y>sXEq{iXf;;JVkGAr!uWiVHAXa*1V0=x~w-yw55df)7MBxyM&ar=nbZdKO<GI+H4aq+XrZAwcv>ud_{WizhD6RiRD1OYRK0+;eS{<$I6zm1-Vgx8A!DKNe!>gc^nfd6GZm8wdpHt;8r|<?$*c#d@Oy`tf6{QYiuklufukaxI~&OQ)1Rq4qg`3#yqY7KfKyFj60HY34XuD9{Fakd20dVlwl5njjPNoBc#5DC+`yqsP93o8Y>JQb6oE-iUcT<e@S%sB9oCN`}RVWlhh^j}latHJvm0TJSFJ%9McY*KubeqsX|DGis%mkt3cQn|Z?ylToo9vg*D-3r+UV%X?8`F<5+>cyK2OWqXqvi(%pcOHKfY51>FN*3DnPS!NZj)}^~hteiMD;Lfoe!(L!wnI2746y9253(V>z|K-g$eXzhkpi)6T7Y4F8nt5Eq$j6{kd_T9=pV3j)Ou(X0hLcQ0*<5*(Xt|`)lNqs8qHEw$BAAN~x5IiEsx8WjjGQO2y;UG#em=Tqv*1l$Fi+2(jgAnR7p^#k(;N-_?#<i3E)qt;vv{VWm}?rvYz6Y5j^>KQogO=*n<Q}+eIJ{;xJ-mMn1d?10^$A<6HfVirXp&GM@dn^;B3w*^C6^TMeF4BusrAB>?lZBh)aAJOJpm+njTs@=970XEuEBT0x4x~Yb0%t02!%!n^X(;&CSjG-3T`v1Pr8*rm`T`I2l48135klduDs8Kp?O?ycJ4HBb+o5-Zyjo<4XIoT$Chih*tW*L<2H!Oe4|aQu_DZS!Dd)`+U)>n{d3xnL?LRjq=f*S9Jg!UGs<AZfVO%?vLo%=T(^#S`~nM0`5O@|I^&$v|9u*ah04kvmNi$Sp0o&#t|QZq<oCb?(wgYnBu$x*$k(pMP#Kq=Q?^<=Ld5e;?U-`P(W8N+2rV)fX4$#(h2qM%4NJGTo_ai7TyQ^(U?9?rAGtK3eVw~f8NlZ6V0Lf%*lQI*x3r1^G<3t(t4ye@en!<D!t&>P~W=e#$G4MLV$B3X;%P$5b6uz=w3HT>@<tiVMt2u{dHSlM8(|^on&Q)9RWT!9E@IejKfn#jLPFpn_&ROz(^}`pmV+r@F53gn-K=b8>t}YP|_nBC`HOSoaVW&{hY`F1-Bu^BgCQ&RBr(1CeeY3sUv5|vr?Ym_@=@;K2?5bMo}&$E;nir0@hX^=?w~jQANxcq45NFQW91+F)s2+RJh`R>JCZ3Ayr#`$Vj6s1Wj*9Lqxl%Fr9HYaW$EEQ2bqw@C#|->%}B@Z!8ctRn$tos}ApWOx~*X@sYzaU*CyQ$rUafEKhj0&%ucyGpA*t^<<XWViay_VZZm(%e-loP+KnO2!cJK{2(@aTI7yG{-j78sBm-|M(wM4`{!p5?x|iLiWHS=?j3LNI>H^q!#)3^B_fwX64zW+$oX|k4w1tuW*D$3Fye;9J7`TCJCeb*%N>CZ=<`B*ED+g=W)fA=6Tg%Sr1XRdVz>dKT7#bv!JPP8ocO=*t@x}4?8pl8$Cr?fExj)DsCf>NCRV!@ay#e(3-JVBMB^=<7C@g|!4qfya4ek4k}~_bx;vGGO~sf9$KXa2%WVQ_DR`MKG~XbnIMMCRcQ0>mij|8BC5kHv&Ldd&=E2ph^GTor`6|gL4^=MaK0lFdX4*Itgm9TS35C=l#7_#!dxWjD+!znj;7JdHn}q07rS(De<i4V=H($sv-qF{EYO=Ko`(P|Xs7X9I8J7Xx<*d7WGs6n3JXr(a>J=~oO2-&ujBrXD{O#_&PQf<;a@jXVD$ONF4ki4L<N73iqD?IU#(Qc&Oe|GH2aLCZ78&~PR8k}NgG&DK@}<#W7it;H*|E4ctPnaSKQwA&Szqm(45&)P0CZGoiCV==UYs2-(VowB89Jem0{krrL5hXzUYtS74jj+TEk~}*QM1>Y3P$0b7&GIO`d>8FwWG_h@I>+XOJBE*QrVU2lJY}uZz<*<;T~e2;MO8i-Ub{cu2&$c9;^`@r?ee&3Ps5U1(#~m3Mm_JIVM91RJ1tpr<Q5>R1&MIRqh0DF(QG$GC8itx$@cD3}Js8<%lzyGZT{X8e`*`9TSWyoJrLspxPy)d}9ty*cjjGm4TWc2@_#Cq%5>#jKobcuae}@JVmTbFGSj!4t!73tyNz`Q3;-iNe4cm)MgKwZY|A&6^7!AvCv!yQJJg?D4tb|-@#aAGwwQehyn+wSm`sxIDylPbA!v(2mTQgdaDTCvsp}8Eti9Lgf6yyYRp@_a)1X03y;S7r^P9wLKIq*?VR%aCz0+(MEH#AJGWdy67XUE#H8vA*uM7OUs7`&AIx`*y8CUiO-?oxY4~Ye6TxW~XkaKPKjGLmPs7uBWf~Hzk;JU^Tqu8JwVst%sS8bj^q2Z4OQS;nT!9me;vH?-&zEU;cuE&C;2lSP3PvsHrR|uqp9q==K<VL60r{8_SY40`UXN(-1kk4hP^8g8WuDBywg^qp%pYNZ)f&MupAXtU9)r>lw=shu6=1L5PC?Z|o<CW8WoP`N=@DNKQ#Bx_5eHNRBmWcx7kOv;9&Av^hhWpBpqA*KZR{wRE!A$CXgMQZAo=Hr@lc{dS(WQTGE{CQl?+(C#ROnMCh^hnDi;cAc{Uj#6bp&_i*3Rpp`rqBP|6q!;#oeWiEZ>HGfbYzs{P$|K>_6o&b?0GCc3eDi$W3AbqQ&B@*5x?JhdwQIoJ-3*NQbC*8Rzn`uh;GH>BfYvbN?4%Eb3@E9O)`?iwfNfoMu20`jw0c4X<}B;4z+osytTh!Tl%Rf6ukH7!fcqGV9^V#r9}O<GghOo2|n-n~&lL)*m8RX_vq4~SnwJ6<|PV6sZ*LYx_eQFsOaB!@pN4C!M|mZ8<umBKU$2r17aSIAiC5?X#QFPpP6X?|Y)?w)+%#k$11HQpfQZ#MBu+8x1RM7aB`9A>k|Euzuy#PB)}$ES4_dKo}dQI0`c+ePSGwN+!a-_bFu@vt6hu2Rn9j7&9BnL7&KW4;1iQdf*%Q>$kM!=osZSMa0Lz)rg`&?Hm`Y;b~h-+c3HMSLfr@9FiWQ6`IczWUhI=YKr)&mB014C+W)`r0Uw2Z`0CZC@L#+EoB~sgw^(3ja~^EM5!-Wfcf_9_)wajuoPa=x8*D9347dqP(}>tmr&(S2B9xUiaH|lB_b1Bxd)sz>t>#AUl`pRrG7R#g8n5L)3i5_1+ep%?lSinp*Bj_N)|yKn~?B@2Jp&j=<B^Sp%{EFmn;)t8AQ#H|ZzfSqPA^U<P)M%pudrQD<+@My_z{KSjxmrG3yue|$X@6G9k|*PWVaIcdNl=xX!FJUe5Jv&;pWuUrXYhB&+;Pf$Cs#hp7~5fTF-vuX0%d2gfUdMAORpVBo-395(yh<@lq=ADl)4BZXA?N*GnFnj5e)7h@o3eaMFUX#Nnk`|udUDTV8rNQl-TsJ@myi)CT9PAdwJIP&-E3?X|<(NUK1DxVce<l$=81cbyJ;c^LW)FYvgzJ0#)G_M$w%yz&$|OZBxS9E+kOn93H{oL5Oo3?3$4_*zYk{z3vaIcymmERq$WpeVtN>#v4cfQTnfa74I}aAna0|`^v4hoj>K*8xSvfC7OcLm<A!Cb)IyFIHYFkPhv7E&zX&02891~PZ36=u5+f)e54yZ%5X>5(uIjK_CLcrR**;dXgxWN%$Wjpmy$;7q_+*KRuY92vV@0<=s2v12W@z%oK01tELQjKt@9V9`uu0f!e?gRn1>iLJ2VJlWPF3n82XxXs%U5D26#D%J{eF<WqosxZ~2Z8_L${B@resYp;E16pw#&%pT6YS|l|FHbt9ucI8Q}4a4*W|R)PACIrpWv7d5&3%}t_gq$T+U<G!3(iYeO_Ne%XTR3p!pf?THzixaVsQ=JCHwr=9FKPj$s71@o4&__Fn)vHIBuzFUqkHy#vM=7J09t2BBipBvf!|eP0F8$76gW-&UGJk@Pe^cqj_7Hj0WX2=WP02*KuBcws*y18qmb1;L?EDP)*>(gek^q5zv=kr4kCHc`^-b9nCDWL4T}g)!DbTvyxOha^$pGMAwnksG09ATTjchjr;TJS#vOjS>Q+u!Rg`*Vm%g3$G#}7&z0ZoP$&_H3c$*^b)8#<$k~lsB%8cPvEzuH9jviNP+XgI`}dH8>EH?#<%_G9Nu~0N;=mwQOcNRvU`Ql*`+PoAoOVK+QhcMq|vlD+9Z|B0aWvx^bfU)|3oVeDceglrKR;qb#F9cAR4pFTpth>aA>szF6DT$p?s%4s#mu2Wy&Xvl?A!+#l6j4)oL{A`kTormTvDjCZvqPaTZd+5$Vq}E9^g4g@mc;&*P)%#EXsKYnnm*m45$TLB7yO+c$`^<-pUg%HQIWTrQ@pF5N<f-YC(ZCTQa-`C(H}^d@%>Nd<PfvrU1~Q7=gmogS^^Y*O{%YTUO9R+O_u$=9S0)r{JYXcvrJE#&Sw>3yXbTmu9g`}GcsQq8sJep?b#6`C;izQF7cf@i#CN*qf(w!l<_Fk)1m%b?L~$u8a7(ENicZcr+00SghsczSklSNJ5uTWOr<G0<ZOi`GY+BjwI{m&0At3K2Yy29PF>Uj)Evcz9zGpw5dYSK#n{l7&~-f%bA;>2*XskDh}xW$OwniFOFhW5kqJq96$AFKwBC*WfQ+&D=A<M+9`+dM%|a(3letNLIf~N74N(C7Xc!#7aLRr{f+U;8YI68i>E5Z4KBE@Aw1Pzi0lynKc@wG6=Snccz>Iru#o8*Fb6g6$qz-M;jGB+aXPd>>f^KM$ato0M^g3xl6*SALCDuxUM4okj=AzPPwSJ<xG#JIy+JkDw~7D^~9a(B;{E@qiiX7A11=^Z*B>q=Agaz30_n^Loa`C^RKc)cqov3_PI@;?g3znc;gSZVbIc{WO})L;*jnG1dlN6#V~1nScp%hv0Rth;dwO@5b&W4041;1CI#{4F_>Q?1T-<6#aE`NiYoSN!Jw=@z9jo3?VUl^yj+MK^HJuC(w`di9FO22tCe~uXB4wu`)@M{NA88v%!)v_{z^&z)O4F^0om&}-x$&hS?qUpVqU>i>kGj73rGtyPbQuCV@@AHp^@3@3Bk9or!5ib+`(GF-?}=VS5Nd?u>KI><O2r|Tnu;S;U#rh7Ui@=K1gYa|3eG5m_t>0_M4`ve0iaejl=WQEjxdBck}wgt6Qo)qZutkF9dfIin0R(jXWo^T8KVKv(Tojxp79~ODWxnkPDo(PiQqwN0H?zS)(7pgkM1mlOa3BpRh=qPO-)m-ixMr!m_LaU!+v`t}`>fVRO+59cu48J=oUv0*pC*vLyt_{@yG~xbph{N!)~z=fF4<ZInTyrsH8yp~X3~(%&;;c0=WZ8}wt?qs2-K&>BsRmS}pK(WP2_h^&lqP>omzZUfCHAoP5T-X9G(PQ~5o&f?gBRfVYmM=*z~i|+{&^i2FAtg<ZI?iQp{Dky!2O9W<ANETxYD^RcPZk-fVrR5|$flYe19~Cg^@=w%tENz2RJ+Ntn4P7EY?b4DFx((6r9`B8Tow*wNLo5i-&{g>$VWdz=mm{P>vyx0;m6~#-+Q2qCN{krvu!x;^2#&Y+)EG7erV#7-=?bNgFH>cE7})wlH+R{dpE&fQ1MdK0@$Z2<wEewvhgfmx7wis0lR88{?Q?L3!1bV6La}1Iz!H+}cF#?oFkm@`8Sz5BHkAlqeXuS9oooeuJ0QppvWRF$MO9M|WT1&j4fBXf8Q8r~o3m}JE*mkr8(@yWA@O(&><&GLm&BMczqa#1q7w}AxP=oX7AnEzgjawiWFthp){@_zpqz%>RQsEow-zY~wpzY(g6_X!>*9zp+ycubcv_RT9H5d};4*1s!U2d0<*qtOxG~zsffoi%3mY_|E2EM-=CX34OrkF$xMrXe=&lq?&=Y>|wk|ut5iqsGmQAzT4*RNwn@X`E4av|!X%&T5TEp%Q#aS*x#!{(bv*_X7pJXYLCU^~3T$~I86htb87F69G*4M2%+S8Zv*{a|@9En#$G@>t;%Nj4oA2`3M%Xsoy2W=G+6vMSIOc2_(v}~?2qTE?q{I=LYFFuRDO^rcNDKUamy7j12%m1?3$$nD-M0nILIcZcHkScTO(|(%L4se7buxKesQv9nVYgf_TX*HmcN%{3nI9KPiw0q)K-Mf0Xsp7#XO{pH-vM$VffiTR<MWb#_bwR2Ep~G!sJC>IwT2!JlgeeR;aS!<I*@Z}s)zzC;+)Otw#)YcjezcHFDt6~4H>H%xQX|g+!mI^$O=fOSbUqXcq8h-}C_)1je2i&p*79{kR!GKz0*O!?*J4&xYk@0`t!K2iv!2JG=2}Z3-iu}G?ZzoP>guMK7cXukVgI(s^2@j?GUA6u#^ilM&Z2f7>#j(w76_>rGB!@TY#8rjuVOfF5WC^XJ8n=dT|K9WiK#0wxeZEPBeWnw&mmU7F*kAK!^KJ-suacixQKlD!n>gwE*AB%#!Ai)N4l-?$1CuT2{*lPA-b@s=`nV0jH}ge#-!;iKQuRbhJ1Ak1q&j6ar4ru9J(9$1j)p--Lja~END)W-%ZNzr0C?p)I)glJU05gkD_+aN+oenAw<sec==dE@HWpUfh<;rt%jRQyH2KXf;>~5nAqJfq`7S3zA9feo*IhdO?HUC4>_iy405R~HbnYP9KA~Ou?Qyt9R}tz<y9%A;`?e^jU;26N>RLs(dUN^@?o=tuCJfYWY7yYRPFfo`#B{<3&<i>D?v&-y2mrs=@eL>)0NduCoWvj9^_%xqC^dIO0<wS?x6hxNp&TCYl!WG-LtCQoT6J~_8n$ZZX7gBW_)I8CaW!DoyG(fL$r2Cjr@c?l3bTWi^grYWS<K@Z|b_HX>_P4qvXx-SAfk4Y|=YipBF(tUPgv@wB>)qkSG0uvdcyIOSFtGxr=2nEINzVC*zqKeQTXmWLktr$b99!j7F~VUe7+h77O+x02_-l4b1b1S*3d=Y3uPPpkZya;15?@+A5`<)g)gRNLW)CR+W&e*-nfg5EMHf?<}T}BaiqbK_RRnQ0Hz`upg&?=2WE-5N|&mH+ph?W|MbeZ}e988(wFihUP5=rv#z>g_No545p39yUa*hJx|-goVmXbQ{L6pQguoi%#D^^E!^wH(zoVqYgko{6?U9vUoR&o^y7WALa56-&94HRDtUuY{_N_hHX<WysFeQCw8^Ndj8ZXIy@xHCo4LnfL2`%XCm_SbY_pZ4#)F4m%rRD&cA7=@c%_-!shSkdo6FJ26ZK2B@1pZ<oEWY#q92Mmb+-YJFzLL-r>TB-gM?ZEGeQOZcDj#~vvv*jlBX^(0D|dtq)%BkOhz=V)h%xsL`%tGMo!cgpq~XyP0()=OiGHqKz#_M_1E>&z*R1!{FhZI{EW$a$Acqpg*ef&#4cNCakj_&1h=aQh@m1&W=A52N?`y(M2HX=F#E&n;-f4TMPrcOSBt^l-hB7+_U3eH{@5Mwa<-N#u^ZGgx3uMJ9q+b8wQ8eST?$`<cYlr(G6Gy3J~QD@MgXHJWm@Ro5I^<>sswug-*c)Md$rEJ8Z_PsDoc>$#N{nlBO+U2^O+>56wv{v<e}GV5jb+%L!vPSIUA2xA#^vi#P0cG*I4)}l|>WzUr*1f9^#b+sywY$5E>4U9?fd^2_dbMKM@Qd8=b64{y-E`ZB4n$m9!RY3tm$}H|4c>F^JaT-S=9iTh)C|jVG;Yu>)+P;=hO(220N>eZ6I!I|yc@kbfvpsTwzKens^G@LOc1qEba*7AM03{e`d}g)mUiITbtiw8JnE3B<f4lV*k>4(OhRfPW4b$3=Vq;T(m(wSQd~tOEEX<%jVKcBZM3Re!-T9|LAXZhid#?E5UHRqP2}b<pj7huY7?#4Lpnl{`z{VQvOw6p_5_+K&isq$lAtC)9JN?*KSdnL<}Z$J`)ugQ7}UDe4UWNw@3W)&q;SzZEu>_2H%})lGHbQU$|efutXtkv_Prk7biT6=APJOqL@P*yhnn6(~q?QRk~f`87^ftjOZib}urkJcB9Xu);;RM}6QH`W9~M-y|2aRke;<e9Z(TvUq@|(;$olDJiP^m@nw0EEA6@lNT@OK@GQ*QRY$C0VZL+%qiKqVNM!>vs}>bE*0My@<+kKBjY<ws6Kvxn<)#?v*`p7g<PuNv(qH9-}CJ~E!bsX5dA4hMp9y&+uE~6_ZzIotCFc`$d(-!)3`2$y49L67h}V@f?T-WkrcPG&(9?B(IBALN^Dh*NM$w_rUHeXDr){=OZ4dFlrc^H3+Q%3mqpecg!wT-cix?OPYRg@B#n@*Df(xg&{rxao(fLWQ>m~&0q(;HGrDq494k~5UQ%rmJe|D+Ed)k;8x&#!syiF~BSg5Z)snKNb71VOyPYMmduI^EOgn>#HrHPO#wjy>HmQ-8*gO)ezn-8%<#eF~f8_Y>d4zCo9*+vT_H;RAK~zDmv+X1hb<s}G_C!Tt$5^Er#8GAU49VeY9P2F0;_|fm&n18k^}TGF8C}sW>f&0xsWOsmp~YR=hhrTSm)gY%?|V<$*;%Pu=H*7ea9Sk9I(|eJQm4v<M<SNT6^o*)q-UU{QfZc0X~|ZRv=*ub_MH>eGen%qbLHLQMqtC1f+_!dl#gDXl#(DeZL_dQO9$dox0t-7Dabz<-_~PxbqgyVir*u)w#(UE3VWgjA4oA%*9kl?s+IUDC>a7{oT1Rmv$^l#G0OV}gUAeQgly&Jsr7lgT=jJmY(HR8-p+n7sb>Qh{9b6_GbPm;sk@=~s%|ct<^s$ZyL9qIH`+LCMCfa{7qBErz_6tFWogu38D_vdPF^Hv?{j*=8-$ssu4Gaq{V)(HyP;#VJqw>E;@)>K+f`G;`@uUoe+3vm)Z4tCtqJ|uQr_E&!WMs3fN(}WPXvc5w`WBwNgj}qjYmj5v?@yiK1mZ$w@+F|$D@^YKHdY4c3ns{O`$4zIR;?G=zVb{arF@NDwZOZ*I&cdyXJ%wlg(-{>U(n6J}S{@A_IO;Mu|wjvQW-FBSgF+w2|cr!}_144q}pJbCUY-mtwlR^nKRttWde)CG+b7^|3t(yoqVCkdU^aeGWB>Vnta8XKix(Pbh?}wv~dXD-8|7w#F?0h~CS>yUaOQFkGA$(I)6Mx?BXN&uc?c5e1JdOCnX1UgVUm#8y6>Jlj(M@)dG9cn<m;#3PwZs>qZxAY1LJdXLdTX?0d+ifkDeMozIP)t>{k8%oa>MMi%6I(8mg@`LIi<+zm9lhwV;F^`6oAMJCbA#+Krec$dK%U}oK9<$zhu;l1SpguiWsZ;TM$@6&>s*wXHVsN3k8{kz%Hck9Q8pG2#^5?%V^_-34;P~{Kvk2*|wZoOl+K7@4>53LNv-IuMnFZf@V}eJUekX35rT}&jOp0eEhuuOAPwa-?k2NTTF>(5L7GT==+$2hL-B(pSpB6I&vL&`vm88UVbVvhdnCZOQM1n{fPK;@U5M)BMi9Hv@iyT_m8aI*7m8E6lik$e)Ya2Zg@jKf`4y&059c|$lqyn!3F51=HYuhwWKgO_R+?<?MBdn>{?b?l|Qc65yDowNNAh)<mOi>$=<ONw~!$E&iX%DSBgE^`el8xY;%}nMPOpO6Yx@9pSJgWh9)a}Y92M#4#vFZyx-p2?8k|u7TYkph-i${9N3&V727P3{0&Az8*v7W5TD6388T<ENYW>2*8292ND{&^%~1eJyFC3aZl{ljdXnACQOQcPF_6ogRjS`I<EZQx7gAavJmo_v9VqKZE2-s##>k%!+#B<X5X7`zOfC7VJRKVh%cYlGZQGZi{ZH<+QX<7;}y<(JPB2E|kjS|W&CA0obh>)T|F@@fulm9fOK4xWI{XgbwiaxJpK9LnK!rz+U8d?b8N9}aUwrCHd;##dqDn>j{j;0y-iOBpV`D`T9zV=iroYDM5B=aifn;?R-ohk?PkHh%P&LYGN%;WBE&z10~VN8(s$eR_eRWp!0s7@o;m25=`2Lhxk=R2pa;Zf6gxg9ihlV}sHpX%}~Y(s5>)W=L2=T}r}4?`0A*H~roxs4aP<74gHWIP&~l^)$j_Y-Q3o3fgvC*?fh#ocp{fGI8&K2x=alKF;A+H4mN$m{M>kP1u)e2AiEE$e^Ps03EMzhOeqKOfz_#a=?oC6%hFN|272dGX')))
_PROXY=make_agent({0:_DEMO},dead_stock=False)
def top_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
top_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=top_style_proxy
