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

# Locally implemented, observation-reactive executor of public production intents.


# Historical episodes supply task targets, not hidden live opponent observations.


import copy


_ITEMS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')


_SEEDS={'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}


_ANIMALS={'COW':400,'SHEEP':500,'GOOSE':300}


_HOME=((4,4),(5,4),(4,5),(5,5))


_STATE={}


_REPORT={'errors':0,'seed_waits':0,'supply_waits':0,'weed_repairs':0}


def _walk(position,target):


    x,y=position;u,v=target


    if x!=u:return ['EAST' if u>x else 'WEST']


    if y!=v:return ['SOUTH' if v>y else 'NORTH']


    return None


def _fib(n):


    a=b=1


    for _ in range(n):a,b=b,a+b


    return a


def _tile(tiles,p):return tiles[p[1]][p[0]]


def _home(p):return min(_HOME,key=lambda h:(abs(p[0]-h[0])+abs(p[1]-h[1]),h))


def _command(obs,actor,tasks,state,needs,seeds,stock,claimed):


    seat=int(obs['player']);day=int(obs['step'])//24;hour=int(obs['step'])%24


    farm=obs['farms'][seat];tiles=farm['tiles'];positions=[farm['farmer']]+farm['hands']


    pos=positions[actor];inv=obs['private']['inventories'][actor]


    pointer=state['pointers'][actor]


    if day==29 and sum(inv.values()) and hour>=21-abs(pos[0]-_home(pos)[0])-abs(pos[1]-_home(pos)[1]):


        return _walk(pos,_home(pos)) or ['DROP']


    while pointer<len(tasks):


        task=tasks[pointer];target=tuple(task['xy']);cmd=list(task['op']);op=cmd[0]
        if hour < max(0,int(task['hour'])-0):
            return _walk(pos,target) or ['PASS']


        tile=_tile(tiles,target);distance=abs(pos[0]-target[0])+abs(pos[1]-target[1])


        skip=False;replacement=None


        if hour<task['hour']:


            return _walk(pos,target) or ['PASS']


        if op=='PICKUP':

            item=cmd[1];quantity=int(cmd[2]) if len(cmd)>2 else 1

            # A historical pickup is additive, not a target carried-inventory level.

            key=(actor,pointer)

            outstanding=state.setdefault('pickup_remaining',{}).get(key,quantity)

            skip=outstanding<=0

            if outstanding:needs[item]=max(needs.get(item,0),outstanding-stock.get(item,0))

            if not skip and not distance:

                take=min(outstanding,stock.get(item,0))

                if take<=0:

                    _REPORT['supply_waits']+=1

                    return ['PASS']

                stock[item]-=take

                if take==outstanding:

                    state['pickup_remaining'].pop(key,None)

                    state['pointers'][actor]=pointer+1

                else:

                    state['pickup_remaining'][key]=outstanding-take

                return ['PICKUP',item,take]

        elif op=='PLANT':


            crop=cmd[1]


            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])


            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


            elif tile is not None:skip=True


            elif seeds.get(crop,0)<=0:


                needs['seed:'+crop]=needs.get('seed:'+crop,0)+1


                if not distance:_REPORT['seed_waits']+=1;return ['PASS']


        elif op in ('BUILD_PASTURE','BUILD_COOP'):


            if isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


            elif tile is not None:skip=tile!='LOCKED'


            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])


        elif op=='DIG':skip=tile is None or isinstance(tile,dict) and 'animal' in tile


        elif op=='WATER':skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or bool(tile.get('watered_today'))


        elif op=='CARE':skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('cared_today'))


        elif op=='FEED':


            skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('fed_today'))


            if not skip and not inv.get('WHEAT',0):needs['WHEAT']=max(1,needs.get('WHEAT',0));return _walk(pos,_home(pos)) or (['PICKUP','WHEAT',1] if stock.get('WHEAT',0) else ['PASS'])


        elif op=='COLLECT_FERTILIZER':skip=not isinstance(tile,dict) or not tile.get('fertilizer_available')


        elif op=='FERTILIZE':


            skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('fertilized_until_day',-1)>=day+2


            if not skip and not inv.get('FERTILIZER',0):needs['FERTILIZER']=max(1,needs.get('FERTILIZER',0));return _walk(pos,_home(pos)) or (['PICKUP','FERTILIZER',1] if stock.get('FERTILIZER',0) else ['PASS'])


        elif op=='HARVEST':


            skip=not isinstance(tile,dict) or int(tile.get('yield_units',0))<=0


            if skip and isinstance(tile,dict) and tile.get('crop') in ('WHEAT','CARROT','MELON') and not tile.get('watered_today'):


                crop=tile['crop'];age=day-int(tile['planted_day']);low,high={'WHEAT':(2,4),'CARROT':(2,3),'MELON':(10,12)}[crop]


                if low<=age<=high:skip=False;replacement=['WATER']


        elif op=='PLACE' and cmd[1] in _ANIMALS:


            if isinstance(tile,dict) and 'animal' in tile:skip=True


            elif not inv.get(cmd[1],0):


                item=cmd[1];needs[item]=max(1,needs.get(item,0));return _walk(pos,_home(pos)) or (['PICKUP',item,1] if stock.get(item,0) else ['PASS'])


            elif tile is None:replacement=['BUILD_COOP' if cmd[1]=='GOOSE' else 'BUILD_PASTURE']


            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


        elif op in ('DROP','PLACE'):skip=not sum(inv.values())


        else:skip=True


        if skip:


            pointer+=1;state['pointers'][actor]=pointer;continue


        if tile=='LOCKED' and op not in ('DROP','PICKUP','PLACE'):


            return _walk(pos,target) or ['PASS']


        if distance:return _walk(pos,target)


        if replacement:


            if replacement[0]=='DIG':_REPORT['weed_repairs']+=1


            return replacement


        if op=='PLANT':seeds[cmd[1]]=max(0,seeds.get(cmd[1],0)-1)


        state['pointers'][actor]=pointer+1


        claimed.add((target,op))


        return cmd


    if sum(inv.values()):return _walk(pos,_home(pos)) or ['DROP']


    return ['PASS']


def _project_stock(obs,commands):


    stock=dict(obs['private']['shed']);seat=int(obs['player'])


    farm=obs['farms'][seat];positions=[farm['farmer']]+farm['hands']


    for i,c in enumerate(commands):


        pos=tuple(positions[i]);inv=obs['private']['inventories'][i]


        if pos not in _HOME or not c:continue


        if c[0]=='PICKUP':


            q=int(c[2]) if len(c)>2 else 1


            stock[c[1]]=max(0,int(stock.get(c[1],0))-q)


        elif c[0]=='DROP':


            for item,q in inv.items():


                take=min(q,max(0,100-sum(stock.values())))


                stock[item]=stock.get(item,0)+take


        elif c[0]=='PLACE' and c[1] not in _ANIMALS:


            q=min(int(c[2]) if len(c)>2 else 1,inv.get(c[1],0),max(0,100-sum(stock.values())))


            stock[c[1]]=stock.get(c[1],0)+q


    return stock





