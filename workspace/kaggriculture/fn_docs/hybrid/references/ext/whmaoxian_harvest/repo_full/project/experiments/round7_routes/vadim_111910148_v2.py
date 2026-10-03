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

# Modified 2026-09-22: public Vadim Vasilenko episode 111910148 action data.
# This is an imitation experiment, not the author's private decision algorithm.
import base64, zlib, json
_DEMO_TAPE = json.loads(zlib.decompress(base64.b85decode('c%1EB%Z_AMZv2;8=c1pI>|Lq5Mruq+CG=w&V?huEcnkx^cp-ad_}^Wss?7UfFe1ovvRZP_suQ=f@}39DLk5F9KmO0fzy0#--~aaO#XtXe@x$f2cNae$F8=+O|NPhgx_xl_@$bL<`X7J$@7vEmUVQ!GuRmXY|K_{P>x;w1tDBD(ho?Us?jQf~_U846SMP71fBg39^7h}CKmGK-hs{sFdG+THKdk;RdC9x0>+9ub?q2Zio3~dN;sY7m>G8X7udZ%K@O(eCuRpxGe*N?9+~0q=`?b@^R-=CS+q)m-50{t6@A0YbSM2)o)fHN>A1}VYdHep`yLqEeAFtlMzYy=r_AQR$IEjZZJl_oD{#A$7hh-SMWt}vhKV4nD-tN(U``}=Xi)n6!J)DPEtwm=4rnnS`lcxQ6@#-=z&Tp@N_uD)V7vEi7-+X^@cs8;?_pd;Ua0olN9*CUkyPFRik%Kcu(ugJ~r?HpBr+9}K{d@R7GNp%=ftq#ud*8o54RH6ayWJx{yf>t$`P{C@<@>9*{0-&BidzHiLiXnLeGe;rl0Gqv{e+;QI1OU2rIto+2Nq75<F9Y^G2h4Vf5#{HFOVw}&1Km5)r9j;<@dxL2S$(Rc5^bj<%tXCJh8os{mGq30XjK1BRKzVM6qKhqf+ziHOF5-ud((an61&}jPF3p+I%ls)zfb-XHWP<?DFxu@DMwl$;+dwOK~W^y1Bl-diDP2KV7|j|K|G5zibD*owDP{$`8BuzkYl3gSPzoBxIs>@*jv}xtjmZX@_1*I6C+`hB1^J7qIEe(qunOelM>1;$dywI_KB+Zq2jpFQav-K1TYN?VGn<KwS1pv;H6qfbRpYl=Z>g3lkW9DVSRNF0gm(+r@3Dd&o!WJ2{)DC+53TPtTSN;4`2_TFx!Fg!8s8EXgdZc>3kt6Q=5hf4mc4=V!q=nF)aPb1|e%eq?aY>}T@;#qjvm&tXqbpBnLp7k@+x6IoXe#nGBJuun{P@^RMI?<CvctkAw&#noz}h!|JYn2YCy<&l81-4UzE9JKWl5p=-gN6J|mVY<<$e8Xw{U?SjA7T+4jRmb~c%S?mG0-~l~T?s4oG62vJzyGAK4A4<w^uzfbBuxbYdUe29D9U6E>S4yh9elP~93l<_%ab^k3L;JY(ei2;4&%G`Z!bT7ef9S3Uu&QhIAYM!J<_nE6BdT>+aYoJ_AkfrpFXF%N{0~j51kR2Z%8bl^Kx+X18<qVTv|Hfs{lh1-vF1l;IJ*fz23CkQCzK8b5X5RGY(*tQV~|7_;#RRWSOx;cDDC}RnH%vYhjpozkHI2AbCSnA>a{fN7$MJUOR-E${A76ba4oPg{0D4NHm|rxtA6gcvve3#B#9ZK~ux=08~8`K;)jmRS?To%);`Lz~q^py%V&s%&u~+J0XmXUjrX;3Ev8_Lv%|s@Hg9J8lu+xnG$k~)CrheeH1%#5SK{?5kN%k$cCRi+JDdX3awrXgrYEygw&T|tUU#|D5Fj}8tCqXc!7^nbp|G)Z6NV&7arI;M#~uYKEaV4A>kOyPx3yUI1g}#!s66mUz*58iDPYKE&LxH7ctzJwUTig=}OKMsp?t)cW_9k7@kal^nD0hI#lBnV|H_Yq?a6`^jF~d(}+HRt4<A*5r0HG{Ft6P$fLy20lOKiiK9P>4@>Se@aVYz+>sabJJf^L6qY=(z}L|Cj^o(~0488Pm;b!~{)hwKb@~%Wu?g!Fv$%H!fG<`%5c3$--A2#HW<DiyEyDWB%|(+F`w4v3Wp#@iO4%-ZXee<uq8b*w0LW^^If%FbYgc_aF{|=LNmOXUUU&i}?0LoSX0C1ycZp-$e|>Zrgb$QjxsqRkBQfsx6<uuhQtI#(phX=Ln?Y3Nod$dg(jM$Y9Z#gQH;;IKacUs9HSqh)1#d8<DAbJheF}iS-O6zfRde88WYU|fSZQ0pvFmujFD!4)ED57HU--|Sg9;pN3q;nyeC9|uJ>WP8i9Uii`>f(<yyLkCT(Z55E&23pflmLocl=AcVqn=o{CGBHM!tqc5%kFQ4i3Qd)tnBn&3mElAt9)`(oA3XCM(H45c;KpQgimRlbAX}^_iP){%)UvaUIjK6cS2o;Kb>2yn&o$HJ3sPl!2LbofvB0$6g`|5AeK5xkQH$ox02L4PC#Pa5m6;1qNQ2Czu|R%0^~k*awwf=@KYHd>c{+dC4_Bbz7QgP^6gy=6FVttG$k(_lP5Y+a~*Iz-J$CZf^hiLXnT3J`u;xLW{PK#CafQbm1gTWm&q1Rp(5quwI9I9OhPkUmJv-(>p@LgJ==;xr!uEqh{F@nibAl=;`1#TLDxb)UzaGj5w`Ks51b5!~p$#2?XaDG*x0Z!=FS5Fm8|(!`K3287^o9(qCEF%fu#qZJO68Jy|4ya2ToWAFJqB*`0n%9yle=JUyU{MLSgjJTWB7Kypa!{XP{*c4AJ;1?tQLl|$0EX-i{dRZ_q{8)OV><Eq9d@!X4B7TqXl_Qn^!lo}xcC0c)=<VJgmR7V<Y3*=Q3ler8SrBDU%^2mEZ06AK<vmOG7Z3@|}PdeEsKPPPhj&|0%WIa#PUQAQFmrQUdG>qC133|xn?*6W9oZ?AMHaXIX8#(7}Bp6!QO`MVo;@81AX@9t03nXy<#i20fCHfZG*m5?L)=lIz%mXlug#^u4Db66fw@kzztR#y>?F(rWXbH{Y55VOT+zIv{6xPr{iJd&6!G7|3hN`$33!@>OU)e0j9#Qzc4wViAqmzuL<x4<D&q`v3qFdqkB&Y#0Sr2)um=NHrpe}Wgo^L0H{?}!FX@lX2JM&}}T4wAaa*KU3o4Xw(<p*?ciIvgvgF}sV`mm}mRG-}Z)QwJFL{zaCnsDrNB&wI2K>>zLfGUoN5MhldpqLb(vrf%O0*YZY^vJwq(aGG{(M?BnQN&3OAtXyaE|85BLV1~+%|=DJ+*!=fSV-_{uljN6m8(W2OatMluvBQwDuLyUz*-}qBfYD^QpI%<Z6Ds>e0TZ&rj0}9xRAGxV;obmFJL<wY)LE5rACVK5V`Bri^F+B1G@KYu!{NY1F00daTb*+rjB^&Qjtb7Y6ulpDafzm%;0cSGP6zDSDB~u-J9z_-{mG%4Ha(Ah#tzg-44(nR_QcG*^DjtC9FP;HG=dUufbRzSl;NB!rBc&*2PEpM7|+7gDURCRtcwZWuspYxQ=r}aJxg9f-_EJ1=oBNddW&xELRQ4U@Gp>=crH#xam#nfg4$OJSs^9iHJHl59$?6Gy0KG!gku3XlRfwAme=CtqxlKSC`GgD;C2HV5H0hp&kv%6tk|C)HJpgBEc#eypLy=Iv4bP=b1Zsi)D<k^8r$I$jw6*6?87iRvzfg3+)OoMkl6WR^ue%<K?A9?C1OLQCnn&15-7KqBG$x4;Y>D5xT}3of@jTxr_r-Sg-P9ti0*|(d_6=9h5fp6c!#gV_|Yfn;i*9VTkM9DPTF2U}|XFXq3K470LQnP!|G=5vl<zttZ<n9U-GM8~z{R{8ZvE!{i_42I_mLy2sN8q(<J$1S>;Mhkd@2eG_#EWMtqvZNl2@-ZrVm&J-+tI1b^Sv;6{VhL;0Kssf-oGe7+_6vBY#b-1ShGcIt9;X%VHICkeMpySXD;KSyhvwrX_)xi&|cnX=729;d8e_jH&Mxan7JImcs3X82}Y0m>|fGSfc-w~LIxm=Kj2J622B}X5%)nhncbp4fMsJt&pMA^e(jl^n^5pF^>(K;1KHS1JW<~VZ!oj}us1%Sj?GHQ=d?U@e^c>AODi<PlNtHH`suxYc7!H%O1$;Sx#kZG!@ezC!hw1iyqMs|?IpU5{ZR6WB&lDT?Bt|>M<zAynT2X-yZH>x9OB=5;3+@K!zQ%GOX>?y8)jfbsbP^k%=&f5__0}`iQ0J2~42qs1F@pSMXVA#nI)p|A68k<XG?O}D46qPLBxZ2Q!CzUc9>Bo?(TNMTtJ4SDmxDO7-9Cn%j*H!LZUI~TeH)+HfFSW6#CLx1=j~rJMxEULN<H?<+I445`a2GZdjpx{Z-t<3r9=_aKW!{X;Dxer#kRD?rZSAEVwLg(``}2HPL!$>~17p$>c-O^Q8qnB_8bDl2XaGNyUEmxY2Zz5_0zVLi9%X6qd~i+?dO_v3ZUbx+kReb$K84MA0DwNp&b>hLNjhV_qERn!r&A<GDEd)!T@sKef(8&NmLtIu1TQ8lHf?Ei86-vRC)97518Cy{i&Gp5+VPshCr_RnO=&k0hAESX+(T**$bO^qaTQylpTo&!q)@1JgvbAPuNaa58p-V~NH2$R5GQGi!@7Ik2p<#%8YNhrQ@Dspm%|}VIJdCxJ#-}U5gXxCMTI+*Wdn^eFc=JOt_y>RivyTKoGd9ssK-!@mU!`77aSv{(vo5VV(Tc!7WoKS_9lIU$gG-2$vFdjKgN4|kiajt3s7T+O_5@>)aaRq)G#j^d`;g`v~5JB;W)<KgcxI7@?^6~!Ia3kaGYbNM00Qviffz%@BhMLr*Xy|5YS4qsogZPzAs?tDMzAjd4T`WkvlejV5+RIk8c#195n-+1<fO=c!*TWUd#e5#s%YPAv8%cU5ACdfM*5Ja9go75hFuI8wlp}ALiiD7B4KLV%e20<M3z<aA$&p0vH{I&<NrOm`kiTPMV(>0F#;s-}*SS0TTc}>_E>Nqy$#RkA`)TH+a-z*VfjUmLB6|tl=ULLrTEMjsbVvSApKqO54oY-c{7P4!Dh^0KJ3}ANT{tK*;Kp2q^T;&CR<jA0z0XCNc6~zf}G?I>Z5gEonzupAXVj1$MG(3TY=Om?WiDM)+CNi)b5@We4aBYXnmaX46;?1PfM65Adak*se>=BWpR+nhshlyOM3mo3Cy-vWQ$%R;Aq33kM5yVw<~AbFJ?D$SI_myzW#3xF0x$K!}-?g{coSkvpagIDJ5vN%TwIu-{b*l0V>h2NDpPIcd-eA4YnSIEZ})`|6KZq#A^r>z1Q4G(at^%dO#mQ2+;}IB}n7**ISJwFS`dUuE(*g&elh<MrEJ-V(!x?Be9A*i!}o4>Sy(B*NylzIh}%#XAejTreK#=YKkZD24-(4H7i3Zm_@+V+~^*BnV;W<S!&1rf{DI9c){z_r>Nw)zpeQ05tNDB4u@eZyRi~9DISn&+;a+A}Ubb$W`wON;(BFrw=e!!bw7;m`jso^7f#9CoJ2+Aa!fICuIFYkFO@oXKxZRuzs&41FMqw8pZ!u=M|o0g}%6nB2GmE?X8gBv{>n=QG?ooX_BY!QRfC4BEQ^t00AQeTss*EL3#k{GfObTHwCNCa3#~b8mR_3m?%<?hbe*xyQq(Pwn`pWPW6nv@iP)$pASoM7}%F+P6Zy@MnHa#7}y#n3#S^@{60)Z^))UmtLwu-DKV4tv<F0~@f3*XpblUYlkP}EIrMIu3Xnu9^e0mtqpY}e+U#T`FCh=c8(UX{c`UJZRh@zU0OY>{so?E`rll45;{}mGl_-uSreyom1IQaO2iXE!&FARX8P;`_yK1Ef9&4ryJQ>M5Q(oDU66-N5VggQWAVav;2F!IPk7<3S+a0U|@SMA*F^_XQ)F8Xbe~5VgdAt#MPT`VXbIJrN0X{8rbN#kMR<AHhY$AbRmhL~eAyEGRBzAv%&XW(R0WZu7Ldl$>qA>PTgp{<gN<BsrMT9Gn2<~A=cAU6cNK8vk8M&(?3N>P{VW)(-WOAcv>7)!@_uJ06@Ys<WrCAUOh!Uo#gT5z7DHS`JJv1A?fOYOM`!Ff4k*%IWv#@z_mQK(P6slfwV&#+~=peiY8%$Ppu{Q;e7Z7%E_;@bS-)q=^nm9Mo01fhM1)r!)g^>@fK2II2!7HJB5T>s(OExBBXk0K2XL4oep1Sot=9C0s2KU;e@i-%orrBn;cl;1C=ZUh$gl5w^UTGmT*yp*(1qI?1{(|%==g=XTqIvA#lpHr^lwOAH3Kg@_<)%IKNG=HtIXiBMVti>xItK4yEW?Ed^tFKC6Enib)er_K6m1K$JL&(G03JUPB>6s1pRIm({l2^BkIjbK0~=r7$@T8x7wJP<dbJa76D!)RRb`e0%;UI`;08n;E!PS%rFa@DA6TCq+7O6ZA02YnAgvxS6uS<ruIA!-BtmZ@q7~>@DunYY<seE36Dx`=qhfH!pRuFuU<!CB&Fl1Aowi#}`iO$4YaV#+@;Li_=}?8XI8Au~gh0KEv?Om;EmTn*7UrRfodzu>M%J`2j%x}@ANcXV55ZPq_VKo5(Uc@9VxM#3<-jRnW+h)U;50R2u%B+}5d7~>X*I!Y$rGalW@FEL)o+Ys<<q<*Es-(eijvM7)e#<7zcHm}3VP%zCZIBrSL;!Y9NH0GJ+xsYk7Aq>S(vC9G3Q*UD6ge51df1}$%X;kmSsA@+WUp4{QZf2#NqjH5g9>;P}av^Wb0FTyr5Z6MzqPqT%1Z?cv_PU7bvXZT9nh6tuZgrkQtp88_s9QG3<>)L^?G>9qt2$LFV;Yw>W)B^I6&44hqU?WXyR-?Mi5?D6Nv{61~+mRiI2x6uZCx9~Qc$Wl>4RTcQZ;-n|r#%FFK<Le4;G9_g1RL~rDSg=_IceP7`Z?*rwUh02STB4Z;@pz*f4wwEhoW9PELW)r5tRu{Y7kxub&b=e8Z(UA38T2OjyzJA0&pI5jNEul``?5<)8C4nVwq`BwhwqmwPivwN;pn7G~-|kWC;;uH86y45~I?#idpxqON=3+8x0S-kv(p&Es&GV5ep<M?s1w{kkOuj8fVO7R*odDrTQz3E8imQ(%G6>+XR+QlXFpp`dKB@q`@aB^sP0oNNJOMXGTBo~@Vt$y*R1E&r3cxm84#A7bi!KFMPW4<ov;j6vuLlax=w=p4@4VQXC@*uF?vz}JE%f}3{a9moQ)b9LkUd(oi<#3+#(J7Fs&5y#_B@eOwpf?F(&Vm!6Tu7<wnbEhCQ-;KF#9xZlPpe<(?1F6gV);jUY^%np%snc6S0KQ9Q+Fht%tPMjJdU(EF>%sLwt2v8DMCP@`VyNDu;^-!;KM`#{z<NvXR2z1sZI8B2R7?jsgD9G6&dHs)z-VdWcH#mdD~*IH~!;;}?GVO^X+>erm~3gE9hE=2>!d8MduLYVzZLf;kBrq?Shaq2XW~^{m-F11#{X0!u7~R}O&eMrtm9l*6&L^kan|1%!0Dc+a^pCr)r`QaTECH1a4=fpX3(<96Ky6RUF=h_cwV4ocz*(Cq<*TBWSDkRH)jMCzy;R+lA-vc^!1LIXissI!B-XP`=M=*@|Q35-BUC?2%bZ+Wfw0FC&N{$zhXrgBGvg__ltVsj7=WYm^~Cq%Ka=jIMVv!wxHj@Q3_^G*8w)RCN_P`U?>1cMk=cT@-qunILrym~<J;F3R-!(YP#SKoYdyqkC{c9wW$X%SiTO2NpSP3Ky@2t*ED$9A@|vxotlqcsts29vV0l`}QH5Y1_Z!KeqgJzJgZW56E$ZWb{DV!iS`Mp!$-lx>0$`2f_PsRV8pzKNQ^;3a+AMx+P13!nr2STC20bCD246B(j2auc)Z3Or)D?!k*L9ZKfETdD!1l*>P58iQZca0P2@?{+b&v<D>fD`CBU+hNePj74v1vW{;fv&dbjSP{9|Tnoai#l{PcrCNao1=yyf7!wt35kUg>$|{&Z5UuMSgThLOQSV6$2u>K!rI_jkAerCZy;mCSwH`%;E~?QH$vR)7_c#Tfyv__I0&A=aru_zX;X3!;Y>{1035&#waXM7dBSqvyU6NFSkd#3LX@7vr1Rw&tq7$tRZvnJb*Oz_!V|%wiDS_z$LP&wemOTOS4Hy87@Nx`|7{!cVcQ5>gMbYdoa{42~LYQPsTkjB>4MWhj>$DSe#+y>q4F=d$To?_zoQ=dYr=;t}X75`SU2EX&c-YZd4;OT?$_`n^1q&gEinkty1Dhf`O{SlxMuQb?x$U7VGvQTR@k(<-#$nrrNdRuc;zq?2>56+mXaI`woQpo<dnjR31F0MA>KPfw1c*lCQOFA!ErC&Odm=(gBXJeaGvaBRmEpFa&TLaRO<n3}0?aI{Kg>%Ri-?ZsEoHT)Zek=+p$JEb3z+FU&uKnQkl4H)Fz?`#dQ9}Jm`rbD1$Q*JcFf*Rr~@moNlHyWK=y{9B}RFeC*CyHWxX;L;UP`9v(=fAFy|%{z*An4L0%y{%DB!9nlv7)%Ge}TjJCSAV)6noYuDb=rY`1DaEyQlmmm+I-0V%NPMFbt;-WYhSK96lf<$Q|#X~$naLgK7Llx?CeE5Y`te$JNs6cAB>s>=Qb!JMPQsROUN%ASNU=l<$A}X1umOZB|KW2*saZAo_&D+Qjq|$s{HxA)^2+`h3;y9yc9dDb6%LZ(s^p(<wGRFt<Q{dg;1_lB^RgFVYg41N~4uhSom4S=!?A#<CK|DlC@rju{r5KpE6_T9vDfAtfhO}q_hkOr})VG4l^C3w*g&?<7-%(cPJ^-Ez;Xw1^4c^nc7q<~E4@!C|r<~vg!<4pWX_C)&!;Z6htyC04BP7Q(^8;dr5*g5Q6@x|*#dbc){Q1q7tyZPMwMV_UqfE1k&ZBdULM|!*{fv8uD`pbnb2I|lzMX&nPj`cAwONS~j%IaHlSpy9%=w=Nf3dQ?EOd*dAYcy^SZWs#&zlcWMjl%hY7)Up&A{>;W*a_+;ehGRNuE%D4-(d-%ZJ=N18pHafPh!^RMR4&0}t}llxTT)K=|ddoZU+SR1vJJN3r4bAa24ndx*3MLaRwgG@8t3aWfg1y2X#GFqrPhOnfKiL{$sG9B{~Sy>q(QdJceck}Uvf79!Ml4m$MJY8{Tq_b0rp-iJTJ-AbrT@c1`t+-uDlP_WrqZlni14N=G~gJ41-(xkH>N~9RV?7>oiI~Z$eLZZ2cD52N^F#~06y+hSXp%BB9BzIm7OjJRPwAHm6r)mzS%_mX8KeMHF&mMzm!N4T%{Fb`jEjb_MWT58I_)OEOusy<74<TH-6;T}yJYw%|4<%Hp4S=^~>x^s{o2Cg#^-y`$1^G6+osFovK!iDGZJ0PB0a0aK2`n68D38z9+XjR{MRZXT{Qa!#xkx?T^UO`wQUs^TQ6M;ga8N1F90WiJl%1*(9sp@Juf}sQq8qnR2x1d71;TnGQEru#lb!ANCLjzd%t*ob8nfjo;-WLOczGRaJ3m@s;{Rwb<>`<R-W2x3kQ~)d)YFRMC0E5}M+`L*f}2rwPz5jDIFq^J;6y1hB7>3x4#h+(Dmdr|B*;wi=**WYxi#5Cl{$H#OC0w3y?{Kd&a6WE$uS;jrC%0iMIatfyaX5orS60x+iId_3^&Ok9%!AT4#v(tGWq$K2oD3`LfP59IJ_wB!R`gsV-)11ZE(kc{Y&v`Qej4t^Rg?k5Aon^@HGBOsMezxpFEW!oM1@sD4EKY3t)(VzuSRC`_iq{2t=v4cQtTK(h4~R%>)M}(tvq!iRT1UVGki-QP$&-2}n=50W^=f{-PH3SlnEbHX09S4cjPUu~Q!Ain~D@NDC5nl{C>-uN<m969}K2We6A4EP<qbA*P^6E(#zWcv|h4{(nI|e9AM58Gv%o2rg&Pm6zD+72>kFp!K5#QcA#iqZ5;E)B(D@i%9yXr!Kw`&19FSPAyr7sKT{hmYKN?&(ctSw0n8xM5weCb`QZ<HPv8EPT@ET@W{7-4hQqiN+qrnvf%V?PG2T-qC^}{OCT^ig>@<752nBW%X6SFPwDkkr4MqI7}Ap0T(zk+XNFxskRv%ZVM2gpCOj>ZVN>p4vb`6cvuY$YAkL=4CMW_hb~aVilRXlv23(I@C)IGKd*4~_*3-m}O8ibAmbA!@>?*CMUuy<JzDgAC@odmhZQL(u&&sXG@o^EqJ!9slG$|A;I0T-kkN*0}%2MZ_Bo6TVd@K7iP-=nFTIUObRd7jTc(5Maaq4$6rI1QoVil@M<^+JE*&#v*6SQ0fU)sR@(d-tpqU3uvY7jW#q1)M%d@NU9z*|^28ZVg?K25O<%$+F>Z8ad1`kOn<ok!-Z;Im8Z0TzKWquh>|SUIh$FnF-uS3`<VW!@NV6O@5PHl3O+L+7qF7P<pNaGa1?4(mV|##AcXVwrAqZi-5elQP{Kn8v7S_+PLH>^4(?=uSkr68;U(*TU#A9%ZbPnx4W}$rLE4b%cC;pbKRqlkz#kze#HFm_I^zUh9zu;rqjqkt_mIeyLW4mBgfMb?ekwD$k-$|NiJlq=<krH<7XZJr$A}zy<Uraa4bvVlwb0l~V9}%8Y?t&8x-O1rRiRUH|QH%j$?X8j>LUBRwL%YeSCJO1FeyK)~I069c9XtV=SK4V?5v>^0rI#HZW=paB@h*!Y6r-9_034)JR3HXISV`3;klZYfZ=x~&4CL5Df>z-S>#;;OZPT7r9k)GzP=*>)r|3XzM~vZq&q%aFJ@5*oR1m^R@&ovE1*;sqs|l@}WGZZg!AO_%~Q4n4jV)fT&Lw9ef_b%%~|X(E*G#_%c+Y~d*m#{jT0M7O^ZBVI^;$SP=<hj1!;OQtC9h-_9_qUJF?SpiIR7Wbo|Age{5fyPQm2Dqk_Yy|6F^PFZwH;h)#0*eC^z)~hCnp_<=mtbXA)N{Nj*&S3-31l6_5;Jxuxil)M1@-UOz}oq#Q@GU`a?}{5N?wwdU_&PESjUJ4u1ph`fQVenUN6)P;ppeymj(_$zg7iRkm<cFV5FSgM$_Nm55Xf~<?On|8q3PP*9Q`NIIJ&VGIr{@RFQ~5Io*ZDoNe$-=BR!7)GmO3hj`>N#ztmU{~YU|a_cC*FaUKyQ%<fel;~Tj?M+bYlEyK7NR@i!EDi<#hEQ_?ry(kzl>ADkF*k)wSWo3(fV2+tj~}5Psul&x;s`FB<EE5W=H<yF8NeWCx-lhm^ehEZVWt4d2<S9}43wkC(~d0U&*n|A2sPt8<R_@{{#oRH;;Hnqd9eK_>b@dmH-sVHX-mvP5^PEn%_@}`2Z)w9*04;&@nfykgl>~7(GY(r4JV5xVnd<man;eJmHe$Ss=fL5EWFd-e80?P%>q-)yCGr7pOJ_xc;rAppzdJ>!B|=}9BqPoF*>wr=@nx|RL*H@mC+d!E36B)vF#}z&g%|dUIimcU*$3w_fDnEf#W5b#hB)@bTOTzeQn^q-x2Mrcmv(svdBlEeaUe2v8o`OY%hv2J~jcyr+!she;GK_*?Wq!m6vUn&)le_&JK%`Wf8_V|J!ZS<IuqbS1@NKR0=iEsR-o$xT23I`0|<%=H@d=Jp!>v?HhU0ovKtdZjWGBTVSx}t4twaCa$9t&w9j6LVpmN&_uP5<Maz0?FgUt@20Kmkp+|Sac`+>*IWTEVs6yjD)pJT8LMwrHp#l33HCPL@kLE5FwUL<dcqbOtb}FNBP`-}yWh_2_OIUF+))JE&9pea%o>_ep5vM97_aeDrkU|P6NE#vIP6FeGbn=KJnU&EaQLt^`^_~f8f#2Pf>_j3OOS8q(JIbFuH!B-z>y<a#KZq$g=47%m<mCL7)5%#=&)vjUN+?{Ep-rZPL2+1sE@+N8}texTGb|9OrqRR%7vtVBT(``Vh685@ai0`yjBOpr?@2V(>3s#bQPXahzw5iPl;k7_4@<dgr`a%ByKXJf-wU46~;<-uGxgLLaU*kA2E70o+_Z28`0X#7Ns04t-11XK@@?LgtNMHNsu;xkQ@@F6Y%Q22Ae=Nt(RyDl{wuCgs(ZRyx4=Fi%RcTB9?bdnb^|~rY~VaQW{mtpP&IF$4z=rTtq}NX`mPZKOyVYzzKS5q?0IB92?WzB9+dKq^_C497ox$wyazUMM4wanz;!k3gR2hL)k(%3*WOz(M>H85^wDjI&WCEL~U8?(mg7SnH>Was3se5<1q9#gVqvi`~$#E=uz+v?i7<b>LAu9!3;iky+Y;;03o9jSY)<DoQp?W&@gX<5I<g;c0Y<>LGa=uP{W&>$w%mF72zudT*HPf+wY#hNzbUfI77MOU46~(yj(Fy91bZyM3(W9suKlo5tq1dB9~F97}Ei(0X`QRs{(Xj@nBOXCx2gY(0Em1rFRvKy}ar~Nje6eYh{uVr4aS4_0qjgi>6xst=ZgKNub*k+TDGcu9Chcyv`T~I12WqeIcO_Fo3ZN;}QZLpDQTXHBR9MEg5t>=^L@9U%jR~hZS|=Fa`co?H(9aHK(d)RV<oXK3eABR~Q!PUa0Rm!DaniQ0Aelo`|&X&Yn0aG7u!|BSfMWUw}WWXB&KRW)!7pP;1HO3S>IJyb-uffbGi(KJh1z8#UO?tB^1gB|csk!WvRtfz#a{F$})iZPu6v#Lx)h$Wgkt%1iN06sEn9_T=vtg^5s*z*g2|h1EUMaB>-8WaBW@q*_bmBX)Vm8lqheoUq0N5{giQ^#FR6E?`Ue=GkPUTu{Qx%hhD=;2_Y)as7y+K|rFYAf>%c5(^)tQ*PN25797-27%6j_XJ8zo86H!e*C)g*&WUcH%1U-#48%Bv~LRg8$?+-U@icV+3ZRygKlS>28louXBtCfnqC`zQCyH?C0#V9<-mkKsjh>CUBUu~jJHH($-7iufn(k+PqS-iynGicn&urnlqV<8bWU-iP@GyuyDp~gOf&kr%fC;>W3QY|ejo)eVIxf0;97d3P-|#dfmGJ+l1g^>SOi(Hj;<({E-ElVt|`Lkl#j7kMRLF@83x&_Lu8F5?wywRPzyEC6$QbF1&0O)&;}<h2r(G5PiX?n4s6CAPAW;QbJAzKiiM%(KV{)zL@tRbi#dAWDiH<&2wTx6MUj>GFm8~56FEA%XP#2+tTz~8mIK8{8BP<Lp_ZZ<@ol!v81;)cV1nGIin(DGQUDiL>76dzpklO?z8W}*(2HZ{g@wb2MUxzYB__&?l$LY1p=SUm`~Z?!jojf;r^b<e5tepcrgy9*4$_8dx%32&fJ|6mtN$LQlI_=K9+Yf%=&g=a8g=0(GiW;bBs?oQqPR}_gqDsYH4DYm7!v69vqhlW9l4v0i$#j0mR{gYHV*{W<6t^f$ajeHCB8!VZyeW5h8Eo}Q=;13vP6q)7Dy+ghEs$|XI#aOJi(pz!AlU?Sl}fd6>>qqH*4e3ivjQy0Y}P8KGbmH$&)85^Y`7=_09M3>AeHBefSWtZyzok-Ob~pRoy+l_e*y_drS&!o^E~7C&3$qQn>0;5Z6*g)HGjcA3FaJmzpUTI8Jy%z{wzd#tREX&!?T1(lnpTB1b$1EG=vK6PvSmQQ7Ca!0}XP>&v!dw+a7PQgp;c0VNx-U-o}2X(f1%D;#%Whw6PU3mh*Q6A^t}LYGtUS*@$Z%b<aN;Ua?1Xpw*VKfPe@0{')))
# The generic dead-stock heuristic considers future SALES only. It does not
# preserve wheat/fertilizer required by PICKUP/FEED/FERTILIZE, so it must be
# disabled for a new production route whose input contracts are not modeled.
_DEMO_IMPL = make_agent({0: _DEMO_TAPE}, dead_stock=False)
def agent(obs, config=None):
    return _DEMO_IMPL(obs, config)
agent.telemetry = _DEMO_IMPL.chassis.diagnostics
