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

_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqTaP5iafScOKJP=`FM3;%BatwrC6-GQwy+Qg$bbw3lC2A1L(qTsN|d<WJrxn>L{?vBrr`(LGE-gCU6mCXan5&s^_N$_{r-2q`Qxjf)Yq?m`=5XKk6-`x_kaGw$N%$J;q^cM=fmq)fBOE9|Mj>3>{owz^}ql3@t@^&{rI2${=Yx|udlxT^0R;W_Ul)#Uw!w*!<+Z7UZ;=$pTGTgy!uIc{px@I{QYnK@cr-p^y(-1udg>2fBx?6*ROtDknIKXrxj^&{&Dfo9v(jb^lANYK|EMcgay-H@Z;ru^Tor%$A88j7ss%@IvuY5>dj{ln~U@I;&|}KeO&y@k6*~EUp##E_LrY7IyQUhcW>T5ygOJTd^6$i-}dpR{qQq<`pJX6^yJf0JYMqQ^{+O5y3gLcd-$}bO25RXPx<M$Uw-xZufKlt&HHZ;S9W{l=U@K()4xCLe_#0Gr@iv@dk@l*X#UE{UV8dzSy~dzPpkIQ(@$&iuUwJG$9}rSr>79l?PqVlJ6sCv5&!(yla<3>d3;X`_e-|#v{>w=r$0xPme{vix0jxN+K~3XXl^LcUV6HrB>7e|_lHXE56ypX#VCD|*}6*k7thvxDgE+c<5hC<Tf}KEJ^d|${96Fuko4u6Ur@Gx7VZYf_7mUjmB&x~Anu)ilsnPf@sn7-NWXj%FHou-!ts~E-7AH^SF-)H75i@!R*HL*U0MZu>FG`=ZfEu`pY5fmpH`&W&n)ERvN5q`W3+d9>28V2E`NHreE8d{f1G97=2<4a{^7fNe406U0N#G})x&4+fBmzEckjRa>dSvW{K#NGugB*ZVE@uSFSDOl`3)smZ?Y`zC&PXRooqnCUU9MkMgH*OD24`I(P(=W_TyIe#~mv_?zHd3liv!tcaMLo#Ga>PVQb{mSJ?I|!tqQcaQS6_HKb>7@|9-#9bf3J_jI@Z^eZTDzRtf-_+El^4~C6b&^Pbjz4`8^5AWXnoBd@3<;xK3>0rL~y1f+Ks-pdAQfns4pC-3vl%iwO2eufI1KY`>MmIbL-?R{4Si#$n$;zjR&#t>6lROO>`M}cXnqGc}Gx`i46?RgSI^INChn(9I`z9{zi@4I&%;cMgk-xpma?=pmvI4!QYW<?;U8s|-NTuwEblH*k*F>|IeDUVpzdn2eykmjZBhs}rDkESYmfx{YxTJ+{C#VA`7A?iwBaL<^PdjE@_H?HljkBX@%JkW|(oLsMH^nA@$dCMKBHK$I?;eiBkyuwLWzyiQq&*Ku+BcAQJP{@Ti74?WqU1jj;lt`Zic|SjAJ}3svBhF$n|PJos2Z?9*-1NHori_jO}0-s((7hGvy#o%&AgQYG=eq5q<@sm7yo0qmO_Tbp4TYfVs7+nbnvq!$5}huOW>E{)&zO8$yWL6Y-f2dfM-WwfRz$Iz{<#IeAlPG@W;-~l(ffhipHK3I(x94?7<dksAK0;tvIdrz3}*<8g!i{&!Ch_v)XT|N7vTumj%>ti05xOXoY!SZYJ?(^Rjj}Z|oC3cas5TzQEU-fBdN9BBge|m)e&qwI5G6qrDfMJoUf;;$-{o{I(je@G4L2SD#m2<%NBfSN2u@%zM<d`Xur1rQ|6W5<2MSr?m3RFwy6pNS}MuHr>QqK$~9%-v^TSuEd|UlIN_I7SCFVJ!@tD;FNtL?YvT2$y;Vy>v_n>Yj8ci$H%@T5FYyt2$cGfw}N!KdYp9SE+5+h-|OBI*D&fK?K&$j0Rl>C;&>UB-WP$N#B2S#{7lYU4t*-o{W{A@s9gUfw7B!j2dTy$r25)HYS24<TslZ4Uh>>_mB}EtRbr0>g*_5f_DIm#6Tx6RVTgVKmAtQ&8E~0G*Htb#aHTiSPVbwOuYKcg9vi|Ad7GX8a{bP~(g{j*Cn)oWyk}oQYx-b*mMVY6ao<@<!{>CH#cb!VbG+o?!HQQUI4yir!jZiG_%n${K5cA$ffj4Iev37+)6zswOC!B4M|xWhw2e8?HfHUV=CHc+EkSK=kk2zW5bnzg_7jh`!L+$td-Hr+(a;8FwAZV>pHE9V`jN$6ufE0(mw4Vt+w0Xg(x)W@{K(_YcYD2hho^(vwL)Vj;itTW^@U_W$(@0*)*0Z1bBTBh{rv6QZypdmV}GP){OqmVc}|<_{wZdB{Gq~~Ic;i0iuO{qEs-p+kbYC<3$`Wlxyrb)a>q>R{gCw=CP^=b4BRkT+KTeh?m3kAyLgXgPBp&06y7+?+EHL1huNbaq)9h{zH5lZ0kCO^Wde8$BzwJjT0Pw3JTlhp^=jAk@J3A>A!U21db~QkQ4=R;-CnBJvgxP`sAvoGPE*{%cQPtE`^wUN4SHP<?+x%HhrM1sv81IgEbs2hG!G!}Yc9@wgRAZ))ggKui-Q){lAyF5#Z5l0odhF&5{!!{!N{Hjn`@xIy&gOX4gd!-?4`y-|7o8N{w+SNZSj|ANmlIiBi=E_=_lLk<YKl+-)r>$B$59~7Oh<HxR7qE#<rwt>h=NUM4b@qqsj4s?NPaY*q82NU;2k0fYy^%zsL);rxVjz0Y`cZ5(?1FlW8+g=4D}dg`o&zOU^l8+D*c->s^}G`eipl$z$amg_d`K{XF689L|2;Sn1~t`D>Z>ijyrjAgyKi&fIQ3D0imtT0lE8$mcbnJ0jkh-L6QK-E@0_wwrFZe6?ZU_6lv-2eo&lmdW(=_8hH}$oHL}5sESbC_Hu+oatFGc!jk5Pd3qrSLhfEi!<KlxlfRtrt&*YX0|D1gtomv8KEVhf{%0sA0s`dmJfZ7sV~UL#s<BU?ggeu_budu<a5!wxf+g%Z#X8t;Yc%3g2!0ZJxv;9znT2(CGoS9!VmcxJu^X66>#kk&eydWi(MO@d0Lm=%``$HMOI0cl1oh}yJfPbCQKJVeio*0N@trvx|Tqb#)E@2&iehM!|%TsQL`>51@4%ehy7&shNHu865VS_bgv~H3WJ1Mj1Wb5xKw>X<%65Ga$zgmOVvX1a7p8&1lvp1XXJ26=Y|^FOV!t7-b-gFA22d|z9?(GBjMa2_r_^D>|ATRI_iVG)YlX@tE%@k8;}?(_BA^nH!5{Sw^wUj(d`vlSM+d2^FDS(dC0}b?#9XX=!k7UC8fFRMe*zJ*opFR$>8E2wwJ1Bqr)ZB{Ip>&ReKnRD%;6Pg148dN8o(aa>L{>P|L(2*NF5{QEr(>wk<XJwv={Kp3D9Lp!p@Al(SZx?`4a*@^L%>rK7OX1f_J$(h|FLtoBlHqY1z!I_#z3MiVwRQE;OP@+K;8G>Qza&}z~q`DOwgbrkuiqsWRW92qc)&wxoDF-7Fjzv&V(%^M|0M_x%2`2KhB2yO%G+;qj9RS&)qX_;q!L|3dGq+vV;L<|7P4dB-yBqa#6lpq2tU`z@mYALL!Mb-j?*VuTu#Nf?IfgY@^Yaea|ZIFPHr%0W^hHZ3*OF9>Tvb|LO$qx@mowKrSFID%-d^~0O+heSbS$_C|o+7s4+`8DZh8DX-=rY_q<b!}|_yr{*H#&cZe_>PGjdCxd+3iO8u<(Kv77m(_!_pOZ1=D-N>Jw67%G*+8MOldzWo5RetZYr$)@sVm)|8VjDZ^q(8R?QT(<NnDEGa8rQg(ZZ!JDNR5VEJO@DiNt!A1<|^bR$?8{NDfQUPdo%44vXs@wA6aCUkp<Wc#wB6ZlNcS0VNPwR9)PwpPV^)S#8)yCV2>>4((aRk|A9j5ch&p@)h#K7QluG-39V&lg&!(Q_EuUc^LIz)%@%76w$x^cY-u)Jt^O|()j(Mq}GddovfyG|?ZhU{y|&~XNm{qhofev}EIRUSXP!H;r@{IHehvB*Aj?XRkCWQ@FNCcd(aJn%r_#Uk!58b}sBm1Tz>45$%Tr4{C&v)e1tnsoSU(!tlH!(WpQUbWfTiMFFhtEsUPB7(g3P%1N$NN6ZkvCb(kx*U?|k`7FF(BPvdiXrW33knWMza!lw?wCQmU$LXE7fYYYo)a|%b(Fimm7jTSt4EI?XHnjIu8i-nQu&_;jF2q>vG^KA1jLP&01s9IEGs7~<eb`Gp*g2cXL`x9PW=F6-<<2o;u-13PS-t&7G_QdokR=GuYrj{z?=@wID?0K#a0(VCj?BG)a^GA)JBG0URq+qilXb$k5G3@W=LE~yuB1ov`OBdIHQNa?IMf(i4&hxnS4o=drFYA-IrRwk@}hmaV+-E!eU=5EtYzY>Ks6R{`gS{oGbGA5y6um!3zYG4obU3Em&51tcC8eR@(7AXvgy+TrmN@fUTR4_XKD&sYv!_D=0OAOg59}r6k&z;$cg4o=Y|DB}DHs`+Jv;skrh^1t8KpY$(y*wx9_h=7wmzwSkXVlNlF|9p6Lw&KKG78*4<W8>(EJz+X1kt3PZx*nye@%)Y%|y)h1#bS$VR+UwQFxE$35fi#*FZGzp;8fWvkF37a9w9v}Z$^wStpz&mLt(A=+jUT^BB8_R%+?SD-lPdM)I4f@8@qJWmthh#^K?IdjfgmfjQ)HFe^3jyf(T&=@1LPhX6LRQB6@HesVS|1D_7`v7zeP6Y%5Kbk<Kvi(xhrM1xG~rLV33b~iE;seWMOo^3fu%y63;ayu_WDS>fIb^Pg|x1$YoK0T<!Hnm@cGR9<*wCuBnz~i(2J4C}nf0`qnE)HFhPX!O9S^(KE!sJJA9!Rp5C|vaYxDRDi*1D8lN{Ro==nJKrnpc&`Er_?fUg931Ry5Ewt=d+oMkO2bBPuh6j3!V0)642iGg$uBJds^~E=NQYfen_f=lx)GV{ZelS5*=Wex5wh)dgse!FD0U1g+cBspgye9^SSl<lN+KyByQ|nPTL_tlOuNh4u=}Yd`-Y<neAKF!#ZPn~P1rY(X6`t^(zLnH!5QgbJ)R%dad$@U;*1=g!;_29Q9Mqe;&%!ameV#pokFbAj%=l!*h)LIrE+CU<+fHTceYZVbfFv;3+2cc%9%DB$n=z<zDYapG#IvBz|?j?E(7@>T9wD6Za*Fcm`N0NBvIEU5{;fM3_bxO@Np}Nw^{+dsjb`Zs`jT#K{t!-Oy&6_z^q;Ptg#olB=PCtNp<!ndl4zvOgvRF1KNnrqg)0rp$t0;9V$r6flTt1HpzG1Bp-MOIv>s~?_0s+_Y8i&XIR<rZrHrpATtBh3@kLSyV2;8L8C`J0FiVS3dlL91p_^1arEH8(}SaoDX-AI2I-HAG^NHAPt9Jg?U08nutxW^m#g<Jq>zfj_ZayG{^1h%j*5ObV<g~=WEVKG^o_#OH|m;!ps~7eI^lCJIuwEp8U>HY+Kd(ej2gYFYf(uLXTn=&>&O$B&SjJ@Yb@L676ljSq~Ay<{jM5$0v#n698q%MH3D`K<9!h!>&CLPJkeQal~%iSdxfq#qyp6@pQjdRIgVWWHq?L1<+c_65*>LR-Ckng9=S-7$;*0z=2!RX8lD1$8iKJRdwg5-fp$Bt4VqOb+=H;DjEcZS$!OalLn2u_R3U$XLs3O@KxE}n#hx%oO^qo~E)t^(3i^-(PGt``S398ux;zVXc@~z-v&y%4wCA<ki|A~r%F|(!r;Cj~6o_CytqArrD>&Ip($ZN=KxZuhiohh&0+X~TFv%W)N#Vz&ou0+UNe@osv10O!75UzJ13^JlYHFb|eU(*hbXK)7)<heV*K7bX52AGHUTS0J9S4~YJay<pl4pjn1<O2@CnuhkDK*TJFJ7D0Y860onOVu@Q)Nl2{#()Wn^?MfF{CK_A)j1`gv28f9Pp*=Y3}k3eSj;2Qkmk~;X3L{atEsu$h_RTy%G;m%C`Q))KpzM&c~s2kEo{V7?+Mx#CY*}Uej%R{G^RW=}cau7d^!G<R`Z0v&abH*olN5fjMIP;4cwC7@1SO<$NBNqF%JZwb*N<a;?(3pSGJO=WvN(R^MJETI3RcjhWXCReK3B!JhsJ_T=>*6CF$d(k5+s-AEBo2hHY?3x4pLn#?;TEA4cQT~h8iV%m8_f71Gq)m|gqpN$^Db{YmS?G*;ZB~!t<k;fIJ9YF%!(>Lz^ab<_cmHVi&3TFO5yt#GFo7-4#?qI#Sa}in{Jf!SsWAlj9cj6triLsnu@f4l58=szacFZA(WOSVZ79BKL)T7FO9?^AMx6<In{F639JgVtw-Ntsx0J4b&b`wqPCYska(ZX(`jon21+9o>ee&5!e75Fw`<UL8*?ksLyT;)@#9h>fO0CEwwJtQ2*u=w$wPkkR!?>(d*JXL4la*x7b;3PccSi?hFz$J)+kgrccKvi{x)yFkf9@p2@aRA>;AIw3BvPhE`(js{QK%5zm<+fg!04ZoPV?e1*ffOn~?ymceyYmZVFDS0($WsL5S4qU$ffx~?U*+Vo4_+-}k_kk2T3Fp_V|AyUwFOPu6%-a-LD7S$c8s&DJ^nQ}R*b^79`uP(*dj8Wb~JgqM`i&*s=5QCHQW@f$#cE}9}trq0Ws1x3k1Z-GwRIl&;uoT9Pgcj1|&=xr#yMfmt(XVff=NOm5_N>LbaE`lhuF>j5~jggNG#q2hTxv6Az9Xj$LAwc@7PdEI@dLO7jsqJ<6T@Bv&YtHH&!XN#hQ)V3MbA7)S_=r!DS`&PwYw8!guyj?};DkK78po;1?nFgeRMu%%n#C56!=DGYoEHhZ*wywJ7MW6SP{6&vpK;K`3w122h9j&K}V-AYzq*d<o`-U0$icO2tZl02lDG=lBxAk=PSLG3o!nk@3(lc@e#-CjhR8?{TEv|2~5cgot9rS(+u^-b~toYz23+qCGk%^t`|;i2=*USizA+obxfKFOp3_m6hBBV|Fbl?8^b;L)GPXPd3q*009pN-R|<u~ea_@i0~Pw5^e5JSd##XW>L1hLd<04o2a+iqk#co$j|GBDf3-d!mOdkddp+exCDCzc`fcvJjxNLV&R*1bD(j{lxRUl0Imc-7l4G(aM;iB;M%Y`BGt}+->QXwxw&ixtR}9t8|-tSNT<jJ+?fP_B?&JMYFgSI~Mp8VB}-Rvb}^joJRg|>YB%gwZ^VNuzz{h?@kMm1|I@5_z;-RySE$f-qx^7ybf#UG?(*78f4lGtxODu1A9IF)N4n0a^y#v*@KlYZmhiAu~_n0?hw`-9N<}b!r%N8{^pUAvSw|?;w%(Pid?4Ca+%4y{3CCn&pdOh@&lR9=dn4`I>ZK-Vr43}`3a>5Wm`wU6Pft*r)jS+OypcXmBR~`cvDxgml)YeOHu+oOKkYF#Q3<g6lhI_%;>uN+n=Dn-6ecZsJ3uP_8j^9HmWDH^Lg9Z#JNf*&Q&nw5Oc$esKLN90|UQl7B+AW6Nq(QAU5qK<_VvOuzYk29!;(jl4T&c;_qn&%V`E1f894<JUo2-XS9WtiB~!%-llT6=%?R)`PJvY{`$=~@4tOV@<2b{ou55y{dp0PwVn)806FW)AO(=Kn$QYNWIESMmB^MVnJrbyTB%amQl+z{%2+E^rVpwUdG%-FK@DX$9E3$SojVpd5uIH>A+AGR^Nrp7NUo!UmhB}bmUp|$y|t|H&GE{&;JXLdI{d&^o++CGJ&PcfA&=j!=gBq@%76l;B5YRy)m{s6ABrfZ=&W92(sGTkDA$M{21D90+n}T8DlUGZ@t4@8M5)dvN`c+>VhKVHezU({hM@{kcg0E{>zjS7-}szCHv^{K3^3~_sD}`f-9#YXCk^#vZSxq+@jZlbkl!eTcLp;(N9om|CI{rRgcZcKbY&xWV9*w(xuf_b^GD{up8yucCxkPCZcIf_c*b?94jm59fJh6&L4ufW5`@fkC~QSP8Iml9XLw<$1CdvHN1xK0SIS`HeP~$kfY%2PUq9k}ebh+lPzS^{xCNYNJb21L=R>&7TD4h9k*04GyzZ>q;x;Q_2$RGGTi-@>G8)es>kR)Dqnb6FYDNH-2kvj#X{>&J(_mgJH_soH8)?sBJfG*VcnrLiH!5~dzV7hn>rOgf7ZCt%ozC{v@gY9K#M%POPR7HI`Ed~+;h=qlf%Xx`MIT}Ez=$&sBj%Axk~^iLB?1ozPOOhGvp&MI<|C~3a=91Y?2P))zx=rwPjvY23w`iuuau|Z0az^e`=fNz2!EvHv}*QW8H>GC{xhq+_+)cv_KK6uq1#{O$!7q+-0^3eHl5i4O{Q&=&5;@fm@|bRc|dtn+rRNdoTT#pzr8}+{}Gq4%()gnqpbOaV|5V2<siDoo+&k?LbR6{J&e4go(w6Bo@&a9tY&Jgn5hE`_>>h*(-dr7BoX6#dEOpj%}nTQ=Ng*frVS&q-915D;aywP?T!YXOfJHV>I#J=Hda*>J1Z-SgFQgW&PwSs&LsaxAo>+da0FgeLUqxh=*R8qV%TdTIY*-997+L`=mG{P0P*GyMu%$lOP{9xwLN*d@l0_V5Do{a`ZIeJ0Zuz`9}_t&i9BW~NdajeLA{!5#6X!bmRK~C@C{Bh#u8-fpDFeuu`T$-w%`NXLl0~Z9qw;CNF!-iY)BG%E7e{g4m%sKEa|+m#049PJbGFYi6^?Ety-m7Z5bL`(JIwxa$t~T-CE=o$_+P*Ek|fHUdXe;^H6jRVheYW8S{mQ5M*9vka-9}+7&_|w}d9!5>oUJ@~o?C&qKA<@RxZ~@%nmO0&47#V2ZQ+1ZMcu&zq$R?RshsCVzJ``3HS{qPzC?JHj&gP?p1kp9l;#PFRb3s_AbBbcf!WsGymbCd-)-4sUK0YtL*ipc5l*I<79@3XWYd48>8uN^h&O2IOn@a=e>cc(ZLn5Sr46S_5^8IMBwXKUWkeRuGqx+^Kpwf(x`AEIauI>*RaV<mJxyWjn6>T+BG@{IQ@Dlj56;Z;?kQl_s4{2Z>F_D%s492vOVw`AxDHYgO|03av`U@CeOb0y~`&>lDE*5x~;{1qeWydqgY04V{HJL1mFTPZi20D>(+M<d|zpjtD@ZOatwb$fB%~2tl<(^0cG3;Dx7M_LTT*%ukkgk`Wjd0xW53J+;ni+hvyzs|%OK88Nfs40#xtJ*M)(Q@kCl5yb=fQd4N;&R}C3gMF<pI2=MzUSu0-jY?Y7sAOBCVp``Gr7fKwk#uyxM#0e&&u`a)&+dAd6+O(;h%_r6gQ*4!Xtq#=w$^9fTCaM6WxUCfFeYPJO^7$Ou+p2xN^d%AE}gWuG^~w3pajjuJWS%%5cpSvqC-RyCLVVqravwsEK4P~1ese8mpHM%=LPYw!oXt-9Q=X8hyT!OiPKZVjw+y=WR++fkYq10oWa|RM8#j(ja3rYL_|b1@UZ`^xm$Ef@<gY=3JKb6&0D%VJ^7rxa5>pajQe(b5u_F<D`xnLCO1Lj+>~TzZY0xm3amKYUc;s76fmganWyPQPc)8`i5CSG&9E1c!8nQ<JB3|^)%SQ2i`AKVHdEyxOWj^VfT;s_idaO6F3MOMGRZ>}AC*;nbXM>&*7P3JLv9YNg;DOrHrij<mi&du5T)?Rn+}SeEJ_(3QOdPds@R!ydxbt1*j@wSM=?#S3!a<pMaOUBVlRLqNimNYA1a2p{awj+mzGG~e3*-(Q;M`s3D81$dYH+G#i%>Vqu^3vd(rV@Hthva?E%HxoG+aWnG#%)CX?7`vcyG`Wmcw?S(#E^lqn^&LAvchAe2oG>w?Q@n|ZW)h98X0qn#eS2laecKr5M5GZj|NRM*m*8ml!Ltkh_(4Mn8sfudAOv{EVaE{!U+_2@ybrc#QIv$1AXuIyy^3F(wn(?w;qO`X*?jWuo46V@qZ<E-2HbfaNUI805%j)RfAc8J#w^~DW-&>Q@qH~8T~gfEJSiYL^g_?1UxMR`PMVDC7dMI2Azlj1c&Pxj#Eiyt??pXNyR`D^I2OM!BvgTh=SX+#e*Cpn;&(L=SAv)&Ri8{A$%W`}lO&)=D}Az;9z71v_{<bxKh@}n_nzL4zUrLjEOlm0V#)t-Z~qcUNOt$*`q=8hhOZvXoT+yzqSO$Re5(k&4gA3HqJ3mH^Y@(#tk<{#uueZyXXPNE9n&qKh|;3z7uL8oCFU`GC|%3ou%$2=#cgg9Axfi#}VD?=-vVi$obGV!LS%tLppO>6k)1%534-@SzrnH)TcVSXGk!-snsH!fE}MbwQ|y9`$CG8gG4&qTQbp4XC^i{9-;Bu+c6*%e(lZCE1+q2TIn*v+Eq?UTJod<kdTcn}NC?VEgzeU>Z9-4r4EK>;Z*>YA<t;5u%#+5?S)l=BuNPqPcWwm9;6B7rAlIDyS~_RO6<vom|9Fv+`E`cURA1=ZFeQJFvv9wn@JLLU1&bmj>|XOu}_p(lOSHsBNC(2Kr(H~}O15-^^#oa2t2xsseisn#2jFZ+)hF^UJlmm#%KZruWi*(R-J3pbkhY)ZT_Z>$(qM2`lCy6Z-JktFg?yv{G*VJ<Hj=2ASVO3fp>bKqPeYCA{saicq5FD3pGUpUI8>4op)sVP^+xkO&r(u`wm<4wzA@gF(B-S$#Kb+?3_$soOBdj(3i&vvJumk1AAh_dxlJHo3HkJBl9cva(3HRHO%nniMqLNm!U2d2@inL+bxVvvS5y8J!!!mL71MdUn>!RL7lepIGR7>XkhtGWZR8a)B&wEJ#)DEz@s;g7rd0~3!hk37O$C(}%O(UE>mc8!zoTFj&VvWPKi?x$Sp1-{e^eEXm=oPG>x(;RVyGNC5$^<nVWhv8gg@;jgA#qnvZ&?JY9Cb&pADbX4qxg=dwZf1u9BzcV1+skpar%MD9JtC0APMxDCA{<Fwto$W5n?qpU`w+fBmYt+K*yhE7Z7QRp*e(#w+j6__25{mLFV*QZ;z-;S5pmQ0(x&qRXO;q?W#Lg{g-3l&cr@q-C(sX0Tzqhnj|k-m%&WX&sh<fVMS@V12ZS2e6jCpjmIJ-^5E<5ZN>N-eqoLYHS>lz|(OVm%v*wqX%XR17TrHQYdDyO+AFbP-vaQ-KEaw#8c{h9UZrWNRyhmu;umRGxBZ<&sHIzyW&7G1sM;l)Khr(Wvn?-kG%`&kjv-78A;4zf4fn6fcnU387nvTOyns!hz!&=)#J}0Ogjcm(^j%Ip5Sd;LbR9djKTgKJkMNuyB#t;GD$zCAcN}2zg3h#*kk`oE&*|p*p>B(HWxN=KTkCeRv!xT}}v{%66vaCZLJ(Qx%>#wT4<ndqBXf^|af-vKBchg`gfLlJcsyTwSx;s~E(APJgZpQ7v72<d>ZsUQGfDpn=(@f7gX{>+>91Lm{Jx2RtFFLL&0O6PP{%yNy##D#CJdzEVX6z1k!qfs7a4FiPPeKT*0YVG!VriaG;_eP5MnaI`8o;H(UQ{JI#-5O<QFy&%V`Sif85B>1WA#TkHvSU3trP$UA@wc;yu1uhQS?Px(U%q#eVK=1Ra(s_=OA}a4s!qC%ywtEUAK{p^c)yGi4%dzT9zj)Mv07R5aVWb+LW<tV&09jaO4SCWi=IT&Akh-a31Y_V=qucce&9)lQ7btI2VFP;Ym+kH57qLNz@D`R@L)TH70im&y_SL$&=EdkbCazo!!_wtD!-9Gq>9C7=mA>FlXdAy2$d&oOu~{vd!}++td{VI}AMNXzN%<y@O{`LS6^j?KDVD1yvWk@=X}=DFdMC$utZ8OtZ+3sFF=rp@w0R9fr*{SFkbsy{478fw&|d=+7fEs=dO4r`fnQ292hfykH^POJKNr=D{?&Zlm%5oKACQWXJJX(=zLxmhIA1@w5oFEP8W8{F^GR=+HD8;@?O#8wIix`J4kuh+G*7Jw~&c&naLkfx8&Y6(6*~K`25SY6(Zf2#f7cC0^JajirZ#pt6A}^Dk^5@J&8oW&VYI1zt^}@r23*bT~pgCl4BoJmV(w+?mQFWB{?1F@f7&M22n-bULy9MVQEs`<(iYt9hZJRF{mizpm~r!Q@&v>uAuRzsaW`W>5NI@uweFUX15(n~ojzXLnkSs_o5dL`Vm8$@FzDvXj!DQ9l64!WGvA`A45}($|Z};m8uANh^rLqJjueAQ|1e2<v0Z6Ab%OEDom+^PNj0E<hOuhyrG?0+_ibACG`W2lmG{+(eExp{l*;*fZ1Y1yYUI`TT@I-|o;6TYsz&T}k2tp|U;oX^0LGImh3FqR)CJZ~V}x__(vxI4LKdLL$Zp-$6KQAe>H<Y`P;dva%zm8&81TSwWTW02>5gQ`yv)puRo<ha&{A$!iL#%O!)+LMRv3TOBNAdl-eFXR2Mf)xA8B>Ie%Mdma5f)Bg9RdoIv3Ik_Z{o|0VnlaTN)sDp}40Gq99g$He2{F?w4CZt2eWVZnI`Eg?{pAA+sp(g~6@ftS+tN~vex{&M2xSGpkj0NqhmgiO#mK{QZq(T!8o4o?X+9;AQNsgsOekD7P4AlRrvPt<UH(33j(nyH%;1cD|@nf4p&k&m<%&fb^%yye`YBQziNi$3SG_%ZKVzGyZnxin%n$6RO!Y%S+U<WIl9K+)#5j3dDbi;6+dAAv+9#PZ%5jBIq#K{NLMcxvwKs~RSXFLdn2ZXGgybCTm!r^0bhr`Q+x5RQdhk8B%GL4VVC*58^QaBy?$=!$2Tv82I#7T%)u*;eS`;P2CC$hid0+~zet|CYI-%)#&J}gAn@u)*RY&6=yD~N_%0j+bU;aYM}D)75-6aS`eFCcf}#`_V~G}IK=6IyOVLv<%LAqJteB7h9OM6bXndIg@l6w&$wOt!woplWa~_`EnzV+rX2QJTggrD^ymP4v`TrEg1lF93c!Hk!XJN5!nEnC{f2Cqi9%S~eph*(>oJO?^-U_=ObQ_4Wej&9i7SdhswRS#cX_=A3*;$xHmH>T_0CkFz@YXWO)fY7mLW`)H`11BFWN-b}iA6Be5{kyj>FS8yVdx444_DmWO*2tkTW$BQ1#l?ppeYkbx7OcOfnF@-ZyCeNP=yo@w?LbLL1Kvre3?-|uZeDqbPlX4H&9MxLQ{`ZCFv(tYM&z_PsOC4>!ZZDF~fr-Dwyh<-cVm~9T-O}`@ODS8MRq?_4zt=5BrOOJM>XM+z8pcAxsmU{`BG07C_7Vax)l^T*@TKZbTBUXxk^AXZRJ0h?5l-6N*`%G;iVW7oFZ*gUG(P0@U~>A5m{(9~w{cr^8+ThjW!{C5>`D&NT0~2AI;?dpg|(uXC?rQU@Hwiy=SNbpPmknd>NF<V_!RauKHZs5x5Rw96eIL-kz%0UhKiauE5;(7G>a6Gu*1dU6BmqD(ov!5U!uJPrrbs#nlJO0$R{hzv#E3P8bdVFg;-=|zIw!7^hfL^{t`2fD*?bL##?rK5k!7iBC0G#Mwu3RpRD+0ppi1mHp(k(BS+$^=A;Pr{Y0d4CR8tn#T_^P`Iz)ZaVHL)kvP;a&p)E=nRHTFqQyM`D~LETH9l;o`I*qo!-Rec^q<O}=qh`nyKzB%rqgCKoi>}#m^Rxy9%vvm1CqRCzvLzFEqO_IT9E09UKLVmv)Js3D=PlDqRL-lqsxl8rV4r%I3Y(-9M(*%@aZ-HJ>>n|uP&i{;!n51V1@GN-#9(!-{438MjrjEDD1_rJ=08`N_&wy?ev)*^HT78ksP5Ki3j%-nv3IO{d70F2f+mG5)vow>In`I<OO?$c1<=1Prtiy`h&i{$tw_(y@UY8H9shh7D;+&EYCGrZ9vWP?G^fXd0UgS^%9M{A%Lo?_R6%BCsscBt@BzQUNMy7b4q<vYplN4oTtD6TH9+NWdwAAF|xMSm|0(|%nk~yU$lTmwRn@$-=ppc5J}A;sUjE}ybWJ95kVLbHS?<e=82T<?nr4Q!rBpxYR>cW%`ktu&ivss8V9XKk_GpP7u-*P`BV5ytTs}Im`pfGJOj<_0Fw!^nS{#@&{hsBiiW(~G*inn0x?i!-_&Hcx}=J<imikqT(8lS|2)`jj>3lCN|M>53#9>ubxp`TT#<URIv}$pT;yqvk*~-io`t%-2+Bgm#4uuOGJJ5Sl07x)&C@69R4h^u@o$f{LCy3eCILiuQ{IDt;0sUCYW5Pi_qql7`uO#~d;1=VO$xkDBYs#4;C_)D9@RtKSwrch!(+nQ2?hzDF`-r%8mHRLGT4sh=&)&4G^N9KXYkw^Ji9Y^BIDe|ME%{x-IN<IH1WZ}QOL)bzGhaw$Cs@Mk~H-lBrr{j^tkMy#}%88V=_@NGBw|BO2GlMmK#oF;xl%McUaJqh6PpD+!b&}BA4mb_)8Q=3k8Xl+E&X!=&kLgVD^9!_aNsFc!X35Y_nY_+f6Y63`a8Y^ydr*-lY)j=?gjIPzE=#t|E-KkwW^kpC24#dT`L_5rD(i96b|&WWyfK6YWw!S>!{bqUswMyt_NtOH3@=6Ndw-N32Tgkh+~j#!SkV=vIW5zyYahDC!kVii?9!u8s~#nignv&sST{SGxqnsL&9iLPLo7L^af_tkr-^Fd<aVQud=p4kAVkLj(oBdIH!=XP`#jxjk3q_9Xs|mDJY{078e{ZcENkUo7Z#g_U@69R$alwv57*jAQDH#5>7~$4ORsIK}WJkxq9KX$m|NFVct#`Nel_Kv1Gfs<H+qDF$UE@>1<&Q$~o~Aq`Gac?3$gmk_EYRl>1HfY8gp_ms7>OJV6hWrhBuG}$56Xjo*8#<Os^%mhY^{nI>9vf+o4Iaou%KKvP8&O4w8RV{T^wKP}-5+o=(egNaS2EeqINKXQ5{v@!@%bkX8^dmZ0cc_tepziE}daR90o-ouX8)J}0bAyohFVF~~CWbKqV5c(KizR^FaY(lM2-c<sSD+1oL;{uG(~}2AoM9kXhUO}}X_`@DA#{m_(4|!fU8VQyO7GWoalfv7Ytx7%mL)C;JxD|SF|Epv&^&kBr=jN?ZLg8u42`yhblN@v7%m7hQS_6EB0FhOvK||q_1O1|^8z_=(UlG<izBNx&j3g*N3u3RxFFrMl~zf3vVg{J;YJmo&ulL`)&m0K4bd;vcmRz{^Dt=u&1oPK;B`q^Ixn7Eu@mjGRXt}kS`s4aZ<ajgFt$o_f>(#wO7?gRKAzJ7owd*!ykB3oYdpU|ugK%)qdMUOhMeM-miTMTJe{*WM_>@npi<yJ!_Jj4K?D%F4+)onc|l8g!w&ZujQr_*3kV4gj=a-N=>T0*&ee2bMx$B!eK#@J;E6=TLnIo0BGK>=iNtBipzU&^#k=8WlCmdSs6+2&Flm@b4nBR4-J^qH&#`tChkVU_Katw9!YA>~XBa3sXkO#w^*NCj+BmX?sz+$kTsc_?RR~6%2i|BGeMq2)$ayx!JQ<v=B4sat&T>d{P&Yz%L9r&!#Nu^@@;QZ0uZy1ax(IZGWe67>U$@hEreJIw1T>XdKSyKj9GwMC$q=VZs!Y&cu*}|1xMmA;nDPa<jL=U)GElS^khFlV41Y3$f4Zx+Ubb3mF>nZciY5~QkHvO}UGW)rVANHCQ4M-hAO%)jRA42KDJs+9%)(buJ-jn>?qkxG403Sa3mZ_h;mVZ0l7VsqkYo>Ome@TTN7nYw1kiJ?+DF$Kirdr`{1l?FT98yThd0c4e{C;PM%3F2un{%pUhBR{v&o;p13hfomy8ogR*llQ0UTUtc1T`p4;h;g<Xs<&-t}a!Cj?$sfYm5dux_u=)i2v?q$hatV>-t$5C{(;I5z=xTVON9zFP)J@C*cle;^oq1Hs#m3{ye7-QiZ5w1!7gZe<VtC<D5GByt%<CuJYsG<*1_w-eHZ6?U3~G1yCBIZQ%YxQV|;U>rmFIRmSrNjM*Vw{Z+53=f_F+3SiV3auAMjVav~`!sp}P2hzY$zDRJEDA(pf^-jj3V1;BUL9R5l-}KJ_=`1ihLAD*J4&kk;u@@w5UEalevD~o=ej{}r(v+NZv^^Owl)k-F2+cwB@Dbw0!hMzU+WIkf=U;-Rr1?KCS;Dd!|I{zfN?#|mDV%)u%5sN;UrI3Pv*^4{Hre_^QE(K0P=oQBE9tDhbo;uWlbL87VWx$@Qrj|)JNxgD~-?WXgCfS=oFEO9oq=tNV7IX8c1>>EEBuOTq=jvN=9vbGHR#o=(2!0qJ26{bdu!qf48w08e+-QeAhfhL~vz9S@+O<N1k*=o`V>8Zd~wi;{pydJdB9W<nXC!bxxsmV$Bhi(CG+=>4=z+YbmjQ&Woy|?u((Dl8_;3HAr5gNfdfk)9e-cPYnq{B2RUS6u;u62UKWAMqP|k8@Clb<}g+__`XC2MT<b6&U@h_O&*9@5(=S;rb8offv_RlA{G5C0trq!tv8wW3S<9;`WJ1@HW252?%rz;uM+JXPsBk1vpR%ZLiV0>prodg%VMF(kCWP3kE?scZfg+=9XtYT>!A%z5HzJJ^pvKaCp^JrOl>RGn32oVXtOD=T#cR(COI<JF{iOIuf}fV#*Ak9oX%;2J*U~6(ggYpuL|xOJ((B|GV|o63DF~;*iAhM&+x;3EpDaPQXI)imF~}U2a{&-zQO46Hm23d*7gfkmuT{$jPtyNRgY1pDbmvekq*)UNc;gjQ!|;BmmMeNHMNEEPRtHML~-~zI<Jrj_7WKMP(TaF_6p<2%}Xa@&E;bs)$tBQ2RB&cd_UK`X^4{x9?!vMF3+qpwnZi^f1^z4Mo~_y)e%Y5=wZZgV9_S;goz$|&yH`^%aCo`5}sDCUa-MobY$Ek2q=)uJ@8zvwQ5uu#5V`QjQ2%&Y!ULwlLp199+_D7+n_oKi3DRHY0b^)O~Vt8(thpaLZ37=|4y)l9A~VBR0Z6g2ggjK%(4SzmS`SXf=x773nn_kGh$k<IY0dM!~X-(^K%3')))

_TASK_ACTIONS=json.loads(zlib.decompress(base64.b85decode('c-qxnU2j`ia{MoT*274Y{E;`WhdX1eXJpuNh|NG443G^11e=FR-h%x1Xh#%zdAqu*y3e8PJej5>@}93g-PP6Azx>aOfBWtCzyIy`7ytCji;r(Ve|~X)@#5cq`_F&<uZK4tUjF^J-~Z!p|NZd#mlr?2|FnJhsrTYfU;g^*+n?Y6^!CGxix=;1cP}n3!`q*K+-^TEe(>?r?e|~a-97wd_v7~M!@qCt@BjB=`GB8qzuf(}e8S^f4^RL8-Cw?ZTz&4(x1ZKOK0ZzSi{*${-+lPy{li_IJjU^Rj<0sx&v)>x(|P^8{qW)Vv6t&HfB)(B<LQvW=N@1E>C5{M-~alsl6PPBOA)`bIkJx*-oD$W^Lt!~)gzQf`}BE>2YB~(Kaj(VIL7$S{)5P{!B?TteE<H3)79Mn=yX_UzpuXU&)e<yr(YMJ8f?<V2H(&B@n>i|{o_eK|KqDJUi`HEaQicO5^#*3Mj5~3`2E@ZmlinA!oyeoe0O--lP@~F*uFj8^872C_D9SburJF)`Sx!6DYrv~H&3U-8tMMYvpL^yU16@6fn034$8nbTTzrPO?)0gaW3KE1wW`6W!9_is{`i6}7+Rf+=7gPC;?>k;W`AJCfPIYLyV&-@a_o<K+f1#$4K570ZVy)D=>r~Te%{LLzZ_l3V20w(5eu?-9Aiz6_L=Qgcw)ToWE(Mzdq36AJ15VQt^LzqV~_9AUp*Q5`c-Shae?F6JB|yPEi~WF#Y7(ue3117u6%hoZ-*D_pOFuKcl+VP_TAmDf8Kt&d;j76znspL8!~`dkB;udiOuXcyh0X3do&6n&<TOd)qQEwlAot<(-1>DzQFw>*P9i^$fc|eFnPQ4C_K11?)!s>iN54;79Xz`Z_{`?BU;zPlN=ujn76_dM3;NNK8qJHeqG%swO9&FeDdb{Vss<s<&1Cq8IRMEdz)A3V|DHs$GO-$FN>#Jxlwq+*hMdQ+`(a@E0H>XrSCePxWl-PUjcUf<6G6){e1W7?e0(8PoMre<klS?F}ReAFR-1w0@T4)IE|agckL(EyIb9bXnjX?pW@ufuc8hbI;6*47d$MzwJP4lYP#SH<A{O?BYtw6%Jk~!!eD4FO|Ps1-4<V!+}`Ny$`_NoUjRtB(0RDUE{DA3EC4)s<HBjWbe%=<ePgZ?GMHVz*>`QCyRa}J%57#lDO~giXRPQIAH7rX3lp5SgE2`5ZmhC&3|7`Z@qZhR=;0ENUN5~2v`vmU_3;8<n@it=6={Tc%^p1i55e_a6y_4qIBAj>ntnz1K8qOP@tJ>o`{|$KZZ2U%X&P$z@ndKl^RglYOK$S6`vE31_*r}g!^(rHSxwkU60C~pT9~E>>(wz_ZTHyBu54k~CFTGEnbN}3$5T6KT`9Wjdu$^fVG~zkZs5jp0}CNXzD*M>b{r)^=fTGxqT?goHH8OCw}9ag$4zzc3y#-B&7&enTfC%~8-jT_o<kL96`1G4<-N46YK-Rh3xqrFl$hL?Mvfxa(Gneo+rTc8EeGJM!#Ez-x&(^@7q`ZFSguJ0TaL@IhU5Imt?aPIr-%-;wj;r{g~yJ<799W+J18}-7o0{2T{cJoYiKe@ubbnh9!tmb=g0+x+E<^wcEGWx5?y|{nkqqk;%n1L*4rIDpb@_6eK=TG6#E0$x0Koj%z!7iYyEX4lP%`NN3y{cJrUv?^zA5+*LLpClW8Ux*I>dC1aQ!=Vor{9G3#DXoY;t$<b<7?(;N{DFu6qsw(iBHsgL^P0q^cOdnC^6cy~{e2k-FpjE-d=eLi<`gV&=U&pqVS2y5!+!M_pxlW=##NFZBtxN|B9UC~R!E=S1ZVb^WeLr7P#1GqDs0L-xspwY2`U^jkM9s|_SW4vOBmK=Z6IFtp`K^VE|N($Q|Z71~;k!h&p03ztO4tjfFC<Dm>hB%m+KTL5z5ew&Ny`irAby(k|g9*lW2KN%6OvAT`@`<8{H|~eA`!N=pET^=AB*yeeTt1B#HJnXCb&GHq^)JhO+dS7u+{$0>$M8t%S8CV{%s8k<2~M4L2Wc-AEJQk1j+{`pGdZsZ6MdM3H5s8bOoxV$4!nwhwD=pPGza+7lzukxu13JoG-sNP3E)&+KZjxE6isURlrb%2rtw<EIXP-L>CgxOm+gZRzruk(x$P-c#rWCau*BWc`PJthPmx7e-{fx|TvC=AE_!+3`ja@DSt!q)P&ild%Cd-hB8yY2JYrt_;?y55v11ZZTzk~5Aff`dw-5ikd|J{6+xY#9N~S;N<ql(@*1uI{b&^Z`;r90Pwg|07hY~Tr@Jt_8Zu!N)k(ami93YuoN2{#1y4nGq(%vsUoGF7b!xnnX*1fw8lkDB*q_TKu8-eIYEjrviPbtFXdz_O+8NfrC<c&TnAk_y}gjS0<Tg*K6-CgD#ij%T+^f7QjhuJ`2rB`P_jmkLTHEoPJb~fUo>LAD!K-bD@vg}0DIm{U;@F7K8>um;Rrm%{m)+|1HAu}+v|3<HKHtE2Sf%Ah>djk*aWAomLUpV;@O$Nh>35mJ62S&Hx=UZmEwz{6JK$!PWIzcq@gR!VvG?E{!Ls8P=PzSd7+;QNK_G6NaMzs3qxu_=+qjOS}&u4hkV_Y#N6ZmyU8f6TB(}^c3mQqF*``UodrHvsXcUTvKl+i-fScHiEFYwAXTLplgz3*Z@9JQC}HiEE}dCqys=uIDmU&!3yUjTFh67Cd=NF$;G5j?XRVrIdu<LARdQOzBifr!M3JI2p>es4I4gF`=z82%JRZ7Xxqs1IF-Zn|ikWL%F57l_#cvTnoF$pML+SR=s-JBNzsU_cx3TcjLXU>p;;kJT1W8Y6Lg835hk4gtp+?Ke8ajFhSOzn8>J?{~_+s03Ust%DRTrQrv!M{z1v!I_}(9-=8saXB&PgwPV!ztybnx1{*yF;jWEbF1UCW@RwR78fQmW>_hb0oZu!x1J{|8CPWCb?w5ZbCRJ2;aeiJ2vf=+(Zz&!FS43_>7-_nQaiH@OoExUa2&9o-hcSZA|Iv|>LW}ReNynqAh-}bzd32f7>>eyn#H5J8^-9n-h7vQ#@Dq(e48ektPoA(I~&VP%(G%5%KJ%bu6qSXQBX%y*ubPw%0o?rA`Fk|dLm&l>RZl^UKHsAJXT>^*P&WD4dCBzV7iev#ArCHKz)Lq3Ya~TSfKE@N6aigbKU~s_!RU);0`IPq4ko#K70T!spV&KH9w}<KxKX^o7mI-B%)do?N8M2btYgPQJiJxtinWi4CzkdR%z|IO_jRkDMfBua@@t-PQ|7gyu=+j&!jg1Gebk7!wual1m2b^zDlaSrKDkmbsgM|9n|Sf7-({km<!&<fn<1!Db8r=ocyHe2ZQ<UNVb;X0a(a)c&EY6mv_z01W18n3vUK_;MX!VK<8#CO?v!5nk$IWAWyutQmVjUpl3N@ey42AX3eHh)7Jc4h#3*m?llXVT}<n;BohNxy4t)z!_#9@bu?)LP%kP^KV0AFmwJgB4|bEpOOjFD{@6Pk;mD0QH~}aS^C^%nnm1!*HfTqwlZoJZx*1)~W=15)`d-0e#uIFsXrIzeG#E3EgGEJ8#Wbj`%9L~h>L+7sBwuNVh!BgHmkm`m$L-IiKbEOjF)~A~mXr!(3`_-r=|8J$BS*F-1oXba1C}5E1y0o{=zEDHSgSD+Rob@Lw;q<a{LE8`VFoGyU@%*uj?t$8(Zz+&+vk0o>mp%TizocouGL(d#1>x-fNRkqdhsAKZK!akkxCw8_s!4=W+>EnDpKMiAZYG`hz*J(Rx2RK#-%}gsL`^?i+PL)<luZa4bEtFVzAoQlxxFvsQX<>c|g$}1_o9aYrnMMAtpy;D7Ys?D&>>}NTev|%~)K;r^Y4z)cTxc=bZ~ERS-7q3mqKLqgPgli6Ahc!wY99sP8Y=pephqF3ZG^S2f}XVBNb}CAGR~mn1yi$DG)b>2jQc{NP_z)Ny=z0evgm7r;veN9w-OB7vrIz!RcZk(&hkxJt#TDho-;B*uOk?(Bv3RRQH~mSAx!;7x-tPqg>ndeoO!;W%w5!-~;xWhE0Zi>#=p>Iefv;a0XncffDFX%gPA@i-$kO6oI{(Y3KO1)cz#1=2KWG0$~UWHfY6n_zTCau+#hCC*~z<$$@a-E*7DhF%ZD?Ayg9*TD{mm?gdS&s~n*q+LL~pWUCm9?N&PKfS%X?QYgM)k-TP8kVPD+&>8?uk_RhOFM5@gpXOfX8@|rXoX$bbcgfqg3I8%$trE-t#Z-w85kn(7wxckRvQ&M$;s~$%S7U&O|zTJ>56(n5J-5K*xUwvyH^$@s6hE=%|*`=m-CtMH0Yr8-@MU9Zpa7;>}|k4Q3#P$;aZKPDz!CJ+AGIuYhdQ>{`K{q)1^vkFsqcjp~@Qc(}5byk`M+cW+&Dgm01LdLghT9P7sG=!A4LJ01U}W4P!7?xBYxKu}FmV@KIxBbO*0$V93=&HHRcB@~*=?{Rzo9HLzSA1K?wmgtCeZvpoCMTr*WW@W6EwxG6t2sS)W)6wwAb+XPRxNY$jv6y3{y4g>6G-JcPfhow)-s1GE$Oc{3clnuKmOc)O!GUddxjHR5~mLl8~0_ze&%2Fb@-<qbk&5*4~cKPuZS#HD{^$6!hwzH@>5TnGQoLNakNMxf$YT)@zGPql-CT)Fk()Wj9`@;`Uf!kR&61}l_%UMp$orch{8yFRYooqEeCaaogYc-XvSgI4JrO^|XQJ8SBgO6WYb6ekKI7@F`c}}kvudM9qI|qe`po@sQSLIo(bZZ`N19B0|5a;!|a2ps3W_BR2A-z`hQ*iGUv6+@0re8#iN6IMdEzOfhAns<d(2sR44gHfGJR^60F`hTupPUTts;PKF{2Dtx7j)D$a6}4^>>G<{p-`PJgJl7-NN}WUsBS_jOq5jF<vU7+W_CS*4%6y2D>lfJW6D&+ZH5;Ly6)HyOM~WCC=7bA2kgVJqB^BRBI1S$5W9dZZzJ2%=ijVU*Z@6eaxaH-#{2#{-T;9F^AHue-3uc|@7HFT2uUE=6?&b>6`wWmITI?doJ6;|fp!kmQGli7=|pD{y=SI$P&slzN#(mfe@n=%;T@#B%jS+TU6cp}CR=7};;(K=6YY%qv?iw*CSn~sI}Z5EPEjXlQ)?CUJ%xhs(9^K>x?LlRHe7+(?~HU@*5$HPyb@3E;+jB)!V#lUn(l)Ix+eE6!=`kQ>7A0%srMRpxtSIZx_QJmze`|_&3#LMr%1mUDq>@y>=_h(C(&#+_M6wTjzP!&mu*akgwm|TxL-|T{xLIqZ<5V>ovs=Qt^vm;X2yBOq17~GAZAgl$OeA|Q<|$98NRq_Ch=KkQ^?7e66hq>R;(q)q2LAG>slnX-){=7SF*|`pC;~Aju*GAq<``7--?h*WH;3N2SwMwDp*dfaMg`|H-B8z%XGwkH@u7{`{?Dk9a}jEy{4HluXRMcYNV0%1=~nEUOoH9jq=#8iYF64F;jnJG{1${-fC#k=_=+dfH<-B>Zm^s#!b66D$A{*wwXp%oD<4%#=$|Q{$f2u@1P^nZ<R;n;5&0!Hms~rDJ$%@T6v^S$`u9t8Lo8tK8>b1G6*;3q>el#{a_EQG{k8H{^y-w%#}7D)}$P8?4Zp%0d-*sTJO<=zzN89-&vS(u9v2WPXn6J8lKo1y`L@qo@{*9)B6Fy2!(p$Z>1xvC6*+{b$u?*O9YB#Go&ux#ez#-wc!%Zt2mHg0CZB(h7nrMMdpjqgar5baid}xk^_&0vRh=pt`HG|GVp+%u~mGG341X`kDL3^jF{ViWo&{;S#Q#C4c^@Q3*KOBcuucDEin3}7K%JLq+i&G^)x)ZuRWCm$q7GQ+E@2}Z&PG13iN;ijf7-Ivle0wPR<cPkEI1Be<rmof)f4ik4+qCZin}Nl<Q-MTqeL2m{YQ&Rv!2doZwZ&2w&ef+kDolK@_CpR4&FeFW8D^E)@LbP{BlB4<o6>F`*hSlUpNah$bOcLfHrbojf{7;~l~70gep|yS=nJ6<jnbd1q`XN)M1$gTCscN>q#!aQ$WVDD^VPLG4z?P))g_HaI(!As@Zm;Mey)Odx|OPZ%ZZel%P!vjhrW&hB}1P>cWk<97Se7O|^Kn;brW`Q~yBUn!g+PN&Dk5aYcVuLkv6ElEELPRmPMHD=Rntr2dASM^;IaVAcs7Mki_%c`gkcznEWw<s0BJxa7cY{k1Tfz8qdX_%A_Y0TPXP@kj|{!nmVo`nQ0XGGVFLd}G1I$h~Y(a2(hEoSMf9gR9NXyerpMM)x$E>3h5NjKW;jDwLE4o;Fsk##fRa2(}<-v59OWs!^`7Mzx=808@`@Q*em9K_lXqG?3EKssEL6&nXw3(V?}n+bAK@K#6}Vad)Bfj>~ELPuJ(8z~A-CBbV2uz)I?aHFXmZI&lo;r1lQeJe=rl#;4f4_-Y_C!Q!ZA4w~aOrA6`fi_K-x)g@t>%m9+pqY!WD%}_rn#4u$oGpxO#l*IamKKqRPh#wQZz3F6jki~kWm7sk$;xuq%0|<wDG~<MZtK;ad;OI1nMmaoDbZ!qFBLg`lv@8JQK#WF=bP6^oIgwklDa--LMETum5Uanmuq#%dlRr;!DQonbX75#bK<}vIi`we{<`f~NRMv=9V>+8n~MDJn`ei`sMY77mn7R*HN&~@^V%3+xi$&L&3X6T0yRL%f(SsXwrtU<fDv3|vEUPm1xg&X2*T?bKoKmojFv#E=skAbC>1J!W0P>y0}P^Vq}P+v*lI8g&+&MUUy-xq=x%I_g{y^K*kM{N|31bkoXiBr?YyQ8!}bwDF$%@>y}krKp45mepb?3P2G=R~b;2rKx9C%YE?^3yV6y7Mr`r}BAuzM(ss*?OEy?Ez{lhZ(aHXt6VP%oAp<C<{g-_X1w>`%tmEl7qj;JrK90guBaTxy-Fl4r#l7{_Fp_`6jYO~k=3AE%p9h@j@?Wk9ebqIW#f4*FPP3owog~_zeB4aAhu_JPz7F9&<zSkxkLoX@nC&aFRl0U_3>wF_XwzMitbKxhotV}g2%66R8QNgARKGn8f57r8*>Mhdrx<$!bL7QT&I7xY@_VKuOn@R<NwJ>6f^jHmcE(SiEf`PYbwN!S76C}wklBE|#q?H0t$!iRi<Pr{lvP~eTnXuBS6L4{6xJkx}&m?)%C?WAVSE2Lm)xBTf0XQCodIPA)-~vsCYQ&qyU@hqay9A8X;bk%?Q`%~={G!BPNIxHXQ-a=;74(U0GXnh;>K_!A)jws`QjW5&j<~q3{;sS-rA@>ELjmL#GZ~lF-%ZdfEi~I?HRyC&QLE!7PlYHOL1&3+l8rS7snpd{E{DyrBYY`eIKtu6Tiz_Y4*<reidMIk%6lls&^i!c6oegG)=%m6H9w^@b#-i-RoEpRB_ZShvmnh=gKK=QOvs@rBewujJR}QG-T~&DAo4>if*4CRMM`XsfaMQH<WNY7Uqjn8Hz|VlHb<dMF;)1)`(b>g-N$9yh*X<eixlV6L4ZF5CT0SF%DpZ4AV`_XDe^<e(LV-!zV>sBum-B`Orn?6oGT9qLSN*n7Y(xf1`@rRS@+UqoeoXMpls==Y4(I7ISLH)!E#;ZtnDGe(kQ&9kor>NBHe%eG9g^wJYyGjCT(>6TokOQ9sUN3`_JZOMd2ex%R+;}h8xNfNq^Ingyy10W%AXyIMU3P@-F>D(ea@KomJ1}t1d%bBluGo`4;1$7-K)~-mz*x6%ebRt25EjU}pw`XWjF=og8p9gqV<r2fd&??eu;#YoeLstANVB*gFyDaRF=Aby09>oI-|hbNU(`SCiC!hMTDq@E8iT7V1R}9mU3Zs?af&_vq<y)@XF`l!3FLa0c2}7^DE|q42}geY(A~*bwU6(N>bCvQJ={gcx)}m@oNx641iL1j=`jpBZMYqz;^B3}`HErHo8vLue+<?mGn(g9eNsDmKM;M3^utRg~Av2^m4k2^QKMEgt;E#5VP$Anz0s&dQedf4?_UEs?4DZR^qYVQCvSLbQojY^%AA!M2um9D8K2563&v7o_7B&hpblapWtk&0;%IglWQ6Q!X<;KtcS9q3y%hR<Oe?zN#WOPVX{UX`FyyHUsx*>aX094Am??Rx8geS`5^q%gadwv+J)xFbm0B6B&F4GFiQ7F)_m52z89|P`+*E*v?WRfHBUuz#S7#Tl_@##9Zpi#5##AzR>a&7IVy23md1A0X7u_rnrX%=b_ODPo6On8@lqU=?qMexrW;qZJUNhZwIJ)4)PdCSlFtp*=y*aj&jEoUZ1KmZ4H$jhd@?rqi0LWl_khQ^2KD2^?P-*N}47$veux8HLn<Ak%`K$oJR-zL%+3mwp)7z@3INx>q<pisSt+-&hda{hp>r$Q8cR{YewH{_L@=#V(qwHvV9R}(pTW|8{UUtrCb)79p7@tasb7qbC4f}>$GqAI0MeZjs#4Zp*rdR=2GCc4tTsvd3y%<e5Njtnd{-ng2vw>&H+4<UNf{=7#XD{vO&;PfUYzyG>o%&Vie&+2qpOhRz7*0`R#|>pTYGvhIxG>Y_QEZ8*B!k^=;6@lsAgB4F*NKf?SzsOLle&S)s@t+?<nJv`30UR5zhMnJs<NY}Fp;nc*fCe#MlytfGYLvc!03Z&AOyUAtOvwh%e+M6w6=IFqqQN)1j`Kx5AoWJjB1#=0PB8Mit%<rtH0+*$I2H9{(Gt*l^MLd9d8LLunxl>QEE>4;AuQ*cx$huZ8+)@+{1tJg4Mh@!#MwE8?u!<>d_T67()s@Y0wVIzfZcWOr%RB1U(ZK(ZTrZC-%O5qH<p|TJ;ZqC*&yQ*senyWlu_h+ZOryEU-H!Bnv4Doxc#v`gPO=#&*C?x~E36tx}E67xO0BI0@P70I%c(F3TuzKgJ8Z|Tu4j=^}_?TSK$w$R%plmgyAc|H*<g{j?sD;nMc2Skcuq1lD-QIpU?a8u7m#*g)Aua{_o@mV1|G%}mP%fgu(;vf?21C%320l-KlmP}*6}cX_+2!jBO6bt1j7J?WmN^%<%0~BmX=W}o_Ej{xxIZSt+%qV2)l_|WF%mxdQW&)fIN6OP8KsI5MCh)mU{F+@-X>BdNqZ@FvRKX->X$$$lRafh`#N0(Z1#s=OT6<6iD}J)yZdX<k|-#x*=`mhbY<cPKq&~zi>OmXEzFcRO$rqU>ox1>7X;SB>&uBTL&d9b6<I39`RamLXX3i!j5mR5jK#aw4~b_Lo7>U84+)6C;7%t;Fa;$DUUpqAOYJWv7|>-yv6i-)lm?I{6*U<+Pf;6wIm%-t^hLAG?y!D}sy3quAulcH?L^4X^OPV&%BfJ?sumJ35Bhf9q=s1wL10x$EG3cg%S5ATsBI?p5Nt-D1~yZ3FY%zD__znFU@wXYZDrV(QK*>Hw#f2qhN)Ihm{+FVfBlu{S3N2gy1P7yo#!A_MP`-X1`+$`5frytANHtHoIf?O?O`YSn!&9CPaEh|=yp|k)QFc&s?w>Es{C5i7BpEwy6SjQtFDI;-b_N*1nw16W!sr<O9iD`<6<RTDMCo1A~vf*@SAuSP6fe|V(@rW;EGg8-<RNU7`>Y>K&4P?2Tin-1(6-mZR*szk%=hFjPd@uTtJ7SXsigA4B&c%7!i*pg)>zwooo4=Zg;vKQ%WN^S|hU#HNuUzmDQjPZTli0tk9<rh(xbth%D)3@CTG2b`4;L>wfsA+fsUwtIe)QxYz`eNp$GA5mD8CHfefRX(OSHsPxp1K=~(`_b^A6ZJA4<v3M%k?X7M$#wPL&l)#I6wpOE<v6U)Rb!AfY<KkHniR4*-N34viPiGUu9FcLd>~32VjR%ryp4geMptqT+pqDgt&4s-#5)Ce`K9H6jQ-tbjLU&1@d23ZgvZSe3CVfzCI+uLdL7MYBR-FBH$Znf4vfE~YZrIn>2Rn@Ebk%3-g~>JlR$5Sg6&<lU*Nxl%ya`^RS@BfiFq=suC6<Rf9#qxAB5)(*fD3cXwt_=aBkni(kvbQhy<u-*S{kE^1abtX4wAZ%yeQwxiV1mGqr0<i%PKi&a<)#V$QZP7e2z}OeoVI&WT_J&YL@EhnyH<$(SbZCKzen0RPoN@gLEs1J^6tGLm54H8p_VXBIHwbI;xm*(X?3p)Xjc52lf&iJM!4zcu)+jcD<@rZc<7yfm0w!G^i2{^bMpUL|Qi|>QdL0@G|Q=RREn{z&lReZ?Oj1VYmU6PkD?zj+?;f`dBv{>1%AD6ldv@(qR53$Z%0ykaO5fm50hIo^;VGsXmaRS1U<_HR36~j#Mi8<j`xzRBCmS1iKc1rjC1`_Q+Bv-6J7KGTH%@qBkQ`Pl?<#8y!wdHUHR$n+S7lSQ5^G_I&v38>6gU8I(2FS*3+qjZ)Eev;xx;15;^rRC>#4h-W3Ql}e(fyzTd<Q`}G1VloyBB3<J`NlCeOq!&$-7nI*Id1+$P$u6PIRuAL(5*j7d7_UCQM4)b!CqMPxu;9_S?3pd12LL{Sopq&7(c%?>)Os^KB)=%~T`EzILarH2?}^g6t>ohsiMZ$|sp5HADN<BWuPKVd&j@36l(9A1qu2nzT{$~Bq<SaGu8fz4f<+g2h(3Dxit`*Fg<E<&Ehb!N@ka#>qti9c5?tmKI;VZn)T&Bfw+ks8a0aey{L!U?uqYNM0BrhdvAtSBtB@1jl-OGYq|B1xLi5W=3qPp@9R*5l-8f!lSE&h|N)`)jSkd@`15D)1PbpS4=z@o+nROy%Ej1WOyt7E_lLQD{UUDQ&0UBb?U^mliWS~z&dYQrqa;%Z>rIgPg3y$@etd@E%wY|Q1knDMAU!(H+UqjpsU!Bj#0IN^|=a9c79)n#}pVRjh=wFIX)vVPzJ3EX8#7RE&T+FcO1=zenDr_Z-G2%(=dd+bs!O|!aKC6dil1e>MtCl<x<2X8DV@<?+22CsiFh&|Z;}%GKz}!F^E7uHy?Kq=W;|PJ6i31?o+4&t*8|?$YK8pvyAPLM699w?P`XCFsMyBO&G@VSJ{3sH1uI`u=I9A+0zn6n-W#@=s5cDcR15Adcj|!)F7E-5T1Tn?+V+67W9M_9^vqNXLLe9MkUJ%{O1#vEqL3`d>?Gg=+qF2UMAnfeTfI&~Bb^BT5O$R3^ynR*rs5K85Ve5n}EUp7%nF@+}c|VgG3NCu5+eENHZ#2>-dXe~c9z8w4u`2x=H#50gnVn*b1TH@4H7-!$i1f(HzgH2edX>iFlKUknU;GN(xoR@0fIs7@b*mI#PAf*t>e^mEGpXyWWr?E%uP7T9NWXSvh|OLKIM*}Ky6~y?1+h#-YDOqam|C%87^0b01%jI;eB=ef@efW*2{j{ONGD24(LZ@gV>WOxpv>wTxPxLD_FzDUMl*;&MN;uM7qie&8)GdWxxNsGs45Jfu?C4vDRMKGK)FB?*>!+o@%(m{-)=HBqeCb$lI13RrsG?;H&nqsSF58Oeb1VDA;i?Cfhk^Zz&fI1++gp!R>s>`coNlGU~Dv4)S=#0Mw=f%3OU6XRRlPaimqVUctvK0C4eLfI6}TYIF}97IyA*zfxss4Bn>Dm-nm*r7Jz2ys8R+C5-9^pqXr%K>T0~wjmt&S`WJCCrg|YYyiAxE3ehDPfKc9>*WrVqXy6!DyZ;Jl3kF87;VP<tuSey#S3stTk-^e#kK~C#kAgQYcS!VhjTENb3PYT<*e%kmH$2wDDi`eh{3ker5T@`Y?gL4Oh6)J_wThI*tQOe$M}72wH!1o#Z1Je|R6T{OuoL#*0Q)#l3`s%*lZ(zQJG>`87Q-jt4f!59tNoL!HZC1Sm`yIkTKXH2Me=pji4Yho4F_{;*Vzt7)d_otI{Wwz<om1F@vu<5<CZ7xwoG=o-WH6N6L@OgDomkwZXK&&eR^0+06N!}@CD5W-HZ`YO*)GsQBr$MA2%uW-g9N}C`R3q7Ap0pK~8R!RiH7ed@p;=QtjkWCYzKGjs;Iw-r0kZ8=6?wm?jGa*VzEF7ZeN-<N8qc0>MfukP<UVEZIzGF;sw>R<J10m@-U=sKvhFxNdMrxig@w2JVeWq2VZkg}YoEaY0t4h!!LR?`XEE*bD)+Im3gAs2u~bhIo=puuAuP+@E{8i;L(pm;N@38k7ADHVI)eM+eH!s2NQ^8xq|&354>>LA|^bCB6nz0uHD$n*#Id?87;5lNg{&8ctp@Wj6P6O7UM7#-JiC!dfJ94)L8vOxWnB>$kO2CsH;8YU%P!_F!cjBfkaRc+BoEhp#5U(;34{VALPisCRBF^OQ7Br8)$&A0uqtE>Pp${dne0qUBdj<q#U_12==VG}h-9BFs*mmg@y2e;(qJE~#Bs7~rfSr#)B|1$m!wB=mYyO#GPY5me3ql}Oa3;oSa&3&tK2Wi3*_Yx|+p2rsG@vt+p=0O5P!Tsec)AHiO^5MvOcD0@`IdD?6evSSrf1uRdmgD`=Gu>3XEFG0P!@)6d|r>pGZ%MpqS38NjTbPSkGjJQf=Vuwtz4TB&m7H!)UgByx}$;$kl?JY2-Lm}(t3-5t}sZ6ljxQ*gA;OU{CYgWgZPL6cEkSevWLF0;mN<sXRfY1^!0DxI+C%SRvc2t1OuntbiWE_*~m~ULRjG&i9v-eD@)TUY%&(lz4fMCg!s-D6_3v<q6TQsPd=z(u=MT&`_I{Lwc1ELBg9J)cFh@W=iDGC1gB6gO_<UYkxst9M0xnO$2XKuP{8Z)C2wycmD3}ys7oKFc|`|7Tzzy!SbSsKUfzM5>U9eKPGFD7nBt<g-OxILo{N$tM|7x_&y3+Y#8$vC379bBuc3EcS#RCWZ9#9Zb9Wv8!ki;^pspn}!M*7QMc609-UNoRmVF&Z7Vs_CDWva{fOxlsamO8QJCfq_)*@2ZgbE`rr;RQv?`JPHtkCucDR-zswz_W-dE67rADBjE9T1MKn3e$Q*b{Qw&(q9Ne#tW%1vm8V6z7DIc)uB*XfWE_E`6N5md>uPSwC*X3k9><NV=t1^njA6lujzp{Q+p8Z{5<^61ghbXv<TiUD55y%p5tr9ue?69l5u11ae`R>oEd')))

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
