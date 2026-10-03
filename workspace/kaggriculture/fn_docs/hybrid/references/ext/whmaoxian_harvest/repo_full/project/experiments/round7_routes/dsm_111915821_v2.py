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

# Modified 2026-09-22: public DSM episode 111915821 action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode('c%0o`U2h#na{VuSo(GGPz23ZWC9Wl`Y#NjlVPhDEfou>U*gQCS3-aGXllRU?*Qs+()y$>60R-sclAP(TuCA^+b*lP@|GE0NpMUxL-+sCJrys7qzxnXt>c{Eo-+%tkfBmnAFCISr{pVl)<8S}{@cD<UKYjY^PdDGa`}XGj)pYgx?(^03;>YRf>+kRH-h6uf@!|W=Z*OlN{{QmFAOCmSJo?@1zkK?B^@qtzKHR>4zdYvg1#jQo-(HCiWNh=-AKu>HK8)byIJ7@~diVa#PY-kd`04R!^T<}CKK<?EL;07>%j56ysg4qRfAjhl3G9cf@9yqDzI~iG`t<qs!^bP}u58`nD9)2O{ld%5K%QPTtv)Qn7{q$ec>a8Q`)0dF<MP45oP}vFg*}|ptJW$rzA1`gns?d{SFdlPaDILDhhOJ8U447|{_eZ0>3WZVo?d~3FohLd4@6G&!`-Ki%E6f;ZA254(-<}J1zzE0|DAqDrgV}F+*uFL`|jgBz~Nnwt5=fMX+Eo!PhU`$)%YYhpU*cRZ|{ds>V+pshZmlofGojihgLIvdYrfQwj+qg$#7C3aXR0eW}+kz&0=^zl5bhk&U=E%_2g{43>vfb6UPlV{H!g^;Ym=c>FczON#{${I4s=(@;yHZy>GFl&m!0Ol9e%EWFG8XTdwmnm-mEE#Gsyk7oI-7N4~y$|Ni#%$DjUud;js>`*;7c9rAY4jteS34DWw)fA@W6tivZV52jV~(NBEB)%*v48#)}}FyL|wV<`C?VA&VZWDh3Ki!zT7Au<!b@%8q}NG|Euw>PKPKYj34%3C0yAj>|P-&+{&0nQv4!2F@<F@kBHeZnBP#t*nD?7Okon^1B6<#MircLSApIrvW5n82o*z0>|`*y;#g4_ukEmyEW9;}QqIX`Z5KWxdx>3oyuV^G0w!?UXC<-ejoJi)H5Lf_drlDsBlDbj5F?M(EgJ7Q{Sq;^TB4mv7a^(|{CqJeC9|y;XlE4^AGx6$h>fD`KEggD{?Nmv0|y`T@MiT$uGY!sbCwL+Tos62k+uV-?;oj~`3~e3czq+KRS(Iwt0Qn{L?-%5U^+u`33EB8vBCq8Wm8EC+P-8SsSmB7tDa?*%>_@Di_kex+%hn*xHEX*{)@$PC(sSA)y>;p6?y=Re)v-~ZJb-spt@Eh!0xzdoW85tK!i`0dU8Kf5|aN3cAI+fE>sS*>>s;Otneeo0}AgP$}3py;sW0JdT+`=}%HPn+-v5cK?E^JXBo!)6Txo4bUYmD{-jP#vSjG3QxDF}t)8NFjV!%>BW-NL~dNOhl>l<-jqHFK4>Z^1ZEBT)@AdrPzxiSUUO=9)J0SeYv$O(tq>(@f3R{3C!6ST@*KSLJCm_JH$aUqsUL7aR&={uy9w>cVYxTlODZH6&dV|X44lKYl<>E8m2i-5qe8V=Qjzg#Mh->6a%>(I~oVP3~3&E1Q>;Pxp!2FFgS~X#nVlnCtVbPiz4q&dO&*x6?a>V=|(SjaMLccfO!T!x&~`gi~O}+-n#?D0%f{f_!Q@l4F5b33EVOSJ3(6Gk1pr|qHqDPvz#j0p<#;A<7AWv9}#BzX<0$X&^Tx|I(~+k?R*2a1~GIjy(S7@ZSFlu0E(Le?u4?(2hk_c@)f-ESHCy!{8j3m&m2kQ+r%$RxIA)#7iHqKM(wCEj~q=kJ@9wt8f2*B9|Sh~jOKSll%t$+WYg%*eVS1{=820-=rrKWRrC#g3`$&|`i*;l5kjJ+vR?BcfhN?Z4;-p$ioscD(__C*j?obY+wE#bL7=S`B{7;ADTx4SurLmugcd4UaQEm$84h1LbAbY<_+lwY=e9rfol5T@fC79+XC4$gj6r~&h7QD$zz~}~k2eY@GkS$3x$e0^ef`9v^{49i&&XEq1F`Eq?2!obfdmqV%;mbWixyqfm5o@a$1#x;ji)NJ01ekQj@+=zC2zHk`cJ{J+u@xqKyBs<bAUb`-K}FMI!vp{N?NgF<-Bne9n|u<A=enpzwe_`HaBB*(5eo{GxOd|yyHg3#o*0=7y2j}EilMgiNI1c@>#u%4}oUTr`qHr5!`TxckLb^TJG>0FjS5iBEyFSdLTKH;JRd@rRh-_n$s)1gvS^qXN$arFBRK<1>PVEU~*~x_TFi*!AH2HT_+V1h?bKLat|%E6FXuZf&?ozF<;v_$0Ge3a0n-!d)*{94O-^sySs<~zEXVVFL96-;arLPc^rt+zMLO93r3!Si{ws1SLov)u9LDq#J_JsJ|Vgz^E*OMg%0BvDWLWTvneF)PaxcP!Jp|?Ffk$n%~LYE3u&{me1#nD#r++AU!L)yVGL2+RTyrYKQP*rK7_xBi0-`d-`w4OxJ{cVw0fz439a9PzocYUycqM}mqPj2^dsGNR41V1lZwx-w3WN>%Qu=ymI&Y?<^-8^uA{Nhp<+yUuI<#XYWMmM7}udo0q51o-Mwf1Xig+>EY}aW;xuEWS}i;V*&+yn>R3GHvz%UAuo3G7LIgdO=(wZqfW0B7g4LU<LbOSAcVdOs)N+2@XR-$VFePuXp)a4-I#wNNnU)o8LNq9GHPHD4R3p*|oP#OikmzU`cA~Eg``ZY`0fOTYiHfcN{1spRdQ+UZKFlxKOdwm=+&&*M;LQpSn?EMmPzNKq^2ZloKn6$Nrl*iH`#QxZWXqWY`|A+u3{1b2+O?28143k^<J~ITu!;6+m^x*q>YjZmF@(iMU5#|9&qkADmo*-Kx}lKZ(92KvG^8*{<XkjF?2fd+-m}1)K#79D!>eipmU1#*ZKkOTB^3Lxt>y6)PXw#rGn&%@gsNt?)?OG!|H<NyL~HocK|YPwNl&D)NdB`@f0ys%IOZVN08{~2WkxV(9htvL)&Hdue*v`gwr-dS!3@`f<TP#y0WI9pRF_^lSmBff!}=&d@hm_#OeiQ4g&lmMrBrbgxXW2^fT>4D^s&5wNp;yg2A}~{QAift0|bLkQzV!&_&fEj(drHnYMd!3nBb>GG>By}fw%@ms?cvv5g=rn$Kb5N9f^Zrar2r4ROoHn;?8ocn?gU05m@Ak<h%SZYzo2LRg6}zV<t+Dq7WOGP=(I}^6}3YerIR-*O@c*?YsAXdCXt(5M6Xw*c+gqWHJv%_Ie8kBCC316M2=5^HOm=&{3~cYZ|I4(L|1j>nq3hd^pV?Sj@0Lbhkl~*s9J1-%5eH2xWcrA_fG+_#~(Ju!q`e2ii1HFMqET9j~woYG^pgyB<JSVA_rsXj`I7$m*NbhF9W;xS2sbU62-{eJODPzXK>*kC6(-vo@$8eriK$C{ZV?cW|kp4Fg^m4`L+FhW<_a^EG6T0JqU{4B=n{<ON0rH3EcqoJ3G@7^BzBF8qjEx*jpjH8mq-FR#kROgZI#XA~b+;1M#ZJTm#fO-2Q0**kIQB2%#H`_qy<X7#eYU2&O3AjIkB2g80j)%0b;<8O_@V))lTRiYGWT>to}l?TSKg8pOj-T_5*9WaS-5X4jQFHo*|N|MgP2TAWw%k-VJpI{-o;f6dBo3~*!qYwJEXYj<Qbp_|45Slo@B5{td0DcP)XGr^xC$B677&|jR%=Z57VQ_!wM`xf$Afh$E{Z!e=PMoG85<m23=(c!IDPRLM8N_U&7nRJ~1ac{6;OQvMr8v$ZzF86eNg5`t+g<-%mR_(q%#&NdfVPa?1qsy6s~VTa2IBeFvR8}Fw37m!42v~))Br9%CTc>L_89jd3<JuU?aiO}_FZY0VN+gezOQyBV_41tVmWe5c#kJn8w-ZPYOMYkwTUF1@p`8b&=}BRL%Q;KS`jW3D2iDX>W5T)?Okxa)q5>dN@+}JjWX~bhO9JOEQ-lF)8Kn3?}C>#(24pui#sd`qpGhS00YflYTYvmv*bnf3Of)I+=ezdJ9O<Z&773#@MJ9iJ!TZ^v_G0!CKhk?6)sdV{?LTGy9HGAjX5@)e4=n<dAK;rk6weavlh;_+i<1!ms|qe*P^^I&sC>FYXzV;Zbcpcl$PdPhH7y*OyzJBHe8FB*wc`x6lfwqa<nP0ffPvW6iA7Yv4m3@X-<9BBbPW#${71ZOpA6wJ*0nGEwv4z0(R$fGy$FLH^QaS-GF$=xE%+$OCWi~4rT_=q9Nl%t2;<luGY4=6AXDp%}h?at^~=wD}Kzwf;^C1b(-BrB@|s<6v6|bVbH{c8kVP<00ZR)`YwPK6@(-(e9;YJWuoRFr!;OGKZKhnr9Nx~3k(s7=d+PA+pW}f9t+SJUV9N|TN-rm$WSP&_81;vH2o}Ri{s%VA_{O65^|A*UOjD*>GwE<s4O(J$ZE&+(FtT^E2>HaEj2{%zB#XNUP9jTs(0}0z)?On7FmZTV{jG&pHx53!B=U+sZ-OZaB}K_p|4Rz*r~}}IhLuB9!lIduI0d+hK1QZf&@1>2&APKLPud$NQF^cxo?g2i2?u-sGE-!(_vzIWicwbMx*tt9f#G+B-a8!DT~L*_YwguLNC4U-r1MJ(JQuJy#3~zQ$D*<Vq!uWq>*<qkT<;DS4u{eI6nq7Dx=$AQPA>qA8czjC5|qEk!tc=FhtKy_9zEiM#2Ipi@yLe>(d4-P|Ei#g}Nw|^%q<v2aQEhzfua21;HuSp1??ll2=(;1=#DXC{5};DdusDRKVJ%CAJP*pwHxrRt3iM1~X;7DH!^q-5I)JDadC!6($N(av?~lM?LxMqC&v*GQEGf0ao$K$GdNDKHlx`#bzG{Y7R721bYcMU73M<(#`w%!C2PI5?jC(FtFZ926<>_I&ec&z##+-oAdCV1`|LGPR0Fx6bR#kDXO#m1boPyFwlCDsnP=$D7F)sF{b;XRYRgu?uo19NAA#KcF6`gL7%0ub)B#ig#w#@AfIZH9h%)BTb57a6qg)HtA+e-YeT-zlKm1@C*fC-F|#T&z`TdLk8^k&#u(>A;{>?qR^H3vYVe9Ct2Q&e$}Fk`Cu6wu4NHA14rdGV`QmZ;FM#>fZr3QnKm0iiFUT>UrNm?!mBN95MA4NfU+Q8(AfxF)K-Y8^{3@61p9^@!TSQ2`JWR&R!U4BfhUvk%bfi}m)ufsz00$+1Jdmj}N1HiAQtz$gj`$miJ25^DK;6>Sz%dKYW^ojb3_28{(4E1WUWmgytw17!qouPd&kEw?^Ir@E@jR~beKauCX8sqBk|k2*ZUhU`6?(}KGSxtAfNYM{<TmiJpiqG>p<R~12`Y$6^Vefl5Z!SA8PzVblO`Bfg4u|nB&gB=hAII>?%0N;A*>8mGr>WZ2UxiC$WBOKW{Ztr$?cDu@*GG37LuQPfYLNNGu%$}y#S<@V1`H0oW`lC6vpl~C&BtPQuGU?oR%qU?JWi&^af_ZI5vpfP*e0ERiW|*h{KkhMTZH^9<jEW_>60G*1%gP$#mke07H|R7mskc&OwY7u7ws)9@a~XCFvg|wsI3MIF(%B&_TEc8fY*SMwJ(fSzkO+e7C{8cj>3sF-<YvfCFJ6Pv^15W2s8;*&sXDD{-u~^6~rUxv^v?%G1DuNY~$i=CaAEKkEC7)i)O)05KX(^t#yHs&;=+(ng+PVm@<;v~Bk<aVXsKV3gYQ2tX>b1p$miKE%(dfSNSZ7~1-wBP%~(&4wC1Z__45lNV88KdrE|Jr+>f*<<~cb#Whc3fUnyI>`l>LbBzf%COTAA!3}Y(o-7J`AVsW%4$WjUr#SUd4%6Zmu9nIysYT_-F68|FL3;#>JJs*zyjv-6q(wCBqK}H!gidDWnsB^Yaex;sIl4_xk*$-A2D}x+(%s&fF0Tcd_off%)SpwQ6mB992AxgV_Wm_FY@?}{^qgFBRXQnLBWs;eQ?Cz4@0~Z9j=_fH+z2M?PMfukoGw<r_9jIgt|mdTNLRsbONOzd%EZnDLA<z#iO?8YBx<|6>8woSTooW>L{~;zs2k~*y@EM{3TZ^x4nr5);p+x4M`$lcwj$<$AFC=K&I0jgregMz>8>+KWf?}5{_X$e>@grx>&^+PbvApP=dJw7%!LI+BW;B5rx_82C*xw3Iv^@Jx*fcP!FdafEz{C%6(+F<tDr;MYrg5P-R*vfotIG&JGIf2`yyTH#b$1$tea=@>T(w6_{wSfI%Ds8JJMQ0F*5Kc97yskOXQ9IWWA&4el7DN#Px=&X9ANR1Mu8oYn1l<5Vf&NwWRCze_kEQ84imkWdfL!Av0xqufbjhqSwz?@?JosvtgkW@Gld%AAKPsW+6aB6lr#)gi!_s(u76CU5g#fqzvBSyFZr_ZoNpE5VGxcB9pttF<LnvOt2eaLC|VNrcQzp7hBBl1=KOVl=m@^6v2=JOm2N44U-hJOL8~;#lCyT43!pX%Kzv*i1+z<5!b^CZN*me$IXt=^6>K5bA#Sj;4AQA-36sEVfLRZ;huIB)}L2t;tAJ+4qzXl+A-9HS5qk6!$Dw4*5NP3~k7g6Io*cN&&0^H(vSI8j*OE$Fr4sU4rJrI@*9EL9u@Xr$^!Ja8IWx;R4?Uq`W<T&o%zC!1akmTcFz>X}c*aoP<*{dZ&ylPb;)^vz(nJS}?V$9@^+3#}W*HKGP&4Sxg`3N(HElOd-8a#X3url&SD*`5n^mG7G;^8|eZ+r2&uigL^{m26PDlDJwck@lF!Iw^c#n(SJ&!O;_t3ZggHtvz`x&V<zlujZtSR`t<0c;ccl0nh3Qauf7LB)^g&LuY)XF^#Pv>EGOzqzzd#55Cn!a1Jt2OhFeqHh!78$ZnQmMi}5ZEnw-Sx2Rk53+CPs*;kfb=?cTBHNekdBv>p+3H9pgZZ$-<Lle@51TRvNTMU));A+t!qq6lf%Ce;2y(AveY1|bpLgb`bI(Vf^F!9D=Xz_6ioujgx6?0A&8BwX2@7VlWr$MLRcZ792>VnR-NuIHN_;Vi$&qG3oqYj`v|%SBk~spZZVmkM{Zf@L|8ih`{^e~mXPY##xms<5y%LtmoKJPRzvE|2Q5i40>7kIBF;St-CmB0Au@EDDJLwh+Cn8OD7vZ(m003UCy;%9pc;lI9csr3>+oJFFo)y6u5cuA7NhS^^_>)||8j!s+~Wd*_j2AgxZRM8q$a<E-cyM(k)y9rpm>SvVebjV={7{1L1my9+$y9g_+>2*_EyzxCCCExuM%ecp?Qx>g4?H}_yG5ECg=6y_OQJ!5P<yV9)gJG=Fxxb?D=Ce3D}4*|DA6B0Q>3kCmx20E5yAq|#^uNFoHE*d*4v!h-+@vc~v-QJ=aa;qOO_ZgRov1-8TH_@<i*_|@ms$Y(Yo2dj2TV#t$W~2XVBxs?Qo{zxN&&ypROy;?yr14A)Poc%i$swgE4g2J*TaDMH$h%`8WguRX{X{xl(r#C<6;g}M$Lenrk!j!vV149Tf{v1ShaS@%_gqHvgS#O2%)59Pr^m8DfH~GI=eRo3<PpttEUFZoiP!R=&qMvg?h-QxHG1(|w=wD=NLIgUz7Zpaw2_OL^8RK;pm2%tIs|+7pw2~h^%<{f0+DqZM&^Uh!R8&I^Kp%fzye0x%Y1GrhCnni8+u`B4p6+-iH<7?al4z2L?5L~y`xBr+-Q~^LlcWc;Ngt-Iy=>hV2fYe!dmk1n~czrd0;yuShoZ|C>23T+c*W@*vQj;UaVtNRNb~3omOLh*y>wJnqtM8&S&1+p7M;TB#UJ@somm20j1bpB6v!pKIaSt&O5IhR9yeGX@o7u=50^3T@FB0(j_J~0WVg4@HB=sxdd^s2_BL$ST2r}#dQ)ihqMvw_Jn6dQ3l*3bvp?SE2HL+d`g5v98PF-_d7c`=euqmooPPZH^O?B_W;E;2r%LMA~dA03085S<LWc7gR+2}0<MY@Gk?KjaY-6Xtz~m)5A?#htrw_ErqJ9oahoxrKhJ3xYu43yrh%b!8C2(D*O5I_L!prBqAEWPSBHIgdwctR@w&0o-+<yx-cx8h#r2!<mu9OWRHamac;dTD{<CNrB<cq%L?Ie3UJC4it_AB9UJ6(Sueb#5kQ?1_XAdAhhAiwa&>;z2KROilR)RJMhKljPg5(!bxWNc-hZ262HSiM0$pul}R_gv$VxW1jN{Z`)m~1!&Y;%N(x3ih^lW*RAlWbLK2_OHoq^}X|0zJ`SJu~kY>oeJg+rXp=ap6gRcb>uIqTwHj9zsgSIW$?dtJ<U;CM_X}%9>Y%=QOS{5XKM@dEBn#TDS=tHw(t+!JIc|FW^oXDeW%Y;t;37Huzz=$-0Qk3y96~qVaaXY;u&o1vFliM&lTuj1cCPsasP3CknEH;Iz$7u*!WbU`NE$91U7-MidX9H_iEf7)u|rAt325v@DB+iwwKOUmbzZp59HNDMWG#V;AIQhiTSrG?W0q3N_B#HTL<WDazy2aIq2r!3g($jR`-+cJ^O9w#g)>_h>z1x9AH}cCHhZl9Zhk^b%7(nzFOv(o8VQrM5md$R=l}5Gi;yKw_)srCiqVdPohcyHfM3<XQ@R90;h(MYRb!B^<;QMjhoL89Ez*VC8`FA$_tA*}tG>S+pLiL=A$q)2(Ub9d;%eQ>f~eBGzL!tY)5_-OgAbunmIF`rtkn4VQYB0?Lk&ciwz5E(~XUFS|4<hnGQAmSuH$391`j&<zW{R^Ur_IE~gdN$7w+g1{lV@G5@!@^c)Bi3+El_QyEK?sb>oG7P0Ko8TI|!o4DZ#c>h+(k-Z1ajHvbS{O8Pu&xQ804`0@_arAEJ-gWI(oImk4tIJv1_h#gUgY+q@#}uJTk7UCL>e-nyWTEMI2rhX0DkSfWDaRB34){s!9xIZB~a8t*D*~jIfZ?|^01;Y!#9i3nS%tBhRAc-5Pc?nU(3bP=PTx=>e7*8yB!UDl&4SlBys%{7K9*`&3TpF62@$#qKJVy1nx~2AfnJD`yal5>qx3k5kq{^>Msk!w}?AYj|D-8a>isg4%)+KcS~3Do+))P32}kv@OQ+Bh5RS_<c9%<3(>jk%f+g2!c>IlU>)2RJ(Ke7Sr438;lq#|)<(u^W?|!0yKewf+oseM$_?>h&Tq$-sW?08=O~0g`;2sA>+rVWZV-W%-}Yap%d#e*t$ky+_rYo;PzkJYwofQpwH&W{9X5%7iG9K_Z+5W|_&rokyZqnh!04`V&b@F+yoH)`S||QtCk?O&D!2eSaFjyGiXx=Yt2v!4JeKD5Jk+s)NowVML;Dm@QZvgd9bgugS25-AYI*OC4^Op&v6%s!MFAHSgY$gBic`e3oDy2HiYgRBFbI-RT*gJ}9?_JA&vv6-Fk8p}b8a8-S?8@rNoM)5Oa4DS!%|xE`WxO2--Er4&gRwy+s!-%a1%|~6HPwlS%&MomPtg^$WMgfkX|QHNpT-F@;OQrirN^)tQ6r87-+JoG8g3wkq*gg^<85dTk$+273g|1;1b2dWkl?`Q+_B7yaaQILIlWagp=l($wQ?;2Ac@4c}nSMQ89dU{583lrC<FT0@B0BV?;14y|x-hIQPiW>0Q`F9i?Iwn9*klh?WYOQ9drW^StPH7?ot5z%1HvS72EAN79EGIGUlVUZWjyCvtjH?lvb`zN}(iE-g2vr6ej-Qj4e!Ptx&cB@zQ}c%u(=8bKKyTS=C;#4k5sVxpUw_q$P$K>Hb2ug*JVS!%Z7cwZPBozw=A4zN?Kj0aLHfbG&NC>4bTcyX_Z9`Fr%nr)<ErDAFX!N$v=Ck8b-$GJz|qSdN$ZW<RY`E;4CB@le^IzsdpC3i^W8X0{C3rlc8rA=OIZ1rMO0hwWq0NYYYWju9Q(r8nobuQ$4wfZhcVlswGEG~!uli;;Z@O~~AMH{`i9E<^A5}JFMQ5my2OZNAH+L(|7ycXTL<;y^Dyp7hT{t)6CkE2|8<|vL2g;omLa2ASQjMvlbt&Aym9G+$MASJ{FEV>VW6;p(sM_%`u>+}TPkWe%dZF#(<T|ff;^+3*<J(9C55X^W^aPC1j9YU%obv9X}&S}cq@p;=jAC(f}6FaiUc$CK22)$CqDTK|F3M!HmByu&txe*T+-BvSMEw%(CEmv%F93g-dGXY;UbEQ-b5`SF=Yd&)#Sz`R++|;mY&k0Yr0Z{sMg9P^jo6nA&SQu&(getwAT>F&B*EqSlydWTO!PRB8#+160;)fm^t4n;F^_s;^)gC5(Uf;IRggL~aCrsEQ_zG_b$l{dRZ48t<L=<Em7Afxovl$k;Ox>dQg9F%}pc72!Ca=8D<s(H+NP%+@jPUGCyeR47BjJ&5-qd7!XU+@vk4cjsfU2a|E(LbN3HRZ>;!F8?81OSqWGt+HGawryI<T4Z^p8jFku_oafT2SOJ=$$Kg4}a`@%BHQ#KRz^--N?+KGJsAgY9ALAR`nZ3w958g(XJ#I^Cec29JP^q}|l~60t_eU%h8sXdmwf1P;mEFUUi{><smLR5KM5Bz{W4^Kqf$8qe&{mZNw*1}{6p@6lCr+KG~zy-1;pNJx_SyWi@UsJQ@u!Au6kq)lJ4_>~X=Dj}Z6Yn1Y*JzD~u2JHh>ltNieFpg!7q>3%EdJ!w-xA79l?J}}nB7|E|HccQ6?;m%C!c_?mf~9ek3#<Y3K-8S5u7Uk6*gQ4LZO(oh-sF4GD7Ni2g%bc2+SNdW9F&qFHl925nhwJU8M;hY4B<d$`{raqgwIWxGuVpY{1|bRxY_ZK-z<^DL<N(bupt(^GNY9&i!P3XMu`ejQf`p;7Dy}-!_!hCk|6P%VU_i-aR^G*GMlY}HUbzaS~wnZOa7mLHZV(l0CMc<3FWy!cOeYZqC>!^Apuxl08HD-n?o13Q*4o>R~wtcvd6$kxCmy6*>2Yup?$8)jdrs`hA^yDAi1gpR@1Ch`*c`V?09~fS!fVug076RL~jsLPLxIp-K9%;7J2_6kVEZO7eTslG|+nUkb*3=c|@MrPicEuFS{-C&aR0_w8Ej%;X>4VWKKk(o=07$wJxqlZG;O^)A@==+LY%Z$yB>@?COixv@x}5>+n~5dysVk5zv|#&-|pLw_NTxLZ#N>(>TvMH^=6KN3Mw5?uu83_;I>1b`pWx1m76OCLwtCGNLuWc@(N@K$r{=Ok1%^<uNdWB;KW$PxAabKWf<a3?_MMLu#}awl*%XNodBZt05l%n!{VpO$Skk&oa=74k+h>R$DL!j<ydcYLRjs5Wp0da_Q#9MyWYMRJ0-X86Ax}TPP!HXCu|w%q+|{SS&TN&<2*VmW^ZfnH5)lcOnO(YYY4`&Tls@=o~vv|Gzjv2KPkK>Yj-NMA5m8n^7zkJDA`DdYjukrQbu@nAc7vU4{}9a2N5%V--y}mMsl)j29`V+E;t8dPk80_JT*g!du05DiSH6tk16b@fZtCvX%FvTF_xsq~Dt=GDmE$l+ziC$Z)@~E32BRw08jqmRIa`B!`F8YOI3T*oW4mAeGdE6PNtV4lw)hkBLvfAp;WbK|Cf_Wx!Ax(*9udSSswPYCOOfP*ZAg%ZUP2Y5Z6@l^E$jT4)*xGK)#GB<p!T;y*N+d<<)P^)rPITUG8Ydd4{EI{65K$AGesfMmsE+W^2-Spe6)&`etrASpJ5GZiUMpuANW1IeyoO2XmMQ_cB4wQ~#Da8f>y9F^-2V4~U$1A8w!s^O{bcHQ8mgI+D9Q6MHkSDiHg#sgSRlU!vmNC;<V&E(H$JOgQ?P)Lb4@)Cldy9!ASB({~#|7&+%zsrKLi?$95cMlv|7e-qv6?h3?`)^^QuZTrpbyV^I<oM9IfdWqk1ki%BK$;j0E7d`g3SAa=cTZuZJ1pHGU9v{p9CC=UcBf5r$pfwm`C0A;Mw5*WsmA8g(74$WH>x@~>VQr}=Qt}-Q`zil;o4D`GikP+ixQ&)&W@8rIYXfugK;`y=_k*$ZkI5W+#JF4QR{>C-(t~NEmbERC4z+up=`HiL&ZkCw8<H*hm2Uc{V<~>Hl^$YhWnVaEKjLx5PW1_t*9o>F;a{Q&CyiNMP*h)#lN9x3Xkp&;6d046pChvRAa%n0^yP%aH<W@kT%YG)T4z~iSb#m$V}8M1|kw?`qH4J#TUc|W4^EFm5izgv6v{K&;f(&g+6(P(!csUW4p*~4X5f*+AtA#+A%neJVPL?USa%hRceCd$po%Ng1X|A`9jy3)GkCsEiEsj@{dHLbxBwN7j|}w%;pSwSo5M-@>4$Dug2+azF8l*4iZ(Y8T$gf>SB--uOov%Mg_B?`ChB23_+jA6q?0DBw`#AsL?g!+lQ00nw6T>qfnF`p!WQk>dJh!5<cf}U!P7v7NrMDOa}~DfoTv1g5gw$lT!z(Y=o0BofH+?fIXvYRwH$TvrxK&JdK7tvf#|<Vg*uOAuEM=IOQ;Kb;xDsBbYndxtCr<OoSPn5<F`C#l1>O;I&gvmbBr7zi;+d+SQ>J#F>RYC((g498&inS$UVzGJ!qrS4aqLWN|=kcl!iFiF>I((x83|TD95N$d`!0MFg594FVW=*8Y!sJgScn>8`8Go5g;cT^>9L*!Jc8C$twaF&l|*Mh{JT*a6LuL?x%)dExr)TE>Uc84~bfgK$Q+X9)nNj&7Z933W_m1(A}WHrHhPyS3ae<4QS@o}1r<J_Ry8i7KkBjifda;N){yawic$kZa&js<?z|yS)95bsds6)a7MC3<+J0mUSP>a25k<Vx@`ms%1cCZ8g)I0H9FRm2Yxpz%Edp?Zp}qg_^G{F~Z>?8K$jtwRVratozetdbN&3s;`g1&Z;0|DSxR~Jfqy}{XO#|>qfg;q@1Q(bz(*?wQ<^wl7X}2kQy9nH1*u;C=n~&gR#FNJy1-zqY6z;Ca|xDT#D6rDnIDsx*AZSp=B+zohe_V_<$BDGsDdz1?$L9)({aJ^va7;|GE;;G8KV~7ZAbP%A*L-zbL>j9_=*o;6~gI9`ZD+a%p)FP$wjX_z)gB3X4RC6q_?u<FHk3T2Ry*^vQ;Ojh;X;%5siQ1tEDdh7r%)O0^o`d+l9T+|Gz0fyoe4>&O?lz0en+WlIUBOw@oBz+_Qk@MoaFWuXrvjitON>r@a~YNG+myyCIP4n)3NBsXYsnB@n*HjfXUp_KAigI>YA3)$o}RN=f0RH=nbKqzUdT^0wyMw_`%VaKsTYt#n%1mLvTFB_Z!k!l|I_ay)f;9%5br(&Dj^EFP7^4QN{#g>sY89zW>dz@K-AC_2%EWq?@Mp5h*cDB=Tiyj_qtZHjDdE}myyFoHMAS5}#?rTtSGo&YkJxP}DWvBLTvI*n~7%nnnPWz0d+JR_{s|YMmU8%VidX0hc5dmGjDUN+d7198|;Q@&8N5$<gbA^mmVIw#TTkvB!H&Hlm^_6{cvcC8tu=c5+MYWFy;2;ignjIqIZ*$1(R)mU6>_xe~F_LJ->~_JU+4BIuG{nm434jQR-_1wt_AWwcP$S<Nr$J&v02#!2rS+u5h6aUT(xp5U^lS5o;*6fY*)7~5>DHNxvUZ-Y;%dt)OIzSI%fKo|9y%H~*Yo}JTLR3Abph|Cv=KzOs*J8s7UG!6XbIy7R&yJX7C+KN6(>%`&#w#g<NpC8eZ1`')))
# The generic dead-stock heuristic considers future SALES only. It does not
# preserve wheat/fertilizer required by PICKUP/FEED/FERTILIZE, so it must be
# disabled for a new production route whose input contracts are not modeled.
_DEMO_IMPL = make_agent({0: _DEMO_TAPE}, dead_stock=False)
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
