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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-qxnO>bODa{Mnm^RR5TI2_-!n%)_~n&ChnZmb8wVgavVz*ryFz8U`S){6b{`ekH9WL7nWJq@Qx^{c9vRh1bT8Ts4)-u(NY|Mu6v{O#tSe!Kbg^@k5PpKove<In%~Z~y(}gD*e+_0NC%&%gZ7m!E&T`TeIq{^{5EPd|Km^YP~PX8+Uf^_Ty?`h5HRo7ca*{rUB~FTZ&6w7<E%`~3O;ZZE$2?VEr8^y~T8*+V|;-n~12`(5_!>yJPDwA+38_WQs8;-|OocQ@>Z)zE(b>Fv88{`6(;A3uHlv(v~Hqdt89*9Y?t&jXBq$EUhpv3IZE><(XeF{odj-hce*>vYgh``w3+H=nIV4KFi)YllC$zZl5#qiz>JoQJVmRKt?O!~d|`{ct(+^_zlEKCavIs?S=9!-JN#arvBEG`z!x`t9b;YkL(AL;CRd+27v$ynFZb%gyaZFV6ELZqdM2FKRgqIn57GpDrxxHh&FqdgV#14ek!V+vh!T`VE=TVO5fK`sL$kbgKt_eQ~9QT5Q4BA9wHhBg#v){-(u)537hrpq_VF=kUDaH^2$TX`O82_^apd^>*LoP+o<puWqHKJ(HC_{7%jMPCt$rN_nM?=bgVZp0IR%drwQg8h!#6)n2~vEw^#1r5$(v$LB*T8Yx(*WN#e@c)i5|yJ~U1f>n{{(D9$6F`vIW{8al!@<rBHzIl50ZujQnpZ>6W|MBg+xBq&%2A4Km_1=DX|MY9cKk8f=XDc|~=ciB5#eO*E7PBRu#^!V7W{Ky4G7xqF#@T=uRoas9O^4;0U^Ghu+`T@0`{{?HpK$pKI!@@}E8%n1WY^BjreG(R?tn2YJmrf;Ilk`nrZNHo{1oEBZSwcA9MiKCGi`n1Ep+mdPLJg40Uo{~o7nT(!Q#+khAfZVinR$B4x!HX0Z%_TRq;4l{Y}a1Ad5NT#DL+h#$Ef`@FnLT1}0Cwwln#)KXP%Q>XSTvVLX%k3(XoHaM$YJdp_yctM`xKNP%EW`c{*?Er7}}fNI?TQXXD%mq-g>o>%(2l8v3l4<-UOTL!dfw~}8yw%>*#UnB0>mA$Cb5s@3y98gg`KU*3Qqz|n_^kP$+t6sFh_YzK7_6r!dHzo~HzPPuuALP#7uH3N?AK$;;|9<!W{U0r47wkZQIMJ)1@c0M`oIE#rj{fxe{l5^q@JDd|B7X82%hDUb@v>h0kvjh4jZc9%z2@K>mkSI(Y`IdoTN<2~i}g633#F$qryZ=^X>#))vhbzA?56q5#~;pTXvfz#9x!s}JKrCTZ`5_2XJ=i<w&*{z<l_stx&Ut`u3zFMcwTAdvz4&B^wzHAhBvcrPUbIL17fHT9aUVk^Yi3eLVm8=;3O5RoXGr^CC`i4U-Io55=3rIeY%UoX0>Iv!k>k1!>9q+>vKlPh$oCr$l8s0e93Ud(2j|bg}O7x7p)LCP}i^$7?7JWf|p>;JJ4<KTyrmKYA#LZxPuuE*=q+*tQhMQ|7Z-%tvsNEZ+?RZXfM1L5V2RS?5*Lj(ug4&!K`<JJk?I-orDPupnJg04i0z0&E8H+&1>N2zTiz?jHTrC0c2I?hYPMQ7=L`X9s*6E?{t6nJk#^nt#UB~8F?Qmm5*X+cNKGuEX#SU{<7HqrViEgu_p8HV4aA;cxG8}4$&pid@AspYfPBL6V#Jq&JB2q>&npyS*M7f^ly>Lm>Y1~4?`qbaOGCUXE^4S;W=K9f7*7On$g9Z<gcWM#<+V@SU(%@%Q-mLfc-|CmKw4%#fzzdR|MtEj@TZ8=R=$F_H;%e4|(7KQGcTLJm3?o%QFn3UIk3C6Wj4bkFm)_3I(8{NiyIVh-BqHt}#`$;1oT%)<o9?gDUGS;SM-+YCMpT7ST2|;p0uo6LYMlgV{K9yB5Nc`(2a$qavYgbP`uurMXVu%YXlD7>nA`ZX{hi$&SK??v;IRn?9uUDj~-vEfly*KdiAWOUY(dNn}3OA#6!PDM;_!;v&c6UtMr=464}v>FLXV9zGX<P?W`#4r|1c<`vqUzVfs%$tX~&@v!Lpt`5s}*fj56|MJ6)22oDW(2lRcH$(>L6#3vO0I=rK)G>&03#k0J9YFx9Fb@DaH}{`?V*zYaHWq_%yDm3fui}qSPak&8;(l~X92fiay-wD%!a4#kcvW<+<Ciu2%!SX!mQ=y>c<pkV1cc<OZIZ!z+bzb?XTycliJS4+uHHNyj-yx^5>MyZZzj$Hpbzn2d;U6H=bqYnTo!vC5W_a*U1VNj^%_poj@urr4Y~+qbP0mIxU!*S^tj8dZ9s0#VnSuDoN`(yPMlRNPGDfY+(kSV!^)i(73@Nok08PTLxY9YvDvPtTM-=K%lA_(%%`_ODlo8mu_$wU`3B0O5ag6i6@A1z&8)Gjl7Tlf+Yc8Dd9k%Ywj+Nv-B*16DY8M6k+-(`3-PpzVC7WBheo`u@1wkM@V3Ml7Ctf_T@3Ac&PS#w(g<o-b?Qsv6-MkKD+^WF3Izoi_|Qi58MC=f>4@GX@FN;Eu|^sxjZ+Y^1egPwv~JV4D>Zj=VyB^MX1VX9Z3rk>476g1vV<4G!P8m$ww2p-CF&T-e}nD~N$WFD87j&W3aVMP0{}#fq=md(PEU%a%Ica8R@GS9l*Jiv<#aIH>%xg~@wrPp>(=rJ2|s38*pa#YEDc_V;BIMP4J_J)4hS7(iF;@QV^TF+g*@byNemr$=ICyBum0wcNhBK!ug^;c&S=wMYKEcXp0hLfI#)rZhxg*d35P{3ADp2&dn<!u0gFbyG5`>)d<bln_}&|NS>U$EZ5B5r7|zhc*|sN#-+oH5F{;_fr#|WRGv)@$e(}#{@g70WrT7yW14t*oTulA*+jsx`HJQevX?S?g3#<><@M$oa0L*<pADZvYC$g<2BpXq<z5`S^da}NY@<c>reW6G?-m#}2z@C{LD<`WJLj^RHp>VjZX{qp$Q+nOIRtX#8xP!FO#i&M&5?pR5mD6Fj&fpjLfp0}!rXfHOT{`p*0iVPKV9F2%jRsf8$g9K*O_6MUy{bh6J|;E13I~$=8-`GpTOH6cwFEG5r5oK7ZOr%#=5+K8m-iM;17o_FS(dPt1^D>%^XrdKMUi$UI++;=kdeBzl+q^%zC&Fr6eNVvAWV<pW|k~PHgFv1K~+yBMFHhDZ27jr0D)031d#2nIkKv!a}dB6G!5F2wPNtnX&l(_(VzweR%vY;vFu(EeRU{2)B3W){Zk`TkBAM$8bObzZ%D-keVmqIlUo$%LT#+Q7M~Az?JG^16Zs+MkbA;iY|@68^31~Bid@-(Gqlr+sPS*sPy`_aZz-plCsI!F$9Z?e&=!jp#WAk}DmvtGaDZtJgUd-V%)6e6rz&uVUw4OdF9XF+8h&LYkC-Y&!y`b)A4<KijC+_k9CXr-L@MT8fG#vy;-b}N@Gu#tv=6{L3a>B-H!BaKwM&eUq_BG!H~tXWSgVl7dhnfhDSdG>L9SW6hE$5#nWNZAnk9V>6=!WTN&E%I#(3ZO?Z-Q(Oap5LZflA#33X#$lQ+p)gFXFMY0LyIGxFipC5+tbrIWzzwhjYmq$rMz)k>VEoYYq=OwIrj>hp>3!E4)=huWg@A`hJVXL{cbSF3LEbrY-e`A1jXSYhdz9fEiz{`tZLk=x}0R-690CmG#&C&XK~abn{pgAI@mwq!PL<d7QrI}Fs0o@YmM;q5cMnNSPTC&>h8mYF>D%BrR^rt!{C8wVvWmJ>+61K74XC*bi~(9$JC;+_VI+mu=WKTNd(wvBRx!i*>e5&;iS9>D6*Daa%wm;Du%x>P&Z<^+-7RU$}2DrQ|<z(?^5G`MPOJSo9*=4&$@@)R9vro&l(sbmiL8iDYdsrEm>*NDLs&TmkB4IPPimPOSFV8}5+ZY*<5VJ&|P@+)SR&6j0W3;;m?XPO6Sd~w1vC`P0ZKoNV+;|BO30z*hE;$xfCjg<_6?>;VUN(i}6UdiS69%gNX&6mp0v)~rOxgmt`)4PB`fN+Nh3G4X<JyZ(`UX}Rb;#P>1sx$ISse>pOSlw?UvwqIbxbK~Gb5D)#lo^1v6#^?JROho5ob4uWOJ7|V6=l;lXUZzzS+6XJ%UZx{4wlEj^DUH!n<VUpm@B=<yNnXp3vg+&gqyPhgf9Ob;M%VK{(Q&mK=s$K#cI`A5#6S+9IUQSk)*tMXBxHzULsR@AUY!jMK4-+kY(BGcovkYN`)(!#164!vLfA$MeYO_Ib{=u_C*kxe94Z0(~P47btXb%rq~S2AkjT*ZYx7Uptq6`3G<j|p6^z<Y+X>kNCq41^m1Q;)9$XOjftdPY|543VYwwQy2R+dGc~4i9=Q{{dX>G$%@UQiaMrsYfBZXADr5AB0a^u?C>Gx(h?s*{H+$36KE7~;1vVjHU0jnDMo>d`$QA1+r7?O1UMMHowdgCX9t@UxEFD~o1Uj#AZknBJcm&?WDlSO@18^I<4Ybro&vS3?GeDArDl`#}#!zE~)5zwjK`K6P4(!4l;%Z?GnUOQRlO9a9GezN~yw<D0ia8@sV#jh5_S++|np2g$j-j$NdZIy;>^~^N*$6$Y%h(L-s2ax}oBiVd%7-Zgry1s7BE>8mm*s%-7@-|?UT{9d_M$4V%tFD7CQ#QDP1qs)vD)q!AODmcx_YtAx45VI5tcwwbVc<3;h6Iiu!ju9z0I)#8w@omTe8-0!b|dy7?A#U@gT`9n(?OWYDVNPQRN@P51P9AG)WW|5z^EV|9QDf;G9P;p5@ouFC$AXxdv6?oON-i8ZVZ?)>NUxk)61}Ar_Fs)_|euGkK9^ofNB=+^cz9I(h(KdwkJ)M=1*fKa_nfD07Xq7&&pV8WRKt5;NJL28dTb#=;7$QI`_)HWgegw!u-U*2H~P|IBC7;NVC0iP<U&VN!KagVB(~%<gjFkgbpd3jKC@cm$N|&Ns&SfG9+$K*?LOI**IG)`X6y5G_+I#R^&IO=62vM<^TYcSmFtNh}0UO<s>JIJMEHD*h96TM8p+a^a)>S?AiG`F(y*UJolKCq}^`hH+v$Yq>0H&aAMvn|jU5Dcp?@2;9CcGN<|>a1*o!XrTZX${A^)b<582+5tiOJj-*TZJdeN%dXlB#KfB*-x*@?VqmbiDi58Q0nY#d5_B+&$l!1UI>q3cVnU_ymN-6Pv<bpTB1L^)-1uC+N5c4P+}{1%EQCLx>kP+=w^z*OdfRX=j>gza4i`<Abndzt$tLhztQX~_c$o`0Cwb#A#&C8H)Id<kR+pOqD^Zm=99oJz@FcS&s^1S6{4(XTNkF5!Sm_q)*~+?LlvbMeu2-qk0yAw}Vy6A>TF@D3zEG~>yifm<RVonxb!i{VipN+3d5DJnc{?mG!28k>l&_0wf|5DJw(W57NS&ut?)9m9MibhXV6(~CcVB;PE34?Wv=)>foqlEanXLIF#=j@rI4cKA=s}c1QY%FifDbz8eGBlsae}E{3Z;$V4h-p4mALt^XF(>;F$yWA7<xy9Q6Akk%_fJGESehlXADoI<#jIw^%T+!)Tibu26p+1OR%94LQ<qn6cWYW87t<dyEZ=<L0TM`Q&|N(c-KvgIv|9cNyAlHD7-_H>H|j9+%evbz#}Gs6O2$e1UHv8{<TDw7zJX+U@4ss11LLFC13D;zy@(Ea6w2-(FS#Im@nrV>z`qFCT_v-RJs$chO;D49mVfihHnOGk0CH7`;G?B`IN}b6`PB4>RqzJrkh}K#19MjV7+@+nT?ByAo=_&2zFhZGItruwfPo;T|J5var;Db`4vNBLm?f|-E5YqS7`Ibb-s*ZDg;%dwX+0eR2Mi(v+70%AvD6ib(+<-@e>ak#*?Fw@)X1<R=y~R1H=>Y!%AB+n|ei>2k@(ygs+i%<!ECBPwH|HztUD~bgV@)$%-ZY-gX@;oxJ6+4<f-Gqt}A0vW=dA+)vB{^h+acY`s=4XSif`bNKzPNWr!+c57R;kT-zwr3#F<6`dpt5(DNsfgvZiZ|0H4a~we2EW6swXhVP1<c=}*C|6FwC<q(Sy+<80O&|mY^v=(vaxnv*PD(cwT+ZZW7H>w;VMez-Au)SBEeiOw1r1L)e~Y@T$VhnW>lMZ2T7<Pq)=m|C=}3DnYlS1zfPzP{ZiTPFpRXf%WkWqIYrs%z`N<S>BT}^b5VPUlVdDZ91m$3<ZIUECnCh?&qBkxZ&~g+Q4$5Q4GSiwNXZJ<9w7Mu<25R%TtghL$tsrVyt>LS0Oqj|}JJ?y8HH9za_av0|(3vnv@t>URDDqQ>EXG(;6+NKia%>u~MAW!hI_spu!Q!IOgemfI>hflzg(3hSZOho(&oZd4IoFEl(fO*lrqF&84D`5Il8<MXz4==E-LlOd4~J>xWhW>MBvk>{I3KZ~SP0C^hRU#DN``>4<Ly<uYzjP&DIaPVKU!>8%1kjm5>JlF`|+Y8#2_+AjqT0i@eAUpJRXir`LFqTFCwDU;wJD|L4oIt1~vhTrM*3iwQd=<$EcL-T-dg$U^-q=q&mUA(_Oz_j1s1}Tud|?I0eMRZ&{!@OTnJ7P7k>i;kk)%q*WbRr9hE7wGmU~K`k&eOTeCgYahvCCx}_JWbY_l?>n7|$cp;4{$~O5nh0B&)yJKBI)iCBSD(z%^_K#~OzFc<J0%bt$}H_Duad|Q>YC&HP$(&R74;yQq7N5sI``Izq_ujj<wHP=HlJStl>4rYNsZuhoO1;~RH-FH=j%RbEPwcExBK;AMB^YFNE;s>aF>60!F$`ZF)10l4he-3E>L8+2!<kzLXo4!kf@31ntwG2-n%dG?i2*>31tBvrUBu|*&qrEE`-p8Oj;tyh$aAT$`*K6@wJtZvE@I1mU{kj;D7uC#sw|gtAX14O(5L{gU6HQ`Lw~K7p`g==hje4W$J!A$T%lWi51FW1@*U!>)CMkARC2<JF%iOA*MS`q&b15kHY|cLM3NKch4x*y%y>ckxsc!g=S4-yy`@u4IrQZUmwgZNT#Q)kVq{MA}p~;_HJY?CP&qR-`k|o?c7c_sXM!|Hi!z$OO%7#A+aU=2Dr<Hjxt9Cyb7s(v6J^tALA>nbOHc^K4vJJklE81wqTwsr|DMRH2s#N1rOFObcD<YGX-Sw{8h&ZRC<@u7MppVy_>}_JFP<yWV}rd7vA$UxT?5Om2b`I?nF&_U(^Peg9~}`jG8LvK|;xr4naR@h2!Ht2q9}L>n2n|*ZntVSxtz(N7_?r{reXrUD3;GfM#`lT2*GTU9GFE_Np2zJH#ppCJHwpE2XLcK!n)R!4wqdeGYyxqhF~-uTrl<`5tR9ump1%whDW@6N13OVbAt**28tW`jVxjR-wHotPdI;j%^cleyDoEa#wCsDQm7?uD6oDWRX=q0sxZPC59@%7Y=-}k2mA>=jAz(PDqzXZFm4q<*nGJNX-LtD)b!&Q?Q$~8&Sh-{zh^b)0h~zT~6FuB1&7V&P1U2@?(J1@Rped)>60x_pY<f_cLratd0ZY!nn0aS+D9hWnS<|kqxGVhwbd5x9!^>>prhRrp1<(5>QMLl@9-rBN0x!SrZ50)r9%?&RG3yVMXqrxsveBQT-x)E$C7?3heofN}aoctUFau?@4ZY-70vqs8$<7hl=#Fy$Gvl%hp%*F{ntbvOi!Dd_(!&kW~C2I6W@;s@RP%=9&Z_L<X@$eU@W5BfSUjlP-}Z6oS_+i^PtPq8ObPv#eZ!z(iBmUK3}V!%-G2;ui|(d6zilijUmtf=vL^ChWt7Ni1Gd+*FmpF}}1+!Ak)+n!aHuP$~W~T}MP^NISkE&33Dly8<~y%K#Cvpj82<0_1JKI{V{-wCXkyUMu2SH9`E$?G*?4;>i)9v}^rZtWk!Z`-<7kO#{3bE?5<DVxqGr4+_4-0+%JECl)%xb_=Mt6ho5yP)HF>y73)&^>WWB+P*2?I^KqtDHH8dI&L>r%g{s=$?vqbNVSHXb32KgTeW?Orr^r_ya8w(SzfPP_E#)GWH--gH+H(y0C)EItmp5YMpKNF0@n!@?>7q(F$HsB&uO*oSX;S)%33C&j%`%L!iBUAYi=OJTvGFEc@#Di4A^N{j7o)|B<?Fkic{%at^NQA#+Q|b?&XaUUsOCma<Q}gFk}}&To5*i?<&ZHRvf+m#(XeY_h({qj#Af<lsyv&3hrH#;bN<C39(wU?(cM}4w1pq8bC<^<4~oHyk5GwApkgzheMGg=1Uhfnj12xgUIMA#nGB}l|dKF+ylFgFouS{!n>#jZ=wR~LTYR(p0~G{E#xX4-$E*hfV8Vr_;+r_eAr%D!Ntfn;e8Q_Vhq_szLt9fh)|kZDn7TRKzIx&s>s?59T2vZw92`n4-?dCRoW!DKjYb9O*ww*iVA{eYfwkw+B`H(VnQ99wh=0(C%}yYxg=JBBq!u_7)P{o7n=3)Xr%RPR(n?WfUh^6^b=mB7HADaOn}EtnP)?~(_^BVpi)C!*tJ2inN%dsy+KC?T$b(_lXy0HzK_h-niM0;vz+4@s-jkYg3|Kx0qhJye`kDi#rs`SpuLV>rIzMd1!28x6=bT|y;5vj&RrYywx{c0spO0ncY{YdYvSlv?vEEiUSb+A18h0<7f#9E)|K9qu-@YwgzFrL1z@WrI}WU?s;Y2bz_mhxA>e<$)D;J{n1VU2hIj#RD^dd`Skns}c>#JOG*{zP!L^UiWw;2zuS#?vtE>)Rm?ZrMKH?qGho!xqZU1qCWU)_FEN0($Tfi&S7sB|TS2FKeIudr$b~h0v*np08b*X5|DQavJA4Ar)nGorjx)BEBeDuB%UnF;a!C%*VyO=IzC$OpQmpx$=7Mhz!5M*2)jbTo%^TOCZ1S-UY?n39Gz6ccd)(8sD<pR8Ds7-i`QH{!H)%tyvp_|;TxRQdjSNGAZZW}<GY5mfkpVth-@!A~@ZWXi00fK3Qf1b5D2mUEsrFhbL+Cs;0_)&ssfve5kQh?pUNeK4)+zynd%Q4YLUEiP-Yga92SQEln6hGsTQ#9@5jy(nMA|%hVtjTF+LDY`KJQoT>of3|4lhr=c)w4Uiithug_B&TfQKSp-3ph=NipsmF^lIa4%G(fs>=CeaUlMvVVIl{OBb+iulRRD%-%lo$McuI`sm%9Z=dj9b0+|T=OgfpZ()f~)o6jICl@H-i;i_yhK(ZoeLb0;5&K_%sZrNxeFP{HalrZobaVEZo-da7C$9F{J$ch$|#J{AW4zcmBx)Aj93;MN8<HGKCVC(A-p#lJd5Bmrz+e<AKzgP<Mwq_u6C0!-al%66RJE3J#Z|mr*#zbn6%=GfQ`n=R>Ml8eI`O)4U2uxjUe^0+?h7s{aE#*bM#;$t-FnLi*sgq!QBS-U+ZI6wz!+A1-PDIRP?105dX(CQ<?Aesr<B%u4z#W@KH&-N`SzIT)9ZXghJ)foA`Z&R9(c%I!)e(XR?-x@xvc_7@$HGAQJoUsrVQPdk#5U=UkKm|Z#Tot5<F}chxVdF&vQ8{$qHQ*4Uk;1kN-O6U6FcG_TYvyP$aEp2*_kaCz)1;_&ir36(bNb&a8PU^lq6s>RE#<don3>YwlPG&Qg7<l_fJ23dh>C9)#WTsT15FqK(DlC(oAYuQ<!3AJP)E<g|D1W=K@eMD2)&Ei&E~6arsGmG(!>pw%$k176mgk<t?01wy+=Up`E0fDiQ}I13nD3c}NpsX?WO2s{~DLH>htS$|pl4N3b(htt(Aj)?$Y`Mz0dZ`>Pq2UBLtQo{qcI-l)(cL3v#i!|>BbqTecH3Rb(wwgr#!sHY@SQY!_U%JPYH0&2%nt0`~I(Ky^8qLihxJlM3L!$Xvnh7G5lC^?_6$5idw)nR4c%lM#=(?@w4t;h|0i&N57@aS9#x_CwOaU_fG$2N@=HS`JSv~FLBwGFCQW?L&(JM8nmow5h)Ag;%f2U2nlbLh(Qm=UA+t|IEVckc+05X<R_jUBUXbp?fs2p5!b3aeD);)OxThFljkBCb@14X(6gKy4}vsE3y$J4vu+gyXc=s@Nm2&9RI7vmrlBWjIZd%_16j4-vgH_)YKyaCQ@|pXX>qH`MeA9Bwy55go92qEjmv`92*%oKm%UnUb;CKrIBN3H-I@U6;eCmJx2+WrPu+G22>EeOm*~p4E)d-b6g_=|<Si%E7Gbr;FX<npzINUkf0x<niQfVadE8KIE9n{n>xLmEA`Zsz=x-CLjfzTV8Ql6aiyx1N=USHk6+Rj1xMpJr-D6zVuLzV|ijX^8~EG>+|n;Izz4TFTK($C?GLnAL)nyaO?GnFf-H!)x8N+kikHGuVLkM&0urr+A3ECfXeku+Z43mUiiCQB*5#rNQ-_Rnk*(f?&#T{0yZix-u0$RI2d@_jA{-Va4e$FK23~lR9;(%V7%Ct0MxsMua!u}y&$0^ml<PTDbX?fsgP?}@7vDAUJ0hs*ST&Q#qm}*<_nSfQ^bG#B+uAO=<5D+s}tjLv9@4kuBQTD$(fpM2si16MEQb{U5|_KIM$VscDpZC?3lsoC^L!lqyT5B3SleF=+#$f*SrMbl6nlK7p_Z08s%+cn(lTrXRAZ4@%DO6@)&UkcoFo11iq4tK_i&d*Xg%~=OLx7Qu|pl64AU5MD%X_lNEeb(xUfm^pgv?O7O-MG3Pk+XlaBgEyBw`McGbT?6Nbf42l+LD|E{OAQ7_0{Z@jXMEM`3YH<!?vM)@qsT~TbfIqPaL+*S)_oGcDmg4%#q)=r|rPn=Aw3>?2Xh5vUb$$6&q!h%`(nf@eHs(O5sLch~30JGZwhLGNz^&YQVQQruIH5c~lQ#igr#dWhzG+GqnH*UVPJt55iIm>>7)`wr-E#YtS9pbi!NhtCl4xfg82qq-tH<}$p)zG92b`w>ab%n5x;WLnbOpO^Eu5Pq3HQV&i8xaBqD%dO<7_hZY^*R}FO)lM#fNV!5|uV5u?pVoE}ApAQ_*x;?VHHBSB2L{Rh}r}iI>0?)OYHFPX;G@PB+1r=G3S-EM!%0u7N8>|1ED7h;)j{5t{2oUxgyoqz+QK4POT8+B6ojuUNkU-u3DwX@n*y3WbuXwo)4TMg*tXD=LhFP!8?L1nC0JXa?x?8z}COQSxM76EI%T#+XI4r5X>3C=IV)KuARoFhG_?9!WP=t|iuL*XU9)5CB4mJpinka4*1kPPakj#w>7kFB+f6JRwvAjhmTxri0j8iXr!H4jr>ZSJxaV2Rl{%^|ojxzE3<bYCJm*=o*@BLzPH(wp%7-k!fn1NpH)14_cWSyfjr6D(l<;;|PBzGdg{dr~(F$2TWiG4-YNYKt43tMwCA6_Ih3ai&jzVYW#=Ch}1nRZpI(cl+Ehh3mS+g;q*9EYHv7=l(2cixb{{;Cn@t=qg>m$;8j5XzIDSvA7bIffk=nX;$b6lVH@>IwS6rF<$5)Nm&`*Ms3!`rHnD1N`8Ne=Ge0xigi<JXrvTKA@uY0eK_ziis<{)qmz$x1NGf$4IspwI06Pn}`l>(PGq3b+LG-o&w{ZWd)r)%?BB6E{^vcvrH?q?Sx)C2Y0Tc6k(Fr*hcwjRr(GI-Y(;Tt%c|hd6&*y_wA{=O(@@$fjD~m?#4iz9Xpc2Ehj<!`(mR2sgmuI#Sgb1|`x7c}10~V>u(Q9YMFB}ghrMl{Nt6e4lTw7yxF(;l?2KNb+nio!vDn+{w=Z#?<t?w=x*Y14Biak-zFo8$PeL=?Bl2y@G)LPCJ`7>+z1$x_Z!Yc4esc_#dC}+JRYMR)LCWCMihH6!B0A>ZAb4JR!wNzG7h>SW6)CBBQ2Uu`4>%2a+Q`EQ3P#4~;kM|^{a#Lp<%GLrK67Bysj461mTb=dpEe&zn3f;tB?+5WE=EFsPmAHm?WnRc>T~_E(ZX2;Y&sJl(227@NwD*id2qobkN<3&Of|NI(Hkzi}Z*rofR%kg<YT>4&VC|sU*VwWE30C#s3!bQ@D3B5<9o<mvsEKa3Fj>MoLV86p)KMm4OA<}yJnmZ=A&nMU-PRp<2p6aWlpg!W`+A={6xA$#J*VwVF)m<@sCXc12y9b+{xks@Ci@~9U(<wzY$N3ul=kc^0)!GnGP<k{G>dEyko@DxG`o@x^=M#BSk9Dx!0T4`?)g<LnX`IC>Zl);_C<>BjBbAH@S*15spzD!v<t6RnkY~jIb`(%RGZ{YIqAmB4Zx%f!N*A}$m4`6`Ue(o@O#`GtAl0mk_5`+Ix}*TZbA~p0JMlrP3W1kI4gNKo`knKP#tytxSws3qpe<`j?wJ3oEc9NNwV>88D$!Bce*QP%?tT9*wUr$_qMNRE)!4?iPVbq_hmgSCqKTJ^D7K7@md74Q(fpGQe|&EPAYP<yQ~#r>WWlWJiTg_0fpo?4kn81$4XB=uS;-#f%|1_h`f+gqfEIdY!X7jYS1lL$gGv_X1^sLzOr(KQW!K0;55;jry&=tMWv3n#)ltG@r5kXm1+!ozAFV%(a0e`R9HiHTbV-Dv)y@}$Cb`|iHQR2TB>t0qx7iyjW&tZ>+8eo0ZDu}L3c`isBauXAdz-`R}CApK2C9nW|w-8>OjZL%f&2#4N)x35zoFEpvn&ZvUyi8Q<fs(vsy8Bq14H>g*-H`+kz{a#y6nOohpTX5q1<3)Vh^d5C)-o;%k&la>iEi(f3ZlP%MQ4c`INtz$sE?k24gb?=~awnYb1AtlFzIi=v!Td<jw|5^YLZn^Mj3)YQ7qy7uz8k|n6Ts~n~DX}?m6`E7~<-cul%TUx(%iHjLRW3%NWC_M<SXga@QwI-O|5xWU!VfqWdz>G`Z8H6Z=S<%<WDx|=@pxU~SQQN>%alFzYR#3O>J6DSS>k)%r|LaIZIIfO^o7obXesEHAfwg;OpSHq->nj*5V3szYqu9>`HQHTG%vTU?ibYgikDG;LX@?LK_^&a`HG}0MJ8|Rz=XDn`FzZv@sbCQsiy%(XOXaS~o2D)#U9U<L$;#N|^?=5gm|3d8KzoVYp>lZbo3jdhU}hlLW5_~>K-L>{jBO%j5kpo-Y~V6Omq)79%ZPJ`0|t|c1EqGZL+jL!Gr~AVW23{8Ka{hj+hi8^y5kI+1=|e7oX8}OVdQrx<$K5LO{hUJVYg^C9KX}^7p>oJ`{4rW1*`IHWLo>dIh|fZL1briU{*Qhb146vKq!u_ir}I8`Tqec+*BU')))
_PROXY=make_agent({0:_DEMO})
def top_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
top_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=top_style_proxy