def _market(obs,commands,needs,target_hands):


    seat=int(obs['player']);step=int(obs['step']);day=step//24


    farm=obs['farms'][seat];prices=obs['market']['prices'];stock=_project_stock(obs,commands)


    animals=sum(isinstance(t,dict) and 'animal' in t for row in farm['tiles'] for t in row)


    reserve={'WHEAT':max(3,animals,needs.get('keep:WHEAT',0)),'FERTILIZER':max(3,needs.get('FERTILIZER',0),needs.get('keep:FERTILIZER',0))}


    if day==29:reserve={'WHEAT':0,'FERTILIZER':0}


    orders=[];cash=float(farm['money'])


    for item in sorted(_ITEMS,key=lambda p:-int(prices.get(p,0))*stock.get(p,0)):


        q=max(0,int(stock.get(item,0))-reserve.get(item,0))


        if q:orders.append(['SELL',item,q]);cash+=q*max(1,int(prices.get(item,1))*.55)


    count=len(farm['hands']);hired=int(farm['hires_today'])


    while count<target_hands and len(orders)<10:


        cost=_fib(hired)


        if cash<cost:break


        orders.append(['HIRE']);cash-=cost;count+=1;hired+=1


    owned=len(farm['unlocked_quadrants']);wanted=int(needs.get('land',owned))


    if wanted>owned and owned<4 and len(orders)<10:


        cost=(1000,2000,4000)[owned-1]


        if cash>=cost+20:orders.append(['BUY_LAND']);cash-=cost


    for item in ('WHEAT','COW','SHEEP','GOOSE','FERTILIZER'):


        q=max(0,int(needs.get(item,0)))


        if not q or len(orders)>=10:continue


        cost=_ANIMALS[item] if item in _ANIMALS else int(prices[item])+12


        q=min(q,max(0,int(cash//cost)))


        if q:orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,q]);cash-=q*cost


    for crop in ('WHEAT','MELON','STRAWBERRY','CARROT','TOMATO'):


        q=max(0,int(needs.get('seed:'+crop,0)))


        if not q or len(orders)>=10:continue


        q=min(q,max(0,int(cash//_SEEDS[crop])))


        if q:orders.append(['BUY_SEED',crop,q]);cash-=q*_SEEDS[crop]


    return orders[:10]





def intent_agent(observation,configuration=None):


    step=int(observation['step']);day=step//24;seat=int(observation['player'])


    farm=observation['farms'][seat];count=len(farm['hands'])+1


    state=_STATE.get(seat)


    if state is None or step==0 or state['day']!=day:


        state=_STATE[seat]={'day':day,'pointers':[0]*30}


    if step==0:


        for key in _REPORT:_REPORT[key]=0


    daily=_PLAN[day];needs={};claimed=set()


    seeds=dict(observation['private']['seeds']);stock=dict(observation['private']['shed'])


    tasks=daily['tasks'];commands=[]


    for actor in range(count):


        commands.append(_command(observation,actor,tasks[actor] if actor<len(tasks) else [],


                                 state,needs,seeds,stock,claimed))


    # Prefund imminent seed tasks rather than waiting at an empty field.


    seed_need={}


    for queue in tasks:


        for task in queue:


            c=task['op']


            if c[0]=='PLANT' and step%24<=task['hour']<=step%24+3:


                seed_need[c[1]]=seed_need.get(c[1],0)+1


    for crop,q in seed_need.items():


        needs['seed:'+crop]=max(needs.get('seed:'+crop,0),q-seeds.get(crop,0))


    # Buy upcoming task inputs before the unit reaches the pickup deadline.
    # Only our own demonstrated task plan is used; no opponent private information.
    next_inputs={}
    hour=step%24
    for actor,queue in enumerate(tasks):
        pointer=state['pointers'][actor]
        for task in queue[pointer:]:
            if task['hour']>hour+_INPUT_LOOK:break
            command=task['op']
            if command[0]=='PICKUP':
                item=command[1]
                quantity=int(command[2]) if len(command)>2 else 1
                next_inputs[item]=next_inputs.get(item,0)+quantity
            if command[0] in ('PLANT','BUILD_PASTURE','BUILD_COOP'):
                tile=_tile(farm['tiles'],task['xy'])
                if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])
    upcoming_stock=_project_stock(observation,commands)
    for item,quantity in next_inputs.items():
        needs[item]=max(needs.get(item,0),quantity-upcoming_stock.get(item,0))
        needs['keep:'+item]=quantity
    orders=_market(observation,commands,needs,sum(h <= step%24+0 for h in daily['hire_hours']))


    return {'farmer':commands[0],'hands':commands[1:],'market':orders}


intent_agent.telemetry=_REPORT


agent=intent_agent





import base64,json,zlib


_INPUT_LOOK=1

_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rk<TaRQ%k^V3J+z)xb@HUJG7-2Kkcvx%KvXCWKVzm<Na*=k0_P_7g2)iyPBEB#3RCV=qi3czusMA$>G9%-=ee?H+KYaJc-~Z*|XXWwX5C8G!fB)Sd{`9v$fBeU9;^Pnh`u6eRuiyRUKfnKPzWMvZ|NQUAe=m>a<A3|7|N8hJAHID1`q#hx^5OB}^}DYhe)wO1U;ps4`1tVOfBWwDfBx=|fBpCm|M$32`t#qu{rt1vefjFE55Il?=HbW6WLJLq`K#A&&Ob8)mH&L)uYdLC)rW`2{9|#ki+}Ov&1XM7XWcHyVnN?7NMgaX3tqoE{OV%Zu87Cq-EThr;SXQD`TX5)4oZ_<`t_?1Z{8o22;X<u__Tj~-9P=t!7e@dv~;qfzJ2`Xa;#gw?^nNi^XALL#c}larGwu$TMM#ED<hvR$g@vvcJ1*`*!eXatp!u)1#|d($7@nrC;2g%ORU<Zr%S9!uRyYvSR8ig>8FV=Ts9YUv`bGHbdnZyd93V$&YQb~u%Mg0uZRn}OWQ;?fBs;Xp8g<FDzO(^wo6Yxtw@_vG#6X9OHV&-NF~X?dnV8BS<S=zXsMNhT_RaaZAkk|vJP``FN@|+AMMi9A4A;L>`yCp>FK9c=>>Ezw8Ss8^ccJg?XVPHXoWwfx4SA~sTI3Y+|__y?)czr((Ypag4r$wH>PO+g0b19r=KS7W%j2{yYzIuoGh_#zx}>SxRQMQ|9Sk!CZ}CVUcdYN^Ea<Q{O%WT-hX)e`P+Xx{J3CuNT0ob_vM3qkIB&IW%lzb-~T11+dS^(fbIFD{S&{y;N2*TvJ}Pl(*Cq=ml_-8;npR!>)HMSj|(bLpsc5cUycvTxhsOazG7f6$<kRY-;!fqxdF*XtN3{XIk1j@#KayK1-QvS!LOcyuD#o(#x?4vZ&aRKAP2DW1@)c3pr0N&*k6&{j%T<_Iz08-=Bf9?zi#5>Bi{;aYk9J1nlf^dZUu)Wzk2olU*3H6VV9{`<R9^@eLC2^61N$lM^Ihsh@7u#a-CqOLup`2bN+)?yGXc_$m6SQU4LU|dpUV2Jezar8J-ltpikNnv`M66RNCzaJK3)T-|r@Rv{LEu2tVSO{FOTL1G_9QR`E_T`0IC|@6hr&6+GwERj&Czet8POROx|nr-#0i9;KeGgBRbsW%gEB*xs$v9k%>}CmzpC%4<~UjU)wnyV9_tdz**1dCA|gC2z-;#9v4rJ<uH++Wyql_J{5=kRQX*Fu^aPGRve}Y;dx1$?t#c*t3bJb)#XQX;+;8Vu8o9lD+&+elmKnAmL@o#7nz+1-e(ETf?Y+%Mk~UzWVU~)z?3N^Zxz6BE+D;zrWx|4to80W{w5e$}V~Njp5!%UZ#;O*ZK(uy}39@FokEbH2y+7?2_}nW#TaS){E}xgd@}mU-1auouVhUwSgZB75j*lI^hnHR5m-|VV9mXiIeYy^I9idR+m9ro1M<(<0HvO-cy}mE8Qr4kBwyes*D^5--!avE8L4E`HqrlJiDy|2lmY=r5(Gi#4({0xXq8{#hv#XSt<yggE<P!uFscV!pW_hJ$dGzv+$Gb=9y#@gf-^65%BAVM&8|Qd=k&#z0BD8v{Nb8T_Llre_BBwA<4~C(`X9a?#stxO!QDH(}S<dp24T@<z6JIC+N@6yWzNGbCj<074#KB+@$Zek*A7fx*=*%*ZT_6yX5Oo1|r0X*B&9RK0>;U?(66VsQtZR6+Y5-tUzBJ0)25<8sdUe@962hBHw!@o-wU7yv;$X<MH1~0|m)mve+@Ij5(Up!%ew|Q#v_~xW*29Z%#k`6hyAgzxJ2!-hK53nZ?x&X5V>n-qs>ld2trI;$*4S?TW6@UFUX56Mw?vVeEFrNmF<t!`>eBoh{|WF6F}F7IkGcG-)xMiq>AgJAB9?{iwxWLldY4SMT<6+Irxaq`IWnRl81pTbfi1Uhk(}uj09f>)Mt~Cc9L<*(b}{;B4oOwzC0`n!O?&5S{{NQ*OACzTpa6%up^b!uvZmnEp2UwOy~GU&-<e(3eUE?sSD60@a<Uee%?3(4Ae_kF$g=_?VWjjBWMGm{%WRkv};0zBQ8#T9VG>s2^40p&WsuO6;JL|J+FYxuGD!yjww|@i*b8Zz$9tc9kG6?6BJfKeE{Mszl>(_Xa<*+x75)6BZAgz#lm2T65gKvJHq!5ooccb=UznE#ZbY!PY?Pd8cxF>rzQxYLh2QdrUVk>OhB=^6?K&FEbA)I$+?rqYF?6fy*Yn5()bC4)+}F1E*cC4p<Kta&iz}x9e3H<FEug3#whOPHPWKJfQb>Jvblg=<$>6dbq_&+PH{zU1=+4Ot;UN%}!GsG8jXcY}d(WT9MwTywtUHz)51-rPcw%%**3tdD6z^WrZV}SmgB*xAe;*qG1JUK(6N~RFgrd20*3<t^b-VfP|T#o_q>1DL(tEvt6t#MFc}=EQHYQ?N2fO*e=jqQ4=%^%yjoGANq;!@gsX^PyEh@TobcAmwa~oAmqL1EZR9}A{cMY8|g7QZC@67HnvPi4y+iZp$h5471%rjQyq=lUQm_aXrr|aR`Iu+b^*4lRrFSyfcoQ4T>eU>4X;9SGI>6M4zcsaL?UqsNXR_%hiJ~`Qu7+176m1{c~(sV4t!J~=K1`wvJnXHb)pRum6(9CsvN3o1GY{J+2%4IaEaW6=;%;4uIjOl-Ss?j0C=v=J1%ilgug#nW0eW{?`@AqTsB38o@h6k&Nz5(X5eMR=_1zD4vi1&l^;FEi1|q`7}-Hu4ea-y`R~8tli#B`-1iGjC$5^KxU&H+F@O8w?dQLKcx)?^w|rZZw@dM3mUPL9zIG;B;{?-d@^UvI-rqZy^pZDA)w^llYig%`MQQc$&JwBcN<K$z<qopnbOz~EM4?nA$h3L04y2GD7B|zqvD&5Tk#ShkxfrJHQuVYsEE(RH^RN_tIrFucc9kWow<Qz*Ob-?-J-h@&KDwpAR>jHuI8%{E=ikG2sF4h9WER?}EVR+q1{c@8v7KL%)AeO7+atY;5d!$$J$pi@!it}d+Bq%CI_1$IR-b717x^t$luVf>)>oQu*J;3S@_1k5*-x3Ll~$ho+IhC}j%2~G##0E#9oAMOA+#WemFm3Zu*B}jl3l9)%!ei2+y4cnBWqI0@b-T}?#QC}<xg+_cUTJde@_n_I{XPdpFh_I#c}zv8S4tncS?m^(LqFz$O?^l=Wed$(cZD7*E%X&R+CDa_qC47mNlgk_sk`FW-feIMWIc68|weCEf6(~<0wID<OQix57E)2K8P4DF^~y9sLlOKi6wt&RHppI&XV?P8KqF@hTTFAOYBaf*rn<^IV`a|iEfvwOYE@3?j(X;s`BRYPAJKh4L&ZqurCvCS~v@%CE-}HhPpvQ2P!K#+b-5jYql#iPF7yCT)w(zhdg|$?8yI8_HYmjd5r+-bqKbP%h+hHbYGiUN?iakN!ThmUyboLq}fZB9`bA&xPmF}+1DLrmnXi}t~lf*YyTJfo60)fY!_=0Hro|i<`CA`WceyZ11;M)rvkKW7br%uLIDa^A0CN?zS*<hm@>SDgwJ|N5)tUM#hd!T_T<Bo$!)LOrSOWZkPS|fpufy*eigGE-EE|&C^-VH<cNHl1n<^bX-!;PM5uVT06BbOQ6^A5i6r<@msSYp>9Xf!IT$!>o|8qoxHRCLtWxoGSY2$_8~fYss2VU;L1yJejg=R5TOIV-+g}3urNE-0g-;?YC>k0i11Nh!wf!A{L(qmYn<2PX7RO;x0C!sKbEd^A4#tgkFz$;4ltI&EWG4Rr6&4T+V$z~#X+N4gvNCyghD#=%d6{_OW#Z*V?Oaeo=eVl9g)s&`tR8w#)ugs&06kTg?$FcWEw^27;Ux!i<-DKRYB%rrfD*MZ`!0t`Smni5eK|@Mpe3Fm1V_kMw2`k(>??u<zqmQEIom}FyNiq!v}*3>-mnrC<de~8G23;G0UDb<c7Ql1*u(;0<wBejtW!y{dNeQiA)fsRjgIk+ONxQj#`H<Olt5-OAeV&(n9#^c(=HSc@ZTN*9RKd=7QCM-cI)FsZjIF&40en=?E)j#o}c~7TrVsE4nl3qB5GUh`tvWQvCB8kJ?&rEv8=`fTQJ*~xfzM2e`MejP(BX=%rzF6>ubQ=u$78Gmf0K}P2d=9mEzVXWnSFq;LJ6e{VKEWJB#22k94x~FG$(M0F(n}8#GW37@+_?U?8dYu&>}6aJOBd0e3<LOxNGm$ZoCmLQ88Avgg((U54lhuXhLR><L^@E?JfB@8?o`A8x}p5JFWj3}?_p{uKDBN0M=4USbgUyzT|s5-hL5BN3R(k-u+5lb4{Gp7i@_ZutqZNxRs~i%zR$%~0V8{1IV3$ur36+0!+35-%~5Sx60KhEgghnYz^YGo--~2v4RgbQol##W{ml00my&%x4J5oaUge*um?jrYuBc4}`q$fgpm>)p6h7))i5mT;t#R?s<i~{}t{YKJ1zv;@HzH-&Qd1k{yl94YY7l3YlGk^g~!0G|axOw)Ft<!UX=94En2?0_{1lFJ7BStIMcem?pg;))jv-3DA($6G*o5$uKai(<>+#HVQDT^5Z7kCFi=?JZE>?{)95Eywtv5=k}eJcC!M=&-tr3LO`HFTh}c<EEokm2hbK}17?~Hn3vdqimi5}BXbf0waVPrCzImUwY!}PBv+OWK3F>Vs;3Nq-4QMs2}f}teW#3{(t&;5llMxK!v{L%y2G3|19K{}&p^vQBT(T0jkKFQfOKxXjg1FLyRBCwu0Wd1G4dd3z6eO#Rub4C7EW7Z;i%)xr^|3_i!2;11FrD2dq>Xmp!EQ9h_})gH@lP8e^#i)%}XtAvG1QG=#+WTNoFz1&1$-Kvzj?iW0?_G*2rzuL8xoCs%~R<pS%_?@RCG_xmw|cMt!%e=84+;92>M&XuP)#>*<$|%y=9&8bsvhsiOJl?OQtpG;DOc#2{>L7m@pG@PPUnsG`LDG+w*E&GFjUT`J8CYcy35NKViP;apHd;JJ)^+JelO9LhQ@cp${4-oNtC*>>chX@A;u`yt8>g@Z?Mmg12L7MXxRiDeB+tSpq+StxO=k#!~wL`Is*l@_U7;_1>>Fi3dm1BU54fR_j(TD-X@Z3@{gl8uQ9>>Uwukyn-Or(F$b$N&~cs95>X#!&gHjP!v_-VuKIT%?Bw+8jq_luv#*IDNyx$qxtTN&vyG-oNoSynp3MOIgFX0nM*<gU95)ffkx3T4<UV4ay4dF3{y&t?al&(pql=kcl^b<xW$O$Kvfd*wid=gA3Z2Lyl;vUSoCb5i32n==9veb3>Pp<WC!aZ<zBm0?>2^!ZK(PaiAfVxCpT%kBHa-)>nsLw9Fb$UK_Z^XJHH+)Io5dyP)|(NWTo#Pa3HYi%2~nXCdUBTA+_3NDR;=6N7^89~5+cM)q<<&BC`i=%M%Ixg0<o4cuy7H^U~bF;w77=n^~S96?cnvOI~ZX|E`m<GaZ!(-d&yJYQC6(d@F?^)Tp`7`fV#(VK#I%N;~p3#M0;h=tZcG@81@N0G(A%N^5hv1*Mc3+VZB!=EoV=|_}Fs*Z)1wL5rPBW7mWNT%8qI$*F}BYgLre!jueID=hcFtIZgVdr3)0@sEU-dU#+VeOpkBt52R%?ynYbQU2PYY4&QXYkoBfl>d2y8KuEIUA1^3?3^0oM&K(bMObO1YhKj<DBO~XuuV7qX`;&Mf67A>NgtwS>aLE%A>5EM_DJ0vdV#gm8X#)EY-rYR2LJqn}em=SxMDoB~@|J&oD-w5}T#S4V8NvD{tA<Y#$8b+LQSOuSIUC!fG$Ni=ZEYB{U_L(3CF%`Xx4ZGqEwQiIs3CTEe|LT+ke>GJo(?8#p#CB`~~s*r$l8r-BY2>?FDSATKMhAT_UyKu!k&DIHg8XmBjHQPHI$FfGTFgv4O#YZbYh0-%{p)X6O3R#;50u0eE-h3LlG2xqbgpUi`={Jg{R4=z0C-s!12cs@IS&zF6;=9T5KpX6QQ8OUQBj;CN__QJa+bbidvhY_wu>P1#ckyt53X04AZYkkyM=c2(H7tKZAqQKun6Yp14Y^k)#Wrn<pkTfTgfCnIhDJ+Jmi18*@hY1xWJ)e@ti)y7UZ|*A)=Hm`MjI+Qq&XOGXw*<i@ts4VG$s6zEZsKBvGBtVTNaUF#*)D<6maVw>5AVKs_2C^th@thB0r|K=Gh+~~84+%=G~`Zf#(ZKk<{d&a&|z!rXsQr-BQGR_IbCGPP2}L&kJ$LGgmzYuCu=AK2P6WZ8H*9*>VQd(-EDY3=;xcZ<l%PhARL3Xpd+k^B?OE~s_k)#H2SGoc`l*WsLl=WBeEI~$cm`b%DBnHWYJ+vACo(8GiLq~%kvF9k3KAgK;^d>2IsVr{A>l&i){A>o-ezFcsVp1N(fl8D`1+uChe}gw3`=P%TA2b6Z$aCE5uoIPXYRY2K4hC&<6t93-o$98l;P~WX9`-XFgP3?Az$;EW%TyKu_!zd{^&Y2F!6-XRir)VKB!s+b%omcjJl(V(a1d(=s@rqn%{9$~%Q%{4X|FxH_EmbXjfWvxt)~Ypd|OiF#q%uCuml&(NU?5n^saj*Ciu<QvAtOr2IzhK(};Gg>S>F{OEo7CUaVhyo5bOrAjpUU6;UwWtCHVsvnohl0>g9%+vb`*V5v73?*Z`DZM=<hSuElwr?dO<P`McpG{4@a@nHJ|#7B<jGhLW<uZt4g$|ih|i9hfZ0YzTH>o_AWu93`E26~ym3tAX%N{F3oCOP`U0n+^HZ7bq2_8fIu3(Mg}r_^N>`22(G~A-N>BWXSCkNqRzh?~d_$agegk>|R5n2Q0=P(IP}Et?uE0qN*-c8gifTFW{cPOuz(f1lh=%HIE7gdMio_EVGOHO48W`>i^T{tX%;%F#o|MV<vCu)ol}^{{j(p}6+@V@>`flbaJA9_NLVp1asL>5Q+XkRxFM5vRTTMrcK~C2WmYJG`Ade_OEUS5J+ZHK12=~U^>=DAw>G*<*YxnpHP&5RWy9=o;O02dBT{wMhu}_*<M(0v5n+s;2VMgU?c5OL_1LLAahq_6g0p1-1mK_A-R&%he=3Hwv5mJMe>;Taq_Oll6KAu6xN1Qk0J`kV1`vC7?tUCC~Xluuu>mvP_GV<DQH=kQ`;SLU?a3tdkWrQx}gDqJXWcF>z?As!b5NR)!v1V339T-XsJYO<<@>>d?--4nCE>5RNiybtrb<)v(8g6joJ_m^-EXytgeU0TXB%AF-MzO3L{b9oaOf^|-R;GD;ERi{<As`bG-p!`{;ES|puxkVXO9KYc3c5`zz*Er&Pc0Y*&o|Nj0!aV8l+$yzOYaxdBlE>mWC`Q)!bSP5$-!^EIj{4r&iIosJl|~j_j5gWB=+2Ja>-uCVZioYHcex!$U?|!X4qCUTYG4r9cm(w3byr0nYMO`#e<VghZ{ulyFnzruaT1`miYz+Cd#Z>C!nf0PnhH6k@IMmz{G>FfkAHWrkQ_EM=WdO&DICciwzWu;BcQyRvX(qD;l(aEo&;aMsr|?O@Sr$*p6~(wwbfU9_t|74&NPXc<xxyGsxD6w}GekLSBp4_w`T=d-`4)g`x@$f?b3UnlZD(WQT?kvd?;z?5kl+3LJS<(WBu^ci)V=Zw7nQ((;NXFByxP^Tm^sPCh~J3lB@BAaIL=PPORky3AQAzHH0J3*EXerD@XoI7I3Ov&Ae=G?DD045YI?!bY3-ip8_C^q9fYV<t<Fkr9=$Xm>7xbD16c#<F%vles9SEuw6hUf4l+2WY~9zS~J7AO*L$LfHM?W#d{d8;a;D(xRtCYmj6iVfI8XX}M5?mdzk^WfLCt5tjEMyxcE6J9u&6ZQJ6dNAvQiJPEDSh!jE%bCFoC?~`E|!&X{O1L$0ELyhNUCyN_u#FZcq5CdqqI|h}uF0%<7)6))0thQS;J-8aVG)(@|kbst+WrVAG#Yl@P<D#lko_l5}0uS}?8#F(D(U?$P_Rk|fL}560yF$-W*sft62$IKvU@1ogc9dHRP$x|2=7I^`b*#CDHh8HvwFFIzo7&qC@BoQa4pD&IY+8w-=sJAoBgnc0V<ajbBXPQh8co)qO^+u{?!JOcGQreHe0GYJWW1-<L*xU~B2H2|9?d5Deec>wbsOEs-}kiZ`wonO;YI{(11GKI43bwvMK`5mwqc;%F1l7TZGt>(#?1dzdZhEDnUC5SmX6UvQY>j-jk>1p=r%XR;^AWvP=S__<V6`tp=Bfv%Eq+mKz55j#5cq{gng0thO|aIm8~OW&>HizcfjO{pW7FQWmv3k&#>6|N9?>Km&?W>@fdpcIAxW4%ET>1hHKif%!|M(&&PGhxTZbdq$Gu(Hm0n$#`Os`S&@%Xh`b|0T=Sv_2VRNK$5ODkyE%cl&J;!cZ6$FQ(h1NN!kKu_%f$fBn=}g`jmrvaTvjlHOaA^jSvLb&G!R+Rzn+ks{Rzpu;38ID%FubZcX}+!B28bFU!=uk1I19F(zBgT%Tp&WGmW&uNEWk3bQgwXNwL|iNt49;#PWU=My(DQwb4Ag!Mo=0iBgewdXlYx25;v>BcVia>h?aNF9sgSuMWBaZ~HQNxn$(?Niv^LQtcAhrevU6;T^V@+X+GES!>!xv8`kI?Cmc(;fvIZ08YzbyR<HoiJoC%TtP<(kxW2Ezq}QGV!2+0Wo^|p(pGa&%Q|a?KRu2cfd+BnB5VYBZcqy0$nL}yR|wzp?llTK?}|D|nZ}+JcFoNfCA}A3>Dzdv@1W^>Hyv2-a*AJqGuK>kp!ti>2j}|aED(Izk(%YO!7)fbn0L;!Ax}y(dpC$*Hi&Q7TZI6ab5Z>ocnNFbb2f{E&?*O7MqVQ_ap)a)O1(>EFC>+f!K}G9kCPPu)nih51+A>h`nvI|0a`a0J-Wdq5cPg--8+yCy}{C$LG@q;fH9?fb&V|Cpc0T}m6yvAtKp7VU=+&wxbh|=?3LMNcVy8GcNX2GpDzYpIGdhXc)ez)APPB#!!c(#FcDR_H5>vl#Qo+(9Z;7v8I4x3(rm;O93YhJ+NWZtY0U>^M`v|bfT|G0raiXWn$kvo+Ld@;yFw$OvGLr!!TXel9fQ{goIbiL@(R4jOO+_ayr1Z*@Jw<!@m3!8DDY!;q~sQNNbYW?9;ljO*kIx@RtiK}N?k1ge1cQTxHs0>95#I(3S^L(Tk$G7P*rbAt0fUvIwF(>6yOZrDZ&?1b1`{hL-?c!9@y6K!0x~U#|uXHh{VIfd-)cAJe7z5LJAbTIT<8>NtacPl~px1R+czeRpRtSnFn6xmwe_5_0!0|&}XoBZ6JDt5Bdrp7SH@h3ljIk?>a8irL1lvA7c``FUMrky2)MrxSl+PIzRgqY8j3kEFAf~Y;+e>aq*i3s>qu(>nKH*5p*Fl-8F2HC;eAU2zRH%da`mWpOxEu*;IoUTg<ha^IhwSh&2IqCwyth{1h&uG8j+_8M|F{Jd7N6fz*3VUUuov+B3~a7PIy`E!-Tg5Ys`2m=0fv>EJ_59of;tx5Ey8hcz<B;^2j5la{mH6u|ie+R{Xujzo{?NasyQ#)|2PxpFb%k<PmYJEENZxy)rTmwC_%_UX%Ij(je2^5rrYUNB#MNuHh8*$+O+Gh8TKIl<f<9zboj02B{ZNOY)zk>e8i92XgL4Ia!@YTW?37L-S|#PkYiLR7q=SlP6)E)D0=L0hX#-dQF3LSi$o=PbPAXtPU<iwhOmflzRXyY*eAdQ0iDh7<D|ls(bicsHS{!5_!?en2R#>8<F?Shz6$ovtW~g-opzCimlIx9t*X1&&}^MNlga+#3%+bRK>f_+=mS3!1hD3V3Vo>ee0Atra7GAYjN`%!CRoFe1BfB!`tH1d<e=??>a6P~D@1nsjq11LV;YU!(PI=`N<_j9yVkOjH^hcr+UTz|BhzHi)ct3Bg;`=9hz>U+%$MgrM*ALUUyACOrPTO){9hlOCccAV-ht)9wkhdnV8()Jb-`1kN`@i~}?Oh~hm@<ZTU_w>4?#>~zgvUlOb6Q{s|RHL>JdL=S_8BCX`Po_xk|NQq^)7;t3%!UVKdj2D)X9-f(imM|<{m9{35c``jLzeTTcSPMJRoN>_GNzPIY>^*sS?#Y9{CwGrmRYzl@j<42f&FmvWI|-P4(A>cXoqoQ-bNzxX(j{=_r_lC-ICJ#l%nk*U@OUZM1;XRWr1HoIM<fr=8&aHgNA%rrC*Mt85f}L2J6Ei6v5SsZE}*$1^Z%}ug&aJACqbf$tjC>Xhs3R{3D%m!fTr_Y*g*4iWnEn1b#cX`iz|LzT;YfQtmjB&E=4zmDPLPt?K&q4c}_ejsBHM*KuC1rt(l8`BAFab>>wL1H8|3=m{ZQXR{L4yxEk4~9<_Dmvs|mg)CLi~!Qnd5b2W~vE2iq>b;By_bXQpe)4w$j=ff!_0U&2Szbx_0Cr7ZY#^8%~iSc^i1j9S({7gu-n9+caA!mCs50h%MC;yq|$ErNs6dfdCdBxu)+838-XC8^p9wa*Zk?71L(V2HxO#Co4c}7xzKV=H^BTBO@Wkjqwd*p8y!h6-hMPB23R)>)W&)ggim;LEC*$+ImG}1)d9f`6cA)v8*V}4o|0c%h=rA8Ub?W#~uYn)Y;5?X0SXs4N-(`INACfwH-ro$~%;AQDS{hYxYaR;|B-E>_VU>+SLO7~d&PhOE8d47b0>QG&YRI(a9uoE52065WX6paM+DVvO6-v87y%~!aQndU}14C*?cT{Zdas%V#7gmrwQ3im+Lg0r#RMBe@?+3r%Np$8Uw0~jw*U{P3c=Ou4e0re_+d7ys-$?cf$Uv%Ys#msvX6j#odjL|I77eULcK~S2H0RLzwD}Q1#@=qS}M|I>b6<^@pZ;kxoIC#R_q{(3~6}gvZF7(LdHjsN`Zp^ut=iLm}6+um>1vSGHNi+AGRNaN#F1)+5`1+uAKXNQ`<JC1wa5`bxsEzHqT|&&p=<pfM=P^0Pb}tu$A6yQ&0*40=93FXO+d(q{WOoL63nQ8UvTXyZz=hk<2Kb%8yG!kzR^~2-Wo4%Y%Y3{pBF2D8xt29%=H)$w&opwx5>JN#XA1O?N=Bla=Zd+_)8F{w%U&Ml9aJ5G>T+N@a4gUPyvwEDIr35u0E&P!=m#b`+Abhf8v_*`f&5p5XRB!JwhJJQ9meTRvWf9-hUxm?5`v?fU4ileJrH)|-IfC1rU&(NGE0e$)2@J93x#<d?Yq!w^GpHQip@}6BYbvO=H}!rfPyd3Jn?=EdB=3}iFyv>$pCXV4=<JKA-lp956ulWu&%U5zS(ZnIO{BMtwIG1q9bp6op!@*8gBZ|*<LsP5j}nt^4TwmjiX&4H4BON#t_LOKJTQm{YL>AK*HbDXnk?tlb=+$*J%RU;z%>DVsh9g$u2IL>%6BwM|AQzqPl6$w2Pq5d)l{&#1qiu&ie^y&dotuZlZ|^U^Ppwca1HO9ELrzG!qH{*)D*LSunQ1aF{B|YY=j(NDgj)UL&AXn@oa-y*1i$t9vZBx;Tr7c7e1)60a@J9?fsHi@;SM{j1)Q!4y5KK7y;B;>g5L!4~6MMyYFrThtXB;p@tTTiP}$@<KBm52*ZLzx&guCOzOs=#YSa2EwAu2yy2g0CBSc5D7BthID0#KIP@1K;n<Y$qFzb1qpIZFxCDqhrJ`qA-XR_An<Vo(E|x2o*Yv=<e0iTtKW&Ul3Ama%o?R+SAZ@_#tNz<jVN0wkY)$<>?(__;YzcHo9%R<t)lozdod(r2SThB_^e8)X;uAtV{{w##>78jX4g&>zqsi`3o|IR=7Xv(<w6i0(+%E-z!7PxNyM^U0`FxB4K&>@F~G&`A}G)ld&DX2ekghPG6n!fR#V&00-%Ck$e5HQxWWPv4h4vH>$HnKgBCjvkn7F?j!63pItM6p+U8)>cACu2M<B)Mpx+`P7N%Yn^Vh08J)?W*8Gr?aX|0MmSHztS@6y^VH0tb6UMARRiQ8~^&QG`Jyi8ioY`+jtyHw26y?T7=o8NZ6^N%=?i_f$3Ah=ebSvDx{k@sm!zWk5E+q+esOh0xFDTsdGg7_?a3p#B)q+0rSx1;}{pKsDi(MT&r6CJ%)90m_a!kacf;#mOeVF>IzJlVRqyZh}G-ESlBNvj*Tbzjo`^cfSK&eUI`=>{pYPHQr2da|E<z)<3WAx&zX?GkwYVA(3Rr`BgzUTp2ui`+duRy;jq)PB;Sec(a+<N@u0EDqDN0HfLMnZ~hm=45m;Qg@E4yvKMvX^aQTlS9yVS$Nib!n3ww$w2syWPTi<nQ{C}H22Vlj=Nnk6bmy<ESY)LV|Bz<_;iocE>c7&+XesJ)<1rA@85mkX6s-x<{rl{n}XzTm%@+Jiu+&DDXruAS-9%>eC7wP)h>aD^o}$QEvh0o5}J`n4DoeKw-cw)JOBcmm)9=gXksbl7b9g8Z%smn+z*t<g67qCx13kDjHeA|Cvby^w5PqSHd81l#X&)-G|9I+IKG3Yp9By6B=Yo=?4h3&5B;RsMaOzFU@$A~w(_KD@aFWBH>W2;{0L4>V$4h|enLhpP}<tmf7s@G#DF#P%$)3F<_z8d(-95hf+eE(x(vHOd|mc)PI1};etH2SnKlnpQ}Cug1TXBC)2A@CdG3>}E-btkpsZMsrG+5urF7wGFKRf-dZ?h+51265-3fDpem=k$!o1xsc|15Qf-2v#S5M1c{VjXNTXvoXS=N--Z7*BZ<k%ULe`iem&KM0eDL<_~Jous(f+uQ01WBVOX(8Fe3{p$oSS@v1(^3zeG(2e=D#Rkn;qwIUiIWFFb?2q-Hd2y3KoUR3fOXh6M%lTB2S~z*1^fxoZF;%&%3!2)m-#ke>T!Gp19o}w3Rd_N0^q<C`Dg@{9U%(`2cJ1boX?C7*n@Atezy?0c?%JR%p7T6a<aKQRJdDY?Fl=7XsPi>GUX?e?-GRJyj0tfwa_4$bI0>{hKIQl?V{r&F4+a*5$6b2aRv@Go^RVdeA{uMJQl^bce?<4lc5>+Ek+fgxSh;^YHJLrXDpad%`#%yk=&$dlgHDbYp6CEqA2N|;P#mO<BR$F&Bxc|i?^Tu`r(Jg2D{XNJt5+WQ&>+N+Tv!g7B|zw4N5y2i)7Khx7r2b8P|9=R$q1%L5vxr?XYOzb&}!}wbEHui7pxiXNS`@u616^w_Y?ChHb7Fg%a5G0=W|-v82i@II#K@`F^5D&s@ZPC%Gs|p7f%+y~Pdte=q&ilePvzoD>OL#D)ytwhOT3i+Md(j{pu(&4HwjzCh~eD{(lcdoM;GxnQJICtO-q3<ahO*qI(+C*y(|4BW{y3?hR&(F5*8lEa5R<K&s9amQqv9qom*EHaQQ)7FSD!(m7&g2ELid0<9x9$m1{)2-S?N)Ezyfw<;7&lKJ>^t$7zXP{4lywNKNHxL4)w@rEw)akdrTN0F_J(!NvRwjk@Y$fd%!`gY0fZ}D-X)l|xr{&8tcHT1L0eR2h$t$`dFV4z#31J2c^bM7NM!-mxpiM<1>>}`C7im=rmTk}#C!wY_U^vl?)P@>gZ__=Arn#ZE#@kvjlW&1Z$ObJ`OTm$$EjPc(jS*|lm~Wa%bq(_)!$Gvs7lZD&7z~!W8N*`EK%{d963<92b_qe4P3*j0w;mn1^{76`fu0dzUr{kkiySHtEq+E`OLB+X*ao*dTrr2k<5C6^iu*dzdCqYKMMNwn5NRS>q?u@uPP0mMnw6}5zPl&AF!v;I=#|y^Rp#vqt6f5nLOMIT(m7X?_pQk<)t~9=7O<c{6Uc!A7){5c*J2l7V*|`gs@dcz2+qsM^G({hN{;W?(RfLEULaLVoBF~5w2c;Q_Y398CXY>%D^!+tT#7vXD5{*QfrrYX*BM8uZ1POZn&-;Dn|YE-^#N!|NBaqoZZ7=_yK$E~uf*1K$1@%yj?$1i`o>_>Ibfh?yfNEF*c$^qqntOJJPM8unR9Gg%IITd&`q+@mN3KN2*cZ;$T&3ZArtsUL#0B?SaRpZ2|;2gCBSov6(?xW^#yrDPn6Xd93&#m^&#-U27raY`*cHEfWkjxwQZ;g@I`U2j(kRDO19Z2L9RaRk&j=tHC(yS2yt_S%62?cR&7f5g0L?e9+mN42D4tOwDr=oSB0UIIb3|oL^sonMu0hqLckN4QV;q8Cr_P>c8S4e-Y&vqlS|$mIA!J$5yB^437;-xNfhbpzM7ag+=+?%c~i(aIkB)wH}XUmn{LYuX!QinR?f~m0J4M>m$PMVhE#*j1^AqA7mo%Gkl!v6_qD`7W2T)T8tnwJo-p_9X)SqaNUKwGDL2mB8ScU~U1$T(4qe!OyS|JGO8`aj?DHxtscpXZjINc8E_pMYi`kpO6A`+j6;H-vdNKAoAO$043Myd-(Yu};D|G7X-Gj&D!Na?LsEXmi5<%u-YaVSuuIWgM>39K^ER`<VSTmkreA1-VQ^>rVxHjC`B-dw?B;DFYzWUN|OY*=iDrxF04*2mK$_OU1Mlgvrf&rweLhs&bF8f7z=|)GgMn(r&G<jEMdd7EKj5yz)+TAl<JpxM|(Rd8|t1D%8(AF-K$Fq_nFjm$&1)fO}P}V4<*q40)0^fdX6pDoKA@s$=a~|tu$Ps9pntahbiI3*dNEO)=m{WKrM)TxYbq^N<2$xbv;d}BNu9XsHr1K8i4Rm_w;?Z`&p{_@rzaCBYo};J45<yR=Nqm7f>JdBC9nDVAiSc30(d*J&sT`BHTn{`YH#w3<5z#zI97w#9F?p1X1(ZM`-jJHyeKB(>LJm7%eo}MiC-uD$JqHs^k0^@%h@!+lVrKPpv9Wr(bwKaxWQb*(lBHnltnZqAzr4H1gKCFG$J!cz(*-SDj1HE4VcnIthi$w)?66CW78T_%CQALi-KH+u#THlWQl~wihAX8S@o)keW`oHX!_uvRj3*-XVxq0aqM2Vr`Rfo_PIn~<Hhse&Z=5}2U|qwDHSgV#Jcn=i3Z-rA*jOjeBsa19wr<{0_?c?+Os2=;oO!xTXRu&CSSGrg;rDdy;FI3Lr*8+p9!Gd-|2BXHkd*B(;e*Hs@T%g$`)sq4@adQ0%Ft}w51)Q1t_+ih(c`Yh+m6Xs_xP%Io)+N9=uxT58ZOJb#V=Z_NW6f(GI02btDY(4zzDJ<M@i;GI-+Y7o1A<x6NN~+Js16Q+3hOyVjkE&E#osKY?@g-uA#JcN^X648PovXyFowWM&BEU!(w>ycgE;2nsj)94aW@5L9z_8AZe-1P^sL7=H9jaLO~2O_Q`v(2i~+id7RiYO=q7D0;hKNx0NNK66nfas4Ge|7!IPrv@Mbddw<PYDcNR6CI=kyNQ!mG06e9ONb;hRCsXvK9hm5&F%c+;FdXXRNo$+||J@zhfztuZj&!rMCK}<HXN^E{ApajgQb<fs8fr4XWX;|1V8F%j=0)ot*v&iQ2qc)+SJqTP%^?cvv{c8Ffc@0Ld7kDr?+P$$$i}pQjZIi1fa@qC=znwY6S`#1B7WDI){w^L5V^)qUp|9u0JAt*I7gBWq1R}27!h>z0NGr9&m^hh&?-V_f4vY2QhmP$c;y8w2wYxPp0LzR`;|A3EF0=pVqA3}-;eK&r<ad4fz~9=@YHDVN#C|TX{WMm3IvG;eHDXd`*4%b>+5#RyN_$Udl>w|M=UEB+X9PncH_D!L-_9SJ{vrdEO^Lqkv`oT!l?Bqp<LJ5NVkM>&&;UlvAPMK>~4PU-Q<BZKR#3~IOrkP^q7ML#|Ty)|5b<J657V9w2gH-rm{O?Dm@EAAz)R9=UH=zR0q8eo!k;XUP-_Ge^F+nh5')))

_TASK_ACTIONS=json.loads(zlib.decompress(base64.b85decode('c-qxnO^;kha{MoI?t|uo6y@89?3IY6Gy-S1jWsb41b7Vt#`+-pX6%1A&6)0g{W3BlGOL<g0SjohhtscKRaRAIWMt&W|GoJ4-+ur5-+sUNmyZ{}+}__`JZ>)j<G26%xBve1!KWYp{@d^W`M3Z1^z+Ay??3$Y*V~`p{&f59Vsr8OZg;V{eB3;J{LA~hHy>U<eENL%<M#H`e_uR4{$q3U)o)+_`NJ=ZKTIBSzkT=a_%)v&@Z;O}+Y9jn8QbCG`yaR4Pb0Wq5AFL8Z{NN7_0zjQeE9rrhmkEt{rtC|zm$J?e0cnK{8iU8_U`ue7ERd4i=Xe_Km7Rlz0ps*?ft{WqnuW_ZkOr0J^zF2lYu-vYP0y^IE>Y_MqAPk|I>E+=5#^UYXzUYpE+~h?YVe<)Y3lIPuid%K5wg!7q4&eOx*wfdu}d%+P=H{`C@bBk0?&i(<3%`XshK~4n)4{{oRKX``YA-p<htG#@g&I@d_U|+w<?pD?QIlGFLx89LBeL)aS)3P1Ry6-ac&K^GB2?YyC}&2S3jv9)Wt^^Gt{5?Y{xOV0^8Eb?krj^u695JRM5BL{|6H(xS;sKmSg>`K5jwGnDd78_zp_XFO@?{Pv!fd^P+8O{zbE;d?gmWlMYR_{YbCDw-*nt7LcW2MABV=KSc5<xS7?K*(3`hbks0{8al&@<rBHzP@|+Zu|P-*FSCFKfHbS_FqqD<J6#Y-|zUp)z`myfA`CU>o<{M?*A>?DTgbBI9-d^TRF7wk`D(kpQbQ|(mfAW^*A-z7nARca~{8h%$aaLuTH-i%}e_6_V)SlPd|7o<t-2}kmEKuJU1Da=Q0_dA9&>92kFFsSJ?YlVNx2uP><IR;8k)7hHr+8dA)KlQr{|ESO=HNdp24*+nZ+xO<dDx$NKBY+vv@h`<<D=S?)8q1<~5CzOm<-qhQhgIx+#lb2>VRhws-;O`M6tdd0Wz9PP(HK6=ahkMunVyt!me;zZ2)TJ2S_*IsyVtB?MOj!*hS%MSuugF#9%xX!No<tNk&OKxRpJ>ZqVyA{s8@Pxzo^B0kToab4z93U|B>(JDTPY4F2oUC-}=fHsK@!8CPaC&GO;>8C53H0U$0tTF^tDgJiy|x6T0sM(jy44MZ=fn(`ZZd4&9~!{pj~}HYvyO3aVXvIS<j7&Bv3kajx9|UwyD{KGKmK(5Q^(BNK?+_5T%{ne(x>%ukl<~iL)m%?!Q_eW+Im!krmfc!!GsUu#jgg)J@F#F$L1(meExbzLAb27+oF4Xg!D64cbbEnIh93NZksRH7Xs=ID|RjywwcrY3SRActPzX*YJM*D1ZVraB(G@tyfM`&uk0G0mweoVc#A$>bQaKPYV(U<C-v!=!zqy=E4!P!lflFakm_R(c)UukFUxJS2Ls&5==mHz0{&GxZE`qQuBS`jvZKp!yawa%j!S*wd#(PVkB>jQ3il81Z+G8s-@pHB5!nPY8<V+<Z#TT9)3JbcW+`oejV*Qu@g~A!pznTs5OjUPxnn$u<Z`1wmVt`HK6U0n4?imU)bSlaK+<~FVe5b|JU-Pn%gRoOFO^#*eTWs9g5Abk+3=9(wKZ{DBYR?;bQ;JVcE~OF`;YG|GxyN)7#prKNmR#Qo!wJTA35kLFP@-W)aX>p=YjJ>fuRDNmdKFeADo2s*kzP>>`+ifcX7N3Q+&K(YxsqoEIJt1VK%to)Q4#zx5;C{Tn3Jn?=A}emM{U1xBt<t(2)0f8<<X`pGuBC&eE}4ukP9X>PV7J=oraub{Kq<@*3~{rPq{ZE`mEXccPF-6#abWUwo<cBaRvvl>u!~`Yu^4KjjYIf&lI$IIwIFvL-Xgokb$T=$v3K!p#gYFp@ARuE1BVv2ra;ojn4)QwxtKfdU9lYwI+{r8ib;b%EY|S%==DHc@o4<mD1y9{H5%L0@2$)ZQ@tUENs%?^;5jYh#k`56I4Nhu)}!5e|L2d<*_ZT>g-PCL@U0fnhw^GK4q|UL)S($AM+Qe7IQL80Q>O#^TV9^?EQAED&HkZpvj6AjoO4lLtoTz;`)gG}s+SJTHv<@?-{{Mq7U}SQtX^ME6{)_<_A12xj#&*n4aZHbb00e~F;Kk))rF@wrNFjxq^MTQvCV&T}i3MWb&v^aLw5Y7jbg5~0Mr9(}-=Pt7vdm30U^f0&o7OZWp9^xMZ89}eAq@WV5ZMXn88atRHYLm2WWBk)fsy0$|LM#6or-QC@%|GeBU^QVaJ%|%UV;Q2)s2e!WBC7_yB*Qj?Gg?$`)4GplsHA`RN1bF@7?(TkDLx~T6V$7xK@WJ}rRX+7;(H)D5FSntL0DGxatOSl$P=#LstQW3ZnEuA9#)#$#n|potyrJ@V>tKp%MWLO5x3897)>gHho57<-TxZ4wOKkYdzH?j%wVjWzd9YjdzTm}|_Ed()*P188S&ze81SJ$J?XbaSp>nL@Z=9Vv>4=g$Ty11%7oGFEoD3X&^|(}GdlQ3RuH~wRQyzf%7MSstjAIaoFIOpgfDwEnc5L06A>dw_Bt<nlrk8m=y$wW7M;2gZe}%?v(RZzy3@YW2rw+-`fJ?&vXl`<pfy4mcT3Hwxb1XoCt5KeMqU5rA0E+*q7gAUozvP<9=TK^+W6*$2$jc6m2_|Wg5?yygB$aCTVN?K0OW;G1Q^r=LCNr+~LkXWG3wkb!V*psEAW7vYz%6L;>rK!pf(J*bikPEyyCz#3nKOgzIiQDgQ>U9<JBWc@W3CX1cH%7_JIClkJd<Z@(H<+75XCbIda^Q+Tbg?#v2T!0f_WGWF(?UBu=hlhai~;B?*v=AOJLM~UUguHUsoJ3BsD23$Ex}aB?bW)5%>t7L{vQRjO<_w_63WN&JSB<<hq8u9~KSFCK#kXd^jVwnfeFUVUxB)9i~3r*+<>i!~l5f(<AfB0A+nWmTNua<HnBFQ|q+(M!5r&NaW?g<HgOxK?aF{k7R*uyqwYf1NZY*QgynV+$4%u9s<*I*}7VE48o!joTVl+kGex8IwYTdEq;CgBPg@f-F6iAJ`NXpN>ouVoFxngo;%A>tk)oK4+>)BQat?m`HmeA&(XQ$h;&$U0B95Eq;n*W&`)pQ{rPj!mWSWaT7jvTd9Vk2Jq*MQ%&$wjYdmAW%>nx{$%-m*_OR`-kU^am(qZ}$fm3!p(+#X5>B&6sblyQiHNkC_&;|qIK0XduMhH6&Je#6RREVV)n=d5;nH?cKZ>bmvSc3FiW>|Xt(YOxAqJm_OC(*m3B2sRk^0JNqMIi7)xj~}bzFqeT1!2(Jc`r@HzN5Fw5h!Z5B_*3pGmirMO330J2QOJGoTzpczybDgHap)e@E_6wLsmz7Ju*rgZqhykZoTlaNLf!OSv2x?5$QulcT_f~fj$+<A8e=sX#^{ah=>m9U}KzjM#GR<>p;Vp_&Ry^H?uxsU+3OI35do8C49y!RZvI|kQodRU>{-lSo<yev$Dmp49XcS(O#Y$L$BCkZ@APT0JVYs`}E+LDeKC}3`An3W=Nwn5vuYK3kPIii{?LmUk3mJm9*ps3jVAi_kKxFCcu4GY-mD3&z0fOOrdXN{^+Y><xgzGBJ#g>Ui^lJ?!7{xgMonrpkfrm?mdTZJ^`Lo^-wvv9-$0?H3AeaM&g!;&wiACOI%%`fUH6tU+VWjek_G4XREIf_ZMUiLARpA>3djQ!*2SZj5KuL$zZ!kUwmotKpr)Z*NgZ#Hw6!_q}3H#qd7JRPTxwgph!f#dHX}L&aLbgOG`aLHz=RzB$XG1MlFs&N!#TMS9d|fO*H}(Ljj-&tT<+hWJ5u0g@tU)S?o5XB^*OP`1JvK;&0E;Jfw`ORa0w_x#w_FcZwO6DIJQLu;+knJIK=XO$_aWofqj$$KOE&cgFn2n^>|c8ORH|Y>{P|BJCRYI)w$~OL5_m-Ym1K8-yLHVl~!%VV)`Tke{RCu;!vwtyaJ{mLU|+0s<$Wr`>wJ770#7f5(bbQp~c;x^a^l4&%1Pd6)Ouw`T`lh`=6f3^7?!rPwOF`U;2mkjZ>A`ZDg*V3Vvbue`n!905WM5=Vpug=9~(i))V>bzSUbVS^IrFfE{TEPY$57GSBX!zY*+#pIn!xNscR@~fNh4sP!P#(DBATYo-|88Pppr$<w;$XD<+&?S-y9A`gxw{qQXYt3i1i<dRjjIryFKOIgy@DZBeNdGGhnFTJVSoiY`C&<GIv~mjS;RRv&jyP&7(O6VpINmMFidZ#|DsPOFG4F-_fFG_C*c^U28tb{bg5FC8snP-QA*ZHEpdw3^jScyk@mNrQ2T|qeaHXhAaJFIj=~k$Q4Qw3YGWgk7ESl#tm6MN&x>(o7k|zm*H3z0>fD*T-;hVl_VP!jfqC>J$U_B)p?euC`{=a5~Oc)F%8=L>MdK2(3=7si=lTEA3sqKJYBGut0pjJr&m!}*KJ)VU1@@8TyU~3LUV0ioME}glm3_8>);?Bs0gpp$@5^sO_0Z<?qw$@=}nJ-%D;ZO!;UY=d=_Oe#>2k9Rj#0Gwm=XiehZLTW76YEG5oiEY8EaDxtH@z-5eF1T9q>LbDvK!ftp`6_Uc*O3BPAJPtN*#6v!@!dhU^CjoTHOvF3#J4pV29KP7f4+MKHmV!KM`L*-UP(JY)9M#scOkEAI3qqHm?wihmADmhzsbwLA;m*n5*?fSEd}}dl|ud#EB?a2mFglh315^mxJ33kxuD@(ApC4QD<MG?iv(uQJ@iOCK=Z)Ek5a$?w%Slz;^)?QzB<|g&-ZhM<D{{Dcj{L!u=mkQ!7I^HLF?2Q7Kocb%yG3BivW`Oa#em0jj`rb}D^@)@e9Y2XI6ZY+@!B(jjf-#76ngrm3n@4g;@V#CfsAh^FyL&`3^goB}x9QH-CAPWd=|mS2pLc3}kU1SF#sU@ULO$bc+S{u%ao@z`rW*`S?_VI5xS&r>k}BI|K-{Y8s_7z?Ehbfk<qnN?f$@x0b=1#BU<v0+IjC!HW71rB#8)<+C|<DLQs17sff-No6iOKO35fLn~Bdc+HH;MpJv%L<Yn_OyP~2`Odl*vPNCR24i@#B#5R<U*$tXHnxk0`>$c=(k&89TIguUY_x~MExud1EKrTsbn~Q4bPkamw-qK%H1V55b_dSY=fs8SXM&rpSZxN2)I{frXtX;$TZW@?B(xS6hvJ438gEU+mEj;R|-YQ1kX`#NppTG70+`gIcV;N51V0{J^#t4>B(*sB^2QFy&mp<x_!7S#(Ux-gZuO>H4gDKT-NL8D+Jj;BkD0=?m1Ve{bUr@0srdMYLhAFe>bJP6gs>VTiBSA8sne@jYu=`BVm<jcC8+o2XcH#BgKQ6qI29NUU)Mm!W{y#_V^VW=|Y;5D2iI>B723I7#aaFyn{x({Bi{_nTucn4L6=@Cfyg;3G(t%zYU=&gFwdCz-e`EF+m5)&eBxmYe)7afc2UWVCIwuLgg4CBT)#!f3<5xN-+shA&MlIT`p*|0w_u`#uT^)wM>AKe@d{P){kdr^Cy(!D+-dTNXXjwSgQ{=DM9y%b_7^!Y&(c|;<RdiGa65VUE?!TD6Am2uno%@=LHXXv4T|>S|GKX*wnm2YfzUT7ix;I91-qw!2`Q=BY_mBsu&YAfcoDB%5zsikxf4rQ(m7_&!IdyjOS|#(B>|Brd2rwsW+{G8z$(H0KaB_*a>mLSw0W4At_{;n2(FHuqVi(^o6Z@o0d+ZkB6jNXWG20bb)CXoY@ICQ!P_q7SDjAev#T0yv~t?l_^f@>X@wU*p5!KCPifoq99I#egYSb2cmrb;HuL2MaHnNzJg|l&w+rEvfX19i9~x*{!_;Oa%nrqPfREyhAKW=g5(-2{dPb*7?L|y^E#K2pc`2C>Q?<q5kG-XE_T1o;LfFUBd7vj@@>5d$6EcsUwYVb+G>U>x)XEc!nx6Q^%8JhBH{YUIM2l{xfcbwI}s4W$-{wBVOQ92nLLa<w-$UfBHWs&)OM5OiSG`eAa~ovMNNI+a_GcCBs>NhNz06~L|;XPqZLW>simQk-Ky;=7c|fzf{6|I7J>QPTuA2(!8YY2;qGi?(YBVd&fK8eX>Y42=GfKf)s~rW;<X+T<PM_o5^L7rZdmHBT-9cq?Mp-PVtZfYYEh8@xlcurkD$8d$a+^ek{)L2sHVG6!Sm;A<K*o?&KuAbpwy`m$DG*!N7m$VFy_=+FTYvC1)n}CG$(U$8J-jJ7#F7p!e-6H*m!Nz%jgFyhWO_vYaBidJv<}EQT!)2Wh5<|!&Ggn`@3!xb>#fnElWuWs;wPVYlUnBU_?K^QpGZXG-74wDfB||{26o+mYfeipqi^l+RNaW0<qq1)U4v*L>N%$sI~}2>1{r=SE<Y=)~QFN>BQw@&Q|Yzn92La5v?3MNhyussBw<fk(f+2_Fu@ZpVC+$yHgRmCF_~<UDP;eB+<WDA!8wmt49qJ!x&bW09wgVd@FH@FD{a0Zv?NPAhRaxgo-z|^pTei*z)ri+QC;z4_f6`5SLUS%o(sGg7HNcj?&h0iHI))DrNYdRWPyzn(olvc9YRQmhqz7hhsUV%u}Us$I^`jv|*18lofW=2p!4&%GzZq=r^;5PKTccG~g|#D(G|a05B9{-J3*{1Tx}^*^wRubR#4=B1R%LY<3Jlg7aS23GwM)7159(Hq3Wl0TVjfflZ64Ll%zW`xC|G3cx(AQXa6=*qy6}To6R{QVu{_jq1-0*Wl1*J_eabxUZEyEW2`t7&PWasSeROa@?FO*28yRqm0K^1NE4ecJ_qI$0QBAZ4?w%6>tQ<&_&2khuac|l|wHj-iQLGy!cgbMTP+>0`p;2k}wfM7&*qlYr@+-A#yEP(P<btGeq~t>Oe$~aUUpRsG<sx4eW{4MHi<(_6@Qmr1QRO`ZOKG`f(RNUcX}I0P4*jCbP77SKx>lu><xCF+Th~f$UyW<xKX-8V;`~)6MF%=rd-84V4Z^%VX!|W2ezYhUl;s!oc@Ri{j<5FRv2J@TRGEV+w|dj+E@G73`bDP`v(_&=G>K0`ImOr`fU)6$6WEO9XZj1?z5~A7UF|y1j-kLjKE9X2BN1QK1TnlJ<H8J5~)9gw{6$<VmXUq9B!iRel*@IXy=cnbvQ<Tz48xy(lWRnyM=1Rda0uFjFd#RG8aEJ<Q1~Y-^`P#3aTj&AbUY_0ifSrpcqer2)&pX^J8$k|7|aAWxU9SD{2OB)QzJH|P~E0XhrqKcmzRowL~|+dz?3GEDy2r0CHXRJ9tiwhEINHh@~=MsMNG+aDU?wWGzeGdMM(zHGJHGe8O|r0?3&obAXwRSD(GswLhAKJVx_qw;|Z7>Ot>y)hu-UXBl-$IaWXQE>zXL+j1tw8`YlX{*MJi|Hbz7_V<hJ-@p1s77m~>C?i!zk4XQgQh{EGt64ECpwL8T?2@uD1y}O23MXNM|!I^m^AUBdqR<PiXI9)Em9d9PskiB;F!pUgZH_Nhpg3Dr!VtNvcp%efH^1O!K?5Cl!vnNhn<E6{<UZk#-hMdPgt|s1o*d2Q4q=?m?%c-N7NVw6Zo_qDN!S}1wXit%)LF76l=Pj-5xSL$w)(`Mgs~C=2OQ>s{RdknqX8X-OHgMGU9*%@S=^;K2g^9>7{P7-y$PxisX=j!nvG``!?5)-S`<|Zjh9m5v2Br1Iv|HXuTBYV9*Ou<e$<$w<^lOL_tLTgBj0Tf`^_yl2pnI$!))O<Yg^O<}7Hetrgt`+@0k3-ex;b(F9kWZ;D=3B_^3YzWISf(25EnUA8Y&wn`hnc$ICnXr6|90Bz@6ezF7zo}(=EV=5|Uor@llQ`w{oiqfXc?RvFqT^k`R&h8u7AN&<4gV^-ADPH`a@(Gr<A;5!@NZe2!e=2k^EpLC_($%;oiWr7yMq*R#Bt7eVVxk1|TAW<9X_KO-t%`}8xI+bG0HM2;S+^7Q=aH|l$-#cweoAJ`=!PTNCV|m0Q`ls@4{L;WoMKC}*@6?&M{9r#aNfr>@lM$P>!h#2UXKj?vZNmEd|mK#Id$FXE5Z9zcG?)ZWeYs}FSXaJId#%~!0rKCsr%*92o1qyGlz<GGGqDelu(fCzwwN;PL}EYn)s>^BK3p`WD9}v(sl{dJByIM2hGO2Rnp}ZDIUGPg6&ZcXZmy$i$}7b*Gfv)?jF?KZH_>vXIsvN)g>uV8aESWvBKP*rsmcel3<_AXs&Bwr1hT^#%HS{&@LjZ^wFhzc&eKFL+YDIBY&kJfU7?q1R#rc##)G2l}dXn-XvW@B~7AEAz)GpO2)*fM_9>%j*$t5JB+B`@8;)kZ2<*8rC5vf2(esACk#?<-P*!BG}Po5*y&r`O<<Hk4C2_HjskNqdZA7<M;QkC@;j1zR&RSsopq{LMud($-}j7#;uUEC=Ea#Jk4+F}M|3eke!-zz*1Ss}j+A#gI@bi7vNl#L&^bcgM1sp?8yG(Fre@p)6h~EsQV@~7VK-mNJ^OeO;wvE3;f#pzW#+}<BQ%_7Ewt6s+^z{;a{{IlWrWEsGp^S8v%)V=yJLMe76<^qT=03HoES01t2+`m>J8j(q)aGvZ?@~Ep`*nHX2Jc=D|+&s){RHwO6*T}aHaA(=@CoMDqIdehoQo8IVvR?=AuwvaWf1>9KZLEM?<(W668iZ4_(<n>ljA33ATVhi>P2C6W7zo30H}SA(~>Dl1b<0AQUtxE1G6=1<Ya&xL`0$Ql^bpka)UCETHC6Xz(yGGrM!eE|`keysoK0=n6y?DE!Rry@~7rSdv$gKz_dG^p4?WHoqtLkqX5nJL*gI!w}9i*BxKAPPisPG>{WX-Bm)L92jhs>^eOGNK0Y5y>>m)`w+BdY9H)$^WjaxH<BdT{@{7M#gAVV4x|hQVlOU>nzkoprQOOxsu4UxMZx-dER^<XOf&OtV%C=sk;}<bodP}vfG+107)m)@pp%GSE141iK&2O%4vU9(uE67?s-mSWaYjrmBQBC`cFu3iu08e|ri20|NH`1~1|pfwB4SlU6x+)r3Wp(!y<YFjub{i&cb6O^Oh~k%DTL^P7q)T$yYiHW>@ylFK?{)*06_~Ne#okE@HcJb0%U)CqK7qcDxLNra;$x|yy%x$P8()MHlzPxRKr$s=*!CqOuj-bFSdKA$R~4#jOX4u$`rZd=Sd0II&~4ygQfPI%2lWD3OUuIpR+&DC-f=>rL;hRG5&V_-ySQAXZi*GXRA3b&L^MW;EY*g;kK80x>?Oj?L@feAbY|l8HvtTxcAEOvuxzT!x_~K^xK-S#BW)!zgz;N>PvQO>IC0xXxsNiExCLjKRm6TeD=<sy~86=#G3okY?nfqid>gc;mT&@NDwG4RcNChjaL&1ZVAmRK@3P$*9~=BU@hL@u+)y_<f;BZ!G4yq3IxiE8a$NZWt>SpOvuy5p@JEX8<MzB8s<19eQZ3D0alx&mECo_K&x`7)Qhi;1x;yu@wLim#wjd>dAFaTo1xwpq;v*$*HfXfM_qvvHlNSJ>uzlQ$*OFVjLw^V0DLjef>PqH(8AA9<KW)JF7KV;V~SZIQc%sb#XW7Bhz{dq{(fR54%y5OECi0IIYEO3!GOLsT%y#k42M_Om*|n`NP{;@UK(m2tOiC(V{qV;Ha25|yoD8LXD~%Sdp|Rs>pPH>Y(|tL%IgSzX5<P0V2IQ_2DmH^$B9?cl*Ilk+7CVOsMdlzyR{M{+O^b+vxoa$fap6x4&oUI5=y(VWP#ghb$ye}*p4I@0fS##Rinc{J_q}Z3be+THrOftjb;@cd9Oiw-H;`e-FCKCg_5P7an)*`3)X_Ond;aLEuc8)XcT%(#ZJ8gdLO7~X<fJURk^Zhx6O@(r79`Uz!iUf(FToV38!ch1Ad+TeV)x_ru6MUDQGmpAd<L|&cIigLvH%%ywsss1=XPru~5kbj~4debBR>#lgsql**!IPBa#yJawrKzXlJ&o)=I0|ZPi4BrfC#J4JfzPg>mFI*GK93>ZIy02CwSp)&Dqp)nqh^TL2!9OzO#fz|uU;R`E>tqttejcHOg5hC|I86wnKLBQvjGZC>K6GA_xfKQI{P0f4ebiP4-Nxe2IbMdb)lRrswM2$h)^Faj-Y0>}WI{kkc;^>;Kr>A;7^go-|pI_aQFs-mk_W2h$QfLdy!j|$^+6#7<HD(d+2B{73b-VF%0ivGcDs&azSbIaNjrC(MfNe*bOv#CL-N(Wt$p4vH#tHtYc7psjJIx7}6mTdsa)EUvU$+HQId2+S-VkndY{8PYrns@S69?vYRg*O0=?}{7QQPme9jRg9AVuAz?CJEJiRnVr#>){k(#pdZ%c+qJZq4|8;7q7R6eDO<N!T{Z}hFEHfAdk^{7I}z5t7Q9)#w)|>x+)Dchw88oDBF~~z9=xqIrQp%=|u2aMbSWOkwUdOxOqlP+;U{oFWU3lE{j4!N)#DX?lsEXAh9VBqKgPzJM;nP5bbLSjKit*=13H$0C^~fTL~w19-L^6rL8NWL4~tQ6R4S8P%qNc`Ri%|9gOEtC+q7n8C7OA^^&JCAPWLBq+s9}26^$^ytXc3&_Z%Y6)`Se9(?3$qK`^=_xeNUeY0he(^gu6u8DB=ehnHEOGKePHVMrvKmj#l@K?bIVe7jdYoZ#R+geV?f4Hs_f`@HI#cH?-8PZ~ktQI<6Cg)_R$FwJUo5rU~G9J8Pxvg$=P$h9OZ9G;wIT=Veqp*zK7~U-)G&^*IiX86UKZTyPS5e#Nrb&g(PuoI+O+Wuh8c_|yQOBaNuTLSm8ley&V&<6m(B5!f0a)tQ*X0i(4>PZdXMXxQI78G0<ozwdJ$Wu6A|U-#=|m#eNQL5q?My-05EGX4gTmc*RNNtLeBUAsdD1hSm{Y`OszS=qdp2rOr~v;+B?J<9WzhhbrN)h3&rK8CZl-m*V8GYvCB^%9M^X{ntu-Z{G=@tfP?@D*IEZdd7f@E65#;_YHo8cwYt^p0KjAzpb6X2KIijVQBx{Hmnn{iI3(Hc_g&sZ>Kc+g?4hmx<u<+<Tx^Gq1g<0Zd<=}0V6X|r*Ue%nrG0K;wcpZ%dos*w%)(JB@Nh&~7K)v*s3f0E%a>lTeLZ}Wgbnmw3UcJY#+v#RT-}J(Cj+A&MouIANQsE}_xdI1Cr7%0Mt&7m05IN1)MhE?3uKm2<j>zKKY$R}+Ds86|ld0B({c?MM-#nm`%YFZaYw8l)v43RL=6b3~kb~Y>5$XcpJex$cpSGuUUddl46HwO;Vk8!~|Bc;D*~c2DDAw4`aFB`7RcRBRple`>M_V;#nk-Roqh>+>prX94C5`LHxmK@{9X_gqjcZDC;xF+cnK((Bu4U&txSy{JFp8>mVQCE2LB7<7+C5=Cr$P!Lp*`H`2>Nt|m~0hc_l(mhb%;t8Z8ZVsN)J2546)cQ#m?Kgq!jJyyKU*~N<!01jo@VfRzY{p*`Xr8IFI6x1iF6vYjNUJGFrcx9>Mu)U1m(34g@ubtfJIm*3Au^7eMX~04luG1c^m!5;ItBWy@)2jd_;+9BNW@lIJM3azL-wpONBG_npR@z{YbEItQ$vtA%E2?d`OZaulJ8CdOSXeF*{e9=+b^eIQ-e(u`SDt2A&)6TYQK#*vPT)V{3puvIP9cL{9cED5EZ^A|xxk%-x7Zw1WsSH@~iOPg*6!e?97cxQ;^mriUzu<-+)oq6IlL~Gc)?DIvAvUY79AcBTYmM#)gQ6zDje3Me$%mb*POM|?bOn{PQ;7s!66cR2tt5rFch!ZKTqF(VMiJFc~h*Vc=@^rLf49&FG4oP3ggje;u`kqZD)Re@1GMy@Mtiq7$k}GWpA&@Eqx1PVgvz2M>o<V?&P8W7GLyDHi6(}i6v^LN+zaOv9EHApRksvFOHLaJ-nktdX)7r8Ni=!Sg3sWpA0`2iD${dIkQrfj<lGuzsS{E7m5O)F&LCkO~M^eeQDsPM;7;u5nIg@8?{PFKU{7wU2-k=#@p76{Iy{cUj#Ez;)fC*(y^h#}^vP1PqT?37*3vHEXxC}^q@m0MBO8fDS^nwEL4AWa?rA6y+s9X8v+Lq$I5u8E(l=HU-NBn@2Cv4`?cO#+}7}RxC-1o4^Y4`RG`9*<f&JN36LtR8Nbt@Po8A;O9-t2XcowT9)lTuzx&MdiGj0g496kPP2+Aoc1E1k(yvX+;LR=p&8OIST*omF)k0jdm5=jttme2y`bfa-944a%1}SAGE^R4|w;b?kZOV63$HtRiNn^i+ENepeZm68_L<Hy6W@2~0W?&VZ9wd!;0bw{>?Ae8;0qDAT#;mX0&)jLEvhvM_|aPoumNxbl6%GwU-DLzg)0)hC@e&`kTeJW6p7QUBAAvM%E?eCsX)qjuC&Z3Qtr-4<CzzO;n_*oPqUqW@k7=Qo<R;dGjj+SbmtT=E_qH~BfQ>>YG0RNa-X)kqdtG(B<bHIDmOCUIcKhEJ>rn^gdXLFS)4{^Rlg07ZRq`T')))

_TASK_RESCUE=True

# Keep demonstrated market commitments while repairing physical prerequisites.
_TASK_PARENT=intent_agent
_TASK_PROXY=make_agent({0:_TASK_ACTIONS})
_TASK_REPORT={'errors':0,'late_input_requests':0}

def task_market_agent(obs,configuration=None):
    if int(obs['step'])==0:
        for key in _TASK_REPORT:_TASK_REPORT[key]=0
    physical=_TASK_PARENT(obs,configuration)
    scheduled=copy.deepcopy(_TASK_ACTIONS[min(718,int(obs['step']))])
    orders=[list(order) for order in scheduled.get('market',[])]
    if _TASK_RESCUE:
        # Only overdue task input purchases may supplement the demonstrated queue.
        seat=int(obs['player']);stock=_project_stock(obs,[physical['farmer']]+physical['hands'])
        plans=_PLAN[int(obs['step'])//24]['tasks'];state=_STATE[seat];required={}
        for actor in range(min(len(plans),len(obs['farms'][seat]['hands'])+1)):
            pointer=state['pointers'][actor]
            if pointer>=len(plans[actor]):continue
            task=plans[actor][pointer];cmd=task['op']
            if task['hour']>int(obs['step'])%24 or cmd[0]!='PICKUP':continue
            item=cmd[1];q=int(cmd[2]) if len(cmd)>2 else 1
            required[item]=required.get(item,0)+q
        for item,q in required.items():
            planned=sum(int(o[2]) for o in orders if len(o)>=3 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL') and o[1]==item)
            missing=max(0,q-stock.get(item,0)-planned)
            if missing and len(orders)<10:
                orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,missing])
                _TASK_REPORT['late_input_requests']+=missing
    physical['market']=orders[:10]
    if int(obs['step'])>=718:
        projected=_project_stock(obs,[physical['farmer']]+physical['hands'])
        physical['market']=[['SELL',i,q] for i,q in projected.items() if q>0 and i in _ITEMS][:10]
    return physical

task_market_agent.telemetry=_TASK_REPORT
agent=task_market_agent
kaggle_submission_agent=task_market_agent
